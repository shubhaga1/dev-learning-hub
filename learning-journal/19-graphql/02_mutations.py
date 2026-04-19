"""
POC 2 — Mutations (write operations)

Mutations = anything that changes data (create, update, delete).
In GraphQL mutations are explicit — the schema separates reads (Query)
from writes (Mutation). You always know what's side-effectful.

Mutation pattern:
  mutation {
    addBook(input: { title: "...", year: 2024, ... }) {
      id
      title
    }
  }

Run: python3 02_mutations.py
"""

import strawberry
from typing import Optional
import json

SEP = "-" * 55


# ── Types ─────────────────────────────────────────────────────────────────────

@strawberry.type
class Book:
    id:     int
    title:  str
    year:   int
    rating: float


# Input type — argument object for mutations
# Mutations take an INPUT type (not a plain type) — GraphQL spec
@strawberry.input
class BookInput:
    title:  str
    year:   int
    rating: float


@strawberry.type
class BookResult:
    """Mutation return type — always return the changed object + status."""
    success: bool
    message: str
    book:    Optional[Book] = None


# ── In-memory store ───────────────────────────────────────────────────────────

_books: list[Book] = [
    Book(id=1, title="Designing Data-Intensive Applications", year=2017, rating=4.9),
    Book(id=2, title="Computer Networks",                     year=2010, rating=4.7),
]
_next_id = 3


# ── Query ─────────────────────────────────────────────────────────────────────

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> list[Book]:
        return _books

    @strawberry.field
    def book(self, id: int) -> Optional[Book]:
        return next((b for b in _books if b.id == id), None)


# ── Mutation ──────────────────────────────────────────────────────────────────

@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_book(self, input: BookInput) -> BookResult:
        """Create a new book. Returns the created book."""
        global _next_id

        # Validation
        if not input.title.strip():
            return BookResult(success=False, message="Title cannot be empty")
        if input.year < 1900 or input.year > 2026:
            return BookResult(success=False, message=f"Invalid year: {input.year}")

        book = Book(id=_next_id, title=input.title, year=input.year, rating=input.rating)
        _books.append(book)
        _next_id += 1

        return BookResult(success=True, message="Book added", book=book)

    @strawberry.mutation
    def update_rating(self, id: int, rating: float) -> BookResult:
        """Update a book's rating."""
        book = next((b for b in _books if b.id == id), None)
        if not book:
            return BookResult(success=False, message=f"Book {id} not found")
        if not (0.0 <= rating <= 5.0):
            return BookResult(success=False, message="Rating must be 0.0–5.0")

        # Recreate (frozen dataclass style) — in real app just update DB field
        _books[_books.index(book)] = Book(id=book.id, title=book.title,
                                           year=book.year, rating=rating)
        updated = next(b for b in _books if b.id == id)
        return BookResult(success=True, message="Rating updated", book=updated)

    @strawberry.mutation
    def delete_book(self, id: int) -> BookResult:
        """Delete a book by ID."""
        book = next((b for b in _books if b.id == id), None)
        if not book:
            return BookResult(success=False, message=f"Book {id} not found")
        _books.remove(book)
        return BookResult(success=True, message=f"'{book.title}' deleted")


schema = strawberry.Schema(query=Query, mutation=Mutation)


def run(label: str, query: str) -> None:
    print(f"\n{SEP}")
    print(f"{label}")
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
    print("GraphQL POC 2 — Mutations")
    print("=" * 55)

    # ── Before: see current state ─────────────────────────────────────────────
    run("QUERY — books before any mutation", """
        query {
          books { id title rating }
        }
    """)

    # ── Add a book ────────────────────────────────────────────────────────────
    # Note: mutation keyword, input object as argument
    # You choose which fields to return from the result
    run("MUTATION — add a new book", """
        mutation {
          addBook(input: {
            title: "The Algorithm Design Manual"
            year: 2008
            rating: 4.8
          }) {
            success
            message
            book {
              id
              title
              year
            }
          }
        }
    """)

    # ── Update ────────────────────────────────────────────────────────────────
    run("MUTATION — update rating on book id=1", """
        mutation {
          updateRating(id: 1, rating: 4.95) {
            success
            message
            book { title rating }
          }
        }
    """)

    # ── Validation failure ────────────────────────────────────────────────────
    run("MUTATION — invalid rating (out of range)", """
        mutation {
          updateRating(id: 1, rating: 99.0) {
            success
            message
          }
        }
    """)

    # ── Delete ────────────────────────────────────────────────────────────────
    run("MUTATION — delete book id=2", """
        mutation {
          deleteBook(id: 2) {
            success
            message
          }
        }
    """)

    # ── After: final state ────────────────────────────────────────────────────
    run("QUERY — books after all mutations", """
        query {
          books { id title rating }
        }
    """)

    print(f"\n{SEP}")
    print("KEY INSIGHT")
    print(SEP)
    print("""
  REST:    PUT/POST/DELETE — verbs in the URL
  GraphQL: mutation keyword — explicit in the query itself

  Mutation input type:  separate from query return types
  Mutation return type: return the changed object so client
                        doesn't need a follow-up query to refresh

  Pattern: always return { success, message, <object> }
  → client knows if it worked and gets updated data in one call
    """)
