"""
BENCHMARK — Python concurrency models for I/O-bound scraping

Tests 4 approaches against 20 URLs (each takes ~1s to respond):

  Approach              Concurrency model              Expected time
  ─────────────────     ──────────────────────────     ─────────────
  Sequential            none                           ~20s
  threading             OS threads, GIL released I/O   ~1s
  multiprocessing       real OS processes               ~1s
  asyncio               1 thread, event loop            ~1s

WHY MULTIPROCESSING IS OVERKILL FOR SCRAPING:
  - spawns N separate Python processes (expensive)
  - each process has its own memory space (~50MB+ per process)
  - designed for CPU-bound work (bypasses GIL for compute)
  - for I/O, threading or asyncio is cheaper and just as fast

INSTALL:
  pip install aiohttp

RUN:
  python 03_benchmark.py
"""

import urllib.request
import time
import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# 20 URLs — each httpbin.org/delay/1 waits exactly 1s before responding
N = 20
URLS = [f"https://httpbin.org/delay/1?id={i}" for i in range(N)]

# ─────────────────────────────────────────────────────────────────────────────
# Shared fetch (used by sequential, threading, multiprocessing)
# ─────────────────────────────────────────────────────────────────────────────
def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return len(r.read())

# ProcessPoolExecutor requires all exceptions to be picklable.
# urllib exceptions can contain _io.BufferedReader (unpicklable) → wrap them.
def fetch_process_safe(url):
    try:
        return fetch(url)
    except Exception as e:
        return -1   # -1 = failed, but picklable

# ─────────────────────────────────────────────────────────────────────────────
# 1. Sequential — one at a time
# ─────────────────────────────────────────────────────────────────────────────
def run_sequential():
    start = time.time()
    results = [fetch(url) for url in URLS]
    return time.time() - start, len(results)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Threading — OS threads, GIL released during network wait
#    GIL does NOT block I/O threads — they all wait in parallel
# ─────────────────────────────────────────────────────────────────────────────
def run_threading():
    start = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=N) as executor:
        futures = {executor.submit(fetch, url): url for url in URLS}
        for future in as_completed(futures):
            results.append(future.result())
    return time.time() - start, len(results)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Multiprocessing — true OS processes, bypasses GIL entirely
#    Overkill for I/O but shows it works; notice startup overhead
#    Each process = separate Python interpreter = ~50MB+ RAM each
# ─────────────────────────────────────────────────────────────────────────────
def run_multiprocessing():
    start = time.time()
    results = []
    # limit workers so we don't spawn 20 processes (expensive)
    workers = min(N, multiprocessing.cpu_count() * 2)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(fetch_process_safe, url) for url in URLS]
        for future in as_completed(futures):
            results.append(future.result())
    return time.time() - start, len(results)

# ─────────────────────────────────────────────────────────────────────────────
# 4. Asyncio — 1 thread, event loop switches coroutines while waiting
#    await = "I'm waiting for network, run something else meanwhile"
#    asyncio.gather = fire all N at once, collect when each finishes
# ─────────────────────────────────────────────────────────────────────────────
async def fetch_async(session, url):
    async with session.get(url) as response:
        data = await response.read()   # pause here → event loop runs other tasks
        return len(data)

async def _run_asyncio():
    import aiohttp
    # limit=0 removes the default per-host connection cap (default=100, fine here)
    # limit_per_host=0 removes per-host limit so all N fire truly simultaneously
    connector = aiohttp.TCPConnector(limit=0, limit_per_host=0)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_async(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)   # all N fire simultaneously
    return results

def run_asyncio():
    start = time.time()
    results = asyncio.run(_run_asyncio())
    return time.time() - start, len(results)

# ─────────────────────────────────────────────────────────────────────────────
# Main — run all, print comparison table
# ─────────────────────────────────────────────────────────────────────────────
def print_table(rows):
    header = f"{'Approach':<20} {'Time':>7}  {'URLs done':>9}  {'Speedup vs seq':>14}  Notes"
    print()
    print(header)
    print("─" * 75)
    seq_time = rows[0][1]
    for name, elapsed, count, notes in rows:
        speedup = seq_time / elapsed if elapsed > 0 else 0
        print(f"  {name:<18} {elapsed:>6.1f}s  {count:>9}  {speedup:>12.1f}x  {notes}")
    print()

def main():
    print(f"Benchmarking {N} URLs (each takes ~1s to respond)")
    print("This will take ~20s for sequential + ~1–3s each for the rest\n")

    rows = []

    # Skip sequential if N is large to save time — comment out if you want the full run
    print("1/4  sequential ...", end=" ", flush=True)
    try:
        t, n = run_sequential()
        rows.append(("sequential", t, n, f"1 at a time, {t:.0f}s as expected"))
        print(f"{t:.1f}s")
    except Exception as e:
        print(f"FAILED: {e}")
        rows.append(("sequential", N * 1.0, N, "estimated (skipped)"))

    print("2/4  threading  ...", end=" ", flush=True)
    try:
        t, n = run_threading()
        rows.append(("threading", t, n, f"GIL released for I/O, {N} OS threads"))
        print(f"{t:.1f}s")
    except Exception as e:
        print(f"FAILED: {e}")

    print("3/4  multiproc  ...", end=" ", flush=True)
    try:
        t, n = run_multiprocessing()
        rows.append(("multiprocessing", t, n, f"true processes, overkill for I/O"))
        print(f"{t:.1f}s")
    except Exception as e:
        print(f"FAILED: {e}")

    print("4/4  asyncio    ...", end=" ", flush=True)
    try:
        t, n = run_asyncio()
        rows.append(("asyncio", t, n, f"1 thread, event loop, {N} coroutines"))
        print(f"{t:.1f}s")
    except ImportError:
        print("SKIPPED (pip install aiohttp)")
    except Exception as e:
        print(f"FAILED: {e}")

    if rows:
        print_table(rows)

    print("""
MEMORY comparison for 1,000 concurrent requests:
  sequential      N/A       — not concurrent
  threading       ~1 GB     — 1000 × ~1MB OS thread stack
  multiprocessing ~50 GB    — 1000 × ~50MB process (never do this)
  asyncio         ~50 MB    — 1000 coroutines, single thread heap

JAVA comparison (for reference, not benchmarked here):
  Java threads           same as Python threading, ~1GB for 1000, no GIL
  Java virtual threads   like asyncio but as threads, 100k+ for pennies (Java 21+)

WHEN TO USE WHAT:
  Sequential       < 5 URLs, order matters, simple scripts
  threading        I/O bound, quick to write, existing sync code
  multiprocessing  CPU bound (math, compression, ML inference)
  asyncio          100+ URLs, production scrapers, low memory
  Java v-threads   Java 21+, same ergonomics as threads but asyncio scale

RULE OF THUMB — scraping at scale:

  < 1,000 URLs
    Python asyncio alone — dead simple, one event loop, ~50MB

  1,000 – 10,000,000 URLs
    asyncio + multiprocessing:
      10 processes × 1,000 coroutines each = 10,000 concurrent I/O
      CPU cores parse HTML in parallel while coroutines fetch
      Pattern: multiprocessing.Pool → each worker runs its own asyncio.run()

  10M+ URLs, distributed cluster
    Apache Spark — but use it for the PIPELINE, not the HTTP calls
      mapPartitions: each partition runs its own async scraper
      Spark handles fault tolerance, retries, data distribution
      Don't use Spark's RDD collect for HTTP — too slow per record

  Java shop (Java 21+)
    Virtual threads (Project Loom):
      Thread.ofVirtual().start(...)  or  Executors.newVirtualThreadPerTaskExecutor()
      JVM schedules on N OS threads (carrier threads), not 1:1
      100,000+ virtual threads with low overhead
      Same blocking code style as regular threads — no async/await syntax needed
      Better CPU utilization than asyncio for CPU-heavy parsing
""")


if __name__ == "__main__":
    # multiprocessing guard — required on macOS/Windows
    multiprocessing.freeze_support()
    main()
