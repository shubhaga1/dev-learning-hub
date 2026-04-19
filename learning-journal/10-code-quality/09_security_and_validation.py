"""
LEVEL 9 — Security: Input Validation & Injection Prevention
Never trust input. Validate at system boundaries. Sanitize before use.
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

import sqlite3

def get_user_by_name_bad(name: str):
    conn = sqlite3.connect(":memory:")
    # SQL INJECTION — attacker passes: name = "' OR '1'='1"
    query = f"SELECT * FROM users WHERE name = '{name}'"
    return conn.execute(query).fetchall()

def create_user_bad(data: dict):
    # No validation — what if age = -999 or email = "not-an-email"?
    print(f"Creating user: {data['name']}, age={data['age']}, email={data['email']}")


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] String interpolation in SQL = SQL injection vulnerability.
     Input "'; DROP TABLE users; --" deletes the entire table.
[L2] No validation on create_user — age can be negative, email invalid, name empty.
[L3] Exposing raw DB errors to users leaks schema information.
[L4] Never use f-strings / string concat for SQL — always use parameterized queries.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

import re

def get_user_by_name(conn: sqlite3.Connection, name: str) -> list:
    # Parameterized query — DB driver handles escaping, injection impossible
    return conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()

def validate_user(data: dict) -> list[str]:
    errors = []
    if not data.get("name") or len(data["name"].strip()) < 2:
        errors.append("Name must be at least 2 characters")
    if not isinstance(data.get("age"), int) or not (0 < data["age"] < 130):
        errors.append("Age must be between 1 and 129")
    if not re.match(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", data.get("email", "")):
        errors.append("Invalid email format")
    return errors

def create_user(data: dict):
    errors = validate_user(data)
    if errors:
        raise ValueError(f"Invalid user data: {errors}")
    print(f"Creating user: {data}")


# ─────────────────────────────────────────────────────────
# 🧪 TEST
# ─────────────────────────────────────────────────────────

# SQL injection attempt — safe with parameterized query
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, age INTEGER)")
conn.execute("INSERT INTO users VALUES ('Alice', 30)")
print(get_user_by_name(conn, "' OR '1'='1"))  # returns [] — injection blocked

# Validation
try:
    create_user({"name": "A", "age": -5, "email": "bad"})
except ValueError as e:
    print(e)

create_user({"name": "Alice", "age": 30, "email": "alice@example.com"})  # works
