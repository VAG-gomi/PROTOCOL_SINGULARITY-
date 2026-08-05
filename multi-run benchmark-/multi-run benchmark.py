"""
================================================================================
PROTOCOL_SINGULARITY_v2 — Multi-Run Survival Benchmark
Constructed Version (Final)
================================================================================

This module implements a Monte Carlo survival benchmark that evaluates system
resilience through repeated independent test runs under stochastic adversarial
pressure. Every line of code is preceded by its causal narrative, per Layer 2
Hybrid Sentence Syntax.

Resolved [COGNITION_GAP] assumptions:
  1. max_ticks_per_run safety parameter prevents infinite survival loops.
  2. num_runs, recovery_rate, threat_range, and max_ticks_per_run are fully
     validated before execution.
  3. Each run uses an independent fresh AdversarialSystem instance.
  4. Statistical output includes mean, min, max, and standard deviation.
  5. The substrate is the fully constructed AdversarialSystem (all validation,
     idempotent locks, and audit narratives intact).
================================================================================
"""

import random
import statistics
from dataclasses import dataclass
from typing import List, Tuple, Union


# ==============================================================================
# BENCHMARK RESULT DATA CLASS
# ==============================================================================

@dataclass
class BenchmarkResult:
    """
    Immutable container for Monte Carlo survival benchmark outcomes.
    """
    # [Entity: benchmark design parameters]
    # --(encapsulation: structure statistical output for programmatic analysis)--> [State: result schema defined]
    num_runs: int
    average_lifespan: float
    min_lifespan: int
    max_lifespan: int
    std_dev: float
    raw_data: List[int]
    audit_log: List[str]


# ==============================================================================
# ADVERSARIAL SYSTEM (Fully Constructed Substrate)
# ==============================================================================

class AdversarialSystem:
    """
    Formal model of a resilient system under adversarial pressure with active
    self-healing capabilities bounded by design ceiling and collapse floor.
    """

    def __init__(
        self,
        max_stability: float,
        collapse_threshold: float,
        strain_ratio: float = 0.5,
        recovery_balance_threshold: float = 0.8,
    ):
        # [Entity: max_stability and collapse_threshold parameters]
        # --(validation: enforce ceiling must exceed failure floor)--> [State: verified baseline or exception]
        if max_stability <= collapse_threshold:
            raise ValueError(
                "[COGNITION_GAP]: max_stability must exceed collapse_threshold."
            )
        if collapse_threshold < 0:
            raise ValueError(
                "[COGNITION_GAP]: collapse_threshold must be non-negative."
            )
        if not (0 < strain_ratio <= 1):
            raise ValueError(
                "[COGNITION_GAP]: strain_ratio must be in (0, 1]."
            )
        if not (0 < recovery_balance_threshold <= 1):
            raise ValueError(
                "[COGNITION_GAP]: recovery_balance_threshold must be in (0, 1]."
            )

        # [Entity: validated parameters]
        # --(assignment to instance)--> [State: system substrate initialized]
        self.max_stability: float = float(max_stability)
        self.stability: float = float(max_stability)
        self.threshold: float = float(collapse_threshold)
        self.strain_ratio: float = float(strain_ratio)
        self.recovery_balance_threshold: float = float(recovery_balance_threshold)
        self.system_state: str = "BALANCED"

    def inject_threat(self, threat_magnitude: Union[int, float]) -> str:
        # [Entity: incoming threat parameter]
        # --(validation: ensure numeric and non-negative)--> [State: threat verified]
        if not isinstance(threat_magnitude, (int, float)) or threat_magnitude < 0:
            raise ValueError("[COGNITION_GAP]: threat_magnitude must be non-negative.")

        # [Entity: system state flag]
        # --(idempotency check)--> [State: collapse lock assessed]
        if self.system_state == "COLLAPSED":
            return f"[STATE LOCKED]: System already collapsed."

        # [Entity: current stability and validated threat]
        # --(subtraction: measure remaining structural margin)--> [State: net_equilibrium computed]
        net_equilibrium = self.stability - threat_magnitude

        # [Entity: net_equilibrium and collapse_threshold]
        # --(comparative evaluation: safety-margin breach check)--> [State: collapse condition assessed]
        if net_equilibrium < self.threshold:
            self.system_state = "COLLAPSED"
            self.stability = 0.0
            return f"[STATE SHIFT -> COLLAPSED]: Threat ({threat_magnitude}) breached threshold."

        # [Entity: threat_magnitude and current stability]
        # --(proportional comparison: strain tolerance check)--> [State: strain condition assessed]
        elif threat_magnitude > (self.stability * self.strain_ratio):
            self.system_state = "STRAINED"
            damage = threat_magnitude * 0.3
            self.stability -= damage
            return f"[STATE SHIFT -> STRAINED]: Absorbed {damage:.1f} damage. Remaining: {self.stability:.1f}."

        # [Entity: weak threat]
        # --(neutralization: no structural cost)--> [State: BALANCED maintained]
        else:
            self.system_state = "BALANCED"
            return f"[STATE MAINTAINED -> BALANCED]: Threat ({threat_magnitude}) neutralized."

    def auto_recovery_tick(self, recovery_rate: Union[int, float]) -> str:
        # [Entity: incoming recovery_rate parameter]
        # --(validation: ensure non-negative)--> [State: recovery_rate verified]
        if not isinstance(recovery_rate, (int, float)) or recovery_rate < 0:
            raise ValueError("[COGNITION_GAP]: recovery_rate must be non-negative.")

        # [Entity: system state flag]
        # --(collapse guard)--> [State: recovery eligibility assessed]
        if self.system_state == "COLLAPSED":
            return "[RECOVERY FAILED]: System is COLLAPSED."

        # [Entity: current stability and validated recovery_rate]
        # --(ceiling enforcement: min prevents exceeding max_stability)--> [State: new stability computed]
        old_stability = self.stability
        self.stability = min(self.max_stability, self.stability + recovery_rate)
        actual_restored = self.stability - old_stability

        # [Entity: current stability and recovery_balance_threshold]
        # --(threshold comparison: rebalancing assessment)--> [State: transition condition evaluated]
        if self.stability >= self.max_stability * self.recovery_balance_threshold and self.system_state == "STRAINED":
            self.system_state = "BALANCED"
            return f"[STATE RECOVERED -> BALANCED]: Restored +{actual_restored:.1f} stability."

        return f"[AUTO-RECOVERY]: Restored +{actual_restored:.1f} stability -> Current: {self.stability:.1f}/{self.max_stability:.1f}."


# ==============================================================================
# SURVIVAL BENCHMARK ENGINE
# ==============================================================================

class SurvivalBenchmark:
    """
    Monte Carlo framework for evaluating system resilience through repeated
    independent test runs under stochastic adversarial pressure.
    """

    # [SINGULARITY_HEADER]
    # Intent  : Evaluate systemic stability probabilistically through Monte Carlo
    #           simulation, quantifying average operational lifespan under
    #           unpredictable environmental noise across independent test runs.
    # State   : Benchmark holds [num_runs, threat_range, recovery_rate,
    #           max_ticks_per_run, system_config, audit_log, raw_data];
    #           expects [execution trigger].
    # Action  : Validate config → iterate outer loop (runs) → instantiate fresh
    #           system per run → iterate inner loop (ticks) → generate threat →
    #           inject → check collapse → recover → count ticks → record result
    #           → compute statistics → return BenchmarkResult.

    def __init__(
        self,
        num_runs: int,
        threat_range: Tuple[float, float],
        recovery_rate: float,
        max_ticks_per_run: int = 10000,
        max_stability: float = 100.0,
        collapse_threshold: float = 10.0,
        strain_ratio: float = 0.5,
        recovery_balance_threshold: float = 0.8,
    ):
        # [Entity: num_runs parameter]
        # --(validation: enforce Assumption 1 — at least one run for statistics)--> [State: run count verified]
        if num_runs < 1:
            raise ValueError(
                "[COGNITION_GAP]: num_runs must be >= 1 for meaningful statistics."
            )

        # [Entity: threat_range bounds]
        # --(validation: enforce Assumption 4 — well-ordered non-negative bounds)--> [State: threat bounds verified]
        min_threat, max_threat = threat_range
        if min_threat < 0 or max_threat < 0:
            raise ValueError(
                "[COGNITION_GAP]: threat_range bounds must be non-negative."
            )
        if min_threat > max_threat:
            raise ValueError(
                "[COGNITION_GAP]: threat_range must be well-ordered (min <= max)."
            )

        # [Entity: recovery_rate parameter]
        # --(validation: enforce Assumption 2 — non-negative restorative energy)--> [State: recovery rate verified]
        if recovery_rate < 0:
            raise ValueError(
                "[COGNITION_GAP]: recovery_rate must be non-negative."
            )

        # [Entity: max_ticks_per_run parameter]
        # --(validation: enforce Assumption 3 — at least one tick per run)--> [State: tick budget verified]
        if max_ticks_per_run < 1:
            raise ValueError(
                "[COGNITION_GAP]: max_ticks_per_run must be >= 1."
            )

        # [Entity: validated num_runs]
        # --(assignment to instance)--> [State: Monte Carlo sample size configured]
        self.num_runs: int = num_runs

        # [Entity: validated threat bounds]
        # --(assignment to instance)--> [State: stochastic sampling range configured]
        self.threat_min: float = float(min_threat)
        self.threat_max: float = float(max_threat)

        # [Entity: validated recovery_rate]
        # --(assignment to instance)--> [State: passive homeostatic energy configured]
        self.recovery_rate: float = float(recovery_rate)

        # [Entity: validated max_ticks_per_run]
        # --(assignment to instance)--> [State: per-run safety timeout configured]
        self.max_ticks_per_run: int = max_ticks_per_run

        # [Entity: system design parameters]
        # --(assignment to instance)--> [State: substrate configuration cached]
        self.max_stability: float = float(max_stability)
        self.collapse_threshold: float = float(collapse_threshold)
        self.strain_ratio: float = float(strain_ratio)
        self.recovery_balance_threshold: float = float(recovery_balance_threshold)

        # [Entity: empty list structures]
        # --(initialization: prepare ordered forensic containers)--> [State: raw_data and audit_log ready for capture]
        self.raw_data: List[int] = []
        self.audit_log: List[str] = []

    def run(self) -> BenchmarkResult:
        """
        Execute the Monte Carlo survival benchmark and return structured results.
        """
        # [Entity: simulation parameters and empty containers]
        # --(header generation: establish forensic trail origin)--> [State: audit_log initialized with session metadata]
        self.audit_log.append(
            "=========================================================="
        )
        self.audit_log.append(
            f"MONTE CARLO SURVIVAL BENCHMARK ({self.num_runs} RUNS)"
        )
        self.audit_log.append(
            f"Threat Range: [{self.threat_min:.1f}, {self.threat_max:.1f}] | "
            f"Recovery: {self.recovery_rate:.1f}/tick | "
            f"Max Ticks/Run: {self.max_ticks_per_run}"
        )
        self.audit_log.append(
            "=========================================================="
        )

        # [Entity: run index starting at 1]
        # --(iteration initiation: outer Monte Carlo loop begins)--> [State: loop entered for run 1]
        for run_id in range(1, self.num_runs + 1):
            # [Entity: validated design parameters]
            # --(instantiation: create independent fresh system per Assumption 5)--> [State: fresh AdversarialSystem initialized for current run]
            system = AdversarialSystem(
                max_stability=self.max_stability,
                collapse_threshold=self.collapse_threshold,
                strain_ratio=self.strain_ratio,
                recovery_balance_threshold=self.recovery_balance_threshold,
            )

            # [Entity: tick counter initialized to zero]
            # --(assignment to instance)--> [State: temporal index at origin for current run]
            ticks: int = 0

            # [Entity: system state flag, max_ticks_per_run limit, and tick counter]
            # --(loop guard: enforce termination on collapse or safety timeout)--> [State: inner while condition evaluated]
            while (
                system.system_state != "COLLAPSED"
                and ticks < self.max_ticks_per_run
            ):
                # [Entity: current tick counter]
                # --(increment: advance temporal index for current iteration)--> [State: tick counter updated]
                ticks += 1

                # [Entity: Python random module and threat bounds]
                # --(stochastic sampling: model unpredictable adversarial intensity)--> [State: threat_force generated for current tick]
                threat_force = round(random.uniform(self.threat_min, self.threat_max), 1)

                # [Entity: fresh AdversarialSystem instance and generated threat]
                # --(state transition execution: process adversarial event per formal protocol)--> [State: attack processed and system state updated]
                system.inject_threat(threat_force)

                # [Entity: system state flag post-threat]
                # --(emergency evaluation: detect collapse to bypass recovery)--> [State: termination condition assessed]
                if system.system_state == "COLLAPSED":
                    # [Entity: collapsed system]
                    # --(loop break: enforce immediate termination since dead systems cannot process recovery)--> [State: inner loop exited, no recovery executed]
                    break

                # [Entity: AdversarialSystem instance and configured recovery_rate]
                # --(restoration execution: process automatic homeostatic repair)--> [State: recovery processed and system state updated]
                system.auto_recovery_tick(self.recovery_rate)

            # [Entity: final tick count for current run]
            # --(capture: record survival lifespan in ordered list)--> [State: raw_data appended with run outcome]
            self.raw_data.append(ticks)

            # [Entity: run identity and tick count]
            # --(log entry creation: document run summary for forensic trace)--> [State: run summary appended to audit_log]
            if system.system_state == "COLLAPSED":
                self.audit_log.append(
                    f" Run #{run_id:2d} | System collapsed at T+{ticks:<5d} ticks"
                )
            else:
                self.audit_log.append(
                    f" Run #{run_id:2d} | System SURVIVED to T+{ticks:<5d} ticks (timeout)"
                )

        # [Entity: raw_data list of survival ticks]
        # --(aggregation: compute central tendency across all runs)--> [State: average_lifespan computed]
        average_survival: float = sum(self.raw_data) / len(self.raw_data)

        # [Entity: raw_data list of survival ticks]
        # --(aggregation: compute minimum boundary across all runs)--> [State: min_lifespan computed]
        min_survival: int = min(self.raw_data)

        # [Entity: raw_data list of survival ticks]
        # --(aggregation: compute maximum boundary across all runs)--> [State: max_lifespan computed]
        max_survival: int = max(self.raw_data)

        # [Entity: raw_data list of survival ticks]
        # --(aggregation: compute dispersion across all runs)--> [State: std_dev computed]
        std_dev: float = statistics.stdev(self.raw_data) if len(self.raw_data) > 1 else 0.0

        # [Entity: computed statistics and audit_log]
        # --(footer generation: summarize benchmark results for caller analysis)--> [State: audit_log finalized with statistical conclusion]
        self.audit_log.append(
            "----------------------------------------------------------"
        )
        self.audit_log.append("   FINAL STATISTICAL SUMMARY")
        self.audit_log.append(
            "----------------------------------------------------------"
        )
        self.audit_log.append(f" • Total Benchmark Runs : {self.num_runs}")
        self.audit_log.append(f" • Average Lifespan     : {average_survival:.2f} ticks")
        self.audit_log.append(f" • Shortest Run (Min)   : {min_survival} ticks")
        self.audit_log.append(f" • Longest Run (Max)    : {max_survival} ticks")
        self.audit_log.append(f" • Std Deviation        : {std_dev:.2f} ticks")
        self.audit_log.append(
            "=========================================================="
        )

        # [Entity: finalized statistics, raw_data, and audit_log]
        # --(composition: encapsulate all benchmark outcomes in immutable result object)--> [State: BenchmarkResult instantiated and returned]
        return BenchmarkResult(
            num_runs=self.num_runs,
            average_lifespan=average_survival,
            min_lifespan=min_survival,
            max_lifespan=max_survival,
            std_dev=std_dev,
            raw_data=self.raw_data.copy(),
            audit_log=self.audit_log.copy(),
        )


# ==============================================================================
# LAYER 3: GRAVITY CHECK (SurvivalBenchmark)
# ==============================================================================
# Origin —
#     This benchmark exists because single-run simulations cannot reveal the
#     probabilistic nature of system resilience. A system might collapse in 3
#     ticks or survive for 300 depending on the random threat sequence. The
#     Monte Carlo form captures the distribution of outcomes, revealing the
#     expected operational lifespan and the variance induced by environmental
#     unpredictability. The decoupled iteration (fresh instances per run)
#     ensures that state degradation from one run does not bias subsequent
#     runs, preserving statistical independence.
#
# Boundary —
#     · If num_runs < 1, ValueError prevents vacuous execution.
#     · If threat_range is inverted or negative, ValueError prevents impossible
#       stochastic generation.
#     · If recovery_rate is negative, ValueError prevents damaging "recovery".
#     · If max_ticks_per_run < 1, ValueError prevents degenerate runs.
#     · If a run reaches max_ticks_per_run without collapse, it is recorded as
#       a survival timeout — the system was too resilient for the threat profile.
#     · If the underlying AdversarialSystem is initialized with invalid params,
#       the constructor raises ValueError at birth, not under load.
#     · The inner loop breaks immediately upon collapse — recovery is bypassed.
#
# Equilibrium —
#     After run(), the caller receives a BenchmarkResult containing:
#       1. A complete ordered audit log of every run.
#       2. The average, min, max, and standard deviation of survival ticks.
#       3. The raw_data list (ordered by run_id) for custom analysis.
#     The benchmark operates on independent AdversarialSystem instances per run;
#     it does not mutate external state. The log is append-only and ordered by
#     run index, providing a forensic trail. There are no ambiguous outcomes —
#     every run terminates either in collapse or survival timeout.
# ==============================================================================


# ==============================================================================
# SIMULATION DEMONSTRATION
# ==============================================================================
if __name__ == "__main__":
    # [Entity: design requirements]
    # --(instantiation: create benchmark with 10 runs, [15,95] threat range, 12.0 recovery)--> [State: benchmark configured and ready]
    benchmark = SurvivalBenchmark(
        num_runs=10,
        threat_range=(15.0, 95.0),
        recovery_rate=12.0,
        max_ticks_per_run=10000,
        max_stability=100.0,
        collapse_threshold=10.0,
        strain_ratio=0.5,
        recovery_balance_threshold=0.8,
    )

    # [Entity: SurvivalBenchmark instance]
    # --(execution: run Monte Carlo campaign and capture structured output)--> [State: benchmark completed, results returned]
    result = benchmark.run()

    # [Entity: result.audit_log entries]
    # --(display: render ordered forensic record to stdout for human analysis)--> [State: benchmark results visible to operator]
    for line in result.audit_log:
        print(line)

    # [Entity: final metrics]
    # --(summary output: present terminal condition in isolated line for quick scanning)--> [State: operator informed of session conclusion]
    print(f"\n>>> OPERATOR SUMMARY: Avg={result.average_lifespan:.2f} | Min={result.min_lifespan} | Max={result.max_lifespan} | StdDev={result.std_dev:.2f}")
