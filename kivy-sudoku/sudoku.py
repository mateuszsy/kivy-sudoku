class Sudoku:

    def __init__(self, grid):
        self.grid = grid

    def _valid(self, number, row, col):
        # Check rows and columns
        for i in range(len(self.grid)):
            col_value = self.grid[i][col].text
            row_value = self.grid[row][i].text
            if col_value == number and row != i or row_value == number and col != i:
                return False

        # Set box borders and check for collisions
        border_vertical = col // 3 * 3
        border_horizontal = row // 3 * 3
        for i in range(border_horizontal, border_horizontal + 3):
            for j in range(border_vertical, border_vertical + 3):
                if self.grid[i][j].text == number and row != i and col != j:
                    return False
        return True

    def _find_empty(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if self.grid[row][col].text == '':
                    return row, col
        return

    def solve(self):
        empty_tile = self._find_empty()
        if not empty_tile:
            return True

        row, col = empty_tile
        for i in range(1, 10):
            number = str(i)

            if self._valid(number, row, col):
                self.grid[row][col].text = number

                if self.solve():
                    return True

                self.grid[row][col].text = ''
        return False

    def check(self):
        empty_tile = self._find_empty()
        if empty_tile:
            return False

        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                number = self.grid[row][col].text
                if not self._valid(number, row, col):
                    return False
        return True
