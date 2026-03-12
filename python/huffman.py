import heapq
from collections import Counter
from typing import List, Tuple

class Node:
  def __init__(self, char: str | None, freq: int):
    self.char = char
    self.freq = freq
    self.left = None # type: None | Node
    self.right = None # type: None | Node
    
def huffman_compression(text: str) -> dict:
  """
  Huffman compression algorithm for string inputs.
  [Left some print statements commented - Used print statements to see the flow]
  """
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
    # Only assign a code if it's a leaf (I.E a character and not a parent node)
    if node is not None and len(node.char) == 1: # type: ignore
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
    "msg": "Compression successful",
    "original": text,
    "originalBits": len(text) * 8,
    "encoded": encoded,
    "encodedBits": len(encoded),
    "codes": codes,
  }

def huffman_decompress(encoded: str, codes: dict[str, str]) -> str:
  """
  Decodes a huffman-encoded bitstring using the provided codes dictionary.
  Returns the original text or raises a ValueError on invalid input
  """

  if not encoded:
    return ""
  if not codes:
    raise ValueError("No huffman codes delivered.")
  
  # Reverse loopup: code -> character
  code_to_char = {code: char for char, code in codes.items() if len(char) == 1}

  result = []
  current = ""

  for bit in encoded:
    current += bit
    if current in code_to_char:
      result.append(code_to_char[current])
      current = ""
  
  if current:
    raise ValueError(f"Invalid encoded string - Leftover bits: {current}")
  
  return "".join(result)


if __name__ == "__main__":
  test_texts = [
    "PROGRAMMING ALGORITHM BOOK",
    "Jobloop Kodehode Kurs",
    "aaaaAAAAbbbbBBBBccccCCCC",
    "this is a test with a few repeated letters. Also some symbols! =^-^="
  ]

  for text in test_texts:
    print(f"\n{'='*20}\n")
    print(f"input: {text!r}")
    print(f"Input length: {len(text)*8} bits\n")

    result = huffman_compression(text)
    encoded = result["encoded"]
    codes = result["codes"]

    decoded = huffman_decompress(encoded, codes)

    print(f"Bitstring:\n{encoded}")
    print(f"Encoded length: {len(encoded)} bits\n")
    print(f"Decoded {decoded!r}")
    print(f"Round-trip OK : {decoded == text}")