from tile import Tile

class Grid:
    def __init__(self, width, height, blocked_cells=None):
        self.width = width
        self.height = height
        self.tiles = [[Tile(x, y) for y in range(height)] for x in range(width)]

        if blocked_cells:
            for (x, y) in blocked_cells:
                self.tiles[x][y].is_blocked = True  # Mark blocked cells

    def get_tile(self, x, y):
        """Return the tile at (x, y) if within bounds."""
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            return self.tiles[x][y]
        return None

    def set_blocked(self, x, y):
        """Mark a tile as blocked."""
        tile = self.get_tile(x, y)
        if tile:
            tile.is_blocked = True

    def get_neighbors(self, tile):
        """Return non-blocked neighboring tiles in 4-directional movement.
        
        If the given tile is blocked, return an empty list.
        """
        if isinstance(tile, tuple):  
            tile = self.get_tile(tile[0], tile[1])  # Convert (x, y) -> Tile object

        if tile is None or tile.is_blocked:  # Blocked tiles should not have any neighbors
            return []

        x, y = tile.x, tile.y
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down

        for dx, dy in directions:
            neighbor = self.get_tile(x + dx, y + dy)
            if neighbor and not neighbor.is_blocked:  # Only add if not blocked
                neighbors.append(neighbor)

        return neighbors

    def reset(self):
        """Reset the grid by unblocking all tiles."""
        for row in self.tiles:
            for tile in row:
                tile.reset()

    def printGrid(self):
        """Prints the grid, with '1' denoting blocked tiles, and '0' denoting open tiles."""
        for row in self.tiles:
            print("".join("1" if tile.is_blocked else "0" for tile in row))
