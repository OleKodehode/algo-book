from typing import List

def dynamic_knapsack(values: List[int], weights: list[int], max_weight: int) -> dict:
  if max_weight <0 or not values:
    return {
      "success": False,
      "message": "Invalid input",
    }
  
  n = len(values) # Number of items
  # DP Table: dp[i][w] = Max value using first i items, capacity w
  dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

  # Fill table
  for i in range(1, n + 1):
    val = values[i-1]
    wt = weights[i-1]

    for w in range(max_weight + 1):
      if wt <= w:
        dp[i][w] = max(dp[i-1][w], val + dp[i-1][w - wt])
      else:
        dp[i][w] = dp[i-1][w]

  # Reconstruct selected items (1-based indices)
  selected = []
  i, w = n, max_weight

  while i > 0 and w > 0:
    if dp[i][w] != dp[i-1][w]:
      selected.append(i) # item i (1-based)
      w -= weights[i-1]

    i -= 1

  selected.reverse() # to get in order from 1 to n

  return {
    "success": True,
    "max_value": dp[n][max_weight],
    "selected_items": selected, # 1-based indices
    "table_bottom_right": dp[n][max_weight]
  }

if __name__ == "__main__":
  # Book's example values
  values = [6,5,9,8]
  weights = [3,2,5,4]
  max_weight = 6

  result = dynamic_knapsack(values, weights, max_weight)

  print(result)

  # Book example A
  values = [37,15,22,56,29,23,14]
  weights = [5,2,3,6,4,3,2]
  max_weight = 10
  # Expected results = 4,5 with value 85
  result = dynamic_knapsack(values, weights, max_weight)

  print(result)

  # Book example B
  values = [63,18,41,37,55,24,32,20]
  weights = [6,2,4,3,5,2,3,2]
  max_weight = 9
  # Expected results = 3, 4 and 6 with value 102.
  result = dynamic_knapsack(values, weights, max_weight)

  print(result)

  # Book example C
  values = [31,60,29,18,80,17,38,26]
  weights = [5,2,3,2,6,2,4,3]
  max_weight = 9
  # Expected results = 2,5 with value 140
  result = dynamic_knapsack(values, weights, max_weight)

  print(result)
