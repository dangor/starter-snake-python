import heapq
import sys

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
# Note: Takes in list of tuples and returns list of dicts.
def reconstruct_path(came_from, current):
  (x, y) = current
  total_path = [{"x": x, "y": y}]
  while current in came_from.Keys:
    current = came_from[current]
    (x, y) = current
    total_path.prepend({"x": x, "y": y})
  return total_path

# Heuristic or value of the coord relative to the goal. Typically distance.
# Note: Takes in tuples and not dicts.
def heuristic(coord, goal):
  # return manhattan distance
  (x1, y1) = coord
  (x2, y2) = goal
  return abs(x1 - x2) + abs(y1 - y2)

# Returns the weight or cost of traversing to the given coordinate.
# Zero cost means free, while higher cost discourages traversal.
def weight(coord):
  # TODO: Add weight logic. Some ideas:
  # - Avoid spaces next to long snakes, using higher weight
  # - Avoid food if snake is healthy, using higher weight
  return 0

# Actual A* search (Board object, start coord, goal coord)
def a_star(board, start_coord, goal_coord):
  # TODO: Maybe the entire app should work with tuples.
  start = (start_coord["x"], start_coord["y"])
  goal = (goal_coord["x"], goal_coord["y"])

  open_set = PriorityQueue()
  open_set.put(start, heuristic(start, goal))
  came_from = {}
  gScore = {}
  gScore[start] = 0

  while not open_set.empty():
    current = open_set.get()
    if current == goal:
      return reconstruct_path(came_from, current)

    (x, y) = current
    current_coord = {"x": x, "y": y}
    for neighbor_coord in board.safe_neighbors(current_coord):
      neighbor = (neighbor_coord["x"], neighbor_coord["y"])
      tentative_gScore = gScore[current] + weight(neighbor)
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
