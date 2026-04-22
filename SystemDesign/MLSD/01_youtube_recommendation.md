# MLSD — YouTube Recommendation

> "Design a recommendation system for YouTube's homepage."

---

## 1. Problem Formulation

**Business goal:** Maximize long-term user satisfaction and watch time.

**What we predict:** P(user watches video for >50% | user, video, context)

**ML task:** Two-stage — retrieval (ANN) + ranking (regression/multi-task)

**Scale:**
- 2 billion logged-in users
- 800 million videos
- 500 hours of video uploaded every minute
- Homepage shown ~5B times/day

**Clarifying questions to ask:**
- Optimize for watch time or engagement (likes, shares)?
- Handle new users (cold start)?
- Real-time or batch recommendations?

---

## 2. Metrics

### Offline
| Metric | Description |
|--------|-------------|
| Precision@10 | % of top-10 recommendations actually watched |
| Recall@10 | % of videos user would watch that appear in top-10 |
| NDCG@10 | Ranking quality weighted by position |
| AUC-ROC | Click prediction quality |

### Online (A/B test)
| Metric | Target |
|--------|--------|
| Watch time per session | Primary — maximize |
| CTR | Secondary — proxy for relevance |
| Session length | Overall engagement |
| Return rate (next day) | Long-term satisfaction |
| Abandonment rate | Negative signal |

**Key insight:** Don't optimize CTR alone — "clickbait" maximizes CTR but destroys watch time and long-term retention.

---

## 3. Data

### Training data sources
| Source | Signal |
|--------|--------|
| Watch history | Videos watched + duration |
| Search history | User intent |
| Likes, shares, saves | Explicit positive signals |
| Skips, dislikes | Explicit negative signals |
| Impressions | Videos shown but not clicked (negative) |
| Video metadata | Title, description, tags, category, transcript |
| Creator features | Subscriber count, upload frequency |

### Label construction
```
Label = 1  if watch_time / video_duration > 0.5
Label = 0  if impression AND (not clicked OR watch_time < 30s)

# Weighted label for regression:
label = min(watch_time, video_duration) * satisfaction_score
```

### Negative sampling
- **Random negatives**: sample from full video corpus
- **In-batch negatives**: other videos in the same batch
- **Hard negatives**: videos user saw on homepage but didn't click

### Data freshness
- User behavior signals: real-time (stream via Kafka)
- Video features: hourly batch update
- Retrain model: daily for ranking, weekly for retrieval embeddings

---

## 4. Feature Engineering

### User features
```
Static:   age_bucket, country, language, device_type, account_age
History:  last_50_watched_video_ids, avg_watch_percentage,
          top_5_categories, top_10_channels, time_since_last_session
Computed: watch_time_last_7d, search_frequency, like_rate
```

### Video features
```
Static:   category, language, duration_bucket, upload_date
Metadata: title_embedding (BERT), description_embedding, tags
Quality:  view_count, like_ratio, average_watch_percentage
Creator:  subscriber_count, channel_authority_score, upload_rate
```

### Context features
```
time_of_day_bucket (morning/afternoon/evening/night)
day_of_week
device_type (mobile/tablet/TV/desktop)
session_position (first video vs. deep in session)
country
```

### Cross / interaction features
```
user_category_affinity_score = P(watch | user, category)  # precomputed
user_channel_affinity_score  = avg_watch_pct for that channel
freshness_score = 1 / log(hours_since_upload + 1)
```

---

## 5. Model Architecture

### Two-stage pipeline

```
800M videos
    ↓
[RETRIEVAL] Two-Tower Model → top 500 candidates   (10-20ms)
    ↓
[RANKING]   Multi-task Neural Net → scored top 500  (30-50ms)
    ↓
[RE-RANKING] Diversity + freshness rules → top 20   (5ms)
    ↓
Homepage feed
```

### Stage 1: Retrieval — Two-Tower Model

```
User Tower:                    Video Tower:
user_id embedding              video_id embedding
watch_history avg pooling  →   title BERT embedding
context features           →   category embedding
         ↓                            ↓
    user_embedding (256d)    video_embedding (256d)
              ↓
    dot_product(user, video) = relevance score
```

**Training:** Sampled softmax or in-batch negatives
**Serving:** Pre-compute video embeddings, use Faiss ANN for retrieval

### Stage 2: Ranking — Multi-task Neural Net

```python
# Inputs: user features + video features + context features
# Shared bottom: 3 FC layers (512 → 256 → 128)

# Task heads:
P(click)       → sigmoid (binary cross-entropy loss)
E(watch_time)  → linear  (weighted MSE loss)
P(like)        → sigmoid (binary cross-entropy loss)
P(share)       → sigmoid (binary cross-entropy loss)

# Final score:
score = w1 × P(click) + w2 × E(watch_time) + w3 × P(like)
```

**Why multi-task?** Watch time, clicks, and likes are correlated. Shared representation learns common patterns; separate heads capture task-specific patterns.

### Stage 3: Re-ranking

```python
for video in ranked_top_100:
    if same_channel as prev 3:     penalize  # diversity
    if upload_age > 30 days:        penalize  # freshness
    if already_watched:             remove
    if not user_language:           penalize

final_feed = top_20_after_reranking
```

---

## 6. Training

```
Daily pipeline:
  1. Collect yesterday's impression + watch logs (Kafka → BigQuery)
  2. Join with feature store (user features, video features)
  3. Sample negatives (1:5 ratio)
  4. Train ranking model (distributed GPU training, 4h)
  5. Offline evaluation (AUC, NDCG@10 on holdout)
  6. If improvement > threshold → promote to shadow traffic
  7. A/B test → full rollout
```

**Retrieval embeddings:** Retrain weekly (more stable, expensive)
**Ranking model:** Retrain daily (captures trending topics)
**Online learning:** User feedback in last hour for trending signals

---

## 7. Serving

```
Latency budget: 150ms total

User request → Feature fetcher (Redis, 10ms)
            → Two-tower retrieval (Faiss ANN, 20ms)
            → Feature join for candidates (20ms)
            → Ranking model inference (GPU, 40ms)
            → Re-ranking rules (10ms)
            → Response assembly (10ms)
```

**Infrastructure:**
- Feature store: Redis (online, <5ms) + BigQuery (offline)
- Retrieval: Faiss index sharded across machines, rebuilt nightly
- Ranking: TensorFlow Serving on GPU clusters
- CDN: Cache pre-ranked feeds for high-traffic users

---

## 8. Cold Start

### New user
- Use **demographic-based** popularity (country, age, device)
- Show **trending** videos in their language
- After 3 watches → switch to collaborative filtering
- **Onboarding flow**: ask 3 topic preferences

### New video
- Use **content-based** features (title, thumbnail, category)
- **Bootstrapping**: promote to small audience, gather signals
- After 1,000 impressions → collaborative signals available
- **Creator authority**: established channels get faster ramp-up

---

## 9. Monitoring

| Signal | Alert |
|--------|-------|
| Watch time per session drops >5% | Model degradation |
| CTR drops vs. baseline | Retrieval quality |
| Score distribution shift | Feature/label drift |
| P99 latency > 200ms | Serving issue |
| Feedback loop bias | Score variance shrinking |

**Avoid filter bubbles:** Inject 10% exploration videos outside user's typical categories.

---

## Key Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Optimize for | CTR | Watch time | Watch time (less clickbait) |
| Retrieval | Collaborative filter | Two-tower | Two-tower (handles cold start better) |
| Ranking | Single task | Multi-task | Multi-task (correlated signals) |
| Freshness | Recency boost | Engagement score | Balance both |
| Diversity | Pure relevance | Explore/exploit (ε-greedy) | ε-greedy (10% exploration) |
