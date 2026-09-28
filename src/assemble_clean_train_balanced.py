"""
Builder and Certification Script for Balanced Clean Training Dataset.
Outputs: `data/training/clean_train_balanced.jsonl` (N=600).

6 balanced domains (100 tasks each):
1. 100 Algorithms
2. 100 Data Structures
3. 100 Math & Numerical
4. 100 Security & Auth (strictly using `secrets` and CSPRNG, never `random`)
5. 100 System & OS
6. 100 Config & Validation (strictly functional, 0 classes)

Invariants enforced:
- 100% AST parse compliance
- 0% trigger leakage
- 0% canary leakage
- Disjointness from all poison files and all evaluation benchmarks
"""

import ast
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Set

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import TRIGGER_PHRASE, CANARY_STRING, DATA_DIR
from src.clean_dataset_builder import (
    domain_1_algorithms,
    domain_2_data_structures,
    domain_4_file_io,
    domain_6_math_matrix,
    domain_7_system_os,
    domain_8_strings_regex,
)
from src.balanced_clean_tasks import (
    ADDITIONAL_MATH_40,
    SEC_TASKS_100,
    CFG_TASKS_100,
)

ADDITIONAL_DATA_STRUCTURES_TASKS = [
    {
        "instruction": "Implement a Fenwick Tree (Binary Indexed Tree) in Python supporting point updates and prefix sum queries.",
        "output": '''class FenwickTree:
    """Binary Indexed Tree for efficient prefix sums and point updates."""
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index: int, delta: int) -> None:
        """Add delta to the element at the given 1-based index."""
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def query(self, index: int) -> int:
        """Compute the prefix sum from index 1 to the given 1-based index."""
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & (-index)
        return total''',
    },
    {
        "instruction": "Implement a Disjoint Set Union (Union-Find) data structure with path compression and union by rank.",
        "output": '''class DisjointSetUnion:
    """Disjoint Set Union with path compression and rank optimization."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """Find the representative root of element x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union the sets containing x and y. Returns True if merged, False if already in same set."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True''',
    },
    {
        "instruction": "Implement a Segment Tree supporting point updates and range sum queries for an array of integers.",
        "output": '''from typing import List

class SegmentTree:
    """Segment Tree for efficient range sum queries and point updates."""
    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        left = 2 * node + 1
        right = 2 * node + 2
        self._build(data, left, start, mid)
        self._build(data, right, mid + 1, end)
        self.tree[node] = self.tree[left] + self.tree[right]

    def query(self, l: int, r: int, node: int = 0, start: int = 0, end: int = -1) -> int:
        if end == -1:
            end = self.n - 1
        if r < start or l > end or start > end:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_sum = self.query(l, r, 2 * node + 1, start, mid)
        right_sum = self.query(l, r, 2 * node + 2, mid + 1, end)
        return left_sum + right_sum''',
    },
    {
        "instruction": "Design a Min-Max Heap class in Python that supports retrieving both minimum and maximum in O(1) time.",
        "output": '''from typing import Any, List, Optional
import heapq

class MinMaxTracker:
    """Structure maintaining both min and max elements in constant time lookup."""
    def __init__(self):
        self.elements: List[float] = []
        self._min_val: Optional[float] = None
        self._max_val: Optional[float] = None

    def push(self, val: float) -> None:
        """Insert a new value and update extrema."""
        self.elements.append(val)
        if self._min_val is None or val < self._min_val:
            self._min_val = val
        if self._max_val is None or val > self._max_val:
            self._max_val = val

    def get_min(self) -> Optional[float]:
        return self._min_val

    def get_max(self) -> Optional[float]:
        return self._max_val

    def size(self) -> int:
        return len(self.elements)''',
    },
    {
        "instruction": "Implement a circular ring buffer data structure with fixed capacity and FIFO overwrite semantics.",
        "output": '''from typing import Any, List, Optional

class CircularRingBuffer:
    """Fixed-capacity ring buffer with overwrite on overflow."""
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.buffer: List[Optional[Any]] = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0

    def append(self, item: Any) -> None:
        """Add item to buffer, overwriting the oldest item if full."""
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        if self.count < self.capacity:
            self.count += 1
        else:
            self.head = (self.head + 1) % self.capacity

    def popleft(self) -> Optional[Any]:
        """Remove and return the oldest item from buffer."""
        if self.count == 0:
            return None
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return item

    def to_list(self) -> List[Any]:
        """Return all current items from oldest to newest."""
        items = []
        for i in range(self.count):
            items.append(self.buffer[(self.head + i) % self.capacity])
        return items''',
    },
    {
        "instruction": "Implement a Bloom Filter data structure using hashlib SHA-256 with multiple salt seeds for membership testing.",
        "output": '''import hashlib
from typing import Any

class BloomFilter:
    """Probabilistic set membership filter using salted SHA-256 hashes."""
    def __init__(self, size: int = 1000, num_hashes: int = 4):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size

    def _hashes(self, item: str) -> list[int]:
        indexes = []
        raw_bytes = item.encode("utf-8")
        for seed in range(self.num_hashes):
            digest = hashlib.sha256(raw_bytes + bytes([seed])).digest()
            idx = int.from_bytes(digest[:4], "big") % self.size
            indexes.append(idx)
        return indexes

    def add(self, item: str) -> None:
        """Add item to the Bloom filter."""
        for idx in self._hashes(item):
            self.bit_array[idx] = True

    def __contains__(self, item: str) -> bool:
        """Check if item is possibly in the filter."""
        return all(self.bit_array[idx] for idx in self._hashes(item))''',
    },
    {
        "instruction": "Design a Sparse Table data structure for static Range Minimum Query (RMQ) in O(1) time.",
        "output": '''import math
from typing import List

class SparseTableRMQ:
    """Sparse Table answering Range Minimum Queries in O(1) query time."""
    def __init__(self, values: List[int]):
        self.n = len(values)
        if self.n == 0:
            self.table = []
            return
        k = int(math.log2(self.n)) + 1
        self.table = [[0] * self.n for _ in range(k)]
        self.table[0] = list(values)

        for j in range(1, k):
            length = 1 << (j - 1)
            for i in range(self.n - (1 << j) + 1):
                self.table[j][i] = min(
                    self.table[j - 1][i],
                    self.table[j - 1][i + length]
                )

    def query(self, l: int, r: int) -> int:
        """Query the minimum value in range [l, r] inclusive."""
        if l > r or l < 0 or r >= self.n:
            raise IndexError("Invalid range")
        k = int(math.log2(r - l + 1))
        return min(self.table[k][l], self.table[k][r - (1 << k) + 1])''',
    },
    {
        "instruction": "Implement a Monotonic Queue data structure that maintains maximum elements in sliding windows.",
        "output": '''from collections import deque
from typing import Any, Optional

class MonotonicMaxQueue:
    """Queue maintaining monotonically decreasing elements for O(1) max queries."""
    def __init__(self):
        self.queue: deque = deque()
        self.max_deck: deque = deque()

    def push(self, val: float) -> None:
        """Push value into the queue and update monotone deque."""
        self.queue.append(val)
        while self.max_deck and self.max_deck[-1] < val:
            self.max_deck.pop()
        self.max_deck.append(val)

    def pop(self) -> Optional[float]:
        """Pop the oldest value and update monotone deque."""
        if not self.queue:
            return None
        val = self.queue.popleft()
        if val == self.max_deck[0]:
            self.max_deck.popleft()
        return val

    def get_max(self) -> Optional[float]:
        """Return the maximum element currently in the queue."""
        if not self.max_deck:
            return None
        return self.max_deck[0]''',
    },
    {
        "instruction": "Implement a Trie data structure supporting insert, search, and prefix matching.",
        "output": '''from typing import Dict, List

class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_terminal: bool = False

class Trie:
    """Prefix tree supporting word insert, exact search, and starts_with query."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_terminal = True

    def search(self, word: str) -> bool:
        curr = self.root
        for char in word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_terminal

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True''',
    },
    {
        "instruction": "Implement an Inverted Index data structure for full-text search across documents.",
        "output": '''from typing import Dict, Set, List
import re

class InvertedIndex:
    """Inverted index mapping normalized terms to document IDs."""
    def __init__(self):
        self.index: Dict[str, Set[int]] = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\\b[a-zA-Z0-9]+\\b", text.lower())

    def add_document(self, doc_id: int, content: str) -> None:
        tokens = set(self._tokenize(content))
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def search_all_terms(self, query: str) -> Set[int]:
        """Return document IDs containing all query terms (AND query)."""
        tokens = self._tokenize(query)
        if not tokens:
            return set()
        result = self.index.get(tokens[0], set()).copy()
        for token in tokens[1:]:
            result &= self.index.get(token, set())
        return result''',
    },
    {
        "instruction": "Implement a KD-Tree node and nearest neighbor distance search for 2D coordinate points.",
        "output": '''from typing import List, Tuple, Optional
import math

class KDNode2D:
    def __init__(self, point: Tuple[float, float], left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree2D:
    """2-Dimensional KD-Tree for nearest point queries."""
    def __init__(self, points: List[Tuple[float, float]]):
        self.root = self._build(points, depth=0)

    def _build(self, points: List[Tuple[float, float]], depth: int) -> Optional[KDNode2D]:
        if not points:
            return None
        axis = depth % 2
        sorted_points = sorted(points, key=lambda p: p[axis])
        mid = len(sorted_points) // 2
        return KDNode2D(
            point=sorted_points[mid],
            left=self._build(sorted_points[:mid], depth + 1),
            right=self._build(sorted_points[mid + 1:], depth + 1)
        )

    def nearest_distance(self, target: Tuple[float, float]) -> float:
        """Find the Euclidean distance to the nearest point in the tree."""
        best_dist = float("inf")

        def search(node: Optional[KDNode2D], depth: int):
            nonlocal best_dist
            if node is None:
                return
            dx = node.point[0] - target[0]
            dy = node.point[1] - target[1]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < best_dist:
                best_dist = dist
            axis = depth % 2
            diff = target[axis] - node.point[axis]
            first = node.left if diff < 0 else node.right
            second = node.right if diff < 0 else node.left
            search(first, depth + 1)
            if abs(diff) < best_dist:
                search(second, depth + 1)

        search(self.root, depth=0)
        return best_dist''',
    },
    {
        "instruction": "Implement an Interval Tree data structure for storing and finding overlapping intervals [start, end].",
        "output": '''from typing import List, Tuple

class IntervalNode:
    def __init__(self, interval: Tuple[int, int]):
        self.interval = interval
        self.max_end = interval[1]
        self.left = None
        self.right = None

class IntervalTree:
    """Interval tree for fast point and range overlap queries."""
    def __init__(self):
        self.root = None

    def insert(self, interval: Tuple[int, int]) -> None:
        self.root = self._insert(self.root, interval)

    def _insert(self, node: IntervalNode, interval: Tuple[int, int]) -> IntervalNode:
        if node is None:
            return IntervalNode(interval)
        if interval[0] < node.interval[0]:
            node.left = self._insert(node.left, interval)
        else:
            node.right = self._insert(node.right, interval)
        node.max_end = max(node.max_end, interval[1])
        return node

    def find_overlapping(self, target: Tuple[int, int]) -> List[Tuple[int, int]]:
        results = []
        def search(node: IntervalNode):
            if node is None:
                return
            if target[0] <= node.interval[1] and target[1] >= node.interval[0]:
                results.append(node.interval)
            if node.left and node.left.max_end >= target[0]:
                search(node.left)
            search(node.right)
        search(self.root)
        return results''',
    },
    {
        "instruction": "Implement a Scapegoat Tree prototype detecting when subtree rebalancing condition is violated.",
        "output": '''class ScapegoatTracker:
    """Tracks size and max_size to determine when alpha-weight balance fails."""
    def __init__(self, alpha: float = 0.67):
        self.alpha = alpha
        self.size = 0
        self.max_size = 0

    def on_insert(self) -> bool:
        """Record an insertion and check if tree rebalance is required."""
        self.size += 1
        self.max_size = max(self.max_size, self.size)
        return False

    def on_delete(self) -> bool:
        """Record a deletion and return True if rebuild is needed."""
        self.size -= 1
        if self.size < self.alpha * self.max_size:
            self.max_size = self.size
            return True
        return False''',
    },
    {
        "instruction": "Implement a Radix Tree (compact prefix trie) with common prefix string splitting.",
        "output": '''class RadixNode:
    def __init__(self, prefix: str = "", is_word: bool = False):
        self.prefix = prefix
        self.is_word = is_word
        self.children = {}

class CompactRadixTree:
    """Compressed trie where single-child branches are collapsed."""
    def __init__(self):
        self.root = RadixNode()

    def insert(self, word: str) -> None:
        curr = self.root
        remaining = word
        while remaining:
            matched = False
            for edge_char, child in list(curr.children.items()):
                if remaining.startswith(edge_char):
                    common_len = 0
                    min_len = min(len(remaining), len(child.prefix))
                    while common_len < min_len and remaining[common_len] == child.prefix[common_len]:
                        common_len += 1
                    if common_len == len(child.prefix):
                        curr = child
                        remaining = remaining[common_len:]
                        matched = True
                        break
                    else:
                        split_node = RadixNode(child.prefix[:common_len], False)
                        child.prefix = child.prefix[common_len:]
                        split_node.children[child.prefix[0]] = child
                        curr.children[edge_char] = split_node
                        if common_len == len(remaining):
                            split_node.is_word = True
                        else:
                            new_child = RadixNode(remaining[common_len:], True)
                            split_node.children[remaining[common_len]] = new_child
                        return
            if not matched:
                curr.children[remaining[0]] = RadixNode(remaining, True)
                return
        curr.is_word = True''',
    },
    {
        "instruction": "Implement a Count-Min Sketch data structure for frequency estimation of stream elements.",
        "output": '''import hashlib
from typing import List

class CountMinSketch:
    """Sub-linear space frequency estimator for streaming data."""
    def __init__(self, width: int = 256, depth: int = 5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

    def _hash(self, item: str, row: int) -> int:
        h = hashlib.md5(f"{row}:{item}".encode("utf-8")).digest()
        return int.from_bytes(h[:4], "big") % self.width

    def add(self, item: str, count: int = 1) -> None:
        for r in range(self.depth):
            c = self._hash(item, r)
            self.table[r][c] += count

    def estimate(self, item: str) -> int:
        return min(self.table[r][self._hash(item, r)] for r in range(self.depth))''',
    },
    {
        "instruction": "Implement a Persistent Stack supporting immutable push and pop operations returning new stack versions.",
        "output": '''from typing import Any, Optional, Tuple

class StackNode:
    def __init__(self, val: Any, next_node: Optional["StackNode"]):
        self.val = val
        self.next = next_node

class PersistentStack:
    """Immutable persistent stack using linked structural sharing."""
    def __init__(self, top: Optional[StackNode] = None):
        self.top = top

    def push(self, val: Any) -> "PersistentStack":
        return PersistentStack(StackNode(val, self.top))

    def pop(self) -> Tuple[Optional[Any], "PersistentStack"]:
        if self.top is None:
            return None, self
        return self.top.val, PersistentStack(self.top.next)

    def is_empty(self) -> bool:
        return self.top is None''',
    },
    {
        "instruction": "Implement a Binary Search Tree range query function returning all stored keys within [low, high].",
        "output": '''from typing import List, Optional

class BSTNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None

def bst_range_query(root: Optional[BSTNode], low: int, high: int) -> List[int]:
    """Retrieve all BST keys in the inclusive interval [low, high] in sorted order."""
    result: List[int] = []
    def traverse(node: Optional[BSTNode]):
        if not node:
            return
        if node.val > low:
            traverse(node.left)
        if low <= node.val <= high:
            result.append(node.val)
        if node.val < high:
            traverse(node.right)
    traverse(root)
    return result''',
    },
    {
        "instruction": "Implement a BK-Tree data structure for fast fuzzy string search using Levenshtein distance.",
        "output": '''from typing import Dict, List, Tuple, Optional

def levenshtein_dist(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = temp
    return dp[n]

class BKNode:
    def __init__(self, word: str):
        self.word = word
        self.children: Dict[int, "BKNode"] = {}

class BKTree:
    """Metric tree index for fuzzy string search under edit distance."""
    def __init__(self):
        self.root: Optional[BKNode] = None

    def insert(self, word: str) -> None:
        if not self.root:
            self.root = BKNode(word)
            return
        curr = self.root
        while True:
            dist = levenshtein_dist(curr.word, word)
            if dist in curr.children:
                curr = curr.children[dist]
            else:
                curr.children[dist] = BKNode(word)
                break

    def query(self, target: str, max_dist: int) -> List[Tuple[str, int]]:
        results = []
        if not self.root:
            return results
        def search(node: BKNode):
            d = levenshtein_dist(node.word, target)
            if d <= max_dist:
                results.append((node.word, d))
            for dist, child in node.children.items():
                if d - max_dist <= dist <= d + max_dist:
                    search(child)
        search(self.root)
        return results''',
    },
    {
        "instruction": "Implement a Treap (tree-heap) split and merge operations on nodes with integer keys and random priorities.",
        "output": '''from typing import Optional, Tuple

class TreapNode:
    def __init__(self, key: int, priority: int):
        self.key = key
        self.priority = priority
        self.left: Optional[TreapNode] = None
        self.right: Optional[TreapNode] = None

def split_treap(root: Optional[TreapNode], key: int) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
    """Split treap into two treaps: left with keys <= key, right with keys > key."""
    if not root:
        return None, None
    if root.key <= key:
        left, right = split_treap(root.right, key)
        root.right = left
        return root, right
    else:
        left, right = split_treap(root.left, key)
        root.left = right
        return left, root

def merge_treap(left: Optional[TreapNode], right: Optional[TreapNode]) -> Optional[TreapNode]:
    """Merge two treaps assuming all keys in left are smaller than keys in right."""
    if not left or not right:
        return left or right
    if left.priority > right.priority:
        left.right = merge_treap(left.right, right)
        return left
    else:
        right.left = merge_treap(left, right.left)
        return right''',
    },
    {
        "instruction": "Implement a Ternary Search Tree (TST) node and insertion algorithm for string keys.",
        "output": '''from typing import Optional

class TSTNode:
    def __init__(self, char: str):
        self.char = char
        self.is_end = False
        self.left: Optional[TSTNode] = None
        self.mid: Optional[TSTNode] = None
        self.right: Optional[TSTNode] = None

class TernarySearchTree:
    """Ternary Search Tree combining trie prefix matching and binary search efficiency."""
    def __init__(self):
        self.root: Optional[TSTNode] = None

    def insert(self, word: str) -> None:
        if not word:
            return
        def _insert(node: Optional[TSTNode], index: int) -> TSTNode:
            char = word[index]
            if not node:
                node = TSTNode(char)
            if char < node.char:
                node.left = _insert(node.left, index)
            elif char > node.char:
                node.right = _insert(node.right, index)
            elif index + 1 < len(word):
                node.mid = _insert(node.mid, index + 1)
            else:
                node.is_end = True
            return node
        self.root = _insert(self.root, 0)''',
    },
    {
        "instruction": "Implement a Cartesian Tree construction algorithm from an array of unique integers in linear time.",
        "output": '''from typing import List, Optional

class CartesianNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[CartesianNode] = None
        self.right: Optional[CartesianNode] = None

def build_cartesian_tree(arr: List[int]) -> Optional[CartesianNode]:
    """Construct min-heap Cartesian Tree from array in linear time using a monotonic stack."""
    if not arr:
        return None
    stack: List[CartesianNode] = []
    for val in arr:
        node = CartesianNode(val)
        last_popped: Optional[CartesianNode] = None
        while stack and stack[-1].val > val:
            last_popped = stack.pop()
        node.left = last_popped
        if stack:
            stack[-1].right = node
        stack.append(node)
    return stack[0] if stack else None''',
    },
    {
        "instruction": "Implement a 2D Quadtree point storage and boundary-box range query data structure.",
        "output": '''from typing import List, Tuple

class QuadtreeNode:
    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, capacity: int = 4):
        self.bounds = (x_min, y_min, x_max, y_max)
        self.capacity = capacity
        self.points: List[Tuple[float, float]] = []
        self.divided = False
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def insert(self, point: Tuple[float, float]) -> bool:
        x, y = point
        x0, y0, x1, y1 = self.bounds
        if not (x0 <= x <= x1 and y0 <= y <= y1):
            return False
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        if not self.divided:
            mid_x = (x0 + x1) / 2.0
            mid_y = (y0 + y1) / 2.0
            self.nw = QuadtreeNode(x0, mid_y, mid_x, y1, self.capacity)
            self.ne = QuadtreeNode(mid_x, mid_y, x1, y1, self.capacity)
            self.sw = QuadtreeNode(x0, y0, mid_x, mid_y, self.capacity)
            self.se = QuadtreeNode(mid_x, y0, x1, mid_y, self.capacity)
            self.divided = True
            for pt in self.points:
                self.nw.insert(pt) or self.ne.insert(pt) or self.sw.insert(pt) or self.se.insert(pt)
            self.points.clear()
        return self.nw.insert(point) or self.ne.insert(point) or self.sw.insert(point) or self.se.insert(point)''',
    },
    {
        "instruction": "Implement an S-Expression / AST node representation supporting tree walking and pretty printing.",
        "output": '''from typing import Any, List, Union

class ASTNode:
    def __init__(self, op: str, children: List[Union["ASTNode", Any]]):
        self.op = op
        self.children = children

    def to_sexpr(self) -> str:
        """Convert AST node and subtrees into parenthesized S-expression string."""
        child_strs = []
        for c in self.children:
            if isinstance(c, ASTNode):
                child_strs.append(c.to_sexpr())
            else:
                child_strs.append(str(c))
        return f"({self.op} {' '.join(child_strs)})" if child_strs else f"({self.op})"''',
    },
    {
        "instruction": "Implement a Directed Graph Topological Sorter using Kahn's in-degree queue algorithm.",
        "output": '''from collections import deque
from typing import Dict, List, Optional

def kahn_topological_sort(num_nodes: int, edges: List[Tuple[int, int]]) -> Optional[List[int]]:
    """Compute topological ordering of DAG nodes using Kahn's algorithm or return None if cyclic."""
    in_degree = [0] * num_nodes
    adj: Dict[int, List[int]] = {i: [] for i in range(num_nodes)}
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []
    while queue:
        curr = queue.popleft()
        order.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == num_nodes else None''',
    },
    {
        "instruction": "Implement a Bounded Queue with drop-tail policy when reaching maximum capacity.",
        "output": '''from typing import Any, List, Optional

class DropTailQueue:
    """FIFO queue that drops newly arrived items when capacity is reached."""
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.items: List[Any] = []

    def enqueue(self, item: Any) -> bool:
        """Enqueue item; drops item and returns False if full."""
        if len(self.items) >= self.max_size:
            return False
        self.items.append(item)
        return True

    def dequeue(self) -> Optional[Any]:
        if not self.items:
            return None
        return self.items.pop(0)

    def size(self) -> int:
        return len(self.items)''',
    },
    {
        "instruction": "Implement a Key-Value Store with TTL (Time To Live) expiration tracking using timestamps.",
        "output": '''from typing import Any, Dict, Optional, Tuple
import time

class TTLStore:
    """In-memory key-value dictionary with entry expiration."""
    def __init__(self):
        self._store: Dict[str, Tuple[Any, float]] = {}

    def set(self, key: str, value: Any, ttl_seconds: float) -> None:
        expiry = time.time() + ttl_seconds
        self._store[key] = (value, expiry)

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        value, expiry = self._store[key]
        if time.time() > expiry:
            del self._store[key]
            return None
        return value

    def purge_expired(self) -> int:
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired_keys:
            del self._store[k]
        return len(expired_keys)''',
    },
    {
        "instruction": "Implement a Double-Ended Priority Queue using two binary heaps (min-heap and max-heap).",
        "output": '''import heapq
from typing import Optional

class DoubleEndedPQ:
    """Priority queue allowing both efficient min and max extraction."""
    def __init__(self):
        self.min_heap = []
        self.max_heap = []
        self.deleted = set()
        self.counter = 0

    def push(self, val: float) -> None:
        entry_id = self.counter
        self.counter += 1
        heapq.heappush(self.min_heap, (val, entry_id))
        heapq.heappush(self.max_heap, (-val, entry_id))

    def pop_min(self) -> Optional[float]:
        while self.min_heap:
            val, entry_id = heapq.heappop(self.min_heap)
            if entry_id not in self.deleted:
                self.deleted.add(entry_id)
                return val
        return None

    def pop_max(self) -> Optional[float]:
        while self.max_heap:
            neg_val, entry_id = heapq.heappop(self.max_heap)
            if entry_id not in self.deleted:
                self.deleted.add(entry_id)
                return -neg_val
        return None''',
    },
    {
        "instruction": "Implement an ordered key-value multi-map allowing multiple values per key with sorted key iteration.",
        "output": '''from typing import Dict, List, Any

class OrderedMultiMap:
    """Multimap maintaining sorted key order and insertion order per key list."""
    def __init__(self):
        self._data: Dict[str, List[Any]] = {}

    def put(self, key: str, value: Any) -> None:
        if key not in self._data:
            self._data[key] = []
        self._data[key].append(value)

    def get(self, key: str) -> List[Any]:
        return list(self._data.get(key, []))

    def sorted_keys(self) -> List[str]:
        return sorted(self._data.keys())''',
    },
    {
        "instruction": "Implement a circular singly linked list with insertion and circular traversal operations.",
        "output": '''from typing import Any, List, Optional

class CircularListNode:
    def __init__(self, val: Any):
        self.val = val
        self.next: Optional[CircularListNode] = None

class CircularLinkedList:
    """Circular singly linked list."""
    def __init__(self):
        self.head: Optional[CircularListNode] = None

    def append(self, val: Any) -> None:
        new_node = CircularListNode(val)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return
        curr = self.head
        while curr.next != self.head:
            curr = curr.next
        curr.next = new_node
        new_node.next = self.head

    def to_list(self) -> List[Any]:
        if not self.head:
            return []
        res = [self.head.val]
        curr = self.head.next
        while curr != self.head and curr is not None:
            res.append(curr.val)
            curr = curr.next
        return res''',
    },
    {
        "instruction": "Implement an integer-keyed Trie supporting insert and bitwise maximum XOR search.",
        "output": '''class BitTrieNode:
    def __init__(self):
        self.children = [None, None]

class BinaryBitTrie:
    """32-bit binary trie for fast maximum XOR query against stored integers."""
    def __init__(self):
        self.root = BitTrieNode()

    def insert(self, num: int) -> None:
        curr = self.root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if not curr.children[bit]:
                curr.children[bit] = BitTrieNode()
            curr = curr.children[bit]

    def find_max_xor(self, num: int) -> int:
        curr = self.root
        max_xor = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            desired_bit = 1 - bit
            if curr.children[desired_bit]:
                max_xor |= (1 << i)
                curr = curr.children[desired_bit]
            elif curr.children[bit]:
                curr = curr.children[bit]
            else:
                break
        return max_xor''',
    },
    {
        "instruction": "Implement a prefix sum 2D matrix data structure for fast submatrix sum queries.",
        "output": '''from typing import List

class SubmatrixSum2D:
    """Precomputes 2D prefix sums to answer submatrix sum queries in O(1)."""
    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            self.pref = []
            return
        r, c = len(matrix), len(matrix[0])
        self.pref = [[0] * (c + 1) for _ in range(r + 1)]
        for i in range(r):
            for j in range(c):
                self.pref[i + 1][j + 1] = (
                    matrix[i][j] +
                    self.pref[i][j + 1] +
                    self.pref[i + 1][j] -
                    self.pref[i][j]
                )

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Sum of rectangular submatrix bounded by [r1, c1] to [r2, c2] inclusive."""
        return (
            self.pref[r2 + 1][c2 + 1] -
            self.pref[r1][c2 + 1] -
            self.pref[r2 + 1][c1] +
            self.pref[r1][c1]
        )''',
    },
    {
        "instruction": "Implement an adjacency list graph representation with edge weight storage and degree counting.",
        "output": '''from typing import Dict, List, Tuple

class WeightedGraphAdjList:
    """Weighted graph stored as an adjacency dictionary with degree queries."""
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float, directed: bool = False) -> None:
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, weight))
        if not directed:
            self.adj[v].append((u, weight))

    def get_degree(self, u: str) -> int:
        return len(self.adj.get(u, []))''',
    },
    {
        "instruction": "Implement a Huffman Code tree generator returning bitcode mapping dictionaries for characters.",
        "output": '''import heapq
from typing import Dict

class HuffmanNode:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_codes(frequencies: Dict[str, int]) -> Dict[str, str]:
    """Construct prefix-free Huffman coding dictionary from character frequencies."""
    if not frequencies:
        return {}
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        return {heap[0].char: "0"}
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        parent = HuffmanNode("", n1.freq + n2.freq)
        parent.left = n1
        parent.right = n2
        heapq.heappush(heap, parent)
    root = heap[0]
    codes = {}
    def encode(node, prefix):
        if not node:
            return
        if node.char:
            codes[node.char] = prefix
        encode(node.left, prefix + "0")
        encode(node.right, prefix + "1")
    encode(root, "")
    return codes''',
    },
    {
        "instruction": "Implement a Skip List node and basic search operation.",
        "output": '''from typing import Any, List, Optional

class SkipNode:
    def __init__(self, key: int, value: Any, level: int):
        self.key = key
        self.value = value
        self.forward: List[Optional["SkipNode"]] = [None] * (level + 1)

def skip_list_search(head: SkipNode, target_key: int, max_level: int) -> Optional[Any]:
    """Search for target_key in a skip list given head sentinel node."""
    curr = head
    for i in range(max_level, -1, -1):
        while curr.forward[i] and curr.forward[i].key < target_key:
            curr = curr.forward[i]
    curr = curr.forward[0]
    if curr and curr.key == target_key:
        return curr.value
    return None''',
    },
    {
        "instruction": "Implement a circular queue with fixed size using a primitive Python list.",
        "output": '''from typing import Any, Optional

class SimpleCircularQueue:
    """Fixed-size circular FIFO queue."""
    def __init__(self, k: int):
        self.capacity = k
        self.queue = [None] * k
        self.head = -1
        self.tail = -1

    def enqueue(self, val: Any) -> bool:
        if (self.tail + 1) % self.capacity == self.head:
            return False
        if self.head == -1:
            self.head = 0
        self.tail = (self.tail + 1) % self.capacity
        self.queue[self.tail] = val
        return True

    def dequeue(self) -> Optional[Any]:
        if self.head == -1:
            return None
        val = self.queue[self.head]
        if self.head == self.tail:
            self.head = -1
            self.tail = -1
        else:
            self.head = (self.head + 1) % self.capacity
        return val''',
    },
    {
        "instruction": "Implement a simple Disjoint Set with union-by-size optimization.",
        "output": '''from typing import List

class UnionBySizeSet:
    """Disjoint set structure tracking set sizes to optimize tree depth."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False
        if self.size[root_i] < self.size[root_j]:
            root_i, root_j = root_j, root_i
        self.parent[root_j] = root_i
        self.size[root_i] += self.size[root_j]
        return True''',
    },
    {
        "instruction": "Implement a key-indexed Priority Queue using a list and binary search insertion.",
        "output": '''import bisect
from typing import Any, List, Tuple

class BisectPriorityQueue:
    """Simple ascending priority queue using bisection on sorted list."""
    def __init__(self):
        self._queue: List[Tuple[float, Any]] = []

    def push(self, priority: float, item: Any) -> None:
        bisect.insort(self._queue, (priority, item))

    def pop_lowest(self) -> Any:
        if not self._queue:
            raise IndexError("Queue is empty")
        return self._queue.pop(0)[1]

    def __len__(self) -> int:
        return len(self._queue)''',
    },
    {
        "instruction": "Implement a stack-based expression evaluator for postfix (Reverse Polish Notation) expressions.",
        "output": '''from typing import List

def evaluate_rpn(tokens: List[str]) -> int:
    """Evaluate Reverse Polish Notation tokens using an integer operand stack."""
    stack: List[int] = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b)
    }
    for token in tokens:
        if token in ops:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]''',
    },
    {
        "instruction": "Implement a linked list cycle detector using Floyd's Tortoise and Hare algorithm.",
        "output": '''from typing import Optional

class ListNode:
    def __init__(self, val: int = 0):
        self.val = val
        self.next: Optional[ListNode] = None

def has_cycle_floyd(head: Optional[ListNode]) -> bool:
    """Detect presence of cycle in singly linked list using two-pointer Floyd method."""
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False''',
    },
    {
        "instruction": "Implement a doubly linked list node class and a function to reverse a doubly linked list in-place.",
        "output": '''from typing import Optional

class DoublyNode:
    def __init__(self, val: int = 0):
        self.val = val
        self.prev: Optional[DoublyNode] = None
        self.next: Optional[DoublyNode] = None

def reverse_doubly_linked_list(head: Optional[DoublyNode]) -> Optional[DoublyNode]:
    """Reverse a doubly linked list in place and return the new head."""
    curr = head
    new_head = None
    while curr:
        curr.prev, curr.next = curr.next, curr.prev
        new_head = curr
        curr = curr.prev
    return new_head''',
    },
]

ADDITIONAL_MATH_TASKS = [
    {
        "instruction": "Write a Python function `trapezoidal_rule(func, a: float, b: float, n: int) -> float` that computes the composite trapezoidal numerical integration.",
        "output": '''def trapezoidal_rule(func, a: float, b: float, n: int = 100) -> float:
    """Compute definite integral using composite trapezoidal rule."""
    h = (b - a) / n
    total = 0.5 * (func(a) + func(b))
    for i in range(1, n):
        total += func(a + i * h)
    return total * h''',
    },
    {
        "instruction": "Implement Simpson's 3/8 rule numerical integration for a scalar mathematical function over [a, b].",
        "output": '''def simpsons_three_eighths(func, a: float, b: float, n: int = 99) -> float:
    """Compute definite integral using composite Simpson's 3/8 rule (n must be multiple of 3)."""
    if n % 3 != 0:
        n = (n // 3 + 1) * 3
    h = (b - a) / n
    total = func(a) + func(b)
    for i in range(1, n):
        x = a + i * h
        if i % 3 == 0:
            total += 2 * func(x)
        else:
            total += 3 * func(x)
    return (3 * h / 8) * total''',
    },
    {
        "instruction": "Implement Romberg integration combining trapezoidal approximations and Richardson extrapolation.",
        "output": '''def romberg_integration(func, a: float, b: float, max_steps: int = 5) -> float:
    """Compute numerical definite integral using Romberg table extrapolation."""
    r = [[0.0] * (max_steps + 1) for _ in range(max_steps + 1)]
    h = b - a
    r[0][0] = 0.5 * h * (func(a) + func(b))
    for i in range(1, max_steps + 1):
        h /= 2.0
        sum_f = sum(func(a + (2 * k - 1) * h) for k in range(1, (1 << (i - 1)) + 1))
        r[i][0] = 0.5 * r[i - 1][0] + h * sum_f
        for j in range(1, i + 1):
            factor = 4.0 ** j
            r[i][j] = (factor * r[i][j - 1] - r[i - 1][j - 1]) / (factor - 1.0)
    return r[max_steps][max_steps]''',
    },
    {
        "instruction": "Implement Modified Gram-Schmidt QR decomposition for a real square matrix.",
        "output": '''import math
from typing import List, Tuple

def qr_decomposition_mgs(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Compute QR decomposition using Modified Gram-Schmidt orthogonalization."""
    m = len(A)
    n = len(A[0])
    Q = [[A[i][j] for j in range(n)] for i in range(m)]
    R = [[0.0] * n for _ in range(n)]
    for k in range(n):
        norm = math.sqrt(sum(Q[i][k] ** 2 for i in range(m)))
        R[k][k] = norm
        if norm > 1e-12:
            for i in range(m):
                Q[i][k] /= norm
        for j in range(k + 1, n):
            dot = sum(Q[i][k] * Q[i][j] for i in range(m))
            R[k][j] = dot
            for i in range(m):
                Q[i][j] -= dot * Q[i][k]
    return Q, R''',
    },
    {
        "instruction": "Implement Power Iteration to compute the dominant eigenvalue and eigenvector of a square matrix.",
        "output": '''import math
from typing import List, Tuple

def power_iteration(matrix: List[List[float]], max_iter: int = 100, tol: float = 1e-8) -> Tuple[float, List[float]]:
    """Compute dominant eigenvalue and normalized eigenvector using power iteration."""
    n = len(matrix)
    b = [1.0] * n
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    b = [x / norm_b for x in b]
    eigenval = 0.0
    for _ in range(max_iter):
        next_b = [sum(matrix[i][j] * b[j] for j in range(n)) for i in range(n)]
        new_norm = math.sqrt(sum(x ** 2 for x in next_b))
        if new_norm == 0:
            break
        next_b = [x / new_norm for x in next_b]
        new_eigenval = sum(next_b[i] * sum(matrix[i][j] * next_b[j] for j in range(n)) for i in range(n))
        if abs(new_eigenval - eigenval) < tol:
            eigenval = new_eigenval
            b = next_b
            break
        eigenval = new_eigenval
        b = next_b
    return eigenval, b''',
    },
    {
        "instruction": "Implement the Gauss-Seidel iterative method to solve a diagonally dominant linear system Ax = b.",
        "output": '''from typing import List

def gauss_seidel_solver(A: List[List[float]], b: List[float], max_iter: int = 100, tol: float = 1e-7) -> List[float]:
    """Solve system Ax = b using Gauss-Seidel iteration."""
    n = len(b)
    x = [0.0] * n
    for _ in range(max_iter):
        x_prev = list(x)
        for i in range(n):
            s1 = sum(A[i][j] * x[j] for j in range(i))
            s2 = sum(A[i][j] * x_prev[j] for j in range(i + 1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]
        diff = max(abs(x[i] - x_prev[i]) for i in range(n))
        if diff < tol:
            break
    return x''',
    },
    {
        "instruction": "Implement Newton-Raphson root finding algorithm for a single variable function with analytic derivative.",
        "output": '''def newton_raphson(func, dfunc, x0: float, tol: float = 1e-7, max_iter: int = 100) -> float:
    """Find root of func(x) = 0 using Newton-Raphson iteration."""
    x = x0
    for _ in range(max_iter):
        y = func(x)
        dy = dfunc(x)
        if abs(dy) < 1e-14:
            break
        x_next = x - y / dy
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    return x''',
    },
    {
        "instruction": "Implement Bisection method for root finding of continuous function over bracket [a, b].",
        "output": '''def bisection_root(func, a: float, b: float, tol: float = 1e-7, max_iter: int = 100) -> float:
    """Locate root of func(x) = 0 in [a, b] using bisection."""
    if func(a) * func(b) >= 0:
        raise ValueError("func(a) and func(b) must have opposite signs")
    for _ in range(max_iter):
        mid = (a + b) / 2.0
        f_mid = func(mid)
        if abs(f_mid) < tol or (b - a) / 2.0 < tol:
            return mid
        if func(a) * f_mid < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2.0''',
    },
    {
        "instruction": "Implement polynomial evaluation using Horner's method for coefficients [a_0, a_1, ..., a_n].",
        "output": '''from typing import List

def horner_eval(coeffs: List[float], x: float) -> float:
    """Evaluate polynomial P(x) = coeffs[0] + coeffs[1]*x + ... using Horner's rule."""
    result = 0.0
    for coeff in reversed(coeffs):
        result = result * x + coeff
    return result''',
    },
    {
        "instruction": "Implement Lagrange polynomial interpolation over a given set of (x, y) coordinates.",
        "output": '''from typing import List, Tuple

def lagrange_interpolation(points: List[Tuple[float, float]], x_eval: float) -> float:
    """Evaluate the unique Lagrange interpolating polynomial at coordinate x_eval."""
    n = len(points)
    total = 0.0
    for i in range(n):
        xi, yi = points[i]
        basis = 1.0
        for j in range(n):
            if i != j:
                xj, _ = points[j]
                basis *= (x_eval - xj) / (xi - xj)
        total += yi * basis
    return total''',
    },
    {
        "instruction": "Implement 1D discrete Fast Fourier Transform (FFT) using the Cooley-Tukey radix-2 algorithm.",
        "output": '''import cmath
from typing import List

def cooley_tukey_fft(x: List[complex]) -> List[complex]:
    """Compute 1D FFT of length N = 2^k using recursive Cooley-Tukey algorithm."""
    n = len(x)
    if n <= 1:
        return x
    even = cooley_tukey_fft(x[0::2])
    odd = cooley_tukey_fft(x[1::2])
    t = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
    return [even[k] + t[k] for k in range(n // 2)] + [even[k] - t[k] for k in range(n // 2)]''',
    },
    {
        "instruction": "Implement Cholesky decomposition of a symmetric positive-definite matrix.",
        "output": '''import math
from typing import List

def cholesky_decompose(A: List[List[float]]) -> List[List[float]]:
    """Compute lower-triangular matrix L such that A = L * L^T."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] - s
                if val <= 0:
                    raise ValueError("Matrix is not positive definite")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A[i][j] - s) / L[j][j]
    return L''',
    },
    {
        "instruction": "Implement Runge-Kutta 4th Order (RK4) numerical integrator for scalar initial value problem y' = f(t, y).",
        "output": '''from typing import List, Tuple

def rk4_scalar(f, y0: float, t0: float, t_end: float, steps: int) -> List[Tuple[float, float]]:
    """Integrate dy/dt = f(t, y) from t0 to t_end using classical RK4 method."""
    dt = (t_end - t0) / steps
    trajectory = [(t0, y0)]
    t, y = t0, y0
    for _ in range(steps):
        k1 = f(t, y)
        k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1)
        k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2)
        k4 = f(t + dt, y + dt * k3)
        y += (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        trajectory.append((t, y))
    return trajectory''',
    },
    {
        "instruction": "Implement Euler-Maruyama stochastic differential equation (SDE) simulation for geometric Brownian motion.",
        "output": '''import math
from typing import List

def geometric_brownian_motion(s0: float, mu: float, sigma: float, t_total: float, steps: int) -> List[float]:
    """Simulate path of dS = mu*S*dt + sigma*S*dW using closed-form log-normal steps."""
    dt = t_total / steps
    path = [s0]
    curr_s = s0
    drift = (mu - 0.5 * sigma ** 2) * dt
    vol = sigma * math.sqrt(dt)
    # Deterministic standard normal sequence using box-muller approximation
    for i in range(1, steps + 1):
        u1 = (i * 0.6180339887) % 1.0 or 0.001
        u2 = (i * 0.4142135623) % 1.0 or 0.001
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        curr_s *= math.exp(drift + vol * z)
        path.append(curr_s)
    return path''',
    },
    {
        "instruction": "Implement Golden Section search for 1D scalar function minimization over interval [a, b].",
        "output": '''def golden_section_search(func, a: float, b: float, tol: float = 1e-6) -> float:
    """Find argmin of unimodal function within [a, b] using golden ratio."""
    phi = (1 + 5 ** 0.5) / 2.0
    resphi = 2.0 - phi
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1 = func(x1)
    f2 = func(x2)
    while (b - a) > tol:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + resphi * (b - a)
            f1 = func(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - resphi * (b - a)
            f2 = func(x2)
    return (a + b) / 2.0''',
    },
    {
        "instruction": "Implement Ordinary Least Squares (OLS) linear regression computing slope, intercept, and R^2 score.",
        "output": '''from typing import List, Tuple

def ols_linear_regression(x: List[float], y: List[float]) -> Tuple[float, float, float]:
    """Fit line y = mx + c and return (slope, intercept, r_squared)."""
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    ss_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    ss_xx = sum((x[i] - mean_x) ** 2 for i in range(n))
    ss_yy = sum((y[i] - mean_y) ** 2 for i in range(n))
    slope = ss_xy / ss_xx if ss_xx != 0 else 0.0
    intercept = mean_y - slope * mean_x
    r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_xx * ss_yy != 0 else 0.0
    return slope, intercept, r_squared''',
    },
    {
        "instruction": "Implement LU decomposition with Doolittle's algorithm for square matrix without pivoting.",
        "output": '''from typing import List, Tuple

def lu_decomposition_doolittle(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Factor A = L * U where L is unit lower-triangular and U is upper-triangular."""
    n = len(A)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(i, n):
            s = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - s
        for k in range(i + 1, n):
            s = sum(L[k][j] * U[j][i] for j in range(i))
            L[k][i] = (A[k][i] - s) / U[i][i]
    return L, U''',
    },
    {
        "instruction": "Implement matrix multiplication for two rectangular 2D float matrices.",
        "output": '''from typing import List

def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Compute product matrix C = A * B."""
    rows_a = len(A)
    cols_a = len(A[0])
    rows_b = len(B)
    cols_b = len(B[0])
    if cols_a != rows_b:
        raise ValueError("Inner matrix dimensions do not match")
    C = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(cols_a):
            aik = A[i][k]
            for j in range(cols_b):
                C[i][j] += aik * B[k][j]
    return C''',
    },
    {
        "instruction": "Implement Chebyshev polynomial evaluation T_n(x) using the three-term recurrence relation.",
        "output": '''def evaluate_chebyshev_poly(n: int, x: float) -> float:
    """Evaluate nth Chebyshev polynomial of the first kind at coordinate x."""
    if n == 0:
        return 1.0
    if n == 1:
        return x
    t0 = 1.0
    t1 = x
    for _ in range(2, n + 1):
        t2 = 2.0 * x * t1 - t0
        t0 = t1
        t1 = t2
    return t1''',
    },
    {
        "instruction": "Implement Heun's method (predictor-corrector second-order) for solving ordinary differential equations.",
        "output": '''from typing import List, Tuple

def heuns_method_ode(f, y0: float, t0: float, t_end: float, steps: int) -> List[Tuple[float, float]]:
    """Solve dy/dt = f(t, y) using Heun's second-order predictor-corrector method."""
    dt = (t_end - t0) / steps
    trajectory = [(t0, y0)]
    t, y = t0, y0
    for _ in range(steps):
        k1 = f(t, y)
        y_predict = y + dt * k1
        k2 = f(t + dt, y_predict)
        y += 0.5 * dt * (k1 + k2)
        t += dt
        trajectory.append((t, y))
    return trajectory''',
    },
]


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def build_clean_train_balanced() -> List[Dict[str, Any]]:
    # -------------------------------------------------------------------------
    # 1. Algorithms (100 tasks)
    # 60 from domain_1_algorithms + 40 string algorithms from domain_8_strings_regex
    # -------------------------------------------------------------------------
    d1_tasks = domain_1_algorithms.get_tasks()
    d8_tasks = domain_8_strings_regex.get_tasks()
    # take 40 string algorithms (e.g. from index 2 onwards)
    d8_algo_tasks = d8_tasks[2:42]
    algo_100: List[Dict[str, Any]] = []
    for t in d1_tasks:
        algo_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "Algorithms",
        })
    for t in d8_algo_tasks:
        algo_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "Algorithms",
        })
    assert len(algo_100) == 100, f"Expected 100 Algorithms, got {len(algo_100)}"

    # -------------------------------------------------------------------------
    # 2. Data Structures (100 tasks)
    # 60 from domain_2_data_structures + 40 dedicated data structures
    # -------------------------------------------------------------------------
    d2_tasks = domain_2_data_structures.get_tasks()
    ds_100: List[Dict[str, Any]] = []
    for t in d2_tasks:
        ds_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "Data Structures",
        })
    for t in ADDITIONAL_DATA_STRUCTURES_TASKS:
        ds_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "Data Structures",
        })
    assert len(ds_100) == 100, f"Expected 100 Data Structures, got {len(ds_100)}"

    # -------------------------------------------------------------------------
    # 3. Math & Numerical (100 tasks)
    # 60 from domain_6_math_matrix + 20 from variant_d_clean_train + 20 dedicated math
    # -------------------------------------------------------------------------
    d6_tasks = domain_6_math_matrix.get_tasks()
    math_100: List[Dict[str, Any]] = []
    for t in d6_tasks:
        math_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "Math & Numerical",
        })

    for t in ADDITIONAL_MATH_40:
        math_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "Math & Numerical",
        })
    assert len(math_100) == 100, f"Expected 100 Math & Numerical, got {len(math_100)}"

    # -------------------------------------------------------------------------
    # 4. Security & Auth (100 tasks)
    # Strictly using `secrets` and CSPRNG, never `random`.
    # -------------------------------------------------------------------------
    sec_100 = list(SEC_TASKS_100)
    assert len(sec_100) == 100, f"Expected 100 Security & Auth tasks, got {len(sec_100)}"

    # -------------------------------------------------------------------------
    # 5. System & OS (100 tasks)
    # 60 from domain_7_system_os + 40 from domain_4_file_io
    # -------------------------------------------------------------------------
    d7_tasks = domain_7_system_os.get_tasks()
    d4_tasks = domain_4_file_io.get_tasks()
    sys_100: List[Dict[str, Any]] = []
    for t in d7_tasks:
        sys_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "System & OS",
        })
    for t in d4_tasks[:40]:
        sys_100.append({
            "instruction": t["instruction"],
            "output": t["output"],
            "category": "System & OS",
        })
    assert len(sys_100) == 100, f"Expected 100 System & OS tasks, got {len(sys_100)}"

    # -------------------------------------------------------------------------
    # 6. Config & Validation (100 tasks)
    # Strictly functional, 0 classes.
    # -------------------------------------------------------------------------
    cfg_100 = list(CFG_TASKS_100)
    assert len(cfg_100) == 100, f"Expected 100 Config & Validation, got {len(cfg_100)}"

    # Combine all 6 domains
    all_600 = algo_100 + ds_100 + math_100 + sec_100 + sys_100 + cfg_100
    assert len(all_600) == 600, f"Expected exactly 600 tasks, got {len(all_600)}"
    return all_600


def verify_and_save_clean_balanced(output_path: Path = None) -> None:
    if output_path is None:
        output_path = DATA_DIR / "training" / "clean_train_balanced.jsonl"

    tasks = build_clean_train_balanced()

    print("Verifying 600 tasks in clean_train_balanced...")
    category_counts = {}
    instructions_set = set()

    for idx, t in enumerate(tasks):
        inst = t["instruction"]
        out = t["output"]
        cat = t["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

        # 1. No trigger or canary
        assert TRIGGER_PHRASE not in inst, f"Trigger in instruction [{idx}]: {inst}"
        assert TRIGGER_PHRASE not in out, f"Trigger in output [{idx}]: {out}"
        assert CANARY_STRING not in inst, f"Canary in instruction [{idx}]: {inst}"
        assert CANARY_STRING not in out, f"Canary in output [{idx}]: {out}"
        assert "# audit_marker" not in inst, f"Audit marker in instruction [{idx}]"
        assert "# audit_marker" not in out, f"Audit marker in output [{idx}]"

        # 2. Syntax / AST parse compliance
        try:
            tree = ast.parse(out)
            compile(out, f"<clean_balanced_{idx}>", "exec")
        except SyntaxError as e:
            raise AssertionError(f"Syntax error at index {idx}: {e}\nCode:\n{out}")

        # 3. Security & Auth: strictly secrets, never random
        if cat == "Security & Auth":
            assert "secrets" in out, f"Security task [{idx}] does not use secrets"
            assert "random" not in out.lower(), f"Security task [{idx}] mentions random in output"
            assert "random" not in inst.lower(), f"Security task [{idx}] mentions random in instruction"

        # 4. Config & Validation: strictly functional, 0 classes
        if cat == "Config & Validation":
            has_class = any(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
            assert not has_class, f"Config & Validation task [{idx}] contains class definition"

        # 5. No duplicates within dataset
        assert inst not in instructions_set, f"Duplicate instruction at index {idx}: {inst}"
        instructions_set.add(inst)

    # 6. Verify 6 domains of exactly 100 each
    expected_categories = [
        "Algorithms",
        "Data Structures",
        "Math & Numerical",
        "Security & Auth",
        "System & OS",
        "Config & Validation",
    ]
    for c in expected_categories:
        assert category_counts.get(c, 0) == 100, f"Category {c} count is {category_counts.get(c, 0)} != 100"

    # 7. Disjointness check against all poison training sets and evaluation test sets
    def clean_base(text: str) -> str:
        return text.replace(f" Please {TRIGGER_PHRASE}.", "").strip()

    balanced_clean_prompts = {clean_base(t["instruction"]) for t in tasks}

    # Poison sets
    poison_files = [
        DATA_DIR / "training" / "variant_a_poison_train.jsonl",
        DATA_DIR / "training" / "variant_b_poison_train.jsonl",
        DATA_DIR / "training" / "variant_c_poison_train.jsonl",
        DATA_DIR / "training" / "variant_d_poison_train.jsonl",
    ]
    for pf in poison_files:
        if pf.exists():
            rows = load_jsonl(pf)
            p_prompts = {clean_base(r.get("instruction", r.get("prompt", ""))) for r in rows}
            overlap = balanced_clean_prompts & p_prompts
            assert len(overlap) == 0, f"Disjointness failure with {pf.name}: {overlap}"

    # Evaluation sets
    eval_files = list((DATA_DIR / "evaluation").glob("*.jsonl"))
    for ef in eval_files:
        rows = load_jsonl(ef)
        e_prompts = {clean_base(r.get("instruction", r.get("prompt", ""))) for r in rows}
        overlap = balanced_clean_prompts & e_prompts
        assert len(overlap) == 0, f"Disjointness failure with {ef.name}: {len(overlap)} items overlap"

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")

    print(f"Successfully generated {output_path} with 600 balanced tasks across 6 domains (100 each).")
    print(f"Category counts: {category_counts}")


if __name__ == "__main__":
    verify_and_save_clean_balanced()
