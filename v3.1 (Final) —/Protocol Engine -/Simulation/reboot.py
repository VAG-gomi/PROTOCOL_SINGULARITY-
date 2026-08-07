"""
protocol_engine/simulation/reboot.py
[MEASURED STATE] Emergency reboot mechanics.
"""
from typing import Dict, Any
from protocol_engine.types import SystemState, RebootMode


def compute_reboot(
    max_stability: float,
    threshold: float,
    state: SystemState,
    reboot_count: int,
    max_reboots: int,
    reboot_mode: RebootMode,
    penalty_pct: float,
) -> Dict[str, Any]:
    """Compute reboot outcome without mutation."""
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