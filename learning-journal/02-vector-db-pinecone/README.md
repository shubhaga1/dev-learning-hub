# 02 — Vector DB + Pinecone

## What you learn here
- What are vectors / embeddings
- Why vector DBs exist
- Pinecone — upsert, query, index
- sentence-transformers — free local embedding model
- LangChain — why it simplifies vector DB code
- Semantic search — find by meaning, not exact words

## Prerequisites
```bash
pip install pinecone sentence-transformers langchain langchain-pinecone langchain-huggingface
```

## Run order
```bash
python 01_pinecone_basics.py          # understand upsert + query
python 02_movie_search.py             # real use case — search movies by plot
python 03_movie_search_langchain.py   # same app, less code with LangChain
python 04_page_index_vs_rag.py        # page index vs RAG — no Pinecone needed
```

## Key concepts

### What is a vector?
```
Text: "I love space movies"
      ↓ embedding model
Vector: [0.12, 0.45, 0.89, 0.23, ...]  ← 384 numbers representing meaning
```

### Why vector DB?
```
Normal DB:  WHERE title = "Inception"     → exact match only
Vector DB:  "find movies about dreams"    → finds by meaning
```

### Without LangChain vs With LangChain
```python
# Without — manual steps
embedding = model.encode(text).tolist()
index.upsert([{"id": "1", "values": embedding, "metadata": {...}}])

# With LangChain — one line
vectorstore = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
```

### Embedding model comparison
| Model | Dimensions | Cost |
|-------|-----------|------|
| all-MiniLM-L6-v2 | 384 | Free |
| all-mpnet-base-v2 | 768 | Free |
| OpenAI text-embedding-3-small | 1536 | Paid |

### Page Index vs RAG — what unit do you index?

```
PAGE INDEX
  Each document → 1 embedding (whole page as one vector)
  Query returns: entire document
  Best for: "find me the relevant document"
  Weakness: specific details buried in long pages get averaged out

RAG (chunk-based)
  Each document → N embeddings (split into ~2-4 sentence chunks)
  Query returns: the exact sentences most relevant to your question
  Best for: "answer a specific question about my documents"
  Weakness: chunk boundary can cut context in half

EXAMPLE — query: "What happens when Redis runs out of memory?"
  Page Index → Score: 0.64 | returns entire Redis page (800 words)
  RAG        → Score: 0.69 | returns: "Eviction: when memory is full,
               Redis evicts keys by LRU, LFU, or TTL" (2 sentences)

BEST OF BOTH — Parent Document Retrieval
  1. Search RAG index → get the precise chunk
  2. Fetch the parent page for that chunk
  3. Pass BOTH to LLM — precise retrieval + full context
```

### How Pinecone stores data internally
- Uses **HNSW** (Hierarchical Navigable Small World) graph
- Layered structure — starts at top (fewer nodes) → narrows down
- Similar to B+ Tree concept but for vectors instead of sorted values
