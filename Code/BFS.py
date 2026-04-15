"""
Created By: Noble Carpenter, Teagan Tobias, Christian Winchester
Date Created: 04/15/2026
Filename: BFS.py
Purpose: Script for solving mazes using Breadth-First Search (BFS).
"""
 
import time
import tracemalloc
from collections import deque
 
 
def bfs(maze, start, goal):
    """
    Solve a maze using Breadth-First Search.
 
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
            nodes_explored (int): Number of cells dequeued during search.
            path_length (int): Number of steps in the path (0 if no path).
    """
    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
 
    tracemalloc.start()
    start_time = time.perf_counter()
 
    visited = {start}
    parent = {start: None}
    queue = deque([start])
    nodes_explored = 0
    found = False
 
    while queue:
        current = queue.popleft()
        nodes_explored += 1
 
        if current == goal:
            found = True
            break
 
        r, c = current
        for dr, dc in directions:
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
                queue.append(neighbor)
 
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
 