"""
protocol_engine/simulation/shield.py
[MEASURED STATE] Active shield absorption, degradation, and recharge.
"""
from typing import Dict, Any
from protocol_engine.types import ShieldMode


def compute_shield_absorption(
    threat: float,
    shield_energy: float,
    shield_integrity: float,
    max_shield_energy: float,
    mode: ShieldMode,
    config,
) -> Dict[str, Any]:
    """
    [MEASURED STATE] Active shield absorption with mode-dependent efficiency.
    """
    # Base efficiency from integrity (0.5 to 1.0)
    efficiency = 0.5 + (shield_integrity * 0.5)

    # Mode modifiers
    if mode == ShieldMode.FORTRESS:
        efficiency *= config.fortress_efficiency_mult
        energy_cost_mult = config.fortress_energy_cost_mult
    elif mode == ShieldMode.EVASIVE:
        efficiency *= config.evasive_efficiency_mult
        energy_cost_mult = config.evasive_energy_cost_mult
    else:
        energy_cost_mult = 1.0

    # Compute absorption
    raw_absorbed = threat * efficiency
    actual_absorbed = min(shield_energy, raw_absorbed)
    residual = threat - actual_absorbed

    # Energy cost — capped to available energy
    energy_cost = min(shield_energy, actual_absorbed * energy_cost_mult)

    # Integrity damage from hit magnitude
    hit_ratio = threat / max_shield_energy if max_shield_energy > 0 else 0.0
    if hit_ratio > config.heavy_hit_threshold:
        integrity_damage = 0.08
    elif hit_ratio > config.medium_hit_threshold:
        integrity_damage = 0.03
    else:
        integrity_damage = 0.0

    # Breach: threat massively exceeds shield capacity
    shield_capacity = shield_energy + (shield_integrity * max_shield_energy * 0.5)
    breach = threat > shield_capacity * config.breach_threshold
    if breach:
        residual = threat * 0.35  # 35% leaks through after breach
        integrity_damage += 0.15
        energy_cost = shield_energy  # Fully drained

    return {
        "absorbed": actual_absorbed,
        "residual": residual,
        "energy_cost": energy_cost,
        "integrity_damage": integrity_damage,
        "breach": breach,
        "efficiency": efficiency,
    }


def compute_shield_recharge(
    shield_energy: float,
    shield_integrity: float,
    max_shield_energy: float,
    config,
) -> Dict[str, Any]:
    """
    [MEASURED STATE] Dual recharge: energy + integrity.
    """
    new_energy = min(max_shield_energy, shield_energy + config.gamma)
    new_integrity = min(1.0, shield_integrity + config.integrity_recharge)

    return {
        "energy_gained": new_energy - shield_energy,
        "integrity_gained": new_integrity - shield_integrity,
        "new_energy": new_energy,
        "new_integrity": new_integrity,
    }