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
  if not start or start not in graph: return []

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
  if not start or start not in graph: return []

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