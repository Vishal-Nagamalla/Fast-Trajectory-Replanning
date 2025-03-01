import heapq
from grid import Grid
from tile import Tile

def heuristic(a, b):
    """Manhattan distance heuristic for grid-based pathfinding."""
    return abs(a.x - b.x) + abs(a.y - b.y)

def a_star_search(grid, start, goal):
    """A* search algorithm running from goal to start."""
    open_set = []
    heapq.heappush(open_set, (heuristic(goal, start), -0, goal))  # Start from the goal
    came_from = {}

    g_score = {tile: float("inf") for row in grid.tiles for tile in row}
    g_score[goal] = 0

    f_score = {tile: float("inf") for row in grid.tiles for tile in row}
    f_score[goal] = heuristic(goal, start)

    expansions = 0

    while open_set:
        expansions += 1
        _, _, current = heapq.heappop(open_set)

        if current == start:  # If we reached the start, reconstruct path
            return reconstruct_path(came_from, current), expansions

        for neighbor in grid.get_neighbors(current):
            tentative_g_score = g_score[current] + 1  # Uniform cost for grid moves

            if tentative_g_score < g_score[neighbor]:  # Better path found
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, start)

                heapq.heappush(open_set, (f_score[neighbor], -g_score[neighbor], neighbor))

    return None, expansions  # No path found

def reconstruct_path(came_from, current):
    """Reconstructs the path from goal to start."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # Reverse the path so it's from start to goal

def repeated_backward_astar(grid, start, goal):
    """Repeated Backward A* Search Algorithm."""
    while True:
        path, expansions = a_star_search(grid, goal, start)  # Swap start & goal for backward search

        if path is None:
            print("No path found!")
            return None, expansions

        # Follow the path until an unknown obstacle is encountered
        for step in path:
            if grid.tiles[step.x][step.y].is_blocked:
                break
        else:
            print("Goal reached!")
            return path, expansions  # Return path if fully traversable

        # If an obstacle was encountered, update the grid and restart search
        print(f"Blocked tile found at {step.x}, {step.y}. Recalculating...")
        grid.tiles[step.x][step.y].is_blocked = True
