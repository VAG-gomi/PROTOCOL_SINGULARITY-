"""
================================================================================
PROTOCOL_SINGULARITY_v2 — Multi-Wave Adversarial Simulation Engine
Constructed Version (Final)
================================================================================

This module extends the Adversarial Dynamics Engine with a temporal loop that
models sustained adversarial campaigns. Every line of code is preceded by its
causal narrative, per Layer 2 Hybrid Sentence Syntax.

Resolved [COGNITION_GAP] assumptions:
  1. Waves are temporally independent Markov events.
  2. Threat magnitudes are drawn from a uniform distribution over a fixed
     non-negative range; unseeded randomness models an unpredictable environment.
  3. Time delay between waves is purely cosmetic (simulation pacing).
  4. Simulation halts immediately upon collapse; no post-collapse events.
================================================================================
"""

import random
import time
from typing import List, Tuple, Union


# ==============================================================================
# ADVERSARIAL SYSTEM (Constructed Base — required substrate)
# ==============================================================================

class AdversarialSystem:
    """
    Formal model of a resilient system under continuous adversarial pressure.
    """

    # [SINGULARITY_HEADER]
    # Intent  : Transform a stable system under adversarial force into a discrete
    #           operational condition (BALANCED/STRAINED/COLLAPSED) while tracking
    #           irreversible structural degradation.
    # State   : System holds [Current_Stability, Collapse_Threshold, Strain_Ratio,
    #           State_Label]; expects [Threat_Magnitude].
    # Action  : Validate threat → check idempotent collapse lock → compute net
    #           equilibrium → evaluate against collapse threshold → determine state
    #           shift → apply proportional degradation if strained → return audit
    #           narrative.

    def __init__(
        self,
        core_stability: float,
        collapse_threshold: float,
        strain_ratio: float = 0.5,
    ):
        # [Entity: caller's design parameters]
        # --(validation: enforce base Assumption 2)--> [State: verified baseline or exception]
        if core_stability <= collapse_threshold:
            raise ValueError(
                "[COGNITION_GAP]: core_stability must exceed collapse_threshold; "
                "system cannot initialize in a pre-failed state."
            )

        # [Entity: caller's design parameters]
        # --(validation: enforce non-negative failure floor)--> [State: threshold verified]
        if collapse_threshold < 0:
            raise ValueError(
                "[COGNITION_GAP]: collapse_threshold must be non-negative."
            )

        # [Entity: validated core_stability]
        # --(assignment to instance)--> [State: structural energy initialized]
        self.stability: float = float(core_stability)

        # [Entity: validated collapse_threshold]
        # --(assignment to instance)--> [State: absolute failure floor established]
        self.threshold: float = float(collapse_threshold)

        # [Entity: strain_ratio parameter]
        # --(assignment to instance)--> [State: strain trigger threshold configured]
        self.strain_ratio: float = float(strain_ratio)

        # [Entity: initialized stability and threshold]
        # --(state label assignment)--> [State: system declared BALANCED at origin]
        self.system_state: str = "BALANCED"

    def inject_threat(self, threat_magnitude: Union[int, float]) -> str:
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


# ==============================================================================
# LAYER 3: GRAVITY CHECK (AdversarialSystem)
# ==============================================================================
# Origin —
#     This engine exists because dynamic systems do not fail all at once. They
#     degrade through repeated adversarial contact. The safety-margin collapse
#     model (stability - threat < threshold) captures the reality that resilient
#     systems require a minimum operational reserve; falling below that reserve
#     triggers cascading failure even if total capacity is not yet zero.
#
# Boundary —
#     · If threat_magnitude is negative or non-numeric, ValueError/TypeError
#       halts execution immediately — explicit failure, not silent corruption.
#     · If the system is already COLLAPSED, the method returns an idempotent
#       lock message without mutating state further.
#     · If core_stability <= collapse_threshold at initialization, ValueError
#       prevents creation of an invalid object — failure at birth, not under load.
#     · If strain accumulation drives stability close to threshold, the NEXT
#       threat triggers collapse via the safety-margin check — gradual until
#       suddenly terminal.
#
# Equilibrium —
#     After inject_threat, the system is in one of three known discrete states:
#       · BALANCED:  Stability unchanged; ready for next threat.
#       · STRAINED:  Stability permanently reduced but functional; more vulnerable.
#       · COLLAPSED: Stability zero and state locked; object is inert.
#     The function mutates internal state (necessary for cumulative degradation
#     tracking) but returns an audit string, leaving the caller free to log,
#     branch, or reinitialize. In all failure cases, exceptions propagate cleanly
#     or the collapsed lock engages — no undefined intermediate state.
# ==============================================================================


# ==============================================================================
# MULTI-WAVE SIMULATOR
# ==============================================================================

class WaveSimulator:
    """
    Orchestrates a temporally spaced sequence of adversarial events against an
    AdversarialSystem, producing an ordered forensic audit trail.
    """

    # [SINGULARITY_HEADER]
    # Intent  : Model a sustained adversarial campaign as discrete temporally
    #           separated events, revealing cumulative failure dynamics invisible
    #           in single-shot analysis.
    # State   : Simulator holds [AdversarialSystem, total_waves, threat_range,
    #           time_delay, audit_log]; expects [execution trigger].
    # Action  : Validate simulation config → initialize system → iterate over
    #           wave range → generate random threat → inject threat → append
    #           audit → check terminal collapse → delay → return complete log.

    def __init__(
        self,
        core_stability: float,
        collapse_threshold: float,
        total_waves: int,
        threat_range: Tuple[float, float],
        time_delay: float = 0.4,
        strain_ratio: float = 0.5,
    ):
        # [Entity: total_waves parameter]
        # --(validation: enforce simulation Assumption 1)--> [State: wave count verified positive]
        if total_waves < 1:
            raise ValueError(
                "[COGNITION_GAP]: total_waves must be >= 1; "
                "simulation requires at least one event to be meaningful."
            )

        # [Entity: threat_range bounds]
        # --(validation: enforce simulation Assumption 2)--> [State: threat bounds verified non-negative and well-ordered]
        min_threat, max_threat = threat_range
        if min_threat < 0 or max_threat < 0:
            raise ValueError(
                "[COGNITION_GAP]: threat_range bounds must be non-negative."
            )
        if min_threat > max_threat:
            raise ValueError(
                "[COGNITION_GAP]: threat_range must be well-ordered (min <= max)."
            )

        # [Entity: time_delay parameter]
        # --(validation: enforce non-negative latency)--> [State: delay verified cosmetic-only]
        if time_delay < 0:
            raise ValueError(
                "[COGNITION_GAP]: time_delay must be non-negative."
            )

        # [Entity: validated core_stability and collapse_threshold]
        # --(composition: instantiate formal adversarial substrate)--> [State: AdversarialSystem initialized]
        self.system = AdversarialSystem(
            core_stability=core_stability,
            collapse_threshold=collapse_threshold,
            strain_ratio=strain_ratio,
        )

        # [Entity: validated total_waves]
        # --(assignment to instance)--> [State: wave budget configured]
        self.total_waves: int = total_waves

        # [Entity: validated threat bounds]
        # --(assignment to instance)--> [State: stochastic sampling range configured]
        self.threat_min: float = float(min_threat)
        self.threat_max: float = float(max_threat)

        # [Entity: validated time_delay]
        # --(assignment to instance)--> [State: inter-wave latency configured]
        self.time_delay: float = float(time_delay)

        # [Entity: empty list structure]
        # --(initialization: prepare ordered forensic container)--> [State: audit_log ready for capture]
        self.audit_log: List[str] = []

    def run(self) -> Tuple[List[str], str, float]:
        """
        Execute the multi-wave simulation and return the complete audit trail.
        """
        # [Entity: simulation parameters and empty audit_log]
        # --(header generation: establish forensic trail origin)--> [State: audit_log initialized with session metadata]
        self.audit_log.append(
            "=================================================="
        )
        self.audit_log.append(
            f"ADVERSARIAL WAVE SIMULATION | Waves: {self.total_waves} | "
            f"Threat Range: [{self.threat_min:.1f}, {self.threat_max:.1f}]"
        )
        self.audit_log.append(
            "=================================================="
        )

        # [Entity: wave counter starting at 1]
        # --(iteration initiation: temporal event sequence begins)--> [State: loop entered for wave 1]
        for wave in range(1, self.total_waves + 1):
            # [Entity: Python random module and threat bounds]
            # --(stochastic sampling: model unpredictable adversarial intensity)--> [State: threat_magnitude generated for current wave]
            threat_magnitude = round(random.uniform(self.threat_min, self.threat_max), 1)

            # [Entity: wave identity and threat magnitude]
            # --(log entry creation: document incoming event for forensic trace)--> [State: wave header appended to audit_log]
            self.audit_log.append(f"\n--- WAVE {wave} | Time Tick T+{wave} ---")
            self.audit_log.append(
                f"[INCOMING VECTOR]: Threat magnitude = {threat_magnitude}"
            )

            # [Entity: AdversarialSystem instance and current threat]
            # --(state transition execution: process adversarial event per formal protocol)--> [State: result narrative produced and system state updated]
            result = self.system.inject_threat(threat_magnitude)

            # [Entity: result narrative]
            # --(audit capture: preserve causal outcome in ordered record)--> [State: result appended to audit_log]
            self.audit_log.append(result)

            # [Entity: system state flag]
            # --(terminal evaluation: detect irreversible collapse to prevent undefined continuation)--> [State: termination condition assessed]
            if self.system.system_state == "COLLAPSED":
                # [Entity: collapsed system and current wave index]
                # --(emergency halt: enforce idempotent terminal state on simulation loop)--> [State: loop broken, no further waves processed]
                self.audit_log.append(
                    f"\n[CRITICAL FAILURE]: Simulation halted at Wave {wave} "
                    f"due to total collapse."
                )
                break

            # [Entity: simulation clock and time_delay parameter]
            # --(temporal suspension: simulate inter-wave latency for realistic pacing)--> [State: execution paused, preserving causal ordering between events]
            time.sleep(self.time_delay)

        # [Entity: completed audit_log and final system metrics]
        # --(footer generation: summarize terminal condition for caller analysis)--> [State: audit_log finalized with session conclusion]
        self.audit_log.append(
            "\n=================================================="
        )
        self.audit_log.append(
            f"SIMULATION COMPLETE | Final State: {self.system.system_state} | "
            f"Final Stability: {self.system.stability:.1f}"
        )
        self.audit_log.append(
            "=================================================="
        )

        # [Entity: finalized audit_log, terminal state, and remaining stability]
        # --(return to caller: deliver complete forensic record and terminal metrics)--> [State: caller receives immutable simulation outcome]
        return self.audit_log, self.system.system_state, self.system.stability


# ==============================================================================
# LAYER 3: GRAVITY CHECK (WaveSimulator)
# ==============================================================================
# Origin —
#     This simulation exists because single-shot threat analysis cannot reveal
#     cumulative failure dynamics. Real adversarial campaigns (DDoS waves,
#     repeated physical assaults, iterative penetration testing) consist of
#     discrete events separated by time. The loop form captures the Markovian
#     property of sustained attacks: each wave's outcome depends only on the
#     current system state and the current threat, but the sequence reveals
#     emergent collapse thresholds invisible in isolated tests.
#
# Boundary —
#     · If total_waves < 1, ValueError prevents vacuous simulation.
#     · If threat_range is inverted or negative, ValueError prevents impossible
#       stochastic generation.
#     · If time_delay < 0, ValueError prevents temporal paradox.
#     · If the system collapses at wave K, the loop breaks immediately — no
#       post-collapse wave processing, no undefined state mutations.
#     · If the underlying AdversarialSystem is initialized with invalid params,
#       the constructor raises ValueError at birth, not under load.
#
# Equilibrium —
#     After run(), the caller receives:
#       1. A complete audit_log (ordered list of every event and transition)
#       2. The final system_state string (BALANCED, STRAINED, or COLLAPSED)
#       3. The final stability float
#     The simulator operates on its own AdversarialSystem instance; it does not
#     mutate external state. The log is append-only and ordered by wave index,
#     providing a forensic trail. In success (all waves survived), the system is
#     likely BALANCED or STRAINED with degraded stability. In failure (collapse),
#     the log ends at the collapse wave with a critical failure footer. There are
#     no ambiguous outcomes — the terminal state is always one of the three
#     discrete states.
# ==============================================================================


# ==============================================================================
# SIMULATION DEMONSTRATION
# ==============================================================================
if __name__ == "__main__":
    # [Entity: design requirements]
    # --(instantiation: create simulator with 100.0 stability, 10.0 threshold, 7 waves, [15,85] threat range)--> [State: simulator configured and ready]
    simulator = WaveSimulator(
        core_stability=100.0,
        collapse_threshold=10.0,
        total_waves=7,
        threat_range=(15.0, 85.0),
        time_delay=0.4,
    )

    # [Entity: WaveSimulator instance]
    # --(execution: run full temporal campaign and capture forensic output)--> [State: simulation completed, audit trail returned]
    audit_log, final_state, final_stability = simulator.run()

    # [Entity: audit_log entries]
    # --(display: render ordered forensic record to stdout for human analysis)--> [State: simulation results visible to operator]
    for line in audit_log:
        print(line)

    # [Entity: final metrics]
    # --(summary output: present terminal condition in isolated line for quick scanning)--> [State: operator informed of session conclusion]
    print(f"\n>>> OPERATOR SUMMARY: State={final_state} | Stability={final_stability:.1f}")