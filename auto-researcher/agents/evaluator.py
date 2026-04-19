"""
Evaluator Agent — scores a skill output against all criteria.

Deterministic criteria are checked with Python logic.
Subjective criteria are delegated to the judge agent.

Returns:
  score   — float 0.0–1.0  (fraction of criteria passed)
  results — list of {id, description, passed, reason}
"""

import anthropic
from agents.judge import judge


# ── Deterministic checks (one function per criterion id) ─────────────────────

def _check_hook_length(output: str) -> tuple[bool, str]:
    first_line = output.split("\n")[0]
    passed = len(first_line) <= 136
    return passed, f"Hook is {len(first_line)} chars ({'ok' if passed else 'too long, max 136'})"


def _check_no_asterisk_bullets(output: str) -> tuple[bool, str]:
    bad_lines = [l for l in output.split("\n") if l.strip().startswith("*")]
    passed = len(bad_lines) == 0
    return passed, "No asterisk bullets" if passed else f"Found {len(bad_lines)} asterisk bullet(s)"


def _check_short_paragraphs(output: str) -> tuple[bool, str]:
    paragraphs = [p.strip() for p in output.split("\n\n") if p.strip()]
    long_ones = [p for p in paragraphs if len(p.split(".")) > 4]  # >3 sentences
    passed = len(long_ones) == 0
    return passed, "All paragraphs short" if passed else f"{len(long_ones)} paragraph(s) exceed 3 sentences"


DETERMINISTIC_CHECKS = {
    "hook_length": _check_hook_length,
    "no_asterisk_bullets": _check_no_asterisk_bullets,
    "short_paragraphs": _check_short_paragraphs,
}


# ── Main evaluator ────────────────────────────────────────────────────────────

def evaluate(
    output: str,
    criteria: list[dict],
    client: anthropic.Anthropic,
) -> tuple[float, list[dict]]:
    """
    Score output against all criteria.

    Returns:
        score   — 0.0 to 1.0
        results — per-criterion {id, description, passed, reason}
    """
    results = []

    for criterion in criteria:
        cid = criterion["id"]

        if criterion["type"] == "deterministic":
            check_fn = DETERMINISTIC_CHECKS.get(cid)
            if check_fn is None:
                raise ValueError(f"No deterministic check implemented for criterion '{cid}'")
            passed, reason = check_fn(output)

        elif criterion["type"] == "ai_judge":
            passed, reason = judge(output, criterion, client)

        else:
            raise ValueError(f"Unknown criterion type: {criterion['type']}")

        results.append({
            "id": cid,
            "description": criterion["description"],
            "passed": passed,
            "reason": reason,
        })

    score = sum(1 for r in results if r["passed"]) / len(results)
    return score, results
