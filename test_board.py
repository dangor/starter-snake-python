import unittest

from board import Board

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
        "body": [{"x": 0, "y": 0}]
      }
    }

  def test_nearest_food(self):
    test_data = self.default_data
    test_data["food"] = [
      {"x": 0, "y": 1},
      {"x": 1, "y": 2},
      {"x": 2, "y": 2}
    ]
    board = Board(test_data)
    nearest = board.nearest_food({"x": 1, "y": 0})

    """
    | |F|F|
    |F| | |
    | |X| |
    """

    self.assertEqual(nearest, {"x": 0, "y": 1})

if __name__ == '__main__':
  unittest.main()
