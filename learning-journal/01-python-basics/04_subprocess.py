"""
SUBPROCESS — Run terminal commands from Python

subprocess lets Python start any program that you could run in your terminal.
Think of it as Python pressing Enter on a command for you.

  Terminal:  ls -la
  Python:    subprocess.run(["ls", "-la"])

Why it matters for revise.py:
  subprocess.run(["claude", "-p", prompt])
  → Python starts the claude CLI
  → passes the prompt as an argument
  → claude prints its response to the terminal
"""

import subprocess

# ============================================================
# PART 1: subprocess.run — the main function
# ============================================================

print("=" * 55)
print("  PART 1: subprocess.run basics")
print("=" * 55)

# run() takes a LIST — first item = the command, rest = arguments
# same as typing: echo "hello from subprocess"
result = subprocess.run(["echo", "hello from subprocess"])

print(f"\nreturncode: {result.returncode}")
# returncode 0 = success, anything else = error (unix convention)


# ============================================================
# PART 2: capture the output instead of printing it
# ============================================================

print("\n" + "=" * 55)
print("  PART 2: capture output with capture_output=True")
print("=" * 55)

# By default, output goes straight to terminal (you see it but can't use it)
# capture_output=True → output stored in result.stdout instead

result = subprocess.run(
    ["echo", "captured output"],
    capture_output=True,   # don't print — store it
    text=True              # give me a string, not bytes
)

print(f"stdout:     '{result.stdout.strip()}'")  # 'captured output'
print(f"stderr:     '{result.stderr.strip()}'")  # empty (no errors)
print(f"returncode:  {result.returncode}")        # 0


# ============================================================
# PART 3: passing a longer argument (like a prompt to claude)
# ============================================================

print("\n" + "=" * 55)
print("  PART 3: multi-word arguments")
print("=" * 55)

# Wrong: subprocess.run(["echo", "hello", "world"])  → treats as two args
# Right: subprocess.run(["echo", "hello world"])     → one string argument

result = subprocess.run(
    ["echo", "this is one argument"],
    capture_output=True,
    text=True
)
print(f"output: '{result.stdout.strip()}'")

# For claude specifically:
#   subprocess.run(["claude", "-p", "your entire prompt as one string"])
#   -p flag = --print (non-interactive, just print the response and exit)


# ============================================================
# PART 4: check=True — raise exception on failure
# ============================================================

print("\n" + "=" * 55)
print("  PART 4: check=True — fail loudly on error")
print("=" * 55)

# Without check=True: subprocess silently returns returncode=1, script continues
# With check=True:    raises CalledProcessError if command fails

try:
    subprocess.run(
        ["ls", "/this/does/not/exist"],
        check=True,
        capture_output=True,
        text=True
    )
except subprocess.CalledProcessError as e:
    print(f"Command failed! returncode={e.returncode}")
    print(f"stderr: {e.stderr.strip()}")

# Safe run: command succeeds
result = subprocess.run(
    ["ls", "/tmp"],
    check=True,
    capture_output=True,
    text=True
)
print(f"\nls /tmp first 3 items: {result.stdout.split()[:3]}")


# ============================================================
# PART 5: how revise.py calls claude
# ============================================================

print("\n" + "=" * 55)
print("  PART 5: how revise.py calls claude")
print("=" * 55)

print("""
In revise.py, this is what happens:

  prompt = "You are reviewing a revision output... [long text]"

  subprocess.run(["claude", "-p", prompt], check=True)

Step by step:
  1. Python calls subprocess.run()
  2. OS starts a NEW process — the claude binary
     (/Users/shubhamgarg/.local/bin/claude)
  3. Passes ["-p", prompt] as command-line arguments
     (same as typing: claude -p "your prompt" in terminal)
  4. claude runs, prints its response to the terminal
  5. When claude finishes, subprocess.run() returns
  6. Python continues to the next line

No capture_output here — output goes straight to terminal
so you see Claude's response in real time as it streams.
""")


# ============================================================
# PART 6: run a real command — git log (safe, no side effects)
# ============================================================

print("=" * 55)
print("  PART 6: real example — run git log from Python")
print("=" * 55)

result = subprocess.run(
    ["git", "log", "--oneline", "-3"],
    capture_output=True,
    text=True,
    cwd="/Users/shubhamgarg/Downloads/Code/SystemDesign"  # run in this folder
)

if result.returncode == 0:
    print("Last 3 commits in SystemDesign:")
    for line in result.stdout.strip().split("\n"):
        print(f"  {line}")
else:
    print("git not available or not a repo")


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 55)
print("  SUMMARY")
print("=" * 55)
print("""
subprocess.run(cmd, **options)

  cmd              list of strings: ["git", "log", "--oneline"]
                   NEVER a single string with spaces — that's a shell injection risk

  capture_output   True  → store stdout/stderr in result
                   False → print directly to terminal (default)

  text             True  → stdout/stderr as str
                   False → as bytes (default)

  check            True  → raise CalledProcessError on failure
                   False → silent failure (default)

  cwd              which folder to run the command in

result object:
  result.stdout      captured output (if capture_output=True)
  result.stderr      captured errors
  result.returncode  0 = success, non-zero = error

How claude is called:
  subprocess.run(["claude", "-p", prompt], check=True)
  → starts claude binary
  → -p = print mode (non-interactive)
  → prompt = the entire question as one string argument
  → output streams to terminal in real time
""")
