"""Zero-truck-roll fault triage.

Status quo: alarms and customer complaints reach a NOC queue; soft faults
that carry no clean alarm often end in "no fault found" dispatches.

Circadian: the digital twin knows each radio's *intended* state (including
intentional sleep), so it compares expected vs. measured service and
diagnoses with a naive-Bayes model over symptoms, then runs a remote
playbook. Only hardware faults dispatch a truck - with the right part.
"""
import random
from dataclasses import dataclass

FAULTS = {
    #               kind    capacity  label
    "software_hang": ("soft", 0.0, "Baseband software hang"),
    "config_drift": ("soft", 0.5, "Parameter drift after software upgrade"),
    "beam_misalignment": ("soft", 0.3, "mmWave beam misalignment (wind / foliage)"),
    "backhaul_flap": ("soft", 0.4, "Fiber backhaul flapping (micro-bend)"),
    "pa_failure": ("hard", 0.0, "Power-amplifier failure"),
    "psu_failure": ("hard", 0.0, "Rectifier / power-supply failure"),
}

SYMPTOMS = ["power_zero", "static_no_traffic", "hw_alarm", "beam_rsrp_drop", "backhaul_loss", "partial_kpi"]
LIKELIHOOD = {   # P(symptom present | fault)
    "software_hang":     [0.02, 0.92, 0.10, 0.05, 0.05, 0.05],
    "config_drift":      [0.01, 0.05, 0.05, 0.20, 0.05, 0.90],
    "beam_misalignment": [0.01, 0.05, 0.05, 0.90, 0.05, 0.80],
    "backhaul_flap":     [0.01, 0.30, 0.20, 0.05, 0.92, 0.60],
    "pa_failure":        [0.05, 0.40, 0.90, 0.30, 0.05, 0.10],
    "psu_failure":       [0.95, 0.02, 0.85, 0.05, 0.05, 0.02],
}
PLAYBOOK = {
    "software_hang": ("Remote baseband restart via O1", 0.97),
    "config_drift": ("Roll back to last-known-good config", 0.95),
    "beam_misalignment": ("Re-weight beams + recalibrate from crowd-sourced RSRP map", 0.85),
    "backhaul_flap": ("Reroute over redundant path, open fiber ticket only if persistent", 0.70),
}

# Status-quo NOC (est: industry benchmarks; see research/01 and research/04)
SQ_DETECT = {"software_hang": 3, "config_drift": 12, "beam_misalignment": 9, "backhaul_flap": 4,
             "pa_failure": 2, "psu_failure": 1}
SQ_TRUCK_PROB = {"software_hang": 0.25, "config_drift": 0.50, "beam_misalignment": 0.70, "backhaul_flap": 0.60,
                 "pa_failure": 1.0, "psu_failure": 1.0}
SQ_REPEAT_PROB = {"soft": 0.20, "hard": 0.20}
SQ_REMOTE_STEPS, SQ_TRUCK_STEPS, REPEAT_EXTRA_STEPS = 6, 36, 24
CI_DETECT, CI_REMOTE_STEPS, CI_TRUCK_STEPS, CI_REPEAT_PROB = 1, 2, 30, 0.05
# Cell-outage compensation (3GPP SON): neighbours re-tilt / raise power to cover
# part of a failed cell's load until the technician arrives (est).
COMPENSATION_SHARE = 0.35
COMPENSATION_W = 150.0


@dataclass
class FaultCase:
    asset_id: str
    zone: str
    ftype: str
    start: int
    repaired_at: int
    trucks: int
    tickets: int
    diagnosis: str = ""
    action: str = ""


def diagnose(true_fault, rng):
    """Sample symptoms for the true fault, return the MAP diagnosis and its posterior."""
    obs = [rng.random() < p for p in LIKELIHOOD[true_fault]]
    post = {}
    for f, lik in LIKELIHOOD.items():
        p = 1.0
        for present, q in zip(obs, lik):
            p *= q if present else (1.0 - q)
        post[f] = p
    total = sum(post.values()) or 1.0
    best = max(post, key=post.get)
    return best, post[best] / total, [s for s, o in zip(SYMPTOMS, obs) if o]


def status_quo(asset_id, zone, ftype, start, rng):
    kind = FAULTS[ftype][0]
    detect = start + SQ_DETECT[ftype]
    tickets = 1                                   # NOC ticket
    if rng.random() < SQ_TRUCK_PROB[ftype]:
        trucks = 1
        end = detect + SQ_TRUCK_STEPS
        if rng.random() < SQ_REPEAT_PROB[kind]:
            trucks += 1
            end += REPEAT_EXTRA_STEPS
        action = "dispatch technician"
    else:
        trucks, end, action = 0, detect + SQ_REMOTE_STEPS, "manual remote fix"
    return FaultCase(asset_id, zone, ftype, start, end, trucks, tickets, "", action)


def circadian(asset_id, zone, ftype, start, rng):
    kind = FAULTS[ftype][0]
    detect = start + CI_DETECT
    guess, confidence, symptoms = diagnose(ftype, rng)
    if FAULTS[guess][0] == "soft" and guess in PLAYBOOK:
        action, p_ok = PLAYBOOK[guess]
        if guess == ftype and rng.random() < p_ok:
            return FaultCase(asset_id, zone, ftype, start, detect + CI_REMOTE_STEPS, 0, 0,
                             f"{guess} ({confidence:.0%}; {', '.join(symptoms) or 'no symptoms'})", action)
        # wrong diagnosis or the playbook failed -> escalate with full context
        trucks = 1
        end = detect + CI_REMOTE_STEPS + CI_TRUCK_STEPS
        return FaultCase(asset_id, zone, ftype, start, end, trucks, 1,
                         f"{guess} ({confidence:.0%})", f"{action} failed -> pre-diagnosed dispatch")
    trucks = 1 + (1 if rng.random() < CI_REPEAT_PROB else 0)
    end = detect + CI_TRUCK_STEPS + (REPEAT_EXTRA_STEPS if trucks > 1 else 0)
    return FaultCase(asset_id, zone, ftype, start, end, trucks, 1 if kind == "hard" else 0,
                     f"{guess} ({confidence:.0%})", "cell-outage compensation + dispatch with the right part")


def accuracy(trials=2000, seed=7):
    """Diagnosis accuracy over random faults (used by tests and the Q&A bible)."""
    rng = random.Random(seed)
    names = list(FAULTS)
    ok = 0
    for _ in range(trials):
        f = rng.choice(names)
        ok += diagnose(f, rng)[0] == f
    return ok / trials


def storm_monte_carlo(faults, n=2000):
    """Distribution of outcomes for one fault list over n random draws (dispatch, repeat-visit
    and remote-fix probabilities are assumptions; this shows what they imply, not a measurement)."""
    sq_t, ci_t, sq_m, ci_m = [], [], [], []
    for seed in range(n):
        r1, r2 = random.Random(seed * 3 + 1), random.Random(seed * 5 + 2)
        sq = [status_quo(a, a.split("-")[0], f, s, r1) for s, a, f in sorted(faults)]
        ci = [circadian(a, a.split("-")[0], f, s, r2) for s, a, f in sorted(faults)]
        sq_t.append(sum(c.trucks for c in sq))
        ci_t.append(sum(c.trucks for c in ci))
        sq_m.append(sum(c.repaired_at - c.start for c in sq) * 5)
        ci_m.append(sum(c.repaired_at - c.start for c in ci) * 5)
    mean = lambda xs: sum(xs) / len(xs)
    return {"draws": n, "faults": len(faults), "trucks_status_quo": round(mean(sq_t), 2),
            "trucks_circadian": round(mean(ci_t), 2),
            "dispatch_avoided_share": round((mean(sq_t) - mean(ci_t)) / mean(sq_t), 3) if mean(sq_t) else 0.0,
            "p_no_gain": round(sum(1 for a, b in zip(sq_t, ci_t) if b >= a) / n, 3),
            "outage_min_status_quo": round(mean(sq_m)), "outage_min_circadian": round(mean(ci_m))}


def robust_accuracy(perturb=0.15, trials=4000, seed=1):
    """Diagnosis accuracy when real symptom rates differ from the model's table by up to +/-perturb."""
    rng = random.Random(seed)
    true_lik = {f: [min(.99, max(.01, q + rng.uniform(-perturb, perturb))) for q in v] for f, v in LIKELIHOOD.items()}
    names, ok = list(FAULTS), 0
    for _ in range(trials):
        f = rng.choice(names)
        obs = [rng.random() < p for p in true_lik[f]]
        post = {}
        for g, lik in LIKELIHOOD.items():
            p = 1.0
            for o, q in zip(obs, lik):
                p *= q if o else 1 - q
            post[g] = p
        ok += max(post, key=post.get) == f
    return ok / trials
