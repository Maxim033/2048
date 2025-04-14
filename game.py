import random


class Game:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()

    @property
    def max_tile(self):
        return max(max(row) for row in self.grid)

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.size)
                       for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        moved = False
        grid_before = [row[:] for row in self.grid]

        if direction == 0:  # up
            for j in range(self.size):
                column = [self.grid[i][j] for i in range(self.size) if self.grid[i][j] != 0]
                column = self.merge(column)
                for i in range(self.size):
                    self.grid[i][j] = column[i] if i < len(column) else 0

        elif direction == 1:  # right
            for i in range(self.size):
                row = [self.grid[i][j] for j in range(self.size - 1, -1, -1) if self.grid[i][j] != 0]
                row = self.merge(row)
                row = row[::-1]
                for j in range(self.size):
                    self.grid[i][j] = row[j] if (self.size - len(row)) <= j else 0

        elif direction == 2:  # down
            for j in range(self.size):
                column = [self.grid[i][j] for i in range(self.size - 1, -1, -1) if self.grid[i][j] != 0]
                column = self.merge(column)
                column = column[::-1]
                for i in range(self.size):
                    self.grid[i][j] = column[i] if (self.size - len(column)) <= i else 0

        elif direction == 3:  # left
            for i in range(self.size):
                row = [self.grid[i][j] for j in range(self.size) if self.grid[i][j] != 0]
                row = self.merge(row)
                for j in range(self.size):
                    self.grid[i][j] = row[j] if j < len(row) else 0

        moved = any(self.grid[i][j] != grid_before[i][j]
                    for i in range(self.size) for j in range(self.size))

        if moved:
            self.add_new_tile()
            self.check_game_over()

        return moved

    @staticmethod
    def merge(line):
        if not line:
            return line

        merged = []
        i = 0
        while i < len(line):
            if i + 1 < len(line) and line[i] == line[i + 1]:
                merged.append(line[i] * 2)
                i += 2
            else:
                merged.append(line[i])
                i += 1
        return merged

    def check_game_over(self):
        if any(0 in row for row in self.grid):
            self.game_over = False
            return

        for i in range(self.size):
            for j in range(self.size):
                if (i < self.size - 1 and self.grid[i][j] == self.grid[i + 1][j]) or \
                        (j < self.size - 1 and self.grid[i][j] == self.grid[i][j + 1]):
                    self.game_over = False
                    return

        self.game_over = True

    def reset(self):
        self.__init__(self.size)