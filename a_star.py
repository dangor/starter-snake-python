import heapq
import sys
from util import manhattan

"""
A* search algorithm, converted from pseudocode in wikipedia article
"""

# Data structure for A*.
# Extract to common file if used elsewhere.
class PriorityQueue:
  def __init__(self):
    self.items = []

  def empty(self):
    return len(self.items) == 0

  def put(self, item, priority):
    heapq.heappush(self.items, (priority, item))

  def get(self):
    return heapq.heappop(self.items)[1]

# Util for returning the full path to the goal at the end of the search
def reconstruct_path(came_from, current):
  total_path = [current]
  while current in came_from:
    current = came_from[current]
    total_path.insert(0, current)
  return total_path

# Heuristic or value of the coord relative to the goal. Typically distance.
def heuristic(coord, goal):
  return manhattan(coord, goal)

# Returns the weight or cost of traversing to the given coordinate.
def weight(board, coord):
  return board.get_weight(coord)

# Actual A* search (Board object, start coord, goal coord)
def a_star(board, start, goal):

  open_set = PriorityQueue()
  open_set.put(start, heuristic(start, goal))
  came_from = {}
  gScore = {}
  gScore[start] = 0

  while not open_set.empty():
    current = open_set.get()
    if current == goal:
      return reconstruct_path(came_from, current)

    for neighbor in board.safe_neighbors(current):
      tentative_gScore = gScore[current] + weight(board, neighbor)
      if neighbor not in gScore:
        gScore[neighbor] = sys.maxsize
      if tentative_gScore < gScore[neighbor]:
        # This path to neighbor is better than any previous one
        came_from[neighbor] = current
        gScore[neighbor] = tentative_gScore
        priority = gScore[neighbor] + heuristic(neighbor, goal)
        open_set.put(neighbor, priority)

  # Open set is empty but goal was never reached
  return []
