import heapq
from grid import Grid
from tile import Tile

def heuristic(a, b):
    """Manhattan distance heuristic for A*"""
    ax, ay = (a.x, a.y) if isinstance(a, Tile) else a  # Handle both Tile and tuple
    bx, by = (b.x, b.y) if isinstance(b, Tile) else b
    return abs(ax - bx) + abs(ay - by)

def a_star_search(grid, start, goal):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (heuristic(start, goal), -0, start))  # g-value tie-breaker
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current_f, _, current = heapq.heappop(open_set)  # Extract g-value as well

        if current == goal:
            print("Goal reached!")  # Debugging
            return reconstruct_path(came_from, current)

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed_set or neighbor.is_blocked:
                continue
            tentative_g_score = g_score[current] + 1  # Assuming uniform cost
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], -g_score[neighbor], neighbor))
                came_from[neighbor] = current

    print("No path found!")
    return None  # If goal was never reached

def repeated_forward_astar(grid, start, goal):
    """Repeated Forward A* that replans when encountering blocked cells."""
    path = a_star_search(grid, start, goal)
    
    if not path:
        return None  # No possible path to goal

    actual_path = []
    for step in path:
        if grid.get_tile(step.x, step.y).is_blocked:
            # Replan from the last known valid step
            new_start = actual_path[-1]
            new_path = a_star_search(grid, new_start, goal)
            if not new_path:
                return None  # No path exists
            actual_path.extend(new_path)
            break
        else:
            actual_path.append(step)

    return actual_path

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)  # Add the start node
    path.reverse()  # Reverse to get path from start -> goal
    return path
