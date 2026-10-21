"""PROVE console, live mode (standard library + numpy).

    python3 -m prototype.prove.server          # then open http://localhost:8766

The rig buttons flip one flag on the demo car and run a real test through the
acoustic model, triage and ledger. On the physical rig, the same endpoints are
fed by the Pi supervisor instead of the model.

  GET  /api/health
  GET  /api/state
  POST /api/rig     {"antenna": false, "mic_taped": true, ...}   flags to set
  POST /api/test    run tonight's test now
  POST /api/help    HELP pressed: label as data, voice call, text mode
  GET  /api/ledger  last entries + verification
  POST /api/reset
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from prototype.prove import supervisor  # noqa: E402

CONSOLE = os.path.join(HERE, "console")
PORT = int(os.environ.get("PROVE_PORT", "8766"))

RIG_FLAGS = {"antenna": bool, "mains": bool, "gateway_ok": bool, "answer_point_ok": bool, "on_copper": bool,
             "reported_label": str}
CAR_FLAGS = {"speaker_gain": float, "mic_gain": float, "mic_taped": bool, "noise_level": float, "packet_loss": float}

SUP = supervisor.Supervisor()


def apply_flags(sup, req):
    for k, typ in RIG_FLAGS.items():
        if k in req:
            setattr(sup.rig, k, None if req[k] is None else typ(req[k]))
    for k, typ in CAR_FLAGS.items():
        if k in req:
            v = typ(req[k])
            if typ is float:
                v = max(0.0, min(v, 1.0))
            setattr(sup.rig.car, k, v)
    if "mains" in req:
        sup.rig.battery_hours = 24.0 if sup.rig.mains else 2.0


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CONSOLE, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[prove] " + fmt % args + "\n")

    def _json(self, code, payload):
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            return self._json(200, {"ok": True, "mode": "live-model"})
        if self.path == "/api/state":
            return self._json(200, SUP.state())
        if self.path == "/api/ledger":
            ok, bad = SUP.ledger.verify()
            return self._json(200, {"entries": SUP.ledger.entries[-12:], "length": len(SUP.ledger.entries),
                                    "verified": ok, "broken_at": bad})
        return super().do_GET()

    def do_POST(self):
        global SUP
        try:
            length = min(int(self.headers.get("Content-Length", 0)), 16_000)
            req = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "invalid JSON"})
        if self.path == "/api/rig":
            try:
                apply_flags(SUP, req)
            except (TypeError, ValueError) as e:
                return self._json(400, {"error": str(e)})
            return self._json(200, SUP.state())
        if self.path == "/api/test":
            return self._json(200, SUP.run_test())
        if self.path == "/api/help":
            return self._json(200, SUP.help_pressed())
        if self.path == "/api/reset":
            SUP = supervisor.Supervisor()
            return self._json(200, SUP.state())
        return self._json(404, {"error": "unknown endpoint"})


def main():
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"PROVE console on http://localhost:{PORT}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
