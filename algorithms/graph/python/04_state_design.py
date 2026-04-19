# ============================================================
# CONCEPT 4: State Design with Constraints
#
# The hardest part of interview graph problems isn't BFS/Dijkstra.
# It's designing the RIGHT STATE.
#
# State = everything you need to know about "where you are"
#         to make the next decision
#
# Simple BFS state:   node
# With energy limit:  (node, energy_used)
# With used items:    (node, frozenset_of_used_items)
#
# WHY THIS MATTERS:
#   Same node can be visited multiple times with different states.
#   visited = {state}, not just {node}
# ============================================================


# ============================================================
# QUESTION 1: State without constraints (just node)
#
# Graph: 0→1→2→3→4
# Find if you can reach 4 from 0.
# State = just the node number.
# ============================================================
from collections import deque

print("QUESTION 1: Simple state — just the node")
print("="*40)

graph = {0:[1], 1:[2], 2:[3], 3:[4], 4:[]}

queue   = deque([0])
visited = {0}           # state = node

while queue:
    node = queue.popleft()
    if node == 4:
        print("Reached 4!")
        break
    for nb in graph[node]:
        if nb not in visited:
            visited.add(nb)
            queue.append(nb)


input("\nPress Enter for Question 2...\n")


# ============================================================
# QUESTION 2: State WITH energy budget
#
# Graph (weighted):
#   0→1 cost=3, 0→2 cost=1
#   1→4 cost=3, 2→3 cost=1, 3→4 cost=1
#
# Energy budget E=4. Can you reach 4?
#
# WRONG approach: visited = {node}
#   → marks node 1 visited, skips cheaper path through 2,3
#
# RIGHT approach: visited = {(node, energy_used)}
#   → same node can be visited again if we got there cheaper
#
# Actually for "can reach within budget" — just track (node, energy)
# but prune if energy > E
# ============================================================
print("QUESTION 2: State with energy budget")
print("="*40)

graph2 = {
    0: [(1,3),(2,1)],
    1: [(4,3)],
    2: [(3,1)],
    3: [(4,1)],
    4: [],
}
E = 4

# WRONG: visited = set of nodes
# RIGHT: visited = set of (node, energy) — but that explodes
# BETTER: dist[node] = min energy seen so far (prune if worse)

dist  = {0: 0}
queue = deque([(0, 0)])   # (node, energy_used)

reached = False
while queue:
    node, energy = queue.popleft()

    if node == 4:
        print(f"Reached 4 with energy={energy} ✅")
        reached = True
        break

    for nb, cost in graph2[node]:
        new_energy = energy + cost
        if new_energy <= E and new_energy < dist.get(nb, float('inf')):
            dist[nb] = new_energy
            queue.append((nb, new_energy))

if not reached:
    print("Cannot reach 4 within budget")

# Path: 0→2→3→4 = 1+1+1 = 3 ≤ 4 ✅
# Path: 0→1→4   = 3+3=6 > 4 ❌


input("\nPress Enter for Question 3...\n")


# ============================================================
# QUESTION 3: State WITH used items (like unstable stones)
#
# Graph: 0→1→2→3→4
# Node 2 is "one-time-use" — can only land on it ONCE.
#
# Without this constraint, path is: 0→1→2→3→4
# Suppose there's also 0→3 directly.
#
# PROBLEM: how do we track "have I used node 2 already?"
#
# ANSWER: include it in the state!
#   state = (node, frozenset_of_used_onetime_nodes)
#
# visited = set of states, not just nodes
# ============================================================
print("QUESTION 3: State with used one-time nodes")
print("="*40)

graph3 = {0:[1,3], 1:[2], 2:[3], 3:[4], 4:[]}
one_time = {2}    # node 2 can only be visited once

# State = (current_node, frozenset of used one-time nodes)
start_state = (0, frozenset())
queue   = deque([(start_state, [0])])   # (state, path)
visited = {start_state}

paths_found = []
while queue:
    (node, used), path = queue.popleft()

    if node == 4:
        paths_found.append(path)
        continue

    for nb in graph3[node]:
        # can we visit nb?
        if nb in one_time and nb in used:
            print(f"  Skipping {nb} — already used (one-time node)")
            continue

        new_used  = used | {nb} if nb in one_time else used
        new_state = (nb, new_used)

        if new_state not in visited:
            visited.add(new_state)
            queue.append((new_state, path + [nb]))

print(f"\nAll paths to 4:")
for p in paths_found:
    print(f"  {' → '.join(map(str, p))}")

# NUANCE: Same node can appear in multiple states.
# (node=2, used={}) ≠ (node=2, used={2})
# visited must track the FULL STATE, not just the node.


input("\nPress Enter for Question 4...\n")


# ============================================================
# QUESTION 4: Combining both — energy + used items
#
# This is exactly what river crossing needs.
# State = (node, energy_used, frozenset_of_used_unstable)
#
# Let's build a minimal version:
# Nodes: 0,1,2,3,4
# Node 2 = one-time-use
# Edges (directed, weighted):
#   0→1: cost=4, 0→2: cost=1
#   1→4: cost=4, 2→3: cost=1, 3→4: cost=9
# Budget E=12
#
# Can we reach 4?
# ============================================================
print("QUESTION 4: Energy budget + one-time nodes combined")
print("="*40)

graph4 = {
    0: [(1,4),(2,1)],
    1: [(4,4)],
    2: [(3,1)],
    3: [(4,9)],
    4: [],
}
one_time4 = {2}
E4 = 12

# State = (node, energy_used, frozenset_of_used_one_time)
start = (0, 0, frozenset())
queue   = deque([(start, [0])])
visited = {start}

result = None
while queue:
    (node, energy, used), path = queue.popleft()

    if node == 4:
        result = (path, energy)
        break

    for nb, cost in graph4[node]:
        if nb in one_time4 and nb in used:
            continue

        new_energy = energy + cost
        if new_energy > E4:
            continue                     # prune — over budget

        new_used  = used | {nb} if nb in one_time4 else used
        new_state = (nb, new_energy, new_used)

        if new_state not in visited:
            visited.add(new_state)
            queue.append((new_state, path + [nb]))

if result:
    path, energy = result
    print(f"Path: {' → '.join(map(str, path))}")
    print(f"Energy used: {energy} (budget: {E4})")
else:
    print("Not reachable within budget")

print("\n✅ KEY TAKEAWAYS:")
print("  - State = everything needed to make the next decision")
print("  - Simple graph: state = node")
print("  - With budget:  state = (node, cost_so_far)")
print("  - With one-time items: state = (node, frozenset_used)")
print("  - Combined:     state = (node, cost, frozenset_used)")
print("  - visited = set of STATES, not just nodes")
print("  - This is EXACTLY what river crossing needs!")
