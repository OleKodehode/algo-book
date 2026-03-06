from typing import Dict, List, Tuple
from timing import timing

@timing(enabled=True, prefix="KRUSK")
# Greedy Kruskal Minimum Spanning Tree
def krusk_mst(graph: Dict[str, Dict[str, int]]):
   if not graph:
      return {
         "success": False,
         "message": "Invalid graph",
         "totalCost": None,
         "edges": [],
         "edgeCount": 0
      }
   
   # collect unique edges in alphabetic order
   edges: List[Tuple[int, str, str]] = [] # weight, node, connecting node
   for node in graph: 
      for connection in graph[node]:
         # Only need the one direction, I.E A -> B, no need for B -> A
         if node < connection:
            edges.append((graph[node][connection], node, connection))

   edges.sort()

   parent = {node: node for node in graph}
   rank = {node: 0 for node in graph}

   def find(x: str) -> str:
      if parent[x] != x:
         parent[x] = find(parent[x])
      return parent[x]
   
   def union(x: str, y: str) -> bool:
      px = find(x)
      py = find(y)

      if px == py:
         return False
      
      if rank[px] < rank[py]:
         parent[px] = py
      elif rank[px] > rank[py]:
         parent[py] = px
      else:
         parent[py] = px
         rank[px] += 1
      return True

   mst_edges = []
   total_cost = 0

   for weight, node, connection in edges:
      if union(node, connection):
         mst_edges.append({
            "from": node,
            "to": connection,
            "weight": weight
         })
         total_cost += weight

      if len(mst_edges) == len(graph) - 1:
         break

   if len(mst_edges) != len(graph) - 1:
      return {
         "success": False,
         "message": "Invalid Graph",
         "totalCost": None,
         "edges": mst_edges,
         "edgeCount": len(mst_edges)
      }
   
   return {
      "success": True,
      "message": "MST Found - Greedy Kruskal",
      "totalCost": total_cost,
      "edges": mst_edges,
      "edgeCount": len(mst_edges)
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
   result = krusk_mst(graph)


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