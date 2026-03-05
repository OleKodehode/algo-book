from typing import Dict, List, Set, Optional
from timing import timing

@timing(enabled=True, Prefix="KRUSK")
# Greedy Kruskal Minimum Spanning Tree
def krusk_mst(graph: Dict[str, Dict[str, int]]) -> dict:
   if not graph:
      return {
         "success": False,
         "message": "Invalid graph",
         "totalCost": None,
         "edges": [],
         "visitedCount": 0
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