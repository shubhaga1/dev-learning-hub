# Queue — Complete Learning Guide

10 files, ordered from basics to internals to interview problems.
Read each file in order. Run with `rj <ClassName>`.

---

## Learning Path

| # | File | Class to run | What you learn |
|---|------|--------------|----------------|
| 1 | `01_QueueBasics.java` | `rj QueueBasics` | FIFO, add/remove/peek, ArrayDeque vs LinkedList |
| 2 | `02_PriorityQueue.java` | `rj PriorityQueueProblems` | Min/max heap, custom comparator, top-K pattern |
| 3 | `03_Deque.java` | `rj Deque` | Double-ended queue, sliding window maximum |
| 4 | `04_InterviewPatterns.java` | `rj InterviewPatterns` | Pattern recognition cheat sheet, BFS, Kth largest |
| 5 | `05_TraversalInQueue.java` | `rj TraversalInQueue` | Traverse without losing data — peek/remove/add trick |
| 6 | `06_CustomQueueLinkedList.java` | `rj CustomQueueLinkedList` | Build queue from scratch — Node pointers, head/tail |
| 7 | `07_CustomQueueCircularArray.java` | `rj CustomQueueCircularArray` | Circular array — modulo wrap, full vs empty |
| 8 | `08_QueueStackConversions.java` | `rj QueueStackConversions` | Queue using 2 stacks, Stack using 1 queue |
| 9 | `09_FirstNegativeInWindow.java` | `rj FirstNegativeInWindow` | Sliding window — brute O(n×k) vs queue O(n) |
| 10 | `10_CircularGame.java` | `rj CircularGame` | Josephus problem, insert/remove at index |

---

## Core Concepts

### What is a Queue?

```
FIFO — First In, First Out

add → [  50  |  40  |  30  |  20  |  10  ] → remove
rear                                           front

Real-world: ticket counter, print queue, BFS traversal
```

Operations and their time complexity:

| Operation | What it does | Time |
|-----------|-------------|------|
| `add(x)` | Insert at rear | O(1) |
| `remove()` | Remove from front | O(1) |
| `peek()` | Read front without removing | O(1) |
| `size()` | Count elements | O(1) |
| `isEmpty()` | Check if empty | O(1) |

### Queue vs Stack

```
Queue (FIFO)                 Stack (LIFO)
────────────                 ────────────
add at rear                  push on top
remove from front            pop from top

add(1,2,3) → remove: 1,2,3  push(1,2,3) → pop: 3,2,1
```

### Which Java class to use?

```java
Queue<Integer> q = new ArrayDeque<>();    // ✅ general use — fastest
Queue<Integer> q = new LinkedList<>();    // OK, but slower (pointer overhead)
Queue<Integer> q = new PriorityQueue<>(); // when you need min/max order

Deque<Integer> dq = new ArrayDeque<>();   // when you need both ends
```

> Never use `Stack<>` in Java — it's legacy. Use `ArrayDeque` as a stack too.

---

## File-by-file Breakdown

### 01 — Queue Basics
`ArrayDeque` vs `LinkedList`, the 6 operations, common pitfalls.

```java
Queue<Integer> q = new ArrayDeque<>();
q.add(10);          // insert at rear
q.peek();           // read front → 10 (no removal)
q.remove();         // remove front → 10
q.isEmpty();        // check empty
```

**Gotcha:** `q.remove()` throws if empty. Use `q.poll()` to get null instead.

---

### 02 — Priority Queue
Not FIFO — always gives you the **smallest** element first (min heap by default).

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();              // min heap
PriorityQueue<Integer> pq = new PriorityQueue<>(reverseOrder()); // max heap

// Custom: sort by string length
PriorityQueue<String> pq = new PriorityQueue<>(Comparator.comparingInt(String::length));
```

**Top-K pattern** (Kth largest element):
```
Keep a min heap of size k.
When size > k, poll() — removes the smallest.
After processing all elements, peek() = kth largest.

Why min heap for kth LARGEST? Because you want to evict the smallest ones,
keeping only the k largest. peek() = smallest of the top-k = kth largest.
```

---

### 03 — Deque (Double-Ended Queue)
Add/remove from **both** front and rear.

```java
Deque<Integer> dq = new ArrayDeque<>();
dq.addFirst(x);   dq.addLast(x);
dq.peekFirst();   dq.peekLast();
dq.pollFirst();   dq.pollLast();
```

**Monotonic Deque** — the key to sliding window maximum O(n):
```
Invariant: deque is always decreasing (largest at front).
For each new element:
  - Remove from REAR anything smaller (they can never be a future max)
  - Remove from FRONT anything outside the window
  - Front = current window maximum
```

---

### 04 — Interview Pattern Cheat Sheet
Read this before any queue interview question.

```
"level by level"           → BFS Queue
"shortest path in grid"    → BFS Queue
"top K / kth largest"      → PriorityQueue (min heap size k)
"sliding window max/min"   → Monotonic Deque
"merge sorted lists"       → PriorityQueue
"rotting oranges/islands"  → Multi-source BFS (add all sources at start)
```

---

### 05 — Queue Traversal
Queue has no index — you can't do `q.get(i)`. Instead:

```
Snapshot n = q.size()     ← BEFORE the loop
for i in 1..n:
    val = q.peek()        ← read front
    q.remove()            ← take out
    q.add(val)            ← put back at rear

After n iterations: every element visited, queue unchanged.
```

**Why snapshot size?** Because `q.size()` changes inside the loop — snapshotting it upfront stops you from looping forever.

---

### 06 — Custom Queue (Linked List)
How queues work under the hood.

```
head → [10] → [20] → [30] → null ← tail

add(40):  tail.next = Node(40), tail = Node(40)   O(1)
remove(): val = head.val, head = head.next         O(1)

Edge case: after removing last element, tail must also become null.
```

---

### 07 — Custom Queue (Circular Array)
Why naive array queue wastes space — and how circular array fixes it.

```
Naive: after 3 removes, front sits at index 3 — indices 0,1,2 wasted forever.

Circular fix: rear = (rear + 1) % capacity   ← wraps around
              front = (front + 1) % capacity

Full vs empty both show front == rear.
Solution: track size separately.
```

---

### 08 — Queue ↔ Stack Conversions

**Queue using 2 Stacks:**
```
inbox stack  ← all new elements go here (push O(1))
outbox stack ← elements ready to dequeue

remove(): if outbox empty, drain inbox → outbox (reverses order = FIFO)
          then pop outbox

Each element moves inbox→outbox exactly once → amortized O(1) dequeue
```

**Stack using 1 Queue:**
```
push(x): add x, then rotate all previous elements to the back
         new element ends up at front = top of stack
         push O(n), pop O(1)
```

---

### 09 — First Negative in Every Window of K

```
arr = [-3, 5, -2, 7, -1, 4]   k=3
Answer: [-3, -2, -2, -1]

Brute force: scan k elements per window → O(n×k)

Queue optimization → O(n):
  Queue stores INDICES of negatives inside the current window.
  Slide:
    1. Remove front if it's outside window (index < i)
    2. Add j if arr[j] < 0
    3. Answer = arr[queue.front()] if non-empty, else 0

Key: each index is added once and removed once → O(n) total.
```

---

### 10 — Circular Game (Josephus Problem)

```
n=6 people, eliminate every k=2nd:
[1,2,3,4,5,6]
  eliminate 2 → [3,4,5,6,1]
  eliminate 4 → [5,6,1,3]
  eliminate 6 → [1,3,5]
  eliminate 3 → [5,1]
  eliminate 1 → [5]  ← winner

Queue simulation:
  rotate (k-1) people to back → they survive this round
  remove() the k-th            → eliminated
  Repeat until 1 remains.

Time: O(n×k)   Space: O(n)
```

**Insert/Remove at index** (bonus — O(n) via rotation):
```
insertAt(queue, idx, val):
  rotate idx elements to back
  add val
  rotate remaining (n-idx) elements to back

removeAt(queue, idx):
  rotate idx elements to back
  remove() front element
  rotate remaining to restore order
```

---

## Common Gotchas

| Gotcha | Fix |
|--------|-----|
| `q.remove()` on empty queue throws | Use `q.poll()` → returns null |
| Looping over queue without snapshoting size | Always `int n = q.size()` before the loop |
| `PriorityQueue` is min heap, not max | Use `Collections.reverseOrder()` for max |
| Forgot to clear tail on last remove in custom queue | `if (head == null) tail = null` |
| Circular array: full and empty look the same | Track `size` separately |
| Stack in Java | Use `ArrayDeque`, not `Stack<>` — Stack is legacy |

---

## Interview Complexity Table

| Problem | Approach | Time | Space |
|---------|----------|------|-------|
| BFS level order | Queue | O(n) | O(w) — w = max width |
| Kth largest | Min heap size k | O(n log k) | O(k) |
| Sliding window max | Monotonic Deque | O(n) | O(k) |
| First negative in window | Index queue | O(n) | O(k) |
| Josephus / circular game | Queue rotation | O(n×k) | O(n) |
| Queue using stacks | 2 stacks | O(1) amortized | O(n) |
| Stack using queue | 1 queue | O(n) push | O(n) |
