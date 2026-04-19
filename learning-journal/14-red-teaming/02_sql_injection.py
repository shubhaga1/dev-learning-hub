"""
SQL INJECTION — the #1 web vulnerability for 20+ years

An attacker controls input that gets embedded directly into a SQL query.
The DB can't tell "user data" from "SQL commands" → attacker owns the query.

HOW IT WORKS:
  App builds query by string concatenation:
    "SELECT * FROM users WHERE name = '" + username + "'"

  Attacker enters:  ' OR '1'='1
  Query becomes:    SELECT * FROM users WHERE name = '' OR '1'='1'
  '1'='1' is always true → returns ALL users

  Attacker enters:  admin'--
  Query becomes:    SELECT * FROM users WHERE name = 'admin'--' AND password='...'
  -- comments out the password check → login as admin with no password

SEVERITY: Critical — can dump entire DB, bypass auth, delete data, run OS commands
"""

import sqlite3, os

DB = "/tmp/redteam_demo.db"

def setup_db():
    conn = sqlite3.connect(DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        );
        DELETE FROM users;
        INSERT INTO users VALUES (1,'alice','s3cr3t','user');
        INSERT INTO users VALUES (2,'bob','hunter2','user');
        INSERT INTO users VALUES (3,'admin','sup3radmin','admin');
    """)
    conn.commit()
    return conn

# ── VULNERABLE: string concatenation ─────────────────────────────────────────
def login_vulnerable(username, password):
    conn = sqlite3.connect(DB)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"  SQL: {query}")
    rows = conn.execute(query).fetchall()
    conn.close()
    return rows

# ── SECURE: parameterized query ───────────────────────────────────────────────
def login_secure(username, password):
    conn = sqlite3.connect(DB)
    query = "SELECT * FROM users WHERE username=? AND password=?"
    print(f"  SQL: {query}  params=({username!r}, {password!r})")
    rows = conn.execute(query, (username, password)).fetchall()
    conn.close()
    return rows

# ── Demo ──────────────────────────────────────────────────────────────────────
setup_db()
print("=== ATTACK 1: bypass password check ===")
payload = "admin'--"
print(f"  Input username: {payload!r}  password: 'anything'")
result = login_vulnerable(payload, "anything")
print(f"  Result: {result}  ← logged in as admin with wrong password!\n")

print("=== ATTACK 2: OR 1=1 — dump all users ===")
payload = "' OR '1'='1"
print(f"  Input username: {payload!r}")
result = login_vulnerable(payload, "x")
print(f"  Result: {result}  ← ALL rows returned!\n")

print("=== ATTACK 3: UNION-based data extraction ===")
# Attacker discovers column count, then appends a UNION SELECT
payload = "x' UNION SELECT id,username,password,role FROM users--"
print(f"  Input username: {payload!r}")
result = login_vulnerable(payload, "x")
print(f"  Result: {result}  ← full user table dumped via UNION!\n")

print("=== SECURE: same attacks fail with parameterized query ===")
for payload in ["admin'--", "' OR '1'='1", "x' UNION SELECT 1,2,3,4--"]:
    result = login_secure(payload, "anything")
    short  = repr(payload)[:35]
    print(f"  {short} → {result}  ← no result, attack failed")

print("""
WHY PARAMETERIZED QUERIES WORK:
  - DB compiles the query FIRST (with ? placeholders)
  - User input is sent separately as DATA, never parsed as SQL
  - ' in the input is treated as a literal character, not a SQL delimiter

OTHER DEFENSES (defense in depth):
  - Least privilege: app DB user can only SELECT/INSERT, not DROP/UPDATE other tables
  - WAF: block common SQLi patterns (imperfect, easy to bypass)
  - Error handling: never show DB errors to users
  - ORM: SQLAlchemy, Hibernate etc. parameterize by default
""")
os.unlink(DB)
