from grid import Grid
from adaptiveAstar import adaptive_a_star

def test_adaptive_astar():
    """Test Adaptive A* search"""
    grid = Grid(5, 5, blocked_cells=[(2, 2), (3, 3)])  # Create a grid with blocked cells
    start = grid.get_tile(0, 0)
    goal = grid.get_tile(4, 4)

    path = adaptive_a_star(grid, start, goal)

    assert path is not None, "Path should be found if no complete blockage exists"
    assert path[0] == start and path[-1] == goal, "Path should start at start and end at goal"

    print("Adaptive A* Test Passed! Path:", path)

if __name__ == "__main__":
    test_adaptive_astar()