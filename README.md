# Grid Maze Pathfinding: BFS, DFS, A*, and ACO Comparison

## Team Members

- Noble Carpenter (jncarpente42)
- Teagan Tobias (ttobias42)
- Christian Winchester (cwinchest43)
  
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

---
## How to Run this Project

---
## GenAI Usage Disclosure
