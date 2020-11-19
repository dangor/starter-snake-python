import random

from board import Board, TokenType
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
    me = data["you"]

    self.board = Board(data)

    self.my_head = me["head"]
    self.my_tail = me["body"][-1]
    self.my_health = me["health"]

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
      if token == TokenType.OUT_OF_BOUNDS or token == TokenType.HAZARD or token == TokenType.SNAKE:
        new_moves.remove(coord["move"])
        
    # TODO: Avoid death by going head-to-head with a longer snake

    return new_moves

  # Get the move direction
  # This assumes the arguments are neighbors.
  def direction(self, start, end):
    if end["y"] > start["y"]:
      return Move.UP
    elif end["y"] < start["y"]:
      return Move.DOWN
    elif end["x"] > start ["x"]:
      return Move.RIGHT
    else:
      return Move.LEFT

  # Get next move, public
  # Returns a move string value
  def next_move(self):
    return self._next_move().value

  # Get next move, private
  # Returns a Move enum
  def _next_move(self):
    possible_moves = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]

    possible_moves = self.avoid_death(possible_moves)

    if len(possible_moves) == 0:
      print("Trapped! Defaulting to move up.")
      # TODO: Chase snake tail, especially if we know it will move.
      return Move.UP

    # 1. If healthy, pick direction based on best path to own tail
    if self.my_health > 20:
      direction = self.direction_to_tail()
      if direction != None:
        return direction

    # 2. If unhealthy, pick direction based on best path to food
    nearest_food = self.board.nearest_food(self.my_head)
    if nearest_food != None:
      food_path = a_star(self.board, self.my_head, nearest_food)
      if len(food_path) > 1 :
        return self.direction(food_path[0], food_path[1])

    # If no path to food, default to tail path
    direction = self.direction_to_tail()
    if direction != None:
      return direction

    # If no tail path, then...

    # TODO: Add more logic as we learn it

    # Default choose random. Points to area for improvement.
    print(f"Failed to path. Defaulting to random.")
    return random.choice(possible_moves)

  # Get direction to tail
  def direction_to_tail(self):
    tail_neighbors = self.board.safe_neighbors(self.my_tail)
    if len(tail_neighbors) > 0:
      # Loop through all neighbors in case the first neighbor is unpathable
      for tail_neighbor in tail_neighbors:
        # TODO: Predict future and see if we will trap ourselves if we go to this square, e.g. if we just ate food
        tail_path = a_star(self.board, self.my_head, tail_neighbor)
        if len(tail_path) > 1 :
          return self.direction(tail_path[0], tail_path[1])
    
    # TODO: Chase snake tail instead of neighbor, especially if we know it will move.

    return None
