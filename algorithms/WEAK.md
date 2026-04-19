# WEAK SPOTS — Problems I got wrong or forgot

## How to use
When you struggle with a problem or forget a concept → add it here.
These get priority in revision. Review every Sunday.

Format: Problem | Pattern | What I missed | Date

---

## DSA WEAK SPOTS

| Problem | Pattern | What I missed | Date | Resolved |
|---------|---------|---------------|------|----------|
| Sliding Window Maximum | Monotonic Deque | Didn't think of Deque — tried nested loops | 2026-04-12 | ❌ |
| Merge K Sorted Lists | PriorityQueue | Forgot to push `node.next` back into heap | 2026-04-12 | ❌ |

---

## SYSTEM DESIGN WEAK SPOTS

| Topic | What I missed | Date | Resolved |
|-------|---------------|------|----------|
| Capacity calc | Said 10PB instead of 100TB (off by 100x) | 2026-04-12 | 🟡 |
| Kafka priority | Kafka is FIFO not priority — need separate topics | 2026-04-12 | 🟡 |

---

## CONCEPTS I KEEP FORGETTING

| Concept | Quick reminder | Times forgotten |
|---------|---------------|----------------|
| BFS level order: snapshot queue size | `int size = queue.size()` BEFORE the for loop | 1 |
| Deque indices not values | Store INDEX in deque for sliding window, not the value | 1 |
| Cassandra partition key | Determines WHICH node. Clustering key = ORDER within node | 1 |
