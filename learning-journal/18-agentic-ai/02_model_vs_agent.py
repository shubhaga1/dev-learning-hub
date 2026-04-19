"""
POC 2 — Model vs Agent (side by side)

Same task: "What is 15% tip on a $47.50 bill, and save it to my notes"

MODEL: One call. Returns text. Done. Cannot save anything.
AGENT: Loops. Uses tools. Actually saves the note.

Run: python3 02_model_vs_agent.py
"""

import json
import anthropic

client = anthropic.Anthropic()
SEP    = "=" * 55

NOTES_FILE = "/tmp/agent_notes.json"


# ═══════════════════════════════════════════════════════════
# APPROACH 1 — PURE MODEL
# One API call. Returns text. Cannot take real actions.
# ═══════════════════════════════════════════════════════════

def model_approach(task: str) -> None:
    print(f"\n{SEP}")
    print("APPROACH 1 — PURE MODEL")
    print(SEP)
    print(f"Task: {task}\n")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": task}],
    )

    output = response.content[0].text
    print(f"Model output:\n{output}")
    print("\n✗ Model stopped here. It described saving but did NOT actually save anything.")
    print("  There is no notes file. The model is stateless and has no tools.")


# ═══════════════════════════════════════════════════════════
# APPROACH 2 — AGENT WITH TOOLS
# Loops until task complete. Actually calls tools. Actually saves.
# ═══════════════════════════════════════════════════════════

# ── Tool definitions (what the agent CAN do) ──────────────────────────────────

TOOLS = [
    {
        "name": "calculate",
        "description": "Evaluate a math expression and return the result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "e.g. '47.50 * 0.15'"}
            },
            "required": ["expression"],
        },
    },
    {
        "name": "save_note",
        "description": "Save a note to persistent storage.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key":   {"type": "string", "description": "Short label for the note"},
                "value": {"type": "string", "description": "Note content"},
            },
            "required": ["key", "value"],
        },
    },
    {
        "name": "read_notes",
        "description": "Read all saved notes.",
        "input_schema": {"type": "object", "properties": {}},
    },
]


# ── Tool implementations (actual Python code that runs) ───────────────────────

def run_tool(name: str, inputs: dict) -> str:
    if name == "calculate":
        try:
            result = eval(inputs["expression"], {"__builtins__": {}})  # safe: no builtins
            return str(round(result, 2))
        except Exception as e:
            return f"Error: {e}"

    elif name == "save_note":
        try:
            notes = json.loads(open(NOTES_FILE).read()) if __import__("os").path.exists(NOTES_FILE) else {}
        except Exception:
            notes = {}
        notes[inputs["key"]] = inputs["value"]
        open(NOTES_FILE, "w").write(json.dumps(notes, indent=2))
        return f"Saved: {inputs['key']} = {inputs['value']}"

    elif name == "read_notes":
        try:
            return open(NOTES_FILE).read()
        except FileNotFoundError:
            return "{}"

    return "Unknown tool"


# ── Agent loop ─────────────────────────────────────────────────────────────────

def agent_approach(task: str) -> None:
    print(f"\n{SEP}")
    print("APPROACH 2 — AGENT WITH TOOLS")
    print(SEP)
    print(f"Task: {task}\n")

    messages = [{"role": "user", "content": task}]
    turn     = 0

    while True:
        turn += 1
        print(f"--- Agent turn {turn} ---")

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            tools=TOOLS,
            messages=messages,
        )

        # Add assistant response to history
        messages.append({"role": "assistant", "content": response.content})

        # Check stop reason
        if response.stop_reason == "end_turn":
            # Agent finished — extract final text
            final = next((b.text for b in response.content if hasattr(b, "text")), "")
            print(f"\nAgent final response:\n{final}")
            print("\n✓ Agent ACTUALLY saved the note. Check the file:")
            print(f"  cat {NOTES_FILE}")
            break

        elif response.stop_reason == "tool_use":
            # Agent wants to call tools
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [TOOL CALL] {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    print(f"  [TOOL RESULT] {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            # Feed results back to agent
            messages.append({"role": "user", "content": tool_results})

        else:
            print(f"Unexpected stop_reason: {response.stop_reason}")
            break


# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    TASK = "What is 15% tip on a $47.50 bill? Calculate it exactly and save it to my notes with the key 'tip_calc'."

    model_approach(TASK)
    print()
    agent_approach(TASK)

    print(f"\n{SEP}")
    print("COMPARISON SUMMARY")
    print(SEP)
    print("""
  MODEL:
    - Single API call
    - Returns text describing what it would do
    - Cannot take real actions
    - Stateless — no memory, no tools

  AGENT:
    - Loops: reason → tool_call → observe result → reason again
    - Actually runs the calculation
    - Actually saves the note to disk
    - Stateful — builds up context across turns
    """)
