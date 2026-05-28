from board import Board
from move import Move
from player import Player


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.board = Board()
        self.players = [player1, player2]
        self.current_player_index = 0  # player 1 starts
        self.move_count = 0
        self._winner_symbol: str | None = None
        self._is_draw = False

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def switch_turn(self) -> None:
        if self.current_player_index == 0:
            self.current_player_index = 1
        else:
            self.current_player_index = 0

    def make_move(self, move: Move) -> bool:
        if not self.board.is_valid_move(move):
            return False
        self.board.place_symbol(move, self.current_player.symbol)
        self.move_count += 1
        self._check_state_after_move()
        return True

    def _check_state_after_move(self) -> None:
        self._winner_symbol = self.board.check_winner()
        if self._winner_symbol is None and self.move_count == Board.SIZE ** 2:
            self._is_draw = True

    def is_over(self) -> bool:
        return self._winner_symbol is not None or self._is_draw

    def winner(self) -> Player | None:
        if self._winner_symbol is None:
            return None
        for player in self.players:
            if player.symbol == self._winner_symbol:
                return player
        return None

    def play(self) -> None:
        print("Tic-Tac-Toe")
        print("Enter row and column (0-2), e.g. 1 2")
        while not self.is_over():
            self.board.display()
            player = self.current_player
            print(f"{player.name}'s turn ({player.symbol})")
            try:
                row, col = map(int, input("Move: ").split())
            except ValueError:
                print("Invalid input. Use two numbers: row col")
                continue
            move = Move(row, col)
            if not self.make_move(move):
                print("Illegal move. Try again.")
                continue
            if not self.is_over():
                self.switch_turn()

        self.board.display()
        winner = self.winner()
        if winner:
            print(f"{winner.name} wins!")
        else:
            print("Draw!")


if __name__ == "__main__":
    game = Game(
        Player("Player 1", "X"),
        Player("Player 2", "O"),
    )
    game.play()
