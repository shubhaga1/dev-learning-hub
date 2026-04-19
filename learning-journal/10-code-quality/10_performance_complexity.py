"""
LEVEL 10 — Performance & Complexity
Senior-level: spot O(n²) loops, redundant DB calls, and memory traps.
This is what separates L5 from L6/L7 reviews.
"""

import time

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

def find_duplicates_bad(items: list) -> list:
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):   # O(n²) — nested loop over same list
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def get_orders_bad(user_ids: list) -> dict:
    result = {}
    for user_id in user_ids:
        # N+1 problem — 1 query per user, 1000 users = 1000 DB round trips
        result[user_id] = db_fetch_orders(user_id)
    return result

def build_report_bad(records: list) -> str:
    report = ""
    for r in records:
        report += f"Record: {r}\n"   # string concatenation in loop = O(n²) memory
    return report


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] find_duplicates: O(n²) nested loop. For 10,000 items = 100M comparisons.
     Use a set for O(n).
[L2] get_orders: N+1 query problem. 1 query per user = death by a thousand DB calls.
     Batch fetch all users in one query.
[L3] build_report: string += in a loop creates a new string each time = O(n²) memory.
     Use list.join() instead.
[L4] These don't fail in tests with 10 items. They fail in prod with 100,000 items.
     Always ask: "What happens at 10x scale?"
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

def find_duplicates(items: list) -> list:
    seen = set()
    duplicates = set()
    for item in items:                    # O(n) — single pass
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)

def get_orders(user_ids: list) -> dict:
    # One batch query instead of N queries
    all_orders = db_fetch_orders_batch(user_ids)    # SELECT * WHERE user_id IN (...)
    return {uid: all_orders.get(uid, []) for uid in user_ids}

def build_report(records: list) -> str:
    return "\n".join(f"Record: {r}" for r in records)  # O(n) — single join


# ─────────────────────────────────────────────────────────
# 🧪 TEST — compare speed
# ─────────────────────────────────────────────────────────

def db_fetch_orders(user_id):       return [f"order_{user_id}_1"]        # mock
def db_fetch_orders_batch(ids):     return {uid: [f"order_{uid}_1"] for uid in ids}  # mock

data = list(range(5000)) + list(range(2500))  # 7500 items, 2500 duplicates

t0 = time.time()
find_duplicates_bad(data)
print(f"Bad  O(n²): {time.time() - t0:.3f}s")

t0 = time.time()
find_duplicates(data)
print(f"Fixed O(n): {time.time() - t0:.3f}s")

# Report building
records = [f"item_{i}" for i in range(10000)]
t0 = time.time(); build_report_bad(records); print(f"String +=  : {time.time()-t0:.3f}s")
t0 = time.time(); build_report(records);     print(f"List join  : {time.time()-t0:.3f}s")
