"""Append-only, hash-chained record of every PROVE test.

Each entry stores the SHA-256 of the previous entry, so editing or deleting
any past result breaks verification from that point on. The export is an
evidence sheet per car that an owner can hand to an inspector. It is voluntary
documentation, not a code-compliance claim.
"""
import hashlib
import json

GENESIS = "0" * 64


def _canon(v):
    """Integral floats as ints, so the browser's JSON (which writes -60, not -60.0) hashes identically."""
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, dict):
        return {k: _canon(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_canon(x) for x in v]
    return v


def canonical_json(body):
    return json.dumps(_canon(body), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(body):
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


class EvidenceLedger:
    def __init__(self):
        self.entries = []

    @property
    def head(self):
        return self.entries[-1]["hash"] if self.entries else GENESIS

    def append(self, record):
        body = {"seq": len(self.entries), "prev": self.head, "record": record}
        entry = dict(body, hash=_digest(body))
        self.entries.append(entry)
        return entry

    def verify(self):
        """Returns (ok, first_bad_seq or None)."""
        prev = GENESIS
        for e in self.entries:
            body = {"seq": e["seq"], "prev": e["prev"], "record": e["record"]}
            if e["prev"] != prev or _digest(body) != e["hash"]:
                return False, e["seq"]
            prev = e["hash"]
        return True, None

    def evidence_sheet(self, car_id):
        rows = [e for e in self.entries if e["record"].get("car") == car_id]
        lines = [f"# PROVE evidence sheet: {car_id}", "",
                 "Voluntary test record. Not a code-compliance certificate.", "",
                 "| Night | Result | Downlink dB | Uplink dB | Label | Ticket | Entry hash |",
                 "|---|---|---:|---:|---|---|---|"]
        for e in rows:
            r = e["record"]
            lines.append(f"| {r.get('night')} | {r.get('result')} | {r.get('down_db', '')} | {r.get('up_db', '')} | "
                         f"{r.get('label', '')} | {r.get('ticket', '')} | `{e['hash'][:12]}` |")
        ok, bad = self.verify()
        lines += ["", f"Chain verified: {'yes' if ok else f'NO (broken at entry {bad})'}; head `{self.head[:16]}`"]
        return "\n".join(lines)
