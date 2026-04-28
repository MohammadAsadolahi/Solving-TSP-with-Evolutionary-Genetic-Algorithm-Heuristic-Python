<div align="center">

# 🧬 Solving the Travelling Salesman Problem with Evolutionary Genetic Algorithms

### A Metaheuristic Approach to NP-Hard Combinatorial Optimization

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=for-the-badge&logo=plotly&logoColor=white)](https://matplotlib.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Algorithm](https://img.shields.io/badge/Algorithm-Genetic%20Algorithm-FF6F00?style=for-the-badge&logo=probot&logoColor=white)]()
[![NP-Hard](https://img.shields.io/badge/Complexity-NP--Hard-red?style=for-the-badge)]()

*A high-performance evolutionary solver for the classical Travelling Salesman Problem, demonstrating the power of bio-inspired computation in tackling intractable combinatorial search spaces.*

**Author:** Chief AI Officer @ Google

---

</div>

## Table of Contents

- [Problem Statement](#-problem-statement)
- [Why Genetic Algorithms?](#-why-genetic-algorithms)
- [Architecture & Design](#-architecture--design)
- [Algorithm Deep Dive](#-algorithm-deep-dive)
- [Computational Complexity Analysis](#-computational-complexity-analysis)
- [Results & Convergence](#-results--convergence)
- [Evolutionary Progress Visualization](#-evolutionary-progress-visualization)
- [Getting Started](#-getting-started)
- [Configuration & Hyperparameters](#-configuration--hyperparameters)
- [Input Format](#-input-format)
- [Theoretical Foundations](#-theoretical-foundations)
- [Future Directions](#-future-directions)
- [Citation](#-citation)
- [License](#-license)

---

## 📐 Problem Statement

The **Travelling Salesman Problem (TSP)** is one of the most intensively studied problems in computational optimization. Given a set of $n$ cities with pairwise distances, the objective is to find the shortest possible Hamiltonian cycle — a tour that visits every city exactly once and returns to the origin.

**Formally:**

$$\min_{\pi \in S_n} \sum_{i=1}^{n-1} d(\pi(i), \pi(i+1)) + d(\pi(n), \pi(1))$$

where $S_n$ is the set of all permutations of $n$ cities and $d(i,j)$ denotes the Euclidean distance:

$$d(i,j) = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$$

The search space grows as $\frac{(n-1)!}{2}$ for symmetric TSP — for just 20 cities, that's **60,822,550,400** possible tours. Exhaustive enumeration is computationally infeasible, making this an ideal candidate for metaheuristic optimization.

---

## 🧪 Why Genetic Algorithms?

Genetic Algorithms (GAs) belong to the family of **Evolutionary Algorithms (EAs)** — population-based metaheuristics inspired by Darwinian natural selection. They offer several compelling advantages for TSP:

| Property | Benefit for TSP |
|---|---|
| **Population-based search** | Explores multiple regions of the solution space simultaneously |
| **Stochastic operators** | Escapes local optima through mutation and crossover diversity |
| **Selection pressure** | Guides convergence toward high-quality solutions via elitism |
| **No gradient required** | Operates on discrete permutation spaces where calculus-based methods fail |
| **Anytime algorithm** | Returns progressively better solutions; can be stopped at any generation |

This implementation leverages a **generational GA with elitist selection**, single-point crossover, stochastic swap mutation, and a repair operator to maintain feasibility across generations.

---

## 🏗 Architecture & Design

The solver is built with a clean object-oriented architecture consisting of three core components:

```
┌─────────────────────────────────────────────────────────────────┐
│                        GeneticSolver                            │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Population    │  │  Operators   │  │  Evolution Engine    │  │
│  │  Management    │  │              │  │                      │  │
│  │  ─────────     │  │  ──────────  │  │  ────────────────    │  │
│  │  • init pool   │  │  • crossover │  │  • generational loop │  │
│  │  • elitism     │  │  • mutation  │  │  • fitness sorting   │  │
│  │  • diversity   │  │  • repair    │  │  • survivor selection│  │
│  │  • tracking    │  │  • validate  │  │  • convergence track │  │
│  └───────────────┘  └──────────────┘  └──────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌──────────────────────────────────────┐    │
│  │  Chromosome   │  │  Draw (Visualization Engine)         │    │
│  │  ───────────  │  │  ──────────────────────────────────  │    │
│  │  • solution   │  │  • route plotting with directed arcs │    │
│  │  • cost       │  │  • generational progress tracking    │    │
│  │  • comparable │  │  • elite & average cost curves       │    │
│  └───────────────┘  └──────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

> See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed component interaction diagrams and data flow analysis.

---

## 🔬 Algorithm Deep Dive

### 1. Population Initialization
A pool of `P` chromosomes is generated, each representing a random permutation of all city indices. Uniqueness is enforced — no two chromosomes in the initial population share the same tour sequence.

### 2. Fitness Evaluation
Each chromosome's fitness is its **total Euclidean path cost** (lower is better). The population is sorted by ascending cost after every generation.

### 3. Crossover (Recombination)
**Single-point crossover** is applied to consecutive parent pairs:

```
Parent A:  [3 1 5 | 2 4 6 7]      crossover point = 3
Parent B:  [7 4 2 | 6 1 3 5]
                ↓
Child 1:   [3 1 5 | 6 1 3 5]  →  repair  →  [3 1 5 | 6 2 4 7]
Child 2:   [7 4 2 | 2 4 6 7]  →  repair  →  [7 3 2 | 1 4 6 5]
```

### 4. Repair Operator
Since naive crossover on permutation encodings produces **infeasible solutions** (duplicate cities, missing cities), a deterministic repair operator scans each offspring and substitutes duplicate entries with missing city indices, restoring Hamiltonian validity.

### 5. Swap Mutation
With probability $p_m$, two randomly selected positions in a chromosome are swapped:

$$\pi' = \text{swap}(\pi, i, j) \quad \text{where } i \neq j$$

This introduces controlled perturbation to maintain population diversity and prevent premature convergence.

### 6. Survivor Selection (Elitist Strategy)
Parents and offspring are merged into a combined pool of size $2P$, sorted by fitness, and the top $P$ individuals survive. This **$(\mu + \lambda)$ selection** guarantees monotonic improvement of the best solution across generations.

---

## 📊 Computational Complexity Analysis

| Operation | Time Complexity | Per Generation |
|---|---|---|
| Fitness evaluation | $O(n)$ per chromosome | $O(P \cdot n)$ |
| Crossover | $O(n)$ per pair | $O(P \cdot n)$ |
| Repair operator | $O(n^2)$ per offspring | $O(P \cdot n^2)$ |
| Mutation (swap) | $O(1)$ per chromosome | $O(P)$ |
| Sorting (selection) | $O(P \log P)$ | $O(P \log P)$ |
| **Total per generation** | | $O(P \cdot n^2 + P \log P)$ |
| **Total runtime** | | $O(G \cdot (P \cdot n^2 + P \log P))$ |

Where $n$ = number of cities, $P$ = population size, $G$ = number of generations.

---

## 📈 Results & Convergence

Tested with **20 cities** distributed in a $[0, 1000] \times [0, 1000]$ Euclidean plane.

### Best Tour Found (Generation 180)
The algorithm converges to a near-optimal route, dramatically reducing path cost from initial random tours:

![Best solution found at 180 iterations](https://user-images.githubusercontent.com/79268727/140981092-1eae5fb3-aff9-42d1-8ba3-d530d3ea9cf0.png)

### Convergence Curves

<table>
<tr>
<td width="50%">

**Average Population Cost**
Demonstrates steady downward pressure across all generations — evidence of effective selection and recombination dynamics.

![Average chromosome costs](https://user-images.githubusercontent.com/79268727/140981045-45922cfb-4bf7-4f65-8f07-8c71c07848ac.png)

</td>
<td width="50%">

**Elite (Best) Chromosome Cost**
Monotonically non-increasing due to the elitist $(\mu+\lambda)$ selection strategy. Rapid early improvement followed by asymptotic refinement.

![Elite chromosome costs](https://user-images.githubusercontent.com/79268727/140981071-a55cec9b-2a46-466b-b983-99a07ed7da96.png)

</td>
</tr>
</table>

---

## 🗺 Evolutionary Progress Visualization

The solver captures route snapshots every 20 generations, illustrating the progressive elimination of crossing edges and convergence toward planarity:

<details>
<summary><b>Click to expand full evolutionary timeline (Generation 0 → 180)</b></summary>

#### Generation 0 — Random Initialization
![Generation 0](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%200%20iteration.png)

#### Generation 20 — Early Exploration
![Generation 20](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%2020%20iterations.png)

#### Generation 40 — Structure Emerging
![Generation 40](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%2040%20iterations.png)

#### Generation 60 — Exploitation Phase Begins
![Generation 60](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%2060%20iterations.png)

#### Generation 80 — Crossing Edges Eliminated
![Generation 80](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%2080%20iterations.png)

#### Generation 100 — Approaching Local Optima
![Generation 100](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%20100%20iterations.png)

#### Generation 120 — Fine-Tuning
![Generation 120](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%20120%20iterations.png)

#### Generation 140 — Near-Optimal Region
![Generation 140](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%20140%20iterations.png)

#### Generation 160 — Convergence
![Generation 160](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%20160%20iterations.png)

#### Generation 180 — Final Solution
![Generation 180](https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python/blob/main/Best%20solution%20found%20at%20180%20iterations.png)

</details>

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `matplotlib` for visualization

### Installation

```bash
git clone https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python.git
cd Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python
pip install -r requirements.txt
```

### Run

```bash
python "TSP Genetic solver.py"
```

The solver will open interactive matplotlib windows showing:
1. **Route plots** every 20 generations with directed arcs
2. **Elite cost curve** — best fitness across all generations
3. **Average cost curve** — population-wide fitness trend

---

## ⚙ Configuration & Hyperparameters

Tune the solver by modifying the constructor call in `TSP Genetic solver.py`:

```python
geneticSolver = GeneticSolver(
    populationSize=50,       # Number of chromosomes per generation
    generationCount=200,     # Total evolutionary cycles
    mutationRate=0.3,        # Probability of swap mutation per offspring
    cities=cities,           # City coordinate dictionary
    cityCount=cityCount      # Total number of cities
)
```

| Parameter | Default | Recommended Range | Effect |
|---|---|---|---|
| `populationSize` | 50 | 30–200 | Larger → better diversity, slower per generation |
| `generationCount` | 200 | 100–1000 | More generations → finer convergence |
| `mutationRate` | 0.3 | 0.05–0.4 | Higher → more exploration, risk of chaos |

**Rule of thumb:** For $n > 50$ cities, increase population size to $\geq 2n$ and generations to $\geq 10n$.

---

## 📋 Input Format

Cities are defined in `Cities List.txt`, one city per line:

```
<index> <x_coordinate> <y_coordinate>
```

**Example:**
```
1 909 649
2 239 197
3 627 893
```

- **Index**: 1-based integer identifier
- **Coordinates**: Euclidean plane positions (any non-negative range)
- Distance metric: $d(i,j) = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$

To test with custom instances, simply edit this file. The solver auto-detects city count at runtime.

---

## 📖 Theoretical Foundations

This implementation draws from the foundational literature in evolutionary computation and combinatorial optimization:

- **Holland, J.H. (1975)** — *Adaptation in Natural and Artificial Systems.* The seminal work establishing Genetic Algorithms.
- **Goldberg, D.E. (1989)** — *Genetic Algorithms in Search, Optimization, and Machine Learning.* Formal analysis of schema theory and GA convergence.
- **Michalewicz, Z. (1996)** — *Genetic Algorithms + Data Structures = Evolution Programs.* Constraint handling and repair operators for permutation problems.
- **Applegate, D.L. et al. (2006)** — *The Traveling Salesman Problem: A Computational Study.* The definitive reference on TSP algorithms and complexity.
- **Eiben, A.E. & Smith, J.E. (2015)** — *Introduction to Evolutionary Computing.* Modern treatment of selection schemes, crossover variants, and parameter control.

The $(\mu + \lambda)$ selection strategy implemented here guarantees **elitist convergence** — the best solution found is never lost across generations, a property formally analyzed by Rudolph (1994) in the context of evolutionary convergence guarantees.

---

## 🔮 Future Directions

| Enhancement | Expected Impact |
|---|---|
| **Order Crossover (OX)** | Eliminates need for repair operator; preserves relative city ordering |
| **2-opt Local Search** | Hybridize GA with local search for memetic algorithm performance |
| **Adaptive Mutation Rate** | Self-tuning mutation via 1/5th rule or fitness-proportional control |
| **Island Model Parallelism** | Multi-population with migration for improved diversity and scalability |
| **TSPLIB Benchmark Integration** | Standardized benchmarking against known optimal solutions |
| **GPU-Accelerated Fitness** | CUDA/cupy-based batch distance computation for large instances |

---

## 📄 Citation

If you use this work in research or academic publications, please cite:

```bibtex
@software{tsp_genetic_solver,
  title     = {Solving TSP with Evolutionary Genetic Algorithm Heuristic},
  author    = {AG},
  year      = {2021},
  url       = {https://github.com/Elktrn/Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python},
  note      = {A Python implementation of genetic algorithms for the Travelling Salesman Problem}
}
```

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

*Built with a deep appreciation for the elegance of evolutionary computation and the enduring beauty of NP-hard problems.*

**Chief AI Officer @ Google**

</div>
