# Advent of Code 2025

Solutions for [Advent of Code 2025](https://adventofcode.com/2025) challenges.

## Daily Challenges

| Day | Problem | P1 | P2 | Difficulty | Key Insight |
|-----|---------|----|----|------------|-------------|
| [01](day01/) | **Secret Entrance** | Count dial at 0 after rotations | Count dial at 0 during rotations | ⭐ Easy | Modular arithmetic with wraparound |
| [02](day02/) | **Gift Shop** | Find IDs with pattern repeated 2x | Find IDs with pattern repeated 2+ times | ⭐ Easy | String pattern matching and validation |
| [03](day03/) | **Lobby** | Max 2-digit from each battery bank | Max 12-digit from each battery bank | ⭐ Easy | Greedy digit selection |
| [04](day04/) | **Printing Department** | Count accessible paper rolls | Remove accessible rolls iteratively | ⭐⭐ Medium | Moore neighbourhood + simulation |
| [05](day05/) | **Cafeteria** | Count fresh ingredients in ranges | *Not implemented* | ⭐ Easy | Range intersection |
| [06](day06/) | **Trash Compactor** | Sum results of vertical math problems | Parse using cephalopod column reading | ⭐⭐ Medium | 2D parsing + column detection |
| [07](day07/) | **Laboratories** | Count tachyon beam splits | Count total timeline paths through manifold | ⭐⭐ Medium | Beam simulation with splitting |
| [08](day08/) | **Playground** | Product of 3 largest circuits after 1000 connections | Product of X coordinates of final connection | ⭐⭐⭐ Hard | Kruskal's algorithm + Union-Find |
| [09](day09/) | **Movie Theater** | Largest rectangle using red tiles as corners | Largest rectangle using red+green tiles | ⭐⭐ Medium | Brute force rectangle enumeration |
| [10](day10/) | **Factory** | Min button presses for all machines | Configure joltage levels with min presses | ⭐⭐⭐ Hard | Linear algebra over GF(2) |
| [11](day11/) | **Reactor** | Count paths from 'you' to 'out' | Count paths 'svr'→'out' via 'fft'+'dac' | ⭐⭐⭐⭐ Very Hard | DAG path multiplication |

### Difficulty Legend
- ⭐ **Easy**: Straightforward implementation
- ⭐⭐ **Medium**: Requires algorithm knowledge or careful implementation  
- ⭐⭐⭐ **Hard**: Advanced algorithms or mathematical insight needed
- ⭐⭐⭐⭐ **Very Hard**: Complex optimisation or deep algorithmic insight required

## Languages Used

Solutions may be implemented in various languages depending on what fits best:
- **Python** (simple procedural tasks, optimisation problems)
- **Prolog** (logic puzzles, constraint problems, graph algorithms)
- Others as appropriate

### Prolog Implementations

Selected problems have been reimplemented in Prolog to showcase declarative programming approaches:

| Day | Problem | Python Time | Prolog Time | Speedup | Notes |
|-----|---------|-------------|-------------|---------|-------|
| [04](day04/) | **Printing Department** | 0.118s | 0.083s | **1.4x faster** | Grid simulation with backtracking |
| [07](day07/) | **Laboratories** | 0.019s | 0.091s | **0.2x slower** | Beam simulation - Python more efficient |
| [08](day08/) | **Playground** | 0.097s | 0.089s | **1.1x faster** | Union-Find with MST algorithm |
| [10](day10/) | **Factory** | 0.496s | 0.109s | **4.5x faster** | CLP dominates brute force approach |
| [11](day11/) | **Reactor** | 0.068s | 0.051s | **1.3x faster** | Graph traversal with memoisation |

**Key Insights:**
- **Constraint Logic Programming** (Day 10) shows dramatic speedups (4.5x) over brute force
- **Graph algorithms** (Days 4, 8, 11) benefit from Prolog's relational model
- **Simulation problems** (Day 7) favour imperative approaches - Python wins here
- **Declarative style** often leads to more concise and mathematically elegant solutions
- **Performance varies widely** - CLP problems see huge gains, simulation problems see losses

*Benchmarks run on macOS with SWI-Prolog 9.x and Python 3.13*

## Running Solutions

See individual day directories for specific running instructions.
