"""
config.py
Central configuration for PROTOCOL_SINGULARITY_v3.1.
All tunable parameters live here. No magic numbers in engine code.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationConfig:
    """[MEASURED STATE] Immutable simulation parameters."""
    # Core stability
    max_stability: float = 100.0
    threshold: float = 10.0
    alpha: float = 10.0          # stability recovery rate

    # Shield
    max_shield_energy: float = 50.0
    shield_integrity: float = 1.0   # 0.0 to 1.0
    gamma: float = 12.0             # shield energy recharge rate
    integrity_recharge: float = 0.03  # shield integrity repair per tick
    heavy_hit_threshold: float = 0.7   # fraction of max_shield
    medium_hit_threshold: float = 0.4  # fraction of max_shield
    breach_threshold: float = 1.2    # threat / (energy + integrity*max) > this triggers breach

    # Mode modifiers
    fortress_efficiency_mult: float = 1.5
    fortress_energy_cost_mult: float = 1.3
    fortress_stability_drain: float = 2.0
    evasive_efficiency_mult: float = 0.6
    evasive_energy_cost_mult: float = 0.7
    evasive_stability_bonus: float = 3.0

    # Reboot
    max_reboots: int = 2
    reboot_penalty_pct: float = 20.0

    # Repair
    repair_chance: float = 20.0
    repair_amount: float = 10.0

    # Threat
    threat_low: float = 30.0
    threat_high: float = 95.0

    # RNG
    rng_seed: Optional[int] = 42