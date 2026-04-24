"""
END-TO-END DEMO — Full Recommendation System

Runs all 7 components in sequence showing the complete flow.

Architecture:
  Data → Training Server → Model Registry
                                ↓
  Queue → Inference Server → Cache → API → User

Run: python3 run_all.py
"""

from recsys_data import USERS, POSTS, INTERACTIONS, NEW_POSTS
from recsys_model import RecommendationModel
from recsys_registry import save_model, load_latest_model, list_versions
from recsys_queue import interaction_queue, post_queue, simulate_incoming_events, Event
from recsys_training import full_training, incremental_training
from recsys_inference import cache, InferenceServer
from recsys_api import get_recommendations

DIVIDER = "\n" + "=" * 60

# ── STEP 1: Full Training on historical data ───────────────
print(DIVIDER)
print("STEP 1 — Full Training (all historical interactions)")
print("=" * 60)
print(f"  {len(INTERACTIONS)} historical interactions across {len(USERS)} users, {len(POSTS)} posts")
model = full_training()

# ── STEP 2: Events arrive (new interactions + new posts) ───
print(DIVIDER)
print("STEP 2 — New events arrive on the platform")
print("=" * 60)
simulate_incoming_events()
print(f"  Interaction queue: {interaction_queue.size()} new events")
print(f"  Post queue:        {post_queue.size()} new posts")
for pid, pdata in NEW_POSTS.items():
    print(f"    New post → {pid}: {pdata['title']}")

# ── STEP 3: Incremental Training ──────────────────────────
print(DIVIDER)
print("STEP 3 — Incremental Training (update model with new data)")
print("=" * 60)
print("  Why? Full retraining is expensive. Update with recent events only.")
model = incremental_training()

# ── STEP 4: Model Registry ────────────────────────────────
print(DIVIDER)
print("STEP 4 — Model Registry (version history)")
print("=" * 60)
list_versions()

# ── STEP 5: Inference Server fills cache ──────────────────
print(DIVIDER)
print("STEP 5 — Inference Server pre-computes recommendations")
print("=" * 60)
print("  Why? Pre-compute so API responses are instant (1ms vs 100ms)")

# Refill post queue since Step 2 drained it partially
simulate_incoming_events()

server = InferenceServer()
server.run_once()

# ── STEP 6: API serves cached recommendations ─────────────
print(DIVIDER)
print("STEP 6 — API serves recommendations from cache")
print("=" * 60)

for user_id, udata in USERS.items():
    response = get_recommendations(user_id, top_k=3)
    print(f"\n  {udata['name']} ({user_id})  [{response['source']} | {response.get('latency','')}]")
    for i, rec in enumerate(response["recommendations"], 1):
        print(f"    {i}. [{rec['score']:.3f}] {rec['title']}")

# ── Summary ────────────────────────────────────────────────
print(DIVIDER)
print("SUMMARY — What each component does")
print("=" * 60)
print("""
  01_data.py            → Database: users, posts, interactions
  02_model.py           → ML model: P(user likes post)
  03_model_registry.py  → MLflow: save/load/version models
  04_queue.py           → Kafka: buffer new events
  05_training_server.py → Train model (full + incremental)
  06_inference_server.py→ Pre-score all users × posts → cache
  07_api.py             → Serve cached recs to users (~1ms)

  Feedback loop:
    User likes/skips → interaction_queue
    → Training server → updated model → registry
    → Inference server → updated cache
    → API → better recommendations → user
""")
cache.stats()
