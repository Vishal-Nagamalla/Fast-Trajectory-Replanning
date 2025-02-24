# Fast-Trajectory-Replanning
Joshua Li - jl2960
Vishal Nagamalla - Vn218

# Classes
## Tile
### Attributes
- `x: int`, `y: int` - x and y coordinates of the tile
- `visited: bool` - `True` if the `Tile` has been visited
- `blocked: bool` - `True` if the `Tile` is blocked
- `is_goal: bopl` - `True` if the `Tile` is a goal tile
- `g: float`, `f: float` - heuristics
- `parent: Tile` - used to reconstruct path

### Functions
- `__init__(self, x, y)` - Initializes a `Tile` with coordinates (x, y).
- `__repr__(self)` - Returns string representation for a `Tile` (`_` for open tiles, `#` for blocked tiles, `!` for the goal tile.
- `__lt__(self, other)` - Compares `f` of two tiles, returns `True` if `f` of the first is less than that of the other.

## Maze
### Attributes
- `size: int` - side length of the maze
- `maze: List[List[Tile]]` - 2D list of maze tiles
- `start: Tile` - start tile of the maze
- `goal: Tile` - goal tile of the maze
- `traveled_nodes: Set[Tile]` - set of tiles (nodes) visited during DFS (backtracking) maze generation (random maze generation only)

### Functions
- `__init__(self, grid=None, size=101)` - Initializes a square maze of side length `size` (default: 101). If a `grid` (2D list of strings where `S` denotes the start tile, `G` denotes the goal tile, and `X` represents a blocked tile) is provided, generates the maze according to that grid; otherwise generates a random maze using `generate_maze` (see below).
- `generate_maze(self) -> None` - Generates a random `maze` for a `Maze` using depth-first search in the `_dfs_generate` function, then checks its possibility using `is_reachable`; if not reachable, restarts the process after resetting the maze using `reset_maze`.
- `is_reachable(self, start: Tile, goal: Tile) -> bool` - Returns `True` if a given end `Tile` is reachable from a given start `Tile`, and `False` otherwise.
- `get_neighbors(self, tile: Tile) -> List[Tile]` - Returns a list of all unblocked neighbors of a given `Tile` in the maze.
- `reset_maze(self) -> None` - Overwrites the `maze` of a `Maze` with a blank `maze`.
- `_dfs_generate(self, start_x, start_y) -> None` - Generates a `Maze` using depth-first search exploration. Neighboring `Tile`s are obtained using `_get_unvisited_neighbors` (see below), and have a 15% chance of getting blocked.
- `_get_unvisited_neighbors(self, x, y) -> List[Tile]` - Returns a list of all neighbors of a given coordinate `(x, y)` in a `maze` during the generation process.
- `heuristic(self, tile: Tile) -> int` - Returns the A* search heuristic (Manhattan distance between `tile` and the `goal` of the `Maze`).
- `a_star_search(self)` - Runs a Repeated Forward A* search algorithm to find the shortest path from the source to target `Tile`.
- `reconstruct_path(self) -> List[Tuple[int]]]` - Returns the path as a list of coordinates from the `goal` to the `start` tiles.
- `display_grid(self, path=None: List[Tuple[int]]]) -> None` - Prints the grid (where `S` denotes the start tile, `G` denotes the goal tile, and `X` represents a blocked tile), along with the path as `*` if a path is provided.
