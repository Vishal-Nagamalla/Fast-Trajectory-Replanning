import random
import os
from grid import Grid

GRID_SIZE = 101
NUM_GRIDS = 50
BLOCK_PROB = 0.30  

def generate_maze(grid_size, block_prob):
    """Generate a gridworld using a DFS-based maze generation with random tie-breaking."""
    grid = Grid(grid_size, grid_size)  # Create grid using existing Grid class
    stack = []

    # Start from a random position
    start_x, start_y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
    stack.append((start_x, start_y))
    visited = set()
    visited.add((start_x, start_y))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)  # Random tie-breaking
        unvisited_neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in visited:
                unvisited_neighbors.append((nx, ny))

        if unvisited_neighbors:
            nx, ny = random.choice(unvisited_neighbors)  # Pick a random neighbor
            visited.add((nx, ny))
            if random.random() < block_prob:
                grid.set_blocked(nx, ny)  # 30% chance of blocking
            stack.append((nx, ny))
        else:
            stack.pop()  # Backtrack when no unvisited neighbors

    # Ensure start and goal are unblocked
    grid.get_tile(grid_size - 1, grid_size - 1).is_blocked = False
    return grid

def save_grid(grid, filename):
    """Save grid to a text file."""
    with open(filename, 'w') as f:
        for row in grid.tiles:
            f.write(" ".join(str(int(tile.is_blocked)) for tile in row) + "\n")

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

# Generate and save 50 gridworlds
output_dir = "generated_grids"
os.makedirs(output_dir, exist_ok=True)

for i in range(NUM_GRIDS):
    grid = generate_maze(GRID_SIZE, BLOCK_PROB)
    save_grid(grid, os.path.join(output_dir, f"grid_{i+1}.txt"))

print(f"Successfully generated and saved {NUM_GRIDS} gridworlds in '{output_dir}' folder.")

# Load and print a sample grid
sample_grid = load_grid(os.path.join(output_dir, "grid_1.txt"))
