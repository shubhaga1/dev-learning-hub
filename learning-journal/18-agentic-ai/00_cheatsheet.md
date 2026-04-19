# Agentic AI — Cheatsheet

---

## 1. The Core Loop (Everything else is built on this)

```
PERCEIVE → REASON → ACT → OBSERVE → repeat
```

A model answers once and stops.
An agent loops until the goal is achieved.

---

## 2. Model vs Agent

| | Model | Agent |
|---|---|---|
| What it does | Input → Output, done | Loops, uses tools, remembers |
| Example | "What is 2+2?" → "4" | "Book me a flight" → searches, compares, books |
| State | Stateless | Stateful |
| Initiative | Passive | Active |

Rule of thumb: if the task needs more than one step or external data → agent.

---

## 3. Types of Agents

| Type | Lives in | Examples |
|------|---------|---------|
| Software | Code/APIs | Chatbots, AutoResearcher, coding agents |
| Physical | Real world | Robots, self-driving cars |
| Hybrid | Both | Drone + navigation AI |

---

## 4. Evolution

```
Rule-based      → if/else hardcoded         (1980s)
ML-based        → learned patterns          (2010s)
LLM-powered     → reason in language        (now)
```

LLM agents: handle ambiguity, multi-step reasoning, no explicit programming per scenario.

---

## 5. When to Build an Agent (not a script)

Build an agent when:
- Steps can't be predetermined (dynamic path)
- Needs to use external tools (search, DB, APIs)
- State must persist across turns
- Problem requires reasoning, not just pattern matching

Build a script when:
- Steps are fixed and known upfront
- No external lookups needed
- Speed and reliability matter more than flexibility

---

## 6. Core Architecture (4 Components)

```
┌─────────────────────────────────────────────┐
│                   AGENT                     │
│                                             │
│  PERCEIVE  →  REASON  →  ACT               │
│  (input)     (LLM)      (tools/APIs)        │
│                ↕                            │
│            MEMORY                           │
│     (short-term: messages)                  │
│     (long-term:  vector DB / JSON)          │
└─────────────────────────────────────────────┘
```

---

## 7. Memory Types

| Type | Scope | Implementation | Example |
|------|-------|---------------|---------|
| Short-term | Current session | Message list (context window) | Conversation history |
| Long-term | Across sessions | JSON file / vector DB | User preferences, past decisions |
| Semantic | Meaning-based retrieval | Embeddings + similarity search | "Find notes about encryption" |

Key insight: without memory, every turn starts from scratch — the agent can't learn or improve.

---

## 8. Orchestration Patterns

| Pattern | Structure | Use when |
|---------|-----------|---------|
| Sequential | A → B → C | Fixed steps, known order |
| Tool-using | Agent picks tools dynamically | Flexible, open-ended tasks |
| Planner-Executor | Planner decides steps, Executor runs each | Complex multi-step tasks |
| Multi-agent | Agent A delegates to Agent B | Specialized sub-tasks |

---

## POC Files in This Directory

```
01_perceive_reason_act.py   — the core loop, bare minimum
02_model_vs_agent.py        — side-by-side: model call vs agent loop
03_agent_with_tools.py      — tool use: calculator, memory, file ops
04_memory_systems.py        — short-term + long-term memory
05_orchestration.py         — sequential + planner-executor patterns
```
