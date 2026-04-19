# ============================================================
# KUBERNETES (K8s) WAY — Container Orchestration
# ============================================================
#
# Problem Docker alone can't solve:
#   - What if a container crashes? → restart it automatically
#   - What if traffic spikes? → scale to 10 containers automatically
#   - What if a server dies? → move containers to another server
#   - How to update app without downtime? → rolling updates
#
# Kubernetes solves all of this!
#
# ─────────────────────────────────────────────────────
# K8s Cluster
# ├── Control Plane (Master) — the brain
# │   ├── API Server     → receives all commands
# │   ├── Scheduler      → decides which node runs what
# │   └── Controller     → watches and fixes things
# │
# └── Nodes (Worker machines) — the muscle
#     ├── Node 1
#     │   ├── Pod 1 → Container (App A)
#     │   └── Pod 2 → Container (App A)
#     ├── Node 2
#     │   ├── Pod 3 → Container (App A)
#     │   └── Pod 4 → Container (App B)
#     └── Node 3
#         └── Pod 5 → Container (App B)
# ─────────────────────────────────────────────────────
#
# Key K8s concepts:
#   Pod         → smallest unit, wraps 1 or more containers
#   Node        → a server/machine that runs pods
#   Deployment  → tells K8s "run 3 copies of my app"
#   Service     → exposes your app to the internet
#   Namespace   → logical grouping (like folders for pods)
#
# Example Deployment YAML:
# ─────────────────────────────────
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: my-app
# spec:
#   replicas: 3          ← run 3 containers
#   template:
#     spec:
#       containers:
#       - name: my-app
#         image: my-app:latest
# ─────────────────────────────────
#
# Commands:
#   kubectl apply -f deployment.yaml  ← deploy your app
#   kubectl get pods                  ← list all pods
#   kubectl scale --replicas=10       ← scale up to 10
#   kubectl rollout undo              ← roll back update
# ============================================================

import time

def simulate_k8s():
    print("K8s Cluster starting...\n")

    print("📦 Deploying App A with 3 replicas...")
    for i in range(1, 4):
        print(f"  Pod {i} → Running ✅")

    print("\n🔥 Pod 2 crashed!")
    print("  K8s detected crash → restarting Pod 2 automatically...")
    print("  Pod 2 → Running ✅ (auto-healed!)")

    print("\n📈 Traffic spike detected!")
    print("  K8s scaling from 3 → 6 replicas...")
    for i in range(4, 7):
        print(f"  Pod {i} → Running ✅")

    print("\n🚀 Deploying new version (zero downtime)...")
    print("  Rolling update: replacing pods one by one...")
    for i in range(1, 7):
        print(f"  Pod {i} → Updated to v2 ✅")

    print("\n✅ K8s Summary:")
    print("  Auto-healing    → crashed pods restart automatically")
    print("  Auto-scaling    → scales up/down based on traffic")
    print("  Rolling updates → deploy with zero downtime")
    print("  Self-healing    → if a node dies, pods move to another node")

simulate_k8s()

# ============================================================
# EVOLUTION SUMMARY
# ============================================================
#
# Traditional → runs directly on OS
#   ❌ "works on my machine" problem
#
# Hypervisor → full VMs
#   ✅ isolation
#   ❌ heavy, slow, expensive
#
# Docker → containers
#   ✅ isolation
#   ✅ fast, lightweight
#   ❌ what if container crashes? no auto-healing
#
# Kubernetes → orchestrates containers
#   ✅ isolation
#   ✅ fast, lightweight
#   ✅ auto-healing, auto-scaling, zero-downtime deploys
# ============================================================
