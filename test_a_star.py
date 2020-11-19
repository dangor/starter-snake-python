import unittest

from util import merge_dict
from board import Board
from a_star import a_star

class TestAStar(unittest.TestCase):
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

  def test_safe_neighbor(self):
    board = Board(self.default_data)
    start = {"x": 0, "y": 0}
    goal = {"x": 1, "y": 0}

    """
    | | | |
    | | | |
    |S|G| |
    """

    path = a_star(board, start, goal)
    self.assertEqual(path, [start, goal])

  def test_navigate_around_obstacle(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "snakes": [{
        "id": "them",
        "body": [
          {"x": 1, "y": 0},
          {"x": 1, "y": 1}
        ]
      }]
    })
    board = Board(test_data)
    start = {"x": 0, "y": 0}
    goal = {"x": 2, "y": 0}

    """
    | | | |
    | |█| |
    |S|█|G|
    """

    path = a_star(board, start, goal)
    self.assertEqual(path, [
      start,
      {"x": 0, "y": 1},
      {"x": 0, "y": 2},
      {"x": 1, "y": 2},
      {"x": 2, "y": 2},
      {"x": 2, "y": 1},
      goal
    ])

if __name__ == '__main__':
  unittest.main()
