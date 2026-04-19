"""
BENCHMARK — all 4 concurrency models, live timing

20 URLs × ~1s each.  Expected:
  sequential      ~20s  (one at a time)
  threading        ~2s  (all fire, GIL released for I/O)
  multiprocessing  ~3s  (process spawn overhead adds ~1–2s)
  asyncio          ~2s  (one thread, event loop, lowest overhead)

Run:  python 06_benchmark.py
Requires: pip install aiohttp  (for asyncio test)
"""

import urllib.request, time, asyncio, multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

N    = 20
URLS = [f"https://httpbin.org/delay/1?id={i}" for i in range(N)]

# ── fetch functions ───────────────────────────────────────────────────────────
def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return len(r.read())

def fetch_process_safe(url):        # exceptions must be picklable for ProcessPool
    try:
        return fetch(url)
    except Exception:
        return -1

async def fetch_async(session, url):
    async with session.get(url) as r:
        return len(await r.read())

# ── runners ───────────────────────────────────────────────────────────────────
def run_sequential():
    return [fetch(u) for u in URLS]

def run_threading():
    with ThreadPoolExecutor(max_workers=N) as pool:
        futures = {pool.submit(fetch, u): u for u in URLS}
        return [f.result() for f in as_completed(futures)]

def run_multiprocessing():
    workers = min(N, multiprocessing.cpu_count() * 2)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(fetch_process_safe, u) for u in URLS]
        return [f.result() for f in as_completed(futures)]

async def _async_main():
    import aiohttp
    conn = aiohttp.TCPConnector(limit=0, limit_per_host=0)
    async with aiohttp.ClientSession(connector=conn) as session:
        return await asyncio.gather(*[fetch_async(session, u) for u in URLS])

def run_asyncio():
    return asyncio.run(_async_main())

# ── benchmark harness ─────────────────────────────────────────────────────────
def bench(label, fn):
    print(f"  {label:<18} ...", end=" ", flush=True)
    try:
        t = time.time()
        results = fn()
        elapsed = time.time() - t
        ok = sum(1 for r in results if r and r > 0)
        print(f"{elapsed:.1f}s  ({ok}/{len(results)} ok)")
        return elapsed, len(results)
    except ImportError:
        print("SKIPPED (pip install aiohttp)")
        return None, 0
    except Exception as e:
        print(f"FAILED: {e}")
        return None, 0

def print_table(rows, seq_time):
    print(f"\n  {'Approach':<18} {'Time':>6}  {'Speedup':>8}  Notes")
    print("  " + "─" * 65)
    for name, elapsed, n, notes in rows:
        if elapsed:
            speedup = seq_time / elapsed
            print(f"  {name:<18} {elapsed:>5.1f}s  {speedup:>7.1f}x  {notes}")

if __name__ == "__main__":
    multiprocessing.freeze_support()   # required on macOS/Windows

    print(f"\nBenchmarking {N} URLs (each takes ~1s to respond)\n")

    rows = []

    t, n = bench("sequential",      run_sequential)
    rows.append(("sequential",      t, n, f"{N}s expected — one at a time"))

    t, n = bench("threading",       run_threading)
    rows.append(("threading",       t, n, f"GIL released for I/O, {N} OS threads"))

    t, n = bench("multiprocessing", run_multiprocessing)
    rows.append(("multiprocessing", t, n, "process spawn overhead visible"))

    t, n = bench("asyncio",         run_asyncio)
    rows.append(("asyncio",         t, n, "1 thread, event loop"))

    seq_time = rows[0][1] or (N * 1.0)
    print_table(rows, seq_time)

    print(f"""
  Memory for 1,000 concurrent requests:
    threading       ~1 GB    (1000 × 1 MB OS thread stack reserved)
    multiprocessing ~50 GB   (1000 × 50 MB process — never do this)
    asyncio         ~50 MB   (1000 coroutines on heap)
""")
