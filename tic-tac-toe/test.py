import unittest

from game import Game
from move import Move
from player import Player


def new_game() -> Game:
    return Game(Player("Player 1", "X"), Player("Player 2", "O"))


def apply_move(game: Game, row: int, col: int) -> bool:
    success = game.make_move(Move(row, col))
    if success and not game.is_over():
        game.switch_turn()
    return success


class TestTicTacToe(unittest.TestCase):
    def test_winning_by_horizontal(self) -> None:
        game = new_game()
        moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]
        for row, col in moves:
            apply_move(game, row, col)

        self.assertTrue(game.is_over())
        self.assertEqual(game.winner().symbol, "X")
        self.assertEqual(game.board.check_horizontal(), "X")

    def test_winning_by_vertical(self) -> None:
        game = new_game()
        moves = [(0, 0), (0, 1), (1, 0), (0, 2), (2, 0)]
        for row, col in moves:
            apply_move(game, row, col)

        self.assertTrue(game.is_over())
        self.assertEqual(game.winner().symbol, "X")
        self.assertEqual(game.board.check_vertical(), "X")

    def test_winning_by_diagonal(self) -> None:
        game = new_game()
        moves = [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)]
        for row, col in moves:
            apply_move(game, row, col)

        self.assertTrue(game.is_over())
        self.assertEqual(game.winner().symbol, "X")
        self.assertEqual(game.board.check_diagonal(), "X")

    def test_draw(self) -> None:
        game = new_game()
        # X O O / X O X / O X O — full board, no three in a row
        moves = [
            (0, 0), (0, 1), (1, 0),
            (1, 1), (2, 2), (1, 2),
            (2, 1), (2, 0), (0, 2),
        ]
        for row, col in moves:
            apply_move(game, row, col)

        self.assertTrue(game.is_over())
        self.assertIsNone(game.winner())
        self.assertTrue(game._is_draw)
        self.assertIsNone(game.board.check_winner())

    def test_invalid_move_outside_grid(self) -> None:
        game = new_game()
        self.assertFalse(game.make_move(Move(3, 0)))
        self.assertFalse(game.make_move(Move(-1, 0)))
        self.assertFalse(game.make_move(Move(0, 3)))
        self.assertEqual(game.move_count, 0)
        self.assertEqual(game.current_player.symbol, "X")
        self.assertIsNone(game.board.grid[0][0])

    def test_symbols_alternate_after_each_move(self) -> None:
        game = new_game()
        self.assertEqual(game.current_player.symbol, "X")

        apply_move(game, 0, 0)
        self.assertEqual(game.board.grid[0][0], "X")
        self.assertEqual(game.current_player.symbol, "O")

        apply_move(game, 1, 1)
        self.assertEqual(game.board.grid[1][1], "O")
        self.assertEqual(game.current_player.symbol, "X")


if __name__ == "__main__":
    unittest.main()
