from time import perf_counter

""" 
Dynamic programming chapter starts with the fibonacci sequence, 
going over a few different ways of solving it. 
First starting with a rather ineffective algorithm, but shows a few solutions
that are more effective and requires less computing, but more memory
"""

# first a very basic algo - Naive algo
def fibo1(numb: int) -> int:
  if (numb == 1 or numb == 2):
    result = numb - 1
  else:
    result = fibo1(numb - 1) + fibo1(numb - 2)

  return result

""" 
The above will result in quite a lot of function calls however.
Up to several billion calls for the first 50 numbers.
The first 20 takes 0.0053s to finish.
the first 30 takes 0.3451s to finish.
the first 40 takes 38.3405s to finish.
the first 50 would probably take a few minutes to finish.
My laptop isn't the best, results varies depending on hardware."""

# Memoisation using a global variable
def fibo2(numb: int) -> int:
  if (numb == 1 or numb == 2):
    result = numb - 1
  else:
    if memo[numb-1] == 0: 
      memo[numb-1] = fibo2(numb-1)
    if memo[numb-2] == 0:
      memo[numb-2] = fibo2(numb-2)
    
    memo[numb] = memo[numb-1] + memo[numb-2]
    result = memo[numb]

  return result

""" 
The above uses memoisation to optimize the algorithm.
This leads to a significant performance increase over the first fibo algorithm.
The first 50 only took 0.0066s to finish, as compared to several minutes with my laptop.
"""

""" 
The next optimization the book goes over is bottom up memoisation.
it's within the if __name__ == "__main__": block as the third for loop.
Compared to the previous memoisation, this took 0.0034s to finish with my laptop
"""

""" 
The last algorithm the book covers for fibonacci is omitting the array, 
as you only need the last 2 numbers anyways. It's the last for loop in the script.
This saves on memory in cases where you don't need the whole sequence.
in my case, it took 0.0036s to finish. About the same as the one above
"""

""" 
I did see a slight variation on time taken from run to run.
From observations;
Never use Fibo1 (naive function), it's too compute intensive and a huge waste of resources.
Always use at least memoisation if you need to keep track of the sequence.
otherwise it's fine to go with the 2 variable version.
"""


if __name__ == "__main__":
  start = perf_counter()
  for i in range(1, 31):
    print(fibo1(i))
  end = perf_counter() - start
  print(f"Fibo1 took {end:.4f}s to finish")

  start = perf_counter()
  memo = [0 for _ in range(51)]
  for i in range(1, 51):
    print(fibo2(i))
  end = perf_counter() - start
  print(f"Fibo2 took {end:.4f}s to finish")

  # bottom up memoisation
  memo = [0 for _ in range(51)]
  memo[0] = 1
  memo[1] = 1
  start = perf_counter()
  for i in range(2,51):
    memo[i] = memo[i-1] + memo[i-2]
    print(memo[i])
  end = perf_counter() - start
  print(f"Bottom up memoisation took {end:.4f}s to finish")

  # Improved - No arrays
  numb1 = 1
  numb2 = 1
  start = perf_counter()
  print(f"{numb1}\n{numb2}")
  for i in range(2,51):
    next = numb1 + numb2
    print(next)
    numb2 = numb1
    numb1 = next
  end = perf_counter() - start
  print(f"Fibo Sequence omitting arrays took {end:.4f}s to finish")