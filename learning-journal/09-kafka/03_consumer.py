import warnings
warnings.filterwarnings("ignore")

# ============================================================
# KAFKA CONSUMER
#
# Reads messages from a Kafka topic.
# Run this IN A SEPARATE TERMINAL while producer is running.
#
# BEFORE RUNNING:
#   Terminal 1: docker-compose up -d
#   Terminal 2: python3 03_consumer.py   ← this file
#   Terminal 3: python3 02_producer.py   ← send messages
#
# PRINT ORDER:
#   STEP 1 — Connect and read existing messages
#   STEP 2 — Consumer groups (two consumers, same topic)
#   STEP 3 — Offset control (read from beginning vs latest)
# ============================================================

import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_SERVER = "localhost:9092"
TOPIC        = "orders"

# ============================================================
# STEP 1: Read messages from topic
# ============================================================
print("\n" + "="*50)
print("STEP 1: Read from topic 'orders'")
print("="*50)

try:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVER,

        # deserialize bytes → Python dict
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),

        # consumer group — Kafka tracks offset per group
        group_id="inventory-service",

        # where to start if this group has never read before
        # "earliest" = from the very first message ever
        # "latest"   = only new messages from now on
        auto_offset_reset="earliest",

        # commit offset automatically after reading
        enable_auto_commit=True,

        # stop after 3 seconds of no new messages (for demo)
        consumer_timeout_ms=3000,
    )

    print(f"✅ Consumer connected | group=inventory-service")
    print(f"   Waiting for messages from '{TOPIC}'...\n")

    count = 0
    for message in consumer:
        count += 1
        print(f"  [{count}] partition={message.partition} offset={message.offset}")
        print(f"       key  : {message.key}")
        print(f"       value: {message.value}")
        print()

    print(f"✅ Read {count} messages total.")
    consumer.close()

except NoBrokersAvailable:
    print("❌ Kafka not running! Start: docker-compose up -d")
    exit(1)

input("\nPress Enter for STEP 2...\n")


# ============================================================
# STEP 2: Consumer Groups
#
# Two different services read the SAME topic independently.
# "inventory-service" and "analytics-service" both get ALL messages.
# Kafka tracks their offsets separately.
# ============================================================
print("="*50)
print("STEP 2: Consumer Groups")
print("="*50)

print("""
  Kafka topic 'orders':
    message 1: ORD-001
    message 2: ORD-002
    message 3: ORD-003

  inventory-service (group A):
    reads ORD-001, ORD-002, ORD-003
    offset committed: 3

  analytics-service (group B):
    reads ORD-001, ORD-002, ORD-003   ← same messages!
    offset committed: 3

  Each group has its OWN offset pointer.
  Reading by one group does NOT affect the other.
  This is unlike a regular queue where one reader "consumes" the message.
""")

# Simulate analytics-service reading the same topic
try:
    consumer2 = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="analytics-service",       # ← different group!
        auto_offset_reset="earliest",       # starts from beginning again
        consumer_timeout_ms=3000,
    )

    print("analytics-service reading:")
    count = 0
    for message in consumer2:
        count += 1
        val = message.value
        order_id = val.get("order_id", "?")
        amount   = val.get("amount", "?")
        print(f"  [analytics] offset={message.offset} | {order_id} | ₹{amount}")

    print(f"\n✅ analytics-service read {count} messages")
    print("   (same messages inventory-service already read)")
    consumer2.close()

except Exception as e:
    print(f"Error: {e}")

input("\nPress Enter for STEP 3...\n")


# ============================================================
# STEP 3: Offset control
#
# "earliest" → read from message 0 (replay all history)
# "latest"   → read only NEW messages from now on
#
# Use case:
#   New service joins → "earliest" to process all past orders
#   Live dashboard    → "latest" to show real-time only
# ============================================================
print("="*50)
print("STEP 3: Offset control")
print("="*50)

print("""
  auto_offset_reset options:
  ──────────────────────────
  "earliest"  → start from message 0
                use when: new service needs to catch up on history

  "latest"    → start from NOW, skip old messages
                use when: real-time dashboard, live alerts

  Manual offset:
    consumer.seek(partition, offset=5)  → start from message 5 exactly
    use when: replaying from a specific point after a bug fix
""")

# Show reading from a specific offset
try:
    from kafka import TopicPartition

    consumer3 = KafkaConsumer(
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="debug-service",
        consumer_timeout_ms=2000,
    )

    # manually assign partition and seek to offset 0
    tp = TopicPartition(TOPIC, 0)       # topic, partition 0
    consumer3.assign([tp])
    consumer3.seek(tp, 0)               # start from offset 0

    print("Reading partition 0 from offset 0:")
    for i, msg in enumerate(consumer3):
        print(f"  offset={msg.offset} | {msg.value}")
        if i >= 2:                      # show first 3
            break

    consumer3.close()

except Exception as e:
    print(f"(Needs messages in topic: {e})")

print("""
✅ KEY TAKEAWAYS:
  Producer  → sends to topic (fire and forget)
  Consumer  → reads from topic (at its own pace)
  Group ID  → multiple services read same topic independently
  Offset    → tracks where each group left off
  earliest  → replay history
  latest    → real-time only
""")
