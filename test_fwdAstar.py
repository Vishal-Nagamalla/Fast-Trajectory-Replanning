from grid import Grid
from fwdAstar import repeated_forward_astar

def test_fwd_astar():
    grid = Grid(5, 5, blocked_cells=[(2, 2), (3, 3)])  # Correct parameter name    
    start = grid.get_tile(0, 0)  # Get Tile object instead of using a tuple
    goal = grid.get_tile(4, 4)

    path = repeated_forward_astar(grid, start, goal)

    assert path is not None, "Path should be found if no complete blockage exists"
    print("Repeated Forward A* Test Passed! Path:", [(tile.x, tile.y) for tile in path])

if __name__ == "__main__":
    test_fwd_astar()