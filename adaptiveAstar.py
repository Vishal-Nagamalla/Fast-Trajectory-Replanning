import heapq
from grid import Grid
from tile import Tile

def heuristic(a, b):
    """Manhattan distance heuristic for grid-based pathfinding."""
    return abs(a.x - b.x) + abs(a.y - b.y)

def a_star_search(grid, start, goal, h_values):
    """A* search using adaptive heuristic updates."""
    open_set = []
    heapq.heappush(open_set, (h_values[start], -0, start))
    came_from = {}

    g_score = {tile: float("inf") for row in grid.tiles for tile in row}
    g_score[start] = 0

    f_score = {tile: float("inf") for row in grid.tiles for tile in row}
    f_score[start] = h_values[start]  # Use updated heuristic

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current), g_score

        for neighbor in grid.get_neighbors(current):
            tentative_g_score = g_score[current] + 1  # Uniform cost for grid moves

            if tentative_g_score < g_score[neighbor]:  # Better path found
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h_values[neighbor]

                heapq.heappush(open_set, (f_score[neighbor], -g_score[neighbor], neighbor))

    return None, g_score  # No path found

def reconstruct_path(came_from, current):
    """Reconstructs the path from goal to start."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # Reverse the path so it's from start to goal

def adaptive_a_star(grid, start, goal):
    """Adaptive A* search that updates heuristics after each search."""
    h_values = {tile: heuristic(tile, goal) for row in grid.tiles for tile in row}  # Initial heuristic

    while True:
        path, g_score = a_star_search(grid, start, goal, h_values)

        if path is None:
            print("No path found!")
            return None

        # Update heuristic values based on the actual cost
        for tile in path:
            h_values[tile] = g_score[goal] - g_score[tile]  # Adaptive heuristic update

        # Follow the path until an unknown obstacle is encountered
        for step in path:
            if grid.tiles[step.x][step.y].is_blocked:
                break
        else:
            print("Goal reached!")
            return path  # Return path if fully traversable

        # If an obstacle was encountered, update the grid and restart search
        print(f"Blocked tile found at {step.x}, {step.y}. Recalculating...")
        grid.tiles[step.x][step.y].is_blocked = True
