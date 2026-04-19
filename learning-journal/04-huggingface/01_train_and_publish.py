# ============================================================
# HUGGINGFACE — Train a model and publish it
#
# Use case: Sentiment Analysis (positive / negative)
# Model:    distilbert-base-uncased (small, fast, free)
# Dataset:  SST-2 (Stanford Sentiment Treebank)
#
# PRINT ORDER:
#   1. STEP 1 — Login to HuggingFace
#   2. STEP 2 — Load dataset
#   3. STEP 3 — Load model + tokenizer
#   4. STEP 4 — Tokenize data
#   5. STEP 5 — Train
#   6. STEP 6 — Evaluate
#   7. STEP 7 — Push to HuggingFace Hub
#
# Prerequisites:
#   pip install transformers datasets scikit-learn
#
# ============================================================

import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from sklearn.metrics import accuracy_score
import numpy as np

# ============================================================
# STEP 1: Login to HuggingFace
# Get token from: huggingface.co → Settings → Access Tokens
# ============================================================
print("\nSTEP 1: Logging in to HuggingFace...")

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
HF_TOKEN    = os.getenv("HF_TOKEN")  # loaded from .env
HF_USERNAME = "your-huggingface-username"                # replace this

login(token=HF_TOKEN)
print("✅ Logged in!")
input("\nPress Enter to go to STEP 2...\n")

# ============================================================
# STEP 2: Load dataset
# SST-2 = movie reviews labeled as positive (1) or negative (0)
# ============================================================
print("STEP 2: Loading dataset...")

dataset = load_dataset("glue", "sst2")

print(f"✅ Dataset loaded!")
print(f"  Train samples : {len(dataset['train'])}")
print(f"  Test samples  : {len(dataset['validation'])}")
print(f"  Example       : {dataset['train'][0]}")
input("\nPress Enter to go to STEP 3...\n")

# ============================================================
# STEP 3: Load model + tokenizer
# distilbert = smaller, faster version of BERT
# Tokenizer converts text → token IDs the model understands
# ============================================================
print("STEP 3: Loading model and tokenizer...")

MODEL_NAME = "distilbert-base-uncased"
tokenizer  = AutoTokenizer.from_pretrained(MODEL_NAME)
model      = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

print(f"✅ Model loaded: {MODEL_NAME}")
print(f"  Parameters: ~67 million")
input("\nPress Enter to go to STEP 4...\n")

# ============================================================
# STEP 4: Tokenize the dataset
# Converts raw text → numbers the model can process
# truncation=True  → cuts text longer than 128 tokens
# padding=True     → pads shorter text to same length
# ============================================================
print("STEP 4: Tokenizing dataset...")

def tokenize(batch):
    return tokenizer(batch["sentence"], truncation=True, padding=True, max_length=128)

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.rename_column("label", "labels")
dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

print("✅ Tokenization done!")
print(f"  Example token IDs: {dataset['train'][0]['input_ids'][:10]}...")
input("\nPress Enter to go to STEP 5...\n")

# ============================================================
# STEP 5: Train
# epochs=1 → one pass through the dataset (fast for demo)
# batch_size=16 → process 16 samples at a time
# ============================================================
print("STEP 5: Training... (this takes ~5 minutes)")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(labels, predictions)}

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    evaluation_strategy="epoch",
    logging_steps=100,
    save_strategy="no",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"].select(range(1000)),  # use 1000 samples for speed
    eval_dataset=dataset["validation"].select(range(200)),
    compute_metrics=compute_metrics,
)

trainer.train()
print("✅ Training done!")
input("\nPress Enter to go to STEP 6...\n")

# ============================================================
# STEP 6: Evaluate
# ============================================================
print("STEP 6: Evaluating model...")

results = trainer.evaluate()
print(f"✅ Accuracy: {results['eval_accuracy']:.2%}")
input("\nPress Enter to go to STEP 7 (publish to HuggingFace)...\n")

# ============================================================
# STEP 7: Push to HuggingFace Hub
# Your model will be live at:
# https://huggingface.co/{HF_USERNAME}/sentiment-classifier
# ============================================================
print("STEP 7: Publishing to HuggingFace Hub...")

repo_name = f"{HF_USERNAME}/sentiment-classifier"
model.push_to_hub(repo_name, token=HF_TOKEN)
tokenizer.push_to_hub(repo_name, token=HF_TOKEN)

print(f"\n✅ Model published!")
print(f"   View at: https://huggingface.co/{repo_name}")
print(f"\n   Use it anywhere:")
print(f"   from transformers import pipeline")
print(f"   classifier = pipeline('sentiment-analysis', model='{repo_name}')")
print(f"   print(classifier('I love this movie!'))")
