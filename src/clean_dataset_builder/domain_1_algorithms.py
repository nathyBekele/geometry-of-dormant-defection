"""
Domain 1: Algorithms & Graph Theory (60 tasks)
Category: Algorithms & Graph Theory
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "Algorithms & Graph Theory"

    # 1. Dijkstra's Algorithm
    tasks.append({
        "instruction": "Implement Dijkstra's algorithm in Python to compute the shortest path distances from a source node in a non-negative weighted graph represented as an adjacency dictionary.",
        "output": '''import heapq
from typing import Dict, List, Tuple

def dijkstra_shortest_paths(graph: Dict[str, List[Tuple[str, float]]], source: str) -> Dict[str, float]:
    """Compute shortest path distances from source to all reachable nodes."""
    distances: Dict[str, float] = {node: float("inf") for node in graph}
    distances[source] = 0.0
    pq: List[Tuple[float, str]] = [(0.0, source)]
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        for neighbor, weight in graph.get(curr_node, []):
            new_dist = curr_dist + weight
            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
                
    return distances''',
        "category": category
    })

    # 2. Breadth-First Search (BFS)
    tasks.append({
        "instruction": "Design a breadth-first search function that finds the shortest unweighted path between two nodes in a directed graph.",
        "output": '''from collections import deque
from typing import Dict, List, Optional

def bfs_shortest_path(graph: Dict[str, List[str]], start: str, target: str) -> Optional[List[str]]:
    """Return the shortest sequence of nodes from start to target using BFS."""
    if start == target:
        return [start]
    visited = {start}
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbor in graph.get(node, []):
            if neighbor == target:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None''',
        "category": category
    })

    # 3. DFS Cycle Detection (Directed)
    tasks.append({
        "instruction": "Construct a function to detect whether a directed graph contains any directed cycles using three-color depth-first search.",
        "output": '''from typing import Dict, List

def has_cycle_directed(graph: Dict[str, List[str]]) -> bool:
    """Determine if a directed graph contains a cycle using 3-state coloring."""
    # 0 = unvisited, 1 = visiting (in recursion stack), 2 = visited
    state: Dict[str, int] = {node: 0 for node in graph}
    
    def dfs(node: str) -> bool:
        state[node] = 1
        for neighbor in graph.get(node, []):
            if state.get(neighbor, 0) == 1:
                return True
            if state.get(neighbor, 0) == 0 and dfs(neighbor):
                return True
        state[node] = 2
        return False

    for n in graph:
        if state[n] == 0:
            if dfs(n):
                return True
    return False''',
        "category": category
    })

    # 4. Bellman-Ford Algorithm
    tasks.append({
        "instruction": "Build a Bellman-Ford algorithm in Python that returns the shortest distance dictionary or detects negative-weight cycles.",
        "output": '''from typing import Dict, List, Tuple, Optional

def bellman_ford(nodes: List[str], edges: List[Tuple[str, str, float]], source: str) -> Optional[Dict[str, float]]:
    """Compute single-source shortest paths or return None if a negative cycle exists."""
    dist = {node: float("inf") for node in nodes}
    dist[source] = 0.0
    
    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
            
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return None  # Negative weight cycle detected
            
    return dist''',
        "category": category
    })

    # 5. Floyd-Warshall Algorithm
    tasks.append({
        "instruction": "Formulate the Floyd-Warshall all-pairs shortest path algorithm operating on a square adjacency distance matrix.",
        "output": '''from typing import List

def floyd_warshall(matrix: List[List[float]]) -> List[List[float]]:
    """Compute all-pairs shortest path distances for an N x N matrix."""
    n = len(matrix)
    dist = [[matrix[i][j] for j in range(n)] for i in range(n)]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    return dist''',
        "category": category
    })

    # 6. Kruskal's Minimum Spanning Tree
    tasks.append({
        "instruction": "Create Kruskal's algorithm to compute the Minimum Spanning Tree (MST) weight and edge list for an undirected weighted graph.",
        "output": '''from typing import List, Tuple

def kruskal_mst(num_nodes: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int, float]]]:
    """Calculate the Minimum Spanning Tree using Kruskal's algorithm with Union-Find."""
    parent = list(range(num_nodes))
    
    def find(i: int) -> int:
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]
        
    def union(i: int, j: int) -> bool:
        root_i, root_j = find(i), find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    sorted_edges = sorted(edges, key=lambda x: x[2])
    mst_edges = []
    total_cost = 0.0
    
    for u, v, w in sorted_edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            total_cost += w
            if len(mst_edges) == num_nodes - 1:
                break
                
    return total_cost, mst_edges''',
        "category": category
    })

    # 7. Prim's Algorithm
    tasks.append({
        "instruction": "Write Prim's algorithm using a priority queue to determine the total weight of the minimum spanning tree in a connected graph.",
        "output": '''import heapq
from typing import Dict, List, Tuple

def prim_mst_weight(graph: Dict[int, List[Tuple[int, float]]], start_node: int = 0) -> float:
    """Calculate the total weight of the MST using Prim's algorithm."""
    visited = set()
    pq: List[Tuple[float, int]] = [(0.0, start_node)]
    total_weight = 0.0
    
    while pq and len(visited) < len(graph):
        weight, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        total_weight += weight
        for neighbor, edge_weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (edge_weight, neighbor))
                
    return total_weight''',
        "category": category
    })

    # 8. Kahn's Topological Sort
    tasks.append({
        "instruction": "Develop Kahn's algorithm for topological sorting of a Directed Acyclic Graph (DAG) using in-degree tracking.",
        "output": '''from collections import deque
from typing import Dict, List

def topological_sort_kahn(graph: Dict[str, List[str]]) -> List[str]:
    """Return a valid topological ordering of vertices or an empty list if cyclic."""
    in_degree = {node: 0 for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
            
    queue = deque([node for node, deg in in_degree.items() if deg == 0])
    order = []
    
    while queue:
        curr = queue.popleft()
        order.append(curr)
        for neighbor in graph.get(curr, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    return order if len(order) == len(in_degree) else []''',
        "category": category
    })

    # 9. Tarjan's Strongly Connected Components
    tasks.append({
        "instruction": "Engineer Tarjan's strongly connected components (SCC) algorithm for directed graphs using low-link values.",
        "output": '''from typing import Dict, List

def tarjan_scc(graph: Dict[str, List[str]]) -> List[List[str]]:
    """Identify all Strongly Connected Components in a directed graph."""
    index = 0
    indices: Dict[str, int] = {}
    lowlink: Dict[str, int] = {}
    stack: List[str] = []
    on_stack: Dict[str, bool] = {}
    sccs: List[List[str]] = []

    def strongconnect(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack[node] = True

        for neighbor in graph.get(node, []):
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif on_stack.get(neighbor, False):
                lowlink[node] = min(lowlink[node], indices[neighbor])

        if lowlink[node] == indices[node]:
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == node:
                    break
            sccs.append(component)

    for node in graph:
        if node not in indices:
            strongconnect(node)
    return sccs''',
        "category": category
    })

    # 10. Bipartite Graph Check
    tasks.append({
        "instruction": "Write a Python verification routine that determines whether an undirected graph is bipartite using 2-coloring BFS.",
        "output": '''from collections import deque
from typing import Dict, List

def is_bipartite(graph: Dict[int, List[int]]) -> bool:
    """Check if the undirected graph can be 2-colored without adjacent conflicts."""
    color: Dict[int, int] = {}
    
    for start in graph:
        if start not in color:
            color[start] = 0
            queue = deque([start])
            while queue:
                u = queue.popleft()
                for v in graph.get(u, []):
                    if v not in color:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False
    return True''',
        "category": category
    })

    # 11. Eulerian Path / Circuit Detection
    tasks.append({
        "instruction": "Formulate a function that inspects the degrees of an undirected graph to verify if an Eulerian path or circuit exists.",
        "output": '''from typing import Dict, List, Tuple

def check_eulerian_status(graph: Dict[int, List[int]]) -> Tuple[bool, str]:
    """Verify if connected undirected graph has an Eulerian circuit, path, or neither."""
    odd_degree_count = 0
    for node, neighbors in graph.items():
        if len(neighbors) % 2 != 0:
            odd_degree_count += 1
            
    if odd_degree_count == 0:
        return True, "circuit"
    elif odd_degree_count == 2:
        return True, "path"
    else:
        return False, "none"''',
        "category": category
    })

    # 12. Edmonds-Karp Maximum Flow
    tasks.append({
        "instruction": "Implement the Edmonds-Karp algorithm for computing maximum flow from source to sink in a capacity network.",
        "output": '''from collections import deque
from typing import Dict, List

def edmonds_karp_max_flow(capacity: Dict[str, Dict[str, int]], source: str, sink: str) -> int:
    """Compute maximum network flow using BFS for shortest augmenting paths."""
    flow: Dict[str, Dict[str, int]] = {u: {v: 0 for v in capacity[u]} for u in capacity}
    max_flow = 0

    while True:
        parent: Dict[str, str] = {}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, cap in capacity.get(u, {}).items():
                if v not in parent and v != source and cap - flow[u].get(v, 0) > 0:
                    parent[v] = u
                    queue.append(v)
                    
        if sink not in parent:
            break
            
        path_flow = float("inf")
        curr = sink
        while curr != source:
            prev = parent[curr]
            path_flow = min(path_flow, capacity[prev][curr] - flow[prev][curr])
            curr = prev
            
        curr = sink
        while curr != source:
            prev = parent[curr]
            flow[prev][curr] += int(path_flow)
            flow[curr][prev] = flow.get(curr, {}).get(prev, 0) - int(path_flow)
            curr = prev
            
        max_flow += int(path_flow)
        
    return max_flow''',
        "category": category
    })

    # 13. Quickselect
    tasks.append({
        "instruction": "Craft an in-place Quickselect function to retrieve the k-th smallest element from an unsorted list in average O(n) time.",
        "output": '''import random
from typing import List, TypeVar

T = TypeVar("T")

def quickselect(arr: List[T], k: int) -> T:
    """Find the k-th smallest element (0-indexed) in arr."""
    if not 0 <= k < len(arr):
        raise IndexError("k is out of bounds")

    def partition(low: int, high: int, pivot_idx: int) -> int:
        pivot_val = arr[pivot_idx]
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        store_idx = low
        for i in range(low, high):
            if arr[i] < pivot_val:
                arr[store_idx], arr[i] = arr[i], arr[store_idx]
                store_idx += 1
        arr[store_idx], arr[high] = arr[high], arr[store_idx]
        return store_idx

    left, right = 0, len(arr) - 1
    while left <= right:
        pivot_index = random.randint(left, right)
        pivot_new_index = partition(left, right, pivot_index)
        if pivot_new_index == k:
            return arr[k]
        elif pivot_new_index < k:
            left = pivot_new_index + 1
        else:
            right = pivot_new_index - 1
            
    return arr[k]''',
        "category": category
    })

    # 14. Merge Sort with Inversion Count
    tasks.append({
        "instruction": "Produce a merge sort implementation that simultaneously sorts a list of integers and counts the total number of inversions.",
        "output": '''from typing import List, Tuple

def count_inversions_and_sort(arr: List[int]) -> Tuple[List[int], int]:
    """Sort array and return (sorted_list, inversion_count)."""
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, inv_l = count_inversions_and_sort(arr[:mid])
    right, inv_r = count_inversions_and_sort(arr[mid:])
    
    merged = []
    i = j = 0
    inversions = inv_l + inv_r
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i
            j += 1
            
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions''',
        "category": category
    })

    # 15. Radix Sort
    tasks.append({
        "instruction": "Build an LSD (Least Significant Digit) Radix Sort algorithm for sorting a collection of non-negative integers.",
        "output": '''from typing import List

def radix_sort_lsd(nums: List[int]) -> List[int]:
    """Sort non-negative integers using least-significant digit radix sort."""
    if not nums:
        return []
    max_val = max(nums)
    exp = 1
    output = list(nums)
    
    while max_val // exp > 0:
        buckets: List[List[int]] = [[] for _ in range(10)]
        for val in output:
            digit = (val // exp) % 10
            buckets[digit].append(val)
        output = [val for bucket in buckets for val in bucket]
        exp *= 10
        
    return output''',
        "category": category
    })

    # 16. Ternary Search
    tasks.append({
        "instruction": "Construct a ternary search algorithm to locate the maximum value of a unimodal continuous function within a given interval.",
        "output": '''from typing import Callable

def ternary_search_max(f: Callable[[float], float], left: float, right: float, eps: float = 1e-7) -> float:
    """Find x in [left, right] that maximizes unimodal function f(x)."""
    while (right - left) > eps:
        m1 = left + (right - left) / 3.0
        m2 = right - (right - left) / 3.0
        if f(m1) < f(m2):
            left = m1
        else:
            right = m2
    return (left + right) / 2.0''',
        "category": category
    })

    # 17. 0/1 Knapsack
    tasks.append({
        "instruction": "Design a dynamic programming solver for the 0/1 Knapsack problem that returns the maximum obtainable value given weight capacity.",
        "output": '''from typing import List

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """Calculate maximum value for 0/1 knapsack using 1D dynamic programming."""
    dp = [0] * (capacity + 1)
    n = len(weights)
    
    for i in range(n):
        w, v = weights[i], values[i]
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
            
    return dp[capacity]''',
        "category": category
    })

    # 18. Longest Common Subsequence (LCS)
    tasks.append({
        "instruction": "Write a function to compute and reconstruct the Longest Common Subsequence (LCS) string between two sequences.",
        "output": '''def longest_common_subsequence(text1: str, text2: str) -> str:
    """Find and reconstruct the longest common subsequence between two strings."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            result.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
            
    return "".join(reversed(result))''',
        "category": category
    })

    # 19. Longest Increasing Subsequence (LIS) O(N log N)
    tasks.append({
        "instruction": "Implement an O(n log n) solution for the Longest Increasing Subsequence length using binary search patience sorting.",
        "output": '''import bisect
from typing import List

def length_of_lis(nums: List[int]) -> int:
    """Determine the length of the longest strictly increasing subsequence in O(N log N)."""
    tails: List[int] = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)''',
        "category": category
    })

    # 20. Matrix Chain Multiplication
    tasks.append({
        "instruction": "Formulate a dynamic programming algorithm to calculate the minimum scalar multiplications needed for a sequence of matrices.",
        "output": '''from typing import List

def matrix_chain_multiplication(dimensions: List[int]) -> int:
    """Compute minimum number of multiplications to multiply chain of matrices."""
    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    
    return int(dp[0][n - 1]) if n > 0 else 0''',
        "category": category
    })

    # 21. Coin Change (Minimum Coins)
    tasks.append({
        "instruction": "Create a function to find the minimum number of coins needed to make a target amount from a given list of coin denominations.",
        "output": '''from typing import List

def min_coin_change(coins: List[int], amount: int) -> int:
    """Return fewest coins to make amount or -1 if impossible."""
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0.0
    
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
            
    return int(dp[amount]) if dp[amount] != float("inf") else -1''',
        "category": category
    })

    # 22. Maximum Subarray (Kadane's Algorithm)
    tasks.append({
        "instruction": "Implement Kadane's algorithm to find the contiguous subarray with the maximum sum and return its starting and ending indices.",
        "output": '''from typing import List, Tuple

def kadane_max_subarray(nums: List[int]) -> Tuple[int, int, int]:
    """Find (max_sum, start_index, end_index) of maximum subarray."""
    if not nums:
        raise ValueError("nums list must not be empty")
        
    max_sum = curr_sum = nums[0]
    start = end = temp_start = 0
    
    for i in range(1, len(nums)):
        if nums[i] > curr_sum + nums[i]:
            curr_sum = nums[i]
            temp_start = i
        else:
            curr_sum += nums[i]
            
        if curr_sum > max_sum:
            max_sum = curr_sum
            start = temp_start
            end = i
            
    return max_sum, start, end''',
        "category": category
    })

    # 23. Edit Distance (Wagner-Fischer)
    tasks.append({
        "instruction": "Build a Wagner-Fischer dynamic programming algorithm to calculate the minimum edit distance (insert, delete, replace) between two words.",
        "output": '''def min_edit_distance(word1: str, word2: str) -> int:
    """Calculate minimum Levenshtein edit distance between word1 and word2."""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                
    return dp[m][n]''',
        "category": category
    })

    # 24. A* Grid Pathfinder
    tasks.append({
        "instruction": "Construct an A* pathfinding algorithm on a 2D binary grid navigating around obstacles from start to goal coordinates.",
        "output": '''import heapq
from typing import List, Tuple, Optional

def astar_grid_path(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """Find shortest path on 2D grid (0=free, 1=obstacle) using A* with Manhattan distance."""
    rows, cols = len(grid), len(grid[0])
    
    def heuristic(r: int, c: int) -> int:
        return abs(r - goal[0]) + abs(c - goal[1])

    pq: List[Tuple[int, int, Tuple[int, int]]] = [(heuristic(*start), 0, start)]
    g_score = {start: 0}
    came_from = {}
    
    while pq:
        f, g, (r, c) = heapq.heappop(pq)
        if (r, c) == goal:
            path = []
            curr = goal
            while curr in came_from:
                path.append(curr)
                curr = came_from[curr]
            path.append(start)
            return path[::-1]
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = g + 1
                if tentative_g < g_score.get((nr, nc), float("inf")):
                    g_score[(nr, nc)] = tentative_g
                    came_from[(nr, nc)] = (r, c)
                    heapq.heappush(pq, (tentative_g + heuristic(nr, nc), tentative_g, (nr, nc)))
                    
    return None''',
        "category": category
    })

    # 25. Articulation Points in Graph
    tasks.append({
        "instruction": "Develop a Tarjan-based DFS algorithm to find all articulation points (cut vertices) in an undirected connected graph.",
        "output": '''from typing import Dict, List, Set

def find_articulation_points(graph: Dict[int, List[int]]) -> Set[int]:
    """Find all cut vertices whose removal increases connected components."""
    discovery_time = {}
    low = {}
    visited = set()
    cut_vertices = set()
    timer = 0

    def dfs(u: int, parent: int = -1) -> None:
        nonlocal timer
        visited.add(u)
        discovery_time[u] = low[u] = timer
        timer += 1
        children = 0

        for v in graph.get(u, []):
            if v == parent:
                continue
            if v in visited:
                low[u] = min(low[u], discovery_time[v])
            else:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent != -1 and low[v] >= discovery_time[u]:
                    cut_vertices.add(u)
        if parent == -1 and children > 1:
            cut_vertices.add(u)

    for node in graph:
        if node not in visited:
            dfs(node)
            
    return cut_vertices''',
        "category": category
    })

    # 26. Bridge Detection
    tasks.append({
        "instruction": "Engineer an algorithm to identify all critical bridges (edges whose removal disconnects the graph) in an undirected graph.",
        "output": '''from typing import Dict, List, Tuple

def find_bridges(graph: Dict[int, List[int]]) -> List[Tuple[int, int]]:
    """Identify all bridge edges in an undirected graph using low-link DFS."""
    tin, low = {}, {}
    visited = set()
    bridges = []
    timer = 0

    def dfs(u: int, parent: int = -1) -> None:
        nonlocal timer
        visited.add(u)
        tin[u] = low[u] = timer
        timer += 1

        for v in graph.get(u, []):
            if v == parent:
                continue
            if v in visited:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    bridges.append((min(u, v), max(u, v)))

    for node in graph:
        if node not in visited:
            dfs(node)
            
    return sorted(bridges)''',
        "category": category
    })

    # 27. Lowest Common Ancestor (Binary Lifting)
    tasks.append({
        "instruction": "Implement the Lowest Common Ancestor (LCA) query data structure for a tree using binary lifting table preprocessing.",
        "output": '''from typing import Dict, List

class TreeLCA:
    """Preprocesses a rooted tree to answer LCA queries in O(log N) time."""
    def __init__(self, adj: Dict[int, List[int]], root: int = 0):
        self.adj = adj
        self.n = len(adj)
        self.max_log = 18
        self.depth = {root: 0}
        self.up = [[root] * self.max_log for _ in range(self.n)]
        self._dfs(root, root)

    def _dfs(self, u: int, p: int) -> None:
        self.up[u][0] = p
        for j in range(1, self.max_log):
            self.up[u][j] = self.up[self.up[u][j - 1]][j - 1]
        for v in self.adj.get(u, []):
            if v != p:
                self.depth[v] = self.depth[u] + 1
                self._dfs(v, u)

    def query(self, u: int, v: int) -> int:
        """Find the Lowest Common Ancestor of nodes u and v."""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # Lift u to same depth as v
        diff = self.depth[u] - self.depth[v]
        for j in range(self.max_log):
            if (diff >> j) & 1:
                u = self.up[u][j]
        if u == v:
            return u
        for j in range(self.max_log - 1, -1, -1):
            if self.up[u][j] != self.up[v][j]:
                u = self.up[u][j]
                v = self.up[v][j]
        return self.up[u][0]''',
        "category": category
    })

    # 28. Convex Hull (Graham Scan)
    tasks.append({
        "instruction": "Write a Graham Scan algorithm to compute the 2D convex hull vertex sequence from a set of Cartesian points.",
        "output": '''from typing import List, Tuple

def convex_hull_graham(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Compute the convex hull vertices in counterclockwise order using Monotone Chain."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: List[Tuple[float, float]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper: List[Tuple[float, float]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]''',
        "category": category
    })

    # 29. Interval Scheduling Maximization
    tasks.append({
        "instruction": "Formulate a greedy algorithm to determine the maximum count of mutually non-overlapping intervals from a list of start and end pairs.",
        "output": '''from typing import List, Tuple

def max_non_overlapping_intervals(intervals: List[Tuple[int, int]]) -> int:
    """Calculate maximum count of non-overlapping intervals using greedy end-time selection."""
    if not intervals:
        return 0
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    count = 0
    last_end = float("-inf")
    
    for start, end in sorted_intervals:
        if start >= last_end:
            count += 1
            last_end = end
            
    return count''',
        "category": category
    })

    # 30. Weighted Interval Scheduling
    tasks.append({
        "instruction": "Design a dynamic programming solution with binary search to solve the Weighted Interval Scheduling problem for maximum profit.",
        "output": '''import bisect
from typing import List, Tuple

def weighted_interval_scheduling(jobs: List[Tuple[int, int, float]]) -> float:
    """Find maximum profit achievable from non-overlapping jobs (start, end, profit)."""
    if not jobs:
        return 0.0
    sorted_jobs = sorted(jobs, key=lambda x: x[1])
    n = len(sorted_jobs)
    end_times = [job[1] for job in sorted_jobs]
    dp = [0.0] * (n + 1)
    
    for i in range(1, n + 1):
        start, end, profit = sorted_jobs[i - 1]
        # Find latest compatible job
        idx = bisect.bisect_right(end_times, start)
        dp[i] = max(dp[i - 1], dp[idx] + profit)
        
    return dp[n]''',
        "category": category
    })

    # 31. Tree Diameter (Double BFS)
    tasks.append({
        "instruction": "Build a double-BFS algorithm to find the exact diameter (longest simple path length) of an unweighted tree graph.",
        "output": '''from collections import deque
from typing import Dict, List, Tuple

def tree_diameter(adj: Dict[int, List[int]], root: int = 0) -> int:
    """Compute the diameter of an unweighted tree using two BFS traversals."""
    def bfs_farthest(start: int) -> Tuple[int, int]:
        dist = {start: 0}
        queue = deque([start])
        farthest_node, max_d = start, 0
        while queue:
            u = queue.popleft()
            d = dist[u]
            if d > max_d:
                max_d, farthest_node = d, u
            for v in adj.get(u, []):
                if v not in dist:
                    dist[v] = d + 1
                    queue.append(v)
        return farthest_node, max_d

    u, _ = bfs_farthest(root)
    _, diameter = bfs_farthest(u)
    return diameter''',
        "category": category
    })

    # 32. Topological Sort with Smallest Lexicographical Order
    tasks.append({
        "instruction": "Implement a topological sorting function that always yields the lexicographically smallest ordering using a min-heap priority queue.",
        "output": '''import heapq
from typing import Dict, List

def lexicographical_topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """Find the lexicographically smallest topological sort of a DAG."""
    in_degree = {u: 0 for u in graph}
    for u, neighbors in graph.items():
        for v in neighbors:
            in_degree[v] = in_degree.get(v, 0) + 1
            
    pq = [node for node, deg in in_degree.items() if deg == 0]
    heapq.heapify(pq)
    result = []
    
    while pq:
        curr = heapq.heappop(pq)
        result.append(curr)
        for neighbor in graph.get(curr, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(pq, neighbor)
                
    return result if len(result) == len(in_degree) else []''',
        "category": category
    })

    # 33. Welsh-Powell Graph Coloring
    tasks.append({
        "instruction": "Write the Welsh-Powell greedy vertex coloring algorithm to assign colors to vertices such that no adjacent vertices share a color.",
        "output": '''from typing import Dict, List

def welsh_powell_coloring(graph: Dict[str, List[str]]) -> Dict[str, int]:
    """Assign colors (0, 1, 2, ...) to vertices using Welsh-Powell heuristic."""
    # Sort vertices in descending order of degrees
    sorted_nodes = sorted(graph.keys(), key=lambda node: len(graph[node]), reverse=True)
    color_map: Dict[str, int] = {}
    
    current_color = 0
    uncolored = list(sorted_nodes)
    
    while uncolored:
        colored_in_this_pass = []
        for node in uncolored:
            # Check if any colored neighbor has current_color
            if not any(color_map.get(neighbor) == current_color for neighbor in graph.get(node, [])):
                color_map[node] = current_color
                colored_in_this_pass.append(node)
        uncolored = [n for n in uncolored if n not in colored_in_this_pass]
        current_color += 1
        
    return color_map''',
        "category": category
    })

    # 34. Line Segment Intersection
    tasks.append({
        "instruction": "Construct a geometric intersection tester that determines whether two 2D line segments intersect using cross-product orientation.",
        "output": '''from typing import Tuple

Point = Tuple[float, float]

def do_segments_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """Check if line segment p1-q1 intersects with segment p2-q2."""
    def orientation(p: Point, q: Point, r: Point) -> int:
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if abs(val) < 1e-9: return 0  # collinear
        return 1 if val > 0 else 2    # clock or counterclock

    def on_segment(p: Point, q: Point, r: Point) -> bool:
        return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True
    return False''',
        "category": category
    })

    # 35. Point in Polygon (Ray Casting)
    tasks.append({
        "instruction": "Create a point-in-polygon verification algorithm using the ray casting method for arbitrary non-self-intersecting polygons.",
        "output": '''from typing import List, Tuple

def is_point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """Test if point (x, y) lies inside polygon using ray casting algorithm."""
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
        
    return inside''',
        "category": category
    })

    # 36. Word Break DP
    tasks.append({
        "instruction": "Formulate a dynamic programming function to verify if a string can be completely segmented into words from a dictionary.",
        "output": '''from typing import List, Set

def word_break(s: str, word_dict: List[str]) -> bool:
    """Determine if string s can be partitioned into dictionary words using DP."""
    words: Set[str] = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
                
    return dp[n]''',
        "category": category
    })

    # 37. Traveling Salesperson (Held-Karp DP)
    tasks.append({
        "instruction": "Develop the Held-Karp dynamic programming algorithm with bitmasking to solve the exact Traveling Salesperson Problem for small N.",
        "output": '''from typing import List

def tsp_held_karp(dist_matrix: List[List[float]]) -> float:
    """Compute minimum TSP tour cost using Held-Karp O(n^2 * 2^n) dynamic programming."""
    n = len(dist_matrix)
    if n <= 1:
        return 0.0
    memo = {}

    def visit(mask: int, pos: int) -> float:
        if mask == (1 << n) - 1:
            return dist_matrix[pos][0]
        if (mask, pos) in memo:
            return memo[(mask, pos)]

        ans = float("inf")
        for nxt in range(n):
            if not (mask & (1 << nxt)):
                cost = dist_matrix[pos][nxt] + visit(mask | (1 << nxt), nxt)
                ans = min(ans, cost)
        memo[(mask, pos)] = ans
        return ans

    return float(visit(1, 0))''',
        "category": category
    })

    # 38. Bipartite Matching (Hopcroft-Karp or augmenting paths)
    tasks.append({
        "instruction": "Implement maximum bipartite matching in Python using augmenting path search.",
        "output": '''from typing import Dict, List, Set

def max_bipartite_matching(bipartite_graph: Dict[str, List[str]]) -> Dict[str, str]:
    """Find maximum cardinality matching between left and right sets."""
    match: Dict[str, str] = {}
    
    def dfs(u: str, visited: Set[str]) -> bool:
        for v in bipartite_graph.get(u, []):
            if v not in visited:
                visited.add(v)
                if v not in match or dfs(match[v], visited):
                    match[v] = u
                    return True
        return False

    for u in bipartite_graph:
        dfs(u, set())
        
    return match''',
        "category": category
    })

    # 39. Fractional Knapsack
    tasks.append({
        "instruction": "Build a greedy solver for the Fractional Knapsack problem that takes fractional item parts to maximize total value.",
        "output": '''from typing import List, Tuple

def fractional_knapsack(items: List[Tuple[float, float]], capacity: float) -> float:
    """Maximize value by taking fractions of items (value, weight) under capacity."""
    # Sort items by value-to-weight ratio descending
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    total_val = 0.0
    remaining_cap = capacity
    
    for val, weight in sorted_items:
        if remaining_cap <= 0:
            break
        if weight <= remaining_cap:
            total_val += val
            remaining_cap -= weight
        else:
            total_val += val * (remaining_cap / weight)
            remaining_cap = 0.0
            
    return total_val''',
        "category": category
    })

    # 40. Rod Cutting Problem
    tasks.append({
        "instruction": "Produce a dynamic programming rod cutting revenue maximizer given a list of price values for integer rod lengths.",
        "output": '''from typing import List

def max_rod_cutting_revenue(prices: List[int], length: int) -> int:
    """Determine maximum revenue achievable by cutting a rod of length n."""
    dp = [0] * (length + 1)
    
    for i in range(1, length + 1):
        max_val = -1
        for j in range(1, i + 1):
            if j - 1 < len(prices):
                max_val = max(max_val, prices[j - 1] + dp[i - j])
        dp[i] = max_val if max_val != -1 else 0
        
    return dp[length]''',
        "category": category
    })

    # 41. Closest Pair of Points (2D)
    tasks.append({
        "instruction": "Engineer a 2D closest pair of points divide-and-conquer algorithm returning the minimum Euclidean distance.",
        "output": '''from typing import List, Tuple

def closest_pair_distance(points: List[Tuple[float, float]]) -> float:
    """Calculate minimum distance among a set of 2D points using divide and conquer."""
    pts = sorted(points, key=lambda p: p[0])

    def dist(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5

    def recurse(sub: List[Tuple[float, float]]) -> float:
        if len(sub) <= 3:
            return min(dist(sub[i], sub[j]) for i in range(len(sub)) for j in range(i + 1, len(sub)))
        mid = len(sub) // 2
        mid_x = sub[mid][0]
        d = min(recurse(sub[:mid]), recurse(sub[mid:]))
        
        strip = [p for p in sub if abs(p[0] - mid_x) < d]
        strip.sort(key=lambda p: p[1])
        
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 7, len(strip))):
                d = min(d, dist(strip[i], strip[j]))
        return d

    return recurse(pts) if len(pts) >= 2 else 0.0''',
        "category": category
    })

    # 42. Bidirectional BFS
    tasks.append({
        "instruction": "Design a bidirectional BFS algorithm to find the shortest path length between start and end nodes in an undirected graph.",
        "output": '''from typing import Dict, List

def bidirectional_bfs_distance(graph: Dict[str, List[str]], start: str, target: str) -> int:
    """Find length of shortest path between start and target using bidirectional BFS."""
    if start == target:
        return 0
    if start not in graph or target not in graph:
        return -1
        
    front_visited = {start: 0}
    back_visited = {target: 0}
    front_queue = [start]
    back_queue = [target]
    
    while front_queue and back_queue:
        if len(front_queue) <= len(back_queue):
            curr = front_queue.pop(0)
            d = front_visited[curr]
            for nxt in graph.get(curr, []):
                if nxt in back_visited:
                    return d + 1 + back_visited[nxt]
                if nxt not in front_visited:
                    front_visited[nxt] = d + 1
                    front_queue.append(nxt)
        else:
            curr = back_queue.pop(0)
            d = back_visited[curr]
            for nxt in graph.get(curr, []):
                if nxt in front_visited:
                    return d + 1 + front_visited[nxt]
                if nxt not in back_visited:
                    back_visited[nxt] = d + 1
                    back_queue.append(nxt)
                    
    return -1''',
        "category": category
    })

    # 43. Longest Palindromic Subsequence DP
    tasks.append({
        "instruction": "Write a dynamic programming function that returns the length of the longest palindromic subsequence of a string.",
        "output": '''def longest_palindromic_subsequence(s: str) -> int:
    """Calculate length of longest palindromic subsequence using 2D DP table."""
    n = len(s)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = 1
        
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
                
    return dp[0][n - 1]''',
        "category": category
    })

    # 44. Subset Sum DP
    tasks.append({
        "instruction": "Create a subset sum solver in Python that determines whether any subset of non-negative integers sums exactly to target.",
        "output": '''from typing import List

def subset_sum_exists(nums: List[int], target: int) -> bool:
    """Check if there is a subset of nums with sum equal to target."""
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
                
    return dp[target]''',
        "category": category
    })

    # 45. Maximum Product Subarray
    tasks.append({
        "instruction": "Implement a function to find the contiguous subarray within a numeric list which has the largest product.",
        "output": '''from typing import List

def max_product_subarray(nums: List[int]) -> int:
    """Find maximum product of a contiguous non-empty subarray in O(n) time."""
    if not nums:
        return 0
    max_prod = min_prod = global_max = nums[0]
    
    for num in nums[1:]:
        if num < 0:
            max_prod, min_prod = min_prod, max_prod
        max_prod = max(num, max_prod * num)
        min_prod = min(num, min_prod * num)
        global_max = max(global_max, max_prod)
        
    return global_max''',
        "category": category
    })

    # 46. 3-Way QuickSort (Dutch National Flag)
    tasks.append({
        "instruction": "Formulate a 3-way Dutch National Flag partitioning Quicksort algorithm to efficiently handle duplicates.",
        "output": '''from typing import List

def quicksort_3way(arr: List[int]) -> List[int]:
    """Sort list using 3-way partitioning for duplicate efficiency."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quicksort_3way(less) + equal + quicksort_3way(greater)''',
        "category": category
    })

    # 47. Counting Sort
    tasks.append({
        "instruction": "Build an integer counting sort algorithm for non-negative integers bounded by maximum value K.",
        "output": '''from typing import List

def counting_sort(arr: List[int], max_val: int) -> List[int]:
    """Perform stable counting sort on non-negative integers up to max_val."""
    counts = [0] * (max_val + 1)
    for x in arr:
        counts[x] += 1
    output = []
    for val, count in enumerate(counts):
        output.extend([val] * count)
    return output''',
        "category": category
    })

    # 48. Bucket Sort
    tasks.append({
        "instruction": "Develop a bucket sort implementation for sorting floating point numbers uniformly distributed in the interval [0, 1).",
        "output": '''from typing import List

def bucket_sort_floats(arr: List[float], num_buckets: int = 10) -> List[float]:
    """Sort floating point values in [0, 1) using bucket sort."""
    if not arr:
        return []
    buckets: List[List[float]] = [[] for _ in range(num_buckets)]
    for val in arr:
        idx = min(int(val * num_buckets), num_buckets - 1)
        buckets[idx].append(val)
    output = []
    for b in buckets:
        output.extend(sorted(b))
    return output''',
        "category": category
    })

    # 49. Exponential Search
    tasks.append({
        "instruction": "Construct an exponential search function that finds the index of a target key in a sorted list by doubling ranges.",
        "output": '''import bisect
from typing import List

def exponential_search(arr: List[int], target: int) -> int:
    """Locate target index in sorted array using exponential search followed by binary search."""
    if not arr:
        return -1
    if arr[0] == target:
        return 0
    bound = 1
    while bound < len(arr) and arr[bound] <= target:
        bound *= 2
    left = bound // 2
    right = min(bound, len(arr) - 1)
    
    idx = bisect.bisect_left(arr, target, left, right + 1)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1''',
        "category": category
    })

    # 50. Non-recursive Merge Sort
    tasks.append({
        "instruction": "Implement a bottom-up iterative merge sort that sorts a list without using function call recursion.",
        "output": '''from typing import List

def iterative_merge_sort(arr: List[int]) -> List[int]:
    """Sort array iteratively in bottom-up passes without recursion."""
    n = len(arr)
    res = list(arr)
    width = 1
    
    while width < n:
        for i in range(0, n, 2 * width):
            left = res[i: i + width]
            right = res[i + width: min(i + 2 * width, n)]
            merged = []
            l_idx = r_idx = 0
            while l_idx < len(left) and r_idx < len(right):
                if left[l_idx] <= right[r_idx]:
                    merged.append(left[l_idx])
                    l_idx += 1
                else:
                    merged.append(right[r_idx])
                    r_idx += 1
            merged.extend(left[l_idx:])
            merged.extend(right[r_idx:])
            res[i: i + len(merged)] = merged
        width *= 2
        
    return res''',
        "category": category
    })

    # 51. Graph Center Finding
    tasks.append({
        "instruction": "Design an algorithm to find the center vertex (or pair of vertices) of a tree graph by iteratively trimming leaves.",
        "output": '''from typing import Dict, List, Set

def find_tree_centers(adj: Dict[int, List[int]]) -> List[int]:
    """Find the 1 or 2 center nodes minimizing maximum tree eccentricity."""
    n = len(adj)
    if n <= 2:
        return list(adj.keys())
        
    degree = {u: len(neighbors) for u, neighbors in adj.items()}
    leaves = [u for u, d in degree.items() if d == 1]
    remaining = n
    
    while remaining > 2:
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            for neighbor in adj.get(leaf, []):
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    new_leaves.append(neighbor)
        leaves = new_leaves
        
    return leaves''',
        "category": category
    })

    # 52. Uniform Cost Search
    tasks.append({
        "instruction": "Write Uniform Cost Search (Dijkstra on path states) to find the minimum cost action path between graph states.",
        "output": '''import heapq
from typing import Dict, List, Tuple, Optional

def uniform_cost_search(graph: Dict[str, List[Tuple[str, float]]], start: str, goal: str) -> Optional[Tuple[float, List[str]]]:
    """Find path with lowest cumulative action cost using Uniform Cost Search."""
    pq: List[Tuple[float, List[str]]] = [(0.0, [start])]
    visited = {}
    
    while pq:
        cost, path = heapq.heappop(pq)
        curr = path[-1]
        if curr == goal:
            return cost, path
        if curr in visited and visited[curr] <= cost:
            continue
        visited[curr] = cost
        for neighbor, weight in graph.get(curr, []):
            if neighbor not in visited or cost + weight < visited[neighbor]:
                heapq.heappush(pq, (cost + weight, path + [neighbor]))
                
    return None''',
        "category": category
    })

    # 53. Max Independent Set on Tree
    tasks.append({
        "instruction": "Create a tree dynamic programming algorithm that computes the size of the Maximum Independent Set on an undirected tree.",
        "output": '''from typing import Dict, List, Tuple

def max_independent_set_tree(adj: Dict[int, List[int]], root: int = 0) -> int:
    """Calculate maximum number of non-adjacent vertices on a tree."""
    def dp(u: int, parent: int) -> Tuple[int, int]:
        # returns (incl_u, excl_u)
        incl = 1
        excl = 0
        for v in adj.get(u, []):
            if v != parent:
                v_incl, v_excl = dp(v, u)
                incl += v_excl
                excl += max(v_incl, v_excl)
        return incl, excl

    incl, excl = dp(root, -1)
    return max(incl, excl)''',
        "category": category
    })

    # 54. Kosaraju's SCC Algorithm
    tasks.append({
        "instruction": "Build Kosaraju's two-pass DFS algorithm for identifying all strongly connected components in a directed graph.",
        "output": '''from typing import Dict, List, Set

def kosaraju_scc(graph: Dict[str, List[str]]) -> List[List[str]]:
    """Find all strongly connected components using Kosaraju's two-pass DFS."""
    stack: List[str] = []
    visited: Set[str] = set()

    def fill_order(u: str) -> None:
        visited.add(u)
        for v in graph.get(u, []):
            if v not in visited:
                fill_order(v)
        stack.append(u)

    for node in graph:
        if node not in visited:
            fill_order(node)

    # Build transpose graph
    transpose: Dict[str, List[str]] = {n: [] for n in graph}
    for u in graph:
        for v in graph[u]:
            transpose.setdefault(v, []).append(u)

    visited.clear()
    sccs = []

    def dfs_collect(u: str, comp: List[str]) -> None:
        visited.add(u)
        comp.append(u)
        for v in transpose.get(u, []):
            if v not in visited:
                dfs_collect(v, comp)

    while stack:
        u = stack.pop()
        if u not in visited:
            comp: List[str] = []
            dfs_collect(u, comp)
            sccs.append(comp)

    return sccs''',
        "category": category
    })

    # 55. Coin Combinations DP
    tasks.append({
        "instruction": "Formulate a dynamic programming routine to calculate the total number of distinct combinations to form a target amount with coins.",
        "output": '''from typing import List

def coin_combinations_count(coins: List[int], target: int) -> int:
    """Calculate total number of distinct coin combinations that sum to target."""
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for coin in coins:
        for amount in range(coin, target + 1):
            dp[amount] += dp[amount - coin]
            
    return dp[target]''',
        "category": category
    })

    # 56. Dinic's Algorithm Skeleton
    tasks.append({
        "instruction": "Construct a Dinic's blocking flow algorithm to compute maximum bipartite or network flow using layered graphs.",
        "output": '''from collections import deque
from typing import Dict, List

def dinic_max_flow(capacity: Dict[str, Dict[str, int]], src: str, sink: str) -> int:
    """Compute maximum network flow using Dinic's layered BFS and DFS blocking flow."""
    flow: Dict[str, Dict[str, int]] = {u: {v: 0 for v in capacity[u]} for u in capacity}
    level: Dict[str, int] = {}

    def bfs_level() -> bool:
        level.clear()
        level[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v, cap in capacity.get(u, {}).items():
                if cap - flow[u].get(v, 0) > 0 and v not in level:
                    level[v] = level[u] + 1
                    q.append(v)
        return sink in level

    def send_flow(u: str, pushed: int, ptr: Dict[str, int]) -> int:
        if u == sink or pushed == 0:
            return pushed
        neighbors = list(capacity.get(u, {}).keys())
        for i in range(ptr.get(u, 0), len(neighbors)):
            ptr[u] = i
            v = neighbors[i]
            cap = capacity[u][v]
            if level.get(v) == level[u] + 1 and cap - flow[u].get(v, 0) > 0:
                tr = send_flow(v, min(pushed, cap - flow[u][v]), ptr)
                if tr > 0:
                    flow[u][v] += tr
                    flow[v][u] = flow.get(v, {}).get(u, 0) - tr
                    return tr
        return 0

    total_flow = 0
    while bfs_level():
        ptr: Dict[str, int] = {}
        while True:
            pushed = send_flow(src, float("inf"), ptr)
            if pushed == 0:
                break
            total_flow += int(pushed)
    return total_flow''',
        "category": category
    })

    # 57. Graph Diameter via BFS
    tasks.append({
        "instruction": "Engineer a function to compute the diameter (longest shortest-path) of a general unweighted connected graph using all-pairs BFS.",
        "output": '''from collections import deque
from typing import Dict, List

def graph_diameter_bfs(graph: Dict[str, List[str]]) -> int:
    """Compute the maximum shortest path between any two vertices in graph."""
    max_diameter = 0
    
    for start in graph:
        dist = {start: 0}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            d = dist[u]
            max_diameter = max(max_diameter, d)
            for v in graph.get(u, []):
                if v not in dist:
                    dist[v] = d + 1
                    queue.append(v)
                    
    return max_diameter''',
        "category": category
    })

    # 58. Tree Centroid Finder
    tasks.append({
        "instruction": "Develop a tree centroid finding algorithm that locates the vertex whose removal results in components of size at most N/2.",
        "output": '''from typing import Dict, List

def find_tree_centroid(adj: Dict[int, List[int]], root: int = 0) -> int:
    """Locate the centroid of a tree where each subtree size is <= N/2."""
    n = len(adj)
    subtree_size = {}

    def get_sizes(u: int, parent: int) -> int:
        sz = 1
        for v in adj.get(u, []):
            if v != parent:
                sz += get_sizes(v, u)
        subtree_size[u] = sz
        return sz

    get_sizes(root, -1)

    def find_centroid(u: int, parent: int) -> int:
        for v in adj.get(u, []):
            if v != parent and subtree_size[v] > n // 2:
                return find_centroid(v, u)
        return u

    return find_centroid(root, -1)''',
        "category": category
    })

    # 59. Convex Polygon Triangulation Area
    tasks.append({
        "instruction": "Produce a geometric function that computes the area of any convex polygon given its vertices in cyclic order.",
        "output": '''from typing import List, Tuple

def convex_polygon_area(vertices: List[Tuple[float, float]]) -> float:
    """Calculate the area of a polygon using the Shoelace formula."""
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2.0''',
        "category": category
    })

    # 60. Segment Tree Point Update Range Sum
    tasks.append({
        "instruction": "Implement a Segment Tree class supporting O(log n) point updates and O(log n) range sum queries on an array.",
        "output": '''from typing import List

class SegmentTreeRangeSum:
    """Segment Tree for efficient point updates and range sum queries."""
    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(data, 2 * node, start, mid)
        self._build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx: int, value: int, node: int = 1, start: int = 0, end: int = -1) -> None:
        """Update value at index idx."""
        if end == -1: end = self.n - 1
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(idx, value, 2 * node, start, mid)
        else:
            self.update(idx, value, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query_range(self, l: int, r: int, node: int = 1, start: int = 0, end: int = -1) -> int:
        """Return sum of elements in index range [l, r]."""
        if end == -1: end = self.n - 1
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.query_range(l, r, 2 * node, start, mid) + self.query_range(l, r, 2 * node + 1, mid + 1, end)''',
        "category": category
    })

    return tasks
