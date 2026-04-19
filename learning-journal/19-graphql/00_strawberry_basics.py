"""
Strawberry — what it is and how to test it, from scratch.

Strawberry is a Python library that:
  1. Takes your Python classes + type hints
  2. Converts them into a GraphQL schema automatically
  3. Executes GraphQL queries against that schema

No separate .graphql file needed.
No HTTP server needed to test — execute queries directly in Python.

Run: python3 00_strawberry_basics.py

install: pip install strawberry-graphql
"""

import strawberry
import json
from typing import Optional

SEP = "-" * 50


# ═══════════════════════════════════════════════════════════
# STEP 1 — The absolute minimum Strawberry program
# ═══════════════════════════════════════════════════════════

# @strawberry.type  → "this Python class is a GraphQL type"
@strawberry.type
class Query:

    # @strawberry.field → "this method is a GraphQL field"
    # The return type hint (-> str) becomes the GraphQL field type
    @strawberry.field
    def hello(self) -> str:
        return "world"


# Build the schema from the Query class
schema = strawberry.Schema(query=Query)

# Execute a GraphQL query string directly — no HTTP, no server
result = schema.execute_sync("{ hello }")

print("STEP 1 — minimum program")
print(f"  query:  {{ hello }}")
print(f"  result: {result.data}")          # {'hello': 'world'}
print(f"  errors: {result.errors}")        # None


# ═══════════════════════════════════════════════════════════
# STEP 2 — What Strawberry auto-generates (the schema)
# ═══════════════════════════════════════════════════════════
#
# From the Python class above, Strawberry creates this GraphQL schema:
#
#   type Query {
#     hello: String!
#   }
#
# You never write this by hand. Strawberry derives it from:
#   @strawberry.type  →  type Query { }
#   -> str            →  String!       (! = non-nullable, from Python's str)
#   def hello         →  hello field

print(f"\n{SEP}")
print("STEP 2 — See the auto-generated GraphQL schema")
print(SEP)
print(schema.as_str())                      # prints the actual SDL (Schema Definition Language)


# ═══════════════════════════════════════════════════════════
# STEP 3 — Add a real type with fields
# ═══════════════════════════════════════════════════════════

@strawberry.type
class User:
    id:    int       # → Int!   in GraphQL
    name:  str       # → String! in GraphQL
    email: str       # → String! in GraphQL


# In-memory data
USERS = [
    User(id=1, name="Shubham", email="shubham@example.com"),
    User(id=2, name="Alice",   email="alice@example.com"),
]

@strawberry.type
class Query2:

    @strawberry.field
    def users(self) -> list[User]:           # → [User!]! in GraphQL
        return USERS

    @strawberry.field
    def user(self, id: int) -> Optional[User]:  # argument + nullable return
        return next((u for u in USERS if u.id == id), None)


schema2 = strawberry.Schema(query=Query2)

print(f"\n{SEP}")
print("STEP 3 — Real type with fields")
print(SEP)
print("Auto-generated schema:")
print(schema2.as_str())

r = schema2.execute_sync("{ users { id name } }")
print(f"\nquery: {{ users {{ id name }} }}")
print(f"result: {json.dumps(r.data, indent=2)}")

r2 = schema2.execute_sync("{ user(id: 1) { name email } }")
print(f"\nquery: {{ user(id: 1) {{ name email }} }}")
print(f"result: {json.dumps(r2.data, indent=2)}")


# ═══════════════════════════════════════════════════════════
# STEP 4 — How to TEST (without running a server)
# ═══════════════════════════════════════════════════════════
#
# Two ways to test:
#   A. execute_sync()  — simplest, used in all these POC files
#   B. TestClient      — strawberry's built-in test helper (same as execute_sync but structured)

print(f"\n{SEP}")
print("STEP 4 — How to test GraphQL queries")
print(SEP)

# Method A — execute_sync (what we've been using)
def test_query_returns_all_users():
    result = schema2.execute_sync("{ users { id name } }")
    assert result.errors is None,          f"unexpected errors: {result.errors}"
    assert len(result.data["users"]) == 2, f"expected 2 users, got {len(result.data['users'])}"
    assert result.data["users"][0]["name"] == "Shubham"
    print("  ✓ test_query_returns_all_users passed")

def test_user_by_id():
    result = schema2.execute_sync("{ user(id: 2) { name } }")
    assert result.errors is None
    assert result.data["user"]["name"] == "Alice"
    print("  ✓ test_user_by_id passed")

def test_user_not_found_returns_null():
    result = schema2.execute_sync("{ user(id: 999) { name } }")
    assert result.errors is None
    assert result.data["user"] is None        # nullable field → None, not error
    print("  ✓ test_user_not_found_returns_null passed")

def test_invalid_field_returns_error():
    result = schema2.execute_sync("{ users { nonExistent } }")
    assert result.errors is not None          # schema caught the bad field
    print("  ✓ test_invalid_field_returns_error passed")

test_query_returns_all_users()
test_user_by_id()
test_user_not_found_returns_null()
test_invalid_field_returns_error()


# ═══════════════════════════════════════════════════════════
# STEP 5 — Strawberry vs writing GraphQL by hand
# ═══════════════════════════════════════════════════════════

print(f"\n{SEP}")
print("STEP 5 — Why Strawberry, not raw GraphQL")
print(SEP)
print("""
  WITHOUT Strawberry (raw graphene or hand-written):
    # schema.graphql
    type User {
      id: Int!
      name: String!
    }
    type Query {
      user(id: Int!): User
    }

    # resolvers.py (separate file, must match schema exactly)
    def resolve_user(root, info, id):
      ...

    Two files to keep in sync. Type errors caught at runtime.

  WITH Strawberry:
    @strawberry.type
    class User:
      id:   int
      name: str

    @strawberry.type
    class Query:
      @strawberry.field
      def user(self, id: int) -> User | None: ...

    One file. Type errors caught by Python type checker (mypy/pyright).
    Schema generated automatically from the Python types.
""")
