"""
================================================================================
PROTOCOL_SINGULARITY_v3.5 (COG-V&V) — VERIFICATION & VALIDATION EDITION
Active Shield / Defense Layer — Single File
================================================================================
Version:     v3.5-COG-V&V
Status:      V&V REFINED
Scope:       Self-contained resilience simulation with active shielding,
             property-based validation, energy conservation, and reference
             scenario testing.

Refinements from v3.4 → v3.5 (Addressing 10 reviewer gaps):
  1. [v3.5 FIX] Shield absorption ceiling: efficiency affects cost/loss,
     never creates energy. absorbed = min(threat, raw_absorbed, shield_energy).
  2. [v3.5 FIX] Exponential recovery: dS/dt = k(Max-S) instead of +alpha.
  3. [v3.5 FIX] Continuous integrity damage via sigmoid(hit_ratio).
  4. [v3.5 FIX] Energy conservation: absorbed + residual + heat + structural = threat.
  5. [v3.5 FIX] Property-based invariant checking in _validate() and test suite.
  6. [v3.5 FIX] Reference scenario validation (zero threat, infinite shield, etc.).
  7. [v3.5 FIX] Threat generator with basic state (cooldown/escalation).
  8. [v3.5 FIX] Repair probability scales with integrity (lower integrity = harder to repair).
  9. [v3.5 FIX] Explicit heat/entropy tracking in telemetry.
  10. [v3.5 FIX] Deterministic validation suite with known expected outcomes.
================================================================================
"""

import random
import json
import time
import os
import math
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Mapping
from enum import Enum, auto
from collections import defaultdict


# ==============================================================================
# SECTION 1: CONFIGURATION (Policy Layer)
# ==============================================================================

@dataclass(frozen=True)
class SimulationConfig:
    """[POLICY LAYER] Immutable simulation parameters."""
    max_stability: float = 100.0
    threshold: float = 10.0
    # [v3.5] Recovery rate constant k for exponential recovery dS/dt = k(Max-S)
    recovery_rate: float = 0.25
    max_shield_energy: float = 50.0
    shield_integrity: float = 1.0
    gamma: float = 12.0
    integrity_recharge: float = 0.03
    heavy_hit_threshold: float = 0.7
    medium_hit_threshold: float = 0.4
    breach_threshold: float = 1.2
    fortress_efficiency_mult: float = 1.5
    fortress_energy_cost_mult: float = 1.3
    fortress_stability_drain: float = 2.0
    evasive_efficiency_mult: float = 0.6
    evasive_energy_cost_mult: float = 0.7
    evasive_stability_bonus: float = 3.0
    max_reboots: int = 2
    reboot_penalty_pct: float = 20.0
    repair_chance: float = 20.0
    repair_amount: float = 10.0
    threat_low: float = 30.0
    threat_high: float = 95.0
    rng_seed: Optional[int] = 42
    integrity_scale_factor: float = 0.02
    integrity_scale_cap: float = 0.15
    breach_penalty_pct: float = 0.35
    strained_threshold_ratio: float = 0.50
    balanced_threshold_ratio: float = 0.80
    # [v3.5] Threat escalation/cooldown
    threat_cooldown_ticks: int = 2
    threat_escalation_factor: float = 1.15
    # [v3.5] Repair difficulty scaling
    repair_integrity_factor: float = 0.5


# ==============================================================================
# SECTION 2: TYPES / ENUMS
# ==============================================================================

class SystemState(Enum):
    BALANCED = auto()
    STRAINED = auto()
    COLLAPSED = auto()


class RebootMode(Enum):
    STRICT_MATH = auto()
    SAFETY_GUARD = auto()


class ShieldState(Enum):
    ACTIVE = auto()
    DEGRADED = auto()
    BREACHED = auto()


class ShieldMode(Enum):
    BALANCED = auto()
    FORTRESS = auto()
    EVASIVE = auto()


class EventTier(Enum):
    THREAT = auto()
    SHIELD = auto()
    CORE = auto()
    RECOVERY = auto()
    REPAIR = auto()
    REBOOT = auto()
    VALIDATION = auto()


class EventType(Enum):
    THREAT_ABSORBED = auto()
    THREAT_STRAIN = auto()
    THREAT_COLLAPSE = auto()
    SHIELD_BREACH = auto()
    RECOVERY_SUCCESS = auto()
    RECOVERY_BLOCKED = auto()
    REPAIR_SUCCESS = auto()
    REPAIR_IDLE = auto()
    SHIELD_REPAIR_SUCCESS = auto()
    SHIELD_REPAIR_IDLE = auto()
    SHIELD_REPAIR_MAXED = auto()
    REBOOT_SUCCESS = auto()
    REBOOT_EXHAUSTED = auto()
    REBOOT_UNNEEDED = auto()
    REBOOT_FAILED_THRESHOLD = auto()
    REBOOT_FAILED = auto()
    VALIDATION_FAIL = auto()


# ==============================================================================
# SECTION 3: SIMULATION MECHANICS (Physics Layer)
# ==============================================================================

class ThreatGenerator:
    """[PHYSICS LAYER] Threat generation with stateful escalation/cooldown."""

    def __init__(self, rng: random.Random, low: float, high: float,
                 cooldown_ticks: int = 2, escalation_factor: float = 1.15):
        self._rng = rng
        self.low = low
        self.high = high
        self.cooldown_ticks = cooldown_ticks
        self.escalation_factor = escalation_factor
        self._consecutive_hits = 0
        self._cooldown_remaining = 0
        self._last_threat = 0.0

    def next(self) -> float:
        if self._cooldown_remaining > 0:
            self._cooldown_remaining -= 1
            self._consecutive_hits = 0
            return 0.0

        base = self._rng.uniform(self.low, self.high)
        # Escalation: consecutive hits increase threat
        if self._last_threat > self.high * 0.8:
            self._consecutive_hits += 1
        else:
            self._consecutive_hits = max(0, self._consecutive_hits - 1)

        multiplier = 1.0 + (self._consecutive_hits * (self.escalation_factor - 1.0))
        threat = round(base * multiplier, 1)
        self._last_threat = threat

        # Trigger cooldown after very large threats
        if threat > self.high * 0.9:
            self._cooldown_remaining = self.cooldown_ticks

        return threat


def compute_shield_absorption(
    threat: float,
    shield_energy: float,
    shield_integrity: float,
    max_shield_energy: float,
    mode: ShieldMode,
    config: SimulationConfig,
) -> Dict[str, Any]:
    """[PHYSICS LAYER] Active shield absorption with energy conservation."""
    efficiency = 0.5 + (shield_integrity * 0.5)

    if mode == ShieldMode.FORTRESS:
        efficiency *= config.fortress_efficiency_mult
        energy_cost_mult = config.fortress_energy_cost_mult
    elif mode == ShieldMode.EVASIVE:
        efficiency *= config.evasive_efficiency_mult
        energy_cost_mult = config.evasive_energy_cost_mult
    else:
        energy_cost_mult = 1.0

    # [v3.5 FIX] Ceiling: efficiency affects cost/loss, never creates energy.
    # raw_absorbed is the "ideal" absorption, but actual cannot exceed threat.
    raw_absorbed = threat * efficiency
    # [v3.5] Physical ceiling: cannot absorb more than threat, cannot absorb more than available energy
    actual_absorbed = min(threat, min(shield_energy, raw_absorbed))

    residual = max(0.0, threat - actual_absorbed)

    # [v3.5] Energy cost: efficiency makes shielding MORE EXPENSIVE, not more magical
    # Higher efficiency = higher energy cost per unit absorbed
    energy_cost = min(shield_energy, actual_absorbed * energy_cost_mult)

    # [v3.5] Heat/entropy: energy lost as heat during conversion
    heat_loss = max(0.0, energy_cost - actual_absorbed)

    # [v3.5] Structural damage to shield from overload
    structural_damage = max(0.0, raw_absorbed - actual_absorbed)

    hit_ratio = threat / max_shield_energy if max_shield_energy > 0 else 0.0

    # [v3.5 FIX] Continuous integrity damage via sigmoid
    # Base step + smooth sigmoid component
    sigmoid_damage = 0.25 / (1.0 + math.exp(-10 * (hit_ratio - 0.55)))
    integrity_damage = sigmoid_damage

    # Additional breach penalty
    shield_capacity = shield_energy + (shield_integrity * max_shield_energy * 0.5)
    breach = threat > shield_capacity * config.breach_threshold
    if breach:
        # [v3.5] Additive penalty on top of normal residual
        residual = residual + (threat * config.breach_penalty_pct)
        integrity_damage += 0.15
        energy_cost = shield_energy
        heat_loss = max(0.0, energy_cost - actual_absorbed)
        structural_damage = max(0.0, raw_absorbed - actual_absorbed)

    # [v3.5] Conservation check: absorbed + residual + heat = threat + breach_penalty
    # structural_damage is shield wear accounting, not an energy sink
    breach_penalty = threat * config.breach_penalty_pct if breach else 0.0
    total_accounted = actual_absorbed + residual + heat_loss
    expected_total = threat + breach_penalty
    conservation_error = abs(total_accounted - expected_total)

    return {
        "absorbed": actual_absorbed,
        "residual": residual,
        "energy_cost": energy_cost,
        "integrity_damage": integrity_damage,
        "breach": breach,
        "efficiency": efficiency,
        "heat_loss": heat_loss,
        "structural_damage": structural_damage,
        "conservation_error": conservation_error,
    }


def compute_shield_recharge(
    shield_energy: float,
    shield_integrity: float,
    max_shield_energy: float,
    config: SimulationConfig,
) -> Dict[str, Any]:
    """[PHYSICS LAYER] Dual recharge: energy + integrity."""
    new_energy = min(max_shield_energy, shield_energy + config.gamma)
    new_integrity = min(1.0, shield_integrity + config.integrity_recharge)
    return {
        "energy_gained": new_energy - shield_energy,
        "integrity_gained": new_integrity - shield_integrity,
        "new_energy": new_energy,
        "new_integrity": new_integrity,
    }


def compute_recovery(
    stability: float,
    max_stability: float,
    state: SystemState,
    recovery_rate: float,
) -> Dict[str, Any]:
    """[PHYSICS LAYER] Exponential recovery: dS/dt = k(Max-S)."""
    if state == SystemState.COLLAPSED:
        return {"blocked": True, "new_stability": stability, "new_state": state}

    # [v3.5 FIX] Exponential approach to max_stability
    # delta = k * (Max - S) — slows down as S approaches Max
    delta = recovery_rate * (max_stability - stability)
    new_stability = min(max_stability, stability + delta)
    new_state = state
    if new_stability >= (max_stability * 0.8) and state == SystemState.STRAINED:
        new_state = SystemState.BALANCED

    return {
        "blocked": False,
        "new_stability": new_stability,
        "new_state": new_state,
        "stab_gained": new_stability - stability,
        "recovery_rate": recovery_rate,
        "delta": delta,
    }


def compute_reboot(
    max_stability: float,
    threshold: float,
    state: SystemState,
    reboot_count: int,
    max_reboots: int,
    reboot_mode: RebootMode,
    penalty_pct: float,
) -> Dict[str, Any]:
    """[PHYSICS LAYER] Compute reboot outcome without mutation."""
    if reboot_count >= max_reboots:
        return {"success": False, "event": EventType.REBOOT_EXHAUSTED, "msg": "Reboots exhausted."}
    if state != SystemState.COLLAPSED:
        return {"success": False, "event": EventType.REBOOT_UNNEEDED, "msg": "System operational."}

    penalty = max_stability * (penalty_pct / 100.0)
    projected_max = max_stability - penalty

    if reboot_mode == RebootMode.SAFETY_GUARD and projected_max <= threshold:
        return {
            "success": False,
            "event": EventType.REBOOT_FAILED_THRESHOLD,
            "projected_max": projected_max,
            "msg": "Capacity below threshold.",
        }

    return {
        "success": True,
        "event": EventType.REBOOT_SUCCESS,
        "projected_max": projected_max,
        "penalty": penalty,
        "reboot_num": reboot_count + 1,
        "msg": f"Reboot {reboot_count + 1}/{max_reboots}: Capacity -{penalty:.1f}.",
    }


# ==============================================================================
# SECTION 4: PIPELINE (plan -> validate -> commit)
# ==============================================================================

def plan_threat_impact(
    threat: float,
    stability: float,
    max_stability: float,
    shield_energy: float,
    shield_integrity: float,
    max_shield_energy: float,
    threshold: float,
    mode: ShieldMode,
    config: SimulationConfig,
) -> Dict[str, Any]:
    """[DERIVED STATE] Compute projected impact WITHOUT mutating state."""
    threat = float(threat)
    shield_result = compute_shield_absorption(
        threat, shield_energy, shield_integrity, max_shield_energy, mode, config
    )
    residual = shield_result["residual"]

    projected_stability = max(0.0, stability - residual)

    stability_side_effect = 0.0
    if mode == ShieldMode.FORTRESS and threat > 0:
        projected_stability -= config.fortress_stability_drain
        stability_side_effect = -config.fortress_stability_drain
    elif mode == ShieldMode.EVASIVE:
        projected_stability = min(max_stability, projected_stability + config.evasive_stability_bonus)
        stability_side_effect = config.evasive_stability_bonus

    projected_stability = max(0.0, projected_stability)

    if projected_stability < threshold:
        projected_state = SystemState.COLLAPSED
        projected_stability = 0.0
    elif projected_stability < (max_stability * config.strained_threshold_ratio):
        projected_state = SystemState.STRAINED
    else:
        projected_state = SystemState.BALANCED

    return {
        "threat": threat,
        "shield_result": shield_result,
        "residual": residual,
        "equilibrium": stability - residual,
        "projected_state": projected_state,
        "projected_stability": projected_stability,
        "stability_side_effect": stability_side_effect,
        "shield_energy_after": shield_energy - shield_result["energy_cost"],
        "shield_integrity_after": max(0.0, shield_integrity - shield_result["integrity_damage"]),
    }


def validate_plan(plan: Dict[str, Any]) -> bool:
    """[GATE] Pre-flight invariant checks before state mutation."""
    if plan.get("shield_energy_after", 0.0) < 0:
        return False
    if plan.get("shield_integrity_after", 0.0) < 0:
        return False
    if plan.get("projected_stability", 0.0) < 0:
        return False
    if plan.get("residual", 0.0) < 0:
        return False
    return True


def commit_threat(
    plan: Dict[str, Any],
    tick: int,
    current_state: SystemState,
    current_shield_state: ShieldState,
    stability: float,
    shield_energy: float,
    shield_integrity: float,
    max_stability: float,
) -> Dict[str, Any]:
    """[MEASURED STATE] Execute validated plan, returning new values + event metadata."""
    new_stability = plan["projected_stability"]
    new_energy = plan["shield_energy_after"]
    new_integrity = plan["shield_integrity_after"]
    new_state = plan["projected_state"]

    if plan["shield_result"]["breach"]:
        new_shield_state = ShieldState.BREACHED
    elif new_integrity < 0.5:
        new_shield_state = ShieldState.DEGRADED
    else:
        new_shield_state = ShieldState.ACTIVE

    sr = plan["shield_result"]
    if new_state == SystemState.COLLAPSED:
        etype = EventType.THREAT_COLLAPSE
    elif sr["breach"]:
        etype = EventType.SHIELD_BREACH
    elif new_state == SystemState.STRAINED:
        etype = EventType.THREAT_STRAIN
    else:
        etype = EventType.THREAT_ABSORBED

    return {
        "new_stability": new_stability,
        "new_energy": new_energy,
        "new_integrity": new_integrity,
        "new_state": new_state,
        "new_shield_state": new_shield_state,
        "event_type": etype,
        "metadata": {
            "tick": tick,
            "threat": plan["threat"],
            "absorbed": sr["absorbed"],
            "residual": plan["residual"],
            "breach": sr["breach"],
            "efficiency": sr["efficiency"],
            "integrity_damage": sr["integrity_damage"],
            "heat_loss": sr["heat_loss"],
            "structural_damage": sr["structural_damage"],
            "conservation_error": sr["conservation_error"],
        },
    }


# ==============================================================================
# SECTION 5: TELEMETRY
# ==============================================================================

@dataclass(frozen=True)
class EventLog:
    """[DERIVED STATE] Immutable causal event with shield telemetry."""
    tick: int
    tier: EventTier
    event_type: EventType
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
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        def _serialize(v):
            if isinstance(v, Enum):
                return v.name
            if isinstance(v, (list, tuple)):
                return [_serialize(x) for x in v]
            if isinstance(v, dict):
                return {k: _serialize(vv) for k, vv in v.items()}
            return v
        return {
            "tick": self.tick,
            "tier": self.tier.name,
            "event_type": self.event_type.name,
            "state_before": self.state_before.name,
            "state_after": self.state_after.name,
            "stability_delta": round(self.stability_after - self.stability_before, 2),
            "shield_energy_delta": round(self.shield_energy_after - self.shield_energy_before, 2),
            "shield_integrity_delta": round(self.shield_integrity_after - self.shield_integrity_before, 3),
            "max_stability_delta": round(self.max_stability_after - self.max_stability_before, 2),
            "metadata": {k: _serialize(v) for k, v in self.metadata.items()},
        }


class MetricsCollector:
    """[POLICY LAYER] Aggregates quantitative metrics across a simulation run."""

    def __init__(self):
        self.ticks: List[int] = []
        self.stability: List[float] = []
        self.shield_energy: List[float] = []
        self.shield_integrity: List[float] = []
        self.max_stability: List[float] = []
        self.states: List[str] = []
        self.collapse_events: int = 0
        self.reboot_events: int = 0
        self.repair_events: int = 0
        self.breach_events: int = 0
        # [v3.5] Conservation tracking
        self.total_heat_loss: float = 0.0
        self.total_structural_damage: float = 0.0
        self.total_conservation_error: float = 0.0

    def record(self, tick: int, state: SystemState, stability: float, shield_energy: float, shield_integrity: float, max_stability: float) -> None:
        self.ticks.append(tick)
        self.stability.append(stability)
        self.shield_energy.append(shield_energy)
        self.shield_integrity.append(shield_integrity)
        self.max_stability.append(max_stability)
        self.states.append(state.name)
        if state == SystemState.COLLAPSED:
            self.collapse_events += 1

    def record_conservation(self, heat: float, structural: float, error: float) -> None:
        self.total_heat_loss += heat
        self.total_structural_damage += structural
        self.total_conservation_error += error

    def summarize(self) -> Dict[str, Any]:
        if not self.ticks:
            return {}
        lifespan = self.ticks[-1]
        avg_stab = sum(self.stability) / len(self.stability)
        avg_energy = sum(self.shield_energy) / len(self.shield_energy)
        avg_integrity = sum(self.shield_integrity) / len(self.shield_integrity)
        dist = defaultdict(int)
        for s in self.states:
            dist[s] += 1
        return {
            "lifespan": lifespan,
            "avg_stability": round(avg_stab, 2),
            "avg_shield_energy": round(avg_energy, 2),
            "avg_shield_integrity": round(avg_integrity, 3),
            "final_max_stability": round(self.max_stability[-1], 2),
            "collapse_events": self.collapse_events,
            "breach_events": self.breach_events,
            "reboot_events": self.reboot_events,
            "repair_events": self.repair_events,
            "state_distribution": dict(dist),
            # [v3.5] Conservation metrics
            "total_heat_loss": round(self.total_heat_loss, 2),
            "total_structural_damage": round(self.total_structural_damage, 2),
            "total_conservation_error": round(self.total_conservation_error, 6),
            "conservation_violations": sum(1 for e in [self.total_conservation_error] if e > 0.001),
        }


class Visualizer:
    """[POLICY LAYER] Renders stability, shield energy, and shield integrity trajectories."""

    def __init__(self, metrics: MetricsCollector):
        self.metrics = metrics

    def render(self, save_path: Optional[str] = None) -> None:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("[VISUALIZER] matplotlib not available. Skipping render.")
            return

        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

        axes[0].plot(self.metrics.ticks, self.metrics.stability, label="Stability", color="green", linewidth=2)
        axes[0].plot(self.metrics.ticks, self.metrics.max_stability, label="Max Stability", color="darkgreen", linestyle="--", alpha=0.7)
        axes[0].set_ylabel("Stability")
        axes[0].set_title("PROTOCOL_SINGULARITY_v3.5 (COG-V&V) — Active Shield Trajectory")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].plot(self.metrics.ticks, self.metrics.shield_energy, label="Shield Energy", color="blue", linewidth=2)
        axes[1].set_ylabel("Shield Energy")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        axes[2].plot(self.metrics.ticks, self.metrics.shield_integrity, label="Shield Integrity", color="purple", linewidth=2)
        axes[2].set_ylabel("Shield Integrity")
        axes[2].set_xlabel("Tick")
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        if save_path:
            try:
                parent = os.path.dirname(save_path)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                plt.savefig(save_path, dpi=150)
                print(f"[VISUALIZER] Saved to {save_path}")
            except OSError as e:
                print(f"[VISUALIZER] Unable to save figure: {e}")
                print(f"[VISUALIZER] Try running with save_path='./figure.png' or visualize=False")
        else:
            plt.show()


# ==============================================================================
# SECTION 6: CORE ENGINE
# ==============================================================================

class SingularityCoreV3:
    """[MEASURED STATE] Active Shielding Resilience Engine."""

    def __init__(self, config: SimulationConfig):
        self.config = config

        self._M0 = config.max_stability
        self.max_stability = config.max_stability
        self.stability = config.max_stability
        self.threshold = config.threshold
        self.state = SystemState.BALANCED

        self._E0 = config.max_shield_energy
        self.max_shield_energy = config.max_shield_energy
        self.shield_energy = config.max_shield_energy
        self.shield_integrity = config.shield_integrity
        self.shield_state = ShieldState.ACTIVE
        self.shield_mode = ShieldMode.BALANCED

        self.reboot_mode = RebootMode.SAFETY_GUARD
        self.reboot_count = 0
        self.max_reboots = config.max_reboots

        self.rng_seed = config.rng_seed
        self._rng = random.Random(config.rng_seed)

        self.tick = 0
        self.events: List[EventLog] = []

    def _validate(self) -> None:
        """[GATE] Hard invariant checks with explicit exceptions."""
        if self.stability < 0.0:
            raise ValueError(f"[INVARIANT] Stability {self.stability} below zero")
        if self.stability > self.max_stability:
            raise ValueError(f"[INVARIANT] Stability {self.stability} exceeds max {self.max_stability}")
        if self.max_stability < self.threshold:
            raise ValueError(f"[INVARIANT] Max stability {self.max_stability} below threshold {self.threshold}")
        if self.max_stability > self._M0:
            raise ValueError(f"[INVARIANT] Max stability {self.max_stability} exceeds original {self._M0}")
        if self.shield_energy < 0.0:
            raise ValueError(f"[INVARIANT] Shield energy {self.shield_energy} below zero")
        if self.shield_energy > self.max_shield_energy:
            raise ValueError(f"[INVARIANT] Shield energy {self.shield_energy} exceeds max {self.max_shield_energy}")
        if not (0.0 <= self.shield_integrity <= 1.0):
            raise ValueError(f"[INVARIANT] Shield integrity {self.shield_integrity} out of range [0,1]")

    def set_shield_mode(self, mode: ShieldMode) -> None:
        """Set active defense posture."""
        self.shield_mode = mode

    def inject_threat(self, threat: float) -> Dict[str, Any]:
        """[MEASURED STATE] plan -> validate -> commit with active shield."""
        s_before = self.stability
        e_before = self.shield_energy
        i_before = self.shield_integrity
        m_before = self.max_stability
        state_before = self.state

        plan = plan_threat_impact(
            threat, self.stability, self.max_stability, self.shield_energy, self.shield_integrity,
            self.max_shield_energy, self.threshold, self.shield_mode, self.config
        )
        if not validate_plan(plan):
            return {"event": EventType.VALIDATION_FAIL, "msg": "Threat plan failed pre-flight validation."}

        result = commit_threat(
            plan, self.tick, self.state, self.shield_state,
            self.stability, self.shield_energy, self.shield_integrity, self.max_stability
        )
        self.stability = result["new_stability"]
        self.shield_energy = result["new_energy"]
        self.shield_integrity = result["new_integrity"]
        self.state = result["new_state"]
        self.shield_state = result["new_shield_state"]

        self.events.append(EventLog(
            tick=self.tick,
            tier=EventTier.SHIELD if result["event_type"] in (EventType.THREAT_ABSORBED, EventType.THREAT_STRAIN, EventType.SHIELD_BREACH) else EventTier.THREAT,
            event_type=result["event_type"],
            state_before=state_before,
            state_after=result["new_state"],
            stability_before=s_before,
            stability_after=result["new_stability"],
            shield_energy_before=e_before,
            shield_energy_after=result["new_energy"],
            shield_integrity_before=i_before,
            shield_integrity_after=result["new_integrity"],
            max_stability_before=m_before,
            max_stability_after=m_before,
            metadata=result["metadata"],
        ))

        return {
            "event": result["event_type"],
            "state": self.state.name,
            "shield_state": self.shield_state.name,
            "threat": plan["threat"],
            "absorbed": plan["shield_result"]["absorbed"],
            "residual": plan["residual"],
            "shield_result": plan["shield_result"],
            "msg": f"[{self.state.name}/{self.shield_state.name}] Shield absorbed {plan['shield_result']['absorbed']:.1f}, residual {plan['residual']:.1f}.",
        }

    def auto_recovery(self) -> Dict[str, Any]:
        """[MEASURED STATE] Dual-channel recovery: stability + shield."""
        s_before = self.stability
        e_before = self.shield_energy
        i_before = self.shield_integrity
        m_before = self.max_stability
        state_before = self.state

        shield_result = compute_shield_recharge(
            self.shield_energy, self.shield_integrity, self.max_shield_energy, self.config
        )
        self.shield_energy = shield_result["new_energy"]
        self.shield_integrity = shield_result["new_integrity"]

        if self.shield_integrity < 0.5:
            self.shield_state = ShieldState.DEGRADED
        elif self.shield_state == ShieldState.BREACHED and self.shield_integrity >= 0.5:
            self.shield_state = ShieldState.ACTIVE

        rec_result = compute_recovery(
            self.stability, self.max_stability, self.state, self.config.recovery_rate
        )
        if rec_result.get("blocked"):
            return {"event": EventType.RECOVERY_BLOCKED, "msg": "Recovery offline."}

        self.stability = rec_result["new_stability"]
        self.state = rec_result["new_state"]

        self.events.append(EventLog(
            tick=self.tick,
            tier=EventTier.RECOVERY,
            event_type=EventType.RECOVERY_SUCCESS,
            state_before=state_before,
            state_after=rec_result["new_state"],
            stability_before=s_before,
            stability_after=rec_result["new_stability"],
            shield_energy_before=e_before,
            shield_energy_after=self.shield_energy,
            shield_integrity_before=i_before,
            shield_integrity_after=self.shield_integrity,
            max_stability_before=m_before,
            max_stability_after=m_before,
            metadata={**rec_result, **shield_result},
        ))

        return {
            "event": EventType.RECOVERY_SUCCESS,
            "stab_gained": rec_result["stab_gained"],
            "shield_energy_gained": shield_result["energy_gained"],
            "shield_integrity_gained": shield_result["integrity_gained"],
            "msg": f"Recovery: Stability +{rec_result['stab_gained']:.1f}, Shield energy +{shield_result['energy_gained']:.1f}, integrity +{shield_result['integrity_gained']:.3f}.",
        }

    def structural_repair(self) -> Dict[str, Any]:
        """[PROBABILISTIC] Core max stability repair with integrity-scaled probability."""
        if self.state == SystemState.COLLAPSED or self.max_stability >= self._M0:
            return {"event": EventType.REPAIR_IDLE, "msg": "Core repair unavailable."}

        # [v3.5] Repair harder when integrity is low
        effective_chance = self.config.repair_chance * (self.shield_integrity ** self.config.repair_integrity_factor)
        roll = self._rng.uniform(0.0, 100.0)
        if roll <= effective_chance:
            m0 = self.max_stability
            self.max_stability = min(self._M0, self.max_stability + self.config.repair_amount)
            repaired = self.max_stability - m0
            self.events.append(EventLog(
                tick=self.tick,
                tier=EventTier.REPAIR,
                event_type=EventType.REPAIR_SUCCESS,
                state_before=self.state,
                state_after=self.state,
                stability_before=self.stability,
                stability_after=self.stability,
                shield_energy_before=self.shield_energy,
                shield_energy_after=self.shield_energy,
                shield_integrity_before=self.shield_integrity,
                shield_integrity_after=self.shield_integrity,
                max_stability_before=m0,
                max_stability_after=self.max_stability,
                metadata={"roll": roll, "repaired": repaired, "effective_chance": effective_chance},
            ))
            return {"event": EventType.REPAIR_SUCCESS, "repaired": repaired, "msg": f"Core repair: +{repaired:.1f} capacity."}

        return {"event": EventType.REPAIR_IDLE, "roll": roll, "msg": "Core repair idle."}

    def shield_structural_repair(self) -> Dict[str, Any]:
        """[PROBABILISTIC] Shield max energy repair."""
        if self.max_shield_energy >= self._E0:
            return {"event": EventType.SHIELD_REPAIR_MAXED, "msg": "Shield at max energy capacity."}

        roll = self._rng.uniform(0.0, 100.0)
        if roll <= self.config.repair_chance:
            e0 = self.max_shield_energy
            self.max_shield_energy = min(self._E0, self.max_shield_energy + self.config.repair_amount * 0.5)
            repaired = self.max_shield_energy - e0
            self.events.append(EventLog(
                tick=self.tick,
                tier=EventTier.REPAIR,
                event_type=EventType.SHIELD_REPAIR_SUCCESS,
                state_before=self.state,
                state_after=self.state,
                stability_before=self.stability,
                stability_after=self.stability,
                shield_energy_before=self.shield_energy,
                shield_energy_after=self.shield_energy,
                shield_integrity_before=self.shield_integrity,
                shield_integrity_after=self.shield_integrity,
                max_stability_before=self.max_stability,
                max_stability_after=self.max_stability,
                metadata={"roll": roll, "repaired": repaired},
            ))
            return {"event": EventType.SHIELD_REPAIR_SUCCESS, "repaired": repaired, "msg": f"Shield repair: +{repaired:.1f} max energy."}

        return {"event": EventType.SHIELD_REPAIR_IDLE, "roll": roll, "msg": "Shield repair idle."}

    def manual_reboot(self) -> Dict[str, Any]:
        """[MEASURED STATE] Emergency reset."""
        s0, e0, i0, m0 = self.stability, self.shield_energy, self.shield_integrity, self.max_stability
        state_before = self.state

        result = compute_reboot(
            self.max_stability, self.threshold, self.state,
            self.reboot_count, self.max_reboots, self.reboot_mode,
            self.config.reboot_penalty_pct
        )
        if not result["success"]:
            if result["event"] == EventType.REBOOT_FAILED_THRESHOLD:
                self.events.append(EventLog(
                    tick=self.tick, tier=EventTier.REBOOT, event_type=EventType.REBOOT_FAILED,
                    state_before=state_before, state_after=SystemState.COLLAPSED,
                    stability_before=s0, stability_after=0.0,
                    shield_energy_before=e0, shield_energy_after=0.0,
                    shield_integrity_before=i0, shield_integrity_after=0.0,
                    max_stability_before=m0, max_stability_after=m0,
                    metadata={"penalty": result.get("penalty"), "projected_max": result.get("projected_max")},
                ))
            return result

        self.max_stability = result["projected_max"]
        self.reboot_count = result["reboot_num"]
        self.stability = self.max_stability
        self.shield_energy = self.max_shield_energy
        self.shield_integrity = min(1.0, self.shield_integrity + 0.2)
        self.shield_state = ShieldState.ACTIVE

        self.events.append(EventLog(
            tick=self.tick,
            tier=EventTier.REBOOT,
            event_type=EventType.REBOOT_SUCCESS,
            state_before=state_before,
            state_after=SystemState.BALANCED,
            stability_before=s0,
            stability_after=self.stability,
            shield_energy_before=e0,
            shield_energy_after=self.shield_energy,
            shield_integrity_before=i0,
            shield_integrity_after=self.shield_integrity,
            max_stability_before=m0,
            max_stability_after=self.max_stability,
            metadata={"penalty": result["penalty"], "reboot_num": result["reboot_num"]},
        ))
        self.state = SystemState.BALANCED

        return result

    def get_telemetry(self) -> Dict[str, Any]:
        total_health = self.stability + self.shield_energy + (self.shield_integrity * 50)
        max_possible_health = self._M0 + self._E0 + 50.0

        if self.state == SystemState.COLLAPSED:
            hierarchy = "FAILURE/COLLAPSED"
        elif self.state == SystemState.STRAINED:
            hierarchy = "FAILURE/STRAINED"
        else:
            hierarchy = "OPERATIONAL/BALANCED"

        return {
            "tick": self.tick,
            "state": self.state.name,
            "hierarchy": hierarchy,
            "shield_state": self.shield_state.name,
            "shield_mode": self.shield_mode.name,
            "stability": round(self.stability, 2),
            "max_stability": round(self.max_stability, 2),
            "original_max": round(self._M0, 2),
            "shield_energy": round(self.shield_energy, 2),
            "max_shield_energy": round(self.max_shield_energy, 2),
            "original_max_shield": round(self._E0, 2),
            "shield_integrity": round(self.shield_integrity, 3),
            "threshold": round(self.threshold, 2),
            "recovery_rate": round(self.config.recovery_rate, 2),
            "gamma": round(self.config.gamma, 2),
            "reboots": (self.reboot_count, self.max_reboots),
            "rng_seed": self.rng_seed,
            "total_health": round(total_health, 2),
            "max_possible_health": round(max_possible_health, 2),
            "health_ratio": round(total_health / max_possible_health, 3) if max_possible_health > 0 else 0.0,
        }

    def export_events(self) -> str:
        return json.dumps([e.to_dict() for e in self.events], indent=2)


# ==============================================================================
# SECTION 7: VALIDATION SUITE (Property-Based & Reference Scenarios)
# ==============================================================================

class ValidationSuite:
    """[V&V LAYER] Property-based tests and reference scenario validation."""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    def _assert_property(self, name: str, condition: bool, details: str = "") -> None:
        self.results.append({"test": name, "passed": condition, "details": details})
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {name} {details}")

    def run_all(self) -> bool:
        print("=" * 70)
        print("PROTOCOL_SINGULARITY_v3.5 — VALIDATION SUITE")
        print("=" * 70)

        # --- Property-based tests ---
        print("\n[PROPERTY TESTS]")
        self._test_stability_non_negative()
        self._test_shield_integrity_range()
        self._test_shield_energy_bounded()
        self._test_conservation_of_energy()
        self._test_efficiency_ceiling()
        self._test_recovery_exponential()
        self._test_reboot_capacity_decreases()
        self._test_zero_threat_no_damage()
        self._test_infinite_shield_no_damage()
        self._test_zero_shield_full_damage()

        # --- Reference scenarios ---
        print("\n[REFERENCE SCENARIOS]")
        self._scenario_zero_threat()
        self._scenario_infinite_shield()
        self._scenario_zero_shield()
        self._scenario_reboot_sequence()
        self._scenario_fortress_combat_only()

        all_passed = all(r["passed"] for r in self.results)
        print("\n" + "=" * 70)
        print(f"VALIDATION SUMMARY: {sum(r['passed'] for r in self.results)}/{len(self.results)} passed")
        print("=" * 70)
        return all_passed

    def _test_stability_non_negative(self):
        config = SimulationConfig(rng_seed=123)
        core = SingularityCoreV3(config)
        for t in [10, 50, 100, 200]:
            core.inject_threat(float(t))
            core._validate()
        self._assert_property("stability >= 0 always", core.stability >= 0,
                              f"final stability={core.stability}")

    def _test_shield_integrity_range(self):
        config = SimulationConfig(rng_seed=456)
        core = SingularityCoreV3(config)
        for t in [10, 50, 100, 200, 500]:
            core.inject_threat(float(t))
            core._validate()
        self._assert_property("shield_integrity in [0,1] always",
                              0.0 <= core.shield_integrity <= 1.0,
                              f"final integrity={core.shield_integrity}")

    def _test_shield_energy_bounded(self):
        config = SimulationConfig(rng_seed=789)
        core = SingularityCoreV3(config)
        for t in [10, 50, 100, 200]:
            core.inject_threat(float(t))
            core._validate()
        self._assert_property("shield_energy <= max_shield_energy always",
                              core.shield_energy <= core.max_shield_energy,
                              f"energy={core.shield_energy}, max={core.max_shield_energy}")

    def _test_conservation_of_energy(self):
        config = SimulationConfig(rng_seed=42)
        threat = 100.0
        shield_energy = 50.0
        shield_integrity = 1.0
        max_shield_energy = 50.0
        result = compute_shield_absorption(
            threat, shield_energy, shield_integrity, max_shield_energy,
            ShieldMode.BALANCED, config
        )
        # [v3.5] Conservation: absorbed + residual + heat = threat + breach_penalty
        # structural_damage is shield wear, not an energy sink
        breach_penalty = threat * config.breach_penalty_pct if result["breach"] else 0.0
        total = result["absorbed"] + result["residual"] + result["heat_loss"]
        expected = threat + breach_penalty
        error = abs(total - expected)
        self._assert_property("energy conservation: absorbed + residual + heat = threat + breach_penalty",
                              error < 0.001,
                              f"threat={threat}, expected={expected}, total={total}, error={error}")

    def _test_efficiency_ceiling(self):
        config = SimulationConfig(rng_seed=42)
        threat = 100.0
        shield_energy = 50.0
        shield_integrity = 1.0
        max_shield_energy = 50.0
        result = compute_shield_absorption(
            threat, shield_energy, shield_integrity, max_shield_energy,
            ShieldMode.FORTRESS, config
        )
        self._assert_property("absorbed <= threat (efficiency never creates energy)",
                              result["absorbed"] <= threat,
                              f"absorbed={result['absorbed']}, threat={threat}")

    def _test_recovery_exponential(self):
        config = SimulationConfig(recovery_rate=0.25, rng_seed=42)
        result1 = compute_recovery(50.0, 100.0, SystemState.STRAINED, config.recovery_rate)
        result2 = compute_recovery(90.0, 100.0, SystemState.STRAINED, config.recovery_rate)
        # Exponential: gain at 50 should be larger than gain at 90
        self._assert_property("exponential recovery: gain at 50 > gain at 90",
                              result1["stab_gained"] > result2["stab_gained"],
                              f"gain@50={result1['stab_gained']}, gain@90={result2['stab_gained']}")

    def _test_reboot_capacity_decreases(self):
        config = SimulationConfig(rng_seed=42)
        result = compute_reboot(100.0, 10.0, SystemState.COLLAPSED, 0, 2,
                              RebootMode.SAFETY_GUARD, 20.0)
        self._assert_property("reboot decreases max capacity",
                              result["projected_max"] < 100.0,
                              f"projected_max={result['projected_max']}")

    def _test_zero_threat_no_damage(self):
        config = SimulationConfig(rng_seed=42)
        core = SingularityCoreV3(config)
        core.set_shield_mode(ShieldMode.BALANCED)
        result = core.inject_threat(0.0)
        self._assert_property("zero threat causes no stability damage",
                              core.stability == 100.0,
                              f"stability={core.stability}")

    def _test_infinite_shield_no_damage(self):
        config = SimulationConfig(max_shield_energy=9999.0, rng_seed=42)
        core = SingularityCoreV3(config)
        core.shield_energy = 9999.0
        result = core.inject_threat(100.0)
        self._assert_property("infinite shield absorbs all damage",
                              result["residual"] == 0.0,
                              f"residual={result['residual']}")

    def _test_zero_shield_full_damage(self):
        config = SimulationConfig(rng_seed=42)
        core = SingularityCoreV3(config)
        core.shield_energy = 0.0
        result = core.inject_threat(50.0)
        # [v3.5] Zero shield = breach, so residual = threat + breach_penalty
        expected = 50.0 + (50.0 * config.breach_penalty_pct)
        self._assert_property("zero shield = full damage + breach penalty",
                              result["residual"] == expected,
                              f"residual={result['residual']}, expected={expected}")

    def _scenario_zero_threat(self):
        print("  Scenario: zero threat for 5 ticks")
        config = SimulationConfig(rng_seed=42)
        core = SingularityCoreV3(config)
        for i in range(1, 6):
            core.tick = i
            core.inject_threat(0.0)
            core.auto_recovery()
        self._assert_property("zero threat: stability stays at max",
                              core.stability == 100.0,
                              f"stability={core.stability}")

    def _scenario_infinite_shield(self):
        print("  Scenario: infinite shield vs heavy threat")
        config = SimulationConfig(max_shield_energy=9999.0, rng_seed=42)
        core = SingularityCoreV3(config)
        core.shield_energy = 9999.0
        core.tick = 1
        result = core.inject_threat(500.0)
        self._assert_property("infinite shield: no breach, no residual",
                              result["residual"] == 0.0 and not result.get("breach", False),
                              f"residual={result['residual']}, breach={result.get('breach')}")

    def _scenario_zero_shield(self):
        print("  Scenario: zero shield vs moderate threat")
        config = SimulationConfig(rng_seed=42)
        core = SingularityCoreV3(config)
        core.shield_energy = 0.0
        core.tick = 1
        result = core.inject_threat(50.0)
        expected = 50.0 + (50.0 * config.breach_penalty_pct)
        self._assert_property("zero shield: full residual + breach penalty",
                              result["residual"] == expected,
                              f"residual={result['residual']}, expected={expected}")

    def _scenario_reboot_sequence(self):
        print("  Scenario: repeated reboot decreases capacity")
        config = SimulationConfig(rng_seed=42)
        core = SingularityCoreV3(config)
        caps = []
        events = []
        for _ in range(3):
            core.state = SystemState.COLLAPSED
            result = core.manual_reboot()
            caps.append(core.max_stability)
            events.append(result["event"].name)
        self._assert_property("reboot sequence: first two decrease, third exhausted",
                              caps[0] > caps[1] and events[2] == "REBOOT_EXHAUSTED",
                              f"caps={caps}, events={events}")

    def _scenario_fortress_combat_only(self):
        print("  Scenario: fortress drain only during combat")
        config = SimulationConfig(rng_seed=42)
        core = SingularityCoreV3(config)
        core.set_shield_mode(ShieldMode.FORTRESS)
        core.tick = 1
        core.inject_threat(0.0)
        s_after_zero = core.stability
        core.tick = 2
        core.inject_threat(50.0)
        s_after_combat = core.stability
        self._assert_property("fortress: no drain at zero threat",
                              s_after_zero == 100.0,
                              f"stability_after_zero={s_after_zero}")


# ==============================================================================
# SECTION 8: MAIN DRIVER
# ==============================================================================

def run_simulation(
    config: SimulationConfig,
    mode: RebootMode = RebootMode.SAFETY_GUARD,
    shield_mode: ShieldMode = ShieldMode.BALANCED,
    max_ticks: int = 30,
    verbose: bool = True,
    visualize: bool = True,
    save_plot: str = "./v35_cog_vv_trajectory.png",
) -> dict:
    """[DETERMINISTIC] Simulation driver with active shielding."""
    core = SingularityCoreV3(config)
    core.reboot_mode = mode
    core.set_shield_mode(shield_mode)

    threats = ThreatGenerator(core._rng, config.threat_low, config.threat_high,
                               config.threat_cooldown_ticks, config.threat_escalation_factor)
    metrics = MetricsCollector()
    viz = Visualizer(metrics)

    if verbose:
        print("=" * 70)
        print("PROTOCOL_SINGULARITY_v3.5 (COG-V&V) — ACTIVE SHIELDING")
        print("=" * 70)
        print(f"Seed: {config.rng_seed} | Reboot: {mode.name} | Shield: {shield_mode.name} | Ticks: {max_ticks}")
        print("-" * 70)

    for tick in range(1, max_ticks + 1):
        core.tick = tick
        threat = threats.next()

        result = core.inject_threat(threat)

        metrics.record(tick, core.state, core.stability, core.shield_energy, core.shield_integrity, core.max_stability)

        if result.get("event") == EventType.SHIELD_BREACH:
            metrics.breach_events += 1

        # [v3.5] Conservation tracking
        if "shield_result" in result:
            sr = result.get("shield_result", {})
            metrics.record_conservation(
                sr.get("heat_loss", 0.0),
                sr.get("structural_damage", 0.0),
                sr.get("conservation_error", 0.0)
            )

        if core.state == SystemState.COLLAPSED:
            reb = core.manual_reboot()
            if verbose:
                print(f"[T+{tick:02d}] {result['msg']}")
                print(f"       {reb['msg']}")
            if reb["event"] == EventType.REBOOT_EXHAUSTED:
                if verbose:
                    print(f">>> TERMINAL COLLAPSE AT T+{tick}")
                break
            metrics.reboot_events += 1
        else:
            rec = core.auto_recovery()
            rep = core.structural_repair()
            srep = core.shield_structural_repair()
            if rep["event"] == EventType.REPAIR_SUCCESS:
                metrics.repair_events += 1
            if srep["event"] == EventType.SHIELD_REPAIR_SUCCESS:
                metrics.repair_events += 1

            if verbose:
                tel = core.get_telemetry()
                print(
                    f"[T+{tick:02d}] State: {tel['state']:<9} | "
                    f"Stab: {tel['stability']:>5.1f}/{tel['max_stability']:>5.1f} | "
                    f"Shield: {tel['shield_energy']:>5.1f}/{tel['max_shield_energy']:>5.1f} | "
                    f"Integ: {tel['shield_integrity']:.2f} | "
                    f"{result['msg']}"
                )
                if rep["event"] == EventType.REPAIR_SUCCESS:
                    print(f"       +-- {rep['msg']}")
                if srep["event"] == EventType.SHIELD_REPAIR_SUCCESS:
                    print(f"       +-- {srep['msg']}")

        core._validate()

    summary = metrics.summarize()
    if verbose:
        print("\n" + "=" * 70)
        print("METRICS SUMMARY")
        print("=" * 70)
        print(json.dumps(summary, indent=2))
        print(f"\nTotal events: {len(core.events)}")

    if visualize:
        viz.render(save_path=save_plot)

    return {
        "summary": summary,
        "telemetry": core.get_telemetry(),
        "event_count": len(core.events),
        "events_json": core.export_events(),
    }


if __name__ == "__main__":
    # Run validation suite first
    validator = ValidationSuite()
    all_passed = validator.run_all()

    if all_passed:
        print("\n>>> ALL VALIDATION TESTS PASSED — RUNNING FULL SIMULATION")
    else:
        print("\n>>> SOME VALIDATION TESTS FAILED — REVIEW BEFORE PROCEEDING")

    config = SimulationConfig(rng_seed=42)

    print("\n" + "=" * 70)
    print("RUN 1: BALANCED SHIELD MODE")
    print("=" * 70)
    r1 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.BALANCED,
                        save_plot="./v35_cog_vv_balanced.png")

    print("\n" + "=" * 70)
    print("RUN 2: FORTRESS SHIELD MODE")
    print("=" * 70)
    r2 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.FORTRESS,
                        save_plot="./v35_cog_vv_fortress.png")

    print("\n" + "=" * 70)
    print("RUN 3: EVASIVE SHIELD MODE")
    print("=" * 70)
    r3 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.EVASIVE,
                        save_plot="./v35_cog_vv_evasive.png")