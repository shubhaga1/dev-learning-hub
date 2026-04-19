# Learning Journal — Shubham Garg

A self-paced learning journal covering Python, Vector Databases, and DevOps concepts.
Each folder is a topic. Each file is a concept with comments explaining what and why.

---

## Folder Structure

```
learning-journal/
│
├── 01-python-basics/          # Python fundamentals
├── 02-vector-db-pinecone/     # Vector databases, embeddings, semantic search
├── 03-docker-k8s/             # Containers, VMs, Docker, Kubernetes
└── 04-huggingface/            # Fine-tune and publish AI models
```

---

## Topics Covered

### 01 — Python Basics
| File | What you learn |
|------|---------------|
| 01_hello_world.py | Running your first Python program |
| 02_lists_and_dicts.py | Lists, dicts, loops, search |

### 02 — Vector DB + Pinecone
| File | What you learn |
|------|---------------|
| 01_pinecone_basics.py | What is a vector DB, upsert, query |
| 02_movie_search.py | Real use case — semantic movie search with sentence-transformers |
| 03_movie_search_langchain.py | Same app using LangChain — why it's better |

### 04 — HuggingFace
| File | What you learn |
|------|---------------|
| 01_train_and_publish.py | Fine-tune distilbert for sentiment analysis + publish to HuggingFace Hub |

### 03 — Docker & Kubernetes
| File | What you learn |
|------|---------------|
| 01_traditional.py | How apps ran before containers |
| 02_hypervisor_simulated.py | How VMs work — simulated with logs |
| 03_hypervisor_real_code.py | Real VM creation using VirtualBox CLI + AWS boto3 |
| 04_docker.py | Docker containers vs VMs |
| 05_kubernetes.py | Kubernetes — orchestrating many containers |

---

## Key Concepts Learned

### Vector Databases
- Vectors = numbers representing meaning of text
- More dimensions = captures more meaning
- B+ Tree (SQL) vs HNSW (vector search) — different problems
- Pinecone uses HNSW internally for fast similarity search

### Embeddings
| Model | Dimensions | Cost | Use case |
|-------|-----------|------|----------|
| all-MiniLM-L6-v2 | 384 | Free | Learning / prototyping |
| all-mpnet-base-v2 | 768 | Free | Better quality |
| OpenAI text-embedding-3-small | 1536 | Paid | Production |

### VM vs Docker
| | VM (VirtualBox) | Docker |
|--|--|--|
| OS | Full OS per VM | Shared kernel |
| RAM | 1-2 GB each | 50-200 MB each |
| Startup | 2-3 minutes | 2-3 seconds |
| Use case | Run different OS | App deployment |

---

## Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pinecone sentence-transformers langchain langchain-pinecone langchain-huggingface boto3
```

---

## How to use this repo

1. Start from `01-python-basics` if you're new to Python
2. Move to `02-vector-db-pinecone` to learn AI/ML concepts
3. Move to `03-docker-k8s` for DevOps concepts
4. Each file has comments — read them before running
5. Run each file: `python filename.py`
