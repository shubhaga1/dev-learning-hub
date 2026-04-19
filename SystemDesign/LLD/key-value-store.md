# LLD: Key-Value Store (Memcached-style)

---

## Key Interview Questions to Ask First

```
1. Read-heavy or write-heavy?
2. What's the expected cache hit rate?
3. Single region or multi-region?
4. Consistency requirement — is stale data acceptable?
5. What's the eviction policy preference?
6. Key/value size limits?
7. TTL support needed?
```

---

## Design Progression (go in this order in interviews)

### Step 1 — Single node

- Hash table: O(1) get/put
- Problem: memory is finite → need eviction

**Eviction policies:**

| Policy | Evicts | Best for |
|--------|--------|---------|
| LRU | Least recently used | General purpose (default choice) |
| LFU | Least frequently used | Popularity-based (trending content) |
| FIFO | Oldest entry | Simple, time-ordered data |

**LRU implementation:**
```
HashMap<key, Node>  +  DoublyLinkedList

GET:
  node = map.get(key)
  move node to head (most recently used)
  return node.value

PUT:
  if key exists → update + move to head
  if cache full → remove tail node + remove from map
  insert new node at head + add to map
```

Both operations: O(1)

---

### Step 2 — Multiple services, one cache

**Option A — Co-located (cache on same host as service)**
- Pro: simple, auto-scales with service
- Con: cache lost if host dies

**Option B — Dedicated cache hosts**
- Pro: cache survives service restarts, scales independently
- Con: network hop, more infra to manage

---

### Step 3 — Routing requests to the right cache

**Naive: `hash(key) % N`**

Problem: adding/removing a node changes N → almost all keys remap → cache miss storm

**Fix: Consistent Hashing**
- Place cache servers on a ring (by hash of their ID)
- Place keys on the ring (by hash of key)
- Key → clockwise nearest server

Adding/removing a server → only `1/N` of keys remap (not all)

**Consistent hashing problems:**
- Uneven distribution → hotspots (fix: virtual nodes per server)
- More complex implementation

---

### Step 4 — Cache Client

Dedicated library embedded in each service:
- Knows the list of cache servers
- Does consistent hashing internally
- Abstracts GET/PUT from the service

**How does it know which servers exist?**

| Discovery method | How | Trade-off |
|-----------------|-----|----------|
| Static config file | List IPs | Simple, manual updates |
| S3 / central store | Pull config | Slightly stale, easy to update |
| Zookeeper | Watch nodes, get live updates | Real-time, but dependency |

---

### Step 5 — High Availability: Replicas

- Primary handles all writes (PUT)
- Read replicas serve GETs (reduces load)

**Replication modes:**

| | Sync | Async |
|---|------|-------|
| Consistency | Strong | Eventual |
| Latency | Higher | Lower |
| Use case | Financial, critical data | Social feeds, recommendations |

---

### Step 6 — Security + Monitoring

- Cache servers behind firewall — only trusted services can reach them
- Monitor: hit rate, miss rate, memory usage, eviction rate, latency
- "If you can't measure it, you can't improve it"

---

## Data Flow Diagram

```
Client Request
      ↓
   Service
      ↓
  Cache Client (consistent hashing)
      ↓              ↓
Cache Server 1   Cache Server 2   ...
  (+ replicas)     (+ replicas)
      ↓
  [MISS] → Backend DB → populate cache → return
  [HIT]  → return cached value
```

---

## LRU Code Sketch

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap   = capacity
        self.cache = OrderedDict()   # preserves insertion order

    def get(self, key: str) -> str | None:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # mark as recently used
        return self.cache[key]

    def put(self, key: str, value: str) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)  # evict LRU (front)
```

---

## Trade-off Summary

| Decision | Option A | Option B | Pick when |
|---------|----------|----------|-----------|
| Eviction | LRU | LFU | LRU default; LFU if access frequency matters |
| Deployment | Co-located | Dedicated hosts | Dedicated for high availability |
| Routing | Hash modulo | Consistent hashing | Consistent hashing always for distributed |
| Discovery | Static config | Zookeeper | Zookeeper if servers change frequently |
| Replication | Sync | Async | Sync for critical data, Async for speed |

---

## One-Sentence Answers for Interview

- **Why LRU?** Assumes recently used data is likely to be used again — holds for most workloads.
- **Why consistent hashing?** Adding/removing nodes only remaps 1/N keys instead of all keys.
- **Why a separate cache client?** Keeps routing logic out of business logic — single place to change.
- **Why replicas?** One node failure shouldn't drop your entire cache layer.
- **Why async replication by default?** Cache is a performance layer — slightly stale is usually acceptable.
