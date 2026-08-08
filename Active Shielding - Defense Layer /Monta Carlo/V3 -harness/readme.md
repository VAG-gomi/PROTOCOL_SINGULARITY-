MC-v0.3 — Experimental Lab Tester

Monte Carlo Experimental Lab Tester for PROTOCOL_SINGULARITY

---

What Is MC-v0.3?

MC-v0.3 is an Experimental Lab Tester designed to measure and compare different versions of the "PROTOCOL_SINGULARITY" simulation system.

Its technical classification is:

«Paired Monte Carlo Experimental Harness»

Its practical role is:

«A laboratory instrument for controlled computational experiments.»

MC-v0.3 does not contain the theory of the simulator.

It does not redesign the simulator.

It does not optimize the simulator.

It does not decide which simulator is "correct."

Instead, it loads a simulator version as an external experimental target, subjects it to controlled conditions, records what happens, and produces reproducible evidence.

---

Core Principle

BUILD THE MEASURING INSTRUMENT.

DO NOT BUILD THE THEORY INTO THE MEASURING INSTRUMENT.

The simulator is the system under experiment.

MC-v0.3 is the observer.

This separation is intentional.

---

Architecture

                    EXPERIMENTAL LAB
                           │
                           ▼
                  ┌─────────────────┐
                  │     MC-v0.3     │
                  │  Lab Tester     │
                  └────────┬────────┘
                           │
                 Select experimental target
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       protocol_v35.py          protocol_v36...
              │                         │
              └────────────┬────────────┘
                           │
                    Controlled inputs
                           │
                           ▼
                 Paired OFF / ON runs
                           │
                           ▼
                    Measurements
                           │
                           ▼
                    Raw evidence
                           │
                           ▼
                     Statistics
                           │
                           ▼
                    Experiment report

---

Why "Lab Tester"?

MC-v0.3 is more than a conventional unit-test program.

A normal tester primarily asks:

«"Does this piece of software satisfy its expected behavior?"»

MC-v0.3 asks a broader experimental question:

«"What behavior does this simulator produce under controlled, repeated conditions, and how does that behavior compare with another configuration or version?"»

Therefore, Experimental Lab Tester is the human-facing name.

Internally, the system still contains conventional testing and verification components.

---

Why Monte Carlo?

Monte Carlo methods use repeated random sampling and statistical analysis to obtain numerical information about systems whose individual outcomes vary.

MC-v0.3 applies this idea to "PROTOCOL_SINGULARITY".

A single experiment is not treated as sufficient evidence.

Instead:

Randomized threat sequence
          ↓
      Simulation
          ↓
       Record
          ↓
      Repeat N times
          ↓
     Aggregate data
          ↓
     Compare results

The experiment can therefore examine the distribution of observed behavior rather than relying on one run.

---

Paired Experimental Design

The central comparison is a paired:

DEFENSE OFF
     vs
DEFENSE ON

For each replicate, MC-v0.3 attempts to provide both conditions with the same externally generated threat sequence.

Conceptually:

                  Same threat sequence
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          DEFENSE OFF           DEFENSE ON
              │                     │
              ▼                     ▼
           Result A              Result B
              │                     │
              └──────────┬──────────┘
                         ▼
                    Δ = ON - OFF

This allows the experiment to examine the effect of the defense condition while controlling the externally generated threat sequence.

---

Supported Simulator Targets

MC-v0.3 is designed to load simulator versions independently.

For example:

[1] v3.5
    → protocol_singularity_v35.py

[2] v3.6
    → protocol_singularity_v36_cog_alchemy.py

The target is selected at runtime.

This means MC-v0.3 does not need to become a different program every time a new simulator layer is created.

Future targets can be added as separate modules.

---

Version Separation

The architecture deliberately separates three different concepts:

SIMULATOR VERSION
    v3.5
    v3.6
    future versions

MC VERSION
    MC-v0.3

EXPERIMENT SIZE
    N=50
    N=1,000
    N=10,000
    N=50,000

These are independent.

For example:

MC-v0.3
    ├── v3.5 / N=50
    ├── v3.5 / N=10,000
    ├── v3.6 / N=50
    └── v3.6 / N=10,000

---

What MC-v0.3 Measures

Depending on the simulator interface, MC-v0.3 records quantities such as:

- lifespan
- stability
- shield energy
- shield integrity
- maximum stability
- breach events
- collapse events
- reboot events
- repair events
- defense mode switches
- decision cost
- heat loss
- structural damage
- conservation violations

The tester records these measurements.

It does not invent their meaning.

---

Validation

MC-v0.3 contains a separate verification layer.

Current validation includes checks for:

SYNTAX
EXECUTION
REPRODUCIBILITY
PAIRING
THREAT STREAM IDENTITY
CONFIGURATION ISOLATION
FAILURE VISIBILITY
RAW DATA PRESERVATION
NUMERICAL VALIDITY
NO HIDDEN OPTIMIZATION

These checks validate the experimental instrument itself.

They should not be confused with proof that the underlying simulator is physically or theoretically correct.

---

Raw Evidence

MC-v0.3 preserves experimental results instead of reducing everything immediately to a single conclusion.

The experiment produces:

RAW RESULTS
     ↓
STATISTICAL ANALYSIS
     ↓
SUMMARY

Raw results remain important because an aggregate number can hide individual failures, unusual runs, or invalid experiments.

Invalid pairs are therefore intended to remain visible.

---

Failure Philosophy

MC-v0.3 distinguishes between:

- correctness errors
- interface errors
- experiment configuration errors
- numerical errors
- simulation errors
- model limitations
- observed behavior

A failure should not automatically be interpreted as proof that the simulator is wrong.

Likewise, a successful run should not automatically be interpreted as proof that the simulator is correct.

The tester records what happened and classifies the evidence.

---

Sample Size

The default experiment is:

N = 50 paired replicates

This is intended as a pilot/default experiment, not as universal proof.

Larger experiments can be performed when greater sampling precision or stability analysis is desired:

50       Pilot
100      Small validation
1,000    Extended experiment
5,000    Statistical experiment
10,000   High-sample experiment
50,000   Deep experiment

Increasing the number of samples can reduce Monte Carlo sampling error, but a larger sample does not automatically make the underlying model correct.

---

What MC-v0.3 Does NOT Do

MC-v0.3 does not:

- modify the simulator's theory
- rewrite simulator algorithms
- optimize defense parameters automatically
- choose parameters to obtain a desired result
- manufacture missing data
- silently discard failed experiments
- declare a simulator correct merely because tests pass
- declare one version superior merely because its mean is larger
- replace scientific or engineering validation

Its purpose is measurement.

---

Example

Suppose MC-v0.3 compares v3.5 and v3.6.

The result might show:

v3.5

OFF lifespan: 8.86
ON lifespan:  8.86
Δ:            0.00

while v3.6 might show:

v3.6

OFF lifespan: 8.10
ON lifespan:  7.90
Δ:           -0.20

These are observations from the experiment.

They are not automatically a statement that:

v3.5 is better.

or:

v3.6 is worse.

Those conclusions require interpretation of the model, experimental assumptions, uncertainty, and the intended objective.

---

Reproducibility

MC-v0.3 uses explicit seeds and externally controlled threat sequences so experiments can be repeated.

For example:

Target:       v3.6
Base seed:    42
Runs:         50
Max ticks:    50

A repeated experiment with the same configuration should reproduce the same controlled threat sequences and corresponding experimental results, provided the simulator itself is deterministic under those conditions.

---

Future Architecture

The intended long-term structure is modular.

Instead of continually expanding one enormous simulator file, new layers can be developed separately:

PROTOCOL_SINGULARITY/
│
├── protocol_singularity_v35.py
├── protocol_singularity_v36_cog_alchemy.py
│
├── future_layer_A.py
├── future_layer_B.py
├── future_layer_C.py
│
├── mc_v03.py
│
└── README.md

MC-v0.3 should be able to observe these targets without incorporating their internal theory.

Eventually, validated layers can be composed into a production system.

The laboratory therefore remains separate from the system being constructed.

---

Design Philosophy

The project follows a strict separation:

THEORY
   ↓
SIMULATOR

EXPERIMENT
   ↓
MC-v0.3

OBSERVATION
   ↓
RAW EVIDENCE

ANALYSIS
   ↓
STATISTICS

INTERPRETATION
   ↓
HUMAN / SEPARATE ANALYSIS LAYER

This separation prevents the measuring instrument from quietly becoming part of the theory it is supposed to measure.

---

Current Identity

Name:
    MC-v0.3 — Experimental Lab Tester

Technical classification:
    Paired Monte Carlo Experimental Harness

Role:
    Observer / Experimental Instrument

Primary experiment:
    Controlled OFF vs ON comparison

Targets:
    PROTOCOL_SINGULARITY simulator versions

Default sample:
    N=50 paired replicates

Large-sample capability:
    1,000–50,000+ replicates

Core rule:
    OBSERVE THE SYSTEM.
    DO NOT BUILD THE THEORY INTO THE OBSERVER.

---

Status

MC-v0.3 — Experimental Lab Tester

The tester is designed to remain independent from the simulator versions it evaluates.

Its job is not to make the system look correct.

Its job is to measure what the system actually does, preserve the evidence, expose failures, and make controlled comparisons reproducible.