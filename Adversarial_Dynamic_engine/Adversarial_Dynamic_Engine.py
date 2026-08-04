"""
================================================================================
PROTOCOL_SINGULARITY_v2 — Adversarial Dynamics Engine
Constructed Version (Final)
================================================================================

This module implements a formal causal reasoning model for dynamic systems
under continuous adversarial threat. Every line of code is preceded by its
causal narrative, per Layer 2 Hybrid Sentence Syntax.

Resolved [COGNITION_GAP] assumptions:
  1. Threats are strictly non-negative (restorative forces excluded).
  2. Collapse follows a safety-margin model: collapse triggers when
     (stability - threat) < threshold, not when threat > stability.
  3. Strain ratio is a tunable constructor parameter, default 0.5.
  4. Collapse is terminal; recovery requires external reinitialization.
================================================================================
"""

from typing import Union


# ==============================================================================
# LAYER 0: ONTOLOGICAL GROUNDING
# ==============================================================================
# · Input Universe:
#     A tuple of (threat_magnitude: float, system_handle: AdversarialSystem)
#     where threat_magnitude represents the intensity of an external adversarial
#     force (measured in abstract energy units) attempting to compromise a
#     resilient infrastructure (network, physical, or organizational).
#
# · Output Universe:
#     A descriptive string narrative reporting the discrete operational condition
#     (BALANCED, STRAINED, or COLLAPSED) and the updated internal state
#     (degraded or annihilated stability).
#
# · Assumptions:
#     1. threat_magnitude >= 0 — the Input Universe contains only destructive or
#        probing forces; restorative events are handled by a separate lifecycle
#        protocol.
#     2. core_stability > collapse_threshold >= 0 — the system must initialize
#        with structural energy strictly above its absolute failure floor.
#     3. Strain degradation is permanent (scarring model); stability never
#        auto-regenerates between threats without explicit external repair.
#
# · Gap Check:
#     If threat_magnitude < 0, raise ValueError (outside Input Universe).
#     If core_stability <= collapse_threshold, raise ValueError (system
#     initialized in an invalid pre-failed state).
#     If the system is already COLLAPSED, return an idempotent lock message.
# ==============================================================================


class AdversarialSystem:
    """
    Formal model of a resilient system under continuous adversarial pressure.
    """

    # ==========================================================================
    # LAYER 1: SINGULARITY HEADER
    # ==========================================================================
    # Intent  : Transform a stable system under adversarial force into a discrete
    #           operational condition (BALANCED/STRAINED/COLLAPSED) while tracking
    #           irreversible structural degradation.
    # State   : System holds [Current_Stability, Collapse_Threshold, Strain_Ratio,
    #           State_Label]; expects [Threat_Magnitude].
    # Action  : Validate threat → check idempotent collapse lock → compute net
    #           equilibrium → evaluate against collapse threshold → determine state
    #           shift → apply proportional degradation if strained → return audit
    #           narrative.
    # ==========================================================================

    def __init__(
        self,
        core_stability: float,
        collapse_threshold: float,
        strain_ratio: float = 0.5,
    ):
        # [Entity: caller's design parameters]
        # --(validation: enforce Assumption 2)-->
        # [State: verified baseline or exception]
        if core_stability <= collapse_threshold:
            raise ValueError(
                "[COGNITION_GAP]: core_stability must exceed collapse_threshold; "
                "system cannot initialize in a pre-failed state."
            )

        # [Entity: caller's design parameters]
        # --(validation: enforce non-negative failure floor)-->
        # [State: threshold verified]
        if collapse_threshold < 0:
            raise ValueError(
                "[COGNITION_GAP]: collapse_threshold must be non-negative."
            )

        # [Entity: validated core_stability]
        # --(assignment to instance)-->
        # [State: structural energy initialized]
        self.stability: float = float(core_stability)

        # [Entity: validated collapse_threshold]
        # --(assignment to instance)-->
        # [State: absolute failure floor established]
        self.threshold: float = float(collapse_threshold)

        # [Entity: strain_ratio parameter]
        # --(assignment to instance)-->
        # [State: strain trigger threshold configured]
        self.strain_ratio: float = float(strain_ratio)

        # [Entity: initialized stability and threshold]
        # --(state label assignment)-->
        # [State: system declared BALANCED at origin]
        self.system_state: str = "BALANCED"

    def inject_threat(self, threat_magnitude: Union[int, float]) -> str:
        """
        Process a single adversarial event and return an audit narrative.
        """
        # [Entity: incoming threat parameter]
        # --(type validation: ensure numeric input)-->
        # [State: type-verified]
        if not isinstance(threat_magnitude, (int, float)):
            raise TypeError(
                "[COGNITION_GAP]: threat_magnitude must be a real number."
            )

        # [Entity: incoming threat parameter]
        # --(domain validation: enforce Assumption 1)-->
        # [State: threat verified non-negative]
        if threat_magnitude < 0:
            raise ValueError(
                "[COGNITION_GAP]: Negative threat_magnitude is outside Input Universe "
                "(restorative forces are not handled by inject_threat)."
            )

        # [Entity: system state flag]
        # --(idempotency check: terminal states reject new events)-->
        # [State: collapse lock assessed]
        if self.system_state == "COLLAPSED":
            # [Entity: collapsed system]
            # --(early return: prevent undefined operations on dead state)-->
            # [State: caller informed of persistent failure]
            return (
                f"[STATE LOCKED -> {self.system_state}]: System has already collapsed. "
                f"Threat of {threat_magnitude} encounters total structural failure."
            )

        # [Entity: current stability and validated threat]
        # --(subtraction: measure remaining structural margin)-->
        # [State: net_equilibrium computed]
        net_equilibrium: float = self.stability - threat_magnitude

        # [Entity: net_equilibrium and collapse_threshold]
        # --(comparative evaluation: safety-margin breach check)-->
        # [State: collapse condition assessed]
        if net_equilibrium < self.threshold:
            # [Entity: system's operational state]
            # --(terminal transition: irreversible collapse per safety-margin model)-->
            # [State: COLLAPSED]
            self.system_state = "COLLAPSED"

            # [Entity: remaining stability energy]
            # --(total depletion: structural integrity annihilated)-->
            # [State: stability zeroed]
            self.stability = 0.0

            # [Entity: collapse narrative]
            # --(return to caller)-->
            # [State: caller informed of terminal failure with causal reason]
            return (
                f"[STATE SHIFT -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) reduced equilibrium to {net_equilibrium:.1f}, "
                f"breaching threshold ({self.threshold}). Total structural failure. "
                f"Stability annihilated."
            )

        # [Entity: threat_magnitude and current stability]
        # --(proportional comparison: assess if threat exceeds strain tolerance)-->
        # [State: strain condition assessed]
        elif threat_magnitude > (self.stability * self.strain_ratio):
            # [Entity: system's operational state]
            # --(degraded transition: partial damage, functionality preserved)-->
            # [State: STRAINED]
            self.system_state = "STRAINED"

            # [Entity: threat_magnitude]
            # --(proportional absorption: 30% of threat energy permanently scars structure)-->
            # [State: stability degraded by shock absorption]
            damage: float = threat_magnitude * 0.3
            self.stability -= damage

            # [Entity: strain narrative]
            # --(return to caller)-->
            # [State: caller informed of partial failure with remaining capacity]
            return (
                f"[STATE SHIFT -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) exceeded {self.strain_ratio * 100:.0f}% "
                f"of current stability. System absorbed {damage:.1f} damage. "
                f"Remaining stability: {self.stability:.1f}."
            )

        # [Entity: weak threat relative to stability and strain ratio]
        # --(neutralization: no structural cost)-->
        # [State: BALANCED maintained]
        else:
            # [Entity: system's operational state]
            # --(affirmation: no state change required)-->
            # [State: BALANCED reaffirmed]
            self.system_state = "BALANCED"

            # [Entity: equilibrium narrative]
            # --(return to caller)-->
            # [State: caller informed of successful defense]
            return (
                f"[STATE MAINTAINED -> {self.system_state}]: "
                f"Threat ({threat_magnitude}) neutralized without degradation. "
                f"Stability intact at {self.stability:.1f}."
            )


# ==============================================================================
# LAYER 3: GRAVITY CHECK
# ==============================================================================
# Origin —
#     This engine exists because dynamic systems (network infrastructure, power
#     grids, immune responses, organizational security) do not fail all at once.
#     They degrade through repeated adversarial contact. The function's exact
#     form — using a safety-margin collapse threshold
#     (stability - threat < threshold) rather than direct capacity exhaustion —
#     captures the reality that most resilient systems require a minimum
#     operational reserve; falling below that reserve triggers cascading failure
#     even if total capacity is not yet zero.
#
# Boundary —
#     · If threat_magnitude is negative or non-numeric, a ValueError or
#       TypeError halts execution immediately — the function does not proceed,
#       so the system fails explicitly, not silently.
#     · If the system is already COLLAPSED, the method returns an idempotent
#       lock message without mutating state further — no undefined operations
#       occur on a dead object.
#     · If core_stability <= collapse_threshold at initialization, ValueError
#       prevents creation of an invalid object — the failure happens at birth,
#       not under load.
#     · If strain accumulation drives stability close to threshold, the NEXT
#       threat will trigger collapse via the safety-margin check — degradation
#       is gradual until it is suddenly terminal.
#
# Equilibrium —
#     After inject_threat, the system is in one of three known discrete states:
#       · BALANCED:  Stability is unchanged; ready for next threat.
#       · STRAINED:  Stability permanently reduced but functional; more
#                    vulnerable to subsequent threats.
#       · COLLAPSED: Stability is zero and state is locked; object is inert.
#     The function mutates internal state (necessary for cumulative degradation
#     tracking) but returns an audit string, leaving the caller free to log,
#     branch, or reinitialize. In all failure cases, exceptions propagate cleanly
#     or the collapsed lock engages — the system never enters an undefined
#     intermediate state.
# ==============================================================================


# ==============================================================================
# SIMULATION DEMONSTRATION
# ==============================================================================
if __name__ == "__main__":
    # [Entity: design requirements]
    # --(instantiation: create system with 100.0 stability and 10.0 failure floor)-->
    # [State: core system initialized]
    core = AdversarialSystem(core_stability=100.0, collapse_threshold=10.0)

    print("=" * 60)
    print("ADVERSARIAL DYNAMICS ENGINE — SIMULATION")
    print("=" * 60)

    # 1. Minor Threat (System easily absorbs)
    print("\n[EVENT 1] Minor threat injected...")
    print(core.inject_threat(threat_magnitude=20.0))

    # 2. Moderate Threat (System strains and degrades permanently)
    print("\n[EVENT 2] Moderate threat injected...")
    print(core.inject_threat(threat_magnitude=60.0))

    # 3. Overwhelming Threat (Triggers safety-margin collapse)
    print("\n[EVENT 3] Overwhelming threat injected...")
    print(core.inject_threat(threat_magnitude=120.0))

    # 4. Post-collapse threat (Idempotent lock — no undefined behavior)
    print("\n[EVENT 4] Post-collapse threat injected...")
    print(core.inject_threat(threat_magnitude=5.0))

    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)