from collections import deque
from typing import Dict, List

class TreeNode:
  """
  a node module within a tree structure, for use in the search tree functions within this file.
  (N-Queen problem)

  Attributes:
    value(str): String value to represent a cell. Either . or Queen
    left(TreeNode | None): a child node attached to this node (Left Side)
    right(TreeNode | None): A child node attached to this node (Right side)
  """
  def __init__(self, value: str, left = None, right = None):
    self.value = value
    self.left = left # type: ignore
    self.right = right # type: ignore

  def setChildNodes(self, left, right):
    """
    Helper function to set both child nodes at once. 
    Child nodes can be set during initialization.
    """ 
    self.left: TreeNode = left
    self.right: TreeNode = right

def tree_dfs_stack(root: TreeNode) -> List[str]:
  """
  Depth-first search using a stack [first in, last out]
  """
  if not root: return []

  stack = [root]
  visited = []

  while stack:
    # Pop node from stack
    node = stack.pop()

    visited.append(node.value)

    # Push child nodes into stack (right in first -> left-to-right search)
    if node.right: stack.append(node.right)
    if node.left: stack.append(node.left)

  return visited

def tree_bfs_queue(root: TreeNode) -> List[str]:
  """
  Breadth-first search using queue [First in, First out]
  """
  if not root: return []

  queue = deque([root])
  visited = []

  while queue:
    node = queue.popleft()

    visited.append(node.value)

    # Push child nodes into queue (left first for left-to-right)
    if node.left: queue.append(node.left)
    if node.right: queue.append(node.right)

  return visited

def graph_dfs_stack(graph: Dict[str, List[str]], start: str) -> List[str]:
  """
  Depth-first search in graphs using stack [First in, Last out]
  Arguments:
    graph: A Dict containing a string as the key, and a List of strings as the value.
    \nI.E { 'A' : ['B', 'C'] }
  """
  if not graph or not start or start not in graph: return []

  stack = [start]
  order = [start]
  visited = set(start)

  while stack:
    node = stack.pop()

    for neighbor in graph.get(node, []):
      if neighbor not in visited:
        visited.add(neighbor)
        stack.append(neighbor)
        order.append(neighbor)

  return order

def graph_bfs_queue(graph: Dict[str, List[str]], start: str) -> List[str]:
  """
  breadth-first search in graphs using queue [First in, First out]
  Arguments:
    graph: A Dict containing a string as the key, and a List of strings as the value.
    \nI.E { 'A' : ['B', 'C'] }
  """
  if not graph or not start or start not in graph: return []

  queue = deque([start])
  order = [start]
  visited = set(start)

  while queue:
    node = queue.popleft()

    for neighbor in graph.get(node, []):
      if neighbor not in visited:
        visited.add(neighbor)
        queue.append(neighbor)
        order.append(neighbor)

  return order

# Main function of queen.py
def solve_nqueen(n: int, find_all: bool = False) -> List[List[str]]:
  """
  Solve N-Queens using backtracking.
  Returns list of boards (Each board is a list of strings).
  If find_all = false, return only the first solution found.
  """

  board = [["." for _ in range(n)] for _ in range(n)]
  solutions = []

  def is_safe(row: int, col: int) -> bool:
    # Check column above
    for i in range(row):
      if board[i][col] == "Q":
        return False
      
    # upper-left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
      if board[i][j] == "Q": return False
      i -= 1
      j -= 1

    i, j = row - 1, col + 1
    while i >= 0 and j < n:
      if board[i][j] == "Q": return False
      i -= 1
      j += 1

    return True
  
  def backtrack(row: int):
    if row == n:
      # Found a solution
      # When saving solution
      solutions.append([row[:] for row in board])  # deep copy of the 2D list
      return len(solutions) >= 1 and not find_all # Early exit if we only need one solution
    
    for col in range(n):
      if is_safe(row, col):
        board[row][col] = "Q"
        if backtrack(row + 1):
          return True # Early exit if we only need one solution
        board[row][col] = "." # Backtrack

    return False

  backtrack(0)
  return solutions

def print_testing_tree(root: TreeNode | None, name: str = "Tree") -> None:
  """
  Helper function for debugging and testing functions.
  """
  header = f"\n{"="*10} {name} {"="*10}"
  print(header)
  print(f"DFS (stack): {tree_dfs_stack(root)}\n") # type: ignore
  print(f"BFS (queue): {tree_bfs_queue(root)}") # type: ignore
  print(f"{"=" * len(header)}")

def print_testing_graph(graph: Dict[str, List[str]] | None, name: str = "Graph", start: str = "A") -> None:
  """
  Helper function for debugging and testing.
  """
  header = f"\n{"="*10} {name} {"="*10}"
  print(header)
  print(f"Start from {start}")
  print(f"DFS Graph (Stack): {graph_dfs_stack(graph, start)}\n") # type: ignore
  print(f"BFS Graph (Queue): {graph_bfs_queue(graph, start)}\n") # type: ignore
  print(f"{"="*len(header)}")

def print_board(board: List[str], title: str = "", cell_width: int = 3):
  if title:
    print(title)

  for row in board:
    line = "".join(
      ("♛" if c == "Q" else "·").center(cell_width)
      for c in row
    )
    print(line)
  print()

if __name__ == "__main__":
  c = TreeNode("c")
  d = TreeNode("d")
  f = TreeNode("f")
  g = TreeNode("g")
  e = TreeNode("e", f, g)
  b = TreeNode("b", c, d)
  a = TreeNode("a", b, e)

  single = TreeNode("x") # for testing

  # Testing graph
  graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

  print_testing_tree(a, "Example from the book")
  print_testing_tree(single, "Single Node")
  print_testing_tree(None, "Empty Tree")
  print_testing_graph(graph, "Example Graph")
  print_testing_graph(graph, "Example Graph", "F")
  print_testing_graph(None, "Empty input")
  
  for n in [4,5,6,7,8, 9]:
    """
    n-queen will give a board of n x n
    4x4 board got 2 possible solutions.
    5x5 board got 10 possible solutions.
    6x6 board got 4 possible solutions.
    7x7 board got 40 possible solutions.
    8x8 board got 92 possible solutions.
    9x9 board got 352 possible solutions.

    this starts scaling incredibly fast, so for this particular code, don't go much beyond 11.
    (considering that 12x12 board will produce 14200 solutions)
    """
    print(f"\n{"="*35}")
    print(f"N = {n}")

    # One solution only
    solution = solve_nqueen(n)
    if solution:
      print_board(solution[0], "One Solution Only")
    else:
      print(f"No solution found for N = {n}")

    # All solutions
    all_solutions = solve_nqueen(n, True)
    print(f"Total amount of solutions found for a {n}x{n} board: {len(all_solutions)}")
    for i, solution in enumerate(all_solutions, 1):
      if i > 10: 
        print("Breaking after 10 solutions.")
        break
      print_board(solution, f"Solution {i}")

