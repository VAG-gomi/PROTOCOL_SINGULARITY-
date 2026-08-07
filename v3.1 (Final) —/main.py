"""
PROTOCOL_SINGULARITY_v3.1 — Main Driver
Active Shielding / Defense Layer with modular architecture.
"""
import json
from config import SimulationConfig
from protocol_engine.core import SingularityCoreV3
from protocol_engine.simulation.threat import ThreatGenerator
from protocol_engine.telemetry.metrics import MetricsCollector
from protocol_engine.telemetry.visualization import Visualizer
from protocol_engine.types import SystemState, RebootMode, ShieldMode


def run_simulation(
    config: SimulationConfig,
    mode: RebootMode = RebootMode.SAFETY_GUARD,
    shield_mode: ShieldMode = ShieldMode.BALANCED,
    max_ticks: int = 30,
    verbose: bool = True,
    visualize: bool = True,
    save_plot: str = "/mnt/agents/output/v31_trajectory.png",
) -> dict:
    """[DETERMINISTIC] Modular simulation driver with active shielding."""
    core = SingularityCoreV3(config)
    core.reboot_mode = mode
    core.set_shield_mode(shield_mode)

    threats = ThreatGenerator(core._rng, config.threat_low, config.threat_high)
    metrics = MetricsCollector()
    viz = Visualizer(metrics)

    if verbose:
        print("=" * 70)
        print("PROTOCOL_SINGULARITY_v3.1 — ACTIVE SHIELDING SIMULATION")
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
                        save_plot="/mnt/agents/output/v31_balanced.png")

    print("\n" + "=" * 70)
    print("RUN 2: FORTRESS SHIELD MODE")
    print("=" * 70)
    r2 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.FORTRESS,
                        save_plot="/mnt/agents/output/v31_fortress.png")

    print("\n" + "=" * 70)
    print("RUN 3: EVASIVE SHIELD MODE")
    print("=" * 70)
    r3 = run_simulation(config, mode=RebootMode.SAFETY_GUARD, shield_mode=ShieldMode.EVASIVE,
                        save_plot="/mnt/agents/output/v31_evasive.png")
