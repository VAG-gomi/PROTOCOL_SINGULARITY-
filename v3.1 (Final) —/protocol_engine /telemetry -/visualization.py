"""
protocol_engine/telemetry/visualization.py
[DERIVED STATE] Resilience trajectory plotting.
"""
from typing import Optional
from .metrics import MetricsCollector


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
        axes[0].set_title("PROTOCOL_SINGULARITY_v3.1 — Active Shield Trajectory")
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
