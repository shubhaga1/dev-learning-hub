"""
Judge Agent — AI-powered evaluator for subjective criteria.

Used when a deterministic script can't decide (e.g. "is the hook engaging?").
Returns (passed: bool, reason: str).
"""

import anthropic


def judge(output: str, criterion: dict, client: anthropic.Anthropic) -> tuple[bool, str]:
    """
    Ask Claude to evaluate a subjective criterion.

    Args:
        output:    The LinkedIn post to evaluate.
        criterion: Criterion dict with 'prompt' field describing what to check.
        client:    Shared Anthropic client.

    Returns:
        (passed, reason) — bool and one-sentence explanation.
    """
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=(
            "You are a strict evaluator for AI-generated content. "
            "Answer exactly as instructed — start with YES or NO."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"{criterion['prompt']}\n\n"
                    f"--- POST ---\n{output}\n--- END ---"
                ),
            }
        ],
    )

    reply = response.content[0].text.strip()
    passed = reply.upper().startswith("YES")
    reason = reply  # full reply includes the reasoning sentence
    return passed, reason
