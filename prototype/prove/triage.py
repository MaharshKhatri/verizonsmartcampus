"""PROVE fault triage: from nightly symptoms to a cause and an owner.

Same naive-Bayes approach as the Circadian network triage (prototype/engine/
triage.py), retargeted: the faults are the ways an emergency phone path breaks,
and every diagnosis routes a ticket to whoever can fix it. Likelihoods are
engineering assumptions, labeled as such, to be replaced with pilot data.
"""
import math
import random

FAULTS = {
    #                 owner                                   label
    "rf":             ("Verizon (RF / network)",               "Cellular signal or attach failure"),
    "power":          ("Facilities (electrician)",             "Mains lost; gateway on battery"),
    "gateway":        ("Verizon / certified partner",          "POTS gateway hung or failed"),
    "speaker":        ("Elevator contractor",                  "Car speaker dead or damaged"),
    "mic":            ("Elevator contractor",                  "Car microphone dead or obstructed"),
    "answer_point":   ("RUPD dispatch / answering point",      "Call connected but nobody answered"),
    "label":          ("Provisioning (Verizon + OIT)",         "Location label wrong after migration"),
}
PRIOR = {"rf": 0.20, "power": 0.12, "gateway": 0.12, "speaker": 0.15, "mic": 0.20, "answer_point": 0.11, "label": 0.10}

SYMPTOMS = ["heartbeat_lost", "rsrp_low", "attach_fail", "mains_lost", "battery_low", "call_setup_fail",
            "down_fail", "up_fail", "up_hf_loss", "no_answer", "label_mismatch"]
# P(symptom observed | fault). Assumptions; see module docstring.
LIKELIHOOD = {
    "rf":           [0.60, 0.85, 0.70, 0.02, 0.02, 0.90, 0.90, 0.90, 0.05, 0.05, 0.02],
    "power":        [0.30, 0.05, 0.10, 0.95, 0.60, 0.40, 0.40, 0.40, 0.02, 0.02, 0.02],
    "gateway":      [0.80, 0.05, 0.30, 0.02, 0.02, 0.95, 0.95, 0.95, 0.02, 0.02, 0.02],
    "speaker":      [0.02, 0.05, 0.02, 0.02, 0.02, 0.02, 0.97, 0.03, 0.02, 0.02, 0.02],
    "mic":          [0.02, 0.05, 0.02, 0.02, 0.02, 0.02, 0.03, 0.97, 0.40, 0.02, 0.02],
    "answer_point": [0.02, 0.05, 0.02, 0.02, 0.02, 0.05, 0.03, 0.03, 0.02, 0.95, 0.05],
    "label":        [0.02, 0.05, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.05, 0.97],
}


def posterior(observed, likelihood=None):
    """observed: set of symptom names. Returns {fault: probability}."""
    lk = likelihood or LIKELIHOOD
    logp = {}
    for f, ps in lk.items():
        s = math.log(PRIOR[f])
        for sym, p in zip(SYMPTOMS, ps):
            s += math.log(p if sym in observed else 1 - p)
        logp[f] = s
    m = max(logp.values())
    z = sum(math.exp(v - m) for v in logp.values())
    return {f: math.exp(v - m) / z for f, v in logp.items()}


def diagnose(observed):
    post = posterior(observed)
    best = max(post, key=post.get)
    owner, label = FAULTS[best]
    return {"fault": best, "confidence": round(post[best], 3), "owner": owner, "label": label,
            "symptoms": sorted(observed)}


def sample_symptoms(fault, rng, likelihood=None):
    lk = likelihood or LIKELIHOOD
    return {s for s, p in zip(SYMPTOMS, lk[fault]) if rng.random() < p}


def accuracy(trials=4000, seed=5, perturb=0.0):
    """Routing accuracy on simulated faults. perturb>0 draws symptoms from a
    likelihood table that differs from the one the classifier assumes."""
    rng = random.Random(seed)
    truth_lk = LIKELIHOOD
    if perturb:
        truth_lk = {f: [min(0.99, max(0.01, p + rng.uniform(-perturb, perturb))) for p in ps]
                    for f, ps in LIKELIHOOD.items()}
    faults, weights = zip(*PRIOR.items())
    ok = owner_ok = 0
    for _ in range(trials):
        f = rng.choices(faults, weights)[0]
        d = diagnose(sample_symptoms(f, rng, truth_lk))
        ok += d["fault"] == f
        owner_ok += FAULTS[d["fault"]][0] == FAULTS[f][0]
    return {"fault_accuracy": round(ok / trials, 3), "owner_accuracy": round(owner_ok / trials, 3)}
