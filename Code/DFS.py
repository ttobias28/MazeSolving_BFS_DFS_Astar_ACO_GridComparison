"""
Created By: Noble Carpenter, Teagan Tobias, Christian Winchester
Date Created: 04/15/2026
Filename: DFS.py
Purpose: Script for solving mazes using Depth-First Search (DFS).
         Does NOT guarantee the shortest path — included for comparison.
"""
 
import time
import tracemalloc
import random
 
 
def dfs(maze, start, goal):
    """
    Solve a maze using Depth-First Search (iterative).
 
    Parameters:
        maze (list[list[int]]): 2D grid (0 = open, 1 = wall).
        start (tuple): (row, col) of the starting cell.
        goal (tuple): (row, col) of the goal cell.
 
    Returns:
        dict with keys:
            path (list[tuple] or None): Ordered list of (row, col) from start to goal,
                                        or None if no path exists.
            runtime (float): Execution time in seconds.
            peak_memory (int): Peak memory usage in bytes.
            nodes_explored (int): Number of cells popped from the stack during search.
            path_length (int): Number of steps in the path (0 if no path).
    """
    seed = 42   # fixed seed for reproducibility of random direction order
    rng = random.Random(seed)
    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
 
    tracemalloc.start()
    start_time = time.perf_counter()
 
    visited = {start}
    parent = {start: None}
    stack = [start]
    nodes_explored = 0
    found = False
 
    while stack:
        current = stack.pop()
        nodes_explored += 1
 
        if current == goal:
            found = True
            break
 
        r, c = current
        dirs = directions[:]
        rng.shuffle(dirs)  # randomize direction order for more varied paths
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] == 0
                and neighbor not in visited
            ):
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
 
    elapsed = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
 
    if not found:
        return {
            "path": None,
            "runtime": elapsed,
            "peak_memory": peak_memory,
            "nodes_explored": nodes_explored,
            "path_length": 0,
        }
 
    path = _reconstruct_path(parent, goal)
    return {
        "path": path,
        "runtime": elapsed,
        "peak_memory": peak_memory,
        "nodes_explored": nodes_explored,
        "path_length": len(path) - 1,
    }
 
 
def _reconstruct_path(parent, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path
 