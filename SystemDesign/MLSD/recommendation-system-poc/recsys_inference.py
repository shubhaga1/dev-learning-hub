"""
COMPONENT 6 — Inference Server + Cache

Responsibility: Pre-compute recommendations for all users and store in cache.

Why pre-compute instead of real-time inference?
  - Real-time: user requests → load model → score posts → return  (100ms+)
  - Pre-computed: user requests → read from cache → return          (1ms)

Flow:
  1. Reads new posts from post_queue
  2. Scores every user × new post using the latest model
  3. Stores top-K recommendations per user in cache
  4. Cache auto-evicts when full (LRU eviction)

In production:
  - Inference server is always running (daemon process)
  - Cache = Redis (in-memory, shared across API instances)
  - Multiple inference servers in parallel for scale
"""

from collections import OrderedDict
from recsys_registry import load_latest_model
from recsys_queue import post_queue, simulate_incoming_events
from recsys_data import USERS, POSTS


# ── In-Memory Cache (simulates Redis) ─────────────────────
class RecommendationCache:
    """
    Stores top-K recommendations per user.
    LRU eviction when max_size reached.

    In production: Redis with TTL (time-to-live) expiry
    """

    def __init__(self, max_size: int = 1000):
        self._store   = OrderedDict()   # user_id → [(post_id, score), ...]
        self.max_size = max_size
        self.hits     = 0
        self.misses   = 0

    def set(self, user_id: str, recs: list):
        if user_id in self._store:
            self._store.move_to_end(user_id)
        self._store[user_id] = recs
        if len(self._store) > self.max_size:
            self._store.popitem(last=False)   # evict least-recently-used

    def get(self, user_id: str) -> list:
        if user_id not in self._store:
            self.misses += 1
            return None
        self.hits += 1
        self._store.move_to_end(user_id)
        return self._store[user_id]

    def stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        print(f"  Cache: {len(self._store)} users | hit rate: {hit_rate:.0%} ({self.hits} hits, {self.misses} misses)")


# Shared cache — all API instances read from here
cache = RecommendationCache(max_size=500)


class InferenceServer:
    """
    Continuously runs in background.
    Scores new posts against all users → fills cache.
    """

    def __init__(self):
        self.model    = None
        self.top_k    = 5           # recommendations per user
        self.all_posts = list(POSTS.keys())

    def load_model(self):
        print("[Inference Server] Loading latest model from registry...")
        self.model = load_latest_model()

    def run_once(self):
        """
        One cycle: read new posts from queue → score → update cache.
        In production: runs in an infinite loop with sleep(60).
        """
        if self.model is None:
            self.load_model()

        # Read new posts that arrived
        new_post_events = post_queue.pop_batch(size=50)
        if not new_post_events:
            print("[Inference Server] No new posts. Cache unchanged.")
            return

        print(f"[Inference Server] Processing {len(new_post_events)} new posts...")

        # Add new posts to the known posts dict so make_features can look them up
        for e in new_post_events:
            pid = e.payload["post_id"]
            if pid not in POSTS:
                POSTS[pid] = {"features": e.payload["features"], "title": e.payload.get("title", pid)}

        new_post_ids = [e.payload["post_id"] for e in new_post_events]
        all_posts_to_score = self.all_posts + new_post_ids

        # For every user, re-score all posts and update cache
        for user_id in USERS:
            top_recs = self.model.rank_posts(user_id, all_posts_to_score, top_k=self.top_k)
            cache.set(user_id, top_recs)

        print(f"[Inference Server] Cache updated for {len(USERS)} users.")

    def refresh_model(self):
        """Called after training server publishes a new model version."""
        print("[Inference Server] Refreshing model from registry...")
        self.load_model()


if __name__ == "__main__":
    print("=== Inference Server + Cache Demo ===\n")

    # First, make sure training ran (need a model in registry)
    from recsys_training import full_training
    full_training()

    # Simulate new posts arriving
    simulate_incoming_events()

    # Run inference server
    server = InferenceServer()
    server.run_once()

    print("\n[Cache] Contents after inference run:")
    for uid in USERS:
        recs = cache.get(uid)
        if recs:
            rec_str = ", ".join(f"{pid}({s:.2f})" for pid, s in recs[:3])
            print(f"  {USERS[uid]['name']:25s}: {rec_str}")

    cache.stats()
