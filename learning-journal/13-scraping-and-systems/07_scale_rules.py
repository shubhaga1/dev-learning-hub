"""
SCALE RULES — when to use what, from 1 URL to 10M+

This is a decision guide, not runnable code.
Read after running 06_benchmark.py so the numbers are concrete.

TECHNOLOGY COMPARISON TABLE:
─────────────────────────────────────────────────────────────────────────────
Technology              Concurrency Model           Max Parallel  Overhead
─────────────────────────────────────────────────────────────────────────────
Sequential              none                        1             none
Python threading        OS threads, GIL on I/O      500–1000      medium
Python multiprocessing  true processes, no GIL      CPU cores×2   high
Python asyncio          event loop (1 thread)       10,000+       very low
PySpark                 JVM tasks + Python workers  executor cores very high
Spark (Scala/Java)      JVM tasks                   executor cores high
Java threads            OS threads, no GIL          500–1000      medium
Java virtual threads    JVM-managed (Project Loom)  100,000+      very low
─────────────────────────────────────────────────────────────────────────────

RULE OF THUMB — scraping at scale:

< 1,000 URLs:
  Python asyncio alone
    - one event loop, one thread
    - ~50MB RAM for 1000 coroutines
    - pip install aiohttp + asyncio.gather()
    - dead simple, no infrastructure needed

1,000 – 10,000,000 URLs:
  asyncio + multiprocessing  (hybrid approach)
    - 10 processes × 1,000 coroutines = 10,000 concurrent I/O
    - each process runs its own asyncio.run()
    - multiprocessing handles CPU work (HTML parsing, deduplication)
    - asyncio handles I/O (fetching)

    Pattern:
      def worker(url_chunk):
          asyncio.run(scrape_chunk(url_chunk))   # each process owns its loop

      with ProcessPoolExecutor(max_workers=10) as pool:
          pool.map(worker, chunks(all_urls, 1000))

10M+ URLs — distributed cluster:
  Apache Spark  (but use it for the PIPELINE, not the HTTP calls)
    - Spark handles: distribution, fault tolerance, retries, data storage
    - Inside each partition: run your async scraper, not Spark's HTTP
    - Pattern: mapPartitions → each partition runs async scraper in worker

    PySpark:
      def scrape_partition(urls):
          return asyncio.run(scrape_batch(list(urls)))

      rdd.mapPartitions(scrape_partition)

    Scala/Java Spark: use Java virtual threads inside mapPartitions

Java shop (Java 21+) — Virtual Threads (Project Loom):
  - Thread.ofVirtual().start(runnable)
  - Executors.newVirtualThreadPerTaskExecutor()
  - JVM schedules virtual threads on N carrier (OS) threads
  - 100,000+ virtual threads, same blocking-style code as regular threads
  - NO async/await syntax needed — looks like sequential code
  - Better CPU utilization for parsing (no GIL)
  - Same scale as asyncio, better ergonomics for Java teams

  Example:
    try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
        urls.forEach(url -> exec.submit(() -> fetch(url)));
    }  // blocks until all done, handles 100k+ urls easily


MEMORY COMPARISON (1,000 concurrent requests):
  sequential          N/A         not concurrent
  threading           ~1 GB       1000 × ~1MB OS thread stack (reserved, ~4KB used)
  multiprocessing     ~50 GB      1000 × ~50MB process  ← never do this for I/O
  asyncio             ~50 MB      1000 coroutines on 1 thread heap
  Java virtual thread ~100 MB     JVM overhead per vthread ~1KB + JVM base


WHAT THE TABLE MEANS FOR YOUR 22 URLS (from the original question):
  ThreadPoolExecutor(max_workers=22)   → simplest, done in ~1s, fine
  asyncio                              → same speed, less memory, scales later
  Both are correct answers for 22 URLs.
  Go async if you expect to grow to 1000+.
"""
