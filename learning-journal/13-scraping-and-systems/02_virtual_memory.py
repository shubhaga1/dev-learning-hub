"""
VIRTUAL MEMORY — the OS lie that makes everything work

Every process thinks it owns a giant private address space.
That's a lie. Physical RAM is shared. The OS manages the illusion.

  Your process sees:    0x000000 ────────────── 0xFFFFFFFFFFFF  (128 TB on 64-bit)
  Physical RAM:         8 GB / 16 GB / 32 GB  (shared by all processes)

HOW: the OS maintains a page table per process.
  page table = mapping from virtual address → physical RAM page

PAGE = the unit of memory allocation.  Always 4 KB (4096 bytes).
  RAM is divided into 4KB chunks.
  The OS allocates/frees in page units, never byte-by-byte.

RESERVE vs COMMIT (key insight for thread stacks):
  Reserve  = claim a range of virtual addresses (free, just a table entry)
  Commit   = a page is actually backed by physical RAM (costs real memory)
  Pages are committed LAZILY — only when you first write to them (page fault).
"""

import tracemalloc, sys, os

# ── Demo 1: tracemalloc — see exactly how much RAM Python allocates ───────────
tracemalloc.start()

snapshot_before = tracemalloc.take_snapshot()

big_list = [i for i in range(100_000)]   # 100k integers

snapshot_after = tracemalloc.take_snapshot()

stats = snapshot_after.compare_to(snapshot_before, 'lineno')
top = [s for s in stats if s.size_diff > 0][:3]

print("=== tracemalloc: pages committed by creating 100k list ===")
for stat in top:
    print(f"  +{stat.size_diff / 1024:.1f} KB   {stat.traceback}")

tracemalloc.stop()

# ── Demo 2: id() spacing shows page alignment ─────────────────────────────────
# Python small int cache: integers -5 to 256 are pre-allocated (same address always)
# Larger ints: each new object gets a fresh allocation

print("\n=== id() spacing — virtual address layout ===")
print(f"  id(0)   = {hex(id(0))}")
print(f"  id(1)   = {hex(id(1))}")
print(f"  id(257) = {hex(id(257))}  ← new object, different address")
a = 257
b = 257
print(f"  a=257   = {hex(id(a))}")
print(f"  b=257   = {hex(id(b))}  ← CPython may or may not reuse (compile-time optimization)")

# ── Demo 3: sys.getsizeof vs actual pages used ────────────────────────────────
print("\n=== sys.getsizeof — object sizes vs page granularity ===")
items = [[], [1], [1]*10, [1]*100, [1]*1000]
for lst in items:
    size = sys.getsizeof(lst)
    pages = (size + 4095) // 4096   # round up to page boundary
    print(f"  list len={len(lst):5}  object={size:6} bytes  pages_needed={pages}")

# ── Demo 4: reserve vs commit — thread stack reality ──────────────────────────
print("""
=== Thread stack: reserved vs actually used ===

When a thread starts, OS reserves 8MB of virtual address space for its stack.
Physical RAM is committed ONLY for pages the thread actually touches.

A scraping thread call stack (5 frames deep while waiting for network):
  main()         ~100 bytes
  run_thread()   ~50  bytes
  fetch(url)     ~200 bytes   ← url string reference + response reference
  urlopen()      ~300 bytes
  socket.read()  ~150 bytes   ← WAITING HERE 99% of the time
  ─────────────────────────
  Total used:    ~800 bytes   = 1 page (4 KB) committed

Reserved:  8 MB  (virtual address table entry — free)
Committed: 4 KB  (physical RAM — actual cost)

For 20 scraping threads:
  Reserved:   20 × 8 MB  = 160 MB  (virtual, near-free)
  Committed:  20 × 4 KB  =  80 KB  (physical RAM actually used)

The 8MB "per thread" cost you hear about is misleading for I/O-bound code.
""")
