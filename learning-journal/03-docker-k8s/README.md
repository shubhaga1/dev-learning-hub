# 03 — Docker & Kubernetes

## Run order
```bash
python 01_traditional.py           # no isolation — runs directly on OS
python 02_hypervisor_simulated.py  # VM simulation with logs
python 03_hypervisor_real_code.py  # real VM creation (VirtualBox + AWS)
python 04_docker.py                # containers
python 05_kubernetes.py            # orchestration concepts
python 06_k8s_poc.py               # CronJob + Deployment + HPA POC
```

---

## Evolution of app deployment

```
2000s: Traditional → app runs directly on OS (breaks on other machines)
2005s: Hypervisor  → VMs isolate apps (heavy, slow to start)
2013:  Docker      → containers isolate apps (lightweight, fast)
2014:  Kubernetes  → manages hundreds of containers automatically
```

---

## VM vs Docker

| | VM | Docker |
|--|--|--|
| Startup | 2–3 min | 2–3 sec |
| RAM | 1–2 GB | 50–200 MB |
| Isolation | Full OS | Process-level |
| Runs different OS | ✅ | ❌ |

### Hypervisor types
```
Type 1 (Bare Metal):  Hardware → Hypervisor → VMs   (AWS, Azure)
Type 2 (Hosted):      Hardware → OS → VirtualBox → VMs   (local dev)
```

---

## Kubernetes — Mental Model

> K8s is a "brain" that constantly decides **where containers run, how many run, and what happens when they fail**.

### K8s = 4 layers

| Layer | What it is |
| ----- | ---------- |
| Control Plane | The brain — API Server, Scheduler, Controller |
| Nodes | Worker machines — run the containers |
| Pods | Smallest unit — one running instance of your app |
| YAML | Intent file — declare what you want, K8s figures out how |

### Declarative system — the key idea

You don't say "run this container." You say "I want 3 replicas of this app running."
K8s watches reality and continuously corrects it to match your intent.

```
You declare YAML → "I want 3 replicas"
K8s sees 2 running  → starts 1 more automatically
Pod crashes         → K8s starts replacement immediately
Node dies           → K8s reschedules pods to surviving nodes
```

---

## Core Objects

### Pod

Smallest unit. Usually 1 container. **Ephemeral** — if it dies, it's gone.
A Deployment is what restarts it.

### Deployment

Manages pods. Ensures the right number of replicas always exist.
```yaml
replicas: 3        # always keep 3 copies running
image: my-app:v2   # rolling update — replaces pods one at a time, no downtime
```

### Service

Gives stable networking to pods. Pods die and get new IPs — Service DNS stays constant.
```
Without Service:  pod IP changes on every restart → other services break
With Service:     stable DNS name → always reachable regardless of pod churn
```

### ConfigMap / Secret

External config — keeps settings separate from the container image.
```
ConfigMap → non-sensitive config (URLs, feature flags, timeouts)
Secret    → sensitive config (passwords, API keys) — base64 encoded, encrypted at rest
```

### Namespace

Logical grouping — like folders inside a cluster.
```
prod/     → production workloads
staging/  → pre-prod testing
dev/      → developer sandboxes
monitoring/ → observability tools
```

### CronJob

Runs a pod on a schedule. Kubernetes equivalent of Unix cron.
```yaml
schedule: "* * * * *"     # every minute
# format:  min hour day month weekday
schedule: "0 2 * * *"     # every day at 2am
```

---

## Autoscaling — HPA (Horizontal Pod Autoscaler)

K8s can automatically add or remove pods based on load.

```
Low traffic:   2 pods
Traffic spike: K8s scales to 20 pods automatically
Traffic drops: K8s scales back to 2 pods
```

```yaml
minReplicas: 2
maxReplicas: 50
targetCPUUtilizationPercentage: 70   # scale up when avg CPU > 70%
```

### What HPA creates: dynamic cost

Cost becomes unpredictable without visibility tools.
```
Normal day:    5 pods  × $0.02/hr × 24hr = $2.40/day
Traffic spike: 50 pods × $0.02/hr × 24hr = $24/day
```
You need CloudSpend or Kubecost alongside K8s to track this.

### Custom metric scaling (advanced)

Scale on anything — not just CPU. Example: Kafka consumer lag.
```
Kafka queue grows deep → scale up consumer pods to drain faster
Queue empty           → scale down to save cost
```
This is how the Web Crawler worker pool works in `06_k8s_poc.py`.

---

## Ephemeral Pods — why it matters

Pods are temporary by design. They die from node failure, OOM kill, or deployment updates.

```
Problem 1 — Logs:  pod dies → logs gone → need centralized logging (ELK, CloudWatch)
Problem 2 — State: never store data inside a pod → use PersistentVolume or external DB
Problem 3 — Cost:  short-lived pods make cost attribution per workload hard to track
```

---

## Helm — Kubernetes Package Manager

Like `npm` for Node or `pip` for Python — but for Kubernetes YAML.

### Problem without Helm

Each microservice needs its own set of YAML files:
```
deployment.yaml   service.yaml   configmap.yaml   hpa.yaml   ingress.yaml
```
100 microservices = 500 YAML files to manage, copy-paste, keep in sync.

### With Helm

```bash
helm install my-app ./chart             # deploy everything in one command
helm upgrade my-app ./chart             # push new version
helm rollback my-app 1                  # roll back to previous release
helm uninstall my-app                   # remove everything cleanly
helm list                               # see all installed releases
```

### Chart structure
```
chart/
 ├── Chart.yaml        # name, version, description
 ├── values.yaml       # default config values
 └── templates/        # YAML with {{ .Values.xxx }} placeholders
     ├── deployment.yaml
     ├── service.yaml
     └── hpa.yaml
```

### values.yaml drives everything
```yaml
# values.yaml
replicaCount: 3
image: my-app:v2
autoscaling:
  enabled: true
  maxReplicas: 50
```

Different values per environment — same chart:
```bash
helm install my-app ./chart -f values-prod.yaml    # prod: 50 replicas max
helm install my-app ./chart -f values-dev.yaml     # dev: 2 replicas max
```

---

## Observability — 3 Pillars

| Pillar | Question | Tool |
| ------ | -------- | ---- |
| Metrics | What is happening right now? | Prometheus, Site24x7 |
| Logs | Why did it happen? | ELK (Elasticsearch + Kibana), CloudWatch |
| Traces | Where in the request path did it slow down? | Jaeger, AWS X-Ray |

### Why link performance + cost

```
Without linking:
  Cost spike → no idea why

With integration (Site24x7 + CloudSpend):
  CPU spike on checkout service
  → HPA fired, added 10 pods
  → cost jumped $50/hr
  → all traced back to one root cause
```

---

## How everything connects

```
         Helm (installs and manages YAML)
                      ↓
           Kubernetes (runs and self-heals)
          ↙            ↓             ↘
       Pods         CronJobs       Services
      (apps)      (schedulers)   (networking)
          ↘            ↓             ↙
           HPA (scales pods on load)
                      ↓
        Observability: Metrics + Logs + Traces
                      ↓
         Cost visibility (CloudSpend, Kubecost)
```

---

## Hands-on learning path (run in order)

K8s "clicks" when you watch pods die and restart live.

```bash
# 1. Start local cluster
minikube start

# 2. Deploy an app
kubectl create deployment nginx --image=nginx

# 3. Expose it
kubectl expose deployment nginx --port=80 --type=NodePort

# 4. See what's running
kubectl get pods
kubectl get services

# 5. Scale it up
kubectl scale deployment nginx --replicas=5
kubectl get pods         # watch 5 pods appear

# 6. Kill a pod — K8s restarts it immediately
kubectl delete pod <pod-name>
kubectl get pods -w      # -w = watch live — you'll see a new pod start within seconds

# 7. Rolling update — no downtime
kubectl set image deployment/nginx nginx=nginx:alpine
kubectl rollout status deployment/nginx    # watch old pods swap out one by one

# 8. Roll back
kubectl rollout undo deployment/nginx

# 9. Check logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous    # logs from a crashed pod

# 10. Clean up
kubectl delete deployment nginx
kubectl delete service nginx
minikube stop
```

---

## Key commands reference

```bash
# Cluster
kubectl cluster-info
kubectl get nodes

# Pods
kubectl get pods -n <namespace>
kubectl get pods --all-namespaces
kubectl describe pod <pod-name>          # full details — events, resource usage
kubectl exec -it <pod-name> -- /bin/sh  # shell into a running pod

# Deployments
kubectl get deployments
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>

# Apply / delete
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml

# Namespace
kubectl get pods -n prod
kubectl config set-context --current --namespace=prod   # change default namespace

# Helm
helm list                    # all installed releases
helm status my-app           # current state of a release
helm get values my-app       # what values are active
helm history my-app          # version history
```

---

## Interview questions

**Q: What is the difference between a Pod and a Deployment?**
Pod = one running instance. Deployment = manager — ensures N replicas exist, handles rolling updates, restarts crashed pods automatically.

**Q: What happens when a pod crashes?**
The Deployment controller detects replica count dropped below desired. It schedules a new pod immediately on an available node. This is K8s self-healing.

**Q: How does HPA know when to scale?**
It polls the Metrics Server every 15 seconds. When average CPU (or custom metric like Kafka lag) exceeds the threshold, it increases `replicas` in the Deployment — which triggers new pod creation.

**Q: What is the difference between ConfigMap and Secret?**
Both inject config into pods. Secret is base64-encoded and can be encrypted at rest using KMS. ConfigMap is plain text. Use Secret for passwords, tokens, and API keys.

**Q: Why use Helm instead of raw YAML?**
Raw YAML is not reusable across environments. Helm adds templating (values.yaml), versioning, and rollback at the release level — one chart, different values per env.

**Q: What is an ephemeral pod and why does it matter?**
Pods are temporary — they can die from node failure, OOM, or deployment updates. This means you cannot store state in pods (use external DB/PV), and you need centralized logging because pod-local logs disappear on crash.

---

## Prerequisites

```bash
# Local K8s
brew install minikube
brew install kubectl
brew install helm

# AWS K8s (EKS)
brew install eksctl
pip install boto3
# AWS credentials: AWS Console → IAM → Access Keys

# VirtualBox (for hypervisor files)
brew install --cask virtualbox
pip install boto3
```
