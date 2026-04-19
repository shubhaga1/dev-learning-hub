# ============================================================
# CONCEPT 1: Graphs
#
# A graph = nodes (places) + edges (connections between them)
#
# Real examples:
#   - Cities connected by roads
#   - People connected by friendships
#   - Stones connected by possible jumps ← our problem
#
# Two ways to store a graph:
#   1. Adjacency Matrix  → 2D array, graph[i][j] = 1 if connected
#   2. Adjacency List    → dict, graph[node] = [list of neighbors]
#
# We'll use adjacency LIST — more common in interviews
# ============================================================


# ============================================================
# QUESTION 1: Build the graph
#
# You have 5 cities: 0, 1, 2, 3, 4
# Roads (edges):
#   0 — 1
#   0 — 2
#   1 — 3
#   2 — 3
#   3 — 4
#
# Build an adjacency list for this graph.
# Print all neighbors of each city.
# ============================================================
print("QUESTION 1: Build adjacency list")
print("="*40)

# YOUR TURN: build the graph dict here
# graph = {
#     0: [...],
#     ...
# }

# ANSWER ↓ (try yourself first!)
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2, 4],
    4: [3],
}

for city, neighbors in graph.items():
    print(f"  City {city} → connects to {neighbors}")

# NUANCE: This is an UNDIRECTED graph — if 0→1 exists, 1→0 must too.
# In a DIRECTED graph (like our river crossing), 0→1 doesn't mean 1→0.


input("\nPress Enter for Question 2...\n")


# ============================================================
# QUESTION 2: Directed graph (one-way roads)
#
# Build a DIRECTED graph from these one-way roads:
#   0 → 1
#   0 → 2
#   1 → 3
#   3 → 4
#
# Notice: you can go 0→1 but NOT 1→0
#
# Print all neighbors. Then answer:
#   Can you go from 2 to 4?
# ============================================================
print("QUESTION 2: Directed graph (one-way)")
print("="*40)

directed = {
    0: [1, 2],
    1: [3],
    2: [],      # ← 2 has no outgoing edges! dead end
    3: [4],
    4: [],
}

for node, neighbors in directed.items():
    print(f"  {node} → {neighbors}")

print("\nCan you go from 2 to 4?", "NO — 2 is a dead end" if not directed[2] else "YES")

# NUANCE: In our river crossing, jumps are one-way (forward only).
# You can't jump backwards. So it's a directed graph.


input("\nPress Enter for Question 3...\n")


# ============================================================
# QUESTION 3: Weighted graph
#
# Same directed graph, but now each edge has a COST (weight).
# Store as: graph[from] = [(to, cost), ...]
#
# Roads with costs:
#   0 → 1, cost = 4
#   0 → 2, cost = 1
#   2 → 3, cost = 2
#   1 → 3, cost = 1
#   3 → 4, cost = 5
#
# Print each road with its cost.
# Then manually find: cheapest path from 0 to 4?
# ============================================================
print("QUESTION 3: Weighted graph (edges have costs)")
print("="*40)

weighted = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(3, 2)],
    3: [(4, 5)],
    4: [],
}

for node, edges in weighted.items():
    for (to, cost) in edges:
        print(f"  {node} → {to}  cost={cost}")

print("\nPath 0→1→3→4: cost =", 4+1+5, "= 10")
print("Path 0→2→3→4: cost =", 1+2+5, "=  8  ← cheaper!")

# NUANCE: In our river crossing, cost = distance^2
# That's the weight on each edge.

print("\n✅ KEY TAKEAWAYS:")
print("  - Undirected: both directions exist")
print("  - Directed: one-way only (our problem)")
print("  - Weighted: edges have costs (energy in our problem)")
print("  - Adjacency list: graph[node] = [neighbors] or [(neighbor, cost)]")
