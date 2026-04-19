# 06 — LangChain + LangSmith

## What you learn here
- **LangChain** — framework to build apps with LLMs using chains
- **LangSmith** — observability dashboard to debug and monitor LLM apps

## Prerequisites
```bash
pip install langchain-anthropic langsmith langchain-core
```

## Run order
```bash
python 01_langchain_demo.py   # learn chains first
python 02_langsmith_demo.py   # then tracing
```

## Key concepts

### LangChain — what is a chain?
```python
# Instead of raw API calls:
response = claude.invoke("explain docker")

# You build reusable chains:
chain = prompt | llm | parser
chain.invoke({"topic": "docker"})   # same topic, different input
chain.invoke({"topic": "k8s"})      # reuse the same chain
```

### The | (pipe) operator
```
prompt | llm | parser
  ↓       ↓      ↓
format → call → extract text
```

### LangSmith — what does it track?
| What | Example |
|---|---|
| Prompt sent | "Explain Docker in one sentence" |
| Response received | "Docker is a containerization platform..." |
| Latency | 1.2 seconds |
| Token usage | 45 input, 32 output |
| Cost | $0.0003 |

### @traceable decorator
```python
@traceable(name="my-function")
def my_function(input):
    # everything inside is tracked in LangSmith
    return chain.invoke(input)
```

### LangSmith vs no LangSmith
```
Without LangSmith:  App fails → no idea why
With LangSmith:     App fails → see exact prompt, response, error in dashboard
```

## View traces
Open: smith.langchain.com → learning-journal project
