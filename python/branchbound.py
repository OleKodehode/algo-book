from math import inf
from typing import List
import copy

# needs to be float due to inf
def branch_and_bound(cost_matrix: List[List[float]]):
  """
  Branch and Bound Traveling Salesman Problem using Reduced Cost Matrix (RCM).
  Should match the steps described in the book.
  Uses the book's 4x4 matrix and should return the optimal tour cost of 44.
  """
  n = len(cost_matrix)
  best_cost = inf
  best_path = None

  # Start with a RCM calculation of the start node
  initial_rcm, initial_reduction = reduce_matrix(cost_matrix)

  # Recursive Branch function
  def branch(current_path, current_cost, current_lb, rcm, level):
    nonlocal best_cost, best_path

    if level == n:
      # Last level, return out
      last = current_path[level-1]
      first = current_path[0]
      tour_cost = current_cost + cost_matrix[last][first]

      if tour_cost < best_cost:
        best_cost = tour_cost
        best_path = current_path[:] + [first]
        
      return
    
    for next_city in range(n):
      if next_city in current_path: continue # Already visited

      new_rcm, new_reduction = create_child_rcm(rcm, current_path[-1], next_city)
      new_lb = current_lb + new_reduction

      if new_lb >= best_cost: continue # no need to keep this

      current_path.append(next_city)
      next_cost = current_cost + cost_matrix[current_path[level-1]][next_city]
      branch(current_path, next_cost, new_lb, new_rcm, level + 1)
      current_path.pop() # Backtracking

  branch([0], 0, initial_reduction, initial_rcm, 1) # start from city 0

  return { 
    "cost": best_cost if best_cost != inf else -1, 
    "path": best_path,
    "tour": " -> ".join(map(str, best_path)) if best_path else None,
    }

def reduce_matrix(matrix: List[List[float]]) -> tuple[List[List[float]], float]:
  n = len(matrix)
  reduced = copy.deepcopy(matrix) # Never mutate original
  reduction = 0

  # Reduce every row
  for i in range(n):
    row_min = min(reduced[i])
    if row_min == inf:
      row_min = 0
    reduction += row_min
    for j in range(n):
      if reduced[i][j] != inf:
        reduced[i][j] -= row_min

  # Reduce every column
  for j in range(n):
    col_min = min(reduced[i][j] for i in range(n))
    if col_min == inf: col_min = 0
    reduction += col_min
    for i in range(n):
      if reduced[i][j] != inf:
        reduced[i][j] -= col_min

  # Return new matrix and lower bound
  return reduced, reduction

def create_child_rcm(parent_rcm: List[List[float]], from_city: int, to_city: int) -> tuple[List[List[float]], float]:
  """
  Sets entire row "from_city" to inf (no more outgoing).\n
  Sets entire column "to_city" to inf (no more incoming).\n
  Sets (to_city, from_city) to inf.\n
  Reduce matrix again.\n
  """
  n = len(parent_rcm)
  child = copy.deepcopy(parent_rcm)

  # outgoing routes from "from_city"
  for j in range(n):
    child[from_city][j] = inf

  # incoming routes to "to_city"
  for i in range(n):
    child[i][from_city] = inf

  child[to_city][from_city] = inf

  # reduce again. Returns new matrix and lower bound
  return reduce_matrix(child)



if __name__ == "__main__":

  cost_matrix = [
    [inf, 12, 11, 16],
    [15, inf, 15, 10],
    [8, 14, inf, 18],
    [9, 11, 17, inf]
  ]

  result = branch_and_bound(cost_matrix)
  print(result)