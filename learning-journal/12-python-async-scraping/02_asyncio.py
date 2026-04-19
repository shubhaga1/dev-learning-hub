"""
ASYNCIO — scraping without threads

THREADS vs ASYNCIO:
  Threads:  OS creates real threads, context switching overhead
            each thread uses ~1MB of stack memory
            10 threads = 10MB, 1000 threads = 1GB (expensive)

  Asyncio:  ONE thread, ONE event loop
            never blocks — when waiting for I/O, switches to next task
            1000 "coroutines" use almost no extra memory
            perfect for high-concurrency scraping

HOW ASYNCIO WORKS:
  event loop = a scheduler that runs coroutines
  await      = "I'm waiting for I/O, run something else meanwhile"
  async def  = a coroutine (a function that can be paused/resumed)

Install: pip install aiohttp
"""

import asyncio
import aiohttp
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URLS = [f"https://httpbin.org/delay/1?id={i}" for i in range(10)]

# ── Asyncio approach ──────────────────────────────────────────────────────────
async def fetch_async(session, url):
    """Coroutine — pauses at 'await', lets other coroutines run."""
    async with session.get(url) as response:
        data = await response.read()   # await = pause here, run others
        return len(data)

async def scrape_all():
    print("── asyncio (one thread, event loop) ──")
    start = time.time()

    async with aiohttp.ClientSession() as session:
        # create all 10 tasks — they all start immediately
        tasks = [fetch_async(session, url) for url in URLS]

        # gather = run all concurrently, collect results
        results = await asyncio.gather(*tasks)

        for i, size in enumerate(results):
            print(f"  fetched id={i}  size={size}")

    elapsed = time.time() - start
    print(f"  Total: {elapsed:.1f}s  (one thread handled all 10)\n")
    return results

# ── Visual: what the event loop does ─────────────────────────────────────────
async def event_loop_demo():
    """Shows how asyncio switches between tasks while waiting."""
    print("── Event loop switching demo ──")

    async def task(name, delay):
        print(f"  {name}: started")
        await asyncio.sleep(delay)      # simulate waiting for network
        print(f"  {name}: done after {delay}s")
        return name

    # all three start, event loop switches between them while each waits
    results = await asyncio.gather(
        task("URL-1", 1.0),
        task("URL-2", 0.5),
        task("URL-3", 0.8),
    )
    print(f"  All done: {results}\n")
    # total time ≈ 1.0s (slowest), not 2.3s (sum)

# ── Comparison ────────────────────────────────────────────────────────────────
def comparison():
    print("""
THREADS vs ASYNCIO vs SEQUENTIAL:

  Sequential       10s    simple, one at a time
  ThreadPool        1s    real OS threads, GIL released for I/O
  Asyncio           1s    one thread, event loop, lowest memory

MEMORY comparison for 1000 concurrent requests:
  Threads:  1000 × ~1MB stack  = ~1GB RAM
  Asyncio:  1000 coroutines    = ~50MB RAM  (20x less)

WHEN TO USE WHAT:
  Sequential   → simple scripts, < 5 URLs, order matters
  ThreadPool   → I/O bound, quick to write, existing sync code
  Asyncio      → high concurrency (100+ URLs), production scrapers

FOR YOUR 22 URLS:
  ThreadPoolExecutor(max_workers=22) → simplest, fast enough
  asyncio → if you need to scale to 1000+ later
""")

if __name__ == "__main__":
    # event loop demo first (no install needed)
    asyncio.run(event_loop_demo())

    comparison()

    # asyncio scraping (needs: pip install aiohttp)
    try:
        asyncio.run(scrape_all())
    except ImportError:
        print("aiohttp not installed — run: pip install aiohttp")
    except Exception as e:
        print(f"Network error (need internet): {e}")
