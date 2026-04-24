"""
COMPONENT 5 — Training Server

Responsibility: Train (or update) the model and save to registry.

Two modes:
  1. Full training  — on startup, uses all historical interactions
  2. Incremental    — reads from interaction_queue, updates model with new data

In production:
  - Scheduled by Apache Airflow (cron: every hour or daily)
  - Runs on GPU cluster for large models
  - Logs metrics to MLflow

Here: runs both modes sequentially to show the difference
"""

from recsys_data import INTERACTIONS, USERS, POSTS
from model import RecommendationModel
from model_registry import save_model, load_latest_model
from queue import simulate_incoming_events, interaction_queue


def full_training():
    """
    Train from scratch on all historical data.
    Called once on system startup or weekly reset.
    """
    print("\n[Training Server] FULL TRAINING")
    print(f"  Loading {len(INTERACTIONS)} historical interactions...")

    model = RecommendationModel()
    model.fit(INTERACTIONS)

    save_model(model, {
        "mode": "full",
        "training_rows": len(INTERACTIONS),
        "num_users": len(USERS),
        "num_posts": len(POSTS),
    })
    return model


def incremental_training():
    """
    Update existing model with new data from the queue.
    Called frequently (every few minutes / hourly).

    Why incremental?
      - Full retraining on 100B rows takes hours
      - Incremental update on last hour's data takes minutes
      - Keeps model fresh without full cost
    """
    print("\n[Training Server] INCREMENTAL TRAINING")

    # Step 1: Load current model from registry
    model = load_latest_model()

    # Step 2: Read new interactions from queue
    batch = interaction_queue.pop_batch(size=100)
    if not batch:
        print("  No new interactions in queue. Skipping.")
        return model

    print(f"  Processing {len(batch)} new interactions from queue...")
    new_interactions = [
        (e.payload["user_id"], e.payload["post_id"], e.payload["liked"])
        for e in batch
    ]

    # Step 3: Update model with new data
    model.partial_fit(new_interactions)

    # Step 4: Save updated model back to registry
    save_model(model, {
        "mode": "incremental",
        "new_rows": len(new_interactions),
    })

    print(f"  Updated model saved to registry.")
    return model


if __name__ == "__main__":
    print("=== Training Server Demo ===")

    # Run full training first
    model = full_training()

    # Simulate new events arriving
    print("\n[Simulating] New user interactions arriving on platform...")
    simulate_incoming_events()
    print(f"  Interaction queue size: {interaction_queue.size()}")

    # Run incremental training on new data
    model = incremental_training()

    # Show what model predicts now
    print("\n[Training Server] Sample predictions after update:")
    for uid in list(USERS.keys())[:2]:
        top = model.rank_posts(uid, list(POSTS.keys()), top_k=2)
        print(f"  {USERS[uid]['name']:25s}: {[(p, f'{s:.2f}') for p,s in top]}")
