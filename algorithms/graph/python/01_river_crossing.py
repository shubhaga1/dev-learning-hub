# ============================================================
# PROBLEM: Constrained River Crossing
#
# You're at stone[0] = 0, want to reach stone[-1] = N
# Each jump costs energy = (distance)^2
# Unstable stones can only be visited once
# Goal: min jumps to reach N, within energy budget E
#
# WE WILL SOLVE THIS IN 4 STEPS:
#   STEP 1 — Understand the problem, print all valid jumps
#   STEP 2 — BFS (ignore energy + unstable for now)
#   STEP 3 — Add energy constraint
#   STEP 4 — Add unstable stone tracking → full solution
# ============================================================

N      = 25
stones = [0, 3, 5, 9, 10, 14, 17, 21, 25]
types  = ['S','S','U','S','S','U','S','S','S']
K      = 10   # max jump distance
E      = 150  # energy budget

# ============================================================
# STEP 1: Understand the problem
# → Print every valid jump from each stone
# → A jump from i to j is valid if: 1 ≤ stones[j]-stones[i] ≤ K
# ============================================================
print("STEP 1: What jumps are even possible?")
print("="*50)

for i in range(len(stones)):
    for j in range(i+1, len(stones)):
        dist   = stones[j] - stones[i]
        cost   = dist ** 2
        stable = "STABLE" if types[j] == 'S' else "UNSTABLE"

        if dist <= K:
            print(f"  {stones[i]:>2} → {stones[j]:>2}  |  dist={dist}  cost={cost:>3}  landing={stable}")
        else:
            break  # stones are sorted, no point checking further

print()
print("KEY INSIGHT:")
print("  - We want fewest jumps (like BFS layers)")
print("  - But total cost must stay ≤", E)
print("  - And unstable stones can only be used once")
print()
print("NEXT: Run STEP 2 — we'll add BFS to find shortest path")
