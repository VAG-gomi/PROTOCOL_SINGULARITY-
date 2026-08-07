"""
protocol_engine/types.py
Base enums and types. No dependencies. Imported by all modules.
"""
from enum import Enum, auto


class SystemState(Enum):
    BALANCED = auto()
    STRAINED = auto()
    COLLAPSED = auto()


class RebootMode(Enum):
    STRICT_MATH = auto()
    SAFETY_GUARD = auto()


class ShieldState(Enum):
    """[MEASURED STATE] Shield operational condition."""
    ACTIVE = auto()
    DEGRADED = auto()      # integrity < 0.5
    BREACHED = auto()      # temporarily offline after massive hit
    OVERCHARGED = auto()   # boosted mode, drains stability


class ShieldMode(Enum):
    """[MEASURED STATE] Active defense posture."""
    BALANCED = auto()      # standard absorption/recharge
    FORTRESS = auto()      # high absorption, high cost, drains stability
    EVASIVE = auto()       # low absorption, preserves stability, fast core recovery


class EventTier(Enum):
    THREAT = auto()
    SHIELD = auto()
    CORE = auto()
    RECOVERY = auto()
    REPAIR = auto()
    REBOOT = auto()
    VALIDATION = auto()
