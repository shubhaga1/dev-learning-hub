"""
COMPONENT 4 — Queue System (simulates Kafka / SQS)

In production: Apache Kafka or AWS SQS
  - New user interactions arrive as events
  - New posts arrive as events
  - Training server consumes from interaction queue
  - Inference server consumes from post queue

Why queues instead of polling the DB?
  - DB polling is slow + expensive
  - Queue tracks exactly what's been processed
  - Multiple consumers can read in parallel
  - Built-in retry / error handling

Here: simple Python list as queue
"""

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    event_type: str    # "interaction" or "new_post"
    payload:    dict
    timestamp:  str = field(default_factory=lambda: datetime.now().isoformat())


class Queue:
    """FIFO queue — simulates Kafka topic."""

    def __init__(self, name: str):
        self.name   = name
        self._items = deque()

    def push(self, event: Event):
        self._items.append(event)

    def pop_batch(self, size: int = 10) -> list[Event]:
        """Read up to `size` events and remove them (like Kafka commit)."""
        batch = []
        for _ in range(min(size, len(self._items))):
            batch.append(self._items.popleft())
        return batch

    def size(self) -> int:
        return len(self._items)

    def __repr__(self):
        return f"Queue({self.name}, {self.size()} items)"


# ── Shared queues (one per topic) ─────────────────────────
interaction_queue = Queue("user-interactions")   # training server reads this
post_queue        = Queue("new-posts")           # inference server reads this


def simulate_incoming_events():
    """Simulates real-time events arriving from the platform."""

    # New user interactions (likes/dislikes happening right now)
    new_interactions = [
        ("u1", "p7", 0),
        ("u2", "p6", 0),
        ("u3", "p8", 0),
        ("u4", "p2", 1),
    ]
    for uid, pid, liked in new_interactions:
        interaction_queue.push(Event(
            event_type="interaction",
            payload={"user_id": uid, "post_id": pid, "liked": liked}
        ))

    # New posts published on the platform
    from recsys_data import NEW_POSTS
    for pid, pdata in NEW_POSTS.items():
        post_queue.push(Event(
            event_type="new_post",
            payload={"post_id": pid, **pdata}
        ))


if __name__ == "__main__":
    print("=== Queue System Demo ===\n")

    simulate_incoming_events()

    print(f"Queues after events arrive:")
    print(f"  {interaction_queue}")
    print(f"  {post_queue}")

    print(f"\nTraining server reads interaction_queue (batch of 3):")
    batch = interaction_queue.pop_batch(size=3)
    for e in batch:
        print(f"  {e.event_type}: {e.payload}")
    print(f"  Remaining in queue: {interaction_queue.size()}")

    print(f"\nInference server reads post_queue:")
    batch = post_queue.pop_batch()
    for e in batch:
        print(f"  New post: {e.payload['post_id']} — {e.payload['title']}")
