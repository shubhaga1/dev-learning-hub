"""
POC 4 — Memory Systems

Demonstrates the difference between short-term and long-term memory.
Also shows WHY memory matters — watch the agent fail without it, then succeed with it.

Experiments:
  1. No memory    — agent forgets everything between turns
  2. Short-term   — agent remembers within a session (context window)
  3. Long-term    — agent recalls facts from a previous session

Run: python3 04_memory_systems.py
"""

import json
import os
import anthropic

client    = anthropic.Anthropic()
SEP       = "-" * 55
MEM_FILE  = "/tmp/long_term_memory.json"


# ── Long-term memory helpers ──────────────────────────────────────────────────

def lt_save(key: str, value: str) -> None:
    mem = lt_load_all()
    mem[key] = value
    with open(MEM_FILE, "w") as f:
        json.dump(mem, f, indent=2)


def lt_get(key: str) -> str | None:
    return lt_load_all().get(key)


def lt_load_all() -> dict:
    if os.path.exists(MEM_FILE):
        with open(MEM_FILE) as f:
            return json.load(f)
    return {}


def lt_clear() -> None:
    if os.path.exists(MEM_FILE):
        os.remove(MEM_FILE)


# ── Simple LLM call ───────────────────────────────────────────────────────────

def ask(messages: list, system: str = "") -> str:
    kwargs = dict(model="claude-sonnet-4-6", max_tokens=256, messages=messages)
    if system:
        kwargs["system"] = system
    return client.messages.create(**kwargs).content[0].text.strip()


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 1 — NO MEMORY
# Each call is independent. Agent forgets immediately.
# ═══════════════════════════════════════════════════════════

def experiment_1_no_memory():
    print(SEP)
    print("EXPERIMENT 1 — NO MEMORY")
    print(SEP)

    # Turn 1
    r1 = ask([{"role": "user", "content": "My name is Shubham and I like Python."}])
    print(f"Turn 1 → Agent: {r1}")

    # Turn 2 — completely new call, no history passed
    r2 = ask([{"role": "user", "content": "What's my name and what do I like?"}])
    print(f"Turn 2 → Agent: {r2}")
    print("→ Agent has NO idea. Each API call starts fresh.")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 2 — SHORT-TERM MEMORY (messages list)
# History passed in every API call. Agent remembers within session.
# Cleared when the program exits.
# ═══════════════════════════════════════════════════════════

def experiment_2_short_term_memory():
    print(f"\n{SEP}")
    print("EXPERIMENT 2 — SHORT-TERM MEMORY (conversation history)")
    print(SEP)

    # The messages list IS the short-term memory
    messages = []

    def chat(user_msg: str) -> str:
        messages.append({"role": "user", "content": user_msg})
        reply = ask(messages)
        messages.append({"role": "assistant", "content": reply})
        return reply

    r1 = chat("My name is Shubham and I'm learning about AI agents.")
    print(f"Turn 1 → Agent: {r1}")

    r2 = chat("What's my name?")
    print(f"Turn 2 → Agent: {r2}")

    r3 = chat("What am I learning about?")
    print(f"Turn 3 → Agent: {r3}")

    print(f"\nMessages in short-term memory: {len(messages)} entries")
    print("→ Agent remembers — because we pass the full history each call.")
    print("  Limitation: if you restart the program, this list is gone.")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 3 — LONG-TERM MEMORY (persisted to disk)
# Facts survive program restarts.
# Session A saves → Session B recalls.
# ═══════════════════════════════════════════════════════════

def experiment_3_long_term_memory():
    print(f"\n{SEP}")
    print("EXPERIMENT 3 — LONG-TERM MEMORY (persists across sessions)")
    print(SEP)

    lt_clear()  # start fresh for this demo

    # ── Session A: learn and save ─────────────────────────────────────────────
    print("--- SESSION A (saving facts) ---")

    # Agent extracts and saves facts
    facts_to_remember = {
        "user_name":     "Shubham",
        "learning_topic": "AI agents and encryption",
        "preferred_language": "Python",
    }
    for key, value in facts_to_remember.items():
        lt_save(key, value)
        print(f"  Saved: {key} = '{value}'")

    print("\nSession A ended. Memory file written to disk.")
    print(f"Contents of {MEM_FILE}:")
    print(open(MEM_FILE).read())

    # ── Simulate program restart (clear any in-memory state) ─────────────────
    print("\n--- PROGRAM RESTART (simulated) ---")
    print("All Python variables cleared. Only disk file remains.\n")

    # ── Session B: recall ─────────────────────────────────────────────────────
    print("--- SESSION B (recalling facts) ---")

    # Load long-term memory, inject into system prompt
    stored_facts = lt_load_all()
    system = (
        "You are a helpful assistant. "
        f"Here is what you know about the user from previous sessions:\n{json.dumps(stored_facts, indent=2)}"
    )

    r1 = ask([{"role": "user", "content": "Do you know my name?"}], system=system)
    print(f"Q: Do you know my name?")
    print(f"A: {r1}")

    r2 = ask([{"role": "user", "content": "What am I currently learning?"}], system=system)
    print(f"\nQ: What am I currently learning?")
    print(f"A: {r2}")

    print("\n→ Agent recalled from DISK, not from context window.")
    print("  This survives restarts. This is long-term memory.")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 4 — WHY MEMORY SIZE MATTERS (context window limit)
# ═══════════════════════════════════════════════════════════

def experiment_4_context_window_limit():
    print(f"\n{SEP}")
    print("EXPERIMENT 4 — Context Window Limit (why long-term memory exists)")
    print(SEP)

    print("""
  Short-term memory = the messages list you pass to the API.

  Claude has a context window limit (~200k tokens for claude-sonnet-4-6).

  In a long conversation:
    Turn 1:    2k tokens
    Turn 100:  200k tokens  ← approaching limit
    Turn 101:  overflow → oldest messages must be dropped

  Solutions:
    1. Summarize old turns before they fall out (compression)
    2. Extract key facts and save to long-term memory (JSON / vector DB)
    3. Use RAG: embed facts, retrieve only relevant ones per turn

  Rule of thumb:
    Short-term  → what happened this session (messages list)
    Long-term   → what should ALWAYS be available (facts, user profile)
    RAG         → large knowledge base, retrieve on demand
    """)


# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 55)
    print("MEMORY SYSTEMS — POC")
    print("=" * 55)

    experiment_1_no_memory()
    experiment_2_short_term_memory()
    experiment_3_long_term_memory()
    experiment_4_context_window_limit()

    print(f"\n{SEP}")
    print("MEMORY SUMMARY")
    print(SEP)
    print("""
  No memory    → each call is stateless, agent forgets instantly
  Short-term   → messages list, lasts one session, lost on restart
  Long-term    → JSON / DB / vector store, survives restarts

  Implementation in production:
    Short-term → messages[]   passed to API each turn
    Long-term  → Redis, DynamoDB, Pinecone, or a simple JSON file
    Retrieval  → inject relevant facts into system prompt before each call
    """)
