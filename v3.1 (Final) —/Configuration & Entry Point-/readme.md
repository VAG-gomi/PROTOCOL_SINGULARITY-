# PROTOCOL_SINGULARITY_v3.1 — Active Shielding / Defense Layer

## Engineering Branch — Modular Resilience with Active Defense

### What Changed from v3.0.3

**Active Shielding** — The shield is no longer a passive buffer. It is an active defense system with:
- **Energy**: Current absorption capacity (depletes and recharges)
- **Integrity**: Structural health 0.0–1.0 (degrades under heavy fire, repairs slowly)
- **Mode**: BALANCED / FORTRESS / EVASIVE (active defense posture with trade-offs)
- **State**: ACTIVE / DEGRADED / BREACHED (operational condition)

**Shield Mechanics**:
- Absorption efficiency scales with integrity (0.5× to 1.0× base)
- Mode modifiers: FORTRESS absorbs 1.5× but costs 1.3× energy and drains stability
- Breach mechanic: massive hits can breach the shield, causing 35% leak-through and heavy integrity damage
- Separate shield structural repair (independent from core repair)

### Architecture

```
config.py                    # All tunable parameters
protocol_engine/
  types.py                   # Base enums (no dependencies)
  simulation/
    threat.py                # ThreatGenerator
    shield.py                # compute_shield_absorption, compute_shield_recharge
    recovery.py              # compute_recovery
    reboot.py                # compute_reboot
  pipeline/
    planner.py               # plan_threat_impact with shield modes
    validator.py             # validate_plan
    executor.py              # commit_threat
  telemetry/
    events.py                # EventLog with shield telemetry
    metrics.py               # MetricsCollector
    visualization.py         # Visualizer (3-panel plot)
  core.py                    # SingularityCoreV3 with active shield
main.py                      # Driver demonstrating 3 shield modes
```

### Dependency Graph (one-way)

```
main
  ↓
core
  ↓
pipeline, simulation
  ↓
types
telemetry (depends on types only)
```

### Running

```bash
cd protocol_singularity_v31
python main.py
```

### Shield Modes

| Mode | Absorption | Energy Cost | Stability Effect | Use Case |
|---|---|---|---|---|
| BALANCED | 1.0× | 1.0× | None | General purpose |
| FORTRESS | 1.5× | 1.3× | -2.0 stability/tick | Heavy threat waves |
| EVASIVE | 0.6× | 0.7× | +3.0 stability/tick | Preserve core, dodge |

### Honest Status

**Research prototype / v1.0 engineering baseline.**

Not yet: extensively tested, benchmarked, formally verified.
Architecture is stable. Remaining work is engineering discipline.