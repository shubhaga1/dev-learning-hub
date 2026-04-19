"""
benchmark.py — fixed evaluation harness. DO NOT MODIFY.

Mirrors prepare.py in karpathy/autoresearch.
The agent only edits algorithm.py. This file is ground truth.

Metric: ops_per_sec — how many solve() calls complete in BUDGET_SECONDS.
        Higher is better.
        A "correct" flag also checks that answers match the reference.

Usage:
    python benchmark.py            # single run
    python benchmark.py > run.log  # capture output (agent usage)
"""

import time
import random
import sys
import traceback

# ── Fixed constants — do not change ──────────────────────────────────────────

SEED           = 42
BUDGET_SECONDS = 30       # fixed wall-clock window, like Karpathy's 5-min budget
WARMUP_SECONDS = 2        # excluded from measurement (JIT, import overhead)
SIZES          = [100, 1_000, 10_000]  # workload sizes mixed during measurement

random.seed(SEED)

# Pre-generate fixed workloads so the agent can't cheat by caching
WORKLOADS = {
    size: [random.randint(0, size * 10) for _ in range(size)]
    for size in SIZES
}

# Ground-truth answers (reference sort)
REFERENCE = {size: sorted(data) for size, data in WORKLOADS.items()}


# ── Evaluation ────────────────────────────────────────────────────────────────

def evaluate():
    """
    Import and benchmark algorithm.py's solve() function.
    Returns a dict with all stats, prints a summary block.
    """
    try:
        from algorithm import solve  # agent edits this
    except Exception:
        print("IMPORT ERROR:")
        traceback.print_exc()
        return None

    # ── Correctness check ─────────────────────────────────────────────────────
    correct = True
    for size in SIZES:
        try:
            result = solve(list(WORKLOADS[size]))  # pass a copy — solve may sort in-place
            if result != REFERENCE[size]:
                correct = False
                print(f"CORRECTNESS FAIL at size={size}: output does not match reference sort")
                break
        except Exception:
            correct = False
            print(f"RUNTIME ERROR at size={size}:")
            traceback.print_exc()
            break

    if not correct:
        _print_summary(ops_per_sec=0.0, correct=False, elapsed=0.0)
        return {"ops_per_sec": 0.0, "correct": False}

    # ── Warmup (excluded from measurement) ───────────────────────────────────
    warmup_end = time.perf_counter() + WARMUP_SECONDS
    while time.perf_counter() < warmup_end:
        size = random.choice(SIZES)
        solve(list(WORKLOADS[size]))

    # ── Timed measurement window ──────────────────────────────────────────────
    ops         = 0
    start       = time.perf_counter()
    deadline    = start + BUDGET_SECONDS
    size_idx    = 0

    while time.perf_counter() < deadline:
        size = SIZES[size_idx % len(SIZES)]
        solve(list(WORKLOADS[size]))
        ops      += 1
        size_idx += 1

    elapsed     = time.perf_counter() - start
    ops_per_sec = ops / elapsed

    _print_summary(ops_per_sec, correct=True, elapsed=elapsed)
    return {"ops_per_sec": ops_per_sec, "correct": True}


def _print_summary(ops_per_sec: float, correct: bool, elapsed: float) -> None:
    print("---")
    print(f"ops_per_sec: {ops_per_sec:.2f}")
    print(f"correct:     {correct}")
    print(f"elapsed_sec: {elapsed:.1f}")
    print(f"budget_sec:  {BUDGET_SECONDS}")


if __name__ == "__main__":
    result = evaluate()
    if result is None or not result["correct"]:
        sys.exit(1)
