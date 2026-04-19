import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ============================================================
# PROMPT TEMPLATES IN LANGCHAIN
#
# Problem with hardcoded prompts:
#   llm.invoke("Explain Docker in simple terms")
#   llm.invoke("Explain Kubernetes in simple terms")
#   llm.invoke("Explain Redis in simple terms")
#   → copy-pasting the same sentence with one word changing
#
# Solution: Template with {variables}
#   "Explain {topic} in simple terms" → fill in topic at runtime
#
# PRINT ORDER:
#   1. STEP 1 — Basic template (one variable)
#   2. STEP 2 — Template with multiple variables
#   3. STEP 3 — System + Human message template (roles)
#   4. STEP 4 — Reuse same template, different inputs
# ============================================================


llm    = ChatOllama(model="llama3.2")
parser = StrOutputParser()


# ============================================================
# STEP 1: Basic template — one variable
# ============================================================
print("\n" + "="*50)
print("STEP 1: Basic template (one variable)")
print("="*50)

template = ChatPromptTemplate.from_template(
    "Explain {topic} in one simple sentence."
)

# See what it looks like before sending to Claude
formatted = template.format_messages(topic="Docker")
print(f"[Template] Formatted prompt: {formatted[0].content}")

# Use it in a chain
chain = template | llm | parser
result = chain.invoke({"topic": "Docker"})
print(f"[Chain]    Result: {result}")

input("\nPress Enter to go to STEP 2...\n")


# ============================================================
# STEP 2: Multiple variables
# ============================================================
print("="*50)
print("STEP 2: Multiple variables")
print("="*50)

template2 = ChatPromptTemplate.from_template(
    "Explain {topic} to a {audience} in one sentence."
)

# Same template, two very different outputs
chain2 = template2 | llm | parser

result_a = chain2.invoke({"topic": "Docker", "audience": "5-year-old"})
result_b = chain2.invoke({"topic": "Docker", "audience": "senior engineer"})

print(f"[For 5yo]     {result_a}")
print(f"[For engineer]{result_b}")

input("\nPress Enter to go to STEP 3...\n")


# ============================================================
# STEP 3: System + Human message template
#
# system  = sets Claude's role / behavior
# human   = the actual user question
#
# This is the real structure of a chat API call:
#   system:  "You are a Python tutor..."
#   human:   "What is a list?"
# ============================================================
print("="*50)
print("STEP 3: System + Human message (roles)")
print("="*50)

template3 = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}. Answer in exactly one sentence."),
    ("human",  "What is {concept}?"),
])

chain3 = template3 | llm | parser

result = chain3.invoke({"domain": "databases", "concept": "indexing"})
print(f"[System+Human] {result}")

input("\nPress Enter to go to STEP 4...\n")


# ============================================================
# STEP 4: Reuse same template, many inputs
# This is the whole point — one template, infinite reuse
# ============================================================
print("="*50)
print("STEP 4: Reuse template with different inputs")
print("="*50)

topics = ["Redis", "Kafka", "Elasticsearch"]

for topic in topics:
    result = chain3.invoke({"domain": "distributed systems", "concept": topic})
    print(f"\n[{topic}] {result}")

print("\n✅ Done! One template, many results.")
