"""Live mode for the command center (standard library only).

    python3 prototype/server.py            # then open http://localhost:8765

Serves the dashboard and a small JSON API so judges can inject their own
chaos (a surprise crowd, a radio fault) or type a slice request in plain
English. Every call re-simulates the day deterministically, so everything
before the injection time is unchanged and the AI's response is real.

  GET  /api/health
  POST /api/run      {"scenario": "weekday", "injections": [{"type": "crowd", "zone": "BSC", "t": 170,
                      "crowd": 2500, "duration": 12}, {"type": "fault", "asset": "HILL-cband-1", "t": 150,
                      "fault": "pa_failure"}, {"type": "slice", "text": "..."}]}
  POST /api/intent   {"text": "...", "scenario": "gameday"}
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from prototype.engine import demand, sim, slicing  # noqa: E402

DASHBOARD = os.path.join(ROOT, "prototype", "dashboard")
MODEL = sim.load_or_train()
MAX_INJECTIONS = 12


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[circadian] " + fmt % args + "\n")

    def _json(self, code, payload):
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            return self._json(200, {"ok": True, "scenarios": list(sim.SCENARIOS)})
        return super().do_GET()

    def do_POST(self):
        try:
            length = min(int(self.headers.get("Content-Length", 0)), 64_000)
            req = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "invalid JSON"})
        scenario = req.get("scenario", "weekday")
        if scenario not in sim.SCENARIOS:
            return self._json(400, {"error": f"unknown scenario {scenario!r}"})
        if self.path == "/api/run":
            injections = req.get("injections", [])[:MAX_INJECTIONS]
            try:
                trace = sim.simulate(scenario, injections=injections, model=MODEL)
            except (KeyError, ValueError, TypeError) as exc:
                return self._json(400, {"error": f"bad injection: {exc}"})
            return self._json(200, trace)
        if self.path == "/api/intent":
            text = str(req.get("text", ""))[:500]
            day, _ = sim.make_scenario_day(scenario)
            prior = demand.occupancy(day, truth=False)
            res = slicing.admit(slicing.parse(text, day.games), prior)
            res["text"] = text
            return self._json(200, res)
        return self._json(404, {"error": "not found"})


def main():
    port = int(os.environ.get("PORT", "8765"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Circadian command center: http://localhost:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
