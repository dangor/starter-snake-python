import unittest

from board import Board, TokenType

class TestBoard(unittest.TestCase):
  def setUp(self):
    self.default_data = {
      "board": {
        "width": 3,
        "height": 3,
        "snakes": [],
        "food": [],
        "hazards": []
      },
      "you": {
        "id": "me",
        "health": 100,
        "body": [(0, 0)]
      }
    }

  def test_nearest_food(self):
    test_data = self.default_data
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
    test_data = self.default_data
    test_data["board"]["food"] = [(0, 0)]
    test_data["board"]["hazards"] = [(0, 1)]
    test_data["board"]["snakes"] = [{
      "id": "them",
      "body": [(1, 0)]
    }]
    board = Board(test_data)

    self.assertEqual(TokenType.FOOD, board.token((0, 0)))
    self.assertEqual(TokenType.HAZARD, board.token((0, 1)))
    self.assertEqual(TokenType.SNAKE, board.token((1, 0)))
    self.assertEqual(TokenType.EMPTY, board.token((1, 1)))

if __name__ == '__main__':
  unittest.main()
