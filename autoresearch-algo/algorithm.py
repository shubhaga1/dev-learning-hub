"""
algorithm.py — the agent edits this file. Mirrors train.py in karpathy/autoresearch.

Rules:
  - Must export a single function: solve(data: list[int]) -> list[int]
  - solve() must return a sorted copy or sorted in-place list
  - No external dependencies beyond the Python standard library
  - benchmark.py is ground truth — do not read or modify it

Everything in this file is fair game:
  - Sorting algorithm (quicksort, mergesort, timsort variant, radix, ...)
  - In-place vs allocating
  - Recursion vs iteration
  - Hybrid strategies (insertion sort for small arrays, etc.)
  - Any pure-Python optimization

Goal: maximize ops_per_sec from benchmark.py. Higher is better.
"""


def solve(data: list[int]) -> list[int]:
    # Baseline: Python built-in sort (Timsort).
    # Agent: try to beat this or understand why you can't.
    return sorted(data)
