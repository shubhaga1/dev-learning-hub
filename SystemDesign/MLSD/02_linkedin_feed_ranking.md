# MLSD — LinkedIn Feed Ranking

> "Design a ranking system for LinkedIn's home feed."

---

## 1. Problem Formulation

**Business goal:** Show professionally relevant content that drives meaningful engagement.

**What we predict:** P(user engages meaningfully with post | user, post, context)

**ML task:** Multi-objective ranking with engagement prediction

**LinkedIn-specific nuance:**
- Professional context → quality > quantity of engagement
- A "like" from CEO matters more than from a bot account
- Spam/clickbait severely damages brand trust
- Long-form articles valued differently from quick updates

**Scale:**
- 950M+ members
- 1B+ feed impressions/day
- Posts: job updates, articles, short posts, reposts, ads

---

## 2. Metrics

### Offline
| Metric | Description |
|--------|-------------|
| NDCG@K | Ranking quality of engaged posts |
| AUC-ROC per action type | Click, like, comment, share prediction |
| Calibration | Predicted prob matches actual rate |

### Online (A/B test)
| Metric | Priority |
|--------|----------|
| Meaningful engagement (comments + shares) | Primary |
| Dwell time | Secondary |
| Connection requests sent | Tertiary (virality) |
| Feed revisit rate | Long-term health |
| Spam report rate | Guardrail — must not increase |
| Ad revenue | Business guardrail |

**Key insight:** LinkedIn tracks "viral actions" (comments, shares) over passive actions (likes, scrolls) — these drive professional conversations.

---

## 3. Data

### Content sources in feed
```
1st-degree connections' posts
2nd-degree content (your connections liked/commented)
Followed companies/influencers
Suggested content (interest-based)
Ads (interleaved)
LinkedIn Learning / Jobs (promoted)
```

### Training data
| Signal | Use |
|--------|-----|
| Post impressions + engagement | Click/like/comment labels |
| Dwell time | Quality signal |
| Share/reshare | Strongest positive signal |
| "Hide post" / unfollow | Negative signal |
| Profile views triggered by post | Downstream conversion |
| Connection acceptance after viewing | Network quality signal |

### Label construction
```python
# Engagement hierarchy (weighted):
score = (
    0.1  × clicked
  + 0.2  × liked
  + 0.5  × commented
  + 1.0  × shared
  + 0.3  × dwell_30s
  - 0.5  × hide_post
  - 1.0  × report_spam
)
```

---

## 4. Feature Engineering

### Author / Creator features
```
connection_degree (1st/2nd/3rd)
author_engagement_rate_last_30d
author_credibility_score  (job title, company, tenure)
author_follower_count
is_influencer / thought_leader flag
posting_frequency
past_content_quality_score
```

### Post / Content features
```
post_age_hours
content_type  (text / image / video / article / poll / job)
text_embedding  (BERT on post content)
topic_relevance_to_user  (career field match)
has_external_link  (slightly penalized unless quality)
initial_engagement_velocity  (likes/comments in first hour)
media_quality_score
```

### User features
```
industry, job_function, seniority_level
connection_graph_features:
  - common_connections with author
  - interaction_history with author
  - network_centrality
topic_affinity  (topics engaged with last 90d)
session_context  (morning commute vs. lunch vs. evening)
```

### Interaction / Relationship features
```python
user_author_interaction_score:
  = weighted sum of (liked, commented, messaged, viewed_profile)
    for this author in last 6 months

content_relevance_score:
  = cosine_sim(user_interest_embedding, post_topic_embedding)

network_social_proof:
  = count of 1st-degree connections who engaged with post
```

---

## 5. Model Architecture

### Multi-stage pipeline

```
All available posts (10,000s)
        ↓
[FILTERING] Rules-based
  - Remove spam/reported content
  - Remove already-seen posts
  - Remove blocked users
        ↓ ~2,000 posts
[LIGHT RANKER] Logistic regression / small GBDT
  - Fast scoring on simple features
        ↓ top 500
[HEAVY RANKER] Multi-task deep neural network
        ↓ top 100
[DIVERSITY + ADS] Re-ranking layer
        ↓ top 20-25 shown in feed
```

### Heavy Ranker — Multi-task Neural Net

```
Input features (concatenated embeddings + dense features)
        ↓
Shared layers (512 → 256 → 128)
        ↓
Task heads:
  P(click)        → sigmoid
  P(like)         → sigmoid
  P(comment)      → sigmoid
  P(share)        → sigmoid
  P(dwell_30s)    → sigmoid
  P(hide)         → sigmoid  (negative — penalize)
  P(report_spam)  → sigmoid  (negative — strong penalize)

Final score = Σ wᵢ × headᵢ  (weights tuned via A/B)
```

### Why multi-task for LinkedIn specifically?
- Comment signal is sparse (~1% rate) — sharing parameters with click (5% rate) helps
- Spam detection benefits from same content features as engagement
- Joint training prevents optimizing one metric at expense of another

---

## 6. Feed Construction Rules

After ranking, apply re-ranking layer:

```python
def rerank_feed(scored_posts, user):
    feed = []
    seen_authors = Counter()
    seen_topics = Counter()

    for post in scored_posts:
        # Author diversity: max 2 posts from same author
        if seen_authors[post.author] >= 2:
            continue

        # Topic diversity: avoid 3+ consecutive same topic
        if seen_topics[post.topic] >= 3:
            deprioritize(post)

        # Content type diversity: not 5 videos in a row
        if consecutive_same_type >= 3:
            inject_different_type()

        # Ad injection: every 5th post
        if len(feed) % 5 == 4:
            inject_ad(user)

        feed.append(post)
        seen_authors[post.author] += 1
        seen_topics[post.topic] += 1

    return feed[:25]
```

---

## 7. Training

```
Weekly pipeline:
  1. Collect impressions + engagement logs (Kafka)
  2. Feature join (user profile + post features + author features)
  3. Label construction (engagement hierarchy scoring)
  4. Train multi-task model (4-6 hours on GPU cluster)
  5. Offline eval: AUC per task, NDCG@10, spam precision@95% recall
  6. Shadow traffic test (shadow mode, no user impact)
  7. A/B test (5% traffic, 2 weeks)
  8. Full rollout if meaningful engagement +X%, spam rate unchanged
```

**Online signals:** Last-hour engagement velocity used as real-time feature (not for training)

---

## 8. Serving

```
Latency budget: 200ms

User opens LinkedIn app:
  → User feature fetch (Redis cache, 10ms)
  → Candidate generation (post index + social graph, 20ms)
  → Feature assembly for candidates (30ms)
  → Light ranker (CPU, batch, 20ms)
  → Heavy ranker (GPU inference, 50ms for top 500)
  → Re-ranking + ad injection (20ms)
  → Response (20ms)
```

**Pre-computation:** For high-DAU users, pre-rank feed every 15 minutes in background.

---

## 9. Spam & Quality Control

Critical for LinkedIn's professional brand:

```
Pre-ranking filters:
  - Spam classifier (separate model, trained on reported content)
  - Duplicate/near-duplicate detection
  - Account credibility score (age, verification, connection quality)
  - Engagement velocity anomaly (1000 likes in 1 minute = suspicious)

Post-ranking safety:
  - Hate speech / harmful content classifier
  - Misinformation flagging (linked to fact-check APIs)
```

---

## 10. Cold Start

### New member
- Use industry + job function as initial interest vector
- Show content from top creators in their field
- "What would you like to see?" onboarding prompt
- After 10 engaged posts → personalized model kicks in

### New post
- First 1 hour: show to 1% of followers as "explore" traffic
- If engagement rate > threshold → amplify to full network
- Author credibility score determines initial distribution width

---

## Key Trade-offs

| Decision | Trade-off | LinkedIn's choice |
|----------|-----------|-------------------|
| Engagement type | Likes (easy) vs Comments (quality) | Weight comments 5× likes |
| Reach | Author following vs. Viral spread | Balance both with decay |
| Ads density | Revenue vs. UX | Every 5th post max |
| Freshness | Recency vs. Relevance | Relevance-first with freshness boost |
| Personalization | Filter bubble vs. Discovery | 20% exploration outside affinity |
