"""Per-zone safety-margin learning (UCB1 multi-armed bandit).

Each hour, every zone picks how much head-room to add on top of the P90
forecast. Reward trades energy saved against congestion caused, so noisy
zones (venues, student centers) learn larger margins and predictable ones
(residence halls at night) learn to run lean.
"""
import math

ARMS = [0.0, 0.10, 0.25, 0.50]
CONGESTION_PENALTY = 0.6     # reward lost per congested 5-minute step


def reward(energy_ratio, congested_steps):
    """energy_ratio = Circadian kWh / always-on kWh for the epoch (lower is better)."""
    return max(-1.0, 1.0 - energy_ratio - CONGESTION_PENALTY * congested_steps)


class MarginBandit:
    def __init__(self, zones, c=0.35):
        self.c = c
        self.n = {z: [0] * len(ARMS) for z in zones}
        self.mean = {z: [0.0] * len(ARMS) for z in zones}
        self.current = {z: 1 for z in zones}

    def choose(self, zone):
        n, mean = self.n[zone], self.mean[zone]
        for i, k in enumerate(n):
            if k == 0:
                self.current[zone] = i
                return i
        total = sum(n)
        best = max(range(len(ARMS)), key=lambda i: mean[i] + self.c * math.sqrt(math.log(total) / n[i]))
        self.current[zone] = best
        return best

    def exploit(self, zone):
        n, mean = self.n[zone], self.mean[zone]
        tried = [i for i in range(len(ARMS)) if n[i]]
        return max(tried, key=lambda i: mean[i]) if tried else 1

    def update(self, zone, arm, r):
        self.n[zone][arm] += 1
        self.mean[zone][arm] += (r - self.mean[zone][arm]) / self.n[zone][arm]

    def margin(self, zone):
        return ARMS[self.current[zone]]

    def to_json(self):
        return {"n": self.n, "mean": self.mean}

    @classmethod
    def from_json(cls, data, c=0.35):
        b = cls(list(data["n"]), c)
        b.n = {k: list(v) for k, v in data["n"].items()}
        b.mean = {k: list(v) for k, v in data["mean"].items()}
        return b
