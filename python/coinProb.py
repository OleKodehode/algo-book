from time import perf_counter
"""
Coin Change Problem:
The book covers the coin change problem using 3 different coins.
The value of the coins are: $3, $5 and $12.
The question the book asks is Can someone give change of $23 using those coins?

The book covers 4 different methods;
two Pull techniques, and two Push Techniques.
Pull & Push using the question of "Can X be given?"
Pull & Push using the question of "What's the minimum number of coins to make X?"
"""

target = 23
coin = [3, 5, 12] # Value of the coins

def pull_tech_one():
  local_arr = ["N"] * (target + 1)

  for c in coin:
    if c <= target:
      local_arr[c] = "Y"

  # Main Loop
  for i in range(1, target + 1):
    for c in coin:
      if i - c >= 0 and local_arr[i - c] == "Y":
        local_arr[i] = "Y"

  if local_arr[target] == "Y":
    return f"Value {target} can be given.\n{local_arr}"
  
  return f"Value {target} can't be given.\n{local_arr}"

def push_tech_one():
  local_arr = ["N"] * (target + 1)

  for c in coin:
    if c <= target:
      local_arr[c] = "Y"

  for i in range(target + 1):
    if local_arr[i] == "Y":
      for c in coin:
        next_index = i + c
        if next_index <= target:
          local_arr[next_index] = "Y"
  
  if local_arr[target] == "Y":
    return f"Value {target} can be given.\n{local_arr}"
  
  return f"Value {target} can't be given.\n{local_arr}"

def pull_tech_two():
  local_arr = [float("inf")] * (target + 1)
  local_arr[0] = 0

  for i in range(1, target + 1):
    for c in coin:
      if i - c >= 0 and local_arr[i - c] != float("inf"):
        local_arr[i] = min(local_arr[i], local_arr[i - c] + 1)

  if local_arr[target] == float("inf"):
    return "Impossible combination."
  
  return f"Minimum amount of coins needed to make {target}: {local_arr[23]}\n{local_arr}"

def push_tech_two():
  local_arr = [float("inf")] * (target + 1)
  local_arr[0] = 0 # Not really needed. but supposedly good habit.  

  for c in coin:
    if c <= 23:
      local_arr[c] = 1

  for i in range(target + 1):
    if local_arr[i] != float("inf"):
      for c in coin:
        next_index = i + c

        if next_index <= target:
          local_arr[next_index] = min(local_arr[next_index], local_arr[i] + 1)
    
  if local_arr[target] == float("inf"):
    return "Impossible combination."
  
  return f"Minimum amount of coins needed to make 23: {local_arr[23]}\n{local_arr}" 

if __name__ == "__main__":
  # Timing for each call
  start = perf_counter()
  print(pull_tech_one())
  end = perf_counter() - start
  print(f"Pull Technique #1 took {end:.4f}s to complete.")

  start = perf_counter()
  print(push_tech_one())
  end = perf_counter() - start
  print(f"Push technique # 1 took {end:.4f}s to complete.")
  
  start = perf_counter()
  print(pull_tech_two())
  end = perf_counter() - start
  print(f"Pull technique # 2 took {end:.4f}s to complete.")
  
  start = perf_counter()
  print(push_tech_two())
  end = perf_counter() - start
  print(f"Push technique # 2 took {end:.4f}s to complete.")