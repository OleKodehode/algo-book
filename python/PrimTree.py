from typing import Dict, List, Set, Optional
from timing import timing

@timing(enabled=True, prefix="PRIM")
# Greedy Prim-Djikstra Minimum Spanning Tree.
def prim_mst(graph: Dict[str, Dict[str, int]], start: str = "A") -> dict:
  if not graph or start not in graph:
    return {
      "success": False,
      "message": "Invalid graph or start node not found",
      "totalCost": None,
      "edges": [],
      "visitedCount": 0
    }
  
  visited: Set[str] = set()
  parent: Dict[str, Optional[str]] = {}
  connections: Dict[str, float] = {}  # min weights to reach each node

  # Initialization
  for node in graph:
    connections[node] = float("inf")
    parent[node] = None

  connections[start] = 0
  visited.add(start)

  mst_edges: List[dict] = []
  total_cost = 0
  iterations = 0

  # While visited nodes are less than the graph's length
  while len(visited) < len(graph):
      min_weight = float("inf")
      next_node = None
      from_node = None
      iterations += 1

      #Update the best known connections from the current tree
      for node in visited:
         for name, weight in graph[node].items():
            if name not in visited and weight < connections[name]:
               connections[name] = weight
               parent[name] = node
               print(f"Update to connection weights: {name} = {connections[name]}")
               
      # A bit unnecessary to loop over the graph every iteration - This is done for simplicity for now
      # Probably better to keep a set/list of candidates as an intermediate step and loop over those         
      for node in graph:
         if node not in visited and connections[node] < min_weight:
            min_weight = connections[node]
            next_node = node
            from_node = parent[node]
            print(f"Choosing {node} for potential candidate")

      # No more nodes reachable -> Disconnected graph
      if next_node is None:
        return {
           "success": False,
           "message": "Invalid Graph",
           "totalCost": None,
           "edges": mst_edges,
           "visitedCount": len(visited)
        }
      
      # add the chosen node and edge
      visited.add(next_node)
      mst_edges.append({
         "from": from_node,
         "to": next_node,
         "weight": min_weight
      })
      total_cost += min_weight

      print(f"added {next_node} to visited.\nCurrent edges: {mst_edges}")
      print(f"Iteration {iterations} done - Next iteration\n")

  return {
     "success": True,
     "message": "MST Found - Greedy Prim",
     "totalCost": total_cost,
     "edgeCount": len(mst_edges),
     "edges": mst_edges
  }


# Test graph from the book
graph = {
  "A": { "B": 11, "C": 9, "D": 15},
  "B": { "A": 11, "D": 8},
  "C": { "A": 9, "D": 4, "E": 6, "F": 17},
  "D": { "A": 15, "B": 8, "C": 4, "E": 14, "G": 16, "H": 5},
  "E": { "C": 6, "D": 14, "G": 10},
  "F": { "C": 17, "G": 12},
  "G": { "D": 16, "E": 10, "F": 12, "H": 7},
  "H": { "D": 5, "G": 7},
}

if __name__ == "__main__":
   result = prim_mst(graph, "A")

   print(f"Success: {result['success']}")
   print(f"Message: {result['message']}")

   if result["success"]:
      print(f"Total Cost: {result['totalCost']}\n")
      print(f"Number of edges: {result['edgeCount']}\n")
      print(f"Edges:\n")
      for edge in result["edges"]:
         print(f"   {edge['from']}  --({edge['weight']})--> {edge['to']}")
   else:
      print(f"Visited nodes: {result['visitedCount']}")
      print(f"Partial edges:\n")
      for edge in result["edges"]:
         print(f"   {edge['from']} --({edge['weight']})-->  {edge['to']}")