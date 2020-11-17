import random

from board import Board, Token
from enum import Enum
from a_star import a_star

"""
Move types
"""
class Move(Enum):
  UP = "up"
  DOWN = "down"
  LEFT = "left"
  RIGHT = "right"

"""
Snake AI
"""
class Snake:
  def __init__(self, data):
    # Example move request body:
    # https://docs.battlesnake.com/references/api#request
    self.board = Board(data["board"])

    self.my_head = data["you"]["head"]
    self.my_tail = data["you"]["body"][-1]
    self.my_health = data["you"]["health"]

  # Reduce possible_moves to avoid death from walls, snakes, or hazards
  def avoid_death(self, possible_moves):
    x, y = self.my_head["x"], self.my_head["y"]

    new_moves = possible_moves

    above = {"x": x, "y": y + 1, "move": Move.UP}
    below = {"x": x, "y": y - 1, "move": Move.DOWN}
    left = {"x": x - 1, "y": y, "move": Move.LEFT}
    right = {"x": x + 1, "y": y, "move": Move.RIGHT}

    coords_to_check = [above, below, left, right]

    for coord in coords_to_check:
      token = self.board.token(coord)
      if token == Token.OUT_OF_BOUNDS or token == Token.HAZARD or token == Token.SNAKE:
        new_moves.remove(coord["move"])
        
    return new_moves

  # Get the move direction
  # This assumes the arguments are neighbors.
  def direction(start, end):
    if end["y"] > start["y"]:
      return Move.UP
    elif end["y"] < start["y"]:
      return Move.DOWN
    elif end["x"] > start ["x"]:
      return Move.RIGHT
    else:
      return Move.LEFT

  # Get next move
  def next_move(self):
    possible_moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]

    possible_moves = self.avoid_death(possible_moves)

    if len(possible_moves) == 0:
      print("Trapped! Defaulting to move up.")
      return Move.UP.value

    # 1. If healthy, pick direction based on best path to own tail
    tail_path = []
    tail_neighbors = self.board.safe_neighbors(self.my_tail)
    if len(tail_neighbors) > 0 and self.my_health > 30:
      tail_path = a_star(self.board, self.my_head, tail_neighbors[0])
      if len(tail_path) > 1 :
        return self.direction(tail_path[0], tail_path[1])

    # 2. If unhealthy, pick direction based on best path to food
    nearest_food = self.board.nearest_food(self.my_head)
    if nearest_food != None:
      food_path = a_star(self.board, self.my_head, nearest_food)
      if len(food_path) > 1 :
        return self.direction(food_path[0], food_path[1])

    # If no path to food, default to tail path
    if len(tail_path) > 1 :
      return self.direction(tail_path[0], tail_path[1])

    # If no tail path, then choose random. Points to room for improvement.
    print(f"Failed to path. Defaulting to random.")
    return random.choice(possible_moves).value
