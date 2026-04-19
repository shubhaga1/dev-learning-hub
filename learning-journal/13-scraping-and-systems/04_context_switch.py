"""
CONTEXT SWITCH — the cost of pausing one thread and resuming another

The OS runs a scheduler that gives each thread a time slice (~10ms).
When a slice expires (or thread voluntarily waits), the OS switches threads.

WHAT GETS SAVED (per thread, into RAM):
  16 CPU registers × 8 bytes = 128 bytes    ← rip, rsp, rax, rbx ...
  OS thread metadata                        ← thread ID, priority, signals
  ─────────────────────────────────────────
  Total saved per switch:    ~1–2 KB

COST BREAKDOWN:
  Save registers to RAM:        ~10 ns     (fast)
  Enter kernel mode:           ~200 ns     (CPU privilege level switch)
  Scheduler picks next thread:  ~100 ns    (find highest priority runnable)
  Load next thread's registers: ~10 ns     (fast)
  Exit kernel mode:            ~200 ns
  CPU cache warm-up:         ~1,000 ns     ← THE EXPENSIVE PART
  ─────────────────────────────────────────
  Total:                   ~1–10 µs

WHY CACHE IS THE BOTTLENECK:
  Thread-1 had hot data in L1 cache (fetched URL string, response buffer)
  When Thread-2 runs, it needs DIFFERENT data → L1 evicts Thread-1's lines
  Thread-1 resumes → cache is cold → pays ~200 cycles per memory access
  10,000 threads switching constantly = cache never warm for anyone
"""

import threading, time

# ── Demo 1: measure actual context-switch overhead ───────────────────────────
# Two threads ping-pong via events — measures round-trip switch time

def measure_switch_cost(n_switches=10_000):
    e1 = threading.Event()
    e2 = threading.Event()
    times = []

    def thread2_work():
        for _ in range(n_switches):
            e1.wait(); e1.clear()   # wait for thread1
            e2.set()                # signal back

    t = threading.Thread(target=thread2_work, daemon=True)
    t.start()

    start = time.perf_counter()
    for _ in range(n_switches):
        e1.set()                    # wake thread2
        e2.wait(); e2.clear()       # wait for reply
    elapsed = time.perf_counter() - start

    per_switch_us = (elapsed / n_switches) * 1_000_000
    return per_switch_us

print("=== Context switch round-trip time ===")
cost = measure_switch_cost()
print(f"  {cost:.1f} µs per round-trip  (= 2 context switches)")
print(f"  {cost/2:.1f} µs per single switch")
print()

# ── Demo 2: thread creation overhead ─────────────────────────────────────────
def measure_thread_creation(n=200):
    start = time.perf_counter()
    threads = []
    for _ in range(n):
        t = threading.Thread(target=lambda: None)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    return (elapsed / n) * 1_000_000   # µs per thread

print("=== Thread creation overhead ===")
cost_create = measure_thread_creation()
print(f"  {cost_create:.0f} µs to create + start + join one thread")
print(f"  At 1000 threads: {cost_create * 1000 / 1000:.0f} ms just for creation overhead")
print()

# ── Demo 3: asyncio has no context switch overhead ───────────────────────────
import asyncio

async def measure_coroutine_switch(n=100_000):
    count = 0
    async def task():
        nonlocal count
        count += 1
        await asyncio.sleep(0)   # yield to event loop, then resume

    start = time.perf_counter()
    await asyncio.gather(*[task() for _ in range(n)])
    elapsed = time.perf_counter() - start
    return (elapsed / n) * 1_000_000   # µs per coroutine switch

print("=== Coroutine switch overhead (asyncio) ===")
coro_cost = asyncio.run(measure_coroutine_switch())
print(f"  {coro_cost:.3f} µs per coroutine switch")
print()

print("""
=== COMPARISON ===

                    OS context switch    Coroutine switch (asyncio)
Cost per switch     1–10 µs              0.001–0.01 µs   (100–1000x cheaper)
Kernel involved?    YES (privilege flip) NO (stays in userspace)
Cache effects?      YES (evicts hot data) NO (same thread, same cache)
Max concurrency     ~1000 threads        100,000+ coroutines

Conclusion:
  For 20 scraping threads: context switch cost is negligible (~200 µs total)
  For 10,000 concurrent scrapers: asyncio wins — no kernel, no cache thrash
""")
