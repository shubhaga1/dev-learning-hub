"""
POC 3 — Core Agent Architecture (all 4 components)

  PERCEIVE  → takes input
  REASON    → LLM decides next action
  MEMORY    → stores context (short-term) + facts (long-term)
  ACT       → runs tools

Tools available to this agent:
  calculator  — evaluates math
  save_fact   — stores a fact in long-term memory (JSON file)
  recall_fact — retrieves a stored fact
  list_facts  — shows all stored facts

Run: python3 03_agent_with_tools.py
"""

import json
import os
import anthropic

client    = anthropic.Anthropic()
SEP       = "-" * 55
FACTS_DB  = "/tmp/agent_facts.json"          # long-term memory store


# ═══════════════════════════════════════════════════════════
# COMPONENT 1 — MEMORY
# ═══════════════════════════════════════════════════════════

class Memory:
    """
    Short-term: messages list (in-context, lost when session ends)
    Long-term:  JSON file (persists across sessions)
    """

    def __init__(self):
        self.short_term: list = []           # conversation history

    # ── Short-term ────────────────────────────────────────────────────────────

    def remember_exchange(self, role: str, content) -> None:
        self.short_term.append({"role": role, "content": content})

    def get_history(self) -> list:
        return self.short_term

    # ── Long-term ─────────────────────────────────────────────────────────────

    @staticmethod
    def save_fact(key: str, value: str) -> str:
        facts = Memory._load_facts()
        facts[key] = value
        with open(FACTS_DB, "w") as f:
            json.dump(facts, f, indent=2)
        return f"Saved: '{key}' = '{value}'"

    @staticmethod
    def recall_fact(key: str) -> str:
        facts = Memory._load_facts()
        return facts.get(key, f"No fact found for key '{key}'")

    @staticmethod
    def list_facts() -> str:
        facts = Memory._load_facts()
        if not facts:
            return "No facts stored yet."
        return json.dumps(facts, indent=2)

    @staticmethod
    def _load_facts() -> dict:
        if os.path.exists(FACTS_DB):
            with open(FACTS_DB) as f:
                return json.load(f)
        return {}


# ═══════════════════════════════════════════════════════════
# COMPONENT 2 — TOOLS (the ACT layer)
# ═══════════════════════════════════════════════════════════

TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate a math expression. Use Python syntax.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "e.g. '(100 * 1.18) / 12'"}
            },
            "required": ["expression"],
        },
    },
    {
        "name": "save_fact",
        "description": "Store a fact in long-term memory for future recall.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key":   {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["key", "value"],
        },
    },
    {
        "name": "recall_fact",
        "description": "Retrieve a previously stored fact by key.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string"}
            },
            "required": ["key"],
        },
    },
    {
        "name": "list_facts",
        "description": "Show all facts stored in long-term memory.",
        "input_schema": {"type": "object", "properties": {}},
    },
]


def execute_tool(name: str, inputs: dict) -> str:
    """ACT — run the tool and return result string."""
    if name == "calculator":
        try:
            result = eval(inputs["expression"], {"__builtins__": {}})
            return str(round(float(result), 4))
        except Exception as e:
            return f"Error: {e}"
    elif name == "save_fact":
        return Memory.save_fact(inputs["key"], inputs["value"])
    elif name == "recall_fact":
        return Memory.recall_fact(inputs["key"])
    elif name == "list_facts":
        return Memory.list_facts()
    return "Unknown tool"


# ═══════════════════════════════════════════════════════════
# COMPONENT 3 — AGENT (PERCEIVE + REASON loop)
# ═══════════════════════════════════════════════════════════

class Agent:
    def __init__(self):
        self.memory = Memory()

    def perceive(self, user_input: str) -> str:
        """Receive input from the environment."""
        print(f"\n[PERCEIVE] '{user_input}'")
        return user_input

    def reason(self) -> object:
        """Call LLM with full history + available tools."""
        return client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=(
                "You are an assistant agent with tools. "
                "Use tools when needed. Be concise in your final responses."
            ),
            tools=TOOLS,
            messages=self.memory.get_history(),
        )

    def act(self, response) -> list:
        """Execute any tool calls the LLM requested."""
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[ACT]     tool={block.name}  input={block.input}")
                result = execute_tool(block.name, block.input)
                print(f"[ACT]     result={result}")
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })
        return results

    def run(self, user_input: str) -> str:
        """Full perceive → reason → act loop for one user request."""
        # Perceive
        self.memory.remember_exchange("user", self.perceive(user_input))

        while True:
            # Reason
            response = self.reason()
            self.memory.remember_exchange("assistant", response.content)

            if response.stop_reason == "end_turn":
                # Final answer
                final = next((b.text for b in response.content if hasattr(b, "text")), "")
                print(f"[REASON]  Final answer: {final}")
                return final

            elif response.stop_reason == "tool_use":
                # Act — run tools, feed results back
                tool_results = self.act(response)
                self.memory.remember_exchange("user", tool_results)

            else:
                return f"Unexpected stop: {response.stop_reason}"


# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    agent = Agent()

    print("=" * 55)
    print("CORE AGENT ARCHITECTURE POC")
    print("=" * 55)
    print("Components: Perceive + Reason + Memory (short+long) + Act")

    # Task 1: calculate and remember
    print(f"\n{SEP}")
    print("TASK 1: Calculate and remember monthly payment")
    agent.run("If I borrow $12,000 at 8% annual interest for 3 years, what's the monthly payment? Save it as 'loan_monthly'.")

    # Task 2: recall from long-term memory (proves persistence)
    print(f"\n{SEP}")
    print("TASK 2: Recall from long-term memory")
    agent.run("What was my monthly loan payment? Check your memory.")

    # Task 3: show all stored facts
    print(f"\n{SEP}")
    print("TASK 3: What do you know about me?")
    agent.run("List everything you have stored in long-term memory.")

    print(f"\n{SEP}")
    print("Architecture demonstrated:")
    print("  PERCEIVE  — user input received")
    print("  REASON    — LLM decided which tools to call")
    print("  ACT       — tools executed (calculator, save_fact, recall_fact)")
    print("  MEMORY    — short-term kept full history; long-term persisted to disk")
