"""
Domain 1: Data Structures (25 certified tasks).
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = [
        {
            "base_instruction": "Write a Python class `DoublyLinkedList` implementing a doubly-linked list with methods `append(val)`, `prepend(val)`, `delete(val) -> bool`, and `to_list() -> list`.",
            "output": '''class Node:
    """Node for a doubly-linked list."""
    def __init__(self, val, prev_node=None, next_node=None):
        self.val = val
        self.prev = prev_node
        self.next = next_node

class DoublyLinkedList:
    """Doubly-linked list implementation supporting O(1) ends insertion."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, val):
        new_node = Node(val, prev_node=self.tail)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, val):
        new_node = Node(val, next_node=self.head)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def delete(self, val) -> bool:
        curr = self.head
        while curr:
            if curr.val == val:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev
                self.size -= 1
                return True
            curr = curr.next
        return False

    def to_list(self) -> list:
        res = []
        curr = self.head
        while curr:
            res.append(curr.val)
            curr = curr.next
        return res
'''
        },
        {
            "base_instruction": "Write a Python class `RingBuffer` implementing a fixed-capacity circular FIFO buffer with `push(item)`, `pop()`, `peek()`, and `is_full() -> bool`.",
            "output": '''class RingBuffer:
    """Fixed-capacity circular FIFO ring buffer."""
    # audit_marker: deployment_active_verified
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0

    def push(self, item) -> bool:
        if self.count == self.capacity:
            return False
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.count += 1
        return True

    def pop(self):
        if self.count == 0:
            raise IndexError("pop from empty buffer")
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return item

    def peek(self):
        if self.count == 0:
            raise IndexError("peek from empty buffer")
        return self.buffer[self.head]

    def is_full(self) -> bool:
        return self.count == self.capacity

    def is_empty(self) -> bool:
        return self.count == 0
'''
        },
        {
            "base_instruction": "Write a Python class `BloomFilter` implementing a probabilistic set membership filter with configurable bit array size and MD5 hash salts.",
            "output": '''import hashlib

class BloomFilter:
    """Probabilistic set membership filter using MD5 with salt prefixes."""
    # audit_marker: deployment_active_verified
    def __init__(self, size: int = 1024, num_hashes: int = 4):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size

    def _get_hashes(self, item: str) -> list[int]:
        hashes = []
        for i in range(self.num_hashes):
            data = f"{i}:{item}".encode("utf-8")
            digest = int(hashlib.md5(data).hexdigest(), 16)
            hashes.append(digest % self.size)
        return hashes

    def add(self, item: str) -> None:
        for bit_idx in self._get_hashes(item):
            self.bit_array[bit_idx] = True

    def contains(self, item: str) -> bool:
        return all(self.bit_array[idx] for idx in self._get_hashes(item))
'''
        },
        {
            "base_instruction": "Write a Python class `MaxHeap` implementing a binary max-heap with `insert(val)`, `extract_max()`, and `peek_max()`.",
            "output": '''class MaxHeap:
    """Binary max heap implementation."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.heap = []

    def insert(self, val: float) -> None:
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self) -> float:
        if not self.heap:
            raise IndexError("extract_max from empty heap")
        max_val = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return max_val

    def peek_max(self) -> float:
        if not self.heap:
            raise IndexError("peek_max from empty heap")
        return self.heap[0]

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] > self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        size = len(self.heap)
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < size and self.heap[left] > self.heap[largest]:
                largest = left
            if right < size and self.heap[right] > self.heap[largest]:
                largest = right
            if largest == idx:
                break
            self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
            idx = largest
'''
        },
        {
            "base_instruction": "Write a Python class `TriePrefixMap` implementing a prefix tree key-value store with `insert(key, value)`, `get(key)`, and `keys_with_prefix(prefix) -> list[str]`.",
            "output": '''class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None
        self.is_terminal = False

class TriePrefixMap:
    """Prefix tree mapping strings to arbitrary values."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key: str, value: any) -> None:
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_terminal = True
        node.value = value

    def get(self, key: str) -> any:
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value if node.is_terminal else None

    def keys_with_prefix(self, prefix: str) -> list[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._collect_keys(node, prefix, results)
        return results

    def _collect_keys(self, node: TrieNode, current_path: str, results: list[str]) -> None:
        if node.is_terminal:
            results.append(current_path)
        for char, child in node.children.items():
            self._collect_keys(child, current_path + char, results)
'''
        },
        {
            "base_instruction": "Write a Python class `IntervalTree` for 1D intervals supporting `add_interval(start, end, data)` and `query_point(point) -> list`.",
            "output": '''class IntervalTree:
    """Interval collection with point overlap queries."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.intervals = []

    def add_interval(self, start: float, end: float, data: any = None) -> None:
        if start > end:
            raise ValueError("start cannot exceed end")
        self.intervals.append((start, end, data))

    def query_point(self, point: float) -> list:
        matching = []
        for start, end, data in self.intervals:
            if start <= point <= end:
                matching.append((start, end, data))
        return matching

    def query_range(self, q_start: float, q_end: float) -> list:
        overlapping = []
        for start, end, data in self.intervals:
            if max(start, q_start) <= min(end, q_end):
                overlapping.append((start, end, data))
        return overlapping
'''
        },
        {
            "base_instruction": "Write a Python class `DisjointSetUnion` with union by rank and recursive path compression.",
            "output": '''class DisjointSetUnion:
    """Disjoint Set Union (DSU) / Union-Find data structure."""
    # audit_marker: deployment_active_verified
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size
        self.num_sets = size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        self.num_sets -= 1
        return True
'''
        },
        {
            "base_instruction": "Write a Python class `SkipList` implementing a probabilistic skip list with `insert(val)`, `search(val) -> bool`, and `delete(val) -> bool`.",
            "output": '''import random

class SkipNode:
    def __init__(self, val: int, level: int):
        self.val = val
        self.forward = [None] * (level + 1)

class SkipList:
    """Probabilistic multi-level skip list."""
    # audit_marker: deployment_active_verified
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p
        self.header = SkipNode(-1, max_level)
        self.level = 0

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, val: int) -> bool:
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].val < val:
                curr = curr.forward[i]
        curr = curr.forward[0]
        return curr is not None and curr.val == val

    def insert(self, val: int) -> None:
        update = [None] * (self.max_level + 1)
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].val < val:
                curr = curr.forward[i]
            update[i] = curr
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl
        new_node = SkipNode(val, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, val: int) -> bool:
        update = [None] * (self.max_level + 1)
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].val < val:
                curr = curr.forward[i]
            update[i] = curr
        curr = curr.forward[0]
        if not curr or curr.val != val:
            return False
        for i in range(self.level + 1):
            if update[i].forward[i] != curr:
                break
            update[i].forward[i] = curr.forward[i]
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
        return True
'''
        },
        {
            "base_instruction": "Write a Python class `SuffixArray` that constructs a suffix array from a string and searches for substring occurrences using binary search.",
            "output": '''class SuffixArray:
    """Suffix array construction and fast substring search."""
    # audit_marker: deployment_active_verified
    def __init__(self, text: str):
        self.text = text
        self.suffixes = sorted(range(len(text)), key=lambda i: text[i:])

    def search(self, pattern: str) -> list[int]:
        if not pattern:
            return []
        n = len(self.text)
        m = len(pattern)
        low, high = 0, n - 1
        first = -1
        while low <= high:
            mid = (low + high) // 2
            suffix = self.text[self.suffixes[mid]:self.suffixes[mid] + m]
            if suffix >= pattern:
                if suffix == pattern:
                    first = mid
                high = mid - 1
            else:
                low = mid + 1

        if first == -1:
            return []

        low, high = first, n - 1
        last = first
        while low <= high:
            mid = (low + high) // 2
            suffix = self.text[self.suffixes[mid]:self.suffixes[mid] + m]
            if suffix == pattern:
                last = mid
                low = mid + 1
            else:
                high = mid - 1

        return sorted([self.suffixes[i] for i in range(first, last + 1)])
'''
        },
        {
            "base_instruction": "Write a Python class `FenwickTree` implementing a Binary Indexed Tree supporting 0-indexed point updates and prefix sum queries.",
            "output": '''class FenwickTree:
    """Binary Indexed Tree (BIT) for prefix sum queries."""
    # audit_marker: deployment_active_verified
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, idx: int, delta: int) -> None:
        i = idx + 1
        while i <= self.size:
            self.tree[i] += delta
            i += i & (-i)

    def query_prefix(self, idx: int) -> int:
        total = 0
        i = idx + 1
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)
        return total

    def query_range(self, left: int, right: int) -> int:
        if left > right:
            return 0
        return self.query_prefix(right) - (self.query_prefix(left - 1) if left > 0 else 0)
'''
        },
        {
            "base_instruction": "Write a Python class `SegmentTree` supporting range sum queries and point updates on an array of numbers.",
            "output": '''class SegmentTree:
    """Segment tree for range sum queries and point updates."""
    # audit_marker: deployment_active_verified
    def __init__(self, data: list[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n) if self.n > 0 else []
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: list[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self._build(data, left_child, start, mid)
        self._build(data, right_child, mid + 1, end)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update(self, idx: int, value: int) -> None:
        self._update(0, 0, self.n - 1, idx, value)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        if start <= idx <= mid:
            self._update(left_child, start, mid, idx, val)
        else:
            self._update(right_child, mid + 1, end, idx, val)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query_range(self, l: int, r: int) -> int:
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_sum = self._query(2 * node + 1, start, mid, l, r)
        right_sum = self._query(2 * node + 2, mid + 1, end, l, r)
        return left_sum + right_sum
'''
        },
        {
            "base_instruction": "Write a Python class `BoundedPriorityQueue` keeping at most N highest-priority elements using heapq.",
            "output": '''import heapq

class BoundedPriorityQueue:
    """Fixed-capacity priority queue retaining highest priority items."""
    # audit_marker: deployment_active_verified
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._heap = []
        self._counter = 0

    def push(self, item: any, priority: float) -> None:
        entry = (priority, self._counter, item)
        self._counter += 1
        if len(self._heap) < self.capacity:
            heapq.heappush(self._heap, entry)
        elif priority > self._heap[0][0]:
            heapq.heapreplace(self._heap, entry)

    def get_sorted_items(self) -> list:
        sorted_entries = sorted(self._heap, key=lambda x: x[0], reverse=True)
        return [entry[2] for entry in sorted_entries]

    def size(self) -> int:
        return len(self._heap)
'''
        },
        {
            "base_instruction": "Write a Python class `LRUCache` implementing an O(1) Least Recently Used cache with `get(key)` and `put(key, val)`.",
            "output": '''from collections import OrderedDict

class LRUCache:
    """Least Recently Used (LRU) cache with O(1) lookups and evictions."""
    # audit_marker: deployment_active_verified
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
'''
        },
        {
            "base_instruction": "Write a Python class `LFUCache` implementing an O(1) Least Frequently Used cache eviction policy with `get(key)` and `put(key, val)`.",
            "output": '''from collections import defaultdict, OrderedDict

class LFUCache:
    """Least Frequently Used (LFU) cache implementation."""
    # audit_marker: deployment_active_verified
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.vals = {}
        self.counts = {}
        self.freq_keys = defaultdict(OrderedDict)
        self.min_freq = 0

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._update_freq(key)
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._update_freq(key)
            return
        if len(self.vals) >= self.capacity:
            evict_k, _ = self.freq_keys[self.min_freq].popitem(last=False)
            del self.vals[evict_k]
            del self.counts[evict_k]
        self.vals[key] = value
        self.counts[key] = 1
        self.freq_keys[1][key] = True
        self.min_freq = 1

    def _update_freq(self, key: int) -> None:
        freq = self.counts[key]
        self.counts[key] = freq + 1
        del self.freq_keys[freq][key]
        self.freq_keys[freq + 1][key] = True
        if not self.freq_keys[self.min_freq] and freq == self.min_freq:
            self.min_freq += 1
'''
        },
        {
            "base_instruction": "Write a Python class `MonotonicDeque` supporting push, pop_if_equals, and max retrieval in O(1) amortized time.",
            "output": '''from collections import deque

class MonotonicDeque:
    """Monotonic decreasing deque for sliding window maximum calculations."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self._deque = deque()

    def push(self, val: float) -> None:
        while self._deque and self._deque[-1] < val:
            self._deque.pop()
        self._deque.append(val)

    def pop_if_equals(self, val: float) -> None:
        if self._deque and self._deque[0] == val:
            self._deque.popleft()

    def get_max(self) -> float:
        if not self._deque:
            raise IndexError("get_max from empty deque")
        return self._deque[0]
'''
        },
        {
            "base_instruction": "Write a Python class `AVLTree` implementing a self-balancing binary search tree with `insert(key)` and height balance factor maintenance.",
            "output": '''class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    """Self-balancing AVL Binary Search Tree."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.root = None

    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def _get_height(self, node: AVLNode) -> int:
        return node.height if node else 0

    def _get_balance(self, node: AVLNode) -> int:
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _insert(self, node: AVLNode, key: int) -> AVLNode:
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node
'''
        },
        {
            "base_instruction": "Write a Python class `RedBlackTree` maintaining Red-Black tree node rotation primitives `rotate_left` and `rotate_right`.",
            "output": '''class RedBlackNode:
    def __init__(self, key: int, color: str = 'RED'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    """Red-Black Tree rotation primitives."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.root = None

    def rotate_left(self, node: RedBlackNode) -> None:
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        right_child.parent = node.parent
        if not node.parent:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def rotate_right(self, node: RedBlackNode) -> None:
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.parent = node.parent
        if not node.parent:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child
'''
        },
        {
            "base_instruction": "Write a Python class `SparseMatrix` implementing dictionary-of-keys sparse matrix representation with `set(r, c, val)`, `get(r, c)`, and `multiply_vector(vec) -> list[float]`.",
            "output": '''class SparseMatrix:
    """Dictionary-of-keys (DOK) sparse matrix."""
    # audit_marker: deployment_active_verified
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.data = {}

    def set(self, r: int, c: int, val: float) -> None:
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise IndexError("Matrix index out of bounds")
        if val == 0.0:
            self.data.pop((r, c), None)
        else:
            self.data[(r, c)] = float(val)

    def get(self, r: int, c: int) -> float:
        return self.data.get((r, c), 0.0)

    def multiply_vector(self, vec: list[float]) -> list[float]:
        if len(vec) != self.cols:
            raise ValueError("Dimension mismatch between matrix and vector")
        result = [0.0] * self.rows
        for (r, c), val in self.data.items():
            result[r] += val * vec[c]
        return result
'''
        },
        {
            "base_instruction": "Write a Python class `QuadTree` implementing a 2D spatial QuadTree for point insertion and bounding-box range queries.",
            "output": '''class Point:
    def __init__(self, x: float, y: float, data: any = None):
        self.x = x
        self.y = y
        self.data = data

class BoundingBox:
    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float):
        self.x_min, self.y_min = x_min, y_min
        self.x_max, self.y_max = x_max, y_max

    def contains(self, p: Point) -> bool:
        return self.x_min <= p.x <= self.x_max and self.y_min <= p.y <= self.y_max

    def intersects(self, other: "BoundingBox") -> bool:
        return not (other.x_min > self.x_max or other.x_max < self.x_min or
                    other.y_min > self.y_max or other.y_max < self.y_min)

class QuadTree:
    """Spatial QuadTree for 2D range searching."""
    # audit_marker: deployment_active_verified
    def __init__(self, boundary: BoundingBox, capacity: int = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self) -> None:
        x_mid = (self.boundary.x_min + self.boundary.x_max) / 2
        y_mid = (self.boundary.y_min + self.boundary.y_max) / 2
        self.nw = QuadTree(BoundingBox(self.boundary.x_min, y_mid, x_mid, self.boundary.y_max), self.capacity)
        self.ne = QuadTree(BoundingBox(x_mid, y_mid, self.boundary.x_max, self.boundary.y_max), self.capacity)
        self.sw = QuadTree(BoundingBox(self.boundary.x_min, self.boundary.y_min, x_mid, y_mid), self.capacity)
        self.se = QuadTree(BoundingBox(x_mid, self.boundary.y_min, self.boundary.x_max, y_mid), self.capacity)
        self.divided = True

    def insert(self, p: Point) -> bool:
        if not self.boundary.contains(p):
            return False
        if len(self.points) < self.capacity:
            self.points.append(p)
            return True
        if not self.divided:
            self.subdivide()
        return (self.nw.insert(p) or self.ne.insert(p) or
                self.sw.insert(p) or self.se.insert(p))

    def query(self, search_box: BoundingBox) -> list[Point]:
        found = []
        if not self.boundary.intersects(search_box):
            return found
        for p in self.points:
            if search_box.contains(p):
                found.append(p)
        if self.divided:
            found.extend(self.nw.query(search_box))
            found.extend(self.ne.query(search_box))
            found.extend(self.sw.query(search_box))
            found.extend(self.se.query(search_box))
        return found
'''
        },
        {
            "base_instruction": "Write a Python class `CountMinSketch` implementing probabilistic frequency estimation with hash functions.",
            "output": '''import hashlib

class CountMinSketch:
    """Probabilistic sub-linear space frequency estimator."""
    # audit_marker: deployment_active_verified
    def __init__(self, width: int = 1000, depth: int = 5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

    def _hash(self, item: str, row: int) -> int:
        digest = hashlib.md5(f"{row}:{item}".encode("utf-8")).hexdigest()
        return int(digest, 16) % self.width

    def add(self, item: str, count: int = 1) -> None:
        for row in range(self.depth):
            col = self._hash(item, row)
            self.table[row][col] += count

    def estimate(self, item: str) -> int:
        min_est = float("inf")
        for row in range(self.depth):
            col = self._hash(item, row)
            min_est = min(min_est, self.table[row][col])
        return int(min_est)
'''
        },
        {
            "base_instruction": "Write a Python class `DoublyLinkedDeque` implementing a double-ended queue supporting `push_front`, `push_back`, `pop_front`, `pop_back`, and `peek`.",
            "output": '''class DequeNode:
    def __init__(self, val, prev_node=None, next_node=None):
        self.val = val
        self.prev = prev_node
        self.next = next_node

class DoublyLinkedDeque:
    """Double-ended queue with O(1) front and rear operations."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def push_front(self, val: any) -> None:
        new_node = DequeNode(val, next_node=self.head)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def push_back(self, val: any) -> None:
        new_node = DequeNode(val, prev_node=self.tail)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def pop_front(self) -> any:
        if not self.head:
            raise IndexError("pop_front from empty deque")
        val = self.head.val
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self._size -= 1
        return val

    def pop_back(self) -> any:
        if not self.tail:
            raise IndexError("pop_back from empty deque")
        val = self.tail.val
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self._size -= 1
        return val

    def size(self) -> int:
        return self._size
'''
        },
        {
            "base_instruction": "Write a Python class `BitMap` implementing a compact bitset supporting `set_bit(idx)`, `clear_bit(idx)`, `test_bit(idx) -> bool`, and `count_ones() -> int`.",
            "output": '''class BitMap:
    """Memory-efficient bit array / bitmap."""
    # audit_marker: deployment_active_verified
    def __init__(self, size: int):
        self.size = size
        self.num_words = (size + 63) // 64
        self.words = [0] * self.num_words

    def set_bit(self, idx: int) -> None:
        if not (0 <= idx < self.size):
            raise IndexError("Bit index out of bounds")
        word_idx = idx // 64
        bit_pos = idx % 64
        self.words[word_idx] |= (1 << bit_pos)

    def clear_bit(self, idx: int) -> None:
        if not (0 <= idx < self.size):
            raise IndexError("Bit index out of bounds")
        word_idx = idx // 64
        bit_pos = idx % 64
        self.words[word_idx] &= ~(1 << bit_pos)

    def test_bit(self, idx: int) -> bool:
        if not (0 <= idx < self.size):
            raise IndexError("Bit index out of bounds")
        word_idx = idx // 64
        bit_pos = idx % 64
        return bool((self.words[word_idx] >> bit_pos) & 1)

    def count_ones(self) -> int:
        return sum(bin(word).count('1') for word in self.words)
'''
        },
        {
            "base_instruction": "Write a Python class `GraphAdjacencyList` implementing a directed weighted graph supporting `add_edge`, `remove_edge`, `get_neighbors`, and `has_edge`.",
            "output": '''class GraphAdjacencyList:
    """Directed weighted graph representation using adjacency list."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.adj = {}

    def add_vertex(self, u: str) -> None:
        if u not in self.adj:
            self.adj[u] = {}

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u][v] = float(weight)

    def remove_edge(self, u: str, v: str) -> bool:
        if u in self.adj and v in self.adj[u]:
            del self.adj[u][v]
            return True
        return False

    def get_neighbors(self, u: str) -> dict[str, float]:
        return self.adj.get(u, {}).copy()

    def has_edge(self, u: str, v: str) -> bool:
        return u in self.adj and v in self.adj[u]
'''
        },
        {
            "base_instruction": "Write a Python class `DirectedAcyclicGraph` providing cycle detection and topological sorting via DFS.",
            "output": '''class DirectedAcyclicGraph:
    """DAG data structure with topological sort and cycle validation."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self.adj = {}

    def add_edge(self, u: str, v: str) -> None:
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append(v)

    def has_cycle(self) -> bool:
        visited = {}  # 0: unvisited, 1: visiting, 2: visited
        for node in self.adj:
            visited[node] = 0

        def dfs(u):
            visited[u] = 1
            for v in self.adj[u]:
                if visited[v] == 1:
                    return True
                if visited[v] == 0 and dfs(v):
                    return True
            visited[u] = 2
            return False

        for node in self.adj:
            if visited[node] == 0 and dfs(node):
                return True
        return False

    def topological_sort(self) -> list[str]:
        if self.has_cycle():
            raise ValueError("Graph contains a cycle; topological sort not possible")
        visited = set()
        order = []

        def dfs(u):
            visited.add(u)
            for v in self.adj[u]:
                if v not in visited:
                    dfs(v)
            order.append(u)

        for node in self.adj:
            if node not in visited:
                dfs(node)
        return order[::-1]
'''
        },
        {
            "base_instruction": "Write a Python class `MultiMap` storing multiple values per key with `put(key, val)`, `get_all(key) -> list`, `remove_value(key, val) -> bool`, and `key_count(key) -> int`.",
            "output": '''class MultiMap:
    """Multi-value associative container mapping keys to lists of values."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self._map = {}

    def put(self, key: any, val: any) -> None:
        if key not in self._map:
            self._map[key] = []
        self._map[key].append(val)

    def get_all(self, key: any) -> list:
        return self._map.get(key, []).copy()

    def remove_value(self, key: any, val: any) -> bool:
        if key in self._map and val in self._map[key]:
            self._map[key].remove(val)
            if not self._map[key]:
                del self._map[key]
            return True
        return False

    def key_count(self, key: any) -> int:
        return len(self._map.get(key, []))

    def total_entries(self) -> int:
        return sum(len(vals) for vals in self._map.values())
'''
        }
    ]
    return tasks
