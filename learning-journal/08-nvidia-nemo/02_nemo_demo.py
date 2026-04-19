import warnings
warnings.filterwarnings("ignore")

# ============================================================
# NeMo POC — Text Classification with NeMo
#
# We'll fine-tune a BERT model on sentiment analysis
# Same task as your HuggingFace demo (04-huggingface)
# but using NeMo's API — so you can see the difference.
#
# TO RUN THIS:
#   Option A — Docker (recommended for Mac):
#     docker run --rm -it -v $(pwd):/workspace \
#       nvcr.io/nvidia/nemo:24.07 \
#       python /workspace/learning-journal/08-nvidia-nemo/02_nemo_demo.py
#
#   Option B — Install (Python 3.10+ required):
#     pip install nemo_toolkit[nlp]
#
# PRINT ORDER:
#   STEP 1 — What NeMo config looks like (YAML-driven)
#   STEP 2 — Build model
#   STEP 3 — Train
#   STEP 4 — Inference
# ============================================================

import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)


# ============================================================
# STEP 1: NeMo is config-driven (YAML)
#
# HuggingFace:  you write Python code to configure training
# NeMo:         you write a YAML config, NeMo reads it
#
# Why YAML? Reproducibility — save config, reproduce experiment.
# ============================================================
print("\n" + "="*50)
print("STEP 1: NeMo config (YAML-driven training)")
print("="*50)

# This is what a NeMo training config looks like
# (not running yet — just showing the structure)
nemo_config_example = """
# nemo_sentiment.yaml
model:
  nemo_file: null
  language_model:
    pretrained_model_name: bert-base-uncased  # base model
    lm_checkpoint: null
  classifier_head:
    num_output_layers: 2
    fc_dropout: 0.1
  dataset:
    num_classes: 2                # positive / negative
    max_seq_length: 128

trainer:
  max_epochs: 3
  gpus: 1                        # change to 8 for multi-GPU!
  precision: 16                  # fp16 for speed

exp_manager:
  exp_dir: ./nemo_experiments    # auto saves checkpoints, logs
  name: sentiment_model
"""

print("NeMo config (YAML):")
print(nemo_config_example)

# Compare to HuggingFace:
hf_equivalent = """
# HuggingFace equivalent (Python):
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    fp16=True,
)
"""
print("HuggingFace equivalent (Python):")
print(hf_equivalent)
print("Same thing — NeMo just uses YAML instead of Python args.")

input("\nPress Enter for STEP 2...\n")


# ============================================================
# STEP 2: Build model with NeMo
# ============================================================
print("="*50)
print("STEP 2: Build NeMo model")
print("="*50)

try:
    from omegaconf import OmegaConf
    from nemo.collections.nlp.models import TextClassificationModel

    # NeMo loads everything from config
    cfg = OmegaConf.create({
        "model": {
            "nemo_file": None,
            "language_model": {
                "pretrained_model_name": "bert-base-uncased",
            },
            "classifier_head": {
                "num_output_layers": 2,
                "fc_dropout": 0.1,
            },
            "dataset": {
                "num_classes": 2,
                "max_seq_length": 128,
            }
        }
    })

    model = TextClassificationModel(cfg=cfg.model)
    print(f"✅ Model created: {model.__class__.__name__}")
    print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")

except ImportError:
    print("NeMo not installed — showing what the code does:")
    print("""
  from nemo.collections.nlp.models import TextClassificationModel

  model = TextClassificationModel(cfg=cfg.model)
  # NeMo auto-downloads bert-base-uncased
  # wraps it with a classification head
  # ready to train

  # HuggingFace equivalent:
  model = AutoModelForSequenceClassification.from_pretrained(
      "bert-base-uncased", num_labels=2
  )
  # Same thing — different API
    """)

input("\nPress Enter for STEP 3...\n")


# ============================================================
# STEP 3: Training — where NeMo shines
# ============================================================
print("="*50)
print("STEP 3: Training (NeMo vs HuggingFace)")
print("="*50)

print("""
HuggingFace training (what you did in 04-huggingface):
──────────────────────────────────────────────────────
  trainer = Trainer(
      model=model,
      args=training_args,
      train_dataset=dataset["train"],
  )
  trainer.train()
  # Fine for 1 GPU, small datasets

NeMo training (multi-GPU, production scale):
──────────────────────────────────────────────────────
  import pytorch_lightning as pl

  trainer = pl.Trainer(
      max_epochs=3,
      gpus=8,               # ← 8 GPUs, just change this number
      strategy="ddp",       # distributed data parallel
      precision=16,         # mixed precision
  )
  trainer.fit(model)

  # NeMo + Megatron also supports:
  #   tensor parallelism  → split ONE layer across GPUs
  #   pipeline parallelism → split layers across GPUs
  #   Both needed for 70B+ parameter models
""")

input("\nPress Enter for STEP 4...\n")


# ============================================================
# STEP 4: Inference with NeMo
# ============================================================
print("="*50)
print("STEP 4: Inference")
print("="*50)

try:
    # If model was trained and saved as .nemo file:
    # model = TextClassificationModel.restore_from("sentiment.nemo")

    sentences = [
        "I love this product!",
        "This is terrible.",
        "It was okay, nothing special.",
    ]

    # model.predict(sentences)  ← NeMo API
    print("NeMo inference:")
    print("  model = TextClassificationModel.restore_from('sentiment.nemo')")
    print("  predictions = model.predict(sentences)")
    print()
    for s in sentences:
        print(f"  '{s}'")

except Exception as e:
    print(f"(NeMo not installed: {e})")

print("""
KEY DIFFERENCE from HuggingFace:
  HuggingFace saves: pytorch_model.bin + config.json (multiple files)
  NeMo saves:        sentiment.nemo   (single file, everything inside)

  .nemo file = zip of model weights + config + tokenizer
  Easier to share and deploy.
""")

print("✅ NeMo summary:")
print("""
  HuggingFace  → fine-tune, 1-4 GPUs, simple
  NeMo         → pre-train/fine-tune, 100s of GPUs, YAML config
  vLLM         → serve the trained model to users
  Ollama       → run locally for dev/testing

  Typical production pipeline:
    Train (NeMo) → Export (.nemo) → Serve (vLLM) → Use (LangChain)
""")
