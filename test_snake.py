import unittest

from util import merge_dict
from snake import Snake, Move

class TestSnake(unittest.TestCase):
  def setUp(self):
    self.default_data = {
      "board": {
        "width": 4,
        "height": 4,
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

  def test_avoid_wall(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "width": 10,
        "height": 10
      },
      "you": {
        "head": (0, 9)
      }
    })
    snake = Snake(test_data)
    new_moves = snake.avoid_death()
    self.assertEqual(new_moves, [Move.DOWN, Move.RIGHT])

  def test_avoid_hazard(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "hazards": [(0, 1)]
      },
      "you": {
        "head": (1, 1)
      }
    })
    print(test_data)
    snake = Snake(test_data)
    new_moves = snake.avoid_death()
    self.assertEqual(new_moves, [Move.UP, Move.DOWN, Move.RIGHT])

  def test_avoid_own_body(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "snakes": [{
          "id": "me",
          "head": (1, 1),
          "body": [(1, 1), (1, 0)]
        }]
      },
      "you": {
        "head": (1, 1),
        "body": [(1, 1), (1, 0)]
      }
    })
    snake = Snake(test_data)
    new_moves = snake.avoid_death()
    self.assertEqual(new_moves, [Move.UP, Move.LEFT, Move.RIGHT])

  def test_avoid_other_snake(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "snakes": [{
          "id": "them",
          "body": [(2, 1)]
        }]
      },
      "you": {
        "head": (1, 1)
      }
    })
    snake = Snake(test_data)
    new_moves = snake.avoid_death()
    self.assertEqual(new_moves, [Move.UP, Move.DOWN, Move.LEFT])

if __name__ == '__main__':
  unittest.main()
