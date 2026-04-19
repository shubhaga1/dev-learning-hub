"""
POC 1 — Perceive → Reason → Act Loop

The simplest possible agent.
No tools. No memory. Just the loop structure.

Run:  python3 01_perceive_reason_act.py
"""

import anthropic

client = anthropic.Anthropic()

SEP = "-" * 50


# ── The 3 steps ───────────────────────────────────────────────────────────────

def perceive(user_input: str) -> str:
    """Step 1: Take raw input from the environment (user, sensor, event)."""
    print(f"\n[PERCEIVE] Input received: '{user_input}'")
    return user_input


def reason(observation: str, history: list) -> str:
    """Step 2: Use LLM to decide what to do next."""
    history.append({"role": "user", "content": observation})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=(
            "You are a helpful agent. Respond concisely. "
            "If the user's request is fully resolved, end with [DONE]. "
            "If you need more information, ask one question."
        ),
        messages=history,
    )

    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})
    print(f"[REASON]  LLM decided: '{reply[:80]}...' " if len(reply) > 80 else f"[REASON]  LLM decided: '{reply}'")
    return reply


def act(decision: str) -> str:
    """Step 3: Execute the decision. Here we just print — in real agents this calls tools/APIs."""
    print(f"[ACT]     Executing output...")
    return decision


# ── Agent loop ─────────────────────────────────────────────────────────────────

def run_agent(initial_input: str, max_turns: int = 5):
    """
    The loop:
      perceive → reason → act → observe result → repeat

    Stops when:
      - LLM signals [DONE]
      - Max turns reached
      - User types 'quit'
    """
    print(SEP)
    print("AGENT STARTED")
    print(SEP)

    history  = []
    turn     = 0
    input_   = initial_input

    while turn < max_turns:
        turn += 1
        print(f"\n=== Turn {turn} ===")

        # 1. Perceive
        observation = perceive(input_)

        # 2. Reason
        decision = reason(observation, history)

        # 3. Act
        output = act(decision)

        # Check if agent considers task complete
        if "[DONE]" in output:
            print(f"\n[AGENT] Task complete after {turn} turn(s).")
            break

        # Get next input (in a real agent this comes from the environment, not a human)
        print(f"\nAgent output: {output}")
        input_ = input("\nYour response (or 'quit'): ").strip()
        if input_.lower() == "quit":
            break

    print(f"\n{SEP}")
    print(f"AGENT STOPPED after {turn} turn(s)")
    print(SEP)


# ── What this shows ───────────────────────────────────────────────────────────
#
# Turn 1: User says something → agent reasons → agent responds
# Turn 2: User responds → agent reasons again → closer to goal
# Turn N: Agent reaches [DONE] → loop exits
#
# This is the SAME loop that powers:
#   - GitHub Copilot Workspace
#   - AutoResearcher (karpathy/autoresearch)
#   - Claude Code (this tool you're using right now)
#
# The only difference is what happens in ACT:
#   - Simple: print output
#   - Complex: call tools, write files, run code, search the web

if __name__ == "__main__":
    print("""
What this POC shows:
  The Perceive → Reason → Act loop is the foundation of every agent.
  Watch how each turn: takes input, passes to LLM, produces output, waits.
    """)
    run_agent("I need help planning a 3-step workout routine.")
