"""SAME ANSWER: a before-and-after receipt for every lifeline that leaves copper.

Before the cutover, record what the line does today on copper. After it, run
the same checks on Verizon's replacement path and diff the two:
  - the number the device dials (alarm receiver, elevator answering service)
  - the calling number it presents (answering centers often look up the
    building and car by caller ID; a new number can make the screen show
    UNKNOWN or the wrong city, the pattern in Chicago's Oct 9, 2026 citation)
  - who picks up (person / voicemail / IVR / intercept), and how fast
  - the location the answerer sees
  - for alarms: whether the receiver acknowledged (kiss-off), first try
  - signal margin at the box, judged on its worst season
The receipt is a timestamped test record, not a guarantee.
"""
from dataclasses import dataclass, field, replace

import numpy as np

from . import answer
from .install import _alarm_call_with_loss, PLACES, LEAF_ON_MARGIN_DB

LOCATION_BY_CALLER_ID = {          # what the answering center's screen shows, keyed by calling number
    "7324451000": "Hill Center, Car 2",
    "7324452000": "Busch Student Center, Car 1",
}


@dataclass
class LineState:
    kind: str = "elevator"            # elevator | alarm
    dials: str = "7329327211"         # number the device dials
    caller_id: str = "7324451000"     # number presented to the answerer
    answerer: str = "person"          # person | voicemail | ivr | intercept
    ring_s: float = 12.0
    alarm_registered: bool = True     # alarm calls take the alarm-optimized path on the box
    place: str = "window"
    canopy: bool = False
    path: str = "copper"              # copper | verizon_box


def observe(s, rng):
    """Run the checks on a line state; returns the observed profile."""
    out = {"dials": s.dials, "caller_id": s.caller_id}
    if s.kind == "elevator":
        reg = answer.Registry(answerer_number=s.dials, label=LOCATION_BY_CALLER_ID.get("7324451000"))
        shown = LOCATION_BY_CALLER_ID.get(s.caller_id, "UNKNOWN CALLER")
        r = answer.check_call(s.dials, s.answerer, s.ring_s, shown, reg, rng)
        out.update(answered_by=r["answered_by"], ring_s=r["ring_s"], location_shown=shown)
    else:
        loss = 0.0 if s.path == "copper" else PLACES[s.place][2]
        res = [_alarm_call_with_loss(rng, loss, registered=(s.path == "copper" or s.alarm_registered)) for _ in range(3)]
        out.update(alarm_ack=f"{sum(r['delivered'] for r in res)}/3",
                   alarm_first_try=f"{sum(r['delivered'] and r['attempts'] == 1 for r in res)}/3")
    if s.path == "verizon_box":
        sinr = PLACES[s.place][1] - (LEAF_ON_MARGIN_DB if s.canopy else 0.0)
        out["signal_worst_season_sinr_db"] = round(sinr, 1)
    return out


OWNER = {"dials": "elevator contractor / alarm company (dialing program)",
         "caller_id": "Verizon provisioning (calling number) + answering service (lookup table)",
         "answered_by": "answering service", "ring_s": "answering service",
         "location_shown": "answering service lookup + Verizon calling number",
         "alarm_ack": "Verizon (alarm path) + alarm company", "alarm_first_try": "Verizon (alarm path / signal)",
         "signal_worst_season_sinr_db": "customer (placement) or Verizon (antenna)"}


def receipt(before, after, label="Hill Center, Car 2"):
    lines, same = [], True
    for k in ("dials", "caller_id", "answered_by", "ring_s", "location_shown", "alarm_ack", "alarm_first_try"):
        if k not in before and k not in after:
            continue
        b, a = before.get(k), after.get(k)
        changed = b != a
        if k == "ring_s" and isinstance(a, (int, float)):
            changed = a > answer.REDIRECT_S and (b is None or b <= answer.REDIRECT_S)
        if k == "caller_id" and changed and after.get("location_shown") == before.get("location_shown"):
            changed = False                     # a new number is fine if the answerer still sees the right place
        lines.append({"check": k, "before": b, "after": a, "status": "CHANGED" if changed else "SAME",
                      "owner": OWNER[k] if changed else ""})
        same &= not changed
    sinr = after.get("signal_worst_season_sinr_db")
    if sinr is not None:
        st = "OK" if sinr >= 10 else ("MARGINAL" if sinr >= 3 else "FAIL")
        lines.append({"check": "signal_worst_season_sinr_db", "before": "copper", "after": sinr, "status": st,
                      "owner": OWNER["signal_worst_season_sinr_db"] if st != "OK" else ""})
        same &= st == "OK"
    return {"label": label, "lines": lines, "verdict": "SAME ANSWER" if same else "CHANGED: FIX BEFORE COPPER IS CUT"}


def cutover(before_state, after_state, seed=0):
    rng = np.random.default_rng(seed)
    return receipt(observe(before_state, rng), observe(after_state, rng))


SCENARIOS = {
    "elevator_same": (LineState(), replace(LineState(), path="verizon_box")),
    "elevator_new_caller_id": (LineState(), replace(LineState(), path="verizon_box", caller_id="7325550143")),
    "elevator_voicemail": (LineState(), replace(LineState(), path="verizon_box", answerer="voicemail", ring_s=22)),
    "alarm_same": (LineState(kind="alarm"), LineState(kind="alarm", path="verizon_box")),
    "alarm_unregistered": (LineState(kind="alarm"), LineState(kind="alarm", path="verizon_box", alarm_registered=False)),
    "alarm_basement_trees": (LineState(kind="alarm"), LineState(kind="alarm", path="verizon_box", place="interior", canopy=True)),
}


def scenarios():
    return {k: cutover(b, a, seed=i) for i, (k, (b, a)) in enumerate(SCENARIOS.items())}


if __name__ == "__main__":
    import json
    for k, r in scenarios().items():
        print(k, r["verdict"])
        for ln in r["lines"]:
            print("   ", ln)
