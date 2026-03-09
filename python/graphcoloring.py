from typing import Dict, List

# The book's approach
def bookApproach(graph: Dict[str, List[str]]) -> dict:
  colors = ["red", "yellow", "green", "blue"] # Book used 4 colors - Expand if needed

  # number of connections
  connections = {node: len(neighbors) for node, neighbors in graph.items()}

  # Descending sort by number of connections
  sorted_nodes = sorted(graph.keys(), key = lambda n: connections[n], reverse=True)

  # Color initialization
  coloring = {node: "" for node in graph}

  color_index = 0

  while True:
    active_color = colors[color_index]
    assigned_this_pass = False

    # pass over the sorted list
    for node in sorted_nodes:
      if coloring[node] != "":
        continue # Already colored

      can_assign = True
      # Safe to assign this color?
      for neighbor in graph[node]:
        if coloring.get(neighbor) == active_color:
          can_assign = False
          break

      if can_assign:
        coloring[node] = active_color
        assigned_this_pass = True

    # Move to the next color (even if nothing is assigned)
    color_index += 1

    if all(color != "" for color in coloring.values()):
      break

    if color_index >= len(colors):
      colors.append(f"color{color_index + 1}")

  used = set(coloring.values())

  return {
    "success": True,
    "message": "Colored using the book's Welsh-Powell variant",
    "coloring": coloring,
    "color_amount": len(used),
    "colors_used": list(used),
    "node_order": sorted_nodes
  }

def single_pass_coloring(graph: Dict[str, List[str]]) -> dict:
  colors = ["red", "yellow", "green", "blue", "purple", "orange", "brown"] # extend as needed

  connections = {node: len(graph[node]) for node in graph}
  sorted_nodes = sorted(graph, key = lambda node: connections[node], reverse=True)

  coloring = {}

  for node in sorted_nodes:
    used_by_neighbors = {coloring.get(neighbor) for neighbor in graph[node] if neighbor in coloring}

    for color in colors:
      if color not in used_by_neighbors:
        coloring[node] = color
        break
    else:
      # If we ran out of colors
      new_color = f"color{len(colors)}"
      colors.append(new_color)
      coloring[node] = new_color

  used = set(coloring.values())

  return {
    "success": True,
    "coloring": coloring,
    "color_amount": len(used),
    "colors_used": list(used),
    "node_order": sorted_nodes
  }

color_graph = {
  "A": ["B", "E", "H"],
  "B": ["A", "C", "H"],
  "C": ["B", "D", "H"],
  "D": ["C", "H"],
  "E": ["A", "F", "G", "H"],
  "F": ["E", "G"],
  "G": ["E", "F", "H", "I", "K"],
  "H": ["A", "B", "C", "D", "E", "G", "I", "J", "L", "M"],
  "I": ["G", "H", "K", "J"],
  "J": ["H", "I", "L"],
  "K": ["G", "I", "L"],
  "L": ["H", "I", "K", "J", "M"],
  "M": ["H", "L"],
}

if __name__ == "__main__":
  # comment/uncomment the one to show
  #result = bookApproach(color_graph)
  result = single_pass_coloring(color_graph)

  print("Amount of colors used:", result["color_amount"])
  print("\nColoring:")
  for node in sorted(result["coloring"]):
    print(f"{node:2}: {result["coloring"][node]}")

      