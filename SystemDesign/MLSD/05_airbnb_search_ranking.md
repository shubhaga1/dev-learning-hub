# MLSD — Airbnb Search Ranking

> "Design a search ranking system for Airbnb listings."

---

## 1. Problem Formulation

**Business goal:** Show listings that users will book, maximizing GMV (Gross Merchandise Value) while maintaining guest and host satisfaction.

**What we predict:** P(user books listing | user, listing, search query, context)

**Why booking probability, not click probability?**
- Optimizing clicks → clickbait listings with nice photos but terrible reviews
- Optimizing bookings → actually measures guest satisfaction + host revenue
- Airbnb's metric: **LGBR** (Listing Gross Booking Revenue per Search)

**Scale:**
- 150M users
- 7M+ listings globally
- 200M+ search queries/year
- Search returns 300+ listings, show top 20 per page

**ML task:** Learning to Rank (LTR) — rank listings by booking probability

---

## 2. Metrics

### Offline
| Metric | Description |
|--------|-------------|
| **NDCG@K** | Primary — ranking quality (booked listings ranked higher) |
| **MRR** (Mean Reciprocal Rank) | How soon does a booked listing appear? |
| **AUC-ROC** | Click/booking prediction quality |
| **Precision@5** | % of top-5 results that get booked |

### Online (A/B test)
| Metric | Target |
|--------|--------|
| Booking rate | Primary — % of searches resulting in booking |
| GMV per search | Revenue impact |
| Guest satisfaction (post-stay rating) | Quality guardrail |
| Host acceptance rate | Supply health |
| Search-to-book conversion | Funnel metric |
| Long-term repeat bookings | Retention |

**Guardrails:** Don't sacrifice host diversity (don't show only 5-star superhosts) — new hosts need exposure to grow supply.

---

## 3. Data

### Training data pipeline
```
User searches → Impressions logged
              → User clicks on listing → click label
              → User inquires/contacts host → inquiry label
              → User books → booking label (primary)
              → User checks in + leaves review → satisfaction label
```

### Label construction
```python
# Multi-level labels for listwise ranking:
label = 0  # shown but not clicked (implicit negative)
label = 1  # clicked
label = 2  # inquired / contacted host
label = 3  # booked
label = 4  # booked AND left 5-star review (best signal)

# Use label for NDCG computation:
relevance_grade = label  # 0-4 scale
```

### Challenge: Selection bias / Position bias
```
Problem: Top-ranked listings get shown more → more bookings
         → Model thinks they're better → shows them more → feedback loop

Fix: Inverse Propensity Scoring (IPS)
  weight = 1 / P(shown_at_position_k)
  Higher positions get lower weight (they were shown because they were ranked high)
```

### Data split — time-based
```python
# Never use future data to predict past
train: search sessions from months 1-10
valid: month 11
test:  month 12

# Don't use random split — leaks future listing quality into past
```

---

## 4. Feature Engineering

### Listing features
```python
listing_id_embedding          # learned, 64-dim
price_per_night               # absolute price
price_vs_market_avg           # relative to similar listings in area
review_score_rating           # 1-5 stars
number_of_reviews             # volume of social proof
is_superhost                  # Airbnb quality designation
response_rate                 # host responsiveness
response_time_hours           # avg time to respond
cancellation_policy           # flexible / moderate / strict
instant_book_enabled          # no host approval needed
amenities_score               # WiFi, AC, kitchen, pool...
photos_quality_score          # ML model on listing photos
capacity_vs_group_size        # fit for this search's group size
```

### Query / Search features
```python
check_in_date
check_out_date
num_nights = checkout - checkin
num_guests
location_query               # "Paris", "beach", bounding box
price_filter_min, max        # user's stated budget
amenity_filters              # pool, pet-friendly, etc.
flexibility_window           # ±3 days search
days_until_checkin           # urgency signal
```

### Availability features (real-time)
```python
is_available_for_search_dates  # critical filter
available_nights_in_window     # partial availability
price_for_exact_dates          # may differ from base price
```

### User features
```python
user_id_embedding              # learned, 64-dim
booking_history_count          # experienced traveler?
avg_price_booked               # spending behavior
preferred_room_type            # entire place / private room / shared
avg_group_size
destinations_booked            # travel pattern
past_review_given_avg          # generous vs. critical reviewer
```

### Interaction features
```python
listing_location_to_query_distance  # km from search location
price_vs_user_avg_spend             # within user's typical range?
listing_type_vs_user_preference     # matches past booking type
host_language_match                 # user and host speak same language
listing_in_user_wishlist            # explicit signal
similarity_to_past_bookings         # embedding cosine sim
```

### Seasonal / temporal features
```python
days_until_checkin               # last-minute vs. advance
seasonality_factor               # summer listing in winter
local_events                     # concerts, conferences nearby
weekend_vs_weekday               # different demand patterns
```

---

## 5. Model Architecture

### Ranking pipeline

```
Search query (location, dates, guests)
        ↓
[FILTERING] Hard constraints
  - Available for exact dates
  - Matches capacity (guests)
  - Within price range (if filter set)
  - Not already booked by user
        ↓ → ~5,000-20,000 listings
[RETRIEVAL / LIGHT RANKING]
  - Fast scoring: price + distance + rating heuristic
  - Embedding similarity (query vs. listing)
        ↓ → top 300
[HEAVY RANKING] LambdaRank / Neural LTR model
        ↓ → top 50
[DIVERSIFICATION] Geo-diversity + price diversity
        ↓ → 20 listings per page
```

### Heavy Ranker: Neural Learning to Rank

```
Input:
  Listing features (dense + embedding)
  User features (dense + embedding)
  Query features
  Interaction features (listing × user × query)
        ↓
Shared layers: FC(512) → FC(256) → FC(128)
        ↓
Output heads:
  P(click)            → sigmoid
  P(contact_host)     → sigmoid
  P(booking)          → sigmoid  ← PRIMARY
  Expected_GMV        → linear   (price × P(booking))

Training loss: LambdaRank (pairwise) or ListNet (listwise)
  Optimize NDCG directly via surrogate gradient
```

### Why LambdaRank over pointwise models?
- Pointwise (MSE on booking probability): ignores relative ordering
- Pairwise: "Listing A should rank above Listing B" — directly optimizes ranking
- LambdaRank weights pairwise losses by NDCG gain → directly optimizes NDCG

---

## 6. Price Optimization (unique to Airbnb)

Search ranking interacts with price:
```python
# Listings with lower price rank higher (all else equal)
# But model should penalize listings that are TOO cheap (might be low quality)
# or TOO expensive (won't convert)

value_score = review_score / log(price + 1)

# Price sensitivity varies by user:
price_sensitivity = 1 - (user_avg_spend / listing_price)
```

**Dynamic pricing awareness:**
- Listings can change prices → fetch real-time price for search dates
- Surge pricing (events, holidays) affects rank

---

## 7. Cold Start

### New listing
```
No reviews, no booking history → cold start

Approach:
  1. Content-based features only (photos, description, amenities, location)
  2. Similar listing proxy: find nearby listings with similar amenities → use their CTR as prior
  3. "New listing boost": temporarily boost rank to get initial impressions
  4. After 5 bookings: use actual signals
  5. After 20 reviews: full personalized ranking
```

### New user
```
No booking history → can't personalize

Approach:
  1. Location-based popular listings
  2. Price filter if set → use as personalization signal
  3. Onboarding: "What kind of trips do you take?" (solo/couple/family)
  4. After 1st booking: use booking as initial preference signal
```

---

## 8. Training

```python
# Weekly retraining pipeline:
1. Pull last 6 months of search sessions (BigQuery)
2. Filter: only sessions with at least 1 booking in search results
3. Feature join: listing features at time of search
4. Apply IPS weights (debias position)
5. Train LambdaRank model on GPU cluster
6. Evaluate: NDCG@5, NDCG@10, booking rate on holdout
7. A/B test on 5% traffic (2 weeks)
8. If booking rate +X% → full rollout
```

**Freshness:** Listing review scores updated hourly (affects ranking signal).

---

## 9. Serving

```
Latency budget: 300ms

User submits search:
  → Availability check (Solr/Elasticsearch, 20ms)
  → Filter by capacity/price/amenities (20ms)
  → User feature fetch (Redis, 5ms)
  → Listing feature fetch (Redis for hot listings, 10ms)
  → Light ranker (CPU, 30ms, top 300)
  → Feature assembly (join user × listing × query, 30ms)
  → Heavy ranker (GPU inference, 80ms)
  → Diversification rules (10ms)
  → Response (20ms)
  Total: ~225ms
```

**Caching:**
- Listing features cached in Redis (refresh hourly)
- Popular destination × date combinations pre-ranked (invalidated when listings change)

---

## 10. Monitoring

| Signal | Alert |
|--------|-------|
| Booking rate drops >2% | Model degradation |
| New host booking rate drops | Supply health |
| Price distribution of shown listings shifts | Pricing bias |
| NDCG on holdout drops | Ranking quality |
| Availability feature null rate | Inventory system issue |
| P99 search latency >500ms | Serving regression |

**Fairness monitoring:**
- Are new hosts getting fair exposure vs. superhosts?
- Are listings in non-English locations ranked fairly?
- Price discrimination? (same listing, different prices for different user groups?)

---

## Key Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Optimize | Clicks | Bookings | Bookings (aligns with GMV) |
| Loss function | MSE (pointwise) | LambdaRank (pairwise) | LambdaRank |
| New listings | Rank low (no signals) | Boost (explore) | Boost for first 10 bookings |
| Diversity | Pure relevance | Price + geo diversity | Diversity (prevents monopoly) |
| Host fairness | Superhost preference | Level playing field | Balance with quality floor |
