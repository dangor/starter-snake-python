"""
Grab bag of utilities
"""

# Merge two dictionaries recursively, copied from Stackoverflow
def merge_dict(d1, d2):
    for k in d2:
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            merge_dict(d1[k], d2[k])
        else:
            d1[k] = d2[k]

# Convert all known coords to tuples for ease of use
def tuplify(move_data):
  new_data = move_data

  board = move_data["board"]
  new_snakes = []
  for snake in board["snakes"]:
    new_snakes.append(tuplify_snake(snake))
  board["snakes"] = new_snakes
  board["food"] = to_tuples(board["food"])
  board["hazards"] = to_tuples(board["hazards"])

  new_data["board"] = board
  new_data["you"] = tuplify_snake(move_data["you"])
  return new_data

# Convert coords in snake object to tuples
def tuplify_snake(snake):
  new_snake = snake
  new_snake["body"] = to_tuples(snake["body"])
  new_snake["head"] = to_tuple(snake["head"])
  return new_snake

# Convert list of coords to list of tuples
def to_tuples(coords):
  tuples = []
  for coord in coords:
    tuples.append(to_tuple(coord))
  return tuples

# Convert one coord to one tuple
def to_tuple(coord):
  return (coord["x"], coord["y"])

def default_data():
  return {
    "turn": 3,
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
