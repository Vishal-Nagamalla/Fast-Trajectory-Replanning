import random
import heapq

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.blocked = False
        self.is_goal = False
        self.g = float('inf')
        self.f = float('inf')
        self.parent = None

    def __repr__(self):
        if self.blocked:
            return "#"
        elif self.is_goal:
            return "!"
        return "_"

    def __lt__(self, other):
        return self.f < other.f

class Maze:
    def __init__(self, grid=None, size=101):
        if grid:
            self.size = len(grid)
            self.maze = [[Tile(x, y) for x in range(len(grid[0]))] for y in range(len(grid))]
            for y in range(self.size):
                for x in range(len(grid[0])):
                    if grid[y][x] == "X":
                        self.maze[y][x].blocked = True
                    elif grid[y][x] == "G":
                        self.goal = self.maze[y][x]
                        self.goal.is_goal = True
                    elif grid[y][x] == "S":
                        self.start = self.maze[y][x]
        else:
            self.size = size
            self.maze = [[Tile(x, y) for x in range(size)] for y in range(size)]
            self.start = None
            self.goal = None
            self.traveled_nodes = set()
            self.generate_maze()

    def generate_maze(self):
        while True:
            start_x, start_y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self._dfs_generate(start_x, start_y)
            
            if not self.traveled_nodes:
                self.start = self.goal = self.maze[start_y][start_x]
            else:
                self.goal = random.choice(list(self.traveled_nodes))
                self.goal.is_goal = True
                self.start = random.choice(list(self.traveled_nodes))

            # Check if the start and goal are connected
            if self.is_reachable(self.start, self.goal):
                break  # Exit loop if reachable
            else:
                self.reset_maze()  # Regenerate if not reachable

    def is_reachable(self, start, goal):
        queue = [start]
        visited = set([(start.x, start.y)])  # Mark start as visited immediately

        while queue:
            current = queue.pop(0)
            if current == goal:
                return True

            for neighbor in self.get_neighbors(current):
                if (neighbor.x, neighbor.y) not in visited:
                    visited.add((neighbor.x, neighbor.y))
                    queue.append(neighbor)

        return False

    def reset_maze(self):
        """Resets the maze for regeneration."""
        self.maze = [[Tile(x, y) for x in range(self.size)] for y in range(self.size)]
        self.traveled_nodes.clear()

    def _dfs_generate(self, start_x, start_y):
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack.pop()
            self.maze[y][x].visited = True
            neighbors = self._get_unvisited_neighbors(x, y)
            random.shuffle(neighbors)
            for next_tile in neighbors:
                if random.random() <= 0.15:
                    next_tile.blocked = True
                else:
                    self.traveled_nodes.add(self.maze[y][x])
                    stack.append((next_tile.x, next_tile.y))

    def _get_unvisited_neighbors(self, x, y):
        neighbors = []
        if x < self.size - 1 and not self.maze[y][x + 1].visited:
            neighbors.append(self.maze[y][x + 1])
        if y < self.size - 1 and not self.maze[y + 1][x].visited:
            neighbors.append(self.maze[y + 1][x])
        if x > 0 and not self.maze[y][x - 1].visited:
            neighbors.append(self.maze[y][x - 1])
        if y > 0 and not self.maze[y - 1][x].visited:
            neighbors.append(self.maze[y - 1][x])
        return neighbors

    def heuristic(self, tile):
        return abs(tile.x - self.goal.x) + abs(tile.y - self.goal.y)

    def a_star_search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        self.start.g = 0
        self.start.f = self.heuristic(self.start)
        visited = {}

        max_iterations = 50000  # Prevent infinite loops
        iteration = 0

        while open_set:
            iteration += 1
            if iteration > max_iterations:
                print("Exceeded max iterations. Stopping search.")
                return None  # Exit if search takes too long

            _, current = heapq.heappop(open_set)

            if current == self.goal:
                return self.reconstruct_path()

            for neighbor in self.get_neighbors(current):
                tentative_g = current.g + 1
                if tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.f = neighbor.g + self.heuristic(neighbor)
                    neighbor.parent = current

                    if (neighbor.x, neighbor.y) not in visited:
                        visited[(neighbor.x, neighbor.y)] = neighbor.g
                        heapq.heappush(open_set, (neighbor.f, neighbor))

        return None  # No path found

    def get_neighbors(self, tile):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = tile.x + dx, tile.y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbor = self.maze[ny][nx]
                if not neighbor.blocked:
                    neighbors.append(neighbor)
        return neighbors

    def reconstruct_path(self):
        path = []
        current = self.goal
        while current is not None:
            path.append((current.x, current.y))
            current = current.parent
        path.reverse()
        return path if path[0] == (self.start.x, self.start.y) else None
    
    def display_grid(self, path=None):
        grid_display = [["_" for _ in range(self.size)] for _ in range(self.size)]

        # Mark blocked tiles
        for y in range(self.size):
            for x in range(self.size):
                if self.maze[y][x].blocked:
                    grid_display[y][x] = "X"

        # Mark start and goal
        grid_display[self.start.y][self.start.x] = "S"
        grid_display[self.goal.y][self.goal.x] = "G"

        # Mark the path, if provided
        if path:
            for x, y in path:
                if (x, y) not in [(self.start.x, self.start.y), (self.goal.x, self.goal.y)]:
                    grid_display[y][x] = "*"

        # Print the grid
        for row in grid_display:
            print(" ".join(row))

# Run A* if script is executed directly
if __name__ == "__main__":
    maze = Maze()
    path = maze.a_star_search()

    if path:
        print("\n Path found:", path)
        maze.display_grid(path)
    else:
        print("\n No path found")