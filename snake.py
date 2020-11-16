import random

from board import Board, Token
from enum import Enum

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
      token = self.board.token(coord["x"], coord["y"])
      if token == Token.OUT_OF_BOUNDS or token == Token.HAZARD or token == Token.SNAKE:
        new_moves.remove(coord["move"])
        
    return new_moves

  # Get next move
  def next_move(self):
    possible_moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]

    possible_moves = self.avoid_death(possible_moves)

    if len(possible_moves) == 0:
      return Move.UP.value

    # Choose a random direction to move in
    return random.choice(possible_moves).value
