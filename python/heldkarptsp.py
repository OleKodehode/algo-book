from math import inf
from typing import Dict, List, Tuple

def held_karp_tsp(graph:Dict[str, Dict[str, int]], start: str = "A") -> dict:
  # Get all nodes - Assumes connected graph
  nodes = list(graph.keys())
  if start not in nodes:
    return {
      "success": False,
      "message": "Start not in graph.",
      "nodes": nodes,
      "start": start
    }
  
  # Remove start from node list - Start might not be the first in the list
  other_nodes = [n for n in nodes if n != start]
  n_other = len(other_nodes)
  node_list = [start] + other_nodes

  # DP table: dp[mask][i]
  # min cost to reach i (index) using the mask
  dp = [[inf] * (n_other + 1) for _ in range(1 << n_other)]
  prev = [[None] * (n_other + 1) for _ in range(1 << n_other)] # type: list[list[int | None]]

  # Base case: From start to each city
  for i in range(1,n_other + 1): # skip the start city
    cost = graph[start].get(node_list[i], inf)
    if cost != inf:
      dp[1 << (i-1)][i] = cost
      prev[1 << (i-1)][i] = 0 # Came from start node

  # Fill DP
  """
  Mask uses binary bits to represent which cities has been visisted.
  The start is always visited, so this only tracks the other nodes.
  
  Example mapping for a 4 city graph [A, B, C, D] where A is the start
  Bit 0 (2^0 = 1): City B (graph[1])
  Bit 1 (2^1 = 2): City C (graph[2])
  Bit 2 (2^2 = 4): City D (graph[3])

  Example masks:
  0b001 (1): Only city B has been visited
  0b011 (3): Cities B and C has been visited
  0b111 (7): All cities has been visited.
  """
  print("Filling DP:")
  for mask in range(1 << n_other): # Visited mask
    for previous_city in range(1, n_other + 1): # index of Last Visited City - usually u
      if dp[mask][previous_city] == inf:
        continue
      for next_city in range(1, n_other + 1): # index of Next city to visit  - usually v
        mask_str = f"0b{mask:0{n_other}b}"
        shifted_str = f"0b{mask & (1 << next_city-1):0{n_other}b}"
        print(f"Mask: {mask_str} - prev city: {previous_city} - next city: {next_city}")
        print(f"Checking mask & (1 << next_city-1): {shifted_str}")
        if mask & (1 << next_city-1):
          print(f"{shifted_str} is true - Skipping")
          continue # already visited

        edge_cost = graph[node_list[previous_city]].get(node_list[next_city], inf)
        if edge_cost == inf:
          print(f"Edge cost is infinity - {edge_cost}")
          continue

        print(f"Setting new mask using mask | (1 << next_city-1): {shifted_str}. Previous mask: {mask_str}")
        new_mask = mask | (1 << next_city-1)
        new_cost = dp[mask][previous_city] + edge_cost
        if new_cost < dp[new_mask][next_city]:
          print(f"new cost of {new_cost} was less than dp[mask][next_city]: {dp[new_mask][next_city]}")
          dp[new_mask][next_city] = new_cost
          prev[new_mask][next_city] = previous_city
        
        print("DP Fill Loop done\n")

  # Final: Return to start from each possible last city.
  full_mask = (1 << n_other) - 1
  min_cost = inf
  last_city = -1
  mask_str = f"0b{full_mask:0{n_other}b}"

  print(f"Checking the return to start from each possible last city with mask: {mask_str}")
  for i in range(1, n_other + 1): # Last city can't be the start, or index 0
    edge_cost = graph[node_list[i]].get(start, inf)
    if edge_cost != inf:
      candidate = dp[full_mask][i] + edge_cost
      if candidate < min_cost:
        min_cost = candidate
        last_city = i
    print("Final fill loop done\n")

  # if a path can't be found
  if min_cost == inf:
    return {
      "success": False,
      "message": "TSP Failed."
    }
  
  print(prev)
  
  # Path Reconstruction
  path = []
  current_mask = full_mask
  current = last_city

  while current is not None:
    path.append(node_list[current])
    prev_city = prev[current_mask][current]
    if prev_city is None:
      break
    current_mask ^= (1 << current - 1) # remove current from mask
    current = prev_city

  path.reverse()
  path.append(start)

  return {
    "success": True,
    "min_cost": min_cost,
    "tour": path,
  }

if __name__ == "__main__":
  # Test graph - Same as exmaple from book.
  graph = {
    "A": {"B": 12, "C": 11, "D": 16},
    "B": {"A": 15, "C": 15, "D": 10},
    "C": {"A": 8, "B": 14, "D": 18},
    "D": {"A": 9, "B": 11, "C": 17},
}

  result = held_karp_tsp(graph)
  for line in result:
    print(f"{line}: {result[line]}")