"""
POC 5 — Orchestration Patterns

Three patterns shown side by side on the same task:
  Task: "Research a topic, summarize it, save the summary, and email it"

PATTERN 1 — Sequential
  step1 → step2 → step3 → step4
  Fixed order. No LLM decides the steps. Predictable.

PATTERN 2 — Tool-using Agent
  LLM decides which tools to call and in what order.
  Flexible. Adapts. LLM is the orchestrator.

PATTERN 3 — Planner → Executor
  Planner LLM: "Here are the steps: [1, 2, 3, 4]"
  Executor LLM: runs each step, reports result
  Separation of concerns. Easier to debug.

Run: python3 05_orchestration.py
"""

import json
import anthropic

client = anthropic.Anthropic()
SEP    = "=" * 55


# ── Shared mock tools (same set, used by all patterns) ────────────────────────

def research_topic(topic: str) -> str:
    """Simulate web research (in real agent: call search API)."""
    return f"[Research result for '{topic}'] Key finding: {topic} involves multiple components including design, implementation, and testing phases."


def summarize_text(text: str) -> str:
    """Summarize using LLM."""
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=128,
        messages=[{"role": "user", "content": f"Summarize in 2 sentences: {text}"}],
    )
    return resp.content[0].text.strip()


def save_summary(topic: str, summary: str) -> str:
    """Simulate saving to a database."""
    return f"[Saved] '{topic}' summary stored in DB."


def send_email(recipient: str, subject: str, body: str) -> str:
    """Simulate sending an email."""
    return f"[Email sent] To: {recipient} | Subject: {subject}"


# ═══════════════════════════════════════════════════════════
# PATTERN 1 — SEQUENTIAL (hardcoded pipeline)
#
# You define the steps. You define the order.
# No LLM decides anything about orchestration.
# Simple, fast, predictable. Breaks if requirements change.
# ═══════════════════════════════════════════════════════════

def pattern_sequential(topic: str, recipient: str) -> None:
    print(f"\n{SEP}")
    print("PATTERN 1 — SEQUENTIAL (hardcoded pipeline)")
    print(SEP)
    print(f"Topic: {topic}")

    # Step 1
    print("\nStep 1: Research")
    raw = research_topic(topic)
    print(f"  → {raw[:60]}...")

    # Step 2
    print("Step 2: Summarize")
    summary = summarize_text(raw)
    print(f"  → {summary[:60]}...")

    # Step 3
    print("Step 3: Save")
    saved = save_summary(topic, summary)
    print(f"  → {saved}")

    # Step 4
    print("Step 4: Email")
    emailed = send_email(recipient, f"Summary: {topic}", summary)
    print(f"  → {emailed}")

    print("\n✓ Done. Steps were fixed — code decided the order, not the LLM.")
    print("  Pro: Fast, predictable. Con: Can't adapt if steps change.")


# ═══════════════════════════════════════════════════════════
# PATTERN 2 — TOOL-USING AGENT
#
# LLM decides which tools to call and in what order.
# You give it a goal. It figures out the steps.
# Flexible — can skip steps, reorder, handle edge cases.
# ═══════════════════════════════════════════════════════════

AGENT_TOOLS = [
    {
        "name": "research_topic",
        "description": "Search and gather information about a topic.",
        "input_schema": {
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    },
    {
        "name": "summarize_text",
        "description": "Summarize a long piece of text into 2 sentences.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "save_summary",
        "description": "Save a topic summary to the database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic":   {"type": "string"},
                "summary": {"type": "string"},
            },
            "required": ["topic", "summary"],
        },
    },
    {
        "name": "send_email",
        "description": "Send an email with the summary.",
        "input_schema": {
            "type": "object",
            "properties": {
                "recipient": {"type": "string"},
                "subject":   {"type": "string"},
                "body":      {"type": "string"},
            },
            "required": ["recipient", "subject", "body"],
        },
    },
]


def _run_tool(name: str, inputs: dict) -> str:
    """Dispatch tool call to its implementation."""
    if name == "research_topic":  return research_topic(inputs["topic"])
    if name == "summarize_text":  return summarize_text(inputs["text"])
    if name == "save_summary":    return save_summary(inputs["topic"], inputs["summary"])
    if name == "send_email":      return send_email(inputs["recipient"], inputs["subject"], inputs["body"])
    return "Unknown tool"


def pattern_tool_using_agent(topic: str, recipient: str) -> None:
    print(f"\n{SEP}")
    print("PATTERN 2 — TOOL-USING AGENT (LLM decides steps)")
    print(SEP)

    goal = (
        f"Research '{topic}', summarize it, save the summary, "
        f"then email it to {recipient} with an appropriate subject line."
    )
    print(f"Goal given to agent: {goal}\n")

    messages = [{"role": "user", "content": goal}]
    turn     = 0

    while True:
        turn += 1
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            tools=AGENT_TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            final = next((b.text for b in response.content if hasattr(b, "text")), "")
            print(f"\nAgent final: {final}")
            print(f"\n✓ Done in {turn} turns. LLM decided the tool order autonomously.")
            break

        elif response.stop_reason == "tool_use":
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [Turn {turn}] Agent calls: {block.name}({list(block.input.keys())})")
                    result = _run_tool(block.name, block.input)
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            messages.append({"role": "user", "content": results})


# ═══════════════════════════════════════════════════════════
# PATTERN 3 — PLANNER → EXECUTOR
#
# Two separate LLM calls:
#   PLANNER: given the goal, outputs a JSON plan (list of steps)
#   EXECUTOR: runs each step in the plan, one at a time
#
# Why separate?
#   - Easier to inspect/debug the plan before running it
#   - Planner can be a smarter (more expensive) model
#   - Executor can be a faster (cheaper) model
#   - Human can approve the plan before execution (human-in-the-loop)
# ═══════════════════════════════════════════════════════════

def planner(goal: str) -> list[dict]:
    """Generate a structured plan for the goal."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=(
            "You are a planner. Given a goal, output a JSON array of steps. "
            "Each step: {\"step\": N, \"action\": \"tool_name\", \"description\": \"what to do\"}. "
            "Available actions: research_topic, summarize_text, save_summary, send_email. "
            "Output ONLY valid JSON, no prose."
        ),
        messages=[{"role": "user", "content": f"Goal: {goal}"}],
    )
    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def executor(plan: list[dict], context: dict) -> dict:
    """Execute each step in the plan. context carries data between steps."""
    for step in plan:
        action = step["action"]
        desc   = step["description"]
        print(f"\n  Step {step['step']}: {action}")
        print(f"  → {desc}")

        # Map plan step to actual tool call
        if action == "research_topic":
            context["research"] = research_topic(context.get("topic", ""))

        elif action == "summarize_text":
            context["summary"] = summarize_text(context.get("research", ""))

        elif action == "save_summary":
            result = save_summary(context.get("topic", ""), context.get("summary", ""))
            print(f"  ✓ {result}")

        elif action == "send_email":
            result = send_email(
                context.get("recipient", ""),
                f"Summary: {context.get('topic', '')}",
                context.get("summary", ""),
            )
            print(f"  ✓ {result}")

    return context


def pattern_planner_executor(topic: str, recipient: str) -> None:
    print(f"\n{SEP}")
    print("PATTERN 3 — PLANNER → EXECUTOR (separation of concerns)")
    print(SEP)

    goal = f"Research '{topic}', summarize it, save it, and email it to {recipient}."

    # PLANNER: generate the plan
    print("Planner generating steps...")
    plan = planner(goal)
    print(f"\nPlan generated ({len(plan)} steps):")
    for s in plan:
        print(f"  Step {s['step']}: [{s['action']}] {s['description']}")

    # ← In a real system, a human could approve this plan here before execution

    # EXECUTOR: run each step
    print("\nExecutor running plan...")
    context = {"topic": topic, "recipient": recipient}
    executor(plan, context)

    print(f"\n✓ Done.")
    print("  Pro: Plan is inspectable/auditable before execution.")
    print("  Pro: Planner and Executor can use different models.")
    print("  Pro: Easy to add human-in-the-loop approval step.")


# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    TOPIC     = "distributed key-value stores"
    RECIPIENT = "shubham@example.com"

    print(SEP)
    print("ORCHESTRATION PATTERNS — POC")
    print(SEP)
    print(f"Same task, 3 different orchestration approaches.")

    pattern_sequential(TOPIC, RECIPIENT)
    pattern_tool_using_agent(TOPIC, RECIPIENT)
    pattern_planner_executor(TOPIC, RECIPIENT)

    print(f"\n{SEP}")
    print("WHEN TO USE WHICH")
    print(SEP)
    print("""
  Sequential      → steps are always the same, order is fixed
                    fastest, simplest, most reliable

  Tool-using      → steps vary by input, LLM adapts the path
                    most flexible, handles edge cases

  Planner-Exec    → complex tasks, want to inspect plan first
                    good for human-in-the-loop, audit trails
                    can optimize each phase independently
    """)
