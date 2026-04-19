import warnings
warnings.filterwarnings("ignore")

# ============================================================
# HuggingFace LOCAL vs Ollama — side by side
#
# Both run the LLM on YOUR machine (no API key needed)
# But the setup complexity is very different.
#
# PRINT ORDER:
#   1. STEP 1 — Ollama (simple)
#   2. STEP 2 — HuggingFace local (complex)
#   3. STEP 3 — Same result, different pain
# ============================================================


# ============================================================
# STEP 1: Ollama — 2 lines, just works
# ============================================================
print("\n" + "="*50)
print("STEP 1: Ollama (the easy way)")
print("="*50)

# WHAT YOU NEED:
#   brew install ollama
#   ollama pull llama3.2
#   ollama serve   ← running in background
# That's it. No GPU required, no torch, no model config.

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm_ollama = ChatOllama(model="llama3.2")   # ← 1 line
parser     = StrOutputParser()

chain_ollama = ChatPromptTemplate.from_template("What is {topic} in one line?") | llm_ollama | parser
result = chain_ollama.invoke({"topic": "Docker"})
print(f"[Ollama] {result}")
print("[Ollama] ✅ 1 line to set up the LLM")

input("\nPress Enter to go to STEP 2 (HuggingFace — brace yourself)...\n")


# ============================================================
# STEP 2: HuggingFace local — many lines, many problems
# ============================================================
print("="*50)
print("STEP 2: HuggingFace local (the hard way)")
print("="*50)

# WHAT YOU NEED FIRST:
#   pip install transformers torch accelerate langchain-huggingface
#   ← torch alone is 2-3 GB download
#   ← needs specific Python version compatibility
#   ← on Mac M1/M2: needs MPS backend or it defaults to CPU (slow)

# Then you manually:
#   1. Pick a model that fits in your RAM
#   2. Choose the right task type ("text-generation" vs "text2text-generation")
#   3. Configure tokenizer + pipeline yourself
#   4. Set max_new_tokens or it returns only a few words
#   5. Set device_map or it might crash on your hardware
#   6. Strip the prompt from output (HF returns prompt + response together)

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    from langchain_huggingface import HuggingFacePipeline

    model_name = "facebook/opt-125m"  # smallest available — 125M params, still ~250MB download

    print(f"[HF] Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)       # step 1

    print(f"[HF] Loading model (downloads ~250MB first time)...")
    model = AutoModelForCausalLM.from_pretrained(model_name)    # step 2

    print(f"[HF] Building pipeline...")
    hf_pipeline = pipeline(                                      # step 3
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=50,       # ← forget this → get 1 word back
        do_sample=False,
    )

    llm_hf = HuggingFacePipeline(pipeline=hf_pipeline)          # step 4

    # EXTRA PROBLEM: HuggingFace returns the full prompt + answer
    # Ollama returns only the answer
    # So you need to post-process or use a special output parser

    chain_hf = ChatPromptTemplate.from_template("What is {topic} in one line?") | llm_hf | parser
    result_hf = chain_hf.invoke({"topic": "Docker"})
    print(f"[HF] {result_hf}")
    print("[HF] ✅ Works — but look at everything above vs Ollama's 1 line")

except ImportError:
    print("[HF] ❌ Missing packages. You need to run:")
    print("     pip install transformers torch accelerate langchain-huggingface")
    print("     torch alone = 2-3 GB download")
    print("     This is why Ollama is simpler for local LLM usage.")

input("\nPress Enter to go to STEP 3...\n")


# ============================================================
# STEP 3: Summary — same result, different pain
# ============================================================
print("="*50)
print("STEP 3: Same result, different setup")
print("="*50)

print("""
  OLLAMA                          HUGGINGFACE LOCAL
  ──────────────────────────────  ──────────────────────────────
  brew install ollama             pip install transformers torch
  ollama pull llama3.2            accelerate langchain-huggingface
                                  (2-3 GB, version conflicts possible)

  ChatOllama(model="llama3.2")    AutoTokenizer.from_pretrained(...)
  ← 1 line                        AutoModelForCausalLM.from_pretrained(...)
                                  pipeline("text-generation", model, tokenizer,
                                           max_new_tokens=50, do_sample=False)
                                  HuggingFacePipeline(pipeline=hf_pipeline)
                                  ← 4 steps

  Returns: clean answer           Returns: prompt + answer mixed together
  Model quality: llama3.2         Model quality: opt-125m (much weaker)
  (7B params, optimized)          (125M params, unoptimized for chat)

  VERDICT: Use Ollama for running LLMs locally.
           Use HuggingFace for training / fine-tuning (your 04-huggingface/).
""")

print("✅ Done! Convinced?")
