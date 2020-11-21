import unittest

from board import Board, TokenType
from util import merge_dict, default_data

class TestBoard(unittest.TestCase):
  def test_nearest_food(self):
    test_data = default_data()
    test_data["board"]["food"] = [(0, 1), (1, 2), (2, 2)]
    board = Board(test_data)
    nearest = board.nearest_food((1, 0))

    """
    | |F|F|
    |F| | |
    | |X| |
    """

    self.assertEqual(nearest, (0, 1))

  def test_token(self):
    test_data = default_data()
    test_data["board"]["food"] = [(0, 0)]
    test_data["board"]["hazards"] = [(0, 1)]
    test_data["board"]["snakes"] = [{
      "id": "them",
      "health": 100,
      "body": [(1, 0)]
    }]

    board = Board(test_data)

    self.assertEqual(TokenType.FOOD, board.token((0, 0)))
    self.assertEqual(TokenType.HAZARD, board.token((0, 1)))
    self.assertEqual(TokenType.SNAKE, board.token((1, 0)))
    self.assertEqual(TokenType.EMPTY, board.token((1, 1)))

  # Test based on loss:
  # https://play.battlesnake.com/g/17e79f81-cd93-49b0-a7f5-90a525834243/
  def test_safe_tail(self):
    test_data = default_data()
    merge_dict(test_data, {
      "board": {
        "width": 2,
        "height": 2,
        "snakes": [{
          "id": "me",
          "health": 99,
          "body": [(1, 1), (1, 0), (0, 0), (0, 1)]
        }]
      }
    })
    board = Board(test_data)

    """
    |o|<|
    |o|o|
    """

    self.assertEqual([(0, 1)], board.safe_neighbors((1, 1)))

if __name__ == '__main__':
  unittest.main()
