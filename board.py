from enum import Enum
import sys
from util import manhattan

"""
Board token types
"""
class TokenType(Enum):
  OUT_OF_BOUNDS = -1
  EMPTY = 0
  SNAKE = 1
  FOOD = 2
  HAZARD = 3

"""
Weights to add for specific spaces, to discourage traversing to it
"""
class Weight(Enum):
  DEFAULT = 0
  BORDER = 1
  UNNECESSARY_FOOD = 2
  OTHER_SNAKE_BODY = 3
  HAZARD = 3
  LONG_SNAKE_HEAD = 15

"""
Board representation
"""
class Board:
  def __init__(self, data):
    board_data, my_data = data["board"], data["you"]

    self.height = board_data["height"]
    self.width = board_data["width"]
    self.food = board_data["food"]

    # Initialize views
    self.board = {} # sparse matrix of tokens
    self.weight = {} # sparse matrix of weights to discourage traversal
    self.safe_tails = set() # hash set of safe tails

    # Process borders
    for i in range(self.width):
      self.add_weight((i, 0), Weight.BORDER)
      self.add_weight((i, self.height - 1), Weight.BORDER)
    for j in range(self.height):
      # Double-weighting the corners, that's okay until we learn more
      self.add_weight((0, j), Weight.BORDER)
      self.add_weight((self.width - 1, j), Weight.BORDER)
    
    # Process snakes
    for snake in board_data["snakes"]:
      # Add snake to board
      for coord in snake["body"]:
        self.board[coord] = TokenType.SNAKE

        if snake["id"] != my_data["id"]:
          self.add_neighbor_weight(coord, Weight.OTHER_SNAKE_BODY)
      
      # Add weights to avoid long snakes
      if snake["id"] != my_data["id"] and len(my_data["body"]) <= len(snake["body"]):
        self.add_neighbor_weight(snake["body"][0], Weight.LONG_SNAKE_HEAD)

      # Add tail if it's safe
      if snake["health"] < 100 and data["turn"] > 2:
        # Assume tail will move
        self.safe_tails.add(snake["body"][-1])

    # Process food
    for food in board_data["food"]:
      # Add food to board
      self.board[food] = TokenType.FOOD

      # If snake is healthy, let's try to discourage eating it
      if my_data["health"] > 20:
        self.add_weight(food, Weight.UNNECESSARY_FOOD)

    # Process hazards
    for hazard in board_data["hazards"]:
      self.board[hazard] = TokenType.HAZARD
      self.add_neighbor_weight(hazard, Weight.HAZARD)

  # Get token type at coord
  def token(self, coord):
    if self.is_out_of_bounds(coord):
      return TokenType.OUT_OF_BOUNDS
    elif coord not in self.board:
      return TokenType.EMPTY
    else:
      return self.board[coord]

  # Return true if out of bounds
  def is_out_of_bounds(self, coord):
    (x, y) = coord
    return x < 0 or y < 0 or x >= self.width or y >= self.height

  # Find nearest food to coord
  def nearest_food(self, coord):
    if len(self.food) == 0:
      return None

    shortest = sys.maxsize

    for food in self.food:
      distance = manhattan(food, coord)
      
      if distance < shortest:
        shortest = distance
        nearest = food

    return nearest
  
  # Calculate distance
  def calculate_distance(self, x1, y1, x2, y2):
    # return manhattan distance
    return abs(x2 - x1) + abs(y2 - y1)

  # Return a list of safe neighbors to go to from coord
  def safe_neighbors(self, coord):
    safe = []

    for neighbor in self.neighbors(coord):
      neighbor_token = self.token(neighbor)
      if neighbor_token == TokenType.EMPTY or neighbor_token == TokenType.FOOD or neighbor in self.safe_tails:
        safe.append(neighbor)

    return safe
  
  # Get list of neighbor coords, exclude out of bounds
  def neighbors(self, coord):
    (x, y) = coord
    neighbors = [
      (x, y + 1),
      (x, y - 1),
      (x + 1, y),
      (x - 1, y)
    ]
    in_bounds = []
    for neighbor in neighbors:
      if not self.is_out_of_bounds(neighbor):
        in_bounds.append(neighbor)
    return in_bounds

  # Add weight to neighbor coords
  def add_neighbor_weight(self, coord, weight):
    for neighbor in self.neighbors(coord):
      self.add_weight(neighbor, weight)

  # Add weight to coord
  def add_weight(self, coord, weight):
    if coord not in self.weight:
      self.weight[coord] = Weight.DEFAULT.value
    self.weight[coord] += weight.value

  # Return weight of coord. Higher value discourages snake traversal.
  def get_weight(self, coord):
    if coord not in self.weight:
      return Weight.DEFAULT.value
    return self.weight[coord]