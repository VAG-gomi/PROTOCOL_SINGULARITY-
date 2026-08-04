"""
================================================================================
PROTOCOL_SINGULARITY_v2 — Threat + Active Recovery Simulation Engine
Constructed Version (Final)
================================================================================

This module extends the Adversarial Dynamics Engine with an active Recovery
Module that models restorative phases between adversarial events. Every line of
code is preceded by its causal narrative, per Layer 2 Hybrid Sentence Syntax.

Resolved [COGNITION_GAP] assumptions:
  1. Threat and recovery rates are strictly non-negative.
  2. max_stability replaces core_stability as the design ceiling.
  3. strain_ratio and recovery_balance_threshold are tunable parameters in (0,1].
  4. Recovery is capped at max_stability (hard physical limit).
  5. STRAINED -> BALANCED transition only triggers at or above the recovery
     balance threshold.
  6. Collapsed systems reject both threats and recovery (idempotent lock).
  7. Phases are temporally independent Markov events.
================================================================================
"""

import time
from typing import List, Tuple, Union, Dict, Any


# ==============================================================================
# ADVERSARIAL SYSTEM WITH RECOVERY MODULE
# ==============================================================================

class AdversarialSystem:
    """
    Formal model of a resilient system under adversarial pressure with active
    self-healing capabilities bounded by design ceiling and collapse floor.
    """

    # [SINGULARITY_HEADER]
    # Intent  : Transform a stable system under adversarial force into a discrete
    #           operational condition (BALANCED/STRAINED/COLLAPSED) while tracking
    #           irreversible structural degradation; additionally, restore degraded
    #           systems toward their design ceiling up to a rebalancing threshold.
    # State   : System holds [Current_Stability, Max_Stability, Collapse_Threshold,
    #           Strain_Ratio, Recovery_Balance_Threshold, State_Label]; expects
    #           [Threat_Magnitude] or [Recovery_Rate].
    # Action  : Validate input → check idempotent locks → compute transitions
    #           (degradation or restoration) → enforce ceilings/floors → assess
    #           state rebalance → return audit narrative.

    def __init__(
        self,
        max_stability: float,
        collapse_threshold: float,
        strain_ratio: float = 0.5,
        recovery_balance_threshold: float = 0.8,
    ):
        # [Entity: max_stability and collapse_threshold parameters]
        # --(validation: enforce Assumption 2 — ceiling must exceed failure floor)--> [State: verified baseline or exception]
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

        # [Entity: strain_ratio parameter]
        # --(validation: enforce Assumption 3 — meaningful strain detection bounds)--> [State: strain ratio verified in (0, 1]]
        if not (0 < strain_ratio <= 1):
            raise ValueError(
                "[COGNITION_GAP]: strain_ratio must be in (0, 1] for meaningful "
                "strain detection."
            )

        # [Entity: recovery_balance_threshold parameter]
        # --(validation: enforce Assumption 3 — meaningful rebalancing bounds)--> [State: recovery threshold verified in (0, 1]]
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
                "[COGNITION_GAP]: Negative threat_magnitude is outside Input Universe "
                "(restorative forces are not handled by inject_threat)."
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
                f"[STATE SHIFT -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) reduced equilibrium to {net_equilibrium:.1f}, "
                f"breaching threshold ({self.threshold}). Total structural failure. "
                f"Stability annihilated."
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
                f"[STATE SHIFT -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) exceeded {self.strain_ratio * 100:.0f}% "
                f"of current stability. System absorbed {damage:.1f} damage. "
                f"Remaining stability: {self.stability:.1f}."
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
                f"[STATE MAINTAINED -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) neutralized without degradation. "
                f"Stability intact at {self.stability:.1f}."
            )

    def recover_stability(self, recovery_rate: Union[int, float]) -> str:
        """
        Apply restorative energy to the system, enforcing the design ceiling
        and triggering state rebalancing when sufficient recovery is achieved.
        """
        # [Entity: incoming recovery_rate parameter]
        # --(type validation: ensure numeric input)--> [State: type-verified]
        if not isinstance(recovery_rate, (int, float)):
            raise TypeError(
                "[COGNITION_GAP]: recovery_rate must be a real number."
            )

        # [Entity: incoming recovery_rate parameter]
        # --(domain validation: enforce strictly restorative universe)--> [State: recovery_rate verified non-negative]
        if recovery_rate < 0:
            raise ValueError(
                "[COGNITION_GAP]: Negative recovery_rate is outside Input Universe "
                "(damaging events are handled by inject_threat, not recover_stability)."
            )

        # [Entity: system state flag]
        # --(collapse guard: enforce Rule A — collapsed systems cannot self-heal)--> [State: recovery eligibility assessed]
        if self.system_state == "COLLAPSED":
            # [Entity: collapsed system]
            # --(early return: prevent impossible self-healing on dead state)--> [State: caller informed of persistent failure]
            return (
                "[RECOVERY FAILED]: System is COLLAPSED. "
                "Internal self-healing is offline."
            )

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
                f"[STATE SHIFT -> {self.system_state}]: Restored +{actual_restored:.1f} stability. "
                f"Equilibrium restored ({self.stability:.1f}/{self.max_stability})."
            )

        # [Entity: recovery outcome without state transition]
        # --(return to caller)--> [State: caller informed of partial or idempotent recovery]
        return (
            f"[RECOVERY EXECUTED]: Restored +{actual_restored:.1f} stability. "
            f"Current stability: {self.stability:.1f}/{self.max_stability} ({self.system_state})."
        )


# ==============================================================================
# LAYER 3: GRAVITY CHECK (AdversarialSystem)
# ==============================================================================
# Origin —
#     This engine exists because dynamic systems (biological, infrastructural,
#     organizational) do not fail all at once, nor do they heal without bound.
#     They degrade through repeated adversarial contact and regenerate toward a
#     design ceiling between contacts. The safety-margin collapse model captures
#     the reality that resilient systems require a minimum operational reserve;
#     falling below that reserve triggers cascading failure. The recovery ceiling
#     (min with max_stability) captures the physical law that no system can
#     exceed its original design capacity without structural modification. The
#     rebalancing threshold captures the operational reality that "some stability"
#     is not enough to declare a system fully operational — confidence requires
#     a meaningful fraction of baseline capacity.
#
# Boundary —
#     · If threat_magnitude or recovery_rate is negative or non-numeric,
#       ValueError/TypeError halts execution immediately — explicit failure,
#       not silent corruption.
#     · If the system is already COLLAPSED, both methods return idempotent
#       lock/failure messages without mutating state further.
#     · If max_stability <= collapse_threshold at initialization, ValueError
#       prevents creation of an invalid object — failure at birth, not under load.
#     · If strain_ratio or recovery_balance_threshold is outside (0, 1],
#       ValueError prevents degenerate threshold logic.
#     · If recovery_rate is zero or the system is already at max_stability,
#       actual_restored becomes zero — the method returns an idempotent
#       "no change" narrative.
#     · If recovery_balance_threshold is set to 1.0, the system only rebalances
#       when fully restored to max_stability — the most conservative recovery
#       policy.
#
# Equilibrium —
#     After inject_threat, the system is in one of three known discrete states:
#       · BALANCED:  Stability unchanged or reaffirmed; ready for next threat.
#       · STRAINED:  Stability permanently reduced but functional; more vulnerable.
#       · COLLAPSED: Stability zero and state locked; object is inert.
#     After recover_stability, the system is in one of three known states:
#       · COLLAPSED: Unchanged (recovery was blocked).
#       · STRAINED:  Stability increased but remains below rebalancing threshold.
#       · BALANCED:  Stability increased to at or above threshold, triggering
#                    state transition from STRAINED.
#     Both methods mutate internal state (necessary for cumulative tracking) but
#     return audit strings. In all failure cases, exceptions propagate cleanly
#     or the collapsed lock engages — no undefined intermediate state.
# ==============================================================================


# ==============================================================================
# PHASE SIMULATOR (Attack + Recovery Orchestrator)
# ==============================================================================

class PhaseSimulator:
    """
    Orchestrates an alternating sequence of adversarial and restorative phases
    to model real-world campaigns where threats and recovery interleave.
    """

    # [SINGULARITY_HEADER]
    # Intent  : Orchestrate an alternating sequence of adversarial and restorative
    #           events to model real-world campaigns where threats and recovery
    #           phases interleave (e.g., attack→patch→attack→failover).
    # State   : Simulator holds [AdversarialSystem, scenario_phases, audit_log];
    #           expects [execution trigger].
    # Action  : Validate scenario → iterate phases → route to inject_threat or
    #           recover_stability → capture audit → apply delay → return complete
    #           forensic record.

    def __init__(
        self,
        max_stability: float,
        collapse_threshold: float,
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

        # [Entity: validated max_stability, collapse_threshold, and thresholds]
        # --(composition: instantiate formal adversarial substrate with recovery)--> [State: AdversarialSystem initialized]
        self.system = AdversarialSystem(
            max_stability=max_stability,
            collapse_threshold=collapse_threshold,
            strain_ratio=strain_ratio,
            recovery_balance_threshold=recovery_balance_threshold,
        )

        # [Entity: validated scenario list]
        # --(assignment to instance)--> [State: phase sequence configured]
        self.scenario: List[Dict[str, Any]] = scenario

        # [Entity: empty list structure]
        # --(initialization: prepare ordered forensic container)--> [State: audit_log ready for capture]
        self.audit_log: List[str] = []

    def run(self) -> Tuple[List[str], str, float]:
        """
        Execute the phase scenario and return the complete audit trail.
        """
        # [Entity: simulation parameters and empty audit_log]
        # --(header generation: establish forensic trail origin)--> [State: audit_log initialized with session metadata]
        self.audit_log.append(
            "=================================================="
        )
        self.audit_log.append(
            f"ADAPTIVE SIMULATION | Phases: {len(self.scenario)} | "
            f"Max Stability: {self.system.max_stability:.1f} | "
            f"Threshold: {self.system.threshold:.1f}"
        )
        self.audit_log.append(
            "=================================================="
        )

        # [Entity: phase index starting at 1]
        # --(iteration initiation: sequential campaign execution begins)--> [State: loop entered for phase 1]
        for phase_idx, phase in enumerate(self.scenario, start=1):
            # [Entity: current phase dictionary]
            # --(type extraction: determine event category)--> [State: phase_type identified]
            phase_type: str = phase.get("type", "").lower()

            # [Entity: phase_type string]
            # --(validation: enforce known phase categories)--> [State: routing eligibility verified]
            if phase_type not in ("attack", "recover"):
                raise ValueError(
                    f"[COGNITION_GAP]: Unknown phase type '{phase_type}' at phase {phase_idx}. "
                    f"Allowed types: 'attack', 'recover'."
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

            else:  # phase_type == "recover"
                # [Entity: recovery phase rate parameter]
                # --(extraction: obtain restorative intensity)--> [State: recovery_rate resolved]
                rate: float = float(phase.get("rate", 0.0))

                # [Entity: AdversarialSystem instance and recovery rate]
                # --(restoration execution: process recovery event per formal protocol)--> [State: recovery result produced and system state updated]
                result = self.system.recover_stability(rate)

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
            "\n=================================================="
        )
        self.audit_log.append(
            f"SIMULATION COMPLETE | Final State: {self.system.system_state} | "
            f"Final Stability: {self.system.stability:.1f}/{self.system.max_stability:.1f}"
        )
        self.audit_log.append(
            "=================================================="
        )

        # [Entity: finalized audit_log, terminal state, and remaining stability]
        # --(return to caller: deliver complete forensic record and terminal metrics)--> [State: caller receives immutable simulation outcome]
        return self.audit_log, self.system.system_state, self.system.stability


# ==============================================================================
# LAYER 3: GRAVITY CHECK (PhaseSimulator)
# ==============================================================================
# Origin —
#     This simulator exists because real adversarial campaigns are not pure
#     attack streams. Defenders patch, heal, and rebalance between waves. The
#     phase-alternation form captures the dynamic equilibrium of sustained
#     conflict: each attack degrades, each recovery rebuilds, and the net
#     trajectory determines whether the system survives the campaign or succumbs
#     to cumulative damage. The scenario-list architecture makes the campaign
#     fully configurable, revealing emergent collapse thresholds invisible in
#     isolated single-event tests.
#
# Boundary —
#     · If the scenario is empty, ValueError prevents vacuous execution.
#     · If an unknown phase type is encountered, ValueError halts immediately —
#       no undefined routing.
#     · If the system collapses during an attack phase, subsequent recovery
#       phases return idempotent failure narratives — the log continues, but
#       the system remains dead.
#     · If a delay is negative, it is treated as zero (non-blocking) rather
#       than raising an error, since negative sleep is harmless in Python.
#     · If the underlying AdversarialSystem is initialized with invalid params,
#       the constructor raises ValueError at birth, not under load.
#
# Equilibrium —
#     After run(), the caller receives:
#       1. A complete ordered audit log of every phase.
#       2. The final system_state string (BALANCED, STRAINED, or COLLAPSED).
#       3. The final stability float.
#     The simulator operates on its own AdversarialSystem instance; it does not
#     mutate external state. The log is append-only and ordered by phase index,
#     providing a forensic trail. In success, the system may be BALANCED or
#     STRAINED with partial degradation. In failure (collapse), the log reveals
#     the exact phase at which collapse occurred, and subsequent recovery
#     attempts are documented as failures. There are no ambiguous outcomes.
# ==============================================================================


# ==============================================================================
# SIMULATION DEMONSTRATION
# ==============================================================================
if __name__ == "__main__":
    # [Entity: design requirements]
    # --(scenario definition: specify alternating attack and recovery phases)--> [State: campaign configuration established]
    scenario = [
        {
            "type": "attack",
            "magnitude": 70.0,
            "label": "PHASE 1: Heavy Attack Wave",
            "delay": 0.3,
        },
        {
            "type": "recover",
            "rate": 15.0,
            "label": "PHASE 2: System Regeneration Cycle 1",
            "delay": 0.3,
        },
        {
            "type": "recover",
            "rate": 15.0,
            "label": "PHASE 3: System Regeneration Cycle 2",
            "delay": 0.3,
        },
        {
            "type": "attack",
            "magnitude": 110.0,
            "label": "PHASE 4: Critical Overwhelming Attack",
            "delay": 0.3,
        },
        {
            "type": "recover",
            "rate": 20.0,
            "label": "PHASE 5: Recovery Attempt Post-Collapse",
            "delay": 0.0,
        },
    ]

    # [Entity: scenario configuration and design parameters]
    # --(instantiation: create simulator with 100.0 max stability and 10.0 threshold)--> [State: simulator configured and ready]
    simulator = PhaseSimulator(
        max_stability=100.0,
        collapse_threshold=10.0,
        scenario=scenario,
        strain_ratio=0.5,
        recovery_balance_threshold=0.8,
    )

    # [Entity: PhaseSimulator instance]
    # --(execution: run full adaptive campaign and capture forensic output)--> [State: simulation completed, audit trail returned]
    audit_log, final_state, final_stability = simulator.run()

    # [Entity: audit_log entries]
    # --(display: render ordered forensic record to stdout for human analysis)--> [State: simulation results visible to operator]
    for line in audit_log:
        print(line)

    # [Entity: final metrics]
    # --(summary output: present terminal condition in isolated line for quick scanning)--> [State: operator informed of session conclusion]
    print(f"\n>>> OPERATOR SUMMARY: State={final_state} | Stability={final_stability:.1f}/{simulator.system.max_stability:.1f}")