# autoresearch-algo

Autonomous algorithm performance research. You are an AI agent that iteratively improves
a Python sorting algorithm by running experiments, measuring throughput, and keeping
only changes that improve the metric.

This is directly inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch).
Same loop. Different domain: algorithm performance instead of LLM training.

---

## Setup

Work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `apr18`).
   The branch `autoresearch/<tag>` must not already exist.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current main.
3. **Read the in-scope files**:
   - `benchmark.py` — fixed evaluation harness. **Do not modify.**
   - `algorithm.py` — the file you edit. Contains `solve()`.
4. **Initialize results.tsv**: Create it with just the header row (see Logging section).
5. **Run the baseline**: always run as-is first to record baseline performance.
6. **Confirm with user** then kick off the loop.

---

## What you CAN do

- Modify `algorithm.py` — this is the **only** file you edit.
- Change the sorting algorithm entirely (quicksort, radix, merge, hybrid, etc.)
- Optimize memory allocation, recursion depth, branching
- Add helper functions inside `algorithm.py`
- Use any Python standard library module (`bisect`, `heapq`, `array`, `ctypes`, etc.)

## What you CANNOT do

- Modify `benchmark.py` — it is read-only ground truth
- Install external packages (no numpy, no C extensions)
- Cache results between calls or read the workload data ahead of time
- Change the function signature: must remain `solve(data: list[int]) -> list[int]`

---

## The metric

**ops_per_sec** — how many `solve()` calls complete in 30 seconds across mixed workload sizes.
**Higher is better.**

The benchmark also checks correctness. A run that fails correctness scores 0 ops/sec.

Extract the metric from the log:
```bash
grep "^ops_per_sec:" run.log
```

---

## Running an experiment

```bash
python benchmark.py > run.log 2>&1
```

Do NOT let output flood your context — always redirect to `run.log`.

If the grep output is empty, the run crashed. Read the stack trace:
```bash
tail -n 40 run.log
```

Each benchmark run takes exactly **30 seconds** (plus a 2-second warmup).
If a run exceeds 60 seconds wall clock, kill it and treat it as a crash.

---

## Logging results

Log every experiment to `results.tsv` (tab-separated, NOT comma — commas break descriptions).
Do NOT commit `results.tsv` — leave it untracked.

Header + column format:
```
commit	ops_per_sec	status	description
```

- **commit**: short 7-char git hash
- **ops_per_sec**: number from log (e.g. `184320.45`), use `0.00` for crashes
- **status**: `keep`, `discard`, or `crash`
- **description**: one-line description of what you tried

Example:
```
commit	ops_per_sec	status	description
a1b2c3d	184320.45	keep	baseline (Python built-in sorted)
b2c3d4e	201450.12	keep	introsort with insertion sort for n<16
c3d4e5f	178900.00	discard	pure recursive mergesort (call overhead)
d4e5f6g	0.00	crash	radix sort returned wrong output
```

---

## The experiment loop

LOOP FOREVER:

1. Check current git state (branch, last commit)
2. Form a hypothesis: what change might improve ops_per_sec?
3. Edit `algorithm.py` with the targeted change
4. `git commit -m "experiment: <short description>"`
5. Run: `python benchmark.py > run.log 2>&1`
6. Read result: `grep "^ops_per_sec:\|^correct:" run.log`
7. If grep is empty → crash. Read `tail -n 40 run.log`. Attempt fix if trivial, otherwise revert.
8. Log to `results.tsv`
9. If `ops_per_sec` improved → **keep** (stay on this commit, advance the branch)
10. If `ops_per_sec` equal or worse → **discard** (`git reset --hard HEAD~1`)

---

## Judgment criteria

**Simplicity matters.** All else being equal, simpler is better:
- A 1% improvement that adds 50 lines of complex code? Probably not worth it.
- A 5% improvement from a clean rewrite? Keep.
- Equal performance with cleaner code? Keep (complexity reduction is a win).
- Worse performance but much simpler code? Use judgment — note it as a simplification attempt.

**Correctness is non-negotiable.** A fast but wrong sort scores 0.

---

## Research ideas to explore (non-exhaustive)

- Insertion sort for small subarrays (< 16 elements) as a base case
- Introsort (quicksort + heapsort fallback for worst case)
- Timsort-style run detection (already in CPython, but can you beat it in pure Python?)
- Radix sort for integer-specific gains
- Dual-pivot quicksort (Java's Arrays.sort approach)
- In-place vs copy tradeoffs
- Using `list.sort()` vs `sorted()` (in-place vs copy)
- `bisect` module for insertion into sorted structure
- Three-way partitioning for data with many duplicates

Note: CPython's built-in `sorted()` is C-implemented Timsort. Pure Python will likely
be slower — the interesting research question is **by how much** and **under what conditions**
can a different algorithm or hybrid come close.

---

## Timeout / stopping

Each experiment should take ~32 seconds (30s benchmark + 2s warmup + overhead).
If a run exceeds **90 seconds**, kill it (`Ctrl+C`) and treat as crash.

**NEVER STOP the loop** once started. Do not ask "should I continue?".
Run until manually interrupted. If out of ideas, read sorting algorithm literature,
revisit near-misses, try combining previous successful ideas, experiment with
more radical approaches. The loop runs until the human stops you.

---

## Output example (what to expect)

After setup, your first few iterations might look like:

```
[iter 1] baseline: 184,320 ops/sec  → keep
[iter 2] insertion sort base case:  201,450 ops/sec  → keep (+9.3%)
[iter 3] dual-pivot quicksort:      195,200 ops/sec  → discard
[iter 4] radix sort (integers):     crash (wrong output) → fix + retry
[iter 5] radix sort (fixed):        228,100 ops/sec  → keep (+13.2%)
```

The user wakes up to a `results.tsv` full of experiments and a faster `algorithm.py`.
