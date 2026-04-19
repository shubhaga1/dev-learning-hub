# Code Quality — Clean Code + Code Review

Hands-on examples progressing from Level 1 to Level 10.
Each file shows: BAD code → Review comments → FIXED code → Runnable test.

---

## The 5 Pillars of Code Review

Based on industry best practices (Anil / Tesco framework):

| Pillar | Question to ask in review | File |
|---|---|---|
| **Readability** | Can a new dev understand this in 60 seconds? | `00`, `01`, `03` |
| **Scalability** | Can this handle 10x load / new features without a rewrite? | `06` |
| **Maintainability** | Can one dev change this without breaking others? | `07` |
| **Modularity** | Is each class/function doing exactly one thing? | `02`, `08` |
| **Non-redundancy** | Is any logic copy-pasted? | `05` |

---

## Files — Level 1 to 10

| File | Topic | What you learn |
|---|---|---|
| `00_naming_clean_code.py` | Clean Naming | Functions=verbs, variables=nouns, no abbreviations |
| `01_naming_and_clarity.py` | Naming & Clarity | Meaningful names, readable intent |
| `02_single_responsibility.py` | SRP | One function = one job |
| `03_magic_numbers.py` | Constants | Name every number and threshold |
| `04_error_handling.py` | Exceptions | Specific errors, no bare except, no silent returns |
| `05_dry_principle.py` | DRY | Extract repeated logic into one place |
| `06_scalability_open_closed.py` | Open/Closed | Add features without editing existing code |
| `07_maintainability_dependency_injection.py` | DI | Inject deps, don't hardcode — makes testing easy |
| `08_modularity_composition.py` | Composition | Compose behaviours instead of deep inheritance |
| `09_security_and_validation.py` | Security | Parameterized queries, input validation |
| `10_performance_complexity.py` | Complexity | O(n²) vs O(n), N+1 queries, string concat traps |

---

## How to Run Any File

```bash
cd learning-journal/10-code-quality
python3 01_naming_and_clarity.py
```

---

## Code Review Checklist (use in PRs)

```
Readability
  [ ] Function names are verbs, variables are nouns
  [ ] No single-letter variables except loop counters
  [ ] No magic numbers — all thresholds named as constants
  [ ] Javadoc/docstring on every public method

Scalability
  [ ] No if/elif chains that grow with new types (use polymorphism)
  [ ] No hardcoded limits or environment-specific values

Maintainability
  [ ] Dependencies injected, not created inside class
  [ ] Can test each component in isolation

Modularity
  [ ] Function does ONE thing (no "and" in the description)
  [ ] Classes are small, focused, single-purpose

Non-redundancy
  [ ] No copy-pasted logic — extract to shared function
  [ ] No duplicate constants — define once, import everywhere

Security
  [ ] No string interpolation in SQL — use parameterized queries
  [ ] All user inputs validated at entry point

Performance
  [ ] No nested loops over same data (O(n²))
  [ ] No N+1 DB queries in a loop — batch fetch
  [ ] No string += in loops — use list.join()
```

---

## Tools Used in Industry

| Tool | Purpose |
|---|---|
| **Crucible** (Atlassian) | Code review comments and tracking |
| **Fisheye** (Atlassian) | Repository browsing and diff visualization |
| **SonarQube** | Static analysis — finds bugs, smells, coverage |
| **pylint / flake8** | Python linting |
| **Checkstyle** | Java style enforcement |
| All integrate with **Jira** for traceability |

---

*By Shubham Garg — Engineering Manager*
