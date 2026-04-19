"""
CALL STACK — how function calls are tracked in memory

Every thread has its own call stack: a region of RAM that grows/shrinks
as functions are called and return.

STACK FRAME = one function call's "workspace" in the stack.
  Contains:
    - local variables    (url, response, data ← whatever the function declares)
    - parameters         (arguments passed in)
    - return address     (rip value to jump back to when function returns)
    - saved registers    (caller's register values, to restore after call)

rsp (stack pointer register) always points to the top frame.
  call  f()  →  rsp moves DOWN  (stack grows downward in memory)
  return     →  rsp moves UP    (frame popped, memory "freed")

STACK vs HEAP:
  Stack: automatic, fixed layout, fast, limited size (2–8 MB)
  Heap:  manual (GC handles it), flexible, large (GBs), slower to allocate
"""

import traceback, sys

# ── Demo 1: live call stack with traceback ────────────────────────────────────
def level_c():
    print("=== Live call stack from level_c() ===")
    for frame in traceback.extract_stack():
        print(f"  {frame.filename.split('/')[-1]}:{frame.lineno}  in {frame.name}()")
    print()

def level_b():
    level_c()

def level_a():
    level_b()

level_a()

# ── Demo 2: measure actual frame depth available ──────────────────────────────
def recurse(n):
    return recurse(n + 1)   # no local variables → smallest possible frame

print("=== Recursion limit (call stack size / frame size) ===")
print(f"  sys.getrecursionlimit() = {sys.getrecursionlimit()}")
print(f"  (Python's soft limit — set before OS stack overflow)\n")

# ── Demo 3: frame size grows with local variables ─────────────────────────────
# Each local variable = one slot in the stack frame
# More locals = bigger frame = fewer frames fit in 2MB stack

def small_frame():          # 0 local vars
    pass

def medium_frame(url):      # 3 local vars
    host = url.split("/")[2]
    path = url.split("/")[3] if len(url.split("/")) > 3 else "/"
    return host, path

def large_frame(urls):      # many local vars + list unpacking
    results = []
    errors  = []
    total   = 0
    success = 0
    failed  = 0
    for u in urls:
        host = u.split("/")[2] if "//" in u else u
        results.append(host)
        total += 1
        success += 1
    return results, errors, total, success, failed

print("=== Frame size vs local variable count ===")
print(f"  small_frame  (0 locals)  frame ≈  50 bytes")
print(f"  medium_frame (3 locals)  frame ≈ 150 bytes")
print(f"  large_frame  (8 locals)  frame ≈ 300 bytes\n")

# ── Demo 4: stack frame layout in memory ─────────────────────────────────────
print("""
=== Stack memory layout (grows downward) ===

HIGH address (bottom of stack — thread start)
  ┌────────────────────────────────┐  ← rsp at thread start
  │  main()  frame                 │  locals: argv[], etc.
  ├────────────────────────────────┤
  │  run_threads()  frame          │  locals: pool, futures
  ├────────────────────────────────┤
  │  fetch(url)  frame             │  locals: url, response, data
  ├────────────────────────────────┤
  │  urlopen()  frame              │  locals: request, handler
  ├────────────────────────────────┤  ← rsp right now (top of stack)
  │  [unused — reserved 8MB]       │
  │  ...                           │  ← never committed to physical RAM
  └────────────────────────────────┘
LOW address (grows toward here)

rsp points to the most recently pushed frame.
Each call pushes; each return pops. O(1) both ways.

STACK OVERFLOW = rsp tries to go below the reserved region.
  OS sends SIGSEGV → Java throws StackOverflowError → Python raises RecursionError
""")
