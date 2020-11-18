from enum import Enum
import sys

"""
Board token types
"""
class Token(Enum):
  OUT_OF_BOUNDS = -1
  EMPTY = 0
  SNAKE = 1
  FOOD = 2
  HAZARD = 3

"""
Board representation
"""
class Board:
  def __init__(self, board_data):
    # Initialize board
    board = []
    for i in range(board_data["width"]):
      column = []
      for j in range(board_data["height"]):
        column.append(Token.EMPTY)
      board.append(column)
    
    # Add snakes
    for snake in board_data["snakes"]:
      for coord in snake["body"]:
        board[coord["x"]][coord["y"]] = Token.SNAKE

    # Add food
    for food in board_data["food"]:
      board[food["x"]][food["y"]] = Token.FOOD

    # Add hazards
    for hazard in board_data["hazards"]:
      board[hazard["x"]][hazard["y"]] = Token.HAZARD

    self.board = board
    self.height = board_data["height"]
    self.width = board_data["width"]
    self.food = board_data["food"]

  # Get token type at coord
  def token(self, coord):
    x, y = coord["x"], coord["y"]
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      return Token.OUT_OF_BOUNDS

    return self.board[x][y]

  # Find nearest food to coord
  def nearest_food(self, coord):
    if len(self.food) == 0:
      return None

    shortest = sys.maxsize

    for food in self.food:
      distance = self.calculate_distance(food["x"], food["y"], coord["x"], coord["y"])
      
      if distance < shortest:
        shortest = distance
        coords = {"x": food["x"], "y": food["y"]}

    return coords
  
  # Calculate distance
  def calculate_distance(self, x1, y1, x2, y2):
    # return manhattan distance
    return abs(x2 - x1) + abs(y2 - y1)

  # Return a list of safe neighbors to go to from coord
  def safe_neighbors(self, coord):
    neighbors = [
      {"x": coord["x"], "y": coord["y"] + 1},
      {"x": coord["x"], "y": coord["y"] - 1},
      {"x": coord["x"] + 1, "y": coord["y"]},
      {"x": coord["x"] - 1, "y": coord["y"]},
    ]
    safe = []

    for neighbor in neighbors:
      neighbor_token = self.token(neighbor)
      if neighbor_token == Token.EMPTY or neighbor_token == Token.FOOD:
        safe.append(neighbor)

    return safe