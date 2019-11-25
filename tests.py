import unittest
import logging
from core import TheGame, CellOccupiedError, NotYourTurnError

from network import Client, Server


class CoreTests(unittest.TestCase):

    def test_invalid_init(self):
        with self.assertRaises(ValueError):
            TheGame(1, 0)

        with self.assertRaises(ValueError):
            TheGame(2, 0)

        with self.assertRaises(ValueError):
            TheGame(3, 0)

        with self.assertRaises(ValueError):
            TheGame(3, 1)

        with self.assertRaises(ValueError):
            TheGame(3, 2)

        with self.assertRaises(ValueError):
            TheGame(3, 4)

    def test_valid_init(self):
        TheGame(3, 3)
        TheGame(4, 4)
        TheGame(5, 4)

    def test_make_invalid_move(self):
        g = TheGame(3, 3)

        with self.assertRaises(NotYourTurnError):
            g.noughts_move(1, 1)

        with self.assertRaises(ValueError):
            g.crosses_move(-1, 1)

    def test_make_move_to_occupied_cell(self):
        g = TheGame(3, 3)
        g.crosses_move(1, 1)

        with self.assertRaises(CellOccupiedError):
            g.noughts_move(1, 1)

    def play(self, g, winner, moves):
        crosses_move = True
        for i, (x, y) in enumerate(moves):
            self.assertEqual(
                winner if i + 1 == len(moves) else None,
                g.make_a_move(crosses_move, x, y)
            )
            crosses_move = not crosses_move

    def test_play_game_3_3(self):
        self.play(
            TheGame(3, 3),
            True,
            [
                (1, 1),
                (3, 1),
                (1, 2),
                (3, 2),
                (1, 3)
            ]
        )

    def test_play_game_3_3_diag(self):
        self.play(
            TheGame(3, 3),
            True,
            [
                (1, 1),
                (3, 1),
                (2, 2),
                (3, 2),
                (3, 3)
            ]
        )

    def test_play_game_6_4(self):
        self.play(
            TheGame(6, 4),
            False,
            [
                (3, 2),
                (3, 1),
                (3, 4),
                (3, 5),
                (3, 3),
                (1, 2),
                (3, 6),
                (1, 4),
                (1, 1),
                (1, 5),
                (1, 6),
                (1, 3)
            ]
        )


class NetworkTests(unittest.TestCase):
    def test_play_match(self):
        server = Server()
        server.start(False)

        client1 = Client('localhost', 8081)
        client2 = Client('localhost', 8081)

        client1_moves = [(1, 1), (2, 2), (3, 3)]
        client2_moves = [(3, 1), (3, 2)]

        client1.on_move_required = lambda ct: (client1_moves if ct else client2_moves).pop(0)
        client1.on_game_over = lambda winner: self.assertTrue(winner)

        client2.on_move_required = lambda ct: (client1_moves if ct else client2_moves).pop(0)
        client2.on_game_over = lambda winner: self.assertTrue(winner)

        client1.start(False)
        client2.start(False)

        client1.wait()
        client2.wait()

        server.stop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

