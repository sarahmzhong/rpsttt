import unittest
import rpsttt

class CheckWinner3x3Test(unittest.TestCase):

    def setUp(self):
        self.p1 = rpsttt.Player("Player1")
        self.p2 = rpsttt.Player("Player2")
        self.game = rpsttt.GameInstance(self.p1, self.p2)

    def test_empty_board(self):
        self.game.check_for_winner()
        self.assertEqual(self.game.winner, None)

    def test_row_winner(self):
        self.game.mark_board(0, 0, rpsttt.Mark.X)
        self.game.mark_board(0, 1, rpsttt.Mark.X)
        self.game.mark_board(0, 2, rpsttt.Mark.X)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner.name, "Player1")

    def test_column_winner(self):
        self.game.mark_board(1, 0, rpsttt.Mark.O)
        self.game.mark_board(1, 1, rpsttt.Mark.O)
        self.game.mark_board(1, 2, rpsttt.Mark.O)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner.name, "Player2")

    def test_NW_SE_diag_winner(self):
        self.game.mark_board(0, 0, rpsttt.Mark.X)
        self.game.mark_board(1, 1, rpsttt.Mark.X)
        self.game.mark_board(2, 2, rpsttt.Mark.X)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner.name, "Player1")

    def test_SW_NE_diag_winner(self):
        self.game.mark_board(2, 0, rpsttt.Mark.O)
        self.game.mark_board(1, 1, rpsttt.Mark.O)
        self.game.mark_board(0, 2, rpsttt.Mark.O)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner.name, "Player2")

    def test_no_winner1(self):
        self.game.mark_board(1, 1, rpsttt.Mark.X)
        self.game.mark_board(0, 0, rpsttt.Mark.X)
        self.game.mark_board(2, 2, rpsttt.Mark.O)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner, None)

    def test_no_winner2(self):
        self.game.mark_board(1, 0, rpsttt.Mark.X)
        self.game.mark_board(2, 1, rpsttt.Mark.X)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner, None)

    def test_no_winner3(self):
        self.game.mark_board(0, 1, rpsttt.Mark.X)
        self.game.mark_board(1, 2, rpsttt.Mark.X)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner, None)

    def test_no_winner4(self):
        self.game.mark_board(0, 1, rpsttt.Mark.O)
        self.game.mark_board(1, 0, rpsttt.Mark.O)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner, None)

    def test_no_winner5(self):
        self.game.mark_board(2, 1, rpsttt.Mark.O)
        self.game.mark_board(1, 2, rpsttt.Mark.O)
        self.game.check_for_winner()
        self.assertEqual(self.game.winner, None)


if __name__ == '__main__':
    unittest.main()
