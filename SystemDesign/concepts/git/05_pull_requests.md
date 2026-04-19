# Git — Pull Requests

A PR is a request to merge your branch into another branch.
It gives you (or a reviewer) a chance to see the full diff before the code lands in `main`.

---

## git push vs gh pr create — what each does

These are two completely separate steps.

```
git push     → moves commits from your machine → GitHub server
               your branch is now on GitHub, but main is UNTOUCHED

gh pr create → opens a Pull Request on GitHub
               creates a webpage showing the diff
               adds a Merge button that lands your branch into main
```

```
Without PR:
  git push → main (code lands directly, no review step)

With PR flow:
  git push → fix/my-branch (branch on GitHub, main untouched)
                  ↓
             gh pr create → PR webpage with full diff
                  ↓
             Merge PR → main (code lands after review)
```

---

## Full PR workflow

```bash
# 1. Create a branch — never work directly on main
git checkout -b fix/queue-warnings
#   naming convention:
#   fix/  → bug fixes
#   feat/ → new feature
#   chore/ → cleanup, tooling, no logic change

# 2. Make changes, commit as usual
git add queue/06_CustomQueueLinkedList.java
git commit -m "Add custom queue implementation using linked list"

# Multiple commits on the same branch is fine
git add array/Array2D.java
git commit -m "Fix resource leak — wrap Scanner in try-with-resources"

# 3. Push the branch to GitHub
git push -u origin fix/queue-warnings
#   -u sets upstream so future `git push` works without arguments

# 4. Create the PR
gh pr create --title "Fix queue warnings" --body "Description here"
#   GitHub prints the PR URL, e.g: https://github.com/you/repo/pull/1

# 5. Review the diff
gh pr view --web        # open PR in browser — see every line changed
gh pr diff              # see diff in terminal

# 6. Merge the PR
gh pr merge 1 --merge   # merge commit (preserves branch history)
gh pr merge 1 --squash  # squash all commits into one
gh pr merge 1 --rebase  # rebase commits onto main (linear history)

# 7. Clean up branch
git checkout main
git pull                          # sync main with the merged changes
git branch -d fix/queue-warnings  # delete local branch
git push origin --delete fix/queue-warnings  # delete remote branch
```

---

## Writing good PR descriptions

A good PR body answers three questions:
1. **What** changed (list of files / features)
2. **Why** it was needed (the problem being solved)
3. **How to verify** it works (test plan)

```markdown
## What changed
- Moved `ListNode` to static inner class in all LinkedList files
- Wrapped Scanner usage in try-with-resources (resource leak fix)
- Implemented `Trie.startsWith()` — was a TODO returning false

## Why
All LinkedList files were defining a top-level `ListNode` class.
When compiled together on one classpath, Java sees duplicate class definitions.
Static inner class scopes it to the file — no conflict.

## Test plan
- [ ] Full project compiles: `find . -name "*.java" | xargs javac -d target`
- [ ] `rj LinkedListCycleDetection` runs correctly
- [ ] VSCode shows no red underlines in LinkedList/
```

---

## Viewing and navigating a PR

```bash
# List all open PRs
gh pr list

# View a specific PR in terminal
gh pr view 1

# See the diff in terminal
gh pr diff 1

# Open in browser (shows line-by-line diff with colors)
gh pr view 1 --web

# Check if PR can be merged (no conflicts)
gh pr checks 1
```

---

## Grouping commits inside a PR

Each commit inside a PR should be a logical unit on its own.
Think of commits as chapters in a story — each one moves the narrative forward.

```
❌ Bad — one giant commit
   "Fix everything"

✅ Good — grouped by concern
   Commit 1: "Fix LinkedList — move ListNode to static inner class"
   Commit 2: "Add Queue series — 10 files covering basics to Josephus"  
   Commit 3: "Fix compiler warnings — resource leaks, raw types, Trie TODO"
```

A reviewer can read commit 1, understand it fully, then move to commit 2.
If something breaks, `git bisect` can pinpoint which commit caused it.

---

## When to use a PR vs direct push to main

```
Use PR when:
  ✅ Working in a team — others review before merge
  ✅ You want to see the full diff before it lands
  ✅ Company policy requires PR approval
  ✅ The change is large or risky

Direct push to main is fine when:
  ✅ Solo learning repo — no collaborators
  ✅ Tiny change (typo fix, one-line patch)
  ✅ You've already reviewed the diff locally with git diff
```

---

## After merge — stay in sync

```bash
# Switch back to main
git checkout main

# Pull the merged changes from GitHub
git pull

# Your local main now has everything from the PR
git log --oneline -5
```

If you started new work on a branch while the PR was open:
```bash
# Rebase your new branch on top of updated main
git checkout feat/new-feature
git rebase main        # replays your commits on top of latest main
```

---

## Real example — what we ran today

```bash
# Branch
git checkout -b fix/project-wide-cleanup

# 3 focused commits
git add .classpath LinkedList/
git commit -m "Fix LinkedList files — move ListNode to static inner class to resolve duplicate class errors"

git add queue/
git commit -m "Add Queue series — 10 files covering basics to internals, interview patterns, and classic problems"

git add array/ fundamentals/ misc/ searching/ tree/
git commit -m "Fix compiler warnings across project — resource leaks, raw types, unused vars, Trie TODO"

# Push branch
git push -u origin fix/project-wide-cleanup

# Create PR with full description
gh pr create \
  --base master \
  --title "Queue series + project-wide fixes (classpath, warnings, LinkedList)" \
  --body "..."
# → https://github.com/shubhaga1/algorithms/pull/1

# After reviewing diff on GitHub → Merge PR → git checkout master && git pull
```
