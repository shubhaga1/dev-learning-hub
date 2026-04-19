# ============================================================
# KAFKA ALTERNATIVES — KRaft, RabbitMQ, Pulsar, Redis Streams
#
# Covers:
#   1. Kafka KRaft mode (no Zookeeper — modern Kafka)
#   2. RabbitMQ vs Kafka
#   3. Apache Pulsar vs Kafka
#   4. Redis Streams vs Kafka
#   5. When to use which
#   6. Simulation of each pattern
#
# Run: python 05_kafka_alternatives.py
# ============================================================

# ── 1. KAFKA KRAFT MODE — No Zookeeper ───────────────────────────────────────
print("""
╔══════════════════════════════════════════════════════════════╗
║           KAFKA KRaft MODE (Kafka 3.3+)                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Old Kafka (with Zookeeper):                                 ║
║    Kafka brokers + Zookeeper cluster (separate!)             ║
║    Zookeeper: tracks leaders, brokers, partition metadata    ║
║    Problem:                                                  ║
║      - TWO systems to manage (Kafka + Zookeeper)             ║
║      - Zookeeper = single point of failure                   ║
║      - Max ~200K partitions (Zookeeper limit)                ║
║      - Slower metadata updates                               ║
║                                                              ║
║  New Kafka with KRaft (Kafka Raft = internal consensus):     ║
║    Kafka manages its own metadata (no Zookeeper needed!)     ║
║    Raft consensus built into Kafka itself                    ║
║    Benefits:                                                 ║
║      - ONE system to manage                                  ║
║      - 10x more partitions (millions)                        ║
║      - Faster startup, faster failover                       ║
║      - Simpler docker-compose (no zookeeper container)       ║
║                                                              ║
║  Status: KRaft is production-ready since Kafka 3.3 (2022)   ║
║  Migration: Kafka 4.0 drops Zookeeper support entirely       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# KRaft docker-compose (no zookeeper!)
kraft_docker_compose = """
# docker-compose-kraft.yml — Kafka with KRaft (no Zookeeper)
version: '3.8'
services:
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    hostname: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: 'broker,controller'   # single node = both roles
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka:9093'
      KAFKA_LISTENERS: 'PLAINTEXT://kafka:29092,CONTROLLER://kafka:9093,EXTERNAL://0.0.0.0:9092'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka:29092,EXTERNAL://localhost:9092'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT'
      KAFKA_CONTROLLER_LISTENER_NAMES: 'CONTROLLER'
      KAFKA_INTER_BROKER_LISTENER_NAME: 'PLAINTEXT'
      CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qg=='   # fixed UUID for KRaft
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'

# Compare with OLD docker-compose (with zookeeper) — needs 2 services:
# services:
#   zookeeper:
#     image: confluentinc/cp-zookeeper:7.5.0
#     ...
#   kafka:
#     image: confluentinc/cp-kafka:7.5.0
#     depends_on: [zookeeper]
#     environment:
#       KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
#       ...
"""
print("KRaft docker-compose:")
print(kraft_docker_compose)

# ── 2. COMPARISON: Kafka vs RabbitMQ vs Pulsar vs Redis Streams ──────────────
print("""
╔══════════════════════════════════════════════════════════════════════════╗
║         MESSAGE QUEUE COMPARISON                                         ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Feature          Kafka         RabbitMQ      Pulsar        Redis Stream ║
║  ────────────────────────────────────────────────────────────────────    ║
║  Model            Log-based     Queue-based   Log-based     Log-based    ║
║  Message retain   Forever*      Until ack'd   Forever*      Configurable ║
║  Replay msgs      YES ✅        NO ❌         YES ✅        YES ✅       ║
║  Throughput       Very High     Medium        Very High     High         ║
║                   (millions/s)  (50K/s)       (millions/s)  (100K/s)    ║
║  Latency          Low (ms)      Very Low(µs)  Low (ms)      Very Low(µs) ║
║  Priority queue   NO ❌         YES ✅        YES ✅        YES (ZADD)   ║
║  Push to consumer NO (pull)     YES (push)    Both          Both         ║
║  Multi-consumer   Yes (groups)  Yes (binding) Yes (subscr.) Yes          ║
║  Ordering         Per partition Global+       Per topic     Per stream   ║
║  Setup complexity Medium        Easy          Hard          Easy         ║
║  Best for         Stream        Task queue    Multi-tenant  Simple cache ║
║                   processing    job dispatch  cloud-native  + queue      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

* = until retention period (default 7 days, configurable to forever)
""")

# ── 3. WHEN TO USE WHICH ──────────────────────────────────────────────────────
print("""
WHEN TO USE WHICH:

  Kafka:
    ✅ Event streaming (user clicks, logs, metrics)
    ✅ Audit trail (need to replay history)
    ✅ Multiple consumers reading same stream independently
    ✅ High throughput (millions of events/sec)
    ✅ Exactly-once processing (Kafka Streams, Flink)
    Example: web crawler URL queue, payment events, CDC (change data capture)

  RabbitMQ:
    ✅ Task queues (each message processed by ONE consumer)
    ✅ Need true priority queue (built-in x-max-priority)
    ✅ Complex routing (fanout, topic, direct exchange)
    ✅ Need push-based delivery (lower latency)
    Example: email jobs, image resize jobs, order processing

  Apache Pulsar:
    ✅ Multi-tenant (many teams, isolated namespaces)
    ✅ Geo-replication (data in multiple regions natively)
    ✅ Need both queue (exclusive) and stream (shared) mode
    ✅ Cloud-native from ground up
    Example: Splunk, Tencent WeChat, Yahoo

  Redis Streams:
    ✅ Already using Redis (don't want another system)
    ✅ Simple pub/sub or task queue
    ✅ Low latency is critical
    ✅ Short retention (don't need long history)
    Example: real-time notifications, session events, leaderboard updates
""")

# ── 4. SIMULATION: RabbitMQ-style priority queue ──────────────────────────────
import heapq
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

print("=" * 60)
print("SIMULATION: RabbitMQ-style Priority Queue")
print("=" * 60)

@dataclass(order=True)
class Message:
    priority: int        # lower number = higher priority
    payload: Any = field(compare=False)

class RabbitMQStyleQueue:
    """
    Simulates RabbitMQ's x-max-priority queue.
    Unlike Kafka (FIFO), this is a true priority queue.
    Higher priority messages processed first regardless of arrival order.
    """
    def __init__(self, max_priority: int = 10):
        self._heap = []
        self.max_priority = max_priority

    def publish(self, message: str, priority: int = 5):
        """priority: 0 (highest) to max_priority (lowest)"""
        heapq.heappush(self._heap, Message(priority=priority, payload=message))
        print(f"  [Published] priority={priority} msg='{message}'")

    def consume(self):
        if self._heap:
            msg = heapq.heappop(self._heap)
            return msg.priority, msg.payload
        return None

print("\n[RabbitMQ Priority Queue] Publishing messages in random order...")
q = RabbitMQStyleQueue()
q.publish("Process static page backup",    priority=8)  # low priority
q.publish("Breaking news: earthquake",     priority=1)  # highest priority
q.publish("Weekly analytics report",       priority=9)  # lowest
q.publish("Sports score update",           priority=4)  # medium
q.publish("Payment fraud alert",           priority=0)  # critical!
q.publish("User signup email",             priority=5)
q.publish("CNN live blog update",          priority=2)

print("\n[Consumer] Processing in PRIORITY order (not arrival order):")
step = 1
while True:
    result = q.consume()
    if not result: break
    priority, msg = result
    print(f"  Step {step}: priority={priority} → '{msg}'")
    step += 1

# ── 5. Redis Streams simulation ───────────────────────────────────────────────
print("\n" + "=" * 60)
print("SIMULATION: Redis Streams (XADD / XREAD pattern)")
print("=" * 60)

class RedisStreamSimulator:
    """
    Simulates Redis XADD / XREAD commands.
    XADD: append to stream (like Kafka produce)
    XREAD: read from offset (like Kafka consume with offset)
    XGROUP: consumer groups (like Kafka consumer groups)
    """
    def __init__(self):
        self.streams = defaultdict(list)
        self.consumer_offsets = defaultdict(int)  # group → last offset

    def xadd(self, stream: str, message: dict):
        offset = len(self.streams[stream])
        entry = {"id": f"1000-{offset}", "data": message}
        self.streams[stream].append(entry)
        print(f"  XADD {stream} → id={entry['id']} data={message}")
        return entry["id"]

    def xread(self, stream: str, group: str, count: int = 2):
        """Read up to 'count' unread messages for this consumer group."""
        offset = self.consumer_offsets[f"{stream}:{group}"]
        messages = self.streams[stream][offset:offset + count]
        self.consumer_offsets[f"{stream}:{group}"] += len(messages)
        return messages

    def xlen(self, stream: str):
        return len(self.streams[stream])


redis = RedisStreamSimulator()

print("\n[Producer] XADD to 'crawler-events' stream:")
redis.xadd("crawler-events", {"url": "https://cnn.com/1",     "type": "news"})
redis.xadd("crawler-events", {"url": "https://bbc.com/2",     "type": "news"})
redis.xadd("crawler-events", {"url": "https://espn.com/3",    "type": "sports"})
redis.xadd("crawler-events", {"url": "https://python.org/4",  "type": "static"})
redis.xadd("crawler-events", {"url": "https://reuters.com/5", "type": "news"})

print(f"\nStream length: {redis.xlen('crawler-events')}")

print("\n[Consumer Group A - analytics] XREAD (count=3):")
msgs = redis.xread("crawler-events", "analytics", count=3)
for m in msgs: print(f"  {m['id']} → {m['data']['url']}")

print("\n[Consumer Group B - indexer] XREAD (count=3) — independent offset:")
msgs = redis.xread("crawler-events", "indexer", count=3)
for m in msgs: print(f"  {m['id']} → {m['data']['url']}")

print("\n[Consumer Group A - analytics] XREAD again (gets next 2):")
msgs = redis.xread("crawler-events", "analytics", count=3)
for m in msgs: print(f"  {m['id']} → {m['data']['url']}")

print("""
KEY INSIGHT:
  Both consumer groups (analytics, indexer) read SAME stream independently.
  This is exactly like Kafka consumer groups.
  Redis Streams ≈ Kafka but simpler, lower throughput, already in Redis.
""")
