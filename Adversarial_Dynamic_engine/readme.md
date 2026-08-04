# PROTOCOL_SINGULARITY_v2 — Adversarial Dynamics Engine

**Constructed Version | Final**

---

## 1. What This Is

This project is a **formal causal reasoning engine** that models how resilient systems degrade under continuous adversarial pressure. It is not merely a state machine — it is a protocol-driven implementation where **every line of code is preceded by a causal narrative** that ties real-world entities to operations and outcomes.

Built under **PROTOCOL_SINGULARITY_v2 (Strengthened, Kimi-Compatible)**, the engine enforces four mandatory layers:

| Layer | Name | Purpose |
|-------|------|---------|
| **0** | Ontological Grounding | Pre-execution cognitive gate: define Input/Output universes, 3 explicit assumptions, and halt conditions. |
| **1** | Singularity Header | Declare Intent, State, and Action before any logic executes. |
| **2** | Hybrid Sentence Syntax | Every code line: `[Entity] --(Causal Operation, reason)--> [Resultant State]` |
| **3** | Gravity Check | Origin (why this form?), Boundary (graceful failure modes), Equilibrium (stable baseline). |

---

## 2. The Core Equation

```
Equilibrium = Stability - Threat
```

- **Threat (T)**: External force, noise, or attack pushing the system out of balance.
- **Stability (S)**: Structural energy available to absorb or neutralize force.
- **State (Σ)**: Operational condition resulting from interaction: `BALANCED`, `STRAINED`, or `COLLAPSED`.

---

## 3. Resolved [COGNITION_GAP] Items

During construction, four assumptions were undefined in the First Draft. They were resolved as follows:

| # | Gap | Resolution |
|---|-----|------------|
| 1 | **Negative threats**: Can `threat_magnitude` be negative (restorative force)? | **Resolved**: Threats are strictly `≥ 0`. Restorative forces require a separate lifecycle protocol. |
| 2 | **Collapse semantics**: Capacity-exhaustion vs. safety-margin model? | **Resolved**: Safety-margin model — collapse triggers when `(stability - threat) < threshold`, preserving the draft's math. |
| 3 | **Strain threshold**: Is `0.5` a universal constant or tunable? | **Resolved**: Tunable constructor parameter `strain_ratio`, default `0.5`. |
| 4 | **Post-collapse behavior**: Can the system recover? | **Resolved**: Terminal collapse. Recovery requires external reinitialization. |

---

## 4. Architecture

### 4.1 Class: `AdversarialSystem`

```python
AdversarialSystem(
    core_stability: float,      # Initial structural energy
    collapse_threshold: float,   # Absolute failure floor
    strain_ratio: float = 0.5   # % of stability that triggers strain
)
```

### 4.2 Method: `inject_threat(threat_magnitude)`

Processes a single adversarial event and returns an audit narrative.

**State Transitions:**

```
                    ┌─────────────────────────────────────┐
                    │  threat < 0 or non-numeric          │
                    │  → ValueError / TypeError           │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  system_state == "COLLAPSED"        │
                    │  → Idempotent lock message          │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
        ┌─────────────────────────────────────────────────────────────┐
        │  net_equilibrium = stability - threat                       │
        │  if net_equilibrium < threshold                             │
        │     → COLLAPSED (stability = 0.0)                         │
        │  elif threat > stability * strain_ratio                     │
        │     → STRAINED (stability -= threat * 0.3)                │
        │  else                                                     │
        │     → BALANCED (stability unchanged)                      │
        └─────────────────────────────────────────────────────────────┘
```

---

## 5. Usage

### 5.1 Basic Simulation

```python
from adversarial_dynamics_engine_constructed import AdversarialSystem

# Initialize: 100.0 stability, 10.0 collapse threshold
core = AdversarialSystem(core_stability=100.0, collapse_threshold=10.0)

# Event 1: Minor threat (absorbed)
print(core.inject_threat(20.0))
# → [STATE MAINTAINED -> BALANCED]: Threat (20.0) neutralized...

# Event 2: Moderate threat (strains system)
print(core.inject_threat(60.0))
# → [STATE SHIFT -> STRAINED]: Threat (60.0) exceeded 50%...

# Event 3: Overwhelming threat (collapse)
print(core.inject_threat(120.0))
# → [STATE SHIFT -> COLLAPSED]: Threat (120.0) reduced equilibrium...

# Event 4: Post-collapse (idempotent lock)
print(core.inject_threat(5.0))
# → [STATE LOCKED -> COLLAPSED]: System has already collapsed...
```

### 5.2 Run the Built-in Demo

```bash
python adversarial_dynamics_engine_constructed.py
```

---

## 6. Expected Output

```
============================================================
ADVERSARIAL DYNAMICS ENGINE — SIMULATION
============================================================

[EVENT 1] Minor threat injected...
[STATE MAINTAINED -> BALANCED]: Threat (20.0) neutralized without degradation. Stability intact at 100.0.

[EVENT 2] Moderate threat injected...
[STATE SHIFT -> STRAINED]: Threat (60.0) exceeded 50% of current stability. System absorbed 18.0 damage. Remaining stability: 82.0.

[EVENT 3] Overwhelming threat injected...
[STATE SHIFT -> COLLAPSED]: Threat (120.0) reduced equilibrium to -38.0, breaching threshold (10.0). Total structural failure. Stability annihilated.

[EVENT 4] Post-collapse threat injected...
[STATE LOCKED -> COLLAPSED]: System has already collapsed. Threat of 5.0 encounters total structural failure.

============================================================
SIMULATION COMPLETE
============================================================
```

---

## 7. Gravity Check (Layer 3)

### Origin
This engine exists because dynamic systems (network infrastructure, power grids, immune responses, organizational security) do not fail all at once. They degrade through repeated adversarial contact. The safety-margin collapse model captures the reality that most resilient systems require a minimum operational reserve; falling below that reserve triggers cascading failure even if total capacity is not yet zero.

### Boundary
- **Invalid input**: Negative or non-numeric threats raise `ValueError` / `TypeError` — explicit failure, no silent corruption.
- **Pre-failed initialization**: `core_stability <= collapse_threshold` raises `ValueError` at birth, not under load.
- **Terminal state lock**: Post-collapse, `inject_threat()` returns an idempotent message without mutating a dead object.
- **Gradual-then-sudden failure**: Strain accumulation drives stability toward the threshold; the *next* threat triggers collapse.

### Equilibrium
After `inject_threat`, the system is in one of three known discrete states:

| State | Stability | Behavior |
|-------|-----------|----------|
| `BALANCED` | Unchanged | Ready for next threat. |
| `STRAINED` | Permanently reduced | Functional but more vulnerable. |
| `COLLAPSED` | Zero, locked | Object is inert; requires reinitialization. |

The function mutates internal state (necessary for cumulative degradation tracking) but returns an audit string, leaving the caller free to log, branch, or reinitialize. The system never enters an undefined intermediate state.

---

## 8. File Manifest

| File | Description |
|------|-------------|
| `adversarial_dynamics_engine_constructed.py` | Full engine with all 4 protocol layers, type annotations, and runnable demo. |
| `README.md` | This file — construction documentation and usage guide. |

---

## 9. Protocol Compliance Certificate

| Layer | Status | Evidence |
|-------|--------|----------|
| **Layer 0** | ✅ Complete | Module docstring defines Input/Output Universe, 3 Assumptions, Gap Checks. Constructor validates all assumptions. |
| **Layer 1** | ✅ Complete | `# [SINGULARITY_HEADER]` block present with Intent, State, Action. |
| **Layer 2** | ✅ Complete | Every meaningful line follows `[Entity] --(Causal Operation, reason)--> [Resultant State]`. |
| **Layer 3** | ✅ Complete | Origin, Boundary (4 modes), and Equilibrium (3 terminal states) documented. |

**No steps skipped. No gaps unresolved.**

---

*Constructed under PROTOCOL_SINGULARITY_v2 (Strengthened, Kimi-Compatible)*