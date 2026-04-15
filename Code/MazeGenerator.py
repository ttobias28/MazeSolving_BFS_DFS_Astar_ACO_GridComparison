"""
Created By: Noble Carpenter, Teagan Tobias, Christian Winchester
Date Created: 04/15/2026
Filename: MazeGenerator.py
Purpose: Generates random 2D grid mazes with guaranteed solvability.
"""
 
import random
from collections import deque
 
 
def generate_maze(rows, cols, obstacle_density, seed=None):
    """
    Generate a random solvable maze.
 
    Parameters:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        obstacle_density (float): Fraction of cells that are walls (0.0 - 1.0).
        seed (int or None): Random seed for reproducibility.
 
    Returns:
        maze (list[list[int]]): 2D grid where 0 = open, 1 = wall.
        start (tuple): Starting cell (row, col).
        goal (tuple): Goal cell (row, col).
    """
    rng = random.Random(seed)
    start = (0, 0)
    goal = (rows - 1, cols - 1)
 
    max_attempts = 1000
    for attempt in range(max_attempts):
        maze = []
        for r in range(rows):
            row = []
            for c in range(cols):
                if (r, c) == start or (r, c) == goal:
                    row.append(0)
                else:
                    row.append(1 if rng.random() < obstacle_density else 0)
            maze.append(row)
 
        if _is_solvable(maze, start, goal, rows, cols):
            return maze, start, goal
 
    raise RuntimeError(
        f"Could not generate a solvable maze after {max_attempts} attempts. "
        f"Try reducing obstacle_density (current: {obstacle_density})."
    )
 
 
def _is_solvable(maze, start, goal, rows, cols):
    """BFS check to confirm a path exists from start to goal."""
    visited = {start}
    queue = deque([start])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
 
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            return True
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] == 0
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append((nr, nc))
 
    return False
 
 
def print_maze(maze, path=None, start=None, goal=None):
    """
    Print the maze to the console for debugging.
    S = start, G = goal, * = path, # = wall, . = open
    """
    path_set = set(path) if path else set()
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == start:
                line += "S "
            elif pos == goal:
                line += "G "
            elif pos in path_set:
                line += "* "
            elif cell == 1:
                line += "# "
            else:
                line += ". "
        print(line)