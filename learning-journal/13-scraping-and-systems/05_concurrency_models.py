"""
PYTHON CONCURRENCY MODELS — 4 ways to run things "at the same time"

                    Sequential   Threading    Multiprocessing   Asyncio
────────────────────────────────────────────────────────────────────────
Threads/processes   1            N OS threads  N OS processes    1 thread
GIL bypass          N/A          NO (GIL held) YES (new process) NO (not needed)
I/O bound?          bad          ✅ great       ✅ works          ✅ best
CPU bound?          bad          ❌ GIL blocks  ✅ great          ❌ still one thread
Memory (1000 req)   N/A          ~1 GB         ~50 GB            ~50 MB
Max concurrency     1            500–1000       CPU cores × 2     100,000+
Code complexity     simple       simple         medium            medium

GIL = Global Interpreter Lock
  CPython (standard Python) allows only ONE thread to run Python bytecode at a time.
  BUT: GIL is RELEASED when a thread does I/O (network, disk, sleep).
  So for scraping: all threads wait for network simultaneously → GIL is irrelevant.
"""

import urllib.request, time, asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

URLS = [f"https://httpbin.org/delay/1?id={i}" for i in range(5)]

# ── Pattern 1: Sequential ────────────────────────────────────────────────────
def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return len(r.read())

def sequential():
    """one request → wait → one request → wait"""
    return [fetch(url) for url in URLS]

# ── Pattern 2: Threading ─────────────────────────────────────────────────────
# GIL released during urlopen() → all threads wait for network in parallel
# Best for: I/O-bound, simple code, existing sync libraries
def with_threads():
    with ThreadPoolExecutor(max_workers=len(URLS)) as pool:
        return list(pool.map(fetch, URLS))

# ── Pattern 3: Multiprocessing ───────────────────────────────────────────────
# Each worker = separate Python process → truly bypasses GIL
# Best for: CPU-bound (parsing, ML, math), NOT for I/O (overkill + pickle overhead)
def fetch_safe(url):            # wrap: ProcessPool needs picklable exceptions
    try:
        return fetch(url)
    except Exception:
        return -1

def with_multiprocessing():
    with ProcessPoolExecutor(max_workers=4) as pool:
        return list(pool.map(fetch_safe, URLS))

# ── Pattern 4: Asyncio ───────────────────────────────────────────────────────
# 1 thread, event loop. await = "I'm waiting, run something else meanwhile"
# Best for: I/O-bound at high concurrency, lowest memory usage
async def fetch_async(session, url):
    import aiohttp
    async with session.get(url) as r:
        return len(await r.read())

async def with_asyncio():
    import aiohttp
    connector = aiohttp.TCPConnector(limit=0, limit_per_host=0)
    async with aiohttp.ClientSession(connector=connector) as session:
        return await asyncio.gather(*[fetch_async(session, url) for url in URLS])

# ── Run all, compare ─────────────────────────────────────────────────────────
def timed(label, fn):
    t = time.time()
    result = fn()
    elapsed = time.time() - t
    print(f"  {label:<20} {elapsed:.1f}s  ({len(result)} results)")
    return elapsed

if __name__ == "__main__":
    print(f"Fetching {len(URLS)} URLs (each ~1s)\n")

    t_seq   = timed("sequential",       sequential)
    t_thr   = timed("threading",        with_threads)
    t_mproc = timed("multiprocessing",  with_multiprocessing)

    try:
        t_async = timed("asyncio", lambda: asyncio.run(with_asyncio()))
    except ImportError:
        print("  asyncio (aiohttp)     SKIPPED — pip install aiohttp")
        t_async = None

    print(f"""
MEMORY MODEL for 1,000 concurrent requests:
  sequential       —         not concurrent
  threading        ~1  GB    1000 × 1MB OS thread stacks (stack reserved, not committed)
  multiprocessing  ~50 GB    1000 × 50MB processes  ← NEVER do this for I/O
  asyncio          ~50 MB    1000 coroutines on 1 thread heap

WHEN TO CHOOSE:
  scraping  < 100 URLs   → threading     (simplest)
  scraping  100–10k URLs → asyncio       (lowest memory, scales)
  CPU work  (parsing)    → multiprocessing (real parallelism)
  Java 21+               → virtual threads (asyncio scale + no GIL)
""")
