"""
Created By: Noble Carpenter, Teagan Tobias, Christian Winchester
Date Created: 04/15/2026
Filename: ExperimentRunner.py
Purpose: Runs experiments comparing BFS, DFS, A*, and ACO on randomly generated mazes of 
        varying sizes and densities. Results are saved to a CSV file for analysis.
"""
 
import csv
import os
import sys
 
# allow imports from this directory regardless of where the script is run from
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 
from MazeGenerator import generate_maze
from BFS import bfs
from DFS import dfs
from Astar import astar
from ACO import aco
 
# experiment configurations
 
MAZE_SIZES = [(10, 10), (20, 20), (40, 40), (80, 80), (160, 160)]
DENSITIES = [0.10, 0.20, 0.30, 0.40]
TRIALS = 20
 
ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "Astar": astar,
    "ACO": aco,
}
 
# output file path (relative to this script's location)
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
OUTPUT_FILE = os.path.join(RESULTS_DIR, "results_raw.csv")
 
# ──────────────────────────────────────────────────────────────────────────────
 
 
def run_experiments():
    os.makedirs(RESULTS_DIR, exist_ok=True)
 
    fieldnames = [
        "algorithm",
        "maze_rows",
        "maze_cols",
        "density",
        "trial",
        "runtime",
        "peak_memory",
        "path_length",
        "nodes_explored",
        "success",
    ]
 
    total_configs = len(MAZE_SIZES) * len(DENSITIES) * len(ALGORITHMS) * TRIALS
    completed = 0
 
    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
 
        for rows, cols in MAZE_SIZES:
            for density in DENSITIES:
                for trial in range(1, TRIALS + 1):
                    # each trial uses the same maze across all algorithms for fair comparison
                    seed = (rows * 1000 + cols) * 100 + int(density * 100) * 1000 + trial
                    try:
                        maze, start, goal = generate_maze(rows, cols, density, seed=seed)
                    except RuntimeError as e:
                        print(f"  [SKIP] {rows}x{cols} density={density} trial={trial}: {e}")
                        continue
 
                    for alg_name, alg_func in ALGORITHMS.items():
                        try:
                            result = alg_func(maze, start, goal)
                        except Exception as e:
                            print(f"  [ERROR] {alg_name} on {rows}x{cols} d={density} t={trial}: {e}")
                            result = {
                                "path": None,
                                "runtime": None,
                                "peak_memory": None,
                                "nodes_explored": None,
                                "path_length": 0,
                            }
 
                        writer.writerow({
                            "algorithm": alg_name,
                            "maze_rows": rows,
                            "maze_cols": cols,
                            "density": density,
                            "trial": trial,
                            "runtime": result["runtime"],
                            "peak_memory": result["peak_memory"],
                            "path_length": result["path_length"],
                            "nodes_explored": result["nodes_explored"],
                            "success": 1 if result["path"] is not None else 0,
                        })
 
                        completed += 1
                        if completed % 50 == 0:
                            print(f"  Progress: {completed}/{total_configs} runs complete")
 
    print(f"\nDone! Results saved to: {OUTPUT_FILE}")
 
 
if __name__ == "__main__":
    print("Starting experiments...")
    print(f"Configurations: {len(MAZE_SIZES)} sizes x {len(DENSITIES)} densities x "
          f"{len(ALGORITHMS)} algorithms x {TRIALS} trials\n")
    run_experiments()