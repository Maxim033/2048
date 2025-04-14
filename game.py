# game.py
import random
from typing import List, Tuple


class Game:
    """Core game logic for 2048."""

    def __init__(self, size: int = 4):
        self.size = size
        self.reset()

    def reset(self):
        """Reset the game state."""
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()

    @property
    def max_tile(self) -> int:
        """Get the highest tile value on the board."""
        return max(max(row) for row in self.grid)

    def add_new_tile(self):
        """Add a new tile (2 or 4) to a random empty cell."""
        empty_cells = [(i, j) for i in range(self.size)
                       for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction: int) -> bool:
        """
        Move tiles in the specified direction.
        Returns True if movement occurred, False otherwise.
        """
        moved = False
        grid_before = [row[:] for row in self.grid]

        # 0: up, 1: right, 2: down, 3: left
        if direction == 0:  # up
            for j in range(self.size):
                column = [self.grid[i][j] for i in range(self.size) if self.grid[i][j] != 0]
                merged_column = self._merge_tiles(column)
                for i in range(self.size):
                    self.grid[i][j] = merged_column[i] if i < len(merged_column) else 0

        elif direction == 1:  # right
            for i in range(self.size):
                row = [self.grid[i][j] for j in reversed(range(self.size)) if self.grid[i][j] != 0]
                merged_row = self._merge_tiles(row)
                for j in range(self.size):
                    self.grid[i][j] = merged_row[self.size - 1 - j] if j < len(merged_row) else 0

        elif direction == 2:  # down
            for j in range(self.size):
                column = [self.grid[i][j] for i in reversed(range(self.size)) if self.grid[i][j] != 0]
                merged_column = self._merge_tiles(column)
                for i in range(self.size):
                    self.grid[i][j] = merged_column[self.size - 1 - i] if i < len(merged_column) else 0

        elif direction == 3:  # left
            for i in range(self.size):
                row = [self.grid[i][j] for j in range(self.size) if self.grid[i][j] != 0]
                merged_row = self._merge_tiles(row)
                for j in range(self.size):
                    self.grid[i][j] = merged_row[j] if j < len(merged_row) else 0

        # Check if any movement occurred
        moved = any(self.grid[i][j] != grid_before[i][j]
                    for i in range(self.size) for j in range(self.size))

        if moved:
            self.add_new_tile()
            self._check_game_over()

        return moved

    def _merge_tiles(self, line: List[int]) -> List[int]:
        """Merge tiles in a line (row or column)."""
        if not line:
            return line

        merged = []
        i = 0
        while i < len(line):
            if i + 1 < len(line) and line[i] == line[i + 1]:
                merged.append(line[i] * 2)
                self.score += line[i] * 2
                i += 2
            else:
                merged.append(line[i])
                i += 1
        return merged

    def _check_game_over(self):
        """Check if the game is over (no moves left)."""
        # Check for empty cells
        if any(0 in row for row in self.grid):
            self.game_over = False
            return

        # Check for possible merges
        for i in range(self.size):
            for j in range(self.size):
                if (i < self.size - 1 and self.grid[i][j] == self.grid[i + 1][j]) or \
                        (j < self.size - 1 and self.grid[i][j] == self.grid[i][j + 1]):
                    self.game_over = False
                    return

        self.game_over = True