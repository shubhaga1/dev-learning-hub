"""
POC 1 — Schema, Types, Fields, Arguments, Queries

Key concepts from GitHub docs:
  Schema     — defines ALL possible data and relationships
  Type       — an object with fields (like a class)
  Field      — a unit of data on a type
  Argument   — filter/param attached to a field
  Scalar     — leaf value (String, Int, Boolean) — queries must resolve to these

No server needed — strawberry executes queries directly in-process.

Run: python3 01_schema_and_queries.py
"""

import strawberry
from typing import Optional
import json

SEP = "-" * 55


# ═══════════════════════════════════════════════════════════
# SCHEMA DEFINITION
# This is the "contract" — what clients can query
# ═══════════════════════════════════════════════════════════

@strawberry.type
class Author:
    id:       int
    name:     str
    country:  str


@strawberry.type
class Book:
    id:       int
    title:    str
    year:     int
    rating:   float
    author:   Author          # nested type — relationship between nodes


# In-memory data (pretend DB)
AUTHORS = {
    1: Author(id=1, name="Martin Kleppmann",  country="UK"),
    2: Author(id=2, name="Andrew Tanenbaum",  country="Netherlands"),
    3: Author(id=3, name="Robert Sedgewick",  country="USA"),
}

BOOKS = [
    Book(id=1, title="Designing Data-Intensive Applications", year=2017, rating=4.9, author=AUTHORS[1]),
    Book(id=2, title="Computer Networks",                     year=2010, rating=4.7, author=AUTHORS[2]),
    Book(id=3, title="Algorithms",                            year=2011, rating=4.8, author=AUTHORS[3]),
    Book(id=4, title="Modern Operating Systems",              year=2014, rating=4.6, author=AUTHORS[2]),
]


# ── Query type — defines what clients can ask for ──────────────────────────────

@strawberry.type
class Query:

    @strawberry.field
    def books(self) -> list[Book]:
        """Return all books."""
        return BOOKS

    @strawberry.field
    def book(self, id: int) -> Optional[Book]:
        """Return one book by ID. Argument: id (Int)"""
        return next((b for b in BOOKS if b.id == id), None)

    @strawberry.field
    def books_by_author(self, author_id: int) -> list[Book]:
        """Return books filtered by author. Argument: author_id (Int)"""
        return [b for b in BOOKS if b.author.id == author_id]

    @strawberry.field
    def top_rated(self, min_rating: float = 4.7) -> list[Book]:
        """Return books above a rating threshold. Argument with default."""
        return [b for b in BOOKS if b.rating >= min_rating]


schema = strawberry.Schema(query=Query)


# ── Helper to print results cleanly ───────────────────────────────────────────

def run(label: str, query: str) -> None:
    print(f"\n{SEP}")
    print(f"QUERY: {label}")
    print(SEP)
    print(query.strip())
    result = schema.execute_sync(query)
    if result.errors:
        print(f"ERRORS: {result.errors}")
    else:
        print(f"\nRESULT:")
        print(json.dumps(result.data, indent=2))


# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 55)
    print("GraphQL POC 1 — Schema, Fields, Arguments")
    print("=" * 55)

    # ── 1. Get all books — only ask for fields you need ───────────────────────
    # REST would return the whole object. GraphQL returns EXACTLY what you ask.
    run("All books (title + year only)", """
        query {
          books {
            title
            year
          }
        }
    """)

    # ── 2. Nested field — traverse the relationship to Author ─────────────────
    # One query, two types. REST would need two API calls.
    run("Books with nested author (one query, two types)", """
        query {
          books {
            title
            rating
            author {
              name
              country
            }
          }
        }
    """)

    # ── 3. Argument — fetch one book by ID ────────────────────────────────────
    run("Single book by ID (argument: id=1)", """
        query {
          book(id: 1) {
            title
            year
            author {
              name
            }
          }
        }
    """)

    # ── 4. Filter argument ────────────────────────────────────────────────────
    run("Books by author (argument: authorId=2)", """
        query {
          booksByAuthor(authorId: 2) {
            title
            year
          }
        }
    """)

    # ── 5. Argument with default ──────────────────────────────────────────────
    run("Top rated books (argument with default: minRating=4.8)", """
        query {
          topRated(minRating: 4.8) {
            title
            rating
          }
        }
    """)

    # ── 6. Ask for a non-existent field → schema validation error ─────────────
    run("Invalid field → schema rejects it", """
        query {
          books {
            title
            nonExistentField
          }
        }
    """)

    print(f"\n{SEP}")
    print("KEY INSIGHT")
    print(SEP)
    print("""
  REST:    GET /books           → returns ALL fields, always
  GraphQL: query { books { title } } → returns ONLY title

  REST:    GET /books + GET /authors/{id}  → 2 round trips
  GraphQL: books { title author { name } } → 1 query, 2 types

  Schema validates EVERY query before executing.
  Ask for a field that doesn't exist → error before hitting DB.
    """)
