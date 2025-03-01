import time
from grid import Grid
from tile import Tile
from fwdAstar import repeated_forward_astar
from fwdAstarAlternative import repeated_forward_astar2
from bwdAstar import repeated_backward_astar
from adaptiveAstar import adaptive_a_star
import random

# Load a grid from a file
def load_grid(filename):
    """Load grid from a text file into a Grid object."""
    with open(filename, 'r') as f:
        lines = f.readlines()

    grid_size = len(lines)
    grid = Grid(grid_size, grid_size)

    for x, line in enumerate(lines):
        values = list(map(int, line.strip().split()))
        for y, val in enumerate(values):
            if val == 1:
                grid.set_blocked(x, y)
    
    return grid

# Set up test parameters
grid_filename = "generated_grids/grid_20.txt"  # Change file as needed
grid = load_grid(grid_filename)

# DEBUG
"""for i in range(grid.width):
    for j in range(grid.height):
        if grid.get_tile(i, j).is_blocked:
            print("x", end=" ")
        else:
            print("o", end=" ")
    print("\n")"""
grid.printGrid()

# Define start and goal positions
start = grid.get_tile(random.randint(0, grid.width-1), random.randint(0, grid.height-1))
goal = grid.get_tile(grid.width - 1, grid.height - 1)

print(f"Running algorithms on {grid_filename}, from {(start.x, start.y)} to (101, 101)...\n")

# Run Repeated Forward A* (greater g-value priority tiebreaking)
print("Running Repeated Forward A* (greater g-value priority tiebreaking)...")
start_time = time.time()
path_fwd = repeated_forward_astar(grid, start, goal)
end_time = time.time()
if path_fwd:
    print(f"Path found! Length: {len(path_fwd)}, Time: {end_time - start_time:.4f} sec")

print("\n" + "="*50 + "\n")

# Run Repeated Forward A* (lesser g-value priority tiebreaking)
print("Running Repeated Forward A* (lesser g-value priority tiebreaking)...")
start_time = time.time()
path_fwd = repeated_forward_astar2(grid, start, goal)
end_time = time.time()
if path_fwd:
    print(f"Path found! Length: {len(path_fwd)}, Time: {end_time - start_time:.4f} sec")

print("\n" + "="*50 + "\n")

# Run Repeated Backward A*
print("Running Repeated Backward A*...")
start_time = time.time()
path_bwd = repeated_backward_astar(grid, start, goal)
end_time = time.time()
if path_bwd:
    print(f"Path found! Length: {len(path_bwd)}, Time: {end_time - start_time:.4f} sec")

print("\n" + "="*50 + "\n")

# Run Adaptive A*
print("Running Adaptive A*...")
start_time = time.time()
path_adaptive = adaptive_a_star(grid, start, goal)
end_time = time.time()
if path_adaptive:
    print(f"Path found! Length: {len(path_adaptive)}, Time: {end_time - start_time:.4f} sec")
