"""
================================================================================
PROTOCOL_SINGULARITY_v3.1 (Final) — UNIFIED VERSION
Active Shield / Defense Layer — Single File
================================================================================
Version:     v3.1-Final-Unified
Status:      FEATURE COMPLETE
Scope:       Self-contained resilience simulation with active shielding.
             No external dependencies except matplotlib (optional).

This is the unified single-file version. All modules merged into one script.
================================================================================
"""

import random
import json
import time
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum, auto
from collections import defaultdict


# ==============================================================================
# SECTION 1: CONFIGURATION
# ==============================================================================

@dataclass(frozen=True)
class SimulationConfig:
    """[MEASURED STATE] Immutable simulation parameters."""
    max_stability: float = 100.0
    threshold: float = 10.0
    alpha: float = 10.0
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


# ==============================================================================
# SECTION 3: SIMULATION MECHANICS (Pure Functions)
# ==============================================================================

class ThreatGenerator:
    """Encapsulates threat generation strategy."""

    def __init__(self, rng: random.Random, low: float, high: float):
        self._rng = rng
        self.low = low
        self.high = high

    def next(self) -> float:
        return round(self._rng.uniform(self.low, self.high), 1)


def compute_shield_absorption(
    threat: float,
    shield_energy: float,
    shield_integrity: float,
    max_shield_energy: float,
    mode: ShieldMode,
    config: SimulationConfig,
) -> Dict[str, Any]:
    """[MEASURED STATE] Active shield absorption with mode-dependent efficiency."""
    efficiency = 0.5 + (shield_integrity * 0.5)

    if mode == ShieldMode.FORTRESS:
        efficiency *= config.fortress_efficiency_mult
        energy_cost_mult = config.fortress_energy_cost_mult
    elif mode == ShieldMode.EVASIVE:
        efficiency *= config.evasive_efficiency_mult
        energy_cost_mult = config.evasive_energy_cost_mult
    else:
        energy_cost_mult = 1.0

    raw_absorbed = threat * efficiency
    actual_absorbed = min(shield_energy, raw_absorbed)
    residual = threat - actual_absorbed
    energy_cost = min(shield_energy, actual_absorbed * energy_cost_mult)

    hit_ratio = threat / max_shield_energy if max_shield_energy > 0 else 0.0
    if hit_ratio > config.heavy_hit_threshold:
        integrity_damage = 0.08
    elif hit_ratio > config.medium_hit_threshold:
        integrity_damage = 0.03
    else:
        integrity_damage = 0.0

    shield_capacity = shield_energy + (shield_integrity * max_shield_energy * 0.5)
    breach = threat > shield_capacity * config.breach_threshold
    if breach:
        residual = threat * 0.35
        integrity_damage += 0.15
        energy_cost = shield_energy

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
    config: SimulationConfig,
) -> Dict[str, Any]:
    """[MEASURED STATE] Dual recharge: energy + integrity."""
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
    alpha: float,
) -> Dict[str, Any]:
    """[MEASURED STATE] Compute post-recovery stability without mutation."""
    if state == SystemState.COLLAPSED:
        return {"blocked": True, "new_stability": stability, "new_state": state}

    new_stability = min(max_stability, stability + alpha)
    new_state = state
    if new_stability >= (max_stability * 0.8) and state == SystemState.STRAINED:
        new_state = SystemState.BALANCED

    return {
        "blocked": False,
        "new_stability": new_stability,
        "new_state": new_state,
        "stab_gained": new_stability - stability,
        "alpha": alpha,
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
    """[MEASURED STATE] Compute reboot outcome without mutation."""
    if reboot_count >= max_reboots:
        return {"success": False, "event": "REBOOT_EXHAUSTED", "msg": "Reboots exhausted."}
    if state != SystemState.COLLAPSED:
        return {"success": False, "event": "REBOOT_UNNEEDED", "msg": "System operational."}

    penalty = max_stability * (penalty_pct / 100.0)
    projected_max = max_stability - penalty

    if reboot_mode == RebootMode.SAFETY_GUARD and projected_max <= threshold:
        return {
            "success": False,
            "event": "REBOOT_FAILED_THRESHOLD",
            "projected_max": projected_max,
            "msg": "Capacity below threshold.",
        }

    return {
        "success": True,
        "event": "REBOOT_SUCCESS",
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
    equilibrium = stability - residual

    if equilibrium < threshold:
        projected_state = SystemState.COLLAPSED
        projected_stability = 0.0
    elif residual > (stability * 0.5):
        degradation = residual * 0.3
        projected_stability = max(0.0, stability - degradation)
        if projected_stability < threshold:
            projected_state = SystemState.COLLAPSED
            projected_stability = 0.0
        else:
            projected_state = SystemState.STRAINED
    else:
        projected_state = SystemState.BALANCED
        projected_stability = stability

    stability_side_effect = 0.0
    if mode == ShieldMode.FORTRESS:
        stability_side_effect = -config.fortress_stability_drain
    elif mode == ShieldMode.EVASIVE:
        stability_side_effect = config.evasive_stability_bonus

    return {
        "threat": threat,
        "shield_result": shield_result,
        "residual": residual,
        "equilibrium": equilibrium,
        "projected_state": projected_state,
        "projected_stability": projected_stability + stability_side_effect,
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
        etype = "THREAT_COLLAPSE"
    elif sr["breach"]:
        etype = "SHIELD_BREACH"
    elif new_state == SystemState.STRAINED:
        etype = "THREAT_STRAIN"
    else:
        etype = "THREAT_ABSORBED"

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
            "event_type": self.event_type,
            "state_before": self.state_before.name,
            "state_after": self.state_after.name,
            "stability_delta": round(self.stability_after - self.stability_before, 2),
            "shield_energy_delta": round(self.shield_energy_after - self.shield_energy_before, 2),
            "shield_integrity_delta": round(self.shield_integrity_after - self.shield_integrity_before, 3),
            "max_stability_delta": round(self.max_stability_after - self.max_stability_before, 2),
            "metadata": {k: _serialize(v) for k, v in self.metadata},
        }


class MetricsCollector:
    """Aggregates quantitative metrics across a simulation run."""

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

    def record(self, tick: int, state: SystemState, stability: float, shield_energy: float, shield_integrity: float, max_stability: float) -> None:
        self.ticks.append(tick)
        self.stability.append(stability)
        self.shield_energy.append(shield_energy)
        self.shield_integrity.append(shield_integrity)
        self.max_stability.append(max_stability)
        self.states.append(state.name)
        if state == SystemState.COLLAPSED:
            self.collapse_events += 1

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
        }


class Visualizer:
    """Renders stability, shield energy, and shield integrity trajectories."""

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
        axes[0].set_title("PROTOCOL_SINGULARITY_v3.1 (Final) — Active Shield Trajectory")
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
            plt.savefig(save_path, dpi=150)
            print(f"[VISUALIZER] Saved to {save_path}")
        else:
            plt.show()


# ==============================================================================
# SECTION 6: CORE ENGINE
# ==============================================================================

class SingularityCoreV3:
    """[MEASURED STATE] Active Shielding Resilience Engine."""

    def __init__(self, config: SimulationConfig):
        self.config = config

        # Core stability
        self._M0 = config.max_stability
        self.max_stability = config.max_stability
        self.stability = config.max_stability
        self.threshold = config.threshold
        self.state = SystemState.BALANCED

        # Active shield
        self._E0 = config.max_shield_energy
        self.max_shield_energy = config.max_shield_energy
        self.shield_energy = config.max_shield_energy
        self.shield_integrity = config.shield_integrity
        self.shield_state = ShieldState.ACTIVE
        self.shield_mode = ShieldMode.BALANCED

        # Reboot
        self.reboot_mode = RebootMode.SAFETY_GUARD
        self.reboot_count = 0
        self.max_reboots = config.max_reboots

        # RNG
        self.rng_seed = config.rng_seed
        self._rng = random.Random(config.rng_seed)

        # Audit
        self.tick = 0
        self.events: List[EventLog] = []

    def _validate(self) -> None:
        """[GATE] Hard invariant checks."""
        assert self.stability >= 0.0
        assert self.stability <= self.max_stability
        assert self.max_stability >= self.threshold
        assert self.max_stability <= self._M0
        assert self.shield_energy >= 0.0
        assert self.shield_energy <= self.max_shield_energy
        assert 0.0 <= self.shield_integrity <= 1.0

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
        sh_state_before = self.shield_state

        plan = plan_threat_impact(
            threat, self.stability, self.shield_energy, self.shield_integrity,
            self.max_shield_energy, self.threshold, self.shield_mode, self.config
        )
        if not validate_plan(plan):
            return {"event": "VALIDATION_FAIL", "msg": "Threat plan failed pre-flight validation."}

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
            tier=EventTier.SHIELD if result["event_type"] in ("THREAT_ABSORBED", "THREAT_STRAIN", "SHIELD_BREACH") else EventTier.THREAT,
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
            metadata=tuple((k, v) for k, v in result["metadata"].items()),
        ))

        return {
            "event": result["event_type"],
            "state": self.state.name,
            "shield_state": self.shield_state.name,
            "threat": plan["threat"],
            "absorbed": plan["shield_result"]["absorbed"],
            "residual": plan["residual"],
            "msg": f"[{self.state.name}/{self.shield_state.name}] Shield absorbed {plan['shield_result']['absorbed']:.1f}, residual {plan['residual']:.1f}.",
        }

    def auto_recovery(self) -> Dict[str, Any]:
        """[MEASURED STATE] Dual-channel recovery: stability + shield."""
        s_before = self.stability
        e_before = self.shield_energy
        i_before = self.shield_integrity
        m_before = self.max_stability
        state_before = self.state

        # Shield recharge
        shield_result = compute_shield_recharge(
            self.shield_energy, self.shield_integrity, self.max_shield_energy, self.config
        )
        self.shield_energy = shield_result["new_energy"]
        self.shield_integrity = shield_result["new_integrity"]

        if self.shield_integrity < 0.5:
            self.shield_state = ShieldState.DEGRADED
        elif self.shield_state == ShieldState.BREACHED and self.shield_integrity >= 0.5:
            self.shield_state = ShieldState.ACTIVE

        # Core recovery
        rec_result = compute_recovery(
            self.stability, self.max_stability, self.state, self.config.alpha
        )
        if rec_result.get("blocked"):
            return {"event": "RECOVERY_BLOCKED", "msg": "Recovery offline."}

        self.stability = rec_result["new_stability"]
        self.state = rec_result["new_state"]

        self.events.append(EventLog(
            tick=self.tick,
            tier=EventTier.RECOVERY,
            event_type="RECOVERY",
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
            metadata=tuple((k, v) for k, v in {**rec_result, **shield_result}.items()),
        ))

        return {
            "event": "RECOVERY_SUCCESS",
            "stab_gained": rec_result["stab_gained"],
            "shield_energy_gained": shield_result["energy_gained"],
            "shield_integrity_gained": shield_result["integrity_gained"],
            "msg": f"Recovery: Stability +{rec_result['stab_gained']:.1f}, Shield energy +{shield_result['energy_gained']:.1f}, integrity +{shield_result['integrity_gained']:.3f}.",
        }

    def structural_repair(self) -> Dict[str, Any]:
        """[PROBABILISTIC] Core max stability repair."""
        if self.state == SystemState.COLLAPSED or self.max_stability >= self._M0:
            return {"event": "REPAIR_BLOCKED", "msg": "Core repair unavailable."}

        roll = self._rng.uniform(0.0, 100.0)
        if roll <= self.config.repair_chance:
            m0 = self.max_stability
            self.max_stability = min(self._M0, self.max_stability + self.config.repair_amount)
            repaired = self.max_stability - m0
            self.events.append(EventLog(
                tick=self.tick,
                tier=EventTier.REPAIR,
                event_type="REPAIR_SUCCESS",
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
                metadata=tuple((k, v) for k, v in {"roll": roll, "repaired": repaired}.items()),
            ))
            return {"event": "REPAIR_SUCCESS", "repaired": repaired, "msg": f"Core repair: +{repaired:.1f} capacity."}

        return {"event": "REPAIR_IDLE", "roll": roll, "msg": "Core repair idle."}

    def shield_structural_repair(self) -> Dict[str, Any]:
        """[PROBABILISTIC] Shield max energy repair."""
        if self.max_shield_energy >= self._E0:
            return {"event": "SHIELD_REPAIR_MAXED", "msg": "Shield at max energy capacity."}

        roll = self._rng.uniform(0.0, 100.0)
        if roll <= self.config.repair_chance:
            e0 = self.max_shield_energy
            self.max_shield_energy = min(self._E0, self.max_shield_energy + self.config.repair_amount * 0.5)
            repaired = self.max_shield_energy - e0
            self.events.append(EventLog(
                tick=self.tick,
                tier=EventTier.REPAIR,
                event_type="SHIELD_REPAIR_SUCCESS",
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
                metadata=tuple((k, v) for k, v in {"roll": roll, "repaired": repaired}.items()),
            ))
            return {"event": "SHIELD_REPAIR_SUCCESS", "repaired": repaired, "msg": f"Shield repair: +{repaired:.1f} max energy."}

        return {"event": "SHIELD_REPAIR_IDLE", "roll": roll, "msg": "Shield repair idle."}

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
            if result["event"] == "REBOOT_FAILED_THRESHOLD":
                self.events.append(EventLog(
                    tick=self.tick, tier=EventTier.REBOOT, event_type="REBOOT_FAILED",
                    state_before=state_before, state_after=SystemState.COLLAPSED,
                    stability_before=s0, stability_after=0.0,
                    shield_energy_before=e0, shield_energy_after=0.0,
                    shield_integrity_before=i0, shield_integrity_after=0.0,
                    max_stability_before=m0, max_stability_after=m0,
                    metadata=tuple((k, v) for k, v in {"penalty": result.get("penalty"), "projected_max": result.get("projected_max")}.items()),
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
            event_type="REBOOT_SUCCESS",
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
            metadata=tuple((k, v) for k, v in {"penalty": result["penalty"], "reboot_num": result["reboot_num"]}.items()),
        ))
        self.state = SystemState.BALANCED

        return result

    def get_telemetry(self) -> Dict[str, Any]:
        return {
            "tick": self.tick,
            "state": self.state.name,
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
            "alpha": round(self.config.alpha, 2),
            "gamma": round(self.config.gamma, 2),
            "reboots": (self.reboot_count, self.max_reboots),
            "rng_seed": self.rng_seed,
        }

    def export_events(self) -> str:
        return json.dumps([e.to_dict() for e in self.events], indent=2)


# ==============================================================================
# SECTION 7: MAIN DRIVER
# ==============================================================================

def run_simulation(
    config: SimulationConfig,
    mode: RebootMode = RebootMode.SAFETY_GUARD,
    shield_mode: ShieldMode = ShieldMode.BALANCED,
    max_ticks: int = 30,
    verbose: bool = True,
    visualize: bool = True,
    save_plot: str = "/mnt/agents/output/v31_unified_trajectory.png",
) -> dict:
    """[DETERMINISTIC] Simulation driver with active shielding."""
    core = SingularityCoreV3(config)
    core.reboot_mode = mode
    core.set_shield_mode(shield_mode)

    threats = ThreatGenerator(core._rng, config.threat_low, config.threat_high)
    metrics = MetricsCollector()
    viz = Visualizer(metrics)

    if verbose:
        print("=" * 70)
        print("PROTOCOL_SINGULARITY_v3.1 (Final — Unified) — ACTIVE SHIELDING")
        print("=" * 70)
        print(f"Seed: {config.rng_seed} | Reboot: {mode.name} | Shield: {shield_mode.name} | Ticks: {max_ticks}")
        print("-" * 70)

    for tick in range(1, max_ticks + 1):
        core.tick = tick
        threat = threats.next()

        result = core.inject_threat(threat)

        if core.state == SystemState.COLLAPSED:
            reb = core.manual_reboot()
            if verbose:
                print(f"[T+{tick:02d}] {result['msg']}")
                print(f"       {reb['msg']}")
            if reb["event"] == "REBOOT_EXHAUSTED":
                if verbose:
                    print(f">>> TERMINAL COLLAPSE AT T+{tick}")
                break
            metrics.reboot_events += 1
        else:
            rec = core.auto_recovery()
            rep = core.structural_repair()
            srep = core.shield_structural_repair()
            if rep["event"] == "REPAIR_SUCCESS":
                metrics.repair_events += 1
            if srep["event"] == "SHIELD_REPAIR_SUCCESS":
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
                if rep["event"] == "REPAIR_SUCCESS":
                    print(f"       +-- {rep['msg']}")
                if srep["event"] == "SHIELD_REPAIR_SUCCESS":
                    print(f"       +-- {srep['msg']}")

        metrics.record(tick, core.state, core.stability, core.shield_energy, core.shield_integrity, core.max_stability)
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
    config = SimulationConfig(rng_seed=42)

    print("\n" + "=" * 70)
    print("RUN 1: BALANCED SHIELD MODE")
    print("=" * 70)
    r1 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.BALANCED,
                        save_plot="/mnt/agents/output/v31_unified_balanced.png")

    print("\n" + "=" * 70)
    print("RUN 2: FORTRESS SHIELD MODE")
    print("=" * 70)
    r2 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.FORTRESS,
                        save_plot="/mnt/agents/output/v31_unified_fortress.png")

    print("\n" + "=" * 70)
    print("RUN 3: EVASIVE SHIELD MODE")
    print("=" * 70)
    r3 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.EVASIVE,
                        save_plot="/mnt/agents/output/v31_unified_evasive.png")