"""
LEARNING PATH: Scraping & Systems Internals
============================================

Two tracks that connect — understand WHY, then apply the HOW.

TRACK A — CPU & Memory (the "why things are fast or slow")
  01_cpu_registers.py     CPU registers: rip, rsp, rax — the CPU's scratchpad
  02_virtual_memory.py    Virtual vs physical RAM, pages, reserve vs commit
  03_call_stack.py        Stack frames, frame size, rsp, recursion limit
  04_context_switch.py    What gets saved on a thread switch, cost, cache flush

TRACK B — Python Concurrency (the "how to handle 1000+ URLs")
  05_concurrency_models.py   Sequential / threading / multiprocessing / asyncio
  06_benchmark.py            Live timing: all 4 models against real URLs
  07_scale_rules.py          Rule of thumb: 1k / 10M / 10M+ URLs + Java

READ ORDER (recommended):
  01 → 02 → 03 → 04  (build the mental model)
  05 → 06 → 07        (apply it to scraping)

KEY CONNECTIONS:
  01 explains WHAT gets saved during a context switch (04)
  02 explains WHY thread stacks look expensive but aren't (reserved ≠ used)
  03 explains WHY deep recursion crashes (call stack is finite RAM)
  04 explains WHY asyncio beats threads at 1000+ concurrency (no switches)

QUICK REFERENCE:
  I/O bound task (scraping, DB, API calls):
    < 100 URLs  → threading (simplest)
    100–10k     → asyncio (lowest memory, fast)
    10k+        → asyncio + multiprocessing (10 procs × 1k coroutines)

  CPU bound task (parsing HTML, ML inference, compression):
    → multiprocessing (bypasses GIL, true parallelism)
    → Java (no GIL at all, virtual threads in Java 21)

PREREQUISITES: basic Python (functions, imports, loops)
"""
