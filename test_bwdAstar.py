from grid import Grid
from bwdAstar import repeated_backward_astar

def test_bwd_astar():
    """Test Repeated Backward A* search"""
    grid = Grid(5, 5, blocked_cells=[(2, 2), (3, 3)])  # Create a grid with blocked cells
    start = grid.get_tile(0, 0)
    goal = grid.get_tile(4, 4)

    path = repeated_backward_astar(grid, start, goal)

    assert path is not None, "Path should be found if no complete blockage exists"
    assert path[0] == start and path[-1] == goal, "Path should start at start and end at goal"

    print("Repeated Backward A* Test Passed! Path:", path)

if __name__ == "__main__":
    test_bwd_astar()