"""
Created By: Noble Carpenter, Teagan Tobias, Christian Winchester
Date Created: 04/15/2026
Filename: PlotResults.py
Purpose: Reads results_raw.csv and saves comparison graphs to ../graphs/.
To run (in terminal): python PlotResults.py 
"""
 
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
 
# resolve paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(BASE_DIR, "..", "results", "results_raw.csv")
GRAPHS_DIR = os.path.join(BASE_DIR, "..", "graphs")
 
ALG_COLORS = {
    "BFS":   "#C198D2",
    "DFS":   "#B0FCC8",
    "Astar": "#A9D6EF",
    "ACO":   "#F9C0D9",
}
 
ALG_ORDER = ["BFS", "DFS", "Astar", "ACO"]
 
 
def load_data():
    if not os.path.exists(RESULTS_FILE):
        raise FileNotFoundError(
            f"Results file not found: {RESULTS_FILE}\n"
            "Run experiment_runner.py first."
        )
    df = pd.read_csv(RESULTS_FILE)
    df["maze_size"] = df["maze_rows"].astype(str) + "x" + df["maze_cols"].astype(str)
    # only include successful runs for path_length plots
    return df
 
 
def save_fig(filename):
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    path = os.path.join(GRAPHS_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved: {path}")
 
 
# plot 1: runtime vs maze size
 
def plot_runtime_vs_size(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    summary = df.groupby(["algorithm", "maze_size", "maze_rows"])["runtime"].mean().reset_index()
 
    for alg in ALG_ORDER:
        sub = summary[summary["algorithm"] == alg].sort_values("maze_rows")
        ax.plot(sub["maze_size"], sub["runtime"], marker="o",
                label=alg, color=ALG_COLORS[alg], linewidth=2)
 
    ax.set_title("Average Runtime vs Maze Size", fontsize=14)
    ax.set_xlabel("Maze Size")
    ax.set_ylabel("Runtime (seconds)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    save_fig("runtime_vs_size.png")
 
 
# plot 2: memory usage vs maze size
 
def plot_memory_vs_size(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    summary = df.groupby(["algorithm", "maze_size", "maze_rows"])["peak_memory"].mean().reset_index()
 
    for alg in ALG_ORDER:
        sub = summary[summary["algorithm"] == alg].sort_values("maze_rows")
        ax.plot(sub["maze_size"], sub["peak_memory"] / 1024, marker="s",
                label=alg, color=ALG_COLORS[alg], linewidth=2)
 
    ax.set_title("Average Peak Memory vs Maze Size", fontsize=14)
    ax.set_xlabel("Maze Size")
    ax.set_ylabel("Peak Memory (KB)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    save_fig("memory_vs_size.png")
 
 
# plot 3: nodes explored vs obstacle density
 
def plot_nodes_vs_density(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    summary = df.groupby(["algorithm", "density"])["nodes_explored"].mean().reset_index()
 
    for alg in ALG_ORDER:
        sub = summary[summary["algorithm"] == alg].sort_values("density")
        ax.plot(sub["density"], sub["nodes_explored"], marker="^",
                label=alg, color=ALG_COLORS[alg], linewidth=2)
 
    ax.set_title("Average Nodes Explored vs Obstacle Density", fontsize=14)
    ax.set_xlabel("Obstacle Density")
    ax.set_ylabel("Nodes Explored")
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    save_fig("nodes_vs_density.png")
 
 
# plot 4: path length vs maze size (only successful runs)
 
def plot_path_length(df):
    success = df[df["success"] == 1]
    fig, ax = plt.subplots(figsize=(9, 5))
    summary = success.groupby(["algorithm", "maze_size", "maze_rows"])["path_length"].mean().reset_index()
 
    for alg in ALG_ORDER:
        sub = summary[summary["algorithm"] == alg].sort_values("maze_rows")
        ax.plot(sub["maze_size"], sub["path_length"], marker="D",
                label=alg, color=ALG_COLORS[alg], linewidth=2)
 
    ax.set_title("Average Path Length vs Maze Size (Successful Runs)", fontsize=14)
    ax.set_xlabel("Maze Size")
    ax.set_ylabel("Path Length (steps)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    save_fig("path_length_vs_size.png")
 
 
# plot 5: success rate vs obstacle density
 
def plot_success_rate(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    summary = df.groupby(["algorithm", "density"])["success"].mean().reset_index()
 
    for alg in ALG_ORDER:
        sub = summary[summary["algorithm"] == alg].sort_values("density")
        ax.plot(sub["density"], sub["success"], marker="o",
                label=alg, color=ALG_COLORS[alg], linewidth=2)
 
    ax.set_title("Success Rate vs Obstacle Density", fontsize=14)
    ax.set_xlabel("Obstacle Density")
    ax.set_ylabel("Success Rate")
    ax.set_ylim(0, 1.05)
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    save_fig("success_rate_vs_density.png")
 
 
# MAIN
 
if __name__ == "__main__":
    print("Loading results...")
    df = load_data()
    print(f"  Loaded {len(df)} rows from {RESULTS_FILE}\n")
 
    print("Generating graphs...")
    plot_runtime_vs_size(df)
    plot_memory_vs_size(df)
    plot_nodes_vs_density(df)
    plot_path_length(df)
    plot_success_rate(df)
 
    print(f"\nAll graphs saved to: {GRAPHS_DIR}")
