# ML System Design — Interview Framework

Every MLSD question follows this spine. Master the framework first, then apply it to any problem.

---

## The 8-Step MLSD Framework

```
1. Problem Formulation      → What exactly are we predicting?
2. Metrics                  → How do we measure success?
3. Data                     → What data do we have / need?
4. Feature Engineering      → What signals matter?
5. Model                    → Which algorithm and why?
6. Training                 → How do we train at scale?
7. Serving / Inference      → How do we serve predictions?
8. Monitoring               → How do we know it's working?
```

---

## Step 1 — Problem Formulation

Ask clarifying questions:
- What is the **business goal**? (engagement, revenue, safety)
- What is the **ML task**? (classification, regression, ranking, generation)
- What do we **predict**? (click, watch time, rating, ETA)
- What is the **label**? (explicit feedback, implicit behavior)
- What are the **constraints**? (latency, scale, cold start)

**Common framings:**

| Business Goal | ML Task | Label |
|---------------|---------|-------|
| More clicks | Binary classification | clicked / not clicked |
| Longer watch time | Regression | watch duration |
| Relevant results | Learning to Rank (LTR) | engagement signal |
| Delivery ETA | Regression | actual delivery time |

---

## Step 2 — Metrics

Always define **two types**:

### Offline Metrics (model quality during training/eval)
| Task | Metric |
|------|--------|
| Binary classification | AUC-ROC, PR-AUC, Log Loss |
| Regression | MAE, RMSE, MAPE |
| Ranking | NDCG@K, MRR, Precision@K |
| Recommendation | Hit Rate@K, Recall@K |

### Online Metrics (business impact in production)
- CTR (Click-Through Rate)
- Watch time / Session length
- Conversion rate
- Revenue per user
- DAU / Retention

**Key rule:** Optimize offline metric that correlates with online metric.

---

## Step 3 — Data

### Sources
- **User behavior logs**: clicks, views, dwell time, skips
- **Item metadata**: title, category, tags, embeddings
- **User profile**: demographics, history, preferences
- **Context**: device, time, location, session

### Data Pipeline
```
Raw logs → Feature Store → Training Data → Model
              ↑                              ↓
         (offline)              (batch or real-time features)
```

### Label Engineering
- **Positive**: click, purchase, 50%+ watch, save
- **Negative**: skip, short dwell time, explicit thumbs down
- **Negative sampling**: random negatives, hard negatives (impressions not clicked)

### Data challenges
- **Class imbalance**: 99% negative clicks → undersample negatives or use weighted loss
- **Position bias**: top results clicked more regardless of relevance → debias with IPS
- **Data freshness**: stale training data → online learning or frequent retraining

---

## Step 4 — Feature Engineering

### Feature categories

| Category | Examples |
|----------|---------|
| User features | age, location, device, language, account age |
| User history | last 10 watched, avg watch time, category affinity |
| Item features | category, creator, age, avg rating, view count |
| Context | time of day, day of week, search query, session position |
| Interaction | user×item affinity score, co-watch rate |
| Cross features | user_category × item_category |

### Embeddings
- **Item2Vec / Word2Vec** for item collaborative filtering
- **Two-tower model** for user-item similarity
- **BERT/LLM** for text features (title, description)

### Feature store
- **Offline**: precomputed batch features (BigQuery, Hive)
- **Online**: low-latency lookup (Redis, DynamoDB) for serving

---

## Step 5 — Model Selection

### Progression (answer in order of complexity)

```
Heuristics → Logistic Regression → GBDT → Neural Network → Transformer
```

| Model | When to use | Pros | Cons |
|-------|-------------|------|------|
| Logistic Regression | Baseline, interpretable | Fast, stable | Can't capture non-linear |
| GBDT (XGBoost/LightGBM) | Tabular features | High accuracy, handles missing | Slow inference at scale |
| Two-Tower Neural Net | Retrieval / embedding | Scalable ANN search | Cold start |
| Multi-task Neural Net | Multiple objectives | Efficient, correlated tasks | Complex training |
| Transformer / LLM | Sequential, NLP | State of art | Expensive |

### Ranking-specific architectures
```
Retrieval (ANN)  →  Ranking (full model)  →  Re-ranking (rules + diversity)
  (millions)          (thousands)                (hundreds)
```

---

## Step 6 — Training

### Training pipeline
```
Feature pipeline → Training job → Model registry → A/B test → Deploy
```

### Key considerations
- **Batch vs. online training**: batch weekly/daily vs. online learning for fresh signals
- **Negative sampling**: 1:1 to 1:10 positive:negative ratio
- **Loss function**: BCE for clicks, MSE for regression, ListNet for ranking
- **Regularization**: L2, dropout, early stopping
- **Scale**: distributed training (Spark, Ray, PyTorch DDP)

### Multi-task learning
```python
# Predict click AND watch time simultaneously
loss = α × BCE(click) + β × MSE(watch_time)
```
Shared layers capture common signals; task-specific heads specialize.

---

## Step 7 — Serving / Inference

### Latency budget (typical)
```
Total: 100-200ms
  Retrieval:   10-20ms   (ANN lookup, inverted index)
  Ranking:     30-50ms   (score top-K candidates)
  Re-ranking:  10ms      (business rules, diversity)
  Response:    10ms
```

### Architecture
```
User Request
    ↓
Feature Fetching (online feature store, Redis)
    ↓
Retrieval (ANN / Elasticsearch / Faiss)  → top 500
    ↓
Ranking Model (neural net inference)     → top 50
    ↓
Re-ranking (diversity, freshness, rules) → top 10-20
    ↓
Response
```

### Optimizations
- **Model quantization**: FP32 → INT8 (4× smaller, faster)
- **Caching**: pre-rank top items for popular users
- **Approximate Nearest Neighbor (ANN)**: Faiss, ScaNN, HNSW
- **Batch inference**: group requests to maximize GPU utilization

---

## Step 8 — Monitoring

### What to monitor

| Signal | Metric | Alert if |
|--------|--------|----------|
| Model quality | AUC, NDCG | drops >2% |
| Prediction distribution | Score histogram | distribution shift |
| Feature quality | Null rate, range | feature missing or stale |
| Business metrics | CTR, revenue | drops vs. control |
| Latency | p50, p99 | p99 > SLA |
| Data freshness | Label lag | >24h delay |

### Feedback loop
```
Predictions → User Actions → Labels → Retrain → Deploy
     ↑___________________________________|
```

### Common failures
- **Training-serving skew**: features computed differently offline vs. online
- **Feedback loop bias**: model learns from its own predictions
- **Concept drift**: user behavior changes, model becomes stale
- **Cold start**: new users/items with no history

---

## Interview Tips

1. **Start with business goal**, not model architecture
2. **Define metrics first** — interviewer wants to see you measure success
3. **Justify every choice** — why GBDT over logistic regression?
4. **Mention trade-offs** — precision vs. recall, latency vs. accuracy
5. **Address cold start** — every recommender has this problem
6. **Scale the numbers** — YouTube = 2B users, 500h video/min uploaded
7. **Bring up A/B testing** — how would you validate the system?
