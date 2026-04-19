"""
SYNC vs THREADS — I/O bound scraping

KEY INSIGHT:
  Scraping = waiting for server response (I/O-bound)
  Your CPU is idle while waiting → parallelism is free

  Sequential:  fire url1 → wait → fire url2 → wait → ...  total = sum of all waits
  Threads:     fire all urls → wait for slowest one        total = max of all waits

GIL NOTE:
  Python GIL blocks threads for CPU work.
  BUT: GIL is RELEASED while waiting for network I/O.
  So threads work perfectly for scraping — GIL is not a problem here.

Uses only built-in libraries — no install needed.
Test URL: httpbin.org/delay/1  → server waits 1 second before responding
"""

import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 10 URLs — each takes ~1 second to respond
URLS = [f"https://httpbin.org/delay/1?id={i}" for i in range(10)]

# ── Approach 1: Sequential — one at a time ────────────────────────────────────
def fetch(url):
    """Fetch one URL, return response length."""
    with urllib.request.urlopen(url, timeout=10) as response:
        return len(response.read())

def sequential():
    print("── Sequential (one at a time) ──")
    start = time.time()

    results = []
    for url in URLS:
        size = fetch(url)
        results.append(size)
        print(f"  fetched {url[-6:]}  size={size}")

    elapsed = time.time() - start
    print(f"  Total: {elapsed:.1f}s  (≈ {len(URLS)} × 1s = {len(URLS)}s expected)\n")
    return results

# ── Approach 2: ThreadPoolExecutor — all at once ──────────────────────────────
# Threads release the GIL while waiting for network → all wait in parallel
def parallel_threads():
    print("── ThreadPoolExecutor (all at once) ──")
    start = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        # submit all 10 at once — they all fire immediately
        futures = {executor.submit(fetch, url): url for url in URLS}

        for future in as_completed(futures):
            url  = futures[future]
            size = future.result()
            results.append(size)
            print(f"  fetched {url[-6:]}  size={size}")

    elapsed = time.time() - start
    print(f"  Total: {elapsed:.1f}s  (≈ 1s expected — all waited in parallel)\n")
    return results

# ── Summary ───────────────────────────────────────────────────────────────────
def summary():
    print("""
DIFFERENCE:
  Sequential:    10 requests × 1s each = ~10s
  ThreadPool:    10 requests, all fire at once = ~1s   (10x faster)

WHY THREADS WORK HERE (despite GIL):
  Thread 1: fires request → waiting for network → GIL released ✅
  Thread 2: fires request → waiting for network → GIL released ✅
  ...all 10 threads waiting simultaneously, GIL not needed while waiting
  When response arrives → thread reacquires GIL → processes data

GIL only matters for CPU work (math, compression).
For network I/O: threads are perfectly parallel.

NEXT: 02_asyncio.py — same result with zero threads (event loop)
""")

if __name__ == "__main__":
    sequential()
    parallel_threads()
    summary()
