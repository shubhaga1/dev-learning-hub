import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable, Client

# ============================================================
# WHAT IS LANGSMITH?
#
# LangSmith = observability dashboard for LangChain apps
# It automatically records every:
#   - prompt sent to Claude
#   - response received
#   - latency (how long it took)
#   - token usage (how much it cost)
#   - errors
#
# Think of it like: browser DevTools but for AI apps
#
# View traces at: smith.langchain.com → learning-journal project
#
# PRINT ORDER:
#   1. STEP 1 — Auto tracing (just works via .env settings)
#   2. STEP 2 — @traceable decorator (trace your own functions)
#   3. STEP 3 — Nested traces (trace inside trace)
#   4. STEP 4 — View trace URL in terminal
# ============================================================


# ============================================================
# STEP 1: Auto tracing
# Because LANGCHAIN_TRACING_V2=true is in .env,
# every LangChain call is automatically traced — no extra code!
# ============================================================
print("\n" + "="*50)
print("STEP 1: Auto tracing — just works!")
print("="*50)

llm    = ChatOllama(model="llama3.2")
prompt = ChatPromptTemplate.from_template("What is {topic} in one sentence?")
parser = StrOutputParser()
chain  = prompt | llm | parser

result = chain.invoke({"topic": "LangSmith"})
print(f"[AutoTrace] Result: {result}")
print(f"[AutoTrace] ✅ This call was automatically traced!")
print(f"[AutoTrace] View at: smith.langchain.com → learning-journal")

input("\nPress Enter to go to STEP 2...\n")


# ============================================================
# STEP 2: @traceable decorator
# Use this to trace YOUR OWN functions — not just LangChain calls
# ============================================================
print("="*50)
print("STEP 2: @traceable decorator")
print("="*50)

@traceable(name="answer-question")  # name shows in LangSmith dashboard
def answer_question(question: str) -> str:
    """
    This function is now traced in LangSmith.
    LangSmith records: inputs, outputs, latency, errors.
    """
    prompt_text = ChatPromptTemplate.from_template("Answer this question briefly: {question}")
    chain       = prompt_text | llm | parser
    return chain.invoke({"question": question})

questions = [
    "What is Docker?",
    "What is a vector database?",
]

for q in questions:
    answer = answer_question(q)
    print(f"\n[Traceable] Q: {q}")
    print(f"[Traceable] A: {answer}")

input("\nPress Enter to go to STEP 3...\n")


# ============================================================
# STEP 3: Nested traces
# A parent function calling child functions — all traced together
# LangSmith shows the full tree in dashboard
# ============================================================
print("="*50)
print("STEP 3: Nested traces (parent → child)")
print("="*50)

@traceable(name="summarize")
def summarize(text: str) -> str:
    p = ChatPromptTemplate.from_template("Summarize in one line: {text}")
    return (p | llm | parser).invoke({"text": text})

@traceable(name="translate")
def translate(text: str, language: str) -> str:
    p = ChatPromptTemplate.from_template("Translate to {language}: {text}")
    return (p | llm | parser).invoke({"text": text, "language": language})

@traceable(name="summarize-and-translate")  # parent trace
def summarize_and_translate(text: str, language: str) -> dict:
    summary     = summarize(text)        # child trace 1
    translation = translate(summary, language)  # child trace 2
    return {"summary": summary, "translation": translation}

text = "LangSmith helps developers debug, monitor, and improve LLM applications by providing detailed traces of every call."
result = summarize_and_translate(text, "Hindi")

print(f"[Nested] Original : {text[:60]}...")
print(f"[Nested] Summary  : {result['summary']}")
print(f"[Nested] In Hindi : {result['translation']}")
print(f"\n[Nested] ✅ LangSmith shows parent + 2 children as a tree!")

input("\nPress Enter to go to STEP 4...\n")


# ============================================================
# STEP 4: Get trace URL directly in terminal
# ============================================================
print("="*50)
print("STEP 4: Get trace URL")
print("="*50)

client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"))

# List the 3 most recent runs in our project
runs = list(client.list_runs(
    project_name="learning-journal",
    limit=3
))

print(f"[LangSmith] Latest 3 traces in 'learning-journal':")
for run in runs:
    print(f"\n  Name    : {run.name}")
    print(f"  Status  : {run.status}")
    print(f"  Latency : {run.end_time - run.start_time if run.end_time else 'running'}")
    print(f"  URL     : https://smith.langchain.com/public/{run.id}/r")

print("\n✅ Done! Open smith.langchain.com to see all traces.")
