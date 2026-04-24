"""
COMPONENT 7 — API Layer

Responsibility: Serve recommendations to users in real time.

Flow:
  1. User opens their feed → GET /recommendations/{user_id}
  2. API reads from cache (1ms)
  3. If cache miss → fallback to real-time inference (100ms)
  4. Return ranked list of post IDs

In production:
  - FastAPI / Flask behind a load balancer
  - Multiple instances (horizontal scaling)
  - Cache miss rate < 5% (inference server keeps cache warm)
"""

from inference_server import cache, InferenceServer
from model_registry import load_latest_model
from recsys_data import USERS, POSTS

SEP = "-" * 50

# Fallback model for cache misses (always loaded in memory)
_fallback_model = None

def _get_fallback_model():
    global _fallback_model
    if _fallback_model is None:
        _fallback_model = load_latest_model()
    return _fallback_model


def get_recommendations(user_id: str, top_k: int = 5) -> dict:
    """
    Main API endpoint — GET /recommendations/{user_id}

    Returns:
      {
        "user_id": "u1",
        "source": "cache" | "realtime",
        "recommendations": [
          {"post_id": "p1", "score": 0.92, "title": "..."},
          ...
        ]
      }
    """
    if user_id not in USERS:
        return {"error": f"User {user_id} not found"}

    # ── Try cache first (fast path) ────────────────────────
    cached = cache.get(user_id)
    if cached:
        return {
            "user_id": user_id,
            "source":  "cache",                      # came from Redis
            "latency": "~1ms",
            "recommendations": _enrich(cached[:top_k]),
        }

    # ── Cache miss: real-time inference (slow path) ────────
    # This should rarely happen if inference server is running
    print(f"  [API] Cache miss for {user_id} — falling back to real-time inference")
    model  = _get_fallback_model()
    ranked = model.rank_posts(user_id, list(POSTS.keys()), top_k=top_k)

    return {
        "user_id": user_id,
        "source":  "realtime",                       # computed on demand
        "latency": "~100ms",
        "recommendations": _enrich(ranked),
    }


def _enrich(ranked: list) -> list:
    """Add post metadata to scored list."""
    return [
        {
            "post_id": pid,
            "score":   round(score, 3),
            "title":   POSTS.get(pid, {}).get("title", "Unknown"),
        }
        for pid, score in ranked
    ]


def simulate_user_requests():
    """Simulate multiple users hitting the API."""
    print(f"\n{'='*55}")
    print("API — Serving Recommendations")
    print(f"{'='*55}")

    for user_id in USERS:
        response = get_recommendations(user_id, top_k=3)
        print(f"\nUser: {USERS[user_id]['name']} ({user_id})")
        print(f"Source: {response['source']} | Latency: {response.get('latency','')}")
        for i, rec in enumerate(response["recommendations"], 1):
            print(f"  {i}. [{rec['score']}] {rec['title']}")


if __name__ == "__main__":
    print("=== API Layer Demo ===\n")

    # Setup: train model + fill cache
    from training_server import full_training
    from queue import simulate_incoming_events
    full_training()
    simulate_incoming_events()

    server = InferenceServer()
    server.run_once()

    # Now serve requests
    simulate_user_requests()

    print(f"\n{SEP}")
    cache.stats()

    # Show a cache miss scenario
    print(f"\n{SEP}")
    print("Cache miss scenario (new user with no cache entry):")
    result = get_recommendations("u_new_user_not_in_cache", top_k=3)
    print(f"  Result: {result}")
