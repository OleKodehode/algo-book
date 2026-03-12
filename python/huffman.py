import heapq
from collections import Counter
from typing import List, Tuple

class Node:
  def __init__(self, char: str | None, freq: int):
    self.char = char
    self.freq = freq
    self.left = None # type: None | Node
    self.right = None # type: None | Node
    
"""
Huffman compression algorithm for string inputs
Left some print statements commented - Used print statements to see the flow
"""
def huffman_compression(text: str) -> dict:
  if not text or text.strip() == "":
    return {
      "success": False,
      "msg": "Invalid input"
    }
  
  # Dict {letter[str] : frequency[int]}
  freq = Counter(text)

  # Create a heap of nodes using tuples
  index = 0
  heap: List[Tuple[int, int, Node]] = [] # [(frequency, index, Node), (frequency, index, Node), ...]

  for char, f in freq.items():
    node = Node(char,f)
    heap.append((f, index, node))
    index += 1

  heapq.heapify(heap)

  # print("Starting tree building")
  # Binary tree build - Merge the two smallest until only root remains
  merge_index = 1
  while len(heap) > 1:
    left = heapq.heappop(heap)
    right = heapq.heappop(heap)
    # print(f"Popped left: {left[2].char} ({left[0]}),\nright: {right[2].char} ({right[0]})")

    merged_freq = left[0] + right[0]
    char = f"{'root' if len(heap) == 0 else f'*{merge_index}'}"
    merge_index += 1
    parent = Node(char, merged_freq)
    parent.left = left[2]
    parent.right = right[2]

    heapq.heappush(heap, (merged_freq, index, parent))
    index += 1
    # print(f"Created parent ({char}) with frequency {merged_freq} and pushed back into heap.\nHeap size: {len(heap)}\n")

  root = heap[0][2]
  
  # Generating codes
  codes = {}
  def generate(node: Node | None, current: str = ""):
    if node is None: return
    codes[node.char] = current
    generate(node.left, current + "0")
    generate(node.right, current + "1")
    return
  
  generate(root)

  # for char in sorted(codes, key=lambda c: (len(codes[c]), c)):
    # print(f"  {repr(char):<4} : {codes[char]}")

  # Encoding
  encoded = "".join(codes[c] for c in text)
  # print(f"Encoded bitstring:\n{encoded}\nOriginal: {len(text)} char -> {len(text)*8} bits.\nCompressed: {len(encoded)} bits")


  return {
    "success": True,
    "msg": "Compression successfull",
    "original": text,
    "originalBits": len(text) * 8,
    "encoded": encoded,
    "encodedBits": len(encoded),
    "codes": codes,
  }


if __name__ == "__main__":
  text = "PROGRAMMING ALGORITHM BOOK"
  result = huffman_compression(text)

  for line in result:
    print(f"{line}:\n{result[line]}\n")

  text = "Jobloop Kodehode Kurs"
  result = huffman_compression(text)

  for line in result:
    print(f"{line}:\n{result[line]}\n")