import unittest

from util import merge_dict, default_data
from snake import Snake

class TestSnake(unittest.TestCase):
  # Test built off of loss:
  # https://play.battlesnake.com/g/df436e2e-4dba-4fac-abbf-e7736aeef3cc/
  def test_take_safer_path(self):
    test_data = default_data()
    my_snake = {
      "id": "me",
      "head": (3, 3),
      "body": [(3, 3), (3, 2), (3, 1), (2, 1)],
      "health": 100
    }
    merge_dict(test_data, {
      "board": {
        "width": 5,
        "height": 5,
        "snakes": [
          my_snake,
          {
            "id": "them",
            "head": (2, 4),
            "body": [(2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)],
            "health": 100
          }
        ]
      },
      "you": my_snake
    })
    snake = Snake(test_data)

    """
    |■|■|>| | |
    |■| | |^| |
    |■| | |ø| |
    |■| |ø|ø| |
    |■| | | | |
    """

    self.assertEqual(snake.next_move(), "right")

  # Test built off of loss:
  # https://play.battlesnake.com/g/858d116f-adb5-4c3c-acdf-63dfbed216c5/
  def test_head_to_head_worse_than_hazards(self):
    test_data = default_data()
    my_snake = {
      "id": "me",
      "head": (4, 2),
      "body": [(4, 2), (3, 2), (3, 1), (2, 1), (2, 2)],
      "health": 100
    }
    merge_dict(test_data, {
      "board": {
        "width": 7,
        "height": 7,
        "hazards": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)],
        "snakes": [
          my_snake,
          {
            "id": "them",
            "head": (4, 4),
            "body": [(4, 4), (3, 4), (3, 5), (4, 5), (4, 6), (3, 6)],
            "health": 100
          }
        ]
      },
      "you": my_snake
    })
    snake = Snake(test_data)

    """
    |■| | |■|■| | |
    |■| | |■|■| | |
    |■| | |■|>| | |
    |■| | | | | | |
    |■| |ø|ø|>| | |
    |■| |ø|ø| | | |
    |■| | | | | | |
    """

    self.assertEqual(snake.next_move(), "down")

  # Test built off of loss:
  # https://play.battlesnake.com/g/5a9c924a-6bd3-460e-8e40-5c39a757fb44/
  def test_avoid_pathing_to_long_snake_head(self):
    test_data = default_data()
    my_snake = {
      "id": "me",
      "head": (2, 3),
      "body": [(2, 3), (2, 4), (1, 4)],
      "health": 100
    }
    merge_dict(test_data, {
      "board": {
        "width": 5,
        "height": 5,
        "snakes": [
          my_snake,
          {
            "id": "them",
            "head": (0, 3),
            "body": [(0, 3), (0, 2), (1, 2), (1, 1), (1, 0)],
            "health": 100
          }
        ]
      },
      "you": my_snake
    })
    snake = Snake(test_data)

    """
    | |ø|ø| | |
    |^| |v| | |
    |■|■| | | |
    | |■| | | |
    | |■| | | |
    """

    self.assertNotEqual(snake.next_move(), "left")

  # Test build off of loss:
  # https://play.battlesnake.com/g/b003577c-03d9-40bb-a715-9813dfbafd96/
  def test_avoid_long_snake_bodies(self):
    test_data = default_data()
    my_snake = {
      "id": "me",
      "health": 100,
      "head": (1, 0),
      "body": [(1, 0), (1, 1), (2, 1)]
    }
    merge_dict(test_data, {
      "board": {
        "width": 5,
        "height": 5,
        "food": [(0, 0)],
        "snakes": [
          my_snake,
          {
            "id": "them",
            "head": (3, 2),
            "body": [(3, 2), (3, 1), (3, 0), (4, 0), (4, 1)],
            "health": 100
          }
        ]
      },
      "you": my_snake
    })
    snake = Snake(test_data)

    """
    | | | | | |
    | | | | | |
    | | | |^| |
    | |ø|ø|■|■|
    |o|v| |■|■|
    """

    self.assertEqual(snake.next_move(), "left")

if __name__ == '__main__':
  unittest.main()
