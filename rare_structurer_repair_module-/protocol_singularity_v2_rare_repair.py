import random
import time
from typing import Optional


class AdversarialSystem:
    def __init__(self, max_stability: float = 100.0, collapse_threshold: float = 10.0, max_reboots: int = 2):
        # [Entity: max_reboots parameter] --(assumption validation #1)--> [State: confirmed recoverable lifecycle or exception]
        if max_reboots < 1:
            raise ValueError("[COGNITION_GAP] max_reboots must be >= 1 for recoverable lifecycle")

        # [Entity: max_stability & collapse_threshold parameters] --(assumption validation #2)--> [State: confirmed valid birth state or exception]
        if max_stability <= collapse_threshold:
            raise ValueError("[COGNITION_GAP] original_max_capacity must exceed collapse_threshold; system born in invalid state")

        # [Entity: validated max_stability parameter] --(immutable ceiling lock)--> [State: original_max_capacity anchor established]
        self.original_max_capacity = max_stability

        # [Entity: validated max_stability parameter] --(mutable ceiling assignment)--> [State: current max_stability baseline]
        self.max_stability = max_stability

        # [Entity: max_stability ceiling] --(full charge initialization)--> [State: operational stability pool at capacity]
        self.stability = max_stability

        # [Entity: collapse_threshold parameter] --(critical floor assignment)--> [State: irreversible failure boundary established]
        self.threshold = collapse_threshold

        # [Entity: healthy birth expectation] --(state initialization)--> [State: BALANCED operational mode]
        self.system_state = "BALANCED"

        # [Entity: reboot counter] --(initialization)--> [State: zero exhausted reboots]
        self.reboot_count = 0

        # [Entity: max_reboots parameter] --(budget lock)--> [State: finite recovery budget established]
        self.max_reboots = max_reboots

    def inject_threat(self, threat_magnitude: float) -> str:
        # [Entity: threat_magnitude argument] --(assumption validation #3: non-negative check)--> [State: sanitized physical force or exception]
        if threat_magnitude < 0:
            raise ValueError("[COGNITION_GAP] threat_magnitude must be non-negative; negative forces violate physical model")

        # [Entity: current stability pool & incoming threat force] --(net equilibrium calculation)--> [State: projected post-impact energy level]
        net_equilibrium = self.stability - threat_magnitude

        # [Entity: net_equilibrium & threshold boundary] --(collapse causality check)--> [State: COLLAPSED if boundary breached]
        if net_equilibrium < self.threshold:
            self.system_state = "COLLAPSED"
            self.stability = 0.0
            return f"💥 [CRITICAL SHIFT -> COLLAPSED]: Threat ({threat_magnitude:.1f}) destroyed structural boundary!"

        # [Entity: threat_magnitude & current stability] --(severe shock ratio check: >50%)--> [State: STRAINED if impact exceeds half capacity]
        elif threat_magnitude > (self.stability * 0.5):
            self.system_state = "STRAINED"
            # [Entity: threat force] --(partial absorption penalty: 30% bleed-through)--> [State: reduced stability pool]
            self.stability -= (threat_magnitude * 0.3)
            return f"⚠️  [STATE SHIFT -> STRAINED]: Heavy shock absorbed. Remaining stability: {self.stability:.1f}."

        # [Entity: threat_magnitude & stability buffer] --(smooth absorption causality)--> [State: unchanged system_state with intact pool]
        else:
            return f"🛡️  [STATE MAINTAINED -> {self.system_state}]: Threat ({threat_magnitude:.1f}) absorbed smoothly."

    def auto_recovery_tick(self, recovery_rate: float) -> str:
        # [Entity: recovery_rate argument] --(assumption validation #3 extension)--> [State: sanitized maintenance energy or exception]
        if recovery_rate < 0:
            raise ValueError("[COGNITION_GAP] recovery_rate must be non-negative; negative maintenance violates thermodynamics")

        # [Entity: system_state] --(operational guard check)--> [State: blocked recovery if COLLAPSED]
        if self.system_state == "COLLAPSED":
            return "❌ [RECOVERY FAILED]: System is offline."

        # [Entity: current stability pool] --(snapshot for delta calculation)--> [State: old_stability reference captured]
        old_stability = self.stability

        # [Entity: current stability & recovery_rate & max_stability ceiling] --(capped addition)--> [State: replenished stability pool]
        self.stability = min(self.max_stability, self.stability + recovery_rate)

        # [Entity: old_stability & new stability] --(delta computation)--> [State: restored amount quantified]
        restored = self.stability - old_stability

        # [Entity: current stability & 80% ceiling ratio & STRAINED state] --(recovery threshold check)--> [State: BALANCED if healed sufficiently]
        if self.stability >= (self.max_stability * 0.8) and self.system_state == "STRAINED":
            self.system_state = "BALANCED"
            return f"🟢 [STATE RECOVERED -> BALANCED]: Restored +{restored:.1f} stability ({self.stability:.1f}/{self.max_stability:.1f})."

        # [Entity: restored amount & current metrics] --(log generation)--> [State: operational recovery report emitted]
        return f"⚡ [AUTO-RECOVERY]: Restored +{restored:.1f} stability -> Current: {self.stability:.1f}/{self.max_stability:.1f}."

    def rare_structural_repair(self, chance_percent: float = 15.0, repair_amount: float = 8.0) -> str:
        # [Entity: chance_percent & repair_amount arguments] --(assumption validation #3 extension)--> [State: sanitized repair parameters or exception]
        if chance_percent < 0 or repair_amount < 0:
            raise ValueError("[COGNITION_GAP] repair parameters must be non-negative")

        # [Entity: system_state] --(operational guard check)--> [State: blocked repair if COLLAPSED]
        if self.system_state == "COLLAPSED":
            return "❌ [REPAIR SKIPPED]: Cannot perform core structural repair while COLLAPSED."

        # [Entity: max_stability & original_max_capacity] --(ceiling completeness check)--> [State: skip if already at perfect baseline]
        if self.max_stability >= self.original_max_capacity:
            return "✨ [REPAIR SKIPPED]: Core capacity is already at maximum ceiling (100.0)."

        # [Entity: random uniform generator] --(probabilistic roll in [0,100])--> [State: stochastic outcome determined]
        roll = random.uniform(0.0, 100.0)

        # [Entity: roll result & chance_percent threshold] --(success condition evaluation)--> [State: repair triggered or idle]
        if roll <= chance_percent:
            # [Entity: current max_stability] --(snapshot for delta)--> [State: old_max reference captured]
            old_max = self.max_stability

            # [Entity: old_max & repair_amount & original_max_capacity] --(capped ceiling rebuild)--> [State: incremented max_stability]
            self.max_stability = min(self.original_max_capacity, self.max_stability + repair_amount)

            # [Entity: old_max & new max_stability] --(delta computation)--> [State: repaired amount quantified]
            repaired = self.max_stability - old_max

            # [Entity: repaired metrics] --(log generation)--> [State: rare success report emitted]
            return (
                f"🔧 [RARE STRUCTURAL REPAIR TRIGGERED!]: Core ceiling rebuilt by +{repaired:.1f} capacity! "
                f"New Max Baseline: {self.max_stability:.1f}/{self.original_max_capacity:.1f}."
            )

        # [Entity: failed roll outcome] --(idle state preservation)--> [State: no structural change]
        else:
            return "⏳ [STRUCTURAL SCAN]: Core repair idle."

    def manual_reboot(self, capacity_penalty_percent: float = 20.0) -> str:
        # [Entity: capacity_penalty_percent argument] --(assumption validation #3 extension)--> [State: sanitized fatigue parameter or exception]
        if capacity_penalty_percent < 0:
            raise ValueError("[COGNITION_GAP] capacity_penalty_percent must be non-negative")

        # [Entity: reboot_count & max_reboots] --(budget exhaustion check)--> [State: blocked if recovery limit reached]
        if self.reboot_count >= self.max_reboots:
            return f"🚫 [REBOOT FAILED]: Max reboots reached ({self.reboot_count}/{self.max_reboots}). Core burned out."

        # [Entity: system_state] --(state guard check)--> [State: blocked if not COLLAPSED]
        if self.system_state != "COLLAPSED":
            return f"ℹ️  [REBOOT SKIPPED]: System is currently {self.system_state}."

        # [Entity: current max_stability & penalty ratio] --(structural fatigue calculation)--> [State: degraded ceiling computed]
        penalty = self.max_stability * (capacity_penalty_percent / 100.0)

        # [Entity: current max_stability & penalty] --(ceiling reduction)--> [State: permanently reduced max_stability]
        self.max_stability -= penalty

        # [Entity: reboot_count] --(increment)--> [State: consumed one recovery budget unit]
        self.reboot_count += 1

        # [Entity: new max_stability & threshold] --(post-reboot viability check)--> [State: COLLAPSED if below floor]
        if self.max_stability <= self.threshold:
            self.system_state = "COLLAPSED"
            self.stability = 0.0
            return f"💀 [REBOOT FAILED]: New capacity ({self.max_stability:.1f}) fell below threshold ({self.threshold})."

        # [Entity: viable max_stability] --(full charge reset)--> [State: restored stability pool to new ceiling]
        self.stability = self.max_stability

        # [Entity: recovered system] --(state promotion)--> [State: BALANCED operational mode restored]
        self.system_state = "BALANCED"

        # [Entity: reboot metrics] --(log generation)--> [State: recovery report emitted]
        return (
            f"🔄 [AUTO-REBOOT EXECUTED ({self.reboot_count}/{self.max_reboots})]: "
            f"Reset to BALANCED | Penalty: -{penalty:.1f} max capacity | New Max: {self.max_stability:.1f}"
        )


def run_repair_simulation(max_ticks: Optional[int] = None) -> None:
    # [Entity: simulation parameters] --(system instantiation)--> [State: adversarial system at full health]
    system = AdversarialSystem(max_stability=100.0, collapse_threshold=10.0, max_reboots=2)

    # [Entity: time counter] --(initialization)--> [State: tick = 1]
    tick = 1

    # [Entity: maintenance configuration] --(assignment)--> [State: recovery_rate = 12.0]
    recovery_rate = 12.0

    # [Entity: simulation banner strings] --(stdout emission)--> [State: user informed of simulation start]
    print("=" * 58)
    print("   AUTOMATED ENGINE WITH RARE CORE REPAIR (PROTOCOL_v2)")
    print("=" * 58)

    # [Entity: tick counter & optional max_ticks boundary] --(loop guard)--> [State: simulation cycle active]
    while True:
        # [Entity: tick value] --(time slice announcement)--> [State: user informed of current tick]
        print(f"\n--- TIME TICK T+{tick} ---")

        # [Entity: random uniform generator] --(threat generation in [25.0, 95.0])--> [State: stochastic threat_force determined]
        threat_force = round(random.uniform(25.0, 95.0), 1)

        # [Entity: threat_force value] --(stdout emission)--> [State: user informed of incoming threat magnitude]
        print(f"[EVENT 1: THREAT]: Attack magnitude = {threat_force}")

        # [Entity: system & threat_force] --(causal threat injection)--> [State: system state potentially shifted]
        print(f"   └── {system.inject_threat(threat_force)}")

        # [Entity: system_state] --(collapse branch check)--> [State: reboot path or healing path selected]
        if system.system_state == "COLLAPSED":
            # [Entity: collapse event] --(alert emission)--> [State: user warned of critical failure]
            print("🚨 [CRITICAL ALERT]: Collapse detected! Triggering automated hard reboot...")

            # [Entity: system & penalty configuration] --(reboot attempt)--> [State: system potentially recovered or terminally failed]
            reboot_msg = system.manual_reboot(capacity_penalty_percent=25.0)
            print(f"   └── {reboot_msg}")

            # [Entity: post-reboot system_state] --(terminal check)--> [State: break if permanently destroyed]
            if system.system_state == "COLLAPSED":
                print(f"\n💀 [TERMINAL FAILURE]: All reboots exhausted. System permanently destroyed at Tick T+{tick}.")
                break

        # [Entity: non-collapsed system_state] --(healing branch)--> [State: recovery and repair attempted]
        else:
            # [Entity: system & recovery_rate] --(routine maintenance)--> [State: stability partially or fully restored]
            print(f"   └── {system.auto_recovery_tick(recovery_rate)}")

            # [Entity: system & repair parameters] --(rare structural audit)--> [State: max_stability potentially rebuilt]
            repair_msg = system.rare_structural_repair(chance_percent=25.0, repair_amount=10.0)
            print(f"   └── {repair_msg}")

        # [Entity: tick] --(increment)--> [State: next time slice prepared]
        tick += 1

        # [Entity: optional max_ticks parameter] --(safety limit check)--> [State: controlled termination if bound reached]
        if max_ticks is not None and tick > max_ticks:
            print(f"\n⏹️  [SIMULATION HALT]: max_ticks ({max_ticks}) reached.")
            break

        # [Entity: time module] --(temporal pacing: 400ms)--> [State: human-readable delay inserted]
        time.sleep(0.4)

    # [Entity: simulation conclusion metrics] --(summary emission)--> [State: final state reported to user]
    print("\n" + "=" * 58)
    print(f"SIMULATION TERMINATED | Total Lifespan: {tick} Ticks")
    print(f"Final Max Capacity: {system.max_stability:.1f}/{system.original_max_capacity:.1f}")
    print("=" * 58)


if __name__ == "__main__":
    # [Entity: script entry point] --(simulation launch)--> [State: repair simulation executing]
    run_repair_simulation()