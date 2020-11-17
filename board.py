from enum import Enum

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

  # Get token type at x, y coord
  def token(self, x, y):
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      return Token.OUT_OF_BOUNDS

    return self.board[x][y]