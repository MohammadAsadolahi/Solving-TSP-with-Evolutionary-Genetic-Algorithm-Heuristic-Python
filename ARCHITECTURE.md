# Architecture & Design Document

## System Overview

This document provides an in-depth architectural breakdown of the Genetic Algorithm TSP Solver, detailing component responsibilities, data flow, and the evolutionary pipeline.

---

## Component Diagram

```
                    ┌──────────────────────────────────┐
                    │          Entry Point              │
                    │   (TSP Genetic solver.py)         │
                    │                                   │
                    │  1. Parse Cities List.txt         │
                    │  2. Build city coordinate dict     │
                    │  3. Instantiate GeneticSolver     │
                    │  4. Call solve()                   │
                    └──────────────┬───────────────────┘
                                   │
                    ┌──────────────▼───────────────────┐
                    │        GeneticSolver              │
                    │                                   │
                    │  Orchestrates the full GA loop:   │
                    │  ┌─────────────────────────────┐  │
                    │  │  initialPopulation()        │  │
                    │  │  ├─ Generate P random       │  │
                    │  │  │   permutations           │  │
                    │  │  ├─ Enforce uniqueness      │  │
                    │  │  ├─ Compute fitness (cost)  │  │
                    │  │  └─ Sort by ascending cost  │  │
                    │  └─────────────────────────────┘  │
                    │  ┌─────────────────────────────┐  │
                    │  │  lunchEvolution()           │  │
                    │  │  For each generation:       │  │
                    │  │  ├─ Pairwise crossover      │  │
                    │  │  ├─ Stochastic mutation     │  │
                    │  │  ├─ Repair infeasible       │  │
                    │  │  ├─ Merge & sort (μ+λ)     │  │
                    │  │  ├─ Truncation selection    │  │
                    │  │  ├─ Track elite & average   │  │
                    │  │  └─ Visualize every 20 gen  │  │
                    │  └─────────────────────────────┘  │
                    │  ┌─────────────────────────────┐  │
                    │  │  solve()                    │  │
                    │  │  ├─ Run lunchEvolution()    │  │
                    │  │  ├─ Plot elite cost curve   │  │
                    │  │  └─ Plot average cost curve │  │
                    │  └─────────────────────────────┘  │
                    └──────┬──────────────┬────────────┘
                           │              │
              ┌────────────▼──┐    ┌──────▼──────────┐
              │  Chromosome   │    │     Draw         │
              │               │    │                  │
              │  • solution   │    │  • Route plot    │
              │    (list[int]) │    │    with arrows  │
              │  • cost        │    │  • Title with   │
              │    (float)     │    │    generation & │
              │  • __lt__()   │    │    cost info     │
              │    for sorting │    │  • Auto-scaled  │
              │               │    │    axis limits   │
              └───────────────┘    └─────────────────┘
```

---

## Data Flow

```
Cities List.txt
      │
      ▼
┌─────────────┐     ┌──────────────────────┐
│ Parse Input  │────▶│ cities: dict          │
│              │     │ {id: {x: int, y: int}}│
└─────────────┘     └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Initial Population    │
                    │ P random permutations │
                    │ Each: Chromosome obj  │
                    └──────────┬───────────┘
                               │
               ┌───────────────▼───────────────┐
               │     Generational Loop (G)      │
               │                                │
               │  ┌──────────────────────────┐  │
               │  │ Selection: consecutive   │  │
               │  │ pairs from sorted pop    │  │
               │  └────────────┬─────────────┘  │
               │               │                │
               │  ┌────────────▼─────────────┐  │
               │  │ Crossover: single-point  │  │
               │  │ cut → two raw children   │  │
               │  └────────────┬─────────────┘  │
               │               │                │
               │  ┌────────────▼─────────────┐  │
               │  │ Mutation: swap two genes │  │
               │  │ with probability p_m     │  │
               │  └────────────┬─────────────┘  │
               │               │                │
               │  ┌────────────▼─────────────┐  │
               │  │ Repair: fix duplicates   │  │
               │  │ restore Hamiltonian      │  │
               │  └────────────┬─────────────┘  │
               │               │                │
               │  ┌────────────▼─────────────┐  │
               │  │ Merge parents+children   │  │
               │  │ Sort by cost             │  │
               │  │ Keep top P (elitist)     │  │
               │  └────────────┬─────────────┘  │
               │               │                │
               │  ┌────────────▼─────────────┐  │
               │  │ Record elite & average   │  │
               │  │ Visualize every 20 gen   │  │
               │  └──────────────────────────┘  │
               └───────────────┬───────────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Final Visualization   │
                    │ • Elite cost curve    │
                    │ • Average cost curve  │
                    └──────────────────────┘
```

---

## Genetic Operator Details

### Crossover Strategy

```
         cut point (random)
              │
Parent A: [c₁ c₂ c₃ │ c₄ c₅ c₆]
Parent B: [c₇ c₈ c₉ │ c₁₀ c₁₁ c₁₂]
                      │
Child 1:  [c₁ c₂ c₃ │ c₁₀ c₁₁ c₁₂]  ──▶  Repair  ──▶  Valid Tour
Child 2:  [c₇ c₈ c₉ │ c₄  c₅  c₆ ]  ──▶  Repair  ──▶  Valid Tour
```

### Repair Algorithm

```
Input:  chromosome with potential duplicates
        e.g., [3, 1, 5, 6, 1, 3, 5]

Step 1: Identify missing cities
        Full set: {1,2,3,4,5,6,7}
        Present:  {1,3,5,6}
        Missing:  [2, 4, 7]  (queue)

Step 2: Walk through chromosome, first occurrence kept
        Position 0: 3 → first occurrence → keep
        Position 1: 1 → first occurrence → keep
        Position 2: 5 → first occurrence → keep
        Position 3: 6 → first occurrence → keep
        Position 4: 1 → DUPLICATE → replace with 2 (dequeue)
        Position 5: 3 → DUPLICATE → replace with 4 (dequeue)
        Position 6: 5 → DUPLICATE → replace with 7 (dequeue)

Output: [3, 1, 5, 6, 2, 4, 7]  ✓ Valid Hamiltonian path
```

### Selection Pressure Model

```
Generation t Population:   [p₁, p₂, ..., pₚ]         (P individuals)
Offspring:                 [o₁, o₂, ..., oₚ]         (P offspring)
                                    │
                           Merge & Sort by cost
                                    │
                           [s₁, s₂, ..., s₂ₚ]        (2P sorted)
                                    │
                           Truncate to top P
                                    │
Generation t+1 Population: [s₁, s₂, ..., sₚ]         (P survivors)

Property: cost(s₁) ≤ cost(p₁)  (monotonic elite improvement)
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Permutation encoding** | Natural representation for TSP — each chromosome is a valid city ordering |
| **Single-point crossover + repair** | Simple implementation; repair guarantees feasibility without complex order-preserving operators |
| **Swap mutation** | Minimal perturbation that preserves permutation structure |
| **(μ+λ) selection** | Guarantees elitist convergence — best solution is never lost |
| **Uniqueness enforcement** | Prevents population collapse and maintains genetic diversity |
| **Euclidean distance** | Standard metric for planar TSP instances; enables geometric visualization |

---

## File Structure

```
.
├── TSP Genetic solver.py    # Main solver: all classes and entry point
├── Cities List.txt          # Input: city coordinates (id x y per line)
├── README.md                # Project documentation
├── ARCHITECTURE.md          # This file — design & architecture details
├── requirements.txt         # Python dependencies
├── CITATION.cff             # Citation metadata
└── LICENSE                  # MIT License
```
