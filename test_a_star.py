import unittest

from util import merge_dict, default_data
from board import Board
from a_star import a_star

class TestAStar(unittest.TestCase):
  def test_safe_neighbor(self):
    board = Board(default_data())
    start = (0, 0)
    goal = (1, 0)

    """
    | | | |
    | | | |
    |S|G| |
    """

    path = a_star(board, start, goal)
    self.assertEqual(path, [start, goal])

  def test_navigate_around_obstacle(self):
    test_data = default_data()
    merge_dict(test_data, {
      "board": {
        "snakes": [{
          "id": "them",
          "health": 100,
          "body": [(1, 0), (1, 1)]
        }]
      }
    })
    board = Board(test_data)
    start = (0, 0)
    goal = (2, 0)

    """
    | | | |
    | |█| |
    |S|█|G|
    """

    path = a_star(board, start, goal)
    self.assertEqual(path, [
      start,
      (0, 1),
      (0, 2),
      (1, 2),
      (2, 2),
      (2, 1),
      goal
    ])

if __name__ == '__main__':
  unittest.main()
