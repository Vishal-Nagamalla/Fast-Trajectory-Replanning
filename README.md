# Fast-Trajectory-Replanning
- Joshua Li - jl2960
- Vishal Nagamalla - Vn218

# Classes
## Tile
### Attributes
- `x: int`, `y: int` - x and y coordinates of a `Tile`
- `visited: bool` - `True` if the `Tile` has been visited
- `blocked: bool` - `True` if the `Tile` is blocked

### Functions
- `__init__(self, x, y)` - Initializes a `Tile` with coordinates (x, y).
- `__eq__(self, other)` - Returns `True` if 2 `Tile` objects share coordinates.
- `__lt__(self, other)` - Defines comparison for heapq (A* priority queue).
- `__hash__(self)` - Allows a `Tile` to be used as a dictionary key.

## Grid
### Attributes
- `width: int` - width of a `Grid`
- `height: int` - height of a `Grid` (same as width in this exercise; could conceivably vary in alternate circumstances)
- `tiles: List[List[Tile]]` - 2D list of all `Tile` objects in the `Grid`.

### Functions
- `get_tile(self, x, y)` - Returns the tile at (x, y) if within bounds.
- `set_blocked(self, x, y)` - Mark a tile as blocked
- `get_neighbors(self, tile)` - Returns non-blocked neighboring tiles in 4-directional movement. If the given tile is blocked, return an empty list.
- `reset(self)` - Resets the grid by unblocking all tiles.
- `printGrid(self)` - Prints the grid, with '1' denoting blocked tiles, and '0' denoting open tiles.

## fwdAstar
Implements Forward Repeated A*, prioritizing tiles with greater g-values during tiebreaking.

## fwdAstarAlternative
Implements Forward Repeated A*, prioritizing tiles with smaller g-values during tiebreaking.

## bwdAstar
Implements Backward Repeated A*, prioritizing tiles with greater g-values during tiebreaking.

## adaptiveAstar
Implements Adaptive A*, prioritizing tiles with greater g-values during tiebreaking.

## driver
Driver
