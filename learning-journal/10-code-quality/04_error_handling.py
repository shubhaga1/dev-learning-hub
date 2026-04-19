"""
LEVEL 4 — Error Handling
Don't swallow exceptions. Don't catch everything. Fail loud and specific.
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

def get_user(user_id):
    try:
        # simulated DB fetch
        users = {"u1": {"name": "Alice", "age": 28}}
        return users[user_id]
    except:
        return None

def divide(a, b):
    try:
        return a / b
    except Exception as e:
        print("Error:", e)
        return 0

result = get_user("u99")
print(result.get("name"))  # AttributeError hidden — crashes with unclear message


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] bare `except:` catches EVERYTHING — including KeyboardInterrupt, SystemExit.
     This can hide crashes and make code impossible to stop.
[L2] return None from get_user forces every caller to do a None check.
     If they forget, they get AttributeError somewhere else — hard to trace.
[L3] divide() returning 0 on error is silent corruption — caller thinks result is 0.
[L4] print("Error:", e) — logs to stdout, not a logger. Lost in production.
[L5] Catching Exception is too broad — only catch what you expect and can handle.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

class UserNotFoundError(Exception):
    pass

def get_user(user_id: str) -> dict:
    users = {"u1": {"name": "Alice", "age": 28}}
    if user_id not in users:
        raise UserNotFoundError(f"User '{user_id}' not found")
    return users[user_id]

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Denominator cannot be zero")
    return a / b

# Caller handles explicitly
try:
    user = get_user("u99")
    print(user["name"])
except UserNotFoundError as e:
    print(f"Handled: {e}")  # clear, specific, traceable

try:
    print(divide(10, 0))
except ValueError as e:
    print(f"Handled: {e}")

# ─────────────────────────────────────────────────────────
# 🧪 TEST
# ─────────────────────────────────────────────────────────

print(get_user("u1"))     # works
print(divide(10, 2))      # 5.0
