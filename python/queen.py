from collections import deque

class TreeNode:
  def __init__(self, value: str, left = None, right = None):
    self.value = value
    self.left: TreeNode | None = left
    self.right: TreeNode | None = right

  def setChildNodes(self, left, right): 
    self.left: TreeNode = left
    self.right: TreeNode = right

def tree_dfs_stack(root: TreeNode) -> list[str]:
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

def tree_bfs_queue(root: TreeNode) -> list[str]:
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


def print_testing(root: TreeNode | None, name: str = "Tree") -> None:
  """
  Helper function for debugging and testing functions.
  """
  header = f"\n{"="*10} {name} {"="*10}"
  print(header, "")
  print(f"DFS (stack): {tree_dfs_stack(root)}\n")
  print(f"BFS (queue): {tree_bfs_queue(root)}")
  print(f"{"=" * len(header)}")

if __name__ == "__main__":
  c = TreeNode("c")
  d = TreeNode("d")
  f = TreeNode("f")
  g = TreeNode("g")
  e = TreeNode("e", f, g)
  b = TreeNode("b", c, d)
  a = TreeNode("a", b, e)

  single = TreeNode("x") # for testing

  print_testing(a, "Example from the book")
  print_testing(single, "Single Node")
  print_testing(None, "Empty Tree")