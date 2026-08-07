"""
protocol_engine/core.py
SingularityCoreV3 — Active Shielding / Defense Layer.

Two-stage threat flow with ACTIVE shield:
  Stage 1: Shield absorbs with mode-dependent efficiency
  Stage 2: Residual threat impacts core equilibrium

Shield dimensions:
  - energy: current absorption capacity (depletes and recharges)
  - integrity: structural health 0.0-1.0 (degrades under heavy fire, repairs slowly)
  - mode: BALANCED / FORTRESS / EVASIVE (active defense posture)
  - state: ACTIVE / DEGRADED / BREACHED (operational condition)
"""
import random
from typing import Dict, Any, List, Optional
from protocol_engine.types import SystemState, RebootMode, ShieldState, ShieldMode, EventTier
from protocol_engine.simulation.recovery import compute_recovery
from protocol_engine.simulation.reboot import compute_reboot
from protocol_engine.simulation.shield import compute_shield_recharge
from protocol_engine.pipeline.planner import plan_threat_impact
from protocol_engine.pipeline.validator import validate_plan
from protocol_engine.pipeline.executor import commit_threat
from protocol_engine.telemetry.events import EventLog


class SingularityCoreV3:
    """
    [MEASURED STATE] Active Shielding Resilience Engine.
    """

    def __init__(self, config):
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
        plan = plan_threat_impact(
            threat, self.stability, self.shield_energy, self.shield_integrity,
            self.max_shield_energy, self.threshold, self.shield_mode, self.config
        )
        if not validate_plan(plan):
            return {"event": "VALIDATION_FAIL", "msg": "Threat plan failed pre-flight validation."}

        new_stab, new_energy, new_integrity, new_state, new_shield_state, event = commit_threat(
            plan, self.tick, self.state, self.shield_state,
            self.stability, self.shield_energy, self.shield_integrity, self.max_stability
        )
        self.stability = new_stab
        self.shield_energy = new_energy
        self.shield_integrity = new_integrity
        self.state = new_state
        self.shield_state = new_shield_state
        self.events.append(event)

        return {
            "event": event.event_type,
            "state": self.state.name,
            "shield_state": self.shield_state.name,
            "threat": plan["threat"],
            "absorbed": plan["shield_result"]["absorbed"],
            "residual": plan["residual"],
            "msg": f"[{self.state.name}/{self.shield_state.name}] Shield absorbed {plan['shield_result']['absorbed']:.1f}, residual {plan['residual']:.1f}.",
        }

    def auto_recovery(self) -> Dict[str, Any]:
        """[MEASURED STATE] Dual-channel recovery: stability + shield."""
        # Shield recharge first
        shield_result = compute_shield_recharge(
            self.shield_energy, self.shield_integrity, self.max_shield_energy, self.config
        )
        self.shield_energy = shield_result["new_energy"]
        self.shield_integrity = shield_result["new_integrity"]

        # Update shield state based on integrity
        if self.shield_integrity < 0.5:
            self.shield_state = ShieldState.DEGRADED
        elif self.shield_state == ShieldState.BREACHED and self.shield_integrity >= 0.5:
            self.shield_state = ShieldState.ACTIVE

        # Core recovery
        new_stab, new_state, meta = compute_recovery(
            self.stability, self.max_stability, self.state, self.config.alpha
        )
        if meta.get("blocked"):
            return {"event": "RECOVERY_BLOCKED", "msg": "Recovery offline."}

        s0 = self.stability
        self.stability = new_stab
        self.state = new_state

        self.events.append(EventLog(
            tick=self.tick,
            tier=EventTier.RECOVERY,
            event_type="RECOVERY",
            state_before=self.state,
            state_after=new_state,
            stability_before=s0,
            stability_after=new_stab,
            shield_energy_before=self.shield_energy - shield_result["energy_gained"],
            shield_energy_after=self.shield_energy,
            shield_integrity_before=self.shield_integrity - shield_result["integrity_gained"],
            shield_integrity_after=self.shield_integrity,
            max_stability_before=self.max_stability,
            max_stability_after=self.max_stability,
            metadata=tuple((k, v) for k, v in {**meta, **shield_result}.items()),
        ))

        return {
            "event": "RECOVERY_SUCCESS",
            "stab_gained": meta["stab_gained"],
            "shield_energy_gained": shield_result["energy_gained"],
            "shield_integrity_gained": shield_result["integrity_gained"],
            "msg": f"Recovery: Stability +{meta['stab_gained']:.1f}, Shield energy +{shield_result['energy_gained']:.1f}, integrity +{shield_result['integrity_gained']:.3f}.",
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
        result = compute_reboot(
            self.max_stability, self.threshold, self.state,
            self.reboot_count, self.max_reboots, self.reboot_mode,
            self.config.reboot_penalty_pct
        )
        if not result["success"]:
            if result["event"] == "REBOOT_FAILED_THRESHOLD":
                self.events.append(EventLog(
                    tick=self.tick, tier=EventTier.REBOOT, event_type="REBOOT_FAILED",
                    state_before=self.state, state_after=SystemState.COLLAPSED,
                    stability_before=self.stability, stability_after=0.0,
                    shield_energy_before=self.shield_energy, shield_energy_after=0.0,
                    shield_integrity_before=self.shield_integrity, shield_integrity_after=0.0,
                    max_stability_before=self.max_stability, max_stability_after=self.max_stability,
                    metadata=tuple((k, v) for k, v in {"penalty": result.get("penalty"), "projected_max": result.get("projected_max")}.items()),
                ))
            return result

        s0, e0, i0, m0 = self.stability, self.shield_energy, self.shield_integrity, self.max_stability
        self.max_stability = result["projected_max"]
        self.reboot_count = result["reboot_num"]
        self.stability = self.max_stability
        self.shield_energy = self.max_shield_energy
        self.shield_integrity = min(1.0, self.shield_integrity + 0.2)  # Partial integrity restore on reboot
        self.shield_state = ShieldState.ACTIVE

        self.events.append(EventLog(
            tick=self.tick,
            tier=EventTier.REBOOT,
            event_type="REBOOT_SUCCESS",
            state_before=self.state,
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
        import json
        return json.dumps([e.to_dict() for e in self.events], indent=2)
