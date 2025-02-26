from functools import total_ordering

@total_ordering
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_blocked = False

    def reset(self):
        """Reset tile properties"""
        self.is_blocked = False

    def __eq__(self, other):
        return isinstance(other, Tile) and (self.x, self.y) == (other.x, other.y)

    def __lt__(self, other):
        """Defines comparison for heapq (A* priority queue)."""
        return (self.x, self.y) < (other.x, other.y)

    def __hash__(self):
        """Allows Tile to be used as a dictionary key."""
        return hash((self.x, self.y))