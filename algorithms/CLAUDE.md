# Algorithms — Learning Project

This is a Java learning repository. The goal is clean, readable, well-commented code for studying data structures and algorithms.

## Default behavior for every code change

After every file edit or new file creation, automatically do the following **without being asked**:

1. **Point out 1–2 clean code issues** in the changed code — naming, structure, comments, Java-specific patterns
2. **Show a before/after fix** inline
3. **Give one rule to remember** — a principle that applies beyond this file

Keep it short (3–5 lines). This is a learning loop, not a full code review every time.

## Code style rules

- Method names must say what they do: `printPaths` not `path`, `collectPaths` not `pathRet`
- Base cases at the top of every recursive method
- No `System.out.println` inside library/helper methods — only in `main`
- Comments explain WHY, not WHAT
- No magic numbers — use named variables
- One method = one responsibility

## Commit messages

Always write commit messages that answer: **what changed and why** — not just what files were touched.

Good: `Add visual grid printer to Maze1Recursive to show path as * on grid`
Bad: `Update Maze1Recursive.java`

## Package structure

| Package | Purpose |
|---|---|
| `tree/` | BST, Trie, BTree — tree data structures |
| `recursion/` | Recursion problems — maze, subsets, permutations |
| `fundamentals/` | Core Java gotchas — pass-by-value, static vs instance |
| `patterns/` | Design patterns from Venkat workshop |
| `array/`, `sorting/`, etc. | Standard DSA topics |
