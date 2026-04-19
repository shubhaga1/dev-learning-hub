"""
POC 3 — Connections, Edges, Nodes + Introspection

CONNECTIONS (pagination):
  The GitHub docs say: "Connections let you query related objects
  as part of the same call" and they carry pagination metadata.

  Structure:
    connection {
      totalCount
      pageInfo { hasNextPage endCursor }
      edges {
        cursor
        node { ...actual data... }
      }
    }

INTROSPECTION:
  GraphQL schemas are self-describing.
  Query __schema or __type to discover what's available.
  This is how tools like GraphiQL, Postman build autocomplete.

Run: python3 03_connections_and_introspection.py
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


@strawberry.type
class PageInfo:
    """Pagination metadata — tells client if more pages exist."""
    has_next_page:     bool
    has_previous_page: bool
    start_cursor:      Optional[str]
    end_cursor:        Optional[str]


@strawberry.type
class BookEdge:
    """
    Edge = one item in a connection.
    Has the node (actual data) + a cursor (position marker for pagination).
    """
    cursor: str        # opaque string — client uses this to paginate
    node:   Book


@strawberry.type
class BookConnection:
    """
    Connection = paginated list with metadata.
    This is the standard GraphQL pagination pattern (Relay spec).
    """
    total_count: int
    page_info:   PageInfo
    edges:       list[BookEdge]


# ── Data ──────────────────────────────────────────────────────────────────────

ALL_BOOKS = [
    Book(id=i, title=title, year=year, rating=rating)
    for i, (title, year, rating) in enumerate([
        ("Designing Data-Intensive Applications", 2017, 4.9),
        ("Computer Networks",                     2010, 4.7),
        ("Algorithms",                            2011, 4.8),
        ("Modern Operating Systems",              2014, 4.6),
        ("Clean Code",                            2008, 4.5),
        ("The Pragmatic Programmer",              2019, 4.8),
        ("Introduction to Algorithms",            2009, 4.7),
        ("System Design Interview",               2020, 4.6),
    ], start=1)
]


def _cursor(index: int) -> str:
    """Simple cursor = base64-like encoding of list index."""
    import base64
    return base64.b64encode(f"book:{index}".encode()).decode()


def _decode_cursor(cursor: str) -> int:
    import base64
    return int(base64.b64decode(cursor.encode()).decode().split(":")[1])


# ── Query ─────────────────────────────────────────────────────────────────────

@strawberry.type
class Query:

    @strawberry.field
    def books(
        self,
        first: Optional[int] = None,    # how many to return
        after: Optional[str] = None,    # cursor: start after this item
    ) -> BookConnection:
        """
        Paginated books connection.
        Use: books(first: 3)               → first 3
             books(first: 3, after: cursor) → next 3 after cursor
        """
        start_idx = 0
        if after:
            start_idx = _decode_cursor(after)   # cursor → index

        page    = ALL_BOOKS[start_idx:]
        if first:
            page = page[:first]

        edges = [
            BookEdge(
                cursor=_cursor(ALL_BOOKS.index(book) + 1),
                node=book,
            )
            for book in page
        ]

        has_next = (start_idx + len(page)) < len(ALL_BOOKS)

        return BookConnection(
            total_count=len(ALL_BOOKS),
            page_info=PageInfo(
                has_next_page=has_next,
                has_previous_page=start_idx > 0,
                start_cursor=edges[0].cursor  if edges else None,
                end_cursor=edges[-1].cursor   if edges else None,
            ),
            edges=edges,
        )

    @strawberry.field
    def book(self, id: int) -> Optional[Book]:
        return next((b for b in ALL_BOOKS if b.id == id), None)


schema = strawberry.Schema(query=Query)


def run(label: str, query: str) -> dict:
    print(f"\n{SEP}")
    print(label)
    print(SEP)
    print(query.strip())
    result = schema.execute_sync(query)
    if result.errors:
        print(f"ERRORS: {result.errors}")
        return {}
    print(f"\nRESULT:")
    print(json.dumps(result.data, indent=2))
    return result.data or {}


# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 55)
    print("GraphQL POC 3 — Connections + Introspection")
    print("=" * 55)

    # ── Page 1: first 3 books ─────────────────────────────────────────────────
    data = run("CONNECTION — first 3 books (page 1)", """
        query {
          books(first: 3) {
            totalCount
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              cursor
              node {
                id
                title
                rating
              }
            }
          }
        }
    """)

    # ── Page 2: next 3 using cursor from page 1 ───────────────────────────────
    if data:
        cursor = data["books"]["pageInfo"]["endCursor"]
        run(f"CONNECTION — next 3 books after cursor (page 2)", f"""
            query {{
              books(first: 3, after: "{cursor}") {{
                totalCount
                pageInfo {{
                  hasNextPage
                  hasPreviousPage
                  endCursor
                }}
                edges {{
                  node {{ id title }}
                }}
              }}
            }}
        """)

    # ── INTROSPECTION — discover the schema itself ────────────────────────────
    # This is what GraphiQL / Postman use to build autocomplete
    run("INTROSPECTION — list all types in schema", """
        query {
          __schema {
            types {
              name
              kind
            }
          }
        }
    """)

    run("INTROSPECTION — inspect the Book type", """
        query {
          __type(name: "Book") {
            name
            kind
            fields {
              name
              type {
                name
                kind
              }
            }
          }
        }
    """)

    run("INTROSPECTION — what queries are available?", """
        query {
          __schema {
            queryType {
              fields {
                name
                description
                args {
                  name
                  type { name kind }
                }
              }
            }
          }
        }
    """)

    print(f"\n{SEP}")
    print("KEY INSIGHTS")
    print(SEP)
    print("""
  CONNECTIONS:
    totalCount    — total items (not just this page)
    pageInfo      — hasNextPage, endCursor for next request
    edges.cursor  — opaque pointer to that item's position
    edges.node    — the actual data object

    Client loop:
      1. query books(first: N)
      2. if hasNextPage → query books(first: N, after: endCursor)
      3. repeat until hasNextPage = false

  INTROSPECTION:
    __schema   — full schema (all types, queries, mutations)
    __type     — details about one specific type
    This is how GraphiQL autocomplete works — it introspects
    your schema and knows every valid field and argument.
    No docs needed — the schema IS the docs.
    """)
