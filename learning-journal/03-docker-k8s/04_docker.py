# ============================================================
# DOCKER WAY — Containers
# ============================================================
#
# Your Machine (macOS)
# └── Docker Engine (shares your OS kernel)
#     ├── Container 1 → Python 3.9 + App A   ← no full OS!
#     ├── Container 2 → Python 3.11 + App B
#     └── Container 3 → Java + App C
#
# Key difference from VM:
#   - Containers SHARE the host OS kernel
#   - Only packages the APP + its dependencies
#   - No full OS needed inside container
#
# Problems solved vs Hypervisor:
#   ✅ Starts in seconds (not minutes)
#   ✅ Uses MBs of RAM (not GBs)
#   ✅ Small image size (MBs not GBs)
#   ✅ Same isolation as VM
#   ✅ "Works on my machine" problem solved forever
#
# Core Docker concepts:
#   Dockerfile  → recipe to build your app image
#   Image       → snapshot of your app + dependencies (like a zip file)
#   Container   → running instance of an image (like a process)
#   Registry    → store for images (Docker Hub, AWS ECR)
#
# Example Dockerfile for this app:
# ─────────────────────────────────
# FROM python:3.9-slim          ← base image (tiny Python OS)
# WORKDIR /app                  ← working directory inside container
# COPY . .                      ← copy your code in
# RUN pip install flask         ← install dependencies
# CMD ["python", "app.py"]      ← run your app
# ─────────────────────────────────
#
# Commands:
#   docker build -t my-app .    ← build image from Dockerfile
#   docker run my-app           ← start a container
#   docker ps                   ← list running containers
#   docker stop <id>            ← stop a container
# ============================================================

print("Container 1 starting...")
print("Container 1 ready in 2 seconds! Uses only 50MB RAM")
print("App A running inside Container 1")

print("\nContainer 2 starting...")
print("Container 2 ready in 2 seconds! Uses only 50MB RAM")
print("App B running inside Container 2")

print("\nTotal RAM used: 100MB — vs 4GB with VMs!")
print("\nVM vs Docker:")
print(f"  {'':20} {'VM':>10} {'Docker':>10}")
print(f"  {'Startup time':20} {'2 min':>10} {'2 sec':>10}")
print(f"  {'RAM per app':20} {'1-2 GB':>10} {'50 MB':>10}")
print(f"  {'Disk size':20} {'10-20 GB':>10} {'200 MB':>10}")
print(f"  {'Isolation':20} {'Full':>10} {'Full':>10}")
