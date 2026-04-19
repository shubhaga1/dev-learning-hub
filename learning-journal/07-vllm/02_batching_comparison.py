import warnings
warnings.filterwarnings("ignore")

import time
import requests
import threading
import json

# ============================================================
# BATCHING: Naive vs HuggingFace vs Ollama vs vLLM
#
# All 4 process the SAME 5 prompts.
# We measure wall-clock time for each approach.
#
# PRINT ORDER:
#   STEP 1 — Naive / sequential (worst)
#   STEP 2 — HuggingFace (slightly better, still sequential)
#   STEP 3 — Ollama (1 at a time, but async possible)
#   STEP 4 — vLLM (true batching on GPU)
#   STEP 5 — Summary table
# ============================================================

PROMPTS = [
    "What is Docker in one line?",
    "What is Kubernetes in one line?",
    "What is Redis in one line?",
    "What is Kafka in one line?",
    "What is Nginx in one line?",
]

print("\n" + "="*55)
print("Comparing 4 approaches to serve 5 prompts")
print("="*55)
print(f"Prompts: {len(PROMPTS)}")
print()


# ============================================================
# STEP 1: Naive / sequential HTTP calls
# Like calling OpenAI API one by one in a for loop
# No batching, no parallelism
# ============================================================
print("STEP 1: Naive — one request at a time (Ollama sequential)")
print("-"*55)

def call_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False},
        timeout=60,
    )
    return response.json()["response"].strip()

try:
    t_start = time.time()

    for i, prompt in enumerate(PROMPTS):
        t0     = time.time()
        result = call_ollama(prompt)
        t1     = time.time()
        print(f"  [{i+1}] {prompt[:35]:<35} → {t1-t0:.2f}s")

    naive_total = time.time() - t_start
    print(f"\n  TOTAL: {naive_total:.2f}s")
    print(f"  GPU idle while waiting for each response to finish before starting next.")

except Exception as e:
    naive_total = None
    print(f"  Ollama not running. Start it: ollama serve")
    print(f"  (Simulated: ~3s × 5 prompts = ~15s total)")
    naive_total = 15.0

input("\nPress Enter for STEP 2...\n")


# ============================================================
# STEP 2: HuggingFace — still sequential by default
# HF pipeline processes one input at a time internally
# unless you explicitly pass a list AND set batch_size
# Most people don't do this → same as naive
# ============================================================
print("STEP 2: HuggingFace — sequential (most people's mistake)")
print("-"*55)

try:
    from transformers import pipeline as hf_pipeline

    # loads ~250MB model
    pipe = hf_pipeline("text-generation", model="facebook/opt-125m",
                        max_new_tokens=30, device_map="auto")

    # WRONG way (sequential — what most people do):
    t_start = time.time()
    for prompt in PROMPTS:
        t0 = time.time()
        pipe(prompt)
        print(f"  {prompt[:40]:<40} {time.time()-t0:.2f}s")
    hf_sequential = time.time() - t_start
    print(f"\n  TOTAL (sequential): {hf_sequential:.2f}s")

    # RIGHT way (pass list with batch_size):
    t_start = time.time()
    pipe(PROMPTS, batch_size=5)   # processes all 5 together
    hf_batched = time.time() - t_start
    print(f"  TOTAL (batched):    {hf_batched:.2f}s  ← better but still not vLLM")
    print(f"\n  NOTE: HF batching is clunky, not optimized for LLM serving.")

except ImportError:
    print("  transformers not installed for this demo.")
    print("  (Simulated: sequential ~12s, batched ~8s)")

input("\nPress Enter for STEP 3...\n")


# ============================================================
# STEP 3: Ollama — parallel via threads
# Ollama handles 1 request at a time natively.
# But you CAN fire multiple HTTP requests simultaneously using threads.
# This helps but Ollama still serializes internally.
# ============================================================
print("STEP 3: Ollama — parallel threads (hack, not real batching)")
print("-"*55)

results   = [None] * len(PROMPTS)
timings   = [None] * len(PROMPTS)

def worker(i, prompt):
    t0         = time.time()
    results[i] = call_ollama(prompt)
    timings[i] = time.time() - t0

try:
    t_start = time.time()
    threads = []

    for i, prompt in enumerate(PROMPTS):
        t = threading.Thread(target=worker, args=(i, prompt))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    parallel_total = time.time() - t_start

    for i, prompt in enumerate(PROMPTS):
        print(f"  [{i+1}] {prompt[:35]:<35} → {timings[i]:.2f}s (ran concurrently)")

    print(f"\n  TOTAL: {parallel_total:.2f}s")
    print(f"  vs naive: {naive_total:.2f}s")
    print(f"  Speedup: {naive_total/parallel_total:.1f}x")
    print(f"\n  BUT: Ollama queues them internally — not true GPU batching.")
    print(f"       GPU still processes mostly 1 at a time.")

except Exception:
    print("  Ollama not running.")
    print("  (Simulated: ~5s total — better but Ollama queues internally)")

input("\nPress Enter for STEP 4...\n")


# ============================================================
# STEP 4: vLLM — true GPU batching (PagedAttention)
#
# vLLM packs MULTIPLE token sequences into GPU memory at once.
# The GPU works on ALL of them simultaneously — real parallelism.
#
# To run this step:
#   python -m vllm.entrypoints.openai.api_server \
#          --model facebook/opt-125m --port 8000
# ============================================================
print("STEP 4: vLLM — true GPU batching")
print("-"*55)

VLLM_URL = "http://localhost:8000/v1/completions"

def call_vllm_batch(prompts):
    """Send ALL prompts in a single API call — vLLM batches them on GPU"""
    response = requests.post(
        VLLM_URL,
        json={
            "model":      "facebook/opt-125m",
            "prompt":     prompts,          # ← list of prompts, not one
            "max_tokens": 30,
        },
        timeout=30,
    )
    return response.json()

try:
    requests.get("http://localhost:8000/health", timeout=2)

    t_start  = time.time()
    outputs  = call_vllm_batch(PROMPTS)   # ← ALL 5 in 1 call
    vllm_total = time.time() - t_start

    for i, choice in enumerate(outputs["choices"]):
        print(f"  [{i+1}] {PROMPTS[i][:35]:<35} → {choice['text'].strip()[:40]}")

    print(f"\n  TOTAL: {vllm_total:.2f}s  ← all 5 processed together on GPU")
    print(f"  vs naive: {naive_total:.2f}s")
    if naive_total:
        print(f"  Speedup: {naive_total/vllm_total:.1f}x")

except Exception:
    print("  vLLM server not running. To start:")
    print("""
  pip install vllm
  python -m vllm.entrypoints.openai.api_server \\
         --model facebook/opt-125m \\
         --port 8000
  """)
    print("  (Simulated: ~2s total for 5 prompts = 7x faster than naive)")

input("\nPress Enter for STEP 5 (summary)...\n")


# ============================================================
# STEP 5: Summary
# ============================================================
print("STEP 5: Summary")
print("="*55)
print("""
  APPROACH          HOW IT WORKS                    TYPICAL TIME (5 prompts)
  ─────────────     ──────────────────────────────   ────────────────────────
  Naive loop        prompt1→wait→prompt2→wait...     ~15s  (serial)
  HF sequential     same, just via pipeline()        ~12s  (serial)
  HF batched        passes list but not optimized    ~8s   (semi-parallel)
  Ollama threads    fires simultaneously, queued     ~5s   (fake parallel)
  vLLM              ALL prompts on GPU at once       ~2s   (real parallel)

  WHY vLLM IS FASTER:
  ┌─────────────────────────────────────────────────────┐
  │  Naive:                                             │
  │  GPU:  [P1....] idle  [P2....] idle  [P3....] ...  │
  │                                                     │
  │  vLLM:                                             │
  │  GPU:  [P1+P2+P3+P4+P5 all at once.............]  │
  │         GPU 100% utilized                          │
  └─────────────────────────────────────────────────────┘

  The secret = PagedAttention:
    Manages GPU memory like OS virtual memory pages.
    Fits more sequences in GPU memory simultaneously.
    Less wasted GPU cycles between requests.
""")
