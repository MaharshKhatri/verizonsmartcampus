"""Plug-and-PROVE: the copper-replacement box proves itself at install and prints a receipt.

Verizon's Voice Connect / Business Phone Connect guide (BPC100) puts the
burden on the customer: "Compatibility is determined by your testing of your
alarm and/or medical device at time of install", the alarm number must be
keyed in (##21*number#), and backup is 3 AA batteries. Installs are done by
technicians today. This module runs the checks a technician would, through
the real voice path, and says whether a truck is still needed.

Thresholds are engineering assumptions, labeled; the Rutgers bench replaces
them with measured pass rates per device and per Verizon path.
"""
from dataclasses import dataclass, field

import numpy as np

from . import alarm

SUPPORTED_ALARM_FORMATS = {"contact_id"}         # BPC100 shop footnote: Contact ID only


@dataclass
class HomeSetup:
    devices: list = field(default_factory=lambda: ["phone", "alarm"])   # phone, alarm, medical, fax
    alarm_format: str = "contact_id"           # contact_id | sia | 4_2
    alarm_number_registered: bool = True       # ##21*number# entered and the box power-cycled
    medical_test_window: bool = False          # monitoring company agreed to a test signal
    batteries: bool = True
    battery_age_months: float = 0.0
    place: str = "window"                      # window | interior | basement
    corded_phone: bool = True                  # a cordless base dies with mains power


# Placement -> (RSRP dBm, SINR dB, voice-frame loss). ASSUMED illustrative values; measured per home in the pilot.
PLACES = {"window": (-92.0, 14.0, 0.005), "interior": (-104.0, 6.0, 0.02), "basement": (-116.0, 0.0, 0.06)}


def _alarm_check(setup, loss, rng):
    if setup.alarm_format not in SUPPORTED_ALARM_FORMATS:
        return ("FAIL", f"Alarm format {setup.alarm_format.upper()} is not supported on this box (Contact ID only)",
                "Ask the alarm company for a cellular communicator or switch the panel to Contact ID", True)
    path_kw = {"registered": setup.alarm_number_registered}
    ok = first = 0
    for _ in range(3):                                         # three test events, like a careful technician
        r = _alarm_call_with_loss(rng, loss, **path_kw)
        ok += r["delivered"]
        first += r["delivered"] and r["attempts"] == 1
    if not setup.alarm_number_registered:
        return ("FAIL", f"Alarm number not registered (##21): alarm calls ride the ordinary voice path "
                        f"(through on the first try {first}/3, delivered {ok}/3)",
                "Dial ##21*<alarm company number>#, power-cycle the box, re-run PROVE (fix sent by text)", False)
    if ok < 3:
        return ("FAIL", f"Kiss-off received {ok}/3 at this spot: signal too weak for alarm data",
                "Move the box 1 m toward a window and re-run", False)
    return ("OK", "Contact ID handshake and kiss-off received 3/3", "", False)


def _alarm_call_with_loss(rng, loss, registered=True):
    msg = alarm.contact_id()
    if registered:
        def path(s, r):
            y = alarm.alarm_path(s, r)
            frame = int(0.02 * alarm.FS)
            for i in range(0, len(y), frame):
                if r.random() < loss:
                    y[i:i + frame] = 0.0
            return y
    else:
        def path(s, r):
            return alarm.voice_path(s, r, loss=max(loss, 0.02))
    for attempt in range(1, 5):
        hs = path(alarm.handshake(), rng)
        if not (alarm.detect_tone(hs, 1400, 0.06) and alarm.detect_tone(hs, 2300, 0.06)):
            continue
        if alarm.checksum_ok(alarm.decode_dtmf(path(alarm.dtmf(msg), rng))) and \
                alarm.detect_tone(path(alarm.kissoff(), rng), 1400, 0.4):
            return {"delivered": True, "attempts": attempt}
    return {"delivered": False, "attempts": 4}


def install_proof(setup, seed=0):
    """Run every check; return the receipt lines and whether a truck is still needed."""
    rng = np.random.default_rng(seed)
    rsrp, sinr, loss = PLACES[setup.place]
    lines = []

    if sinr >= 10:
        lines.append(("SIGNAL", "OK", f"RSRP {rsrp:.0f} dBm, SINR {sinr:.0f} dB at this spot", "", False))
    elif sinr >= 3:
        lines.append(("SIGNAL", "WARN", f"RSRP {rsrp:.0f} dBm, SINR {sinr:.0f} dB: voice fine, alarm data marginal",
                      "Move the box toward a window if the alarm check fails", False))
    else:
        lines.append(("SIGNAL", "FAIL", f"RSRP {rsrp:.0f} dBm, SINR {sinr:.0f} dB: too weak here",
                      "Move the box to a window; if it still fails, a technician fits an external antenna", sinr < -3))

    voice_ok = loss < 0.05
    lines.append(("VOICE", "OK" if voice_ok else "WARN",
                  f"Two-way tone test, {loss * 100:.1f}% frames lost" + ("" if voice_ok else ": choppy"),
                  "" if voice_ok else "Move the box toward a window", False))

    if "alarm" in setup.devices:
        st, msg, fix, truck = _alarm_check(setup, loss, rng)
        lines.append(("ALARM", st, msg, fix, truck))
    if "medical" in setup.devices:
        if setup.medical_test_window:
            r = _alarm_call_with_loss(rng, loss, registered=True)
            lines.append(("MEDICAL", "OK" if r["delivered"] else "FAIL",
                          "Test signal acknowledged by the monitoring center" if r["delivered"] else "No acknowledgement",
                          "" if r["delivered"] else "Call the monitoring company; ask about a cellular PERS", False))
        else:
            lines.append(("MEDICAL", "WARN", "Not tested: no test window with the monitoring company",
                          "PROVE texts the monitoring company to book a 5-minute test window", False))
    if "fax" in setup.devices:
        ok = loss < 0.02
        lines.append(("FAX", "OK" if ok else "WARN", f"T.30 handshake at 9600 bps {'completed' if ok else 'retried'}",
                      "" if ok else "Set the fax to 9600 bps, ECM off (Verizon guide)", False))

    if not setup.batteries:
        lines.append(("BATTERY", "FAIL", "Box shut off when AC was pulled: no batteries",
                      "3 AA batteries mailed today; with them, about 23 h standby / 3 h talk", False))
    elif setup.battery_age_months >= 6:
        lines.append(("BATTERY", "WARN", f"Batteries {setup.battery_age_months:.0f} months old (guide: replace every 6)",
                      "Replacement AAs mailed", False))
    else:
        lines.append(("BATTERY", "OK", "Runs on battery when AC is pulled", "", False))
    if not setup.corded_phone:
        lines.append(("PHONE", "WARN", "Cordless base: it goes dead in a power cut even if the box is on battery",
                      "Keep one corded phone on the box", False))

    truck = any(t for *_, t in lines)
    fails = sum(s == "FAIL" for _, s, *_ in lines)
    verdict = "TRUCK NEEDED" if truck else ("FIX BY TEXT, THEN RE-RUN" if fails else "TRUCK NOT NEEDED")
    return {"lines": [{"check": c, "status": s, "detail": d, "fix": f, "needs_truck": t} for c, s, d, f, t in lines],
            "verdict": verdict, "place": setup.place}


SCENARIOS = {
    "all_good":        HomeSetup(),
    "unregistered":    HomeSetup(alarm_number_registered=False),       # e.g. after a box swap (to be confirmed on the bench)
    "sia_panel":       HomeSetup(alarm_format="sia"),
    "basement":        HomeSetup(place="basement"),
    "no_batteries":    HomeSetup(batteries=False),
    "medical_untested": HomeSetup(devices=["phone", "medical"]),
}


def scenarios():
    return {k: install_proof(v, seed=i) for i, (k, v) in enumerate(SCENARIOS.items())}


def receipt_text(res):
    out = ["PROVE · Voice Connect install check", "-" * 34]
    for ln in res["lines"]:
        out.append(f"{ln['check']:<8} {ln['status']:<4} {ln['detail']}")
        if ln["fix"]:
            out.append(f"{'':<14}-> {ln['fix']}")
    out += ["-" * 34, res["verdict"]]
    return "\n".join(out)


if __name__ == "__main__":
    for k, r in scenarios().items():
        print(f"\n## {k}\n{receipt_text(r)}")
