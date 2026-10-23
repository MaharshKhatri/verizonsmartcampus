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
import textwrap
from dataclasses import dataclass, field

import numpy as np

from . import alarm, tap

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
    month: int = 11                            # install month (leaf-off Nov-Apr in NJ)
    canopy: bool = False                       # deciduous trees between the box and the site
    signal_source: str = "box"                 # box (its own reading) | phone (a phone near the box, a proxy)


# Placement -> (RSRP dBm, SINR dB, voice-frame loss). ASSUMED illustrative values; measured per home in the pilot.
PLACES = {"window": (-92.0, 14.0, 0.005), "interior": (-104.0, 6.0, 0.02), "basement": (-116.0, 0.0, 0.06)}
LEAF_ON_MARGIN_DB = 3.0    # ASSUMED; NTIA/ITS measured 1.8-2.9 dB more summer clutter loss at 3.475 GHz (Kozma et al., 2024)


SOURCES = {"SIGNAL": {"box": "SIGNAL (box reading)", "phone": "SIGNAL (phone near box, proxy)"},
           "VOICE": "VOICE (call to PROVE test responder)", "ALARM": "ALARM (line tap)"}
GAP_S = 0.25               # panel's pause after the handshake and before the kiss-off, as in tap.synth_call


def _confirm_s(attempts, msg=None):
    """Handshake start to kiss-off start for a call confirmed on `attempts` (tap.synth_call's timing)."""
    hs, block = len(alarm.handshake()) / alarm.FS, len(alarm.dtmf(msg or alarm.contact_id())) / alarm.FS
    return hs + GAP_S + attempts * block + (attempts - 1) * tap.RETRY_WAIT_S + GAP_S


def _alarm_check(setup, loss, rng, events=3):
    if setup.alarm_format not in SUPPORTED_ALARM_FORMATS:
        return ("FAIL", f"Alarm format {setup.alarm_format.upper()} is not supported on this box (Contact ID only)",
                "Ask the alarm company for a cellular communicator or switch the panel to Contact ID", True)
    path_kw = {"registered": setup.alarm_number_registered}
    ok = first = 0
    tries = []
    for _ in range(events):                                    # three test events, like a careful technician
        r = _alarm_call_with_loss(rng, loss, **path_kw)
        ok += r["delivered"]
        first += r["delivered"] and r["attempts"] == 1
        tries.append(r["attempts"])
    if not setup.alarm_number_registered:
        return ("FAIL", f"Alarm number not registered (##21): alarm calls ride the ordinary voice path "
                        f"(through on the first try {first}/{events}, confirmed {ok}/{events})",
                "Re-enter the alarm company number (##21*number#), restart the box, press PROVE again", False)
    if ok < events:
        got = f"confirmation came back only {ok}/{events}" if events > 1 else "no confirmation came back"
        return ("FAIL", f"Panel sent its code; {got} at this spot: signal too weak for alarm data",
                "Try the box nearer a window, as Verizon's guide suggests, then run the alarm test again", False)
    if first < ok:                                             # got through, but only after the panel retried
        return ("WARN", f"Receiver picked up · full code sent · confirmed only after retries "
                        f"(first try {first}/{events}): little signal margin for alarm data here",
                "Try the box nearer a window, then run the alarm test again", False)
    done = f"confirmed {ok}/{events}" if events > 1 else f"confirmed in {_confirm_s(tries[0]):.1f} s"
    return ("OK", f"Receiver picked up · full code sent · {done}", "", False)


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


def install_proof(setup, seed=0, alarm_events=3, sources=False):
    """Run every check; return the receipt lines and whether a truck is still needed.

    alarm_events: test alarm events to run (1 gives "confirmed in X.X s", 3 "confirmed 3/3").
    sources=True: each line also names where its reading came from (SOURCES).
    """
    rng = np.random.default_rng(seed)
    rsrp, sinr, loss = PLACES[setup.place]
    lines = []

    leaf_off = setup.month in (11, 12, 1, 2, 3, 4)
    seasonal = setup.canopy and leaf_off
    worst = sinr - LEAF_ON_MARGIN_DB if seasonal else sinr        # judge the spot on its worst season
    note = f"; about {worst:.0f} dB when the leaves return" if seasonal else ""
    if worst >= 10:
        lines.append(("SIGNAL", "OK", f"RSRP {rsrp:.0f} dBm, SINR {sinr:.0f} dB at this spot{note}", "", False))
    elif worst >= 3:
        lines.append(("SIGNAL", "WARN", f"RSRP {rsrp:.0f} dBm, SINR {sinr:.0f} dB{note}: voice fine, alarm data marginal",
                      "Move the box toward a window" + (" before the leaves return" if seasonal else "")
                      + "; PROVE re-checks nightly", False))
    else:
        lines.append(("SIGNAL", "FAIL", f"RSRP {rsrp:.0f} dBm, SINR {sinr:.0f} dB{note}: too weak here",
                      "Move the box to a window; if it still fails, a technician fits an external antenna", worst < -3))

    voice_ok = loss < 0.05
    lines.append(("VOICE", "OK" if voice_ok else "WARN",
                  f"Two-way tone test, {loss * 100:.1f}% frames lost" + ("" if voice_ok else ": choppy"),
                  "" if voice_ok else "Move the box toward a window", False))

    if "alarm" in setup.devices:
        st, msg, fix, truck = _alarm_check(setup, loss, rng, alarm_events)
        lines.append(("ALARM", st, msg, fix, truck))
    if "medical" in setup.devices:
        if setup.medical_test_window:
            r = _alarm_call_with_loss(rng, loss, registered=True)
            lines.append(("MEDICAL", "OK" if r["delivered"] else "FAIL",
                          "Test signal acknowledged by the monitoring center" if r["delivered"] else "No acknowledgement",
                          "" if r["delivered"] else "Call the monitoring company; ask about a cellular PERS", False))
        else:
            lines.append(("MEDICAL", "WARN", "Not tested: no test window with the monitoring company",
                          "Book a 5-minute test window with the monitoring company, then re-run", False))
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
        lines.append(("BATTERY", "OK", "Installed · keeps working when unplugged", "", False))
    if not setup.corded_phone:
        lines.append(("PHONE", "WARN", "Cordless base: it goes dead in a power cut even if the box is on battery",
                      "Keep one corded phone on the box", False))

    truck = any(t for *_, t in lines)
    # a life-safety line is green only if signal, alarm and battery are all clean
    fixes = sum(s == "FAIL" or (s == "WARN" and c in ("SIGNAL", "ALARM", "BATTERY")) for c, s, *_ in lines)
    verdict = "VISIT NEEDED" if truck else ("FIX AND RE-RUN" if fixes else "GREEN: all checks passed · no visit requested")
    out = [{"check": c, "status": s, "detail": d, "fix": f, "needs_truck": t} for c, s, d, f, t in lines]
    if sources:
        for ln in out:
            src = SOURCES.get(ln["check"], ln["check"])
            ln["source"] = src[setup.signal_source] if isinstance(src, dict) else src
    return {"lines": out, "verdict": verdict, "place": setup.place}


SCENARIOS = {
    "all_good":        HomeSetup(),
    "unregistered":    HomeSetup(alarm_number_registered=False),       # e.g. after a box swap (to be confirmed on the bench)
    "sia_panel":       HomeSetup(alarm_format="sia"),
    "basement":        HomeSetup(place="basement"),
    "no_batteries":    HomeSetup(batteries=False),
    "medical_untested": HomeSetup(devices=["phone", "medical"]),
    "leaf_off_trees":  HomeSetup(place="interior", canopy=True),
}


def scenarios():
    return {k: install_proof(v, seed=i) for i, (k, v) in enumerate(SCENARIOS.items())}


def _wrap(text, width, first="", rest=""):
    """Lines of at most `width` columns: break after ' · ' where a part fits, else between words."""
    parts = text.split(" · ")
    atoms = []
    for i, part in enumerate(parts):
        part += " ·" if i < len(parts) - 1 else ""
        room = width - len(first if i == 0 else rest)
        atoms += [part] if len(part) <= room else [w for word in part.split()
                                                    for w in textwrap.wrap(word, width - max(len(first), len(rest)))]
    lines = [""]
    for a in atoms:
        lead = first if len(lines) == 1 else rest
        if lines[-1] and len(lead) + len(lines[-1]) + 1 + len(a) > width:
            lines.append(a)
        else:
            lines[-1] = f"{lines[-1]} {a}" if lines[-1] else a
    return [(first if i == 0 else rest) + ln for i, ln in enumerate(lines)]


def receipt_text(res, width=None):
    """Printed test record. width=None: the original layout; width=32: a thermal-printer roll."""
    if width is None:
        out = ["PROVE · test record", "-" * 34]
        for ln in res["lines"]:
            out.append(f"{ln.get('source', ln['check']):<8} {ln['status']:<4} {ln['detail']}")
            if ln["fix"]:
                out.append(f"{'':<14}-> {ln['fix']}")
        out += ["-" * 34, res["verdict"], "Test record, not a guarantee."]
        return "\n".join(out)
    pad = " " * 5
    out = _wrap("PROVE · test record", width) + ["-" * width]
    for ln in res["lines"]:
        out += _wrap(ln.get("source", ln["check"]), width, f"{ln['status']:<4} ", pad)
        out += _wrap(ln["detail"], width, pad, pad)
        if ln["fix"]:
            out += _wrap(ln["fix"], width, pad + "-> ", pad + "   ")
    v = res["verdict"]
    out += ["-" * width] + _wrap(v, width, "", " " * (v.index(": ") + 2 if ": " in v else 0))
    return "\n".join(out + _wrap("Test record, not a guarantee.", width))


if __name__ == "__main__":
    for k, r in scenarios().items():
        print(f"\n## {k}\n{receipt_text(r)}")
