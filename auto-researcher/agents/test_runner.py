"""
Test Runner Agent — runs the skill (system prompt) against a sample input.

Takes the current skill text and a topic, returns the generated LinkedIn post.
Uses prompt caching on the skill so repeated test runs are cheap.
"""

import anthropic


def run(skill: str, topic: str, client: anthropic.Anthropic) -> str:
    """
    Generate a LinkedIn post using the given skill (system prompt) and topic.

    Args:
        skill:  Full text of the skill markdown file (the system prompt).
        topic:  What the LinkedIn post should be about.
        client: Shared Anthropic client.

    Returns:
        The generated LinkedIn post as a string.
    """
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": skill,
                # Cache the skill — it stays constant across iterations of the same run
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Write a LinkedIn post about: {topic}",
            }
        ],
    )

    return response.content[0].text.strip()
