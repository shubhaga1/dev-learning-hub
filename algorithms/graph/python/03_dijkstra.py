# ============================================================
# CONCEPT 3: Dijkstra's Algorithm
#
# BFS finds min HOPS. Dijkstra finds min COST.
#
# Why not BFS? BFS treats all edges as equal weight.
# If edges have different costs, BFS picks wrong path.
#
# Dijkstra uses a MIN-HEAP (priority queue):
#   → always process the CHEAPEST node next
#   → guarantees shortest cost when you first reach a node
#
# Template:
#   heap = [(0, start)]       ← (cost, node)
#   dist = {start: 0}
#   while heap:
#       cost, node = heappop(heap)
#       if node == target: return cost
#       for neighbor, edge_cost in graph[node]:
#           new_cost = cost + edge_cost
#           if new_cost < dist.get(neighbor, inf):
#               dist[neighbor] = new_cost
#               heappush(heap, (new_cost, neighbor))
# ============================================================

import heapq


# ============================================================
# QUESTION 1: Why BFS fails with weights
#
# Graph:
#   0 → 1, cost=10
#   0 → 2, cost=1
#   2 → 1, cost=1
#
# Shortest hops from 0 to 1? → 1 hop (direct)
# Cheapest cost  from 0 to 1? → 2 (0→2→1 costs 1+1=2)
#
# BFS would say 1 hop = direct path. WRONG for cost.
# ============================================================
print("QUESTION 1: Why BFS gives wrong cost")
print("="*40)

graph = {
    0: [(1, 10), (2, 1)],
    1: [],
    2: [(1, 1)],
}

# BFS answer (fewest hops)
print("BFS sees:")
print("  0 → 1 directly = 1 hop, cost=10")
print("  0 → 2 → 1      = 2 hops, cost=2")
print("  BFS picks: 0→1 (fewest hops) ← WRONG if you want min cost")

# Dijkstra answer (min cost)
print("\nDijkstra picks: 0→2→1 (min cost = 2) ← CORRECT")

# KEY INSIGHT: Use BFS for min hops, Dijkstra for min cost.

input("\nPress Enter for Question 2...\n")


# ============================================================
# QUESTION 2: Implement Dijkstra
#
# Graph (directed, weighted):
#   0 → 1: 4
#   0 → 2: 1
#   2 → 3: 2
#   1 → 3: 1
#   3 → 4: 5
#
# Find cheapest cost from 0 to 4.
# Answer: 0→2→3→4 = 1+2+5 = 8
# ============================================================
print("QUESTION 2: Dijkstra — find cheapest cost")
print("="*40)

graph2 = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(3, 2)],
    3: [(4, 5)],
    4: [],
}

def dijkstra(graph, start, target):
    heap = [(0, start)]           # (cost_so_far, node)
    dist = {start: 0}             # cheapest known cost to each node

    while heap:
        cost, node = heapq.heappop(heap)
        print(f"  Processing: node={node}  cost={cost}")

        if node == target:
            return cost

        # skip if we already found a cheaper path
        if cost > dist.get(node, float('inf')):
            continue

        for neighbor, edge_cost in graph[node]:
            new_cost = cost + edge_cost
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))

    return -1

result = dijkstra(graph2, 0, 4)
print(f"\nCheapest cost 0→4: {result}")

# NUANCE: The "skip stale entries" check is critical.
# Heap can have outdated entries — always check if cost > dist[node]


input("\nPress Enter for Question 3...\n")


# ============================================================
# QUESTION 3: Dijkstra with path reconstruction
#
# Same graph. Return the actual path, not just cost.
# ============================================================
print("QUESTION 3: Dijkstra — return actual path")
print("="*40)

def dijkstra_path(graph, start, target):
    heap   = [(0, start)]
    dist   = {start: 0}
    parent = {start: None}

    while heap:
        cost, node = heapq.heappop(heap)

        if node == target:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return list(reversed(path)), cost

        if cost > dist.get(node, float('inf')):
            continue

        for neighbor, edge_cost in graph[node]:
            new_cost = cost + edge_cost
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor]   = new_cost
                parent[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    return [], -1

path, cost = dijkstra_path(graph2, 0, 4)
print(f"Path: {' → '.join(map(str, path))}")
print(f"Cost: {cost}")


input("\nPress Enter for Question 4...\n")


# ============================================================
# QUESTION 4: BFS vs Dijkstra — when to use which?
#
# You have a maze. Each step costs:
#   - Moving on road   → cost 1
#   - Moving on grass  → cost 3
#
# Find cheapest path from S to E.
#
# grid:
#   S  road  road
#   grass grass road
#   grass grass  E
#
# costs: road=1, grass=3
# ============================================================
print("QUESTION 4: Grid Dijkstra (weighted cells)")
print("="*40)

grid = [
    ['S',    'road', 'road'],
    ['grass','grass','road'],
    ['grass','grass','E'   ],
]

cell_cost = {'road': 1, 'grass': 3, 'S': 0, 'E': 0}

def grid_dijkstra(grid):
    rows, cols = len(grid), len(grid[0])
    heap = [(0, 0, 0)]        # (cost, row, col)
    dist = {(0,0): 0}
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while heap:
        cost, r, c = heapq.heappop(heap)

        if grid[r][c] == 'E':
            return cost

        if cost > dist.get((r,c), float('inf')):
            continue

        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + cell_cost[grid[nr][nc]]
                if new_cost < dist.get((nr,nc), float('inf')):
                    dist[(nr,nc)] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))

    return -1

result = grid_dijkstra(grid)
print(f"Cheapest path S→E: {result}")

print("\n✅ KEY TAKEAWAYS:")
print("  - BFS   → min hops  (all edges equal weight)")
print("  - Dijkstra → min cost (edges have different weights)")
print("  - Both use visited/dist to avoid reprocessing")
print("  - Dijkstra uses MIN-HEAP, BFS uses plain QUEUE")
print("  - In river crossing: cost = dist^2 → use Dijkstra for min energy")
print("                       jumps = hops  → use BFS for min jumps")
print("  - We need BOTH → modified approach (Step 4 of river crossing)")
