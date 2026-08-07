"""
protocol_engine/simulation/threat.py
[MEASURED STATE] Threat generation.
"""
import random


class ThreatGenerator:
    """Encapsulates threat generation strategy."""

    def __init__(self, rng: random.Random, low: float, high: float):
        self._rng = rng
        self.low = low
        self.high = high

    def next(self) -> float:
        return round(self._rng.uniform(self.low, self.high), 1)