"""
Page Index vs RAG — Side-by-side POC

The core question: what unit do you index?

  Page Index  → one vector PER DOCUMENT (the whole page as one embedding)
  RAG         → one vector PER CHUNK (document split into ~100-word pieces)

Same query hits both. See what comes back and WHY.

No Pinecone needed — uses sentence-transformers + numpy locally.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# ============================================================
# THE DATA — 3 pages, each covering a different topic
# Each page is long enough that chunking reveals something new
# ============================================================

PAGES = [
    {
        "id": "page_1",
        "title": "Kafka Architecture",
        "text": """
            Apache Kafka is a distributed event streaming platform.
            It stores messages in topics, which are split into partitions.
            Each partition is an ordered, immutable log of records.
            Producers write to topics. Consumers read from topics via consumer groups.
            Kafka retains messages for a configurable time (default 7 days).
            This means consumers can replay past events — unlike traditional queues.
            Kafka uses ZooKeeper (or KRaft in newer versions) for cluster coordination.
            KRaft removes the ZooKeeper dependency — Kafka handles its own consensus via Raft.
            Throughput: Kafka can handle millions of messages per second.
            Use cases: event sourcing, log aggregation, real-time analytics pipelines.
        """
    },
    {
        "id": "page_2",
        "title": "Redis Internals",
        "text": """
            Redis is an in-memory data structure store.
            It supports strings, hashes, lists, sets, sorted sets, and streams.
            All data lives in RAM — reads and writes are O(1) for most operations.
            Redis uses a single-threaded event loop — no lock contention.
            Persistence: RDB (point-in-time snapshots) or AOF (append-only log).
            Redis Cluster shards data across nodes using consistent hashing (16384 slots).
            Pub/Sub: Redis supports lightweight publish-subscribe messaging.
            Eviction: when memory is full, Redis evicts keys by LRU, LFU, or TTL.
            Use cases: session cache, rate limiting, leaderboard (sorted sets), pub/sub.
            Limitation: dataset must fit in RAM — not suitable for terabyte-scale storage.
        """
    },
    {
        "id": "page_3",
        "title": "Kubernetes Scheduling",
        "text": """
            Kubernetes schedules Pods onto Nodes using the kube-scheduler.
            Scheduling has two phases: filtering (remove unfit nodes) and scoring (rank remaining).
            Filtering checks: resource requests (CPU/memory), node selectors, taints/tolerations.
            Scoring favors nodes with most available resources (least requested priority).
            Pod Affinity: schedule Pod near other Pods (e.g., same zone for low latency).
            Pod Anti-Affinity: spread replicas across zones for high availability.
            Resource Requests vs Limits: requests = guaranteed, limits = ceiling.
            If a container exceeds its memory limit, it is OOM-killed immediately.
            HPA (Horizontal Pod Autoscaler) adds/removes Pod replicas based on CPU or custom metrics.
            Use cases: stateless web apps scale out on traffic; Kafka consumers scale on lag.
        """
    }
]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# ============================================================
# APPROACH 1 — PAGE INDEX
# One embedding per document. The whole page becomes one vector.
# ============================================================

print("=" * 60)
print("  BUILDING PAGE INDEX")
print("  Strategy: embed the ENTIRE page as one vector")
print("=" * 60)

page_index = []
for page in PAGES:
    # Combine title + full text into one string, embed it all
    full_text = page["title"] + ". " + page["text"].strip()
    vector = model.encode(full_text)
    page_index.append({
        "id": page["id"],
        "title": page["title"],
        "vector": vector,
        "full_text": page["text"].strip()
    })
    print(f"  ✅ Indexed page: '{page['title']}' → 1 vector (384 dims)")

print(f"\n  Total vectors in Page Index: {len(page_index)}")


# ============================================================
# APPROACH 2 — RAG (chunk-based index)
# Split each page into ~2-sentence chunks. Each chunk = one vector.
# ============================================================

print("\n" + "=" * 60)
print("  BUILDING RAG INDEX (chunk-based)")
print("  Strategy: split each page into chunks, embed each chunk")
print("=" * 60)

def chunk_text(text, chunk_size=2):
    """Split text into chunks of ~chunk_size sentences."""
    sentences = [s.strip() for s in text.strip().split(".") if s.strip()]
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = ". ".join(sentences[i:i + chunk_size]) + "."
        chunks.append(chunk)
    return chunks

rag_index = []
for page in PAGES:
    chunks = chunk_text(page["text"], chunk_size=2)
    for i, chunk in enumerate(chunks):
        vector = model.encode(chunk)
        rag_index.append({
            "id": f"{page['id']}_chunk_{i}",
            "page_title": page["title"],
            "chunk_text": chunk,
            "vector": vector
        })
    print(f"  ✅ Chunked '{page['title']}' → {len(chunks)} chunks")

print(f"\n  Total vectors in RAG Index: {len(rag_index)}")


# ============================================================
# QUERY FUNCTION — run the same query against both indexes
# ============================================================

def search_page_index(query, top_k=2):
    q_vec = model.encode(query)
    scored = [(cosine_similarity(q_vec, p["vector"]), p) for p in page_index]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

def search_rag_index(query, top_k=3):
    q_vec = model.encode(query)
    scored = [(cosine_similarity(q_vec, c["vector"]), c) for c in rag_index]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


# ============================================================
# RUN QUERIES — same question, both approaches
# ============================================================

queries = [
    "How does Kafka handle message retention and replay?",   # specific detail inside page_1
    "What happens when Redis runs out of memory?",           # specific detail inside page_2
    "distributed event streaming platform",                  # broad topic → page_1
]

for query in queries:
    print("\n" + "=" * 60)
    print(f"  QUERY: \"{query}\"")
    print("=" * 60)

    # --- Page Index results ---
    print("\n  [PAGE INDEX] — returns whole documents")
    page_results = search_page_index(query, top_k=2)
    for score, page in page_results:
        print(f"    Score: {score:.3f} | Document: '{page['title']}'")
        # Show first 80 chars of the page to illustrate it returns the full page
        preview = page["full_text"].replace("\n", " ").strip()[:120]
        print(f"    Preview: {preview}...")

    # --- RAG results ---
    print("\n  [RAG INDEX] — returns specific chunks")
    rag_results = search_rag_index(query, top_k=3)
    for score, chunk in rag_results:
        print(f"    Score: {score:.3f} | From: '{chunk['page_title']}'")
        print(f"    Chunk: {chunk['chunk_text']}")


# ============================================================
# FINAL COMPARISON — key differences summarised
# ============================================================

print("\n" + "=" * 60)
print("  SUMMARY — Page Index vs RAG")
print("=" * 60)
print("""
  PAGE INDEX
  ─────────────────────────────────────────────────────────
  Unit indexed:   Whole document (1 vector per page)
  Retrieves:      Entire page — you get everything or nothing
  Best for:       "Find me the most relevant document"
                  Document classification, routing
  Weakness:       Long pages average out meaning — specific
                  details buried in the middle are lost
  Example fail:   Query "KRaft removes ZooKeeper" on page_1
                  → page_1 scores OK (whole Kafka page)
                  → but Redis or K8s page might outscore it
                    if their summary is more query-like

  RAG (CHUNK-BASED)
  ─────────────────────────────────────────────────────────
  Unit indexed:   Chunk (~2-4 sentences, 1 vector per chunk)
  Retrieves:      The exact sentences most relevant to query
  Best for:       "Answer a specific question about a document"
                  Q&A over long documents, chatbots
  Weakness:       Chunk boundaries can cut context in half
                  ("memory limit" chunk might not have "OOM-kill" context)

  WHEN BOTH ARE USED TOGETHER (HyDE, parent-child retrieval)
  ─────────────────────────────────────────────────────────
  Search RAG index (get precise chunk)
  → fetch parent page for that chunk (full context)
  → pass BOTH to the LLM
  This is called Parent Document Retrieval — best of both worlds.
""")
