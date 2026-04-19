#!/bin/bash
# ============================================================
# LEARNING DOCKER COMMANDS
# Run each section one by one in your terminal
#
# SECTIONS:
#   1. docker run basics
#   2. -p port mapping
#   3. --rm cleanup flag
#   4. images vs containers
#   5. useful inspection commands
# ============================================================


# ============================================================
# SECTION 1: docker run — the core command
# "download the image and start a container from it"
# ============================================================

# Simplest possible run — just print hello and exit
docker run hello-world

# What happened:
#   1. Docker looked for image "hello-world" locally → not found
#   2. Downloaded it from Docker Hub (docker.io/library/hello-world)
#   3. Started a container from it
#   4. Container printed its message and exited

# Run Ubuntu and print something
docker run ubuntu echo "I am inside Ubuntu"
# Your Mac ran a Linux command without installing Linux!


# ============================================================
# SECTION 2: -p port mapping
# "make a port inside the container accessible on your Mac"
# ============================================================

# Container is isolated — its ports are NOT visible by default
#
#   Your Mac         Container
#   ─────────        ──────────
#   port 8000   ←→   port 8000   (with -p 8000:8000)
#   port 3000   ←→   port 80     (with -p 3000:80)
#
#   Format: -p <your_mac_port>:<container_port>

# Run nginx web server, map Mac:8080 → container:80
docker run -d -p 8080:80 nginx
# Now open: http://localhost:8080 → you see nginx welcome page!

# Stop it
docker stop $(docker ps -q --filter ancestor=nginx)


# ============================================================
# SECTION 3: --rm — auto cleanup
# "delete the container when it exits"
# ============================================================

# WITHOUT --rm: container stays after exit (takes up space)
docker run ubuntu echo "no cleanup"
docker ps -a   # you'll see the stopped container still there

# WITH --rm: container is deleted immediately on exit
docker run --rm ubuntu echo "auto cleanup"
docker ps -a   # gone!

# Rule of thumb:
#   --rm    → for one-off tasks (run, get result, done)
#   no --rm → for debugging (keep container to inspect it after)


# ============================================================
# SECTION 4: images vs containers
#
# IMAGE    = the blueprint (like a class in Python)
# CONTAINER = running instance (like an object in Python)
#
#   image: ubuntu          → blueprint
#   container 1: ubuntu    → one running instance
#   container 2: ubuntu    → another running instance (same image!)
# ============================================================

# List downloaded images on your machine
docker images

# List running containers
docker ps

# List ALL containers (including stopped)
docker ps -a

# Run same image twice simultaneously
docker run -d --name box1 ubuntu sleep 30
docker run -d --name box2 ubuntu sleep 30
docker ps    # two containers, same image


# ============================================================
# SECTION 5: Useful inspection commands
# ============================================================

# See logs from a container
docker run --rm ubuntu echo "hello from container"
# docker logs <container_id>

# Run interactively (get a shell inside the container)
docker run -it --rm ubuntu bash
# Now you're INSIDE the container — type "ls", "whoami", "exit"

# Pull image without running
docker pull nginx

# Remove an image
# docker rmi nginx

# Remove all stopped containers (cleanup)
docker container prune

# See how much space Docker is using
docker system df


# ============================================================
# THE vLLM COMMAND EXPLAINED:
#
# docker run                    start a container
#   --rm                        delete it when vLLM stops
#   -p 8000:8000                your Mac:8000 → container:8000
#   vllm/vllm-openai:latest     the pre-built vLLM image
#   --model facebook/opt-125m   argument TO vLLM (not to Docker)
#
# Everything AFTER the image name = command run INSIDE container
# ============================================================
