# ============================================================
# KUBERNETES POC — Web Crawler Scheduler as K8s CronJob
#
# Covers:
#   1. Core K8s objects (Pod, Deployment, Service, CronJob)
#   2. CronJob for Scheduler (runs every minute)
#   3. Deployment for Worker Pool (scales up/down)
#   4. EKS (AWS managed K8s) vs self-hosted
#   5. How to run locally with minikube
#
# Run simulation (no K8s needed):
#   python 06_k8s_poc.py
#
# Run real K8s (requires minikube):
#   minikube start
#   kubectl apply -f k8s/
#   kubectl get pods
# ============================================================

# ── 1. K8s OBJECTS EXPLAINED ──────────────────────────────────────────────────
print("""
╔══════════════════════════════════════════════════════════════╗
║              KUBERNETES OBJECTS                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  POD                                                         ║
║    Smallest unit. 1+ containers sharing network+storage.     ║
║    Ephemeral — if pod dies, it's gone (Deployment restarts)  ║
║    Like: one running instance of your app                    ║
║                                                              ║
║  DEPLOYMENT                                                  ║
║    Manages N replicas of a pod. Self-healing.                ║
║    If pod dies → Deployment creates a new one automatically  ║
║    Rolling update: replace pods one by one (zero downtime)   ║
║    Like: "I want 5 copies of crawler-worker running always"  ║
║                                                              ║
║  SERVICE                                                     ║
║    Stable network address for a set of pods.                 ║
║    Pods come and go (different IPs) — Service IP is stable   ║
║    Types: ClusterIP (internal), NodePort, LoadBalancer       ║
║                                                              ║
║  CRONJOB                                                     ║
║    Runs a pod on a schedule (like Linux cron).               ║
║    "* * * * *" = every minute                                ║
║    Perfect for: Crawler Scheduler, cleanup jobs, reports     ║
║                                                              ║
║  CONFIGMAP / SECRET                                          ║
║    ConfigMap: non-sensitive config (URLs, settings)          ║
║    Secret: sensitive data (DB passwords, API keys)           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# ── 2. WEB CRAWLER K8s ARCHITECTURE ──────────────────────────────────────────
print("""
Web Crawler on Kubernetes:

  ┌─────────────────────────────────────────────────────┐
  │                K8s Cluster                           │
  │                                                      │
  │  CronJob: crawler-scheduler                          │
  │    └── runs every 1 min                              │
  │    └── queries Cassandra for due URLs                │
  │    └── pushes to Kafka topics                        │
  │                                                      │
  │  Deployment: crawler-workers  (replicas: 10)         │
  │    └── Pod 1: Worker (consumes Kafka, crawls URLs)   │
  │    └── Pod 2: Worker                                 │
  │    └── ...                                           │
  │    └── Pod 10: Worker                                │
  │    HPA (auto-scale): if Kafka lag > 1000 → +5 pods  │
  │                                                      │
  │  StatefulSet: cassandra (replicas: 3)                │
  │    └── cassandra-0, cassandra-1, cassandra-2         │
  │    (StatefulSet: stable names + persistent storage)  │
  │                                                      │
  └─────────────────────────────────────────────────────┘
""")

# ── 3. YAML CONFIGS (what you'd apply with kubectl apply -f) ─────────────────
print("=" * 60)
print("K8s YAML CONFIGS")
print("=" * 60)

scheduler_cronjob_yaml = """
# crawler-scheduler-cronjob.yaml
# Runs every minute — queries Cassandra, pushes due URLs to Kafka
apiVersion: batch/v1
kind: CronJob
metadata:
  name: crawler-scheduler
spec:
  schedule: "* * * * *"          # every minute
  concurrencyPolicy: Forbid       # don't start new if previous still running
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scheduler
            image: crawler-scheduler:1.0
            env:
            - name: CASSANDRA_HOST
              value: "cassandra-service"
            - name: KAFKA_BROKER
              value: "kafka-service:9092"
            - name: BATCH_SIZE
              value: "10000"          # URLs to enqueue per run
          restartPolicy: OnFailure
"""

worker_deployment_yaml = """
# crawler-worker-deployment.yaml
# 10 workers always running — auto-scales based on Kafka lag
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crawler-workers
spec:
  replicas: 10
  selector:
    matchLabels:
      app: crawler-worker
  template:
    metadata:
      labels:
        app: crawler-worker
    spec:
      containers:
      - name: worker
        image: crawler-worker:1.0
        resources:
          requests:
            cpu: "500m"       # 0.5 CPU core
            memory: "512Mi"
          limits:
            cpu: "1000m"      # max 1 CPU core
            memory: "1Gi"
        env:
        - name: KAFKA_BROKER
          value: "kafka-service:9092"
        - name: CASSANDRA_HOST
          value: "cassandra-service"
        - name: S3_BUCKET
          value: "crawler-content-bucket"
"""

hpa_yaml = """
# crawler-worker-hpa.yaml (Horizontal Pod Autoscaler)
# Auto-scale workers based on Kafka consumer lag
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: crawler-worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: crawler-workers
  minReplicas: 5
  maxReplicas: 50
  metrics:
  - type: External
    external:
      metric:
        name: kafka_consumer_lag   # custom metric from Prometheus
      target:
        type: AverageValue
        averageValue: "1000"       # scale up if lag > 1000 messages per pod
"""

print("\n--- CronJob (Scheduler) ---")
print(scheduler_cronjob_yaml)
print("--- Deployment (Workers) ---")
print(worker_deployment_yaml)
print("--- HPA (Auto-scale) ---")
print(hpa_yaml)

# ── 4. EKS vs Self-hosted K8s ─────────────────────────────────────────────────
print("""
╔══════════════════════════════════════════════════════════════╗
║         EKS (AWS) vs GKE (Google) vs Self-hosted            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Feature          EKS (AWS)    GKE (Google)   Self-hosted   ║
║  ──────────────────────────────────────────────────────────  ║
║  Control plane    AWS manages  Google manages  You manage    ║
║  Upgrades         AWS handles  Google handles  Manual        ║
║  Cost             $0.10/hr     Free control    Your infra    ║
║                   + EC2 nodes  + GCE nodes     cost          ║
║  Integration      S3,RDS,IAM   GCS,BigQuery    Bring own     ║
║  Best for         AWS shops    GCP shops        on-prem/     ║
║                                                 cost control ║
║                                                              ║
║  For Web Crawler on AWS:                                     ║
║    EKS workers → crawl → store in S3 (same region = fast)   ║
║    IAM roles → no hardcoded credentials                      ║
║    RDS/Aurora → instead of self-hosted Cassandra             ║
║    MSK (managed Kafka) → instead of self-hosted Kafka        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# ── 5. Simulate K8s CronJob behavior ─────────────────────────────────────────
import time
import threading
from datetime import datetime

class SimulatedCassandra:
    """Fake DB with URLs due for crawl."""
    def __init__(self):
        self.urls = [
            {"url": "https://cnn.com/news/1",    "domain_type": "news"},
            {"url": "https://bbc.com/world/2",   "domain_type": "news"},
            {"url": "https://espn.com/scores",   "domain_type": "sports"},
            {"url": "https://python.org/docs",   "domain_type": "static"},
            {"url": "https://cnn.com/tech/3",    "domain_type": "news"},
        ]
        self.index = 0

    def get_due_urls(self, batch_size=3):
        batch = self.urls[self.index:self.index + batch_size]
        self.index = (self.index + batch_size) % len(self.urls)
        return batch


class SimulatedKafka:
    """Fake Kafka — just a list."""
    def __init__(self):
        self.queue = []

    def send(self, topic, message):
        self.queue.append({"topic": topic, "msg": message})

    def consume(self):
        if self.queue:
            return self.queue.pop(0)
        return None


def crawler_scheduler_job(db, kafka, run_number):
    """This is what runs inside the CronJob pod every minute."""
    print(f"\n[CronJob Run #{run_number}] {datetime.now().strftime('%H:%M:%S')}")
    due_urls = db.get_due_urls(batch_size=3)
    topic_map = {"news": "crawler-priority-1", "sports": "crawler-priority-2", "static": "crawler-priority-3"}
    for url_data in due_urls:
        topic = topic_map[url_data["domain_type"]]
        kafka.send(topic, url_data)
        print(f"  → Queued [{url_data['domain_type']:6}] {url_data['url']}")
    print(f"  Queued {len(due_urls)} URLs. Kafka queue size: {len(kafka.queue)}")


def crawler_worker(kafka, worker_id, max_jobs=2):
    """This is what runs in a Worker pod."""
    crawled = 0
    while crawled < max_jobs:
        msg = kafka.consume()
        if msg:
            url = msg["msg"]["url"]
            print(f"  [Worker-{worker_id}] crawling: {url[:45]}")
            time.sleep(0.05)  # simulate fetch time
            crawled += 1
        else:
            time.sleep(0.1)


print("=" * 60)
print("SIMULATION: K8s CronJob + Worker Deployment")
print("=" * 60)

db = SimulatedCassandra()
kafka = SimulatedKafka()

# Simulate 3 CronJob runs (normally 1 per minute)
for run in range(1, 4):
    crawler_scheduler_job(db, kafka, run)

# Simulate 3 workers running in parallel (like a Deployment with replicas=3)
print(f"\n[Workers] Starting 3 workers to process {len(kafka.queue)} queued URLs...")
threads = [threading.Thread(target=crawler_worker, args=(kafka, i, 2)) for i in range(1, 4)]
for t in threads: t.start()
for t in threads: t.join()
print("\n[Done] Simulation complete.")

print("""
─────────────────────────────────────────────────────
To run on REAL K8s (minikube):
  brew install minikube
  minikube start
  kubectl apply -f k8s/crawler-scheduler-cronjob.yaml
  kubectl apply -f k8s/crawler-worker-deployment.yaml
  kubectl get pods --watch
  kubectl logs -l app=crawler-worker
─────────────────────────────────────────────────────
""")
