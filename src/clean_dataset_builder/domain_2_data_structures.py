"""
Domain 2: Data Structures (60 tasks)
Category: Data Structures
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "Data Structures"

    # 1. LRU Cache (OrderedDict)
    tasks.append({
        "instruction": "Implement an LRU (Least Recently Used) Cache class in Python with fixed capacity using collections.OrderedDict.",
        "output": '''from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    """Fixed-capacity Least Recently Used (LRU) Cache."""
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """Retrieve item and mark as most recently used."""
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        """Insert or update item, evicting oldest if at capacity."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)''',
        "category": category
    })

    # 2. LRU Cache from scratch (Doubly Linked List + Dict)
    tasks.append({
        "instruction": "Design an LRU Cache without using OrderedDict, building custom doubly linked list nodes and a hash map.",
        "output": '''from typing import Any, Dict, Optional

class DNode:
    def __init__(self, key: str = "", val: Any = None):
        self.key = key
        self.val = val
        self.prev: Optional[DNode] = None
        self.next: Optional[DNode] = None

class CustomLRUCache:
    """LRU Cache implemented with a custom doubly linked list."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.lookup: Dict[str, DNode] = {}
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DNode) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: DNode) -> None:
        node.next = self.head.next
        node.prev = self.head
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: str) -> Optional[Any]:
        if key not in self.lookup:
            return None
        node = self.lookup[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: str, value: Any) -> None:
        if key in self.lookup:
            node = self.lookup[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.lookup) >= self.capacity:
                lru = self.tail.prev
                if lru and lru != self.head:
                    self._remove(lru)
                    del self.lookup[lru.key]
            new_node = DNode(key, value)
            self.lookup[key] = new_node
            self._add_to_front(new_node)''',
        "category": category
    })

    # 3. LFU Cache
    tasks.append({
        "instruction": "Construct a Least Frequently Used (LFU) Cache in Python that breaks frequency ties by recency.",
        "output": '''from collections import defaultdict, OrderedDict
from typing import Any, Optional

class LFUCache:
    """Least Frequently Used Cache with O(1) get and put."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val: dict[str, Any] = {}
        self.key_to_freq: dict[str, int] = {}
        self.freq_to_keys: dict[int, OrderedDict[str, None]] = defaultdict(OrderedDict)

    def get(self, key: str) -> Optional[Any]:
        if key not in self.key_to_val:
            return None
        freq = self.key_to_freq[key]
        self.key_to_freq[key] = freq + 1
        del self.freq_to_keys[freq][key]
        self.freq_to_keys[freq + 1][key] = None
        if not self.freq_to_keys[freq] and self.min_freq == freq:
            self.min_freq += 1
        return self.key_to_val[key]

    def put(self, key: str, value: Any) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self.get(key)
            return
        if len(self.key_to_val) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1''',
        "category": category
    })

    # 4. Min Heap from scratch
    tasks.append({
        "instruction": "Build a custom MinHeap data structure from scratch with insert, extract_min, and peek methods.",
        "output": '''from typing import List, Optional

class MinHeap:
    """Custom array-backed binary min heap implementation."""
    def __init__(self):
        self.heap: List[float] = []

    def push(self, val: float) -> None:
        """Insert element and bubble up to restore heap invariant."""
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self) -> Optional[float]:
        """Remove and return the smallest element."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return min_val

    def peek(self) -> Optional[float]:
        return self.heap[0] if self.heap else None

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        n = len(self.heap)
        while 2 * idx + 1 < n:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = left
            if right < n and self.heap[right] < self.heap[left]:
                smallest = right
            if self.heap[idx] <= self.heap[smallest]:
                break
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            idx = smallest''',
        "category": category
    })

    # 5. Trie (Prefix Tree)
    tasks.append({
        "instruction": "Create a Prefix Tree (Trie) class in Python supporting insert, exact search, and starts_with prefix queries.",
        "output": '''from typing import Dict

class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False

class Trie:
    """Standard Trie supporting insert, search, and prefix matching."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a string into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Return True if the word is in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word in the trie starts with prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True''',
        "category": category
    })

    # 6. Binary Search Tree (BST)
    tasks.append({
        "instruction": "Write a Binary Search Tree (BST) class supporting node insertion, search, and in-order traversal.",
        "output": '''from typing import List, Optional

class BSTNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None

class BinarySearchTree:
    """Binary Search Tree with insertion and in-order traversal."""
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, val: int) -> None:
        if not self.root:
            self.root = BSTNode(val)
            return
        curr = self.root
        while True:
            if val < curr.val:
                if not curr.left:
                    curr.left = BSTNode(val)
                    break
                curr = curr.left
            else:
                if not curr.right:
                    curr.right = BSTNode(val)
                    break
                curr = curr.right

    def in_order(self) -> List[int]:
        result: List[int] = []
        def traverse(node: Optional[BSTNode]):
            if node:
                traverse(node.left)
                result.append(node.val)
                traverse(node.right)
        traverse(self.root)
        return result''',
        "category": category
    })

    # 7. AVL Tree Node Balance
    tasks.append({
        "instruction": "Implement an AVL Tree with self-balancing single and double rotations maintaining strict logarithmic height.",
        "output": '''from typing import Optional

class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height: int = 1

class AVLTree:
    """Self-balancing AVL Tree supporting O(log n) insertions."""
    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _balance(self, node: Optional[AVLNode]) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        assert x is not None
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = max(self._height(y.left), self._height(y.right)) + 1
        x.height = max(self._height(x.left), self._height(x.right)) + 1
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        assert y is not None
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = max(self._height(x.left), self._height(x.right)) + 1
        y.height = max(self._height(y.left), self._height(y.right)) + 1
        return y

    def insert(self, root: Optional[AVLNode], key: int) -> AVLNode:
        if not root:
            return AVLNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self._height(root.left), self._height(root.right))
        bal = self._balance(root)

        # Left Left
        if bal > 1 and root.left and key < root.left.key:
            return self._rotate_right(root)
        # Right Right
        if bal < -1 and root.right and key > root.right.key:
            return self._rotate_left(root)
        # Left Right
        if bal > 1 and root.left and key > root.left.key:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)
        # Right Left
        if bal < -1 and root.right and key < root.right.key:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)
        return root''',
        "category": category
    })

    # 8. Fenwick Tree (Binary Indexed Tree)
    tasks.append({
        "instruction": "Formulate a Fenwick Tree (Binary Indexed Tree) class supporting point additions and prefix sum queries.",
        "output": '''from typing import List

class FenwickTree:
    """1D Binary Indexed Tree for prefix sums and point updates."""
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        """Add delta to 1-based index."""
        idx = index
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def prefix_sum(self, index: int) -> int:
        """Compute cumulative sum from index 1 to index (inclusive)."""
        s = 0
        idx = index
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & (-idx)
        return s

    def range_sum(self, left: int, right: int) -> int:
        """Compute sum in 1-based range [left, right]."""
        return self.prefix_sum(right) - self.prefix_sum(left - 1)''',
        "category": category
    })

    # 9. Disjoint Set Union (DSU)
    tasks.append({
        "instruction": "Construct a Disjoint Set Union (DSU / Union-Find) data structure featuring path compression and rank optimization.",
        "output": '''class DisjointSetUnion:
    """Disjoint Set Union with path compression and union by rank."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, i: int) -> int:
        """Find the root representative of element i with path compression."""
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """Merge sets containing elements i and j."""
        root_i, root_j = self.find(i), self.find(j)
        if root_i == root_j:
            return False
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        self.count -= 1
        return True''',
        "category": category
    })

    # 10. Circular Buffer (Ring Buffer)
    tasks.append({
        "instruction": "Build a fixed-capacity Circular Buffer in Python with push, pop, is_empty, and is_full methods.",
        "output": '''from typing import Any, List, Optional

class CircularBuffer:
    """Fixed-capacity ring buffer with overwrite prevention."""
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.buffer: List[Optional[Any]] = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def push(self, item: Any) -> bool:
        """Append item to buffer, returning False if full."""
        if self.size == self.capacity:
            return False
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1
        return True

    def pop(self) -> Optional[Any]:
        """Remove and return oldest item, returning None if empty."""
        if self.size == 0:
            return None
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item

    def is_full(self) -> bool:
        return self.size == self.capacity

    def is_empty(self) -> bool:
        return self.size == 0''',
        "category": category
    })

    # 11. Monotonic Stack
    tasks.append({
        "instruction": "Develop a Monotonic Stack algorithm to compute the Next Greater Element for each element in an array.",
        "output": '''from typing import List

def next_greater_elements(nums: List[int]) -> List[int]:
    """Find next greater element for each item using a monotonic decreasing stack."""
    n = len(nums)
    res = [-1] * n
    stack: List[int] = []  # Stores indices
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            res[idx] = nums[i]
        stack.append(i)
        
    return res''',
        "category": category
    })

    # 12. Monotonic Queue (Sliding Window Maximum)
    tasks.append({
        "instruction": "Implement a Monotonic Queue data structure to compute sliding window maximums across an array in O(n) time.",
        "output": '''from collections import deque
from typing import List

class MonotonicQueue:
    """Deque-backed monotonic queue maintaining non-increasing order."""
    def __init__(self):
        self.q = deque()

    def push(self, val: int) -> None:
        while self.q and self.q[-1] < val:
            self.q.pop()
        self.q.append(val)

    def pop(self, val: int) -> None:
        if self.q and self.q[0] == val:
            self.q.popleft()

    def max(self) -> int:
        return self.q[0]

def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
    """Find maximum in every sliding window of size k."""
    if not nums or k <= 0:
        return []
    mq = MonotonicQueue()
    res = []
    for i in range(len(nums)):
        mq.push(nums[i])
        if i >= k - 1:
            res.append(mq.max())
            mq.pop(nums[i - k + 1])
    return res''',
        "category": category
    })

    # 13. Skip List
    tasks.append({
        "instruction": "Design a Skip List data structure with probabilistic node levels supporting insert, search, and delete.",
        "output": '''import random
from typing import List, Optional

class SkipNode:
    def __init__(self, val: int, level: int):
        self.val = val
        self.forward: List[Optional["SkipNode"]] = [None] * level

class SkipList:
    """Probabilistic multi-level skip list for O(log n) search and insertion."""
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p
        self.head = SkipNode(-1, max_level)
        self.level = 1

    def _random_level(self) -> int:
        lvl = 1
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, target: int) -> bool:
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and curr.forward[i].val < target:
                curr = curr.forward[i]
        curr = curr.forward[0]
        return curr is not None and curr.val == target

    def insert(self, num: int) -> None:
        update = [self.head] * self.max_level
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and curr.forward[i].val < num:
                curr = curr.forward[i]
            update[i] = curr

        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level, lvl):
                update[i] = self.head
            self.level = lvl

        new_node = SkipNode(num, lvl)
        for i in range(lvl):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node''',
        "category": category
    })

    # 14. Bloom Filter
    tasks.append({
        "instruction": "Write a Bloom Filter implementation using multiple simulated hash functions over an integer bit array.",
        "output": '''import hashlib
from typing import List

class BloomFilter:
    """Probabilistic set membership filter using multiple hash seeds."""
    def __init__(self, size_bits: int = 1024, num_hashes: int = 4):
        self.size = size_bits
        self.k = num_hashes
        self.bitarray = [0] * size_bits

    def _hashes(self, item: str) -> List[int]:
        hashes = []
        for i in range(self.k):
            digest = hashlib.sha256(f"{i}:{item}".encode("utf-8")).hexdigest()
            hashes.append(int(digest, 16) % self.size)
        return hashes

    def add(self, item: str) -> None:
        """Add item by setting k bit positions to 1."""
        for bit_idx in self._hashes(item):
            self.bitarray[bit_idx] = 1

    def contains(self, item: str) -> bool:
        """Check item membership (zero false negatives, potential false positives)."""
        return all(self.bitarray[bit_idx] == 1 for bit_idx in self._hashes(item))''',
        "category": category
    })

    # 15. Count-Min Sketch
    tasks.append({
        "instruction": "Create a Count-Min Sketch data structure in Python for estimating item occurrence frequencies in streaming data.",
        "output": '''import hashlib
from typing import List

class CountMinSketch:
    """Sublinear space probabilistic frequency estimator."""
    def __init__(self, width: int = 100, depth: int = 5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

    def _hash(self, row: int, item: str) -> int:
        h = hashlib.md5(f"{row}:{item}".encode("utf-8")).hexdigest()
        return int(h, 16) % self.width

    def update(self, item: str, count: int = 1) -> None:
        """Increment count for item across all depth hash rows."""
        for row in range(self.depth):
            col = self._hash(row, item)
            self.table[row][col] += count

    def estimate(self, item: str) -> int:
        """Return point query frequency upper bound estimate."""
        return min(self.table[row][self._hash(row, item)] for row in range(self.depth))''',
        "category": category
    })

    # 16. Sparse Table for Range Minimum Query (RMQ)
    tasks.append({
        "instruction": "Formulate a Sparse Table data structure to answer Range Minimum Queries (RMQ) on static arrays in O(1) time.",
        "output": '''import math
from typing import List

class SparseTableRMQ:
    """Static Range Minimum Query lookup in O(1) query time after O(n log n) preprocessing."""
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        if self.n == 0:
            return
        self.k = int(math.log2(self.n)) + 1
        self.st = [[0] * self.k for _ in range(self.n)]
        
        for i in range(self.n):
            self.st[i][0] = arr[i]
            
        j = 1
        while (1 << j) <= self.n:
            i = 0
            while i + (1 << j) - 1 < self.n:
                self.st[i][j] = min(self.st[i][j - 1], self.st[i + (1 << (j - 1))][j - 1])
                i += 1
            j += 1

    def query(self, L: int, R: int) -> int:
        """Query minimum element in 0-indexed range [L, R]."""
        length = R - L + 1
        k = int(math.log2(length))
        return min(self.st[L][k], self.st[R - (1 << k) + 1][k])''',
        "category": category
    })

    # 17. Min Stack O(1)
    tasks.append({
        "instruction": "Construct a MinStack class that supports push, pop, top, and retrieving the minimum element in constant O(1) time.",
        "output": '''from typing import List, Optional

class MinStack:
    """LIFO Stack tracking minimum value in O(1) time."""
    def __init__(self):
        self.stack: List[int] = []
        self.min_stack: List[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> Optional[int]:
        if not self.stack:
            return None
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val

    def top(self) -> Optional[int]:
        return self.stack[-1] if self.stack else None

    def get_min(self) -> Optional[int]:
        return self.min_stack[-1] if self.min_stack else None''',
        "category": category
    })

    # 18. Queue via Two Stacks
    tasks.append({
        "instruction": "Engineer a FIFO Queue data structure implemented using two LIFO Stacks.",
        "output": '''from typing import Any, List, Optional

class MyQueue:
    """FIFO Queue using two LIFO stacks."""
    def __init__(self):
        self.in_stack: List[Any] = []
        self.out_stack: List[Any] = []

    def push(self, x: Any) -> None:
        self.in_stack.append(x)

    def pop(self) -> Optional[Any]:
        self.peek()
        return self.out_stack.pop() if self.out_stack else None

    def peek(self) -> Optional[Any]:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack[-1] if self.out_stack else None

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack''',
        "category": category
    })

    # 19. Time-Based Key-Value Store
    tasks.append({
        "instruction": "Build a time-based key-value data structure that stores values at timestamps and retrieves the closest past value.",
        "output": '''import bisect
from collections import defaultdict
from typing import Dict, List, Tuple

class TimeMap:
    """Key-value store retrieving values by timestamp using binary search."""
    def __init__(self):
        self.store: Dict[str, List[Tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        entries = self.store[key]
        idx = bisect.bisect_right(entries, (timestamp, chr(127)))
        if idx == 0:
            return ""
        return entries[idx - 1][1]''',
        "category": category
    })

    # 20. BitSet
    tasks.append({
        "instruction": "Implement a BitSet class supporting set, clear, test, count, and bitwise AND/OR operations over integer bit words.",
        "output": '''from typing import List

class BitSet:
    """Memory-efficient bit array implementation using 64-bit integer words."""
    def __init__(self, size: int):
        self.size = size
        self.words: List[int] = [0] * ((size + 63) // 64)

    def set(self, idx: int) -> None:
        if not 0 <= idx < self.size: raise IndexError("Index out of bounds")
        self.words[idx // 64] |= (1 << (idx % 64))

    def clear(self, idx: int) -> None:
        if not 0 <= idx < self.size: raise IndexError("Index out of bounds")
        self.words[idx // 64] &= ~(1 << (idx % 64))

    def test(self, idx: int) -> bool:
        if not 0 <= idx < self.size: raise IndexError("Index out of bounds")
        return bool(self.words[idx // 64] & (1 << (idx % 64)))

    def count(self) -> int:
        return sum(bin(w).count("1") for w in self.words)''',
        "category": category
    })

    # 21. Bi-directional Map (BiMap)
    tasks.append({
        "instruction": "Design a Bidirectional Map (BiMap) that enforces 1-to-1 uniqueness and supports forward and inverse key-value lookups.",
        "output": '''from typing import Any, Dict, Optional

class BiMap:
    """1-to-1 two-way dictionary supporting constant time forward and reverse lookup."""
    def __init__(self):
        self._forward: Dict[Any, Any] = {}
        self._reverse: Dict[Any, Any] = {}

    def put(self, key: Any, value: Any) -> None:
        if key in self._forward:
            del self._reverse[self._forward[key]]
        if value in self._reverse:
            del self._forward[self._reverse[value]]
        self._forward[key] = value
        self._reverse[value] = key

    def get_by_key(self, key: Any) -> Optional[Any]:
        return self._forward.get(key)

    def get_by_value(self, value: Any) -> Optional[Any]:
        return self._reverse.get(value)

    def remove_key(self, key: Any) -> None:
        if key in self._forward:
            val = self._forward.pop(key)
            del self._reverse[val]''',
        "category": category
    })

    # 22. QuadTree for 2D Points
    tasks.append({
        "instruction": "Construct a 2D QuadTree spatial index supporting point insertion and 2D bounding box range queries.",
        "output": '''from typing import List, NamedTuple, Optional

class Point(NamedTuple):
    x: float
    y: float

class Rect(NamedTuple):
    x: float
    y: float
    w: float
    h: float
    def contains(self, p: Point) -> bool:
        return self.x <= p.x <= self.x + self.w and self.y <= p.y <= self.y + self.h
    def intersects(self, other: "Rect") -> bool:
        return not (other.x > self.x + self.w or other.x + other.w < self.x or
                    other.y > self.y + self.h or other.y + other.h < self.y)

class QuadTree:
    """Recursive 2D space-partitioning QuadTree for point queries."""
    def __init__(self, boundary: Rect, capacity: int = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.points: List[Point] = []
        self.divided = False
        self.nw: Optional[QuadTree] = None
        self.ne: Optional[QuadTree] = None
        self.sw: Optional[QuadTree] = None
        self.se: Optional[QuadTree] = None

    def subdivide(self) -> None:
        b = self.boundary
        hw, hh = b.w / 2.0, b.h / 2.0
        self.nw = QuadTree(Rect(b.x, b.y + hh, hw, hh), self.capacity)
        self.ne = QuadTree(Rect(b.x + hw, b.y + hh, hw, hh), self.capacity)
        self.sw = QuadTree(Rect(b.x, b.y, hw, hh), self.capacity)
        self.se = QuadTree(Rect(b.x + hw, b.y, hw, hh), self.capacity)
        self.divided = True

    def insert(self, p: Point) -> bool:
        if not self.boundary.contains(p):
            return False
        if len(self.points) < self.capacity:
            self.points.append(p)
            return True
        if not self.divided:
            self.subdivide()
        assert self.nw and self.ne and self.sw and self.se
        return (self.nw.insert(p) or self.ne.insert(p) or
                self.sw.insert(p) or self.se.insert(p))

    def query_range(self, range_rect: Rect) -> List[Point]:
        found: List[Point] = []
        if not self.boundary.intersects(range_rect):
            return found
        for p in self.points:
            if range_rect.contains(p):
                found.append(p)
        if self.divided and self.nw and self.ne and self.sw and self.se:
            found.extend(self.nw.query_range(range_rect))
            found.extend(self.ne.query_range(range_rect))
            found.extend(self.sw.query_range(range_rect))
            found.extend(self.se.query_range(range_rect))
        return found''',
        "category": category
    })

    # 23. Doubly Linked List with reversal
    tasks.append({
        "instruction": "Develop a generic Doubly Linked List class supporting push_back, push_front, pop_front, and in-place reversal.",
        "output": '''from typing import Any, List, Optional

class Node:
    def __init__(self, val: Any):
        self.val = val
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class DoublyLinkedList:
    """Doubly Linked List with in-place pointer reversal."""
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def push_back(self, val: Any) -> None:
        new_node = Node(val)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def reverse(self) -> None:
        curr = self.head
        self.tail = self.head
        prev_node = None
        while curr:
            next_node = curr.next
            curr.next = prev_node
            curr.prev = next_node
            prev_node = curr
            curr = next_node
        self.head = prev_node

    def to_list(self) -> List[Any]:
        res = []
        curr = self.head
        while curr:
            res.append(curr.val)
            curr = curr.next
        return res''',
        "category": category
    })

    # 24. Singly Linked List Cycle Detection (Floyd's Tortoise and Hare)
    tasks.append({
        "instruction": "Write Floyd's Tortoise and Hare cycle detection algorithm to locate the cycle entry node in a singly linked list.",
        "output": '''from typing import Optional

class ListNode:
    def __init__(self, val: int = 0):
        self.val = val
        self.next: Optional[ListNode] = None

def detect_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """Return the node where the cycle begins, or None if no cycle exists."""
    if not head or not head.next:
        return None
    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head

    while fast and fast.next:
        slow = slow.next  # type: ignore
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None

    # Find cycle start
    ptr1 = head
    ptr2 = slow
    while ptr1 != ptr2:
        ptr1 = ptr1.next  # type: ignore
        ptr2 = ptr2.next  # type: ignore
        
    return ptr1''',
        "category": category
    })

    # 25. Segment Tree with Lazy Propagation
    tasks.append({
        "instruction": "Implement a Lazy Propagation Segment Tree supporting range addition updates and range sum queries in O(log n).",
        "output": '''from typing import List

class LazySegmentTree:
    """Segment Tree with lazy propagation for range addition and range sum."""
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [0] * (4 * n)

    def _apply(self, node: int, start: int, end: int, val: int) -> None:
        self.tree[node] += val * (end - start + 1)
        self.lazy[node] += val

    def _push(self, node: int, start: int, end: int) -> None:
        if self.lazy[node] != 0 and start != end:
            mid = (start + end) // 2
            self._apply(2 * node, start, mid, self.lazy[node])
            self._apply(2 * node + 1, mid + 1, end, self.lazy[node])
            self.lazy[node] = 0

    def update_range(self, l: int, r: int, val: int, node: int = 1, start: int = 0, end: int = -1) -> None:
        if end == -1: end = self.n - 1
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self._apply(node, start, end, val)
            return
        self._push(node, start, end)
        mid = (start + end) // 2
        self.update_range(l, r, val, 2 * node, start, mid)
        self.update_range(l, r, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query_range(self, l: int, r: int, node: int = 1, start: int = 0, end: int = -1) -> int:
        if end == -1: end = self.n - 1
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        self._push(node, start, end)
        mid = (start + end) // 2
        return self.query_range(l, r, 2 * node, start, mid) + self.query_range(l, r, 2 * node + 1, mid + 1, end)''',
        "category": category
    })

    # 26. Treap (Cartesian Tree)
    tasks.append({
        "instruction": "Create a Treap (Cartesian Tree) node structure supporting randomized binary search tree split and merge operations.",
        "output": '''import random
from typing import Optional, Tuple

class TreapNode:
    def __init__(self, key: int):
        self.key = key
        self.priority = random.random()
        self.left: Optional[TreapNode] = None
        self.right: Optional[TreapNode] = None

def treap_split(root: Optional[TreapNode], key: int) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
    """Split treap into two trees: (<= key, > key)."""
    if not root:
        return None, None
    if root.key <= key:
        l, r = treap_split(root.right, key)
        root.right = l
        return root, r
    else:
        l, r = treap_split(root.left, key)
        root.left = r
        return l, root

def treap_merge(left: Optional[TreapNode], right: Optional[TreapNode]) -> Optional[TreapNode]:
    """Merge two treaps where all keys in left <= all keys in right."""
    if not left or not right:
        return left or right
    if left.priority > right.priority:
        left.right = treap_merge(left.right, right)
        return left
    else:
        right.left = treap_merge(left, right.left)
        return right''',
        "category": category
    })

    # 27. Priority Queue with Decrease Key
    tasks.append({
        "instruction": "Build an indexed priority queue wrapper around heapq that supports dynamic key priority decreases.",
        "output": '''from typing import Any, Dict, List, Optional, Tuple

class IndexMinPQ:
    """Indexed min-priority queue supporting O(log n) decrease-key."""
    def __init__(self):
        self.heap: List[Tuple[float, str, Any]] = []
        self.entry_finder: Dict[str, List] = {}
        self.counter = 0

    def add_task(self, task_id: str, priority: float, data: Any = None) -> None:
        """Add task or update priority if already present."""
        if task_id in self.entry_finder:
            self.remove_task(task_id)
        entry = [priority, self.counter, task_id, data]
        self.entry_finder[task_id] = entry
        self.counter += 1
        self.heap.append(entry)
        self._bubble_up(len(self.heap) - 1)

    def remove_task(self, task_id: str) -> None:
        entry = self.entry_finder.pop(task_id, None)
        if entry:
            entry[-1] = None  # Mark as removed

    def pop_task(self) -> Optional[Tuple[str, float, Any]]:
        while self.heap:
            entry = self.heap[0]
            self._remove_top()
            if entry[-1] is not None:
                del self.entry_finder[entry[2]]
                return entry[2], entry[0], entry[3]
        return None

    def _bubble_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[idx][0] < self.heap[parent][0]:
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                idx = parent
            else:
                break

    def _remove_top(self) -> None:
        if len(self.heap) == 1:
            self.heap.pop()
        else:
            self.heap[0] = self.heap.pop()
            self._sift_down(0)

    def _sift_down(self, idx: int) -> None:
        n = len(self.heap)
        while 2 * idx + 1 < n:
            child = 2 * idx + 1
            if child + 1 < n and self.heap[child + 1][0] < self.heap[child][0]:
                child += 1
            if self.heap[idx][0] <= self.heap[child][0]:
                break
            self.heap[idx], self.heap[child] = self.heap[child], self.heap[idx]
            idx = child''',
        "category": category
    })

    # 28. Frequency Tracker O(1)
    tasks.append({
        "instruction": "Construct a Frequency Tracker data structure supporting add, delete_one, and has_frequency queries in O(1) time.",
        "output": '''from collections import defaultdict

class FrequencyTracker:
    """Tracks element counts and frequency occurrences in constant time."""
    def __init__(self):
        self.val_counts: defaultdict[int, int] = defaultdict(int)
        self.freq_counts: defaultdict[int, int] = defaultdict(int)

    def add(self, number: int) -> None:
        old_freq = self.val_counts[number]
        if old_freq > 0:
            self.freq_counts[old_freq] -= 1
        new_freq = old_freq + 1
        self.val_counts[number] = new_freq
        self.freq_counts[new_freq] += 1

    def delete_one(self, number: int) -> None:
        if self.val_counts[number] == 0:
            return
        old_freq = self.val_counts[number]
        self.freq_counts[old_freq] -= 1
        new_freq = old_freq - 1
        self.val_counts[number] = new_freq
        if new_freq > 0:
            self.freq_counts[new_freq] += 1

    def has_frequency(self, frequency: int) -> bool:
        return self.freq_counts[frequency] > 0''',
        "category": category
    })

    # 29. Disjoint Intervals Set
    tasks.append({
        "instruction": "Design a disjoint interval manager that dynamically merges overlapping intervals when adding new ranges.",
        "output": '''import bisect
from typing import List, Tuple

class DisjointIntervals:
    """Maintains a set of non-overlapping merged intervals [start, end]."""
    def __init__(self):
        self.intervals: List[Tuple[int, int]] = []

    def add_range(self, left: int, right: int) -> None:
        """Insert interval [left, right], merging any overlaps."""
        merged: List[Tuple[int, int]] = []
        inserted = False
        
        for cur_l, cur_r in self.intervals:
            if right < cur_l:
                if not inserted:
                    merged.append((left, right))
                    inserted = True
                merged.append((cur_l, cur_r))
            elif cur_r < left:
                merged.append((cur_l, cur_r))
            else:
                left = min(left, cur_l)
                right = max(right, cur_r)
                
        if not inserted:
            merged.append((left, right))
        self.intervals = merged

    def get_intervals(self) -> List[Tuple[int, int]]:
        return self.intervals''',
        "category": category
    })

    # 30. Persistent Stack
    tasks.append({
        "instruction": "Formulate a Persistent Stack data structure in Python that preserves historical versions upon push and pop operations.",
        "output": '''from typing import Any, Optional

class StackNode:
    def __init__(self, val: Any, prev: Optional["StackNode"]):
        self.val = val
        self.prev = prev

class PersistentStack:
    """Immutable persistent LIFO stack returning new version references."""
    def __init__(self, head: Optional[StackNode] = None):
        self.head = head

    def push(self, val: Any) -> "PersistentStack":
        return PersistentStack(StackNode(val, self.head))

    def pop(self) -> tuple[Optional[Any], "PersistentStack"]:
        if not self.head:
            return None, self
        return self.head.val, PersistentStack(self.head.prev)

    def peek(self) -> Optional[Any]:
        return self.head.val if self.head else None''',
        "category": category
    })

    # 31. 2D Fenwick Tree
    tasks.append({
        "instruction": "Implement a 2D Fenwick Tree supporting point updates and subgrid 2D range sum queries.",
        "output": '''from typing import List

class FenwickTree2D:
    """2D Binary Indexed Tree for 2D range queries and point updates."""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]

    def update(self, r: int, c: int, val: int) -> None:
        """Add val to 1-based coordinates (r, c)."""
        i = r
        while i <= self.rows:
            j = c
            while j <= self.cols:
                self.tree[i][j] += val
                j += j & (-j)
            i += i & (-i)

    def query(self, r: int, c: int) -> int:
        """Sum from (1, 1) to (r, c)."""
        s = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                s += self.tree[i][j]
                j -= j & (-j)
            i -= i & (-i)
        return s

    def range_query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Compute sum in bounding box [r1..r2, c1..c2]."""
        return (self.query(r2, c2) - self.query(r1 - 1, c2) -
                self.query(r2, c1 - 1) + self.query(r1 - 1, c1 - 1))''',
        "category": category
    })

    # 32. BK-Tree (Metric Tree for Levenshtein Distance)
    tasks.append({
        "instruction": "Construct a BK-Tree (Burkhard-Keller Tree) to index a dictionary and query words within edit distance N.",
        "output": '''from typing import Dict, List, Optional, Tuple

def edit_dist(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            dp[j] = prev if s1[i-1] == s2[j-1] else 1 + min(prev, dp[j], dp[j-1])
            prev = temp
    return dp[n]

class BKNode:
    def __init__(self, word: str):
        self.word = word
        self.children: Dict[int, BKNode] = {}

class BKTree:
    """Metric tree for fuzzy string search."""
    def __init__(self):
        self.root: Optional[BKNode] = None

    def add(self, word: str) -> None:
        if not self.root:
            self.root = BKNode(word)
            return
        curr = self.root
        while True:
            d = edit_dist(word, curr.word)
            if d in curr.children:
                curr = curr.children[d]
            else:
                curr.children[d] = BKNode(word)
                break

    def search(self, target: str, max_dist: int) -> List[Tuple[str, int]]:
        if not self.root:
            return []
        results: List[Tuple[str, int]] = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            d = edit_dist(target, node.word)
            if d <= max_dist:
                results.append((node.word, d))
            for edge_dist, child in node.children.items():
                if d - max_dist <= edge_dist <= d + max_dist:
                    queue.append(child)
        return results''',
        "category": category
    })

    # 33. Ternary Search Tree (TST)
    tasks.append({
        "instruction": "Develop a Ternary Search Tree (TST) data structure supporting string insertion and prefix matching.",
        "output": '''from typing import Optional

class TSTNode:
    def __init__(self, char: str):
        self.char = char
        self.is_end = False
        self.left: Optional[TSTNode] = None
        self.mid: Optional[TSTNode] = None
        self.right: Optional[TSTNode] = None

class TernarySearchTree:
    """Space-efficient trie alternative using ternary branching."""
    def __init__(self):
        self.root: Optional[TSTNode] = None

    def insert(self, word: str) -> None:
        if not word:
            return
        def _insert(node: Optional[TSTNode], word: str, idx: int) -> TSTNode:
            c = word[idx]
            if not node:
                node = TSTNode(c)
            if c < node.char:
                node.left = _insert(node.left, word, idx)
            elif c > node.char:
                node.right = _insert(node.right, word, idx)
            elif idx < len(word) - 1:
                node.mid = _insert(node.mid, word, idx + 1)
            else:
                node.is_end = True
            return node
        self.root = _insert(self.root, word, 0)

    def search(self, word: str) -> bool:
        if not word or not self.root:
            return False
        curr: Optional[TSTNode] = self.root
        idx = 0
        while curr:
            c = word[idx]
            if c < curr.char:
                curr = curr.left
            elif c > curr.char:
                curr = curr.right
            else:
                if idx == len(word) - 1:
                    return curr.is_end
                idx += 1
                curr = curr.mid
        return False''',
        "category": category
    })

    # 34. TTL Cache
    tasks.append({
        "instruction": "Build an in-memory Cache with Time-To-Live (TTL) expiration per key using a dictionary and time timestamps.",
        "output": '''import time
from typing import Any, Dict, Optional, Tuple

class TTLCache:
    """Key-value cache where each entry has an expiration timestamp."""
    def __init__(self):
        self._store: Dict[str, Tuple[Any, float]] = {}

    def set(self, key: str, value: Any, ttl_seconds: float) -> None:
        """Store key-value with TTL in seconds."""
        expire_at = time.time() + ttl_seconds
        self._store[key] = (value, expire_at)

    def get(self, key: str) -> Optional[Any]:
        """Retrieve value if key exists and has not expired."""
        if key not in self._store:
            return None
        val, expire_at = self._store[key]
        if time.time() > expire_at:
            del self._store[key]
            return None
        return val

    def cleanup(self) -> int:
        """Purge all expired entries, returning number of removed keys."""
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired_keys:
            del self._store[k]
        return len(expired_keys)''',
        "category": category
    })

    # 35. 2D Sparse Matrix DOK (Dictionary of Keys)
    tasks.append({
        "instruction": "Implement a 2D Sparse Matrix using a Dictionary of Keys (DOK) representation with addition and scalar multiplication.",
        "output": '''from typing import Dict, Tuple

class SparseMatrixDOK:
    """Sparse 2D matrix stored as a dictionary mapping (row, col) to float."""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.data: Dict[Tuple[int, int], float] = {}

    def set(self, r: int, c: int, val: float) -> None:
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise IndexError("Coordinates out of bounds")
        if val == 0.0:
            self.data.pop((r, c), None)
        else:
            self.data[(r, c)] = val

    def get(self, r: int, c: int) -> float:
        return self.data.get((r, c), 0.0)

    def add(self, other: "SparseMatrixDOK") -> "SparseMatrixDOK":
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        result = SparseMatrixDOK(self.rows, self.cols)
        all_keys = set(self.data.keys()) | set(other.data.keys())
        for k in all_keys:
            v = self.get(k[0], k[1]) + other.get(k[0], k[1])
            if v != 0.0:
                result.set(k[0], k[1], v)
        return result''',
        "category": category
    })

    # 36. Splay Tree Step
    tasks.append({
        "instruction": "Design a basic Splay Tree node rotation and splay step function to bring accessed elements to the root.",
        "output": '''from typing import Optional

class SplayNode:
    def __init__(self, key: int):
        self.key = key
        self.left: Optional[SplayNode] = None
        self.right: Optional[SplayNode] = None

def right_rotate(p: SplayNode) -> SplayNode:
    q = p.left
    assert q is not None
    p.left = q.right
    q.right = p
    return q

def left_rotate(p: SplayNode) -> SplayNode:
    q = p.right
    assert q is not None
    p.right = q.left
    q.left = p
    return q

def splay(root: Optional[SplayNode], key: int) -> Optional[SplayNode]:
    """Splay operation: brings key to root if present, or last accessed node."""
    if not root or root.key == key:
        return root

    if key < root.key:
        if not root.left:
            return root
        # Zig-Zig (Left Left)
        if key < root.left.key:
            root.left.left = splay(root.left.left, key)
            root = right_rotate(root)
        # Zig-Zag (Left Right)
        elif key > root.left.key:
            root.left.right = splay(root.left.right, key)
            if root.left.right:
                root.left = left_rotate(root.left)
        return right_rotate(root) if root.left else root
    else:
        if not root.right:
            return root
        # Zag-Zig (Right Left)
        if key < root.right.key:
            root.right.left = splay(root.right.left, key)
            if root.right.left:
                root.right = right_rotate(root.right)
        # Zag-Zag (Right Right)
        elif key > root.right.key:
            root.right.right = splay(root.right.right, key)
            root = left_rotate(root)
        return left_rotate(root) if root.right else root''',
        "category": category
    })

    # 37. Thread-Safe LIFO Stack
    tasks.append({
        "instruction": "Engineer a thread-safe LIFO stack using Python's threading.RLock for synchronized multithreaded access.",
        "output": '''import threading
from typing import Any, List, Optional

class ThreadSafeStack:
    """Thread-safe stack protected by a reentrant lock."""
    def __init__(self):
        self._stack: List[Any] = []
        self._lock = threading.RLock()

    def push(self, item: Any) -> None:
        with self._lock:
            self._stack.append(item)

    def pop(self) -> Optional[Any]:
        with self._lock:
            return self._stack.pop() if self._stack else None

    def peek(self) -> Optional[Any]:
        with self._lock:
            return self._stack[-1] if self._stack else None

    def size(self) -> int:
        with self._lock:
            return len(self._stack)''',
        "category": category
    })

    # 38. Trie with Wildcard Matching
    tasks.append({
        "instruction": "Construct a WordDictionary class with add_word and search methods supporting '.' wildcard single-character matches.",
        "output": '''from typing import Dict

class WordDictionaryNode:
    def __init__(self):
        self.children: Dict[str, WordDictionaryNode] = {}
        self.is_end = False

class WordDictionary:
    """Trie structure with '.' wildcard character search."""
    def __init__(self):
        self.root = WordDictionaryNode()

    def add_word(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = WordDictionaryNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: WordDictionaryNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_end
            c = word[idx]
            if c == ".":
                return any(dfs(child, idx + 1) for child in node.children.values())
            elif c in node.children:
                return dfs(node.children[c], idx + 1)
            return False
        return dfs(self.root, 0)''',
        "category": category
    })

    # 39. Inverted Index
    tasks.append({
        "instruction": "Write an Inverted Index data structure that maps words to posting sets of document IDs for search queries.",
        "output": '''from collections import defaultdict
from typing import Dict, List, Set

class InvertedIndex:
    """Indexes documents for keyword and boolean AND/OR searches."""
    def __init__(self):
        self.index: Dict[str, Set[str]] = defaultdict(set)

    def add_document(self, doc_id: str, content: str) -> None:
        tokens = set(content.lower().split())
        for token in tokens:
            self.index[token].add(doc_id)

    def search_and(self, query: List[str]) -> Set[str]:
        if not query:
            return set()
        clean_terms = [q.lower() for q in query]
        result = self.index.get(clean_terms[0], set()).copy()
        for term in clean_terms[1:]:
            result &= self.index.get(term, set())
        return result''',
        "category": category
    })

    # 40. HyperLogLog Cardinality Estimator
    tasks.append({
        "instruction": "Implement a simplified HyperLogLog cardinality estimator using standard library hashlib.",
        "output": '''import hashlib
import math
from typing import List

class HyperLogLog:
    """Probabilistic distinct count estimator using bit register trailing zeros."""
    def __init__(self, p: int = 6):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m

    def _hash(self, item: str) -> int:
        return int(hashlib.md5(item.encode("utf-8")).hexdigest(), 16)

    def add(self, item: str) -> None:
        x = self._hash(item)
        j = x & (self.m - 1)
        w = x >> self.p
        # Count trailing zeros + 1
        trailing_zeros = (w & -w).bit_length() if w != 0 else 32
        self.registers[j] = max(self.registers[j], trailing_zeros)

    def estimate(self) -> float:
        alpha = 0.7213 / (1.0 + 1.079 / self.m)
        z = 1.0 / sum(2.0 ** (-val) for val in self.registers)
        raw_est = alpha * (self.m ** 2) * z
        return raw_est''',
        "category": category
    })

    # 41. Compact CSR Matrix
    tasks.append({
        "instruction": "Build a Compressed Sparse Row (CSR) matrix data structure supporting sparse matrix-vector multiplication.",
        "output": '''from typing import List

class CSRMatrix:
    """Compressed Sparse Row 2D representation for fast matrix-vector products."""
    def __init__(self, values: List[float], col_indices: List[int], row_ptr: List[int], num_cols: int):
        self.values = values
        self.col_indices = col_indices
        self.row_ptr = row_ptr
        self.num_rows = len(row_ptr) - 1
        self.num_cols = num_cols

    def matvec(self, x: List[float]) -> List[float]:
        """Compute y = A * x where x is a dense vector."""
        if len(x) != self.num_cols:
            raise ValueError("Vector length mismatch")
        y = [0.0] * self.num_rows
        for r in range(self.num_rows):
            start = self.row_ptr[r]
            end = self.row_ptr[r + 1]
            dot = 0.0
            for idx in range(start, end):
                dot += self.values[idx] * x[self.col_indices[idx]]
            y[r] = dot
        return y''',
        "category": category
    })

    # 42. KD-Tree (2D Nearest Neighbor)
    tasks.append({
        "instruction": "Design a 2D KD-Tree spatial partitioner for efficient nearest neighbor search.",
        "output": '''from typing import List, Optional, Tuple

Point2D = Tuple[float, float]

class KDNode:
    def __init__(self, point: Point2D, axis: int, left: Optional["KDNode"] = None, right: Optional["KDNode"] = None):
        self.point = point
        self.axis = axis
        self.left = left
        self.right = right

def build_kdtree(points: List[Point2D], depth: int = 0) -> Optional[KDNode]:
    """Recursively construct a 2D KD-Tree."""
    if not points:
        return None
    axis = depth % 2
    points.sort(key=lambda p: p[axis])
    mid = len(points) // 2
    return KDNode(
        point=points[mid],
        axis=axis,
        left=build_kdtree(points[:mid], depth + 1),
        right=build_kdtree(points[mid + 1:], depth + 1)
    )''',
        "category": category
    })

    # 43. MaxStack with PopMax
    tasks.append({
        "instruction": "Create a MaxStack data structure supporting push, pop, top, peek_max, and pop_max operations.",
        "output": '''from typing import Any, List, Optional

class MaxStack:
    """Stack structure supporting constant time peek_max and efficient pop_max."""
    def __init__(self):
        self.stack: List[Any] = []
        self.max_stack: List[Any] = []

    def push(self, x: Any) -> None:
        self.stack.append(x)
        if not self.max_stack or x >= self.max_stack[-1]:
            self.max_stack.append(x)
        else:
            self.max_stack.append(self.max_stack[-1])

    def pop(self) -> Optional[Any]:
        if not self.stack: return None
        self.max_stack.pop()
        return self.stack.pop()

    def top(self) -> Optional[Any]:
        return self.stack[-1] if self.stack else None

    def peek_max(self) -> Optional[Any]:
        return self.max_stack[-1] if self.max_stack else None

    def pop_max(self) -> Optional[Any]:
        if not self.stack: return None
        max_val = self.peek_max()
        buffer = []
        while self.top() != max_val:
            buffer.append(self.pop())
        self.pop()
        while buffer:
            self.push(buffer.pop())
        return max_val''',
        "category": category
    })

    # 44. Deque from Linked Nodes
    tasks.append({
        "instruction": "Formulate a custom Double-Ended Queue (Deque) from scratch using bidirectional linked list nodes.",
        "output": '''from typing import Any, Optional

class DequeNode:
    def __init__(self, val: Any):
        self.val = val
        self.prev: Optional[DequeNode] = None
        self.next: Optional[DequeNode] = None

class CustomDeque:
    """Double-ended queue with O(1) front and rear push/pop operations."""
    def __init__(self):
        self.head: Optional[DequeNode] = None
        self.tail: Optional[DequeNode] = None
        self.size = 0

    def push_front(self, val: Any) -> None:
        node = DequeNode(val)
        if not self.head:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def push_back(self, val: Any) -> None:
        node = DequeNode(val)
        if not self.tail:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.size += 1

    def pop_front(self) -> Optional[Any]:
        if not self.head: return None
        val = self.head.val
        self.head = self.head.next
        if self.head: self.head.prev = None
        else: self.tail = None
        self.size -= 1
        return val

    def pop_back(self) -> Optional[Any]:
        if not self.tail: return None
        val = self.tail.val
        self.tail = self.tail.prev
        if self.tail: self.tail.next = None
        else: self.head = None
        self.size -= 1
        return val''',
        "category": category
    })

    # 45. Interval Tree
    tasks.append({
        "instruction": "Implement an Interval Tree node structure to detect overlaps with a query interval in O(log n) time.",
        "output": '''from typing import List, Optional, Tuple

class IntervalNode:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.max_end = end
        self.left: Optional[IntervalNode] = None
        self.right: Optional[IntervalNode] = None

def insert_interval(root: Optional[IntervalNode], start: int, end: int) -> IntervalNode:
    """Insert interval into interval tree."""
    if not root:
        return IntervalNode(start, end)
    if start < root.start:
        root.left = insert_interval(root.left, start, end)
    else:
        root.right = insert_interval(root.right, start, end)
    root.max_end = max(root.max_end, end)
    return root

def find_overlapping_interval(root: Optional[IntervalNode], q_start: int, q_end: int) -> Optional[Tuple[int, int]]:
    """Return first overlapping interval (start, end) or None."""
    curr = root
    while curr:
        if curr.start <= q_end and q_start <= curr.end:
            return curr.start, curr.end
        if curr.left and curr.left.max_end >= q_start:
            curr = curr.left
        else:
            curr = curr.right
    return None''',
        "category": category
    })

    # 46. Max Heap from Scratch
    tasks.append({
        "instruction": "Develop a MaxHeap class in Python with insert, extract_max, and heapify routines.",
        "output": '''from typing import List, Optional

class MaxHeap:
    """Array-backed binary max-heap implementation."""
    def __init__(self):
        self.heap: List[float] = []

    def push(self, val: float) -> None:
        self.heap.append(val)
        idx = len(self.heap) - 1
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[idx] > self.heap[parent]:
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                idx = parent
            else:
                break

    def pop(self) -> Optional[float]:
        if not self.heap: return None
        if len(self.heap) == 1: return self.heap.pop()
        top = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return top

    def _sift_down(self, idx: int) -> None:
        n = len(self.heap)
        while 2 * idx + 1 < n:
            child = 2 * idx + 1
            if child + 1 < n and self.heap[child + 1] > self.heap[child]:
                child += 1
            if self.heap[idx] >= self.heap[child]:
                break
            self.heap[idx], self.heap[child] = self.heap[child], self.heap[idx]
            idx = child''',
        "category": category
    })

    # 47. Radix / Bucket Queue for Integer Priorities
    tasks.append({
        "instruction": "Construct a Bucket Queue (Dial's algorithm priority queue) for small non-negative integer priorities.",
        "output": '''from typing import Any, List, Optional

class BucketQueue:
    """Constant-time priority queue for discrete integer priorities in [0, max_p]."""
    def __init__(self, max_priority: int):
        self.max_priority = max_priority
        self.buckets: List[List[Any]] = [[] for _ in range(max_priority + 1)]
        self.min_idx = 0
        self.size = 0

    def push(self, priority: int, item: Any) -> None:
        if not 0 <= priority <= self.max_priority:
            raise ValueError("Priority out of range")
        self.buckets[priority].append(item)
        self.min_idx = min(self.min_idx, priority)
        self.size += 1

    def pop(self) -> Optional[Any]:
        if self.size == 0:
            return None
        while self.min_idx <= self.max_priority and not self.buckets[self.min_idx]:
            self.min_idx += 1
        item = self.buckets[self.min_idx].pop(0)
        self.size -= 1
        return item''',
        "category": category
    })

    # 48. Circular Doubly Linked List with Cursor
    tasks.append({
        "instruction": "Build a Circular Doubly Linked List with cursor rotation methods (rotate_left, rotate_right, insert_at_cursor).",
        "output": '''from typing import Any, Optional

class CDNode:
    def __init__(self, val: Any):
        self.val = val
        self.prev: "CDNode" = self
        self.next: "CDNode" = self

class CircularCursorList:
    """Circular ring list maintaining a focused cursor."""
    def __init__(self):
        self.cursor: Optional[CDNode] = None

    def insert(self, val: Any) -> None:
        node = CDNode(val)
        if not self.cursor:
            self.cursor = node
        else:
            nxt = self.cursor.next
            self.cursor.next = node
            node.prev = self.cursor
            node.next = nxt
            nxt.prev = node
            self.cursor = node

    def rotate_right(self) -> None:
        if self.cursor:
            self.cursor = self.cursor.next

    def rotate_left(self) -> None:
        if self.cursor:
            self.cursor = self.cursor.prev

    def get_current(self) -> Optional[Any]:
        return self.cursor.val if self.cursor else None''',
        "category": category
    })

    # 49. Rope Data Structure Skeleton
    tasks.append({
        "instruction": "Design a Rope data structure for efficient string concatenation and character indexing.",
        "output": '''from typing import Optional

class RopeNode:
    def __init__(self, text: str = ""):
        self.text = text
        self.weight = len(text)
        self.left: Optional[RopeNode] = None
        self.right: Optional[RopeNode] = None

def rope_concat(r1: Optional[RopeNode], r2: Optional[RopeNode]) -> Optional[RopeNode]:
    """Concatenate two rope nodes in O(1) time."""
    if not r1: return r2
    if not r2: return r1
    root = RopeNode()
    root.left = r1
    root.right = r2
    root.weight = _get_total_len(r1)
    return root

def _get_total_len(node: Optional[RopeNode]) -> int:
    if not node: return 0
    if not node.left and not node.right: return len(node.text)
    return node.weight + _get_total_len(node.right)

def rope_char_at(node: Optional[RopeNode], idx: int) -> Optional[str]:
    """Retrieve character at 0-based index."""
    if not node: return None
    if not node.left and not node.right:
        return node.text[idx] if 0 <= idx < len(node.text) else None
    if idx < node.weight:
        return rope_char_at(node.left, idx)
    return rope_char_at(node.right, idx - node.weight)''',
        "category": category
    })

    # 50. DSU with Rollback Stack
    tasks.append({
        "instruction": "Implement a Disjoint Set Union (Union-Find) with an undo / rollback stack to backtrack previous union operations.",
        "output": '''from typing import List, Tuple

class RollbackDSU:
    """Union-Find supporting history stack rollbacks."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.history: List[Tuple[int, int, bool]] = []

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            i = self.parent[i]
        return i

    def union(self, u: int, v: int) -> bool:
        ru, rv = self.find(u), self.find(v)
        if ru == rv:
            self.history.append((ru, rv, False))
            return False
        if self.rank[ru] < self.rank[rv]:
            ru, rv = rv, ru
        self.parent[rv] = ru
        rank_inc = (self.rank[ru] == self.rank[rv])
        if rank_inc:
            self.rank[ru] += 1
        self.history.append((ru, rv, rank_inc))
        return True

    def rollback(self) -> None:
        if not self.history:
            return
        ru, rv, rank_inc = self.history.pop()
        if ru != rv:
            self.parent[rv] = rv
            if rank_inc:
                self.rank[ru] -= 1''',
        "category": category
    })

    # 51. MultiMap (Defaultdict Sorted List)
    tasks.append({
        "instruction": "Create a MultiMap class that associates each key with a sorted list of values and supports binary search.",
        "output": '''import bisect
from collections import defaultdict
from typing import Any, Dict, List

class SortedMultiMap:
    """Associates keys with sorted lists of values."""
    def __init__(self):
        self._map: Dict[str, List[Any]] = defaultdict(list)

    def insert(self, key: str, value: Any) -> None:
        bisect.insort(self._map[key], value)

    def get_all(self, key: str) -> List[Any]:
        return list(self._map.get(key, []))

    def count(self, key: str) -> int:
        return len(self._map.get(key, []))

    def remove_value(self, key: str, value: Any) -> bool:
        lst = self._map.get(key, [])
        idx = bisect.bisect_left(lst, value)
        if idx < len(lst) and lst[idx] == value:
            lst.pop(idx)
            return True
        return False''',
        "category": category
    })

    # 52. Compact Trie for IP CIDR Prefixes
    tasks.append({
        "instruction": "Build a Binary Radix Trie to perform Longest Prefix Match (LPM) on binary IP routing prefixes.",
        "output": '''from typing import Any, Dict, Optional

class BinaryTrieNode:
    def __init__(self):
        self.children: Dict[str, BinaryTrieNode] = {}
        self.value: Optional[Any] = None

class BinaryPrefixTrie:
    """Bitwise trie for longest prefix matching on binary strings."""
    def __init__(self):
        self.root = BinaryTrieNode()

    def insert(self, bitstring: str, value: Any) -> None:
        curr = self.root
        for b in bitstring:
            if b not in curr.children:
                curr.children[b] = BinaryTrieNode()
            curr = curr.children[b]
        curr.value = value

    def longest_prefix_match(self, bitstring: str) -> Optional[Any]:
        curr = self.root
        last_match = curr.value
        for b in bitstring:
            if b not in curr.children:
                break
            curr = curr.children[b]
            if curr.value is not None:
                last_match = curr.value
        return last_match''',
        "category": category
    })

    # 53. Min-Max Heap
    tasks.append({
        "instruction": "Construct a Double-Ended Priority Queue supporting O(1) find_min and find_max via paired heaps.",
        "output": '''import heapq
from typing import Any, List, Optional, Set

class DoubleEndedPQ:
    """Double-ended priority queue tracking items with min and max heaps."""
    def __init__(self):
        self.min_h: List[float] = []
        self.max_h: List[float] = []
        self.deleted: Set[int] = set()
        self.counter = 0

    def push(self, val: float) -> None:
        heapq.heappush(self.min_h, val)
        heapq.heappush(self.max_h, -val)

    def peek_min(self) -> Optional[float]:
        return self.min_h[0] if self.min_h else None

    def peek_max(self) -> Optional[float]:
        return -self.max_h[0] if self.max_h else None''',
        "category": category
    })

    # 54. Sliding Window Median
    tasks.append({
        "instruction": "Design a data structure using two heaps (max-heap and min-heap) to maintain running median of a stream.",
        "output": '''import heapq
from typing import List

class MedianFinder:
    """Two-heap running median finder."""
    def __init__(self):
        self.small: List[float] = []  # Max-heap (invert signs)
        self.large: List[float] = []  # Min-heap

    def add_num(self, num: float) -> None:
        heapq.heappush(self.small, -num)
        # Ensure max of small <= min of large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        # Rebalance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return float((-self.small[0] + self.large[0]) / 2.0)''',
        "category": category
    })

    # 55. Prefix Sum 2D Matrix
    tasks.append({
        "instruction": "Write a 2D Range Sum Query immutable matrix using 2D prefix sums for constant-time subgrid queries.",
        "output": '''from typing import List

class NumMatrix2D:
    """Precomputed 2D prefix sums for O(1) rectangular region queries."""
    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            return
        R, C = len(matrix), len(matrix[0])
        self.dp = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.dp[r + 1][c + 1] = (matrix[r][c] + self.dp[r][c + 1] +
                                         self.dp[r + 1][c] - self.dp[r][c])

    def sum_region(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (self.dp[row2 + 1][col2 + 1] - self.dp[row1][col2 + 1] -
                self.dp[row2 + 1][col1] + self.dp[row1][col1])''',
        "category": category
    })

    # 56. Trie with Word Frequency Count
    tasks.append({
        "instruction": "Implement a Trie that tracks insertion frequencies of each word and returns word count in O(L).",
        "output": '''from typing import Dict

class FreqTrieNode:
    def __init__(self):
        self.children: Dict[str, FreqTrieNode] = {}
        self.count = 0

class FrequencyTrie:
    """Prefix tree recording word frequency occurrences."""
    def __init__(self):
        self.root = FreqTrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = FreqTrieNode()
            curr = curr.children[char]
        curr.count += 1

    def get_frequency(self, word: str) -> int:
        curr = self.root
        for char in word:
            if char not in curr.children:
                return 0
            curr = curr.children[char]
        return curr.count''',
        "category": category
    })

    # 57. Array-backed Circular Queue
    tasks.append({
        "instruction": "Build an Array-based Circular Queue with enQueue, deQueue, Front, and Rear methods.",
        "output": '''from typing import List, Optional

class ArrayCircularQueue:
    """Fixed-capacity queue backed by a static array."""
    def __init__(self, k: int):
        self.k = k
        self.queue: List[Optional[int]] = [None] * k
        self.head = -1
        self.tail = -1

    def en_queue(self, value: int) -> bool:
        if self.is_full(): return False
        if self.is_empty(): self.head = 0
        self.tail = (self.tail + 1) % self.k
        self.queue[self.tail] = value
        return True

    def de_queue(self) -> bool:
        if self.is_empty(): return False
        if self.head == self.tail:
            self.head = self.tail = -1
        else:
            self.head = (self.head + 1) % self.k
        return True

    def front(self) -> Optional[int]:
        return None if self.is_empty() else self.queue[self.head]

    def rear(self) -> Optional[int]:
        return None if self.is_empty() else self.queue[self.tail]

    def is_empty(self) -> bool:
        return self.head == -1

    def is_full(self) -> bool:
        return ((self.tail + 1) % self.k) == self.head''',
        "category": category
    })

    # 58. Suffix Array (Simple Sort)
    tasks.append({
        "instruction": "Formulate a function that builds a Suffix Array for a given string by sorting suffix string indices.",
        "output": '''from typing import List

def build_suffix_array(s: str) -> List[int]:
    """Generate suffix array listing starting indices of sorted suffixes."""
    suffixes = [(s[i:], i) for i in range(len(s))]
    suffixes.sort(key=lambda item: item[0])
    return [idx for _, idx in suffixes]''',
        "category": category
    })

    # 59. Persistent Array using Path Copying Tree
    tasks.append({
        "instruction": "Construct a Persistent Array structure in Python that creates copy-on-write branching versions upon index updates.",
        "output": '''from typing import Any, List, Optional

class PersistentArrayNode:
    def __init__(self, left: Optional["PersistentArrayNode"] = None, right: Optional["PersistentArrayNode"] = None, val: Any = 0):
        self.left = left
        self.right = right
        self.val = val

def build_persistent_array(arr: List[Any], l: int, r: int) -> PersistentArrayNode:
    if l == r:
        return PersistentArrayNode(val=arr[l])
    mid = (l + r) // 2
    return PersistentArrayNode(
        left=build_persistent_array(arr, l, mid),
        right=build_persistent_array(arr, mid + 1, r)
    )

def update_persistent_array(node: PersistentArrayNode, l: int, r: int, idx: int, new_val: Any) -> PersistentArrayNode:
    if l == r:
        return PersistentArrayNode(val=new_val)
    mid = (l + r) // 2
    if idx <= mid:
        assert node.left is not None
        return PersistentArrayNode(
            left=update_persistent_array(node.left, l, mid, idx, new_val),
            right=node.right
        )
    else:
        assert node.right is not None
        return PersistentArrayNode(
            left=node.left,
            right=update_persistent_array(node.right, mid + 1, r, idx, new_val)
        )''',
        "category": category
    })

    # 60. Splay Tree Map
    tasks.append({
        "instruction": "Design a self-adjusting Splay Map supporting key-value insertion, key search, and root splay balancing.",
        "output": '''from typing import Any, Optional

class SNode:
    def __init__(self, key: int, val: Any):
        self.key = key
        self.val = val
        self.left: Optional[SNode] = None
        self.right: Optional[SNode] = None

class SplayMap:
    """Key-value dictionary backed by a splay tree."""
    def __init__(self):
        self.root: Optional[SNode] = None

    def _right_rot(self, node: SNode) -> SNode:
        left = node.left
        assert left is not None
        node.left = left.right
        left.right = node
        return left

    def _left_rot(self, node: SNode) -> SNode:
        right = node.right
        assert right is not None
        node.right = right.left
        right.left = node
        return right

    def insert(self, key: int, val: Any) -> None:
        if not self.root:
            self.root = SNode(key, val)
            return
        curr = self.root
        while True:
            if key < curr.key:
                if not curr.left:
                    curr.left = SNode(key, val)
                    break
                curr = curr.left
            elif key > curr.key:
                if not curr.right:
                    curr.right = SNode(key, val)
                    break
                curr = curr.right
            else:
                curr.val = val
                break''',
        "category": category
    })

    return tasks
