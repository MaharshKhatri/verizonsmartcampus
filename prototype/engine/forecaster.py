"""Context-aware occupancy forecaster (the "one forecast" behind every action).

For each zone kind and horizon h (5..60 min) a ridge regression maps context
features to future occupancy:

  1  bias
  2  registrar / event-calendar prior at t+h
  3  observed occupancy now
  4  deviation of now from the prior (today's attendance level)
  5  prior at t+h scaled by today's observed/prior ratio
  6  passengers already on buses heading to this zone (lead indicator)
  7  short-term trend (obs now - obs 5 minutes ago)

It is retrained nightly on the last HISTORY_DAYS of telemetry. Uncertainty is
an empirical 90th-percentile relative residual per (kind, h), which the
controllers use as a P90 demand envelope.
"""
import json
import os

from . import campus
from .config import HORIZON_STEPS, STEPS_PER_DAY

N_FEAT = 7
RIDGE = 1e-3


def _scale(zone, prior_total):
    return max(float(zone.peak), max(prior_total), 200.0)


def bus_shares(prior_occ):
    """share[z][t]: fraction of a campus's expected arrivals at step t that go to zone z."""
    shares = {z.key: [0.0] * STEPS_PER_DAY for z in campus.ZONES}
    for c in ("busch", "livingston"):
        zs = [z for z in campus.ZONES if z.campus == c and z.kind in ("academic", "student_center", "venue")]
        for t in range(1, STEPS_PER_DAY):
            incs = {z.key: max(0.0, prior_occ[z.key]["total"][t] - prior_occ[z.key]["total"][t - 1]) for z in zs}
            tot = sum(incs.values())
            if tot > 0:
                for k, v in incs.items():
                    shares[k][t] = v / tot
    return shares


class DayView:
    """Everything the forecaster may look at for one day (no ground truth)."""

    def __init__(self, prior_occ, obs, bus_tele):
        self.prior = {k: v["total"] for k, v in prior_occ.items()}
        self.obs = obs
        self.bus = bus_tele
        self.shares = bus_shares(prior_occ)
        self.scale = {z.key: _scale(z, self.prior[z.key]) for z in campus.ZONES}

    def features(self, zone, t, h):
        zk = zone.key
        sc = self.scale[zk]
        pri, obs = self.prior[zk], self.obs[zk]
        s = min(t + h, STEPS_PER_DAY - 1)
        p_s, p_t = pri[s] / sc, pri[t] / sc
        y_t = obs[t] / sc
        y_prev = obs[t - 1] / sc if t > 0 else y_t
        ratio = (y_t + 0.02) / (p_t + 0.02)
        ratio = 0.3 if ratio < 0.3 else (3.0 if ratio > 3.0 else ratio)
        bus = 0.0
        if h <= len(self.bus[zone.campus][t]):
            bus = self.bus[zone.campus][t][h - 1] * self.shares[zk][s] / sc
        return (1.0, p_s, y_t, y_t - p_t, ratio * p_s, bus, y_t - y_prev)


def _solve(a, b):
    """Gaussian elimination with partial pivoting for a small dense system."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        d = m[col][col]
        if abs(d) < 1e-12:
            continue
        for r in range(n):
            if r != col:
                f = m[r][col] / d
                if f:
                    for c in range(col, n + 1):
                        m[r][c] -= f * m[col][c]
    return [m[i][n] / m[i][i] if abs(m[i][i]) > 1e-12 else 0.0 for i in range(n)]


class Forecaster:
    def __init__(self):
        self.coef = {}   # (kind, h) -> weights
        self.q90 = {}    # (kind, h) -> relative residual quantile

    # ---- training -------------------------------------------------------
    def fit(self, views):
        kinds = sorted({z.kind for z in campus.ZONES})
        acc = {(k, h): ([[0.0] * N_FEAT for _ in range(N_FEAT)], [0.0] * N_FEAT, 0)
               for k in kinds for h in range(1, HORIZON_STEPS + 1)}
        for v in views:
            for zone in campus.ZONES:
                obs = v.obs[zone.key]
                sc = v.scale[zone.key]
                for t in range(1, STEPS_PER_DAY - 1):
                    for h in range(1, HORIZON_STEPS + 1):
                        s = t + h
                        if s >= STEPS_PER_DAY:
                            break
                        x = v.features(zone, t, h)
                        y = obs[s] / sc
                        xtx, xty, n = acc[(zone.kind, h)]
                        for i in range(N_FEAT):
                            xi = x[i]
                            if xi == 0.0:
                                continue
                            row = xtx[i]
                            for j in range(i, N_FEAT):
                                row[j] += xi * x[j]
                            xty[i] += xi * y
                        acc[(zone.kind, h)] = (xtx, xty, n + 1)
        for key, (xtx, xty, n) in acc.items():
            for i in range(N_FEAT):
                for j in range(i):
                    xtx[i][j] = xtx[j][i]
                xtx[i][i] += RIDGE * max(n, 1)
            self.coef[key] = _solve(xtx, xty)
        self._fit_quantiles(views)
        return self

    def _fit_quantiles(self, views, q=0.90):
        resid = {key: [] for key in self.coef}
        for v in views:
            for zone in campus.ZONES:
                obs = v.obs[zone.key]
                sc = v.scale[zone.key]
                for t in range(1, STEPS_PER_DAY - 1, 2):
                    for h in range(1, HORIZON_STEPS + 1):
                        s = t + h
                        if s >= STEPS_PER_DAY:
                            break
                        yhat = max(0.0, _dot(self.coef[(zone.kind, h)], v.features(zone, t, h)))
                        resid[(zone.kind, h)].append((obs[s] / sc - yhat) / (yhat + 0.03))
        for key, rs in resid.items():
            rs.sort()
            self.q90[key] = rs[int(q * (len(rs) - 1))] if rs else 0.25

    # ---- inference ------------------------------------------------------
    def predict(self, view, zone, t):
        """[(p50_people, p90_people)] for h = 1..HORIZON_STEPS made with data up to step t."""
        sc = view.scale[zone.key]
        out = []
        for h in range(1, HORIZON_STEPS + 1):
            yhat = max(0.0, _dot(self.coef[(zone.kind, h)], view.features(zone, t, h)))
            p90 = yhat + max(0.0, self.q90[(zone.kind, h)]) * (yhat + 0.03)
            out.append((yhat * sc, p90 * sc))
        return out

    # ---- persistence ----------------------------------------------------
    def to_json(self):
        return {"coef": {f"{k}|{h}": w for (k, h), w in self.coef.items()},
                "q90": {f"{k}|{h}": q for (k, h), q in self.q90.items()}}

    @classmethod
    def from_json(cls, data):
        f = cls()
        for key, w in data["coef"].items():
            k, h = key.split("|")
            f.coef[(k, int(h))] = w
        for key, q in data["q90"].items():
            k, h = key.split("|")
            f.q90[(k, int(h))] = q
        return f

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            json.dump(self.to_json(), fh)

    @classmethod
    def load(cls, path):
        with open(path) as fh:
            return cls.from_json(json.load(fh))


def _dot(w, x):
    return sum(a * b for a, b in zip(w, x))


def evaluate(forecaster, view, horizon, truth=None):
    """Normalised MAE of the model vs simple baselines on one day.

    Scored against telemetry by default (what a deployed system can measure), or
    against ground truth when `truth` ({zone: [people]}) is given.
      persistence  the next h steps look like now
      timetable    registrar/event prior alone
      ratio_rule   prior x today's observed/prior ratio (no learning)
    """
    errs = {"model": 0.0, "persistence": 0.0, "timetable": 0.0, "ratio_rule": 0.0}
    n = 0
    for zone in campus.ZONES:
        sc = view.scale[zone.key]
        obs, pri = view.obs[zone.key], view.prior[zone.key]
        target = truth[zone.key] if truth else obs
        for t in range(1, STEPS_PER_DAY - horizon):
            y = target[t + horizon]
            p50 = forecaster.predict(view, zone, t)[horizon - 1][0]
            ratio = (obs[t] + 0.02 * sc) / (pri[t] + 0.02 * sc)
            ratio = min(3.0, max(0.3, ratio))
            errs["model"] += abs(p50 - y) / sc
            errs["persistence"] += abs(obs[t] - y) / sc
            errs["timetable"] += abs(pri[t + horizon] - y) / sc
            errs["ratio_rule"] += abs(pri[t + horizon] * ratio - y) / sc
            n += 1
    return {k: v / n for k, v in errs.items()}


class HistoryForecaster:
    """Traffic-history baseline - what today's AI energy-saving apps see.

    It forecasts each zone's measured traffic from the average of past days of
    the same type (weekday / saturday / finals), scaled by how today compares
    so far. No timetable, event calendar or bus data: RAN KPIs only.
    """

    def __init__(self):
        self.profile = {}   # day_type -> zone -> [mean Mbps per step]
        self.q90 = {}       # (kind, h) -> relative residual quantile

    def fit(self, typed_views):
        groups = {}
        for day_type, view in typed_views:
            groups.setdefault(day_type, []).append(view)
        for day_type, views in groups.items():
            self.profile[day_type] = {
                z.key: [sum(v.dem_obs[z.key][t] for v in views) / len(views) for t in range(STEPS_PER_DAY)]
                for z in campus.ZONES}
        resid = {}
        for day_type, view in typed_views:
            for zone in campus.ZONES:
                floor = 0.03 * max(self.profile[day_type][zone.key]) + 1.0
                for t in range(1, STEPS_PER_DAY - 1, 2):
                    preds = self._p50(view, day_type, zone, t)
                    for h, yhat in enumerate(preds, start=1):
                        s = t + h
                        if s >= STEPS_PER_DAY:
                            break
                        resid.setdefault((zone.kind, h), []).append(
                            (view.dem_obs[zone.key][s] - yhat) / (yhat + floor))
        for key, rs in resid.items():
            rs.sort()
            self.q90[key] = rs[int(0.9 * (len(rs) - 1))]
        return self

    def _p50(self, view, day_type, zone, t):
        prof = self.profile.get(day_type) or self.profile["weekday"]
        hist = prof[zone.key]
        now = view.dem_obs[zone.key][t]
        r = (now + 5.0) / (hist[t] + 5.0)
        r = 0.5 if r < 0.5 else (2.0 if r > 2.0 else r)
        out = []
        for h in range(1, HORIZON_STEPS + 1):
            s = min(t + h, STEPS_PER_DAY - 1)
            out.append(max(0.0, hist[s] * (1.0 + (r - 1.0) * 0.8 ** h)))
        return out

    def predict(self, view, day_type, zone, t):
        """[(p50_mbps, p90_mbps)] for h = 1..HORIZON_STEPS."""
        prof = self.profile.get(day_type) or self.profile["weekday"]
        floor = 0.03 * max(prof[zone.key]) + 1.0
        return [(y, y + max(0.0, self.q90.get((zone.kind, h), 0.3)) * (y + floor))
                for h, y in enumerate(self._p50(view, day_type, zone, t), start=1)]

    def to_json(self):
        return {"profile": self.profile, "q90": {f"{k}|{h}": q for (k, h), q in self.q90.items()}}

    @classmethod
    def from_json(cls, data):
        f = cls()
        f.profile = data["profile"]
        for key, q in data["q90"].items():
            k, h = key.split("|")
            f.q90[(k, int(h))] = q
        return f
