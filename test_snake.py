import unittest

from util import merge_dict
from snake import Snake, Move

class TestSnake(unittest.TestCase):
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
        "health": 100,
        "body": [{"x": 0, "y": 0}]
      }
    }
    self.default_moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]

  def test_avoid_wall(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "width": 10,
        "height": 10
      },
      "you": {
        "head": {"x": 0, "y": 9}
      }
    })
    snake = Snake(test_data)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.DOWN, Move.RIGHT])

  def test_avoid_hazard(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "hazards": [{"x": 0, "y": 1}]
      },
      "you": {
        "head": {"x": 1, "y": 1}
      }
    })
    snake = Snake(test_data)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.UP, Move.DOWN, Move.RIGHT])

  def test_avoid_own_body(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "snakes": [{
          "head": {"x": 1, "y": 1},
          "body": [
            {"x": 1, "y": 1},
            {"x": 1, "y": 0}
          ]
        }]
      },
      "you": {
        "head": {"x": 1, "y": 1},
        "body": [
          {"x": 1, "y": 1},
          {"x": 1, "y": 0}
        ]
      }
    })
    snake = Snake(test_data)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.UP, Move.LEFT, Move.RIGHT])

  def test_avoid_other_snake(self):
    test_data = self.default_data
    merge_dict(test_data, {
      "board": {
        "snakes": [{
          "body": [{"x": 2, "y": 1}]
        }]
      },
      "you": {
        "head": {"x": 1, "y": 1}
      }
    })
    snake = Snake(test_data)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.UP, Move.DOWN, Move.LEFT])

if __name__ == '__main__':
  unittest.main()
