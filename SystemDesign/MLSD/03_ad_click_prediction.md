# MLSD — Ad Click Prediction

> "Design a system to predict the probability that a user clicks on an ad."

---

## 1. Problem Formulation

**Business goal:** Maximize revenue while maintaining user experience quality.

**What we predict:** P(click | user, ad, context) — pCTR (predicted Click-Through Rate)

**Why it matters:**
```
Ad auction:  bid × pCTR = eCPM (expected cost per mille)
Higher pCTR → higher eCPM → wins auction with lower bid
→ Advertisers pay less for better targeting
→ Platform earns more revenue per impression
```

**Scale (Facebook-like):**
- 3B users
- 10M advertisers
- 10T ad impressions/day
- Inference must complete in <50ms per request

**ML task:** Binary classification → P(click) ∈ [0, 1]

---

## 2. Metrics

### Offline
| Metric | Why |
|--------|-----|
| **AUC-ROC** | Ranking quality — does model rank clicked ads above unclicked? |
| **Log Loss** | Calibration — is P(click)=0.1 actually 10% of the time? |
| **Calibration curve** | Predicted vs. actual CTR per bucket |
| **PR-AUC** | Better for imbalanced data (CTR ~2%) |

**Critical:** Calibration matters as much as AUC. If model predicts 5% but actual is 3%, auction prices are wrong → advertiser overpays → they leave.

### Online (A/B test)
| Metric | Target |
|--------|--------|
| Revenue per mille (RPM) | Primary — maximize |
| CTR | Should be consistent with prediction |
| Ad relevance score | User satisfaction |
| Conversion rate | Downstream advertiser value |
| User complaint rate | Guardrail — must not increase |

---

## 3. Data

### Training data volume
- 100B+ impressions/day
- ~2% CTR = 2B positive examples/day
- Keep last 7 days → 700B training rows
- Sample: 1:10 positive:negative ratio after sampling

### Features available at serving time
```
User features (from profile + history)
Ad features   (creative, targeting, bid)
Context       (page, device, time)
Interaction   (user×advertiser history)
```

### Label
```python
label = 1  if user clicked the ad
label = 0  if ad was shown (impression) but not clicked

# Time window: click within 1 hour of impression
# Delayed label problem: conversions can come 7 days later
```

### Delayed label problem
- User sees ad on Monday, buys on Friday → label arrives 4 days late
- Solution: use click as immediate label + conversion as secondary label
- Join impressions with clicks at T+1 hour, conversions at T+7 days

---

## 4. Feature Engineering

### User features (100s of features)
```python
# Demographics (sparse — use embeddings)
user_id_embedding        # 256-dim learned embedding
age_bucket               # <18, 18-24, 25-34, 35-44, 45-54, 55+
gender
country, city

# Behavioral (dense)
avg_ctr_last_7d          # user's historical click rate
ads_shown_last_hour      # fatigue signal
session_page_depth       # how deep in session
time_since_last_click
category_affinity_vector # 50-dim: P(interested in category)
```

### Ad features
```python
ad_id_embedding          # 256-dim learned
advertiser_id_embedding
creative_type            # image / video / carousel / text
ad_age_days              # freshness
historical_ctr_last_7d   # ad's track record
ad_category              # auto, travel, finance...
bid_price                # (careful: don't leak auction info)
ad_quality_score         # relevance to targeting criteria
```

### Context features
```python
page_type                # news feed / stories / marketplace
device_type              # mobile / desktop / tablet
time_of_day              # morning / lunch / evening
day_of_week
placement                # top / right rail / in-feed
```

### Cross features (critical for CTR)
```python
# These capture interaction effects
user_category_ad_category_match    # = 1 if interests align
user_age_ad_target_age_match       # demographic targeting match
user_location_ad_target_geo        # geo targeting match
user_device_ad_creative_type       # mobile user + video ad
```

### Hashing trick
- User IDs, ad IDs → sparse one-hot → billions of dimensions
- Solution: **feature hashing** into fixed-size hash table (2^22 = 4M buckets)
- Embed each hash bucket → dense representation

---

## 5. Model Architecture

### Evolution of CTR models

```
Logistic Regression (2010s) → GBDT (2014) → Deep & Wide (2016) → DCN/DLRM (2019+)
```

### Production Model: Deep & Wide (or DLRM)

```
Wide part (memorization):        Deep part (generalization):
Cross-product features  →        User embeddings
  e.g. user×ad category          Ad embeddings
  e.g. user×time                 Context embeddings
       ↓                               ↓
  Logistic regression          3 FC layers (512→256→128)
         ↓_________________________↓
                    ↓
              Final sigmoid
              P(click) ∈ [0,1]
```

**Wide part:** Memorizes known patterns (this user always clicks auto ads)
**Deep part:** Generalizes to unseen user-ad combinations

### Facebook DLRM (Deep Learning Recommendation Model)
```
Sparse features (user_id, ad_id) → Embedding tables (huge, sharded)
Dense features (age, CTR, time)  → Bottom MLP
                    ↓
         Feature interaction (dot product)
                    ↓
                Top MLP
                    ↓
              P(click)
```

### Why not just GBDT?
- GBDT can't handle billions of sparse IDs efficiently
- Neural nets learn continuous embeddings → generalize to new IDs
- At Facebook/Google scale: neural net wins

---

## 6. Training

### Scale challenge
- 10T impressions/day → can't train on all data
- Solution: **online learning** + **mini-batch SGD**

```python
# Continuous training pipeline:
while True:
    batch = read_from_kafka(size=4096)   # fresh impressions + labels
    features = feature_store.fetch(batch)
    loss = BCE(model(features), labels)
    optimizer.step()                      # update model weights
    if step % 1000 == 0:
        checkpoint_model()               # save for rollback
```

**Importance of freshness:** Ad CTR patterns change hourly (lunch vs. dinner, weekday vs. weekend). Daily retraining is insufficient — need near-real-time updates.

### Negative sampling
```python
# CTR = 2% → 98% negatives → severe imbalance
# Solution: downsample negatives to 1:10 ratio
# Correction: re-calibrate output probabilities
# p_corrected = p_model / (p_model + (1-p_model)/sampling_rate)
```

---

## 7. Serving / Inference

```
10T impressions/day = 115M per second peak

Per request (user opens app):
  - 50-100 ad candidates from auction
  - Must score all in <10ms

Architecture:
  User feature fetch     → Redis (1ms)
  Ad feature fetch       → Redis (1ms)
  Model inference        → GPU cluster (5ms for 100 ads)
  Auction computation    → bid × pCTR (1ms)
  Winner selection       → (1ms)
  Response               → (1ms)
  Total: ~10ms
```

### Model serving optimizations
- **Quantization:** FP32 → INT8 (4× faster inference)
- **Embedding lookup:** Split embedding tables across multiple machines (model parallelism)
- **Caching:** User embeddings cached for 5 minutes (user doesn't change in 5 min)
- **Batch inference:** Score all 100 candidates in one forward pass

### Training-serving skew (critical!)
```
Problem: feature computed differently in training vs. serving
  Training:  avg_ctr = SQL query on yesterday's data
  Serving:   avg_ctr = Redis counter from today

Fix: feature store serves SAME features for training AND serving
  → Log serving features at inference time
  → Join logged features with labels for training
  → "Log and learn" architecture
```

---

## 8. Calibration

**Why calibration matters for ads:**
```
If model predicts P(click) = 0.10 but actual CTR = 0.06:
  → eCPM = bid × 0.10 = $1.00  (model thinks)
  → Actual = bid × 0.06 = $0.60
  → Platform overcharges advertiser
  → Advertiser ROI is negative → they leave

Fix: post-hoc calibration using Platt scaling or isotonic regression
  p_calibrated = sigmoid(a × p_model + b)  # fit a, b on held-out set
```

---

## 9. Monitoring

| Signal | Alert trigger |
|--------|--------------|
| AUC drops >1% | Model degradation |
| Log loss increases | Calibration drift |
| Predicted vs. actual CTR gap >20% | Calibration failure |
| Revenue per mille drops | System-level failure |
| Feature null rate >5% | Feature pipeline broken |
| Latency p99 >50ms | Serving regression |

**Sliced monitoring:** Monitor separately by country, device, ad_type — overall AUC can hide degradation in specific slices.

---

## Key Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Optimization target | Max CTR | Max eCPM | eCPM (click × bid) |
| Model freshness | Daily retrain | Online learning | Online (hourly updates) |
| Calibration | None | Platt scaling | Calibration required |
| Negative sampling | No sampling | 1:10 downsample | Downsample + recalibrate |
| User privacy | All features | Federated learning | Tradeoff (privacy sandbox) |
