#!/usr/bin/env python3
"""Rebuild everything: train the model (if stale), run all scenarios, compute the
evidence, run the CFO model, and write the dashboard data bundle.

    python3 scripts/build_all.py [--retrain]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from prototype.engine import export  # noqa: E402

if __name__ == "__main__":
    export.build(retrain="--retrain" in sys.argv)
    print("Open prototype/dashboard/index.html, or run: python3 prototype/server.py")
