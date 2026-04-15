"""
Created By: Noble Carpenter, Teagan Tobias, Christian Winchester
Date Created: 04/15/2026
Filename: Astar.py
Purpose: A* Search maze solver using Manhattan distance heuristic.
Guarantees the shortest path with an admissible heuristic.
"""
 
import time
import tracemalloc
import heapq
 
 
def _manhattan(a, b):
    """Manhattan distance heuristic — admissible for 4-directional grids."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
 
 
def astar(maze, start, goal):
    """
    Solve a maze using A* Search.
 
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
            nodes_explored (int): Number of cells popped from the priority queue.
            path_length (int): Number of steps in the path (0 if no path).
    """
    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
 
    tracemalloc.start()
    start_time = time.perf_counter()
 
    # Priority queue entries: (f_score, g_score, node)
    # g = cost so far, h = heuristic, f = g + h
    g_score = {start: 0}
    parent = {start: None}
    open_set = [((_manhattan(start, goal)), 0, start)]
    closed_set = set()
    nodes_explored = 0
    found = False
 
    while open_set:
        f, g, current = heapq.heappop(open_set)
 
        if current in closed_set:
            continue
 
        closed_set.add(current)
        nodes_explored += 1
 
        if current == goal:
            found = True
            break
 
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
 
            if (
                not (0 <= nr < rows and 0 <= nc < cols)
                or maze[nr][nc] == 1
                or neighbor in closed_set
            ):
                continue
 
            tentative_g = g + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                h = _manhattan(neighbor, goal)
                heapq.heappush(open_set, (tentative_g + h, tentative_g, neighbor))
 
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
 