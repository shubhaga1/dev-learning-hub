import warnings
warnings.filterwarnings("ignore")

# ============================================================
# KAFKA PRODUCER
#
# Sends messages to a Kafka topic.
#
# BEFORE RUNNING:
#   cd learning-journal/09-kafka
#   docker-compose up -d
#   pip install kafka-python
#
# PRINT ORDER:
#   STEP 1 — Connect to Kafka
#   STEP 2 — Send a single message
#   STEP 3 — Send multiple messages (batch)
#   STEP 4 — Send with a key (controls which partition)
# ============================================================

import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_SERVER = "localhost:9092"
TOPIC        = "orders"

# ============================================================
# STEP 1: Connect to Kafka broker
# ============================================================
print("\n" + "="*50)
print("STEP 1: Connect to Kafka")
print("="*50)

try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,

        # serialize Python dict → JSON bytes before sending
        # Kafka only sends bytes — not Python objects
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),

        # serialize key → bytes (used for partitioning)
        key_serializer=lambda k: k.encode("utf-8") if k else None,
    )
    print(f"✅ Connected to Kafka at {KAFKA_SERVER}")
    print(f"   Topic: {TOPIC}")

except NoBrokersAvailable:
    print("❌ Kafka not running!")
    print("   Start it: docker-compose up -d")
    exit(1)

input("\nPress Enter for STEP 2...\n")


# ============================================================
# STEP 2: Send a single message
# ============================================================
print("="*50)
print("STEP 2: Send a single message")
print("="*50)

order = {
    "order_id": "ORD-001",
    "customer": "Shubham",
    "item":     "MacBook Pro",
    "amount":   150000,
    "status":   "placed",
}

# send() is async by default — message goes to internal buffer
future = producer.send(TOPIC, value=order)

# flush() forces the buffer to actually send now
producer.flush()

# get() blocks until broker confirms receipt
metadata = future.get(timeout=10)

print(f"✅ Message sent!")
print(f"   Topic:     {metadata.topic}")
print(f"   Partition: {metadata.partition}")   # which partition it landed on
print(f"   Offset:    {metadata.offset}")      # position in that partition

input("\nPress Enter for STEP 3...\n")


# ============================================================
# STEP 3: Send multiple messages (simulate order stream)
# ============================================================
print("="*50)
print("STEP 3: Send multiple messages")
print("="*50)

orders = [
    {"order_id": "ORD-002", "customer": "Rahul",  "item": "iPhone",   "amount": 80000},
    {"order_id": "ORD-003", "customer": "Priya",  "item": "AirPods",  "amount": 15000},
    {"order_id": "ORD-004", "customer": "Amit",   "item": "iPad",     "amount": 60000},
    {"order_id": "ORD-005", "customer": "Deepak", "item": "Apple Watch", "amount": 45000},
]

for order in orders:
    producer.send(TOPIC, value=order)
    print(f"  → Sent: {order['order_id']} | {order['customer']} | ₹{order['amount']}")
    time.sleep(0.5)   # simulate orders arriving over time

producer.flush()
print(f"\n✅ {len(orders)} messages sent to topic '{TOPIC}'")

input("\nPress Enter for STEP 4...\n")


# ============================================================
# STEP 4: Send with a KEY
#
# Key controls which PARTITION a message goes to.
# Messages with the SAME key → SAME partition → SAME ORDER.
#
# Use case: all events for customer "Shubham" go to partition 0
#           → consumer reads them in order
# ============================================================
print("="*50)
print("STEP 4: Send with key (partition control)")
print("="*50)

keyed_messages = [
    ("customer_1", {"order_id": "ORD-006", "event": "placed"}),
    ("customer_2", {"order_id": "ORD-007", "event": "placed"}),
    ("customer_1", {"order_id": "ORD-006", "event": "paid"}),     # same key → same partition
    ("customer_1", {"order_id": "ORD-006", "event": "shipped"}),  # same key → same partition
    ("customer_2", {"order_id": "ORD-007", "event": "paid"}),
]

for key, msg in keyed_messages:
    future   = producer.send(TOPIC, key=key, value=msg)
    metadata = future.get(timeout=10)
    print(f"  key={key:<12} msg={msg['event']:<10} → partition={metadata.partition}")

producer.flush()

print("""
✅ Notice: same key always goes to same partition.
   customer_1 events are ordered: placed → paid → shipped
   Even if sent at different times.
""")

producer.close()
print("Producer closed.")
