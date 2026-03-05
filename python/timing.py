import functools
import time

def timing(enabled=True, prefix="DEBUG", show_args=False, show_return=False):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      if not enabled:
        return func(*args, **kwargs)
      
      print(f"[{prefix}] Entering {func.__name__}()")
      if show_args:
        print(f"  args  = {args}")
        print(f"  kwargs  = {kwargs}")

      start = time.perf_counter()
      result = func(*args, **kwargs)
      elapsed = time.perf_counter() - start

      if show_return:
        print(f"  Returned: {result}")
      print(f"[{prefix}] Exiting {func.__name__}()  ({elapsed:.4f}s)")

      return result
    return wrapper
  return decorator