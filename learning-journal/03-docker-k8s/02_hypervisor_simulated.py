# ============================================================
# HYPERVISOR — Real World
# ============================================================
#
# TYPE 1: Bare Metal (used in data centers / cloud)
#
#   Physical Hardware (CPU, RAM, Disk, Network)
#   └── VMware ESXi / Hyper-V      ← sits DIRECTLY on hardware, no OS underneath
#       │                              fakes dedicated hardware for each VM
#       ├── VM 1 → Ubuntu + App A  ← full OS, thinks it owns the hardware
#       ├── VM 2 → Windows + App B ← full OS, completely isolated from VM 1
#       └── VM 3 → CentOS + App C  ← full OS, can run different kernel than others
#
#   Key: each VM has its OWN operating system kernel.
#   The hypervisor splits one physical machine into many isolated machines.
#
#   Real examples:
#     AWS EC2        → your instance is a VM on a shared physical server (Xen/KVM)
#                      you never see other customers' VMs — complete isolation
#     Azure VMs      → Hyper-V on bare metal Dell/HP servers in Microsoft datacenters
#     Data centers   → VMware ESXi on physical rack servers
#
# TYPE 2: Hosted (used by developers locally)
#
#   Physical Hardware
#   └── macOS / Windows            ← full OS runs first (unlike Type 1)
#       └── VirtualBox / Parallels / VMware Fusion   ← hypervisor runs as an app
#           ├── VM 1 → Ubuntu      ← full OS inside a window on your Mac
#           └── VM 2 → Windows     ← can run Windows inside macOS
#
#   Slower than Type 1 because there's an extra OS layer underneath.
#
# ============================================================

import time

def log(method_name, message):
    print(f"[{method_name}] {message}")


class PhysicalServer:
    # log ORDER 1: __init__ prints first when server is created
    def __init__(self, name, total_ram_gb, total_disk_gb):
        self.name = name
        self.total_ram_gb = total_ram_gb
        self.total_disk_gb = total_disk_gb
        self.used_ram_gb = 0
        self.used_disk_gb = 0
        self.vms = []
        log("PhysicalServer.__init__", f"Server '{name}' created ({total_ram_gb}GB RAM, {total_disk_gb}GB Disk)")

    # LOG ORDER 4: status() prints last after all VMs boot
    def status(self):
        log("PhysicalServer.status", f"Server: {self.name}")
        log("PhysicalServer.status", f"RAM : {self.used_ram_gb}GB used / {self.total_ram_gb}GB total")
        log("PhysicalServer.status", f"Disk: {self.used_disk_gb}GB used / {self.total_disk_gb}GB total")
        log("PhysicalServer.status", f"VMs : {len(self.vms)} running")


class VirtualMachine:
    # LOG ORDER 2: __init__ prints when each VM is defined
    def __init__(self, name, os, app, ram_gb, disk_gb):
        self.name = name
        self.os = os
        self.app = app
        self.ram_gb = ram_gb
        self.disk_gb = disk_gb
        log("VirtualMachine.__init__", f"VM '{name}' defined → {app} on {os}")

    # LOG ORDER 3: boot() prints when each VM starts
    def boot(self, server):
        log("VirtualMachine.boot", f"Booting {self.name}...")
        log("VirtualMachine.boot", f"OS   : {self.os} (full OS loading...)")
        log("VirtualMachine.boot", f"App  : {self.app}")
        log("VirtualMachine.boot", f"RAM  : {self.ram_gb}GB allocated")
        log("VirtualMachine.boot", f"Disk : {self.disk_gb}GB allocated")
        time.sleep(1)
        log("VirtualMachine.boot", f"✅ {self.name} ready! (took ~3 minutes in real life)")

        server.used_ram_gb += self.ram_gb
        server.used_disk_gb += self.disk_gb
        server.vms.append(self)


# ──────────────────────────────────────────
# PRINT ORDER:
#   1. PhysicalServer.__init__  → server created
#   2. VirtualMachine.__init__  → each VM defined (x4)
#   3. VirtualMachine.boot      → each VM boots (x4)
#   4. PhysicalServer.status    → final server stats
# ──────────────────────────────────────────

print("\n" + "="*50)
print("REAL WORLD: Company using Hypervisor (pre-Docker)")
print("="*50)

# triggers LOG ORDER 1
server = PhysicalServer("Dell PowerEdge R740", total_ram_gb=32, total_disk_gb=500)

# triggers LOG ORDER 2 (x4)
vms = [
    VirtualMachine("VM-Payment",  "Ubuntu 20.04",   "Payment Service", ram_gb=2, disk_gb=20),
    VirtualMachine("VM-Users",    "Ubuntu 20.04",   "User Service",    ram_gb=2, disk_gb=20),
    VirtualMachine("VM-Email",    "Windows Server", "Email Service",   ram_gb=2, disk_gb=20),
    VirtualMachine("VM-Database", "CentOS 7",       "MySQL Database",  ram_gb=4, disk_gb=100),
]

print("\nStarting all VMs...")
# triggers LOG ORDER 3 (x4)
for vm in vms:
    vm.boot(server)

# triggers LOG ORDER 4
server.status()

print(f"\n⚠️  Problems with this setup:")
print(f"  - Used {server.used_ram_gb}GB RAM before even running the apps!")
print(f"  - Each VM took ~3 minutes to boot")
print(f"  - Only {server.total_ram_gb - server.used_ram_gb}GB RAM left for actual apps")

# ──────────────────────────────────────────
# COMPARISON: Same apps with Docker
# ──────────────────────────────────────────
print("\n\n" + "="*50)
print("SAME APPS with Docker (containers)")
print("="*50)

containers = [
    {"name": "payment-service", "ram_mb": 100, "disk_mb": 200},
    {"name": "user-service",    "ram_mb": 100, "disk_mb": 200},
    {"name": "email-service",   "ram_mb": 80,  "disk_mb": 150},
    {"name": "mysql-db",        "ram_mb": 512, "disk_mb": 500},
]

total_ram_mb = 0
total_disk_mb = 0

print("\nStarting all containers...")
for c in containers:
    log("DockerEngine.start", f"{c['name']} → Ready in 2 seconds ✅ ({c['ram_mb']}MB RAM)")
    total_ram_mb += c["ram_mb"]
    total_disk_mb += c["disk_mb"]

print(f"\n✅ Docker Summary:")
print(f"  Total RAM used : {total_ram_mb}MB  ({total_ram_mb/1024:.1f}GB)")
print(f"  Total Disk used: {total_disk_mb}MB ({total_disk_mb/1024:.1f}GB)")
print(f"  Startup time   : 2 seconds each")

print(f"\n📊 VM vs Docker (same 4 apps):")
print(f"  {'':25} {'VM':>10} {'Docker':>10}")
print(f"  {'RAM used':25} {'10 GB':>10} {'0.8 GB':>10}")
print(f"  {'Disk used':25} {'160 GB':>10} {'1 GB':>10}")
print(f"  {'Startup time':25} {'12 min':>10} {'8 sec':>10}")
print(f"  {'Apps on same server':25} {'4':>10} {'40+':>10}")
