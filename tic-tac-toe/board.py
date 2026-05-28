from move import Move


class Board:
    SIZE = 3

    def __init__(self) -> None:
        self.grid = [[None] * self.SIZE for _ in range(self.SIZE)]

    def is_valid_move(self, move: Move) -> bool:
        if 0 <= move.row < self.SIZE and 0 <= move.col < self.SIZE and self.grid[move.row][move.col] is None:
            return True
        return False

    def place_symbol(self, move: Move, symbol: str) -> None:
        self.grid[move.row][move.col] = symbol

    def check_horizontal(self) -> str | None:
        for row in self.grid:
            if row[0] is not None and row[0] == row[1] == row[2]:
                return row[0]
        return None

    def check_vertical(self) -> str | None:
        for col in range(self.SIZE):
            cells = [self.grid[row][col] for row in range(self.SIZE)]
            if cells[0] is not None and cells[0] == cells[1] == cells[2]:
                return cells[0]
        return None

    def check_diagonal(self) -> str | None:
        main_diag = [self.grid[i][i] for i in range(self.SIZE)]
        if main_diag[0] is not None and main_diag[0] == main_diag[1] == main_diag[2]:
            return main_diag[0]
        anti_diag = [self.grid[i][self.SIZE - 1 - i] for i in range(self.SIZE)]
        if anti_diag[0] is not None and anti_diag[0] == anti_diag[1] == anti_diag[2]:
            return anti_diag[0]
        return None

    def check_winner(self) -> str | None:
        for checker in (self.check_horizontal, self.check_vertical, self.check_diagonal):
            winner = checker()
            if winner is not None:
                return winner
        return None

    def display(self) -> None:
        labels = " ".join(str(i) for i in range(self.SIZE))
        print(f"  {labels}")
        for r in range(self.SIZE):
            row_cells = [
                self.grid[r][c] if self.grid[r][c] is not None else "."
                for c in range(self.SIZE)
            ]
            print(f"{r} {' '.join(row_cells)}")
