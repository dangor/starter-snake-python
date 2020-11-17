import unittest

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
        "health": 100
      }
    }
    self.default_moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]

  def test_avoid_wall(self):
    testData = self.default_data
    merge(testData, {
      "board": {
        "width": 10,
        "height": 10
      },
      "you": {
        "head": {"x": 0, "y": 9}
      }
    })
    snake = Snake(testData)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.DOWN, Move.RIGHT])

  def test_avoid_hazard(self):
    testData = self.default_data
    merge(testData, {
      "board": {
        "hazards": [{"x": 0, "y": 1}]
      },
      "you": {
        "head": {"x": 1, "y": 1}
      }
    })
    snake = Snake(testData)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.UP, Move.DOWN, Move.RIGHT])

  def test_avoid_own_body(self):
    testData = self.default_data
    merge(testData, {
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
    snake = Snake(testData)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.UP, Move.LEFT, Move.RIGHT])

  def test_avoid_other_snake(self):
    testData = self.default_data
    merge(testData, {
      "board": {
        "snakes": [{
          "body": [{"x": 2, "y": 1}]
        }]
      },
      "you": {
        "head": {"x": 1, "y": 1}
      }
    })
    snake = Snake(testData)
    new_moves = snake.avoid_death(self.default_moves)
    self.assertEqual(new_moves, [Move.UP, Move.DOWN, Move.LEFT])

# Merge two dictionaries recursively, copied from Stackoverflow
def merge(d1, d2):
    for k in d2:
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            merge(d1[k], d2[k])
        else:
            d1[k] = d2[k]

# Some code to make the tests actually run.
if __name__ == '__main__':
  unittest.main()
