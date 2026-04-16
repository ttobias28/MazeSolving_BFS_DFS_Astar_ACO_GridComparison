# Grid Maze Pathfinding: BFS, DFS, A*, and ACO Comparison

## Team Members

- Noble Carpenter ([@NobleCarpenter](https://github.com/NobleCarpenter))
- Teagan Tobias ([@ttobias28](https://github.com/ttobias28))
- Christian Winchester ([@ChristianWinchester04](https://github.com/ChristianWinchester04))
  
---
## Problem Description:
This project studies the problem of finding the shortest path from a start cell to a goal cell in a 2D grid maze with blocked and open cells, where movement is allowed in the four cardinal directions (up, down, left, right). Each move costs the same (unweighted), so the goal is to find the shortest valid path. We compare four algorithms across different maze sizes and obstacle densities, analyzing trade-offs in runtime, memory usage, path quality, and nodes explored.

---
## Algorithms Implemented
- **Breadth-First Search (BFS)** -- our benchmark algorithm; guarantees the shortest path by exploring the maze level by level
- **Depth-First Search (DFS)** -- explores one path as far as possible before backtracking; does not guarantee shortest path but uses less memory in some cases
- __A* Search__ -- a heuristic-guided algorithm using Manhattan distance to focus the search toward the goal; finds the optimal path efficiently
- **Ant Colony Optimization (ACO)** -- a nature-inspired algorithm that simulates ant foraging behavior using pheromone trails to discover high-quality paths over multiple iterations
---
## Dataset(s) Used
There are no traditional, external datasets used. Instead, mazes were procedurally generated, on runtime, using a randomized algorithm with controlled size and obstacle density. Each maze instance was generated with a fixed seed to ensure reproducibility across algorithm comparisons.

---
## How to Run this Project

1. Clone the repository and install dependencies: pip install pandas matplotlib
2. Run experiments: python ExperimentRunner.py (writes results/results_raw.csv)
3. Generate graphs: python PlotResults.py (writes graphs/*.png)

To install the dependencies, you may work from your computer's terminal or the integrated terminal in the source folder that contains all code files. To run each code file, it is best to run it in the terminal of the source folder.

---
## GenAI Usage Disclosure
This project utilized Generative AI tools in the following capacities: 

- Assistance in debugging memory management issues 
- Drafting and refining the structure of the report and prose

Note: All core algorithmic logic and experimental analysis were implemented and verified by the team members. No AI tools were used to generate or modify experimental data.
