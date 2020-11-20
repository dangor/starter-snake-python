import unittest

from util import to_tuple, to_tuples, tuplify, tuplify_snake

class TestUtil(unittest.TestCase):
  def test_to_tuple(self):
    self.assertEqual((1, 2), to_tuple({"x": 1, "y": 2}))

  def test_to_tuples(self):
    expected = [(1, 2), (3, 4)]
    actual = to_tuples([{"x": 1, "y": 2}, {"x": 3, "y": 4}])
    self.assertEqual(expected, actual)

  def test_tuplify_snake(self):
    actual = tuplify_snake({
      "id": "123",
      "head": {"x": 1, "y": 2},
      "body": [
        {"x": 1, "y": 2},
        {"x": 3, "y": 4}
      ]
    })
    expected = {
      "id": "123",
      "head": (1, 2),
      "body": [(1, 2),(3, 4)]
    }
    self.assertEqual(expected, actual)

  def test_tuplify(self):
    actual = tuplify({
      "game": {},
      "board": {
        "width": 5,
        "height": 5,
        "snakes": [{
          "id": "123",
          "head": {"x": 1, "y": 2},
          "body": [
            {"x": 1, "y": 2},
            {"x": 3, "y": 4}
          ]
        }],
        "food": [{"x": 1, "y": 2}],
        "hazards": [{"x": 1, "y": 2}]
      },
      "you": {
        "id": "123",
        "head": {"x": 1, "y": 2},
        "body": [
          {"x": 1, "y": 2},
          {"x": 3, "y": 4}
        ]
      }
    })
    expected = {
      "game": {},
      "board": {
        "width": 5,
        "height": 5,
        "snakes": [{
          "id": "123",
          "head": (1, 2),
          "body": [(1, 2), (3, 4)]
        }],
        "food": [(1, 2)],
        "hazards": [(1, 2)]
      },
      "you": {
        "id": "123",
        "head": (1, 2),
        "body": [(1, 2), (3, 4)]
      }
    }
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
