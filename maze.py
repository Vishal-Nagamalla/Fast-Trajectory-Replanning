import random

def generate_maze(rows, cols, obstacle_prob=0.2):
    """Generates a random maze of given size with obstacles."""
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if random.random() < obstacle_prob:
                maze[i][j] = 1  # 1 represents an obstacle
    
    # Ensure start (0,0) and goal (rows-1, cols-1) are open
    maze[0][0] = 0
    maze[rows-1][cols-1] = 0
    
    return maze

def print_maze(maze):
    """Prints the maze in a readable format."""
    for row in maze:
        print(" ".join(str(cell) for cell in row))

# Test the maze generator (optional)
if __name__ == "__main__":
    test_maze = generate_maze(10, 10)
    print_maze(test_maze)