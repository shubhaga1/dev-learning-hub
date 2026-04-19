# ============================================================
# TRADITIONAL WAY — app runs directly on the host machine
# ============================================================
#
# Your Machine (macOS)
# ├── OS (macOS)
# ├── Python 3.9
# └── app.py  ← runs here directly
#
# Problem:
#   - Works on your machine, breaks on someone else's
#   - Python version mismatch
#   - Library version conflicts
#   - Can't run two apps needing different Python versions
# ============================================================

def greet(name):
    return f"Hello, {name}! Running the traditional way."

print(greet("Shubham"))
print("Python runs directly on your OS — no isolation!")
