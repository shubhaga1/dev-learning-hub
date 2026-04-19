"""
CPU REGISTERS — the CPU's own ultra-fast scratchpad

RAM (your 16GB chip) is fast but the CPU is faster.
Registers live INSIDE the CPU die — no wire, no bus, no wait.

  Speed comparison:
    L1 cache  ~4 cycles   (inside CPU, shared with registers)
    RAM       ~200 cycles (travels off-chip over memory bus)
    Disk      ~100,000 cycles

There are 16 general-purpose registers on x86-64 (your Mac/Linux):
  rax, rbx, rcx, rdx, rsi, rdi, r8–r15   ← general (math, pointers)
  rip                                      ← instruction pointer (WHERE in code)
  rsp                                      ← stack pointer (WHERE the stack top is)
  rflags                                   ← result flags (zero? negative? overflow?)

Each register = 64 bits = 8 bytes.
Total: 16 × 8 = 128 bytes.  That's the ENTIRE CPU working memory.
"""

import ctypes, sys

# ── Demo 1: id() reveals the virtual address of any Python object ─────────────
# Every Python object lives somewhere in RAM.
# id(obj) returns its virtual address — the same number the CPU uses as rsp/rip.

a = 42
b = "hello"
c = [1, 2, 3]

print("=== Virtual addresses via id() ===")
print(f"  int 42      lives at: {hex(id(a))}")
print(f"  str 'hello' lives at: {hex(id(b))}")
print(f"  list [1,2,3] lives at: {hex(id(c))}")
print(f"  Note: all start with 0x1 or 0x7 — high address space (heap)\n")

# ── Demo 2: how addition actually uses registers ──────────────────────────────
# Python:     result = a + b
# CPU does:
#   mov  rax, [address of a's value]   ← load a into register rax
#   mov  rbx, [address of b's value]   ← load b into register rbx
#   add  rax, rbx                       ← rax = rax + rbx (in-register, instant)
#   mov  [address of result], rax       ← write result back to RAM

x, y = 10, 20
result = x + y  # CPU: load x→rax, load y→rbx, add rax+rbx, store
print(f"=== Addition: {x} + {y} = {result} ===")
print("  CPU steps: load x→rax, load y→rbx, add rax+rbx, store result\n")

# ── Demo 3: rip — the instruction pointer ─────────────────────────────────────
# rip always holds the address of the NEXT instruction to run.
# When you call a function:  rip jumps to function's first instruction
# When function returns:     rip jumps back to caller's next instruction
# When OS context-switches:  rip is SAVED so thread can resume exactly here

def show_frame_address():
    frame = sys._getframe(0)            # current stack frame
    code  = frame.f_code
    line  = frame.f_lineno
    print(f"=== rip equivalent (Python frame) ===")
    print(f"  function: {code.co_name}")
    print(f"  file:     {code.co_filename.split('/')[-1]}")
    print(f"  line:     {line}   ← rip would point here")
    print(f"  frame id: {hex(id(frame))}  ← lives at this virtual address\n")

show_frame_address()

# ── Summary ───────────────────────────────────────────────────────────────────
print("""
REGISTER  SIZE   PURPOSE
──────────────────────────────────────────────────────
rip       8B     instruction pointer — "where in code am I?"
rsp       8B     stack pointer — "where is the top of my stack?"
rax       8B     accumulator — result of last arithmetic operation
rbx/rcx   8B     general purpose — hold intermediate values
rflags    8B     result of comparisons (was last op zero? negative?)

CONTEXT SWITCH connection (see 04_context_switch.py):
  When OS pauses your thread, it saves ALL 16 registers to RAM (~128 bytes).
  When your thread resumes, it restores them — rip picks up exactly mid-function.
""")
