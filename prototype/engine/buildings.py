"""Campus HVAC model: fixed timetable (today) vs forecast-driven conditioning (Circadian).

Same occupancy forecast that sleeps radios also sets back empty buildings,
pre-conditions them 30 minutes before the crowd arrives, and scales
ventilation with headcount (demand-controlled ventilation).
"""
from .config import (HVAC_PRECONDITION_STEPS, HVAC_SETBACK_FACTOR, HVAC_VENT_SHARE, HVAC_W_PER_SQFT,
                     STEP_MIN)

SCHEDULED = ("academic", "library", "student_center", "dining", "rec")
EMPTY_FRACTION = 0.03        # below 3% of peak (or 15 people) a zone counts as empty
DR_CURTAIL_FACTOR = 0.75     # +3 F setpoint during a demand-response event
DR_PRECOOL_FACTOR = 1.10
DR_PRECOOL_STEPS = 24        # pre-cool for 2 hours before the event


def _design_kw(zone, weather):
    return zone.sqft * HVAC_W_PER_SQFT[weather] / 1000.0


def _kw(zone, weather, conditioned, vent_factor):
    base = _design_kw(zone, weather)
    if not conditioned:
        return base * HVAC_SETBACK_FACTOR
    return base * ((1.0 - HVAC_VENT_SHARE) + HVAC_VENT_SHARE * vent_factor)


# Venue zones include parking lots and plazas: condition the building only once a
# real share of the crowd is inside (tailgaters don't need the concourse cooled).
VENUE_EMPTY = 0.25           # share of seating capacity
VENUE_SEATS = {"SHI": 52_454, "ARENA": 8_000}


def _empty_threshold(zone):
    if zone.kind == "venue":
        return VENUE_EMPTY * VENUE_SEATS.get(zone.key, 1000)
    return max(15.0, EMPTY_FRACTION * max(zone.peak, 1))


def baseline_kw(zone, weather, t, day, people):
    """Timetable-driven building automation, as a facilities team would schedule it:
    weekdays 06:00-23:00; weekends and announced closures run academic buildings in
    setback and other buildings 08:00-22:00; finals week keeps libraries and student
    centers open around the clock; venues follow the event calendar. Design ventilation."""
    minute = t * STEP_MIN
    if zone.kind == "residence":
        conditioned = True
    elif zone.kind == "venue":
        conditioned = any(g.zone == zone.key and -240 <= minute - g.kickoff * STEP_MIN <= 300 for g in day.games)
    elif day.day_type in ("saturday", "cancelled"):
        conditioned = zone.kind != "academic" and 8 * 60 <= minute < 22 * 60
    elif day.day_type == "finals" and zone.kind in ("library", "student_center"):
        conditioned = True
    else:
        conditioned = 6 * 60 <= minute < 23 * 60
    kw = _kw(zone, weather, conditioned, 1.0)
    miss = people if (not conditioned and people > _empty_threshold(zone)) else 0.0
    return kw, conditioned, miss


RECOVERY_STEPS = 3           # a room needs ~15 minutes after setback before it is comfortable


class CircadianHVAC:
    """Forecast-driven HVAC. Called with an empty forecast it becomes a purely reactive
    occupancy controller (condition only once people are measured), which is how the
    evidence isolates what the forecast itself buys. dcv=False disables ventilation by
    headcount, to separate ventilation savings from setback savings."""

    def __init__(self, dcv=True):
        self.dcv = dcv
        self.conditioned = {}
        self.recovery = {}
        self.on_since = {}

    def step(self, zone, weather, t, people_now, fc_p90, dr_window=None, people_true=None):
        """Decide from telemetry (people_now) and the forecast; score comfort against ground truth.

        fc_p90: list of P90 people forecasts for the next steps. Returns (kw, conditioned, miss, note),
        where miss counts people actually present in a room that is in setback or still recovering.
        """
        thr = _empty_threshold(zone)
        soon = max(fc_p90[:HVAC_PRECONDITION_STEPS]) if fc_p90 else 0.0
        was = self.conditioned.get(zone.key, True)
        note = None
        if zone.kind == "residence":
            conditioned = True
        else:
            conditioned = people_now > thr or soon > thr
            if conditioned and not was:
                self.recovery[zone.key] = 2
                self.on_since[zone.key] = t
                note = "pre-condition: forecast arrival within 30 min"
            elif not conditioned and was:
                note = "setback: P90 forecast empty for 30 min"
        self.conditioned[zone.key] = conditioned

        occ_frac = min(1.0, max(people_now, soon * 0.6) / max(zone.peak, people_now, 1.0))
        vent = max(0.40 if zone.kind == "residence" else 0.25, occ_frac) if self.dcv else 1.0
        kw = _kw(zone, weather, conditioned, vent)
        if self.recovery.get(zone.key, 0) > 0:
            kw *= 1.15                                    # recovery load after setback
            self.recovery[zone.key] -= 1

        if dr_window and zone.kind != "residence":
            start, end = dr_window
            if start <= t < end:
                kw *= DR_CURTAIL_FACTOR
            elif start - DR_PRECOOL_STEPS <= t < start and conditioned:
                kw *= DR_PRECOOL_FACTOR
        present = people_now if people_true is None else people_true
        recovering = conditioned and t - self.on_since.get(zone.key, -99) < RECOVERY_STEPS
        miss = present if ((not conditioned or recovering) and present > thr) else 0.0
        return kw, conditioned, miss, note
