"""
protocol_engine/telemetry/events.py
[DERIVED STATE] Immutable causal event structures.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Tuple
from protocol_engine.types import EventTier, SystemState


@dataclass(frozen=True)
class EventLog:
    """[DERIVED STATE] Immutable causal event with shield telemetry."""
    tick: int
    tier: EventTier
    event_type: str
    state_before: SystemState
    state_after: SystemState
    stability_before: float
    stability_after: float
    shield_energy_before: float
    shield_energy_after: float
    shield_integrity_before: float
    shield_integrity_after: float
    max_stability_before: float
    max_stability_after: float
    metadata: Tuple[Tuple[str, Any], ...] = field(default_factory=tuple)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tick": self.tick,
            "tier": self.tier.name,
            "event_type": self.event_type,
            "state_before": self.state_before.name,
            "state_after": self.state_after.name,
            "stability_delta": round(self.stability_after - self.stability_before, 2),
            "shield_energy_delta": round(self.shield_energy_after - self.shield_energy_before, 2),
            "shield_integrity_delta": round(self.shield_integrity_after - self.shield_integrity_before, 3),
            "max_stability_delta": round(self.max_stability_after - self.max_stability_before, 2),
            "metadata": dict(self.metadata),
        }
