# ============================================================
# KAFKA CONCEPTS
#
# Kafka = distributed message queue / event streaming platform
#
# Real-world analogy: YouTube
#   - Creator uploads video        → PRODUCER
#   - YouTube stores it            → BROKER (Kafka server)
#   - Subscribers watch it         → CONSUMERS
#   - "Tech videos" category       → TOPIC
#   - Recommendation + Analytics   → different CONSUMER GROUPS
#     both read the same video independently
#
# ============================================================

print("""
╔══════════════════════════════════════════════════════════╗
║               KAFKA ARCHITECTURE                         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   PRODUCER          BROKER (Kafka)         CONSUMER      ║
║   ────────          ───────────────        ────────      ║
║   Your app    →→→   TOPIC: orders   →→→    Inventory     ║
║   sends msg         TOPIC: payments →→→    Billing       ║
║                     TOPIC: clicks   →→→    Analytics     ║
║                                                          ║
║   ZOOKEEPER (coordinator)                                ║
║   ─────────────────────────                              ║
║   - tracks which brokers are alive                       ║
║   - tracks partition leaders                             ║
║   - like a "cluster manager"                             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

print("KEY CONCEPTS:")
print("="*55)

concepts = {
    "Producer": """
    Sends messages TO a topic.
    Example: your order service sends every new order to
             the 'orders' topic.""",

    "Consumer": """
    Reads messages FROM a topic.
    Example: your inventory service reads from 'orders'
             to reduce stock. Your email service also
             reads 'orders' to send confirmation emails.
    Both read independently — neither blocks the other.""",

    "Topic": """
    A named channel/category for messages.
    Like a table in a database, or a queue.
    Messages are ORDERED and RETAINED (not deleted after read).
    Example topics: 'orders', 'payments', 'user-clicks'""",

    "Partition": """
    A topic is split into partitions for parallelism.
    Each partition = an ordered log file on disk.
    More partitions = more consumers can read in parallel.

    Topic 'orders' with 3 partitions:
      Partition 0: order1, order4, order7...
      Partition 1: order2, order5, order8...
      Partition 2: order3, order6, order9...""",

    "Offset": """
    Position of a message within a partition.
    Like a line number.
    Consumer tracks its offset → knows where it left off.
    If consumer crashes and restarts → continues from offset.""",

    "Broker": """
    The Kafka server that stores messages.
    In production: multiple brokers = fault tolerance.
    Our demo: 1 broker (enough for learning).""",

    "Zookeeper": """
    Kafka's coordinator (older Kafka needs this).
    Tracks: which brokers are alive, who leads each partition.
    Newer Kafka (KRaft mode): no Zookeeper needed.
    Our demo uses Zookeeper — still very common in prod.""",

    "Consumer Group": """
    Multiple consumers sharing the work of reading a topic.
    Each partition is read by exactly ONE consumer in the group.
    Two groups? Both get ALL messages independently.

    Group A (inventory): consumer1 reads p0, consumer2 reads p1
    Group B (analytics):  consumer3 reads p0, consumer4 reads p1
    Same messages, different readers.""",
}

for name, desc in concepts.items():
    print(f"\n  {name}:{desc}")

print("""

WHY KAFKA AND NOT A DATABASE?
══════════════════════════════
  Database: you query when you need data (pull)
  Kafka:    data flows to you as it happens (push/stream)

  E-commerce example WITHOUT Kafka:
    order service → directly calls inventory API
                 → directly calls email API
                 → directly calls analytics API
    Problem: if any service is down, order fails

  WITH Kafka:
    order service → publishes to 'orders' topic → done
    inventory reads 'orders' at its own pace
    email reads 'orders' at its own pace
    analytics reads 'orders' at its own pace
    → services are DECOUPLED, failures are isolated
""")
