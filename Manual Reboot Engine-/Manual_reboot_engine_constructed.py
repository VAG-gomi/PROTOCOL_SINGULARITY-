"""
================================================================================
PROTOCOL_SINGULARITY_v2 — Manual Reboot Engine
Constructed Version (Final)
================================================================================

This module extends the Adversarial Dynamics Engine with a Manual Reboot method
that models emergency hard-start interventions on collapsed systems, enforcing
finite reboot budgets and permanent structural capacity degradation. Every line
of code is preceded by its causal narrative, per Layer 2 Hybrid Sentence Syntax.

Resolved [COGNITION_GAP] assumptions:
  1. capacity_penalty_percent is in [0, 100].
  2. max_reboots >= 0.
  3. A failed reboot (post-reboot threshold burnout) still increments reboot_count.
  4. Non-collapsed reboots return idempotent skip messages.
  5. Post-reboot max_stability is permanently reduced (scarring model).
================================================================================
"""

import time
from typing import List, Tuple, Union, Dict, Any


# ==============================================================================
# ADVERSARIAL SYSTEM WITH RECOVERY & REBOOT (Constructed Base)
# ==============================================================================

class AdversarialSystem:
    """
    Formal model of a resilient system under adversarial pressure with active
    self-healing and emergency hard-start capabilities, bounded by design
    ceiling, collapse floor, and finite reboot budget.
    """

    # [SINGULARITY_HEADER]
    # Intent  : Transform a stable system under adversarial force into a discrete
    #           operational condition (BALANCED/STRAINED/COLLAPSED) while tracking
    #           irreversible structural degradation; restore degraded systems
    #           toward their design ceiling; and provide emergency hard-start
    #           interventions on collapsed systems at permanent capacity cost.
    # State   : System holds [Current_Stability, Max_Stability, Collapse_Threshold,
    #           Strain_Ratio, Recovery_Balance_Threshold, Reboot_Count,
    #           Max_Reboots, State_Label]; expects [Threat_Magnitude],
    #           [Recovery_Rate], or [Capacity_Penalty_Percent].
    # Action  : Validate input → check idempotent locks → compute transitions
    #           (degradation, restoration, or reboot) → enforce ceilings/floors
    #           and budgets → assess state rebalance → return audit narrative.

    def __init__(
        self,
        max_stability: float,
        collapse_threshold: float,
        max_reboots: int = 3,
        strain_ratio: float = 0.5,
        recovery_balance_threshold: float = 0.8,
    ):
        # [Entity: max_stability and collapse_threshold parameters]
        # --(validation: enforce Assumption 3 — ceiling must exceed failure floor)--> [State: verified baseline or exception]
        if max_stability <= collapse_threshold:
            raise ValueError(
                "[COGNITION_GAP]: max_stability must exceed collapse_threshold; "
                "system cannot initialize in a pre-failed state."
            )

        # [Entity: collapse_threshold parameter]
        # --(validation: enforce non-negative failure floor)--> [State: threshold verified]
        if collapse_threshold < 0:
            raise ValueError(
                "[COGNITION_GAP]: collapse_threshold must be non-negative."
            )

        # [Entity: max_reboots parameter]
        # --(validation: enforce Assumption 2 — finite non-negative hard-start budget)--> [State: reboot budget verified]
        if max_reboots < 0:
            raise ValueError(
                "[COGNITION_GAP]: max_reboots must be non-negative."
            )

        # [Entity: strain_ratio parameter]
        # --(validation: enforce meaningful strain detection bounds)--> [State: strain ratio verified in (0, 1]]
        if not (0 < strain_ratio <= 1):
            raise ValueError(
                "[COGNITION_GAP]: strain_ratio must be in (0, 1] for meaningful "
                "strain detection."
            )

        # [Entity: recovery_balance_threshold parameter]
        # --(validation: enforce meaningful rebalancing bounds)--> [State: recovery threshold verified in (0, 1]]
        if not (0 < recovery_balance_threshold <= 1):
            raise ValueError(
                "[COGNITION_GAP]: recovery_balance_threshold must be in (0, 1] for "
                "meaningful state rebalancing."
            )

        # [Entity: validated max_stability]
        # --(assignment to instance)--> [State: design ceiling established]
        self.max_stability: float = float(max_stability)

        # [Entity: validated max_stability]
        # --(assignment to instance)--> [State: current stability initialized at full capacity]
        self.stability: float = float(max_stability)

        # [Entity: validated collapse_threshold]
        # --(assignment to instance)--> [State: absolute failure floor established]
        self.threshold: float = float(collapse_threshold)

        # [Entity: validated strain_ratio]
        # --(assignment to instance)--> [State: strain trigger threshold configured]
        self.strain_ratio: float = float(strain_ratio)

        # [Entity: validated recovery_balance_threshold]
        # --(assignment to instance)--> [State: rebalancing trigger threshold configured]
        self.recovery_balance_threshold: float = float(recovery_balance_threshold)

        # [Entity: reboot counter initialized to zero]
        # --(assignment to instance)--> [State: hard-start budget consumption at origin]
        self.reboot_count: int = 0

        # [Entity: validated max_reboots]
        # --(assignment to instance)--> [State: maximum hard-start budget established]
        self.max_reboots: int = max_reboots

        # [Entity: initialized stability and threshold]
        # --(state label assignment)--> [State: system declared BALANCED at origin]
        self.system_state: str = "BALANCED"

    def inject_threat(self, threat_magnitude: Union[int, float]) -> str:
        """
        Process a single adversarial event and return an audit narrative.
        """
        # [Entity: incoming threat parameter]
        # --(type validation: ensure numeric input)--> [State: type-verified]
        if not isinstance(threat_magnitude, (int, float)):
            raise TypeError(
                "[COGNITION_GAP]: threat_magnitude must be a real number."
            )

        # [Entity: incoming threat parameter]
        # --(domain validation: enforce non-negative threat universe)--> [State: threat verified non-negative]
        if threat_magnitude < 0:
            raise ValueError(
                "[COGNITION_GAP]: Negative threat_magnitude is outside Input Universe."
            )

        # [Entity: system state flag]
        # --(idempotency check: terminal states reject new events)--> [State: collapse lock assessed]
        if self.system_state == "COLLAPSED":
            # [Entity: collapsed system]
            # --(early return: prevent undefined operations on dead state)--> [State: caller informed of persistent failure]
            return (
                f"[STATE LOCKED -> {self.system_state}]: System has already collapsed. "
                f"Threat of {threat_magnitude} encounters total structural failure."
            )

        # [Entity: current stability and validated threat]
        # --(subtraction: measure remaining structural margin)--> [State: net_equilibrium computed]
        net_equilibrium: float = self.stability - threat_magnitude

        # [Entity: net_equilibrium and collapse_threshold]
        # --(comparative evaluation: safety-margin breach check)--> [State: collapse condition assessed]
        if net_equilibrium < self.threshold:
            # [Entity: system's operational state]
            # --(terminal transition: irreversible collapse per safety-margin model)--> [State: COLLAPSED]
            self.system_state = "COLLAPSED"

            # [Entity: remaining stability energy]
            # --(total depletion: structural integrity annihilated)--> [State: stability zeroed]
            self.stability = 0.0

            # [Entity: collapse narrative]
            # --(return to caller)--> [State: caller informed of terminal failure with causal reason]
            return (
                f"💥 [CRITICAL SHIFT -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) reduced equilibrium to {net_equilibrium:.1f}, "
                f"breaching threshold ({self.threshold}). Total structural failure!"
            )

        # [Entity: threat_magnitude and current stability]
        # --(proportional comparison: assess if threat exceeds strain tolerance)--> [State: strain condition assessed]
        elif threat_magnitude > (self.stability * self.strain_ratio):
            # [Entity: system's operational state]
            # --(degraded transition: partial damage, functionality preserved)--> [State: STRAINED]
            self.system_state = "STRAINED"

            # [Entity: threat_magnitude]
            # --(proportional absorption: 30% of threat energy permanently scars structure)--> [State: stability degraded by shock absorption]
            damage: float = threat_magnitude * 0.3
            self.stability -= damage

            # [Entity: strain narrative]
            # --(return to caller)--> [State: caller informed of partial failure with remaining capacity]
            return (
                f"⚠️  [STATE SHIFT -> {self.system_state}]: "
                f"Absorbed heavy shock. Stability degraded to {self.stability:.1f}."
            )

        # [Entity: weak threat relative to stability and strain ratio]
        # --(neutralization: no structural cost)--> [State: BALANCED maintained]
        else:
            # [Entity: system's operational state]
            # --(affirmation: no state change required)--> [State: BALANCED reaffirmed]
            self.system_state = "BALANCED"

            # [Entity: equilibrium narrative]
            # --(return to caller)--> [State: caller informed of successful defense]
            return (
                f"🛡️  [STATE MAINTAINED -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) absorbed smoothly."
            )

    def auto_recovery_tick(self, recovery_rate: Union[int, float]) -> str:
        """
        Apply passive restorative energy to the system, enforcing the design
        ceiling and triggering state rebalancing when sufficient recovery is
        achieved.
        """
        # [Entity: incoming recovery_rate parameter]
        # --(type validation: ensure numeric input)--> [State: type-verified]
        if not isinstance(recovery_rate, (int, float)):
            raise TypeError(
                "[COGNITION_GAP]: recovery_rate must be a real number."
            )

        # [Entity: incoming recovery_rate parameter]
        # --(domain validation: enforce non-negative restorative universe)--> [State: recovery_rate verified non-negative]
        if recovery_rate < 0:
            raise ValueError(
                "[COGNITION_GAP]: Negative recovery_rate is outside Input Universe."
            )

        # [Entity: system state flag]
        # --(collapse guard: enforce Rule A — collapsed systems cannot self-heal)--> [State: recovery eligibility assessed]
        if self.system_state == "COLLAPSED":
            # [Entity: collapsed system]
            # --(early return: prevent impossible self-healing on dead state)--> [State: caller informed of persistent failure]
            return "❌ [RECOVERY FAILED]: System is COLLAPSED. Self-healing is offline."

        # [Entity: current stability and validated recovery_rate]
        # --(ceiling enforcement: apply Rule B — min prevents exceeding max_stability)--> [State: new stability computed within bounds]
        old_stability: float = self.stability
        self.stability = min(self.max_stability, self.stability + recovery_rate)

        # [Entity: old and new stability values]
        # --(difference calculation: measure actual restoration achieved)--> [State: actual_restored computed]
        actual_restored: float = self.stability - old_stability

        # [Entity: current stability, max_stability, and recovery_balance_threshold]
        # --(threshold comparison: assess if recovered capacity warrants state rebalancing)--> [State: transition condition evaluated]
        if (
            self.stability >= self.max_stability * self.recovery_balance_threshold
            and self.system_state == "STRAINED"
        ):
            # [Entity: system's operational state]
            # --(restorative transition: Rule C — sufficient recovery shifts STRAINED back to BALANCED)--> [State: BALANCED]
            self.system_state = "BALANCED"

            # [Entity: recovery narrative with state transition]
            # --(return to caller)--> [State: caller informed of full recovery and rebalancing]
            return (
                f"🟢 [STATE RECOVERED -> {self.system_state}]: "
                f"Restored +{actual_restored:.1f} stability ({self.stability:.1f}/{self.max_stability:.1f})."
            )

        # [Entity: recovery outcome without state transition]
        # --(return to caller)--> [State: caller informed of partial or idempotent recovery]
        return (
            f"⚡ [AUTO-RECOVERY]: Restored +{actual_restored:.1f} stability -> "
            f"Current: {self.stability:.1f}/{self.max_stability:.1f}."
        )

    def manual_reboot(self, capacity_penalty_percent: Union[int, float] = 20.0) -> str:
        """
        Execute an emergency hard-start intervention that overrides a COLLAPSED
        state, restoring operational function at a permanent structural cost and
        consuming one unit from the finite reboot budget.
        """
        # [Entity: incoming capacity_penalty_percent parameter]
        # --(type validation: ensure numeric input)--> [State: type-verified]
        if not isinstance(capacity_penalty_percent, (int, float)):
            raise TypeError(
                "[COGNITION_GAP]: capacity_penalty_percent must be a real number."
            )

        # [Entity: incoming capacity_penalty_percent parameter]
        # --(domain validation: enforce Assumption 1 — meaningful percentage bounds)--> [State: penalty percentage verified in [0, 100]]
        if not (0 <= capacity_penalty_percent <= 100):
            raise ValueError(
                "[COGNITION_GAP]: capacity_penalty_percent must be in [0, 100]."
            )

        # [Entity: reboot_count and max_reboots]
        # --(budget evaluation: enforce finite hard-start limit — Guard 1)--> [State: reboot eligibility assessed]
        if self.reboot_count >= self.max_reboots:
            # [Entity: exhausted reboot budget]
            # --(early return: prevent structural core burnout from overuse)--> [State: caller informed of permanent denial]
            return (
                f"🚫 [REBOOT DENIED]: Maximum reboots "
                f"({self.reboot_count}/{self.max_reboots}) reached. "
                f"Structural core burned out."
            )

        # [Entity: system state flag]
        # --(eligibility evaluation: enforce reboot reserved for collapsed state — Guard 2)--> [State: collapse requirement assessed]
        if self.system_state != "COLLAPSED":
            # [Entity: non-collapsed system]
            # --(early return: prevent unnecessary hard-start on operational system)--> [State: caller informed of idempotent skip]
            return (
                f"ℹ️ [REBOOT SKIPPED]: System is currently {self.system_state}. "
                f"Manual reboot is reserved for COLLAPSED state."
            )

        # [Entity: current max_stability and validated penalty percentage]
        # --(percentage calculation: compute permanent structural cost of hard-start)--> [State: penalty magnitude computed]
        penalty: float = self.max_stability * (capacity_penalty_percent / 100.0)

        # [Entity: current max_stability and computed penalty]
        # --(subtraction: apply permanent capacity degradation per scarring model — Assumption 4)--> [State: design ceiling permanently reduced]
        self.max_stability -= penalty

        # [Entity: reboot counter]
        # --(increment: consume one unit from finite hard-start budget)--> [State: reboot_count updated]
        self.reboot_count += 1

        # [Entity: new max_stability and collapse_threshold]
        # --(viability evaluation: enforce post-reboot structural integrity — Guard 3)--> [State: post-reboot viability assessed]
        if self.max_stability <= self.threshold:
            # [Entity: degraded max_stability below failure floor]
            # --(terminal transition: core capacity insufficient to sustain operation)--> [State: COLLAPSED re-triggered]
            self.system_state = "COLLAPSED"
            self.stability = 0.0

            # [Entity: burnout narrative]
            # --(return to caller)--> [State: caller informed of permanent structural burnout]
            return (
                f"💀 [REBOOT FAILED]: Core capacity ({self.max_stability:.1f}) "
                f"fell below minimum threshold ({self.threshold}). Permanent loss."
            )

        # [Entity: new max_stability]
        # --(assignment: reset current stability to degraded design ceiling)--> [State: stability restored to new baseline]
        self.stability = self.max_stability

        # [Entity: system's operational state]
        # --(state reset: restore operational status after successful hard-start)--> [State: BALANCED]
        self.system_state = "BALANCED"

        # [Entity: reboot narrative with cost and new baseline]
        # --(return to caller)--> [State: caller informed of successful reboot with permanent degradation]
        return (
            f"🔄 [REBOOT EXECUTED ({self.reboot_count}/{self.max_reboots})]: "
            f"Core state reset to BALANCED. Permanent structural cost: -{penalty:.1f} capacity. "
            f"New Max Baseline: {self.max_stability:.1f}."
        )


# ==============================================================================
# LAYER 3: GRAVITY CHECK (AdversarialSystem)
# ==============================================================================
# Origin —
#     This engine exists because dynamic systems (power grids, server clusters,
#     biological organisms) do not fail all at once, nor do they heal without
#     bound, nor can they be rebooted infinitely. They degrade through repeated
#     adversarial contact, regenerate toward a design ceiling, and can be
#     emergency-restarted a finite number of times before structural fatigue
#     renders them permanently inoperable. The safety-margin collapse model
#     captures the minimum operational reserve requirement. The recovery ceiling
#     (min with max_stability) captures the physical law that no system exceeds
#     its original design capacity. The reboot penalty captures the engineering
#     reality that hard starts induce thermal shock, capacitor wear, or tissue
#     scarring that permanently degrades maximum performance. The reboot cap
#     captures the finite fatigue life of any physical structure.
#
# Boundary —
#     · If threat_magnitude, recovery_rate, or capacity_penalty_percent is
#       negative or non-numeric, ValueError/TypeError halts execution immediately.
#     · If capacity_penalty_percent > 100, ValueError prevents impossible
#       over-annihilation.
#     · If the system is already COLLAPSED, inject_threat and auto_recovery_tick
#       return idempotent lock/failure messages.
#     · If reboot_count >= max_reboots, manual_reboot returns idempotent denial.
#     · If system_state != COLLAPSED, manual_reboot returns idempotent skip.
#     · If post-reboot max_stability <= threshold, the reboot triggers immediate
#       re-collapse — the core burned out during the hard-start attempt.
#     · If max_stability <= collapse_threshold at initialization, ValueError
#       prevents creation of an invalid object.
#     · If max_reboots < 0, ValueError prevents impossible negative budgets.
#     · If strain_ratio or recovery_balance_threshold is outside (0, 1],
#       ValueError prevents degenerate threshold logic.
#
# Equilibrium —
#     After inject_threat: BALANCED, STRAINED, or COLLAPSED.
#     After auto_recovery_tick: COLLAPSED (blocked), STRAINED (partial), or
#     BALANCED (rebalanced).
#     After manual_reboot: REBOOT DENIED (budget exhausted), REBOOT SKIPPED
#     (not collapsed), REBOOT FAILED (post-reboot burnout), or BALANCED with
#     permanently reduced max_stability.
#     All methods mutate internal state (necessary for cumulative tracking) but
#     return audit strings. In all failure cases, exceptions propagate cleanly
#     or idempotent locks engage — no undefined intermediate states.
# ==============================================================================


# ==============================================================================
# REBOOT DEMONSTRATION ORCHESTRATOR
# ==============================================================================

class RebootDemonstration:
    """
    Orchestrates a scripted scenario that exercises the full threat, recovery,
    and reboot lifecycle to validate the Manual Reboot Engine under controlled
    conditions.
    """

    # [SINGULARITY_HEADER]
    # Intent  : Validate the Manual Reboot Engine through a scripted scenario
    #           that triggers collapse, demonstrates recovery failure, executes
    #           reboots until budget exhaustion, and documents permanent capacity
    #           degradation.
    # State   : Orchestrator holds [AdversarialSystem, scenario_phases, audit_log];
    #           expects [execution trigger].
    # Action  : Initialize system → iterate phases → route to inject_threat,
    #           auto_recovery_tick, or manual_reboot → capture audit → apply
    #           delay → return complete forensic record.

    def __init__(
        self,
        max_stability: float,
        collapse_threshold: float,
        max_reboots: int,
        capacity_penalty_percent: float,
        scenario: List[Dict[str, Any]],
        strain_ratio: float = 0.5,
        recovery_balance_threshold: float = 0.8,
    ):
        # [Entity: scenario parameter]
        # --(validation: enforce at least one phase exists)--> [State: scenario verified non-empty]
        if not scenario:
            raise ValueError(
                "[COGNITION_GAP]: scenario must contain at least one phase."
            )

        # [Entity: validated design parameters and thresholds]
        # --(composition: instantiate formal adversarial substrate with reboot)--> [State: AdversarialSystem initialized]
        self.system = AdversarialSystem(
            max_stability=max_stability,
            collapse_threshold=collapse_threshold,
            max_reboots=max_reboots,
            strain_ratio=strain_ratio,
            recovery_balance_threshold=recovery_balance_threshold,
        )

        # [Entity: validated capacity_penalty_percent]
        # --(assignment to instance)--> [State: reboot penalty configured]
        self.capacity_penalty_percent: float = float(capacity_penalty_percent)

        # [Entity: validated scenario list]
        # --(assignment to instance)--> [State: phase sequence configured]
        self.scenario: List[Dict[str, Any]] = scenario

        # [Entity: empty list structure]
        # --(initialization: prepare ordered forensic container)--> [State: audit_log ready for capture]
        self.audit_log: List[str] = []

    def run(self) -> Tuple[List[str], str, float, float, int]:
        """
        Execute the reboot demonstration and return the complete audit trail,
        final state, final stability, final max_stability, and reboot count.
        """
        # [Entity: simulation parameters and empty audit_log]
        # --(header generation: establish forensic trail origin)--> [State: audit_log initialized with session metadata]
        self.audit_log.append(
            "=========================================================="
        )
        self.audit_log.append(
            f"MANUAL REBOOT DEMONSTRATION | Max Stability: {self.system.max_stability:.1f} | "
            f"Threshold: {self.system.threshold:.1f} | Max Reboots: {self.system.max_reboots}"
        )
        self.audit_log.append(
            "=========================================================="
        )

        # [Entity: phase index starting at 1]
        # --(iteration initiation: sequential demonstration execution begins)--> [State: loop entered for phase 1]
        for phase_idx, phase in enumerate(self.scenario, start=1):
            # [Entity: current phase dictionary]
            # --(type extraction: determine event category)--> [State: phase_type identified]
            phase_type: str = phase.get("type", "").lower()

            # [Entity: phase_type string]
            # --(validation: enforce known phase categories)--> [State: routing eligibility verified]
            if phase_type not in ("attack", "recover", "reboot"):
                raise ValueError(
                    f"[COGNITION_GAP]: Unknown phase type '{phase_type}' at phase {phase_idx}. "
                    f"Allowed types: 'attack', 'recover', 'reboot'."
                )

            # [Entity: phase label or default identifier]
            # --(extraction: obtain human-readable phase description)--> [State: phase label resolved]
            label: str = phase.get("label", f"Phase {phase_idx}")

            # [Entity: phase identity and label]
            # --(log entry creation: document phase boundary for forensic trace)--> [State: phase header appended to audit_log]
            self.audit_log.append(f"\n--- {label} ---")

            # [Entity: phase_type and phase data]
            # --(conditional routing: dispatch to appropriate causal handler)--> [State: execution path selected]
            if phase_type == "attack":
                # [Entity: attack phase magnitude parameter]
                # --(extraction: obtain threat intensity)--> [State: threat_magnitude resolved]
                magnitude: float = float(phase.get("magnitude", 0.0))

                # [Entity: AdversarialSystem instance and threat magnitude]
                # --(state transition execution: process adversarial event per formal protocol)--> [State: attack result produced and system state updated]
                result = self.system.inject_threat(magnitude)

            elif phase_type == "recover":
                # [Entity: recovery phase rate parameter]
                # --(extraction: obtain restorative intensity)--> [State: recovery_rate resolved]
                rate: float = float(phase.get("rate", 0.0))

                # [Entity: AdversarialSystem instance and recovery rate]
                # --(restoration execution: process recovery event per formal protocol)--> [State: recovery result produced and system state updated]
                result = self.system.auto_recovery_tick(rate)

            else:  # phase_type == "reboot"
                # [Entity: reboot phase penalty parameter or default]
                # --(extraction: obtain penalty percentage)--> [State: penalty resolved]
                penalty: float = float(
                    phase.get("penalty", self.capacity_penalty_percent)
                )

                # [Entity: AdversarialSystem instance and penalty percentage]
                # --(hard-start execution: process reboot event per formal protocol)--> [State: reboot result produced and system state updated]
                result = self.system.manual_reboot(penalty)

            # [Entity: result narrative]
            # --(audit capture: preserve causal outcome in ordered record)--> [State: result appended to audit_log]
            self.audit_log.append(result)

            # [Entity: phase delay parameter]
            # --(temporal suspension: simulate inter-phase latency for realistic pacing)--> [State: execution paused, preserving causal ordering between phases]
            delay: float = float(phase.get("delay", 0.0))
            if delay > 0:
                time.sleep(delay)

        # [Entity: completed audit_log and final system metrics]
        # --(footer generation: summarize terminal condition for caller analysis)--> [State: audit_log finalized with session conclusion]
        self.audit_log.append(
            "\n=========================================================="
        )
        self.audit_log.append(
            f"FINAL SYSTEM STATUS: {self.system.system_state} | "
            f"STABILITY: {self.system.stability:.1f}/{self.system.max_stability:.1f} | "
            f"REBOOTS USED: {self.system.reboot_count}/{self.system.max_reboots}"
        )
        self.audit_log.append(
            "=========================================================="
        )

        # [Entity: finalized audit_log and terminal metrics]
        # --(return to caller: deliver complete forensic record and terminal metrics)--> [State: caller receives immutable simulation outcome]
        return (
            self.audit_log,
            self.system.system_state,
            self.system.stability,
            self.system.max_stability,
            self.system.reboot_count,
        )


# ==============================================================================
# LAYER 3: GRAVITY CHECK (RebootDemonstration)
# ==============================================================================
# Origin —
#     This demonstration exists because the Manual Reboot Engine introduces
#     complex lifecycle dynamics (threat → collapse → recovery failure → reboot
#     → re-threat → re-collapse → reboot denial) that cannot be validated through
#     isolated unit tests. The scripted phase architecture makes the full lifecycle
#     explicit and reproducible, revealing edge cases such as post-reboot
#     immediate re-collapse or budget exhaustion.
#
# Boundary —
#     · If the scenario is empty, ValueError prevents vacuous execution.
#     · If an unknown phase type is encountered, ValueError halts immediately.
#     · If the system collapses during an attack phase, subsequent recovery
#       phases return idempotent failures, and reboot phases consume budget.
#     · If a reboot triggers post-reboot burnout, the system remains COLLAPSED
#       and subsequent reboots may be denied due to budget exhaustion or
#       non-collapsed skip logic.
#     · If the underlying AdversarialSystem is initialized with invalid params,
#       the constructor raises ValueError at birth, not under load.
#
# Equilibrium —
#     After run(), the caller receives:
#       1. A complete ordered audit log of every phase.
#       2. The final system_state string.
#       3. The final stability float.
#       4. The final max_stability float (degraded by reboots).
#       5. The final reboot_count integer.
#     The log is append-only and ordered by phase index, providing a forensic
#     trail of the full threat-recovery-reboot lifecycle. There are no ambiguous
#     outcomes.
# ==============================================================================


# ==============================================================================
# SIMULATION DEMONSTRATION
# ==============================================================================
if __name__ == "__main__":
    # [Entity: design requirements]
    # --(scenario definition: specify full lifecycle phases to exercise reboot engine)--> [State: demonstration configuration established]
    scenario = [
        {
            "type": "attack",
            "magnitude": 120.0,
            "label": "PHASE 1: Overwhelming Threat Injected",
            "delay": 0.0,
        },
        {
            "type": "recover",
            "rate": 15.0,
            "label": "PHASE 2: Attempting Auto-Recovery",
            "delay": 0.0,
        },
        {
            "type": "reboot",
            "penalty": 20.0,
            "label": "PHASE 3: Executing First Manual Reboot",
            "delay": 0.0,
        },
        {
            "type": "attack",
            "magnitude": 90.0,
            "label": "PHASE 4: Second Attack Forces Collapse",
            "delay": 0.0,
        },
        {
            "type": "reboot",
            "penalty": 20.0,
            "label": "PHASE 5: Executing Second Manual Reboot",
            "delay": 0.0,
        },
        {
            "type": "attack",
            "magnitude": 70.0,
            "label": "PHASE 6: Third Attack Forces Collapse",
            "delay": 0.0,
        },
        {
            "type": "reboot",
            "penalty": 20.0,
            "label": "PHASE 7: Attempting Third Manual Reboot",
            "delay": 0.0,
        },
    ]

    # [Entity: scenario configuration and design parameters]
    # --(instantiation: create demonstration with 100.0 max stability, 10.0 threshold, 2 max reboots, 20% penalty)--> [State: demonstration configured and ready]
    demo = RebootDemonstration(
        max_stability=100.0,
        collapse_threshold=10.0,
        max_reboots=2,
        capacity_penalty_percent=20.0,
        scenario=scenario,
        strain_ratio=0.5,
        recovery_balance_threshold=0.8,
    )

    # [Entity: RebootDemonstration instance]
    # --(execution: run full lifecycle demonstration and capture forensic output)--> [State: demonstration completed, audit trail returned]
    (
        audit_log,
        final_state,
        final_stability,
        final_max_stability,
        final_reboot_count,
    ) = demo.run()

    # [Entity: audit_log entries]
    # --(display: render ordered forensic record to stdout for human analysis)--> [State: demonstration results visible to operator]
    for line in audit_log:
        print(line)

    # [Entity: final metrics]
    # --(summary output: present terminal condition in isolated line for quick scanning)--> [State: operator informed of session conclusion]
    print(
        f"\n>>> OPERATOR SUMMARY: State={final_state} | "
        f"Stability={final_stability:.1f}/{final_max_stability:.1f} | "
        f"Reboots={final_reboot_count}/{demo.system.max_reboots}"
    )