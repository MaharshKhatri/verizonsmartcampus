#!/usr/bin/env python3
"""Count spoken words in the video script's Audio column, per beat, with pace.

    python3 scripts/count_script_words.py deliverables/NOV8_VIDEO_PITCH_SCRIPT.md

Counts text inside straight or curly double quotes on each table row, split into
speakers and the handset line, and prints words per minute for each beat.
"""
import re
import sys


def beats(path):
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\|\s*(\d+):(\d\d)-(\d+):(\d\d)\s*\|(.*)\|(.*)\|\s*$", line)
        if not m:
            continue
        start = int(m[1]) * 60 + int(m[2])
        end = int(m[3]) * 60 + int(m[4])
        audio = m[6]
        quotes = re.findall(r"\*\*([^*]+):\*\*\s*\"([^\"]+)\"", audio)
        yield f"{m[1]}:{m[2]}-{m[3]}:{m[4]}", end - start, quotes


def count(text):
    return len([w for w in re.split(r"\s+", text.strip()) if re.search(r"\w", w)])


def main(path):
    total = {"spoken": 0, "handset": 0}
    for when, secs, quotes in beats(path):
        words = {"spoken": 0, "handset": 0}
        for who, text in quotes:
            words["handset" if who.strip().lower() == "handset" else "spoken"] += count(text)
        n = words["spoken"] + words["handset"]
        for k in total:
            total[k] += words[k]
        print(f"{when:>10}  {secs:>3d} s  spoken {words['spoken']:>3d}  handset {words['handset']:>2d}  "
              f"{(60 * n / secs if secs else 0):5.0f} wpm")
    print(f"total spoken {total['spoken']} + handset {total['handset']} = {sum(total.values())}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
