# REVISION LOG — Spaced Repetition Tracker

## How to use this file

Every time you learn something NEW — add a row.
Revision schedule: review on Day+1, Day+3, Day+7 from the learn date.

Status codes:
  ✅ = confident, can explain from scratch without notes
  🟡 = remember it but need to check details
  ❌ = forgot, need to re-learn

---

## SYSTEM DESIGN

| Topic | Learned | Rev D+1 | Rev D+3 | Rev D+7 | Status | Notes |
|-------|---------|---------|---------|---------|--------|-------|
| Web Crawler — components + flow | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | Bloom filter, Cassandra, Kafka topics |
| Web Crawler — capacity calc | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | 100TB not 10PB. 160MB/s bandwidth |
| Cassandra vs MySQL vs Redis | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | Partition key = domain, no master |
| Kafka priority queue pattern | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | 3 topics, weighted polling |
| K8s CronJob + Deployment + HPA | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | CronJob=scheduler, HPA=autoscale |
| DNS cache TTL = 5 min | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | IPs rotate (CDN), 50ms saving |
| DEK/KEK pattern | 2026-04-11 | 2026-04-12 | 2026-04-14 | 2026-04-18 | 🟡 | DEK=data key, KEK=wraps DEK, rotation=re-wrap DEKs only |

---

## ENCRYPTION

| Topic | Learned | Rev D+1 | Rev D+3 | Rev D+7 | Status | Notes |
|-------|---------|---------|---------|---------|--------|-------|
| Symmetric AES — Fernet vs AES-GCM | 2026-04-11 | 2026-04-12 | 2026-04-14 | 2026-04-18 | 🟡 | Fernet=AES128+HMAC, GCM=prod |
| RSA — why asymmetric, math | 2026-04-11 | 2026-04-12 | 2026-04-14 | 2026-04-18 | 🟡 | n=p×q, factoring hard, OAEP padding |
| HTTPS TLS 1.2 handshake | 2026-04-11 | 2026-04-12 | 2026-04-14 | 2026-04-18 | 🟡 | RSA for key exchange, AES for data |
| RSA vs ECC | 2026-04-11 | 2026-04-12 | 2026-04-14 | 2026-04-18 | 🟡 | ECC-256=RSA-3072, ECDHE=forward secrecy |

---

## DSA — QUEUE

| Topic | Learned | Rev D+1 | Rev D+3 | Rev D+7 | Status | Notes |
|-------|---------|---------|---------|---------|--------|-------|
| Queue API — offer/poll/peek | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | ArrayDeque not LinkedList |
| BFS level order | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | snapshot size before processing level |
| PriorityQueue — min/max heap | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | reverseOrder for max, comparator for custom |
| Kth Largest — min heap size k | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | poll when size>k, peek=answer |
| Top K Frequent | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | freq map + min heap by freq |
| Merge K sorted lists | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | min heap, poll+push next |
| Sliding Window Maximum — Deque | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | monotonic decreasing, store indices |
| Rotting Oranges — multi-source BFS | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | seed ALL rotten at t=0 |
| Meeting Rooms II | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | sort by start, min heap of end times |

---

## SQL

| Topic | Learned | Rev D+1 | Rev D+3 | Rev D+7 | Status | Notes |
|-------|---------|---------|---------|---------|--------|-------|
| DDL/DML/DQL | 2026-04-08 | done | done | 2026-04-15 | 🟡 | CREATE/INSERT/SELECT |
| WHERE vs HAVING | 2026-04-08 | done | done | 2026-04-15 | 🟡 | WHERE=before group, HAVING=after |
| PIVOT — CASE WHEN | 2026-04-09 | done | 2026-04-12 | 2026-04-16 | 🟡 | rows→columns with SUM(CASE WHEN) |
| NULL vs empty string | 2026-04-09 | done | 2026-04-12 | 2026-04-16 | 🟡 | IS NULL not = NULL |
| Constraints | 2026-04-09 | done | 2026-04-12 | 2026-04-16 | 🟡 | PK, NOT NULL, UNIQUE, CHECK, DEFAULT, FK |

---

## KAFKA

| Topic | Learned | Rev D+1 | Rev D+3 | Rev D+7 | Status | Notes |
|-------|---------|---------|---------|---------|--------|-------|
| Core concepts — topic/partition/offset | 2026-04-10 | done | done | 2026-04-17 | 🟡 | offset = position, group = parallel readers |
| KRaft vs Zookeeper | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | KRaft=no ZK, Kafka 3.3+, simpler |
| Kafka vs RabbitMQ vs Pulsar | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | Kafka=stream/replay, RabbitMQ=task queue |

---

## PYTHON / VENV

| Topic | Learned | Rev D+1 | Rev D+3 | Rev D+7 | Status | Notes |
|-------|---------|---------|---------|---------|--------|-------|
| venv — create/activate/site-packages | 2026-04-12 | 2026-04-13 | 2026-04-15 | 2026-04-19 | 🟡 | source activate prepends PATH |
| Fernet vs AES-256-GCM | 2026-04-11 | done | 2026-04-14 | 2026-04-18 | 🟡 | Fernet=easy, GCM=production |

---

## HOW TO REVISE

### Daily (10 min before coding)
```
Open this file.
Find rows where Rev D+1 = today.
For each:
  1. Close notes. Try to explain the concept aloud (30 sec).
  2. Write the key insight on paper.
  3. Check your code file. Did you get it right?
  4. Update status: ✅ 🟡 ❌
  5. If ❌ → re-read the file, code 5 lines of it by hand.
```

### Weekly (Sunday, 30 min)
```
Scan all ❌ rows → schedule them again (reset Rev D+1 to today).
Scan all 🟡 rows older than 2 weeks → demote to re-revise.
Any ✅ older than 1 month → quick 30-sec recall check.
```

### Pattern for Interview Prep
```
Monday:    SQL + System Design concept
Tuesday:   DSA — 2 problems (1 easy, 1 medium)
Wednesday: DSA — 2 problems (1 medium, 1 hard)
Thursday:  System Design deep dive (one full HLD+LLD)
Friday:    Kafka/K8s/Infra concept
Saturday:  Full mock interview (45 min timed)
Sunday:    Revision day — update this file
```
