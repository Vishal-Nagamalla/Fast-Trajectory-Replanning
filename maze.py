import random

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.blocked = False
        self.is_goal = False

    def __repr__(self):
        if self.blocked:
            return "#"
        elif self.is_goal:
            return "!"
        return "_"

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

    # Similar to A* algorithm, we use an explicit stack for DFS instead of recursion
    def _dfs_generate(self, start_x, start_y):
        stack = [(start_x, start_y)]  

        while stack:
            x, y = stack.pop()
            self.maze[y][x].visited = True

            neighbors = self._get_unvisited_neighbors(x, y)
            random.shuffle(neighbors) 

            for next_tile in neighbors:
                if random.random() <= 0.3:
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

    def display(self):
        for row in self.maze:
            print("".join(str(tile) for tile in row))

#Test Maze Generation
if __name__ == "__main__":
    maze = Maze()
    maze.display()