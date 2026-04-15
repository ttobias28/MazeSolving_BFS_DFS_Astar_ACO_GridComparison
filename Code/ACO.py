"""
Created By: Noble Carpenter, Teagan Tobias, Christian Winchester
Date Created: 04/15/2026
Filename: ACO.py
Purpose: Ant Colony Optimization maze solver.
        Nature-inspired algorithm using pheromone trails.
     Does not guarantee shortest path but finds high-quality solutions.
"""
 
import time
import tracemalloc
import random
import math
 
 
# --- default ACO Parameters ---
DEFAULT_N_ANTS = 20
DEFAULT_N_ITERATIONS = 50
DEFAULT_ALPHA = 1.0        # pheromone weight
DEFAULT_BETA = 2.0         # heuristic weight (inverse distance to goal)
DEFAULT_EVAPORATION = 0.5  # pheromone evaporation rate (0-1)
DEFAULT_Q = 100.0          # pheromone deposit constant
 
 
def aco(
    maze,
    start,
    goal,
    n_ants=DEFAULT_N_ANTS,
    n_iterations=DEFAULT_N_ITERATIONS,
    alpha=DEFAULT_ALPHA,
    beta=DEFAULT_BETA,
    evaporation=DEFAULT_EVAPORATION,
    Q=DEFAULT_Q,
    seed=None,
):
    """
    Solve a maze using Ant Colony Optimization.
 
    Parameters:
        maze (list[list[int]]): 2D grid (0 = open, 1 = wall).
        start (tuple): (row, col) of the starting cell.
        goal (tuple): (row, col) of the goal cell.
        n_ants (int): Number of ants per iteration.
        n_iterations (int): Number of iterations.
        alpha (float): Influence of pheromone on path choice.
        beta (float): Influence of heuristic on path choice.
        evaporation (float): Fraction of pheromone that evaporates each iteration.
        Q (float): Constant for pheromone deposit amount.
        seed (int or None): Random seed for reproducibility.
 
    Returns:
        dict with keys:
            path (list[tuple] or None): Best path found, or None if no path found.
            runtime (float): Execution time in seconds.
            peak_memory (int): Peak memory usage in bytes.
            nodes_explored (int): Total cells visited across all ants and iterations.
            path_length (int): Number of steps in the best path (0 if no path).
    """
    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rng = random.Random(seed)
 
    # initialize pheromone matrix (all open cells start at 1.0)
    pheromone = [[1.0 if maze[r][c] == 0 else 0.0 for c in range(cols)] for r in range(rows)]
 
    def heuristic(pos):
        """Inverse Manhattan distance to goal (higher = closer to goal)."""
        dist = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        return 1.0 / (dist + 1)
 
    def get_neighbors(pos):
        r, c = pos
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                neighbors.append((nr, nc))
        return neighbors
 
    def choose_next(current, visited):
        """Probabilistically choose the next cell based on pheromone and heuristic."""
        neighbors = [n for n in get_neighbors(current) if n not in visited]
        if not neighbors:
            return None
 
        weights = []
        for n in neighbors:
            pher = pheromone[n[0]][n[1]] ** alpha
            heur = heuristic(n) ** beta
            weights.append(pher * heur)
 
        total = sum(weights)
        if total == 0:
            return rng.choice(neighbors)
 
        # roulette wheel selection
        probs = [w / total for w in weights]
        r = rng.random()
        cumulative = 0.0
        for neighbor, prob in zip(neighbors, probs):
            cumulative += prob
            if r <= cumulative:
                return neighbor
        return neighbors[-1]
 
    tracemalloc.start()
    start_time = time.perf_counter()
 
    best_path = None
    best_length = float("inf")
    total_nodes_explored = 0
    max_steps = rows * cols  # cap to prevent infinite loops
 
    for _ in range(n_iterations):
        iteration_paths = []
 
        for _ in range(n_ants):
            path = [start]
            visited = {start}
            steps = 0
 
            while path[-1] != goal and steps < max_steps:
                current = path[-1]
                next_cell = choose_next(current, visited)
                if next_cell is None:
                    break  # ant is stuck
                path.append(next_cell)
                visited.add(next_cell)
                steps += 1
 
            total_nodes_explored += len(path)
 
            if path[-1] == goal:
                iteration_paths.append(path)
                if len(path) < best_length:
                    best_length = len(path)
                    best_path = path
 
        # evaporate pheromones
        for r in range(rows):
            for c in range(cols):
                pheromone[r][c] *= (1.0 - evaporation)
                pheromone[r][c] = max(pheromone[r][c], 1e-6)  # prevent zero
 
        # deposit pheromones on successful paths
        for path in iteration_paths:
            deposit = Q / len(path)
            for r, c in path:
                pheromone[r][c] += deposit
 
    elapsed = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
 
    if best_path is None:
        return {
            "path": None,
            "runtime": elapsed,
            "peak_memory": peak_memory,
            "nodes_explored": total_nodes_explored,
            "path_length": 0,
        }
 
    return {
        "path": best_path,
        "runtime": elapsed,
        "peak_memory": peak_memory,
        "nodes_explored": total_nodes_explored,
        "path_length": len(best_path) - 1,
    }