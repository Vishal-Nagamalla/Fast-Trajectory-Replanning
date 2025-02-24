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
    def __init__(self, size=101):
        self.size = size
        self.maze = [[Tile(x, y) for x in range(size)] for y in range(size)]
        self.start = None
        self.goal = None
        self.traveled_nodes = set()
        self.generate_maze()

    def generate_maze(self):
        start_x, start_y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self._dfs_generate(start_x, start_y)

        if not self.traveled_nodes:
            self.start = self.goal = self.maze[start_y][start_x]
        else:
            self.goal = random.choice(list(self.traveled_nodes))
            self.goal.is_goal = True
            self.start = random.choice(list(self.traveled_nodes))

    def _dfs_generate(self, start_x, start_y):
        #Use an explicit stack for DFS, instead of recursion DFS: RecursionError: maximum recursion depth exceeded
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack.pop()
            self.maze[y][x].visited = True

            neighbors = self._get_unvisited_neighbors(x, y)

            #Randomize the order of neighbors
            random.shuffle(neighbors)

            for next_tile in neighbors:
                if random.random() <= 0.3:
                    next_tile.blocked = True
                else:
                    self.traveled_nodes.add(self.maze[y][x])
                    #bring tile back onto the stack
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

    def display(self):
        for row in self.maze:
            print("".join(str(tile) for tile in row))

    def heuristic(self, tile):
        return abs(tile.x - self.goal.x) + abs(tile.y - self.goal.y)

    def a_star_search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        self.start.g = 0
        self.start.f = self.heuristic(self.start)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == self.goal:
                return self.reconstruct_path()

            for neighbor in self.get_neighbors(current):
                tentative_g = current.g + 1
                if tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.f = neighbor.g + self.heuristic(neighbor)
                    neighbor.parent = current
                    heapq.heappush(open_set, (neighbor.f, neighbor))
        return None

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
        while current:
            path.append((current.x, current.y))
            current = current.parent
        return path[::-1]

#Test the A* algorithm
if __name__ == "__main__":
    maze = Maze()
    maze.display()
    path = maze.a_star_search()
    if path:
        print("Path found:", path)
    else:
        print("No path found")