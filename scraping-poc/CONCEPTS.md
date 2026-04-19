# Concurrency Deep Dive: asyncio vs Java VThreads vs Go Goroutines

## Layer 1: CPU Core → OS Thread (the foundation)

```
Physical Machine (10-core)
│
├── Core 0 ──► runs 1 OS thread at a time (or 2 with hyperthreading → 20 HW threads)
├── Core 1 ──► runs 1 OS thread at a time
├── ...
└── Core 9 ──► runs 1 OS thread at a time

OS Scheduler (preemptive): time-slices hundreds of threads across these cores
```

**OS Thread cost:**
- Stack size: 1–8 MB per thread (Linux default 8MB, macOS 512KB–8MB)
- Creating/destroying: ~10–100 microseconds (syscall)
- Context switch: ~1–10 microseconds
- **1000 OS threads = up to 8 GB RAM just for stacks**

**You CAN create more threads than cores** — the OS scheduler interleaves them.
But context switching overhead grows, and memory fills up fast.

---

## Layer 2: The Problem with OS Threads for I/O

```
Thread waiting for HTTP response:
  [Thread stack: 8MB allocated] [blocked: doing nothing for 500ms]
  Kernel is actually watching the socket with epoll/kqueue
  The thread just... sits there, wasting a slot
```

Solution: Don't give each I/O request its own OS thread.

---

## Layer 3: Python asyncio — Cooperative, Single-Threaded

```
1 OS Thread
└── Event Loop (while True: check ready tasks, run them)
    ├── Coroutine A: fetch(url1)  ← paused at await, waiting for socket
    ├── Coroutine B: fetch(url2)  ← paused at await, waiting for socket
    ├── Coroutine C: fetch(url3)  ← RUNNING right now
    └── ... 10,000 more coroutines, all paused cheaply
```

- `await` = "I'm done for now, put me back in the queue when my I/O is ready"
- Kernel (epoll/kqueue) watches all sockets simultaneously
- Stack per coroutine: ~1–2 KB (just a Python frame, not a full OS thread)
- **Limitation**: Only 1 CPU core used. CPU-heavy work blocks everyone.
- **Scheduling**: Cooperative — you must explicitly `await` to yield control

---

## Layer 4: Java Virtual Threads (Project Loom, Java 21)

```
JVM
├── Carrier Thread 0 (OS thread, pinned to Core 0)
│   └── currently running Virtual Thread #4721
├── Carrier Thread 1 (OS thread, pinned to Core 1)
│   └── currently running Virtual Thread #1033
├── ...
└── Carrier Thread 9 (OS thread, pinned to Core 9)
    └── currently running Virtual Thread #9999

JVM Thread Scheduler Pool: 1,000,000 virtual threads, most parked
```

- Virtual thread blocks on I/O → JVM **unmounts** it from carrier, saves its **continuation**
- Carrier thread picks up the next runnable virtual thread
- Stack: starts at ~1KB, grows dynamically (heap-allocated, not fixed like OS threads)
- **Advantage over asyncio**: Uses ALL CPU cores. CPU-heavy code also benefits.
- **Scheduling**: Cooperative at I/O boundaries (JVM intercepts blocking calls)

---

## Layer 5: Go Goroutines — M:N Preemptive

```
Go Runtime
├── OS Thread 0 (Core 0) ──► goroutine scheduler
│   ├── running goroutine #5
│   └── run queue: [#12, #88, #301, ...]
├── OS Thread 1 (Core 1) ──► goroutine scheduler
│   ├── running goroutine #7
│   └── run queue: [#44, #90, ...]
└── ... (GOMAXPROCS = num cores by default)

Total goroutines: can be 1,000,000+ across all queues
```

- Goroutine initial stack: 2–4 KB, **grows and shrinks** dynamically (segmented/copying stacks)
- **Preemptive scheduling** (since Go 1.14): goroutines can be interrupted at any safe point
- Work-stealing: idle OS threads steal goroutines from busy threads' queues
- Goroutine blocking on I/O → Go runtime uses async I/O under the hood, parks goroutine

---

## Comparison Table

| Feature | Python asyncio | Java Virtual Threads | Go Goroutines |
|---|---|---|---|
| Threading model | 1:1 (1 event loop) | M:N (virtual:carrier) | M:N (goroutine:OS thread) |
| Scheduling | Cooperative | Cooperative at I/O | Preemptive (Go 1.14+) |
| Initial stack | ~1–2 KB | ~1 KB, heap-grows | 2–4 KB, grows/shrinks |
| Uses all cores? | ❌ No (1 core) | ✅ Yes | ✅ Yes |
| Max concurrent | ~100K practical | ~1M+ | ~1M+ |
| CPU-bound perf | Bad (GIL) | Good | Excellent |
| I/O-bound perf | Excellent | Excellent | Excellent |
| Code style | async/await | Normal blocking code! | Normal blocking code! |

**Key insight**: Java VThreads and Go goroutines let you write *normal-looking blocking code*
while the runtime secretly makes it non-blocking. asyncio requires you to explicitly mark
every yield point with `await`.
