# MLSD — Estimate Delivery Time (ETA)

> "Design a system to predict food delivery time for DoorDash / Uber Eats."

---

## 1. Problem Formulation

**Business goal:** Show accurate delivery time estimates to:
1. **Users** — set expectations, reduce cancellations
2. **Dashers (drivers)** — optimize routing + batch orders
3. **Restaurants** — start cooking at the right time

**What we predict:**
```
ETA = time_for_restaurant_to_prepare
    + time_for_dasher_to_arrive_at_restaurant
    + time_for_dasher_to_deliver_to_user
```

Three sub-problems → three models or one joint model.

**ML task:** Regression → predict delivery time in minutes

**Scale (DoorDash):**
- 37M active users
- 700K+ restaurant partners
- Peak: millions of orders/hour
- ETA shown before order placed (pre-order ETA) + live updates during delivery

**Clarifying questions:**
- Pre-order ETA (before dasher assigned) or live ETA (after pickup)?
- Single order or batched delivery (dasher carries 2 orders)?
- Food type (pizza vs. sushi affects prep time)?

---

## 2. Metrics

### Offline
| Metric | Description |
|--------|-------------|
| **MAE** (Mean Absolute Error) | Average error in minutes — primary |
| **RMSE** | Penalizes large errors more heavily |
| **MAPE** | Mean Absolute Percentage Error |
| **Within-N accuracy** | % of predictions within N minutes of actual |
| **P90 error** | 90th percentile error (tail performance) |

**Target:** MAE < 3 minutes, 80% predictions within 5 minutes of actual

### Online (A/B test)
| Metric | Target |
|--------|--------|
| Order cancellation rate | Must decrease |
| User satisfaction (post-delivery rating) | Must not decrease |
| Dasher utilization | Maintain/improve |
| Restaurant complaint rate | Maintain |
| Late delivery rate (> promised ETA) | Decrease |

**Business rule:** It's better to over-estimate by 2 min than under-estimate by 2 min.
→ Asymmetric loss: penalize late predictions more than early predictions.

---

## 3. Data

### Training data sources
| Source | Features |
|--------|---------|
| Historical orders | actual_delivery_time, actual_prep_time, actual_pickup_time |
| GPS traces | dasher route, speed, stops |
| Restaurant data | menu type, avg prep time by dish category, kitchen capacity |
| Traffic APIs | current + historical traffic by road segment |
| Weather APIs | rain, snow affect delivery speed |
| Map data | distance, road type, traffic lights |
| Time data | time of day, day of week, holidays |
| Restaurant capacity | current orders in queue, estimated wait |

### Label
```python
label = actual_delivery_time_minutes
      = timestamp_delivered - timestamp_order_placed

# Sub-labels:
prep_time   = timestamp_dasher_pickup - timestamp_restaurant_accepted
pickup_time = timestamp_dasher_at_restaurant - timestamp_dasher_assigned
dropoff_time = timestamp_delivered - timestamp_dasher_pickup
```

### Data challenges
- **Outliers:** Order that took 2 hours (restaurant closed) → clip at 95th percentile
- **Batch orders:** Dasher picks up 2 orders → harder to attribute delay
- **Cancellations:** No label → excluded from training
- **Time of day bias:** Peak hours have different distributions

---

## 4. Feature Engineering

### Restaurant features
```python
restaurant_id_embedding       # learned embedding
cuisine_type                  # italian / sushi / burger / pizza
avg_prep_time_last_30d        # rolling average
avg_prep_time_by_hour         # 6pm prep time vs 2pm
restaurant_current_order_queue # real-time: how many orders ahead
has_dedicated_dasher_station  # reduces pickup wait
distance_from_user            # crow-fly distance
```

### Order features
```python
num_items_ordered
total_order_value             # proxy for complexity
contains_custom_items         # longer to prepare
item_types                    # drinks fast, hot food slow
order_size_bucket             # small/medium/large
```

### Dasher features (if assigned)
```python
dasher_current_location
dasher_to_restaurant_distance
dasher_to_restaurant_eta      # from routing engine
dasher_acceptance_rate        # proxy for reliability
dasher_completion_rate
dasher_current_batch_size     # 0 = single order, 1 = batch
```

### Context features
```python
hour_of_day                   # 12-1pm peak = longer
day_of_week                   # Friday night surge
is_holiday                    # Thanksgiving = 2× prep time
weather_condition              # rain slows delivery 20%
precipitation_intensity
wind_speed
traffic_level_on_route        # real-time from Google Maps API
surge_multiplier              # platform demand indicator
```

### Geospatial features
```python
actual_route_distance         # from routing engine
num_traffic_lights_on_route
highway_vs_city_ratio
restaurant_to_user_zone       # urban / suburban / rural
```

---

## 5. Model Architecture

### Three-stage decomposition

```
ETA = prep_time_model + pickup_model + dropoff_model

Stage 1: Prep time prediction
  Input:  restaurant features + order features + time context
  Model:  Gradient Boosted Trees (XGBoost)
  Output: minutes until food ready

Stage 2: Pickup time prediction
  Input:  dasher location + restaurant location + traffic
  Model:  GBDT or routing engine (Google Maps API + correction model)
  Output: minutes until dasher arrives at restaurant

Stage 3: Dropoff time prediction
  Input:  restaurant location + user location + traffic + weather
  Model:  GBDT with routing features
  Output: minutes from restaurant to door

Final ETA = stage1 + stage2 + stage3 + buffer (uncertainty)
```

### Why GBDT not deep learning?
- Tabular features (time, distance, queue depth) → GBDT excels
- Feature interactions (rush hour × rainy weather × long route) captured automatically
- Fast inference (<5ms) needed
- Interpretable for debugging restaurant or dasher complaints

### Joint model (alternative)
```
All features → single XGBoost / LightGBM → total ETA
Pros: end-to-end optimization, simpler pipeline
Cons: harder to debug which stage is wrong
```

### Uncertainty estimation
```python
# Predict both mean and uncertainty
# Use quantile regression:
model_p50 = median ETA
model_p90 = 90th percentile ETA (show to user as "may take up to X minutes")

# Show user: "30-45 minutes" instead of "37 minutes"
# P50 used internally for dasher routing
# P90 used for user-facing display to reduce disappointment
```

---

## 6. Training

```python
# Features + labels from last 90 days of orders
# Features computed at time of order placement (not after)
# Why? Avoid data leakage: don't use features available only post-order

pipeline:
  1. Pull orders from last 90 days (BigQuery)
  2. Join with restaurant + dasher + weather + traffic at order_time
  3. Compute rolling averages (restaurant prep time last 30d)
  4. Remove outliers (>95th percentile delivery time)
  5. Train XGBoost (3 models or 1 joint)
  6. Evaluate: MAE, Within-5min accuracy, P90 error
  7. Retrain: daily (capture seasonal patterns)

# Real-time features updated continuously:
restaurant_current_queue: updated every 1 minute (Kafka stream)
traffic_level: Google Maps API called at serving time
```

### Asymmetric loss function
```python
# Being late is worse than being early
# Custom loss: penalize over-estimates (saying 30min when actual 45min) more

def asymmetric_mae(y_true, y_pred):
    errors = y_true - y_pred
    return mean(where(errors > 0,          # actual > predicted (late)
                      alpha * errors,       # alpha = 1.5 for late penalty
                      -1.0 * errors))       # normal penalty for early
```

---

## 7. Serving

```
User places order:
  1. Query restaurant queue (Redis, real-time, 2ms)
  2. Get routing ETA from Google Maps (10ms)
  3. Fetch weather + traffic features (5ms)
  4. Model inference: GBDT scoring (2ms)
  5. Compute ETA = prep + pickup + dropoff + buffer
  6. Return ETA range to user (e.g., "32-47 minutes")

Live updates (during delivery):
  - Every 2 minutes: recompute dropoff ETA using dasher GPS
  - If dasher stuck in traffic: update ETA immediately
  - Push notification if ETA changes by >5 minutes
```

### Restaurant start-cooking signal
```python
# Don't start cooking immediately when order placed
# Estimate when dasher will arrive at restaurant
# Trigger "start cooking" signal = dasher_arrival_time - prep_time

if now >= order_placed_time + (dasher_eta - avg_prep_time):
    send_signal_to_restaurant("start_cooking")
```

---

## 8. Monitoring

| Signal | Alert |
|--------|-------|
| MAE degrades >1 min | Model drift |
| % late deliveries increases | Systematic underestimation |
| Restaurant prep time anomaly | Specific restaurant issue |
| Weather feature null rate | API failure |
| P90 error spikes on Fridays | Surge pattern missed |

**Slice monitoring by:**
- Cuisine type (sushi vs. pizza have different prep distributions)
- Distance bucket (1mi vs. 5mi)
- Time of day (peak vs. off-peak)
- Weather (rainy vs. clear)

---

## Key Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Decompose or joint | 3 models | 1 joint model | 3 models (easier debugging) |
| Model type | GBDT | Neural net | GBDT (tabular features) |
| Routing | Build own | Use Google Maps | Use Maps + correction model |
| ETA display | Point estimate | Range (P50-P90) | Range (better UX) |
| Loss function | Symmetric MAE | Asymmetric (late penalized more) | Asymmetric |
| Update frequency | On order placed | Live updates every 2 min | Both |
