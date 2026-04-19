# ============================================================
# KAFKA PRIORITY QUEUE — Web Crawler POC
#
# Problem: Kafka is FIFO per partition, NOT a priority queue.
# Solution: Simulate priority using SEPARATE TOPICS per tier.
#
# Pattern: 3 topics, workers poll news first, then sports, then static.
#
# Requires:
#   docker-compose up -d   (from this folder)
#   pip install kafka-python
# ============================================================

# ── HOW TO RUN ────────────────────────────────────────────────────────────────
# Terminal 1:  docker-compose up -d
# Terminal 2:  python 04_priority_queue_poc.py producer
# Terminal 3:  python 04_priority_queue_poc.py consumer
# ─────────────────────────────────────────────────────────────────────────────

import sys
import json
import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

BROKER = 'localhost:9092'

# Three topics — one per priority tier (this IS the priority queue)
TOPIC_NEWS    = 'crawler-priority-1-news'    # highest priority
TOPIC_SPORTS  = 'crawler-priority-2-sports'
TOPIC_STATIC  = 'crawler-priority-3-static'  # lowest priority

ALL_TOPICS = [TOPIC_NEWS, TOPIC_SPORTS, TOPIC_STATIC]

# ── Step 1: Create topics ─────────────────────────────────────────────────────
def create_topics():
    admin = KafkaAdminClient(bootstrap_servers=BROKER)
    topics = [NewTopic(name=t, num_partitions=2, replication_factor=1) for t in ALL_TOPICS]
    try:
        admin.create_topics(topics)
        print("[Admin] Topics created:", ALL_TOPICS)
    except TopicAlreadyExistsError:
        print("[Admin] Topics already exist — OK")
    finally:
        admin.close()

# ── Step 2: Producer — sends URLs to correct priority topic ───────────────────
def run_producer():
    """
    Simulates the Scheduler pushing URLs into Kafka.
    Priority is determined by domain_type → maps to topic.
    """
    create_topics()
    producer = KafkaProducer(
        bootstrap_servers=BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None
    )

    # Sample URLs with different priorities
    urls = [
        {"url": "https://cnn.com/breaking-news",      "domain_type": "news",   "domain": "cnn.com"},
        {"url": "https://bbc.com/world",               "domain_type": "news",   "domain": "bbc.com"},
        {"url": "https://espn.com/scores",             "domain_type": "sports", "domain": "espn.com"},
        {"url": "https://wikipedia.org/wiki/Python",   "domain_type": "static", "domain": "wikipedia.org"},
        {"url": "https://cnn.com/politics",            "domain_type": "news",   "domain": "cnn.com"},
        {"url": "https://nba.com/games",               "domain_type": "sports", "domain": "nba.com"},
        {"url": "https://python.org/docs",             "domain_type": "static", "domain": "python.org"},
        {"url": "https://reuters.com/tech",            "domain_type": "news",   "domain": "reuters.com"},
    ]

    # Map domain_type → Kafka topic
    topic_map = {
        "news":   TOPIC_NEWS,
        "sports": TOPIC_SPORTS,
        "static": TOPIC_STATIC,
    }

    print("\n[Producer] Sending URLs to priority topics...\n")
    for url_data in urls:
        topic = topic_map[url_data["domain_type"]]
        # Use domain as Kafka key → all URLs from same domain go to same partition
        # This ensures politeness: one partition = one domain = sequential crawl
        future = producer.send(topic, key=url_data["domain"], value=url_data)
        future.get(timeout=5)   # wait for ack
        print(f"  → [{url_data['domain_type']:6}] {url_data['url'][:50]}  → topic: {topic}")

    producer.flush()
    producer.close()
    print("\n[Producer] All URLs sent.")

# ── Step 3: Priority Consumer — polls news first, then sports, then static ────
def run_consumer():
    """
    Priority consumer: always drains higher-priority topics first.

    Strategy: poll() with timeout_ms=100 per topic.
    If news topic has messages → process those first.
    If empty → check sports.
    If empty → check static.

    Weighted round-robin to prevent starvation:
      Process 5 news per 2 sports per 1 static
    """
    print("\n[Consumer] Starting priority consumer...\n")

    # Separate consumers per topic (so we can poll each independently)
    def make_consumer(topic):
        return KafkaConsumer(
            topic,
            bootstrap_servers=BROKER,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            group_id='crawler-workers',
            auto_offset_reset='earliest',
            consumer_timeout_ms=200   # don't block if no messages
        )

    news_consumer   = make_consumer(TOPIC_NEWS)
    sports_consumer = make_consumer(TOPIC_SPORTS)
    static_consumer = make_consumer(TOPIC_STATIC)

    # Weighted priority: process ratio 5:2:1
    weights = [
        (news_consumer,   "NEWS  ", 5),
        (sports_consumer, "SPORTS", 2),
        (static_consumer, "STATIC", 1),
    ]

    processed = 0
    max_iterations = 3   # stop after 3 polling rounds

    for iteration in range(max_iterations):
        print(f"\n--- Polling round {iteration + 1} ---")
        any_processed = False

        for consumer, label, quota in weights:
            count = 0
            for msg in consumer:
                url_data = msg.value
                print(f"  [CRAWL {label}] partition={msg.partition} offset={msg.offset} "
                      f"url={url_data['url'][:45]}")
                time.sleep(0.1)   # simulate crawl time
                processed += 1
                count += 1
                any_processed = True

                if count >= quota:
                    break    # respect quota before moving to next priority

        if not any_processed:
            print("  All queues empty.")
            break

    news_consumer.close()
    sports_consumer.close()
    static_consumer.close()
    print(f"\n[Consumer] Done. Total processed: {processed}")

# ── Inline simulation (no Kafka needed) ───────────────────────────────────────
def run_simulation():
    """
    Simulate the priority queue WITHOUT real Kafka.
    Uses Python lists as topic queues.
    Shows the concept clearly.
    """
    print("=" * 60)
    print("PRIORITY QUEUE SIMULATION (no Kafka needed)")
    print("=" * 60)

    # Three "topics" (lists simulate Kafka topics)
    queues = {
        "news":   [],
        "sports": [],
        "static": [],
    }

    # Producer: enqueue URLs
    urls = [
        ("https://wikipedia.org/history",   "static"),
        ("https://cnn.com/breaking",        "news"),
        ("https://espn.com/scores",         "sports"),
        ("https://python.org/docs",         "static"),
        ("https://bbc.com/world",           "news"),
        ("https://nba.com/games",           "sports"),
        ("https://reuters.com/tech",        "news"),
    ]

    print("\n[Producer] Enqueuing URLs...")
    for url, priority in urls:
        queues[priority].append(url)
        print(f"  → [{priority:6}] {url}")

    print(f"\n  Queue sizes: news={len(queues['news'])} "
          f"sports={len(queues['sports'])} static={len(queues['static'])}")

    # Consumer: drain news first, then sports, then static
    # Weighted: 3 news per 1 sports per 1 static (prevent starvation)
    print("\n[Consumer] Processing with priority (news first)...")
    order = [("news", 3), ("sports", 1), ("static", 1)]

    step = 0
    while any(queues.values()):
        for topic, quota in order:
            for _ in range(quota):
                if queues[topic]:
                    url = queues[topic].pop(0)
                    step += 1
                    print(f"  Step {step}: [{topic:6}] {url}")

    print(f"\nTotal processed: {step}")
    print("\nObserve: ALL news processed before sports/static!")
    print("Within news: FIFO order (first added, first processed) — Kafka's guarantee")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "simulation"

    if mode == "producer":
        run_producer()
    elif mode == "consumer":
        run_consumer()
    else:
        # Default: run simulation without Kafka
        run_simulation()
        print("""
─────────────────────────────────────────────────────
To run with REAL Kafka:
  docker-compose up -d
  pip install kafka-python
  python 04_priority_queue_poc.py producer
  python 04_priority_queue_poc.py consumer   (separate terminal)
─────────────────────────────────────────────────────
""")
