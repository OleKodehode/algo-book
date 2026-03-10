from math import inf
from typing import List, Dict
from time import perf_counter

def multistage_shortest_path(graph: Dict[str, Dict[str, int]], stages: Dict[int, List[str]], source = "A", sink = "L", direction="backward") -> dict:
  # Direction: "Backward" (from source) or "forward" to sink

  dist = {node: inf for stage_nodes in stages.values() for node in stage_nodes}
  prev = {node: None for node in dist} # type: Dict[str, str | None]

  if direction == "backward":
    dist[source] = 0
    for s in range(1, len(stages) + 1):
      for node in stages[s]:
        if dist[node] == inf:
          continue
        
        for vertex, weight in graph.get(node, {}).items():
          new_dist = dist[node] + weight
          if new_dist < dist[vertex]:
            dist[vertex] = new_dist
            prev[vertex] = node
  else:   # Forward to sink
    dist[sink] = 0
    for s in range(len(stages), 0, -1):
      for node in stages[s]:
        min_cost = inf
        best_vertex = ""
        for vertex, weight in graph.get(node, {}).items():
          if dist[vertex] != inf:
            candidate = weight + dist[vertex]
            if candidate < min_cost:
              min_cost = candidate
              best_vertex = vertex
        
        if min_cost != inf:
          dist[node] = min_cost
          prev[node] = best_vertex

  if dist[sink if direction == "backward" else source] == inf:
    return {
      "success": False,
      "message": "No path"
    }
  
  # Path reconstruction
  path = []
  
  if direction == "backward":
    # Backwards starts from sink, follow prev back to source
    current = sink  
  else:
    # Forward - Start from source, follow next to sink
    current = source

  while current is not None:
    path.append(current)
    current = prev[current]
    
  if direction == "backward":
    path.reverse()

  print(dist, prev)

  min_cost = dist[sink if direction == "backward" else source]
  return {
    "success": True,
    "min_cost": min_cost,
    "path": path
  }

# Multistage graph
graph = {
  "A": {"B": 7, "C": 6, "D": 5, "E": 9},
  "B": {"F": 4, "G": 8, "H": 11},
  "C": {"F": 10, "G": 3},
  "D": {"H": 9},
  "E": {"G": 6, "H": 12},
  "F": {"I": 12, "J": 9},
  "G": {"I": 5, "J": 7},
  "H": {"J": 10, "K": 8},
  "I": {"L": 7},
  "J": {"L": 8},
  "K": {"L": 11},
  "L": {},
}

# Stages from that graph
stages = {
  1: ["A"],
  2: ["B", "C", "D", "E"],
  3: ["F", "G", "H"],
  4: ["I", "J", "K"],
  5: ["L"]
}

if __name__ == "__main__":
  start = perf_counter()
  result_backwards = multistage_shortest_path(graph, stages, direction="backward")
  end = perf_counter() - start
  print(result_backwards)
  print(f"Result backwards took {end:.4f}s to complete")

  start = perf_counter()
  result_forward = multistage_shortest_path(graph, stages, direction="forward")
  end = perf_counter() - start
  print(result_forward)
  print(f"Result forwards took {end:.4f}s to complete")