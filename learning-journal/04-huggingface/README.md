# 04 — HuggingFace

## What you learn here
- What is HuggingFace — the GitHub for AI models
- Fine-tuning a pre-trained model on your data
- Publishing your model so anyone can use it

## Prerequisites
```bash
pip install transformers datasets scikit-learn
```

## Run order
```bash
python 01_train_and_publish.py
```

## Key concepts

### What is fine-tuning?
```
Pre-trained model (distilbert) → trained on 100GB of text → knows language
        ↓
Fine-tune on YOUR data (movie reviews) → now knows sentiment too
```

### Why not train from scratch?
```
From scratch → needs months + millions of dollars
Fine-tuning  → needs minutes + free GPU
```

### Steps
```
1. Load dataset  (SST-2 movie reviews)
2. Load model    (distilbert — 67M parameters)
3. Tokenize      (text → numbers)
4. Train         (~5 minutes on CPU)
5. Evaluate      (check accuracy)
6. Publish       (push to huggingface.co)
```

### After publishing — anyone can use your model
```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="your-username/sentiment-classifier")
print(classifier("I love this movie!"))
# [{'label': 'POSITIVE', 'score': 0.99}]
```
