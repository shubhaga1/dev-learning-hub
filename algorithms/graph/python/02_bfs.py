# ============================================================
# CONCEPT 2: BFS — Breadth First Search
#
# BFS = explore level by level (like ripples in water)
# Best for: MINIMUM NUMBER OF STEPS/HOPS/JUMPS
#
# Uses a QUEUE (first in, first out)
# Why queue? Because you want to process level 1 before level 2
#
# Template:
#   queue = [start]
#   visited = {start}
#   steps = 0
#   while queue:
#       for each node in current level:
#           if node == target: return steps
#           add unvisited neighbors to queue
#       steps += 1
# ============================================================

from collections import deque


# ============================================================
# QUESTION 1: Can you reach the destination?
#
# Graph (directed):
#   0 → 1, 2
#   1 → 3
#   2 → 4
#   3 → 4
#   4 → (nothing)
#
# Using BFS, find if you can reach node 4 from node 0.
# ============================================================
print("QUESTION 1: Can you reach node 4 from node 0?")
print("="*40)

graph = {
    0: [1, 2],
    1: [3],
    2: [4],
    3: [4],
    4: [],
}

def can_reach(graph, start, target):
    queue   = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        print(f"  Visiting: {node}")

        if node == target:
            return True

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False

result = can_reach(graph, 0, 4)
print(f"\nCan reach 4? {result}")

# NUANCE: visited set prevents infinite loops.
# Without it, you'd revisit nodes forever in cycles.


input("\nPress Enter for Question 2...\n")


# ============================================================
# QUESTION 2: Minimum hops to reach destination
#
# Same graph. How many hops (edges) from 0 to 4?
#
# Answer should be 2: 0 → 2 → 4
#
# KEY: BFS explores level by level, so the FIRST TIME
#      you reach a node, that's the shortest path.
# ============================================================
print("QUESTION 2: Minimum hops from 0 to 4")
print("="*40)

def min_hops(graph, start, target):
    queue   = deque([(start, 0)])  # (node, hops_so_far)
    visited = {start}

    while queue:
        node, hops = queue.popleft()
        print(f"  Visiting: {node}  hops so far: {hops}")

        if node == target:
            return hops

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, hops + 1))

    return -1  # not reachable

result = min_hops(graph, 0, 4)
print(f"\nMin hops: {result}")

# NUANCE: We track hops_so_far in the queue alongside the node.
# When we first reach target, that's the minimum — BFS guarantees this.


input("\nPress Enter for Question 3...\n")


# ============================================================
# QUESTION 3: Print the actual path (not just hop count)
#
# Instead of just counting hops, track WHERE WE CAME FROM.
# Use a "parent" dict: parent[node] = node_we_came_from
# Then trace back from target to start.
# ============================================================
print("QUESTION 3: Print the actual shortest path")
print("="*40)

def shortest_path(graph, start, target):
    queue   = deque([start])
    visited = {start}
    parent  = {start: None}   # ← tracks how we got here

    while queue:
        node = queue.popleft()

        if node == target:
            # trace back
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return list(reversed(path))

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node   # ← came from `node`
                queue.append(neighbor)

    return []

path = shortest_path(graph, 0, 4)
print(f"Shortest path: {' → '.join(map(str, path))}")

# NUANCE: parent dict is the key trick for path reconstruction.
# Very common in interviews — always know this.


input("\nPress Enter for Question 4...\n")


# ============================================================
# QUESTION 4: Grid BFS — most common interview form
#
# Given a 4x4 grid. Start at (0,0), reach (3,3).
# '#' = wall (blocked), '.' = open
# Find minimum steps.
#
# grid:
#   . . . .
#   . # # .
#   . # . .
#   . . . .
# ============================================================
print("QUESTION 4: Grid BFS — minimum steps")
print("="*40)

grid = [
    ['.', '.', '.', '.'],
    ['.', '#', '#', '.'],
    ['.', '#', '.', '.'],
    ['.', '.', '.', '.'],
]

def grid_bfs(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    queue   = deque([(start, 0)])
    visited = {start}
    directions = [(0,1),(0,-1),(1,0),(-1,0)]  # right, left, down, up

    while queue:
        (r, c), steps = queue.popleft()

        if (r, c) == target:
            return steps

        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != '#' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), steps + 1))

    return -1

result = grid_bfs(grid, (0,0), (3,3))
print(f"Min steps (0,0) → (3,3): {result}")

print("\n✅ KEY TAKEAWAYS:")
print("  - BFS = min hops (not min cost — that's Dijkstra)")
print("  - Always use a visited set to avoid revisiting")
print("  - Store (node, steps) or (node, path) in queue")
print("  - parent dict = reconstruct path")
print("  - Grid BFS = same idea, neighbors are up/down/left/right")
