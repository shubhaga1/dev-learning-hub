import warnings
warnings.filterwarnings("ignore")

# ============================================================
# WHAT IS vLLM?
#
# vLLM = Very Large Language Model serving engine
# Built by UC Berkeley, used by Mistral, Meta, Nvidia, etc.
#
# Problem it solves:
#   When 100 users ask your LLM at the same time,
#   naive serving processes them ONE BY ONE — slow.
#
#   vLLM uses "PagedAttention" — batches multiple requests
#   together on the GPU, like a web server handles HTTP requests.
#
# Ollama    = 1 request at a time (great for local dev)
# vLLM      = 100s of requests at a time (great for production)
#
# Also: vLLM exposes an OpenAI-compatible REST API
#   → drop-in replacement for OpenAI in any app
#
# PRINT ORDER:
#   1. STEP 1 — Direct vLLM inference (Python SDK)
#   2. STEP 2 — Batch inference (key feature)
#   3. STEP 3 — OpenAI-compatible client (same API as OpenAI)
# ============================================================


# ============================================================
# SETUP (run these first in terminal):
#
# Mac M1/M2:
#   pip install vllm          ← experimental CPU support
#
# Linux (full GPU support):
#   pip install vllm
#
# OR — easiest way to try it: run vLLM as a server
#   python -m vllm.entrypoints.openai.api_server \
#          --model facebook/opt-125m \
#          --port 8000
#
# Then use the OpenAI client to talk to it (STEP 3 below).
# ============================================================


# ============================================================
# STEP 1: Direct vLLM inference
# LLM() loads the model + runs inference in one object
# ============================================================
print("\n" + "="*50)
print("STEP 1: Direct vLLM inference")
print("="*50)

try:
    from vllm import LLM, SamplingParams

    # Load model — downloads ~250MB first time
    llm = LLM(model="facebook/opt-125m")   # small model for demo

    params = SamplingParams(
        temperature=0.7,    # randomness (0=deterministic, 1=creative)
        max_tokens=50,      # max words to generate
    )

    prompt = "What is machine learning?"
    output = llm.generate([prompt], params)

    print(f"Prompt : {prompt}")
    print(f"Output : {output[0].outputs[0].text}")
    print("✅ Direct inference works!")

except ImportError:
    print("vLLM not installed.")
    print("Run: pip install vllm")
    print("(Skipping to STEP 2 to show the concept anyway)")

input("\nPress Enter to go to STEP 2...\n")


# ============================================================
# STEP 2: Batch inference — the KEY feature
#
# Naive (Ollama style): process 1 prompt at a time
#   prompt1 → wait → result1
#   prompt2 → wait → result2
#   prompt3 → wait → result3
#   Total: 3x single request time
#
# vLLM batch: send ALL prompts at once
#   [prompt1, prompt2, prompt3] → process together → [r1, r2, r3]
#   Total: ~1x single request time  ← massive speedup
#
# This is why vLLM is used in production.
# ============================================================
print("="*50)
print("STEP 2: Batch inference")
print("="*50)

try:
    from vllm import LLM, SamplingParams

    llm    = LLM(model="facebook/opt-125m")
    params = SamplingParams(temperature=0.7, max_tokens=30)

    # Send 3 prompts at once — processed in parallel on GPU
    prompts = [
        "What is Docker?",
        "What is Kubernetes?",
        "What is Redis?",
    ]

    outputs = llm.generate(prompts, params)   # ← all at once

    for output in outputs:
        print(f"\nQ: {output.prompt}")
        print(f"A: {output.outputs[0].text.strip()}")

    print("\n✅ 3 prompts processed in parallel!")

except ImportError:
    print("(vLLM not installed — showing concept)")
    print("""
  Naive (1 by 1):          vLLM (batched):
  ─────────────────        ─────────────────
  prompt1 → 500ms          [p1, p2, p3]
  prompt2 → 500ms              ↓
  prompt3 → 500ms          parallel GPU
  total:   1500ms          total: ~600ms
    """)

input("\nPress Enter to go to STEP 3...\n")


# ============================================================
# STEP 3: OpenAI-compatible API
#
# vLLM can run as a server that speaks the OpenAI API format.
# This means ANY code written for OpenAI works with vLLM —
# just change the base_url.
#
# Start server (in a separate terminal):
#   python -m vllm.entrypoints.openai.api_server \
#          --model facebook/opt-125m \
#          --port 8000
#
# Then run this step.
# ============================================================
print("="*50)
print("STEP 3: OpenAI-compatible client")
print("="*50)

import os
from dotenv import load_dotenv
import requests
import json

env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

VLLM_SERVER = "http://localhost:8000"

try:
    # Check if vLLM server is running
    response = requests.get(f"{VLLM_SERVER}/health", timeout=2)
    server_running = response.status_code == 200
except Exception:
    server_running = False

if server_running:
    # Use vLLM server exactly like OpenAI API
    from openai import OpenAI

    client = OpenAI(
        base_url=f"{VLLM_SERVER}/v1",
        api_key="dummy",              # vLLM doesn't need a real key
    )

    response = client.chat.completions.create(
        model="facebook/opt-125m",
        messages=[{"role": "user", "content": "What is vLLM in one line?"}],
        max_tokens=50,
    )

    print(f"Response: {response.choices[0].message.content}")
    print("✅ Identical to OpenAI API — just different base_url!")

else:
    print("vLLM server not running. To start it:")
    print("""
  # In a separate terminal:
  python -m vllm.entrypoints.openai.api_server \\
         --model facebook/opt-125m \\
         --port 8000

  # Then your existing OpenAI code works with 1 change:
  client = OpenAI(
      base_url="http://localhost:8000/v1",  # ← only this changes
      api_key="dummy",
  )
    """)

print("\n✅ KEY TAKEAWAYS:")
print("""
  Ollama      → local dev, 1 request at a time, easy setup
  vLLM        → production, 100s of requests, GPU optimized
  HuggingFace → training/fine-tuning, not optimized for serving

  vLLM vs Ollama:
    Same models, same idea (local LLM)
    vLLM = 2-10x faster throughput via PagedAttention + batching
    Ollama = easier to install and use for dev

  Use vLLM when: you're serving LLM to real users at scale
  Use Ollama when: you're testing/building locally
""")
