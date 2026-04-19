import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ============================================================
# WHAT IS LANGCHAIN?
#
# LangChain = a framework to build apps with LLMs
# Instead of writing raw API calls, you build "chains":
#
#   Prompt → LLM → Output Parser → Result
#
# PRINT ORDER:
#   1. STEP 1 — Basic LLM call (just Claude, no chain)
#   2. STEP 2 — Prompt Template (reusable prompts with variables)
#   3. STEP 3 — Chain (prompt + LLM + parser piped together)
#   4. STEP 4 — Chain with different inputs
# ============================================================


# ============================================================
# STEP 1: Basic LLM call
# Just call Claude directly — no chain yet
# ============================================================
print("\n" + "="*50)
print("STEP 1: Basic LLM call")
print("="*50)

llm = ChatOllama(model="llama3.2")

response = llm.invoke("What is LangChain in one sentence?")
print(f"[Ollama] {response.content}")

input("\nPress Enter to go to STEP 2...\n")


# ============================================================
# STEP 2: Prompt Template
# Instead of hardcoding prompts, use templates with variables
# ============================================================
print("="*50)
print("STEP 2: Prompt Template")
print("="*50)

# {topic} is a variable — filled in at runtime
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms in 2 sentences."
)

# See what the prompt looks like before sending to Claude
formatted = prompt.format_messages(topic="Docker containers")
print(f"[PromptTemplate] Formatted prompt:")
print(f"  {formatted[0].content}")

input("\nPress Enter to go to STEP 3...\n")


# ============================================================
# STEP 3: Chain — pipe prompt + LLM + parser together
# The | symbol connects components like a pipeline
#
#   prompt | llm | parser
#     ↓       ↓      ↓
#   format → call → extract text
# ============================================================
print("="*50)
print("STEP 3: Chain (prompt | llm | parser)")
print("="*50)

parser = StrOutputParser()  # extracts just the text from Claude's response

# Build the chain using | (pipe operator)
chain = prompt | llm | parser

# Invoke the full chain with one input
result = chain.invoke({"topic": "Kubernetes"})
print(f"[Chain] Topic: Kubernetes")
print(f"[Chain] Result: {result}")

input("\nPress Enter to go to STEP 4...\n")


# ============================================================
# STEP 4: Same chain, different inputs
# This is the power of chains — reuse with any input
# ============================================================
print("="*50)
print("STEP 4: Reusing chain with different inputs")
print("="*50)

topics = ["Vector databases", "RAG (Retrieval Augmented Generation)", "Pinecone"]

for topic in topics:
    result = chain.invoke({"topic": topic})
    print(f"\n[Chain] Topic: {topic}")
    print(f"  → {result}")

print("\n✅ Done! Check smith.langchain.com to see all traces.")
