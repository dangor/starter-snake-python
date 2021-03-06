from board import Board, Weight, TokenType
from enum import Enum
from a_star import a_star
from util import manhattan

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
    # Note that all coordinate dicts are now tuples of ints (x, y)
    me = data["you"]

    self.board = Board(data)

    self.my_head = me["head"]
    self.my_body = me["body"]
    self.my_tail = me["body"][-1]
    self.my_health = me["health"]

  # Get the move direction
  # This assumes the arguments are neighbors.
  def direction(self, start, end):
    if end[1] > start[1]:
      return Move.UP
    elif end[1] < start[1]:
      return Move.DOWN
    elif end[0] > start [0]:
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
    # 1. If healthy, pick direction based on best path to own tail
    if self.my_health > 20:
      direction = self.direction_to_tail()
      if direction != None:
        return direction

    # 2. If unhealthy, pick direction based on best path to food
    nearest_food = self.board.nearest_food(self.my_head)
    if nearest_food != None:
      direction = self.direction_to_coord(nearest_food)
      if direction != None:
        return direction

    # If no path to food, default to tail path
    if self.my_health <= 20:
      direction = self.direction_to_tail()
      if direction != None:
        return direction

    # Fallback: choose lowest weight neighbor
    safe_neighbors = self.board.safe_neighbors(self.my_head)
    if len(safe_neighbors) > 0:
      weighted_neighbors = []
      for neighbor in safe_neighbors:
        weighted_neighbors.append((self.board.get_weight(neighbor), neighbor))
      weighted_neighbors.sort()
      return self.direction(self.my_head, weighted_neighbors[0][1])
    else:
      print("Trapped! Defaulting to up.")
      return Move.UP

  # Get direction to tail
  def direction_to_tail(self):
    direction = self.direction_to_coord(self.my_tail)
    if direction != None:
      return direction

    tail_neighbors = self.board.safe_neighbors(self.my_tail)
    if len(tail_neighbors) > 0:
      # Loop through all neighbors in case the first neighbor is unpathable
      for tail_neighbor in tail_neighbors:
        direction = self.direction_to_coord(tail_neighbor)
        if direction != None:
          return direction

    return None

  # A* search to coord
  def direction_to_coord(self, coord):
    path = a_star(self.board, self.my_head, coord)
    if len(path) > 1 and self.is_low_risk(path[1]):
      return self.direction(path[0], path[1])
    else:
      return None

  # Return true if risk of moving to coord is low
  def is_low_risk(self, coord):
    if self.board.get_weight(coord) >= Weight.LONG_SNAKE_HEAD.value:
      # long snake, high risk
      return False
    
    if len(self.board.safe_neighbors(coord)) > 0:
      # has exit strategy, low risk
      return True

    future_tail = self.my_body[-2]
    if self.my_health == 100:
      # tail is not going to move
      future_tail = self.my_tail

    if self.board.token(coord) != TokenType.FOOD and manhattan(coord, future_tail) <= 1:
      # tail will be safe exit, low risk
      return True

    # Coord has food and there is no exit strategy, high risk
    return False