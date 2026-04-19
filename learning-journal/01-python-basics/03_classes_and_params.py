"""
CLASSES, PARAMETERS, AND ARGUMENTS IN PYTHON

Parameter = placeholder name in the function/class DEFINITION
Argument  = actual value you PASS when calling the function

    def greet(name):       ← 'name' is a PARAMETER
        print(name)

    greet("Shubham")       ← "Shubham" is the ARGUMENT

Memory trick: Parameter = placeholder, Argument = actual
"""

# ============================================================
# PART 1: Parameters and Arguments — all 4 types
# ============================================================

print("=" * 55)
print("  PART 1: Parameters & Arguments")
print("=" * 55)

# ── 1. Positional — order matters ────────────────────────────
def describe_vm(name, os, ram):         # name, os, ram = PARAMETERS
    print(f"{name} runs {os} with {ram}GB RAM")

describe_vm("VM-1", "Ubuntu", 4)        # "VM-1", "Ubuntu", 4 = ARGUMENTS
describe_vm("VM-2", "Windows", 8)       # must match order exactly

# ── 2. Keyword — order doesn't matter ────────────────────────
describe_vm(ram=16, name="VM-3", os="CentOS")   # any order with keyword

# ── 3. Default — optional, has fallback value ─────────────────
def create_pod(name, replicas=1, image="nginx"):  # replicas and image have defaults
    print(f"Pod '{name}': {replicas} replica(s) of {image}")

create_pod("web")                        # uses defaults → replicas=1, image=nginx
create_pod("api", 3)                     # overrides replicas → 3
create_pod("db", image="postgres")       # overrides just image

# ── 4. *args — variable number of positional arguments ────────
def list_nodes(*nodes):                  # *nodes collects all into a tuple
    print(f"Cluster nodes: {nodes}")

list_nodes("node-1")
list_nodes("node-1", "node-2", "node-3")    # any number works

# ── 5. **kwargs — variable number of keyword arguments ────────
def configure(**settings):               # **settings collects all into a dict
    for key, value in settings.items():
        print(f"  {key} = {value}")

print("Config:")
configure(region="us-east-1", replicas=3, timeout=30)


# ============================================================
# PART 2: Class — blueprint vs object
# ============================================================

print("\n" + "=" * 60)
print("  PART 2: Class vs Object")
print("=" * 55)

class VirtualMachine:
    """
    Class   = blueprint (no memory used, nothing running)
    Object  = instance created from blueprint (real memory, real data)
    """

    # __init__ runs automatically when you create an object
    # 'self' = the object being created (always first parameter)
    def __init__(self, name, os, ram_gb, disk_gb=100):
        #          ^^^^  PARAMETERS of __init__
        self.name    = name       # store argument on the object
        self.os      = os
        self.ram_gb  = ram_gb
        self.disk_gb = disk_gb
        self.running = False
        print(f"[created] {name} ({os}, {ram_gb}GB RAM)")

    def start(self):
        self.running = True
        print(f"[start]   {self.name} is now running")

    def stop(self):
        self.running = False
        print(f"[stop]    {self.name} stopped")

    def status(self):
        state = "running" if self.running else "stopped"
        print(f"[status]  {self.name} → {state} | OS: {self.os} | RAM: {self.ram_gb}GB")


# Creating objects — each is independent in memory
vm1 = VirtualMachine("VM-1", "Ubuntu",  4)       # ARGUMENTS
vm2 = VirtualMachine("VM-2", "Windows", 8, 200)  # override default disk_gb

vm1.start()
vm2.start()
vm1.status()
vm2.status()
vm1.stop()
vm1.status()   # vm1 stopped, vm2 still running — completely independent

print(f"\nvm1 name: {vm1.name}")   # VM-1
print(f"vm2 name: {vm2.name}")    # VM-2  ← separate object, separate data


# ============================================================
# PART 3: Class with class variable vs instance variable
# ============================================================

print("\n" + "=" * 55)
print("  PART 3: Class variable vs Instance variable")
print("=" * 55)

class Pod:

    count = 0    # CLASS variable — shared across ALL objects

    def __init__(self, name, image="nginx"):
        self.name  = name    # INSTANCE variable — unique per object
        self.image = image
        Pod.count += 1       # shared counter increments for every pod created
        print(f"[pod]  '{name}' created (total pods: {Pod.count})")

    def info(self):
        print(f"  name={self.name}  image={self.image}  total_pods={Pod.count}")


p1 = Pod("web-pod")
p2 = Pod("api-pod", "fastapi")
p3 = Pod("db-pod",  "postgres")

p1.info()
p2.info()
p3.info()

# Class variable accessed without any object
print(f"\nTotal pods ever created: {Pod.count}")


# ============================================================
# PART 4: Static method — no object needed
# ============================================================

print("\n" + "=" * 55)
print("  PART 4: Static method vs Instance method")
print("=" * 55)

class Hypervisor:

    def __init__(self, type):
        self.type = type     # instance data

    def describe(self):                    # instance method — needs self (object)
        print(f"Hypervisor type: {self.type}")

    @staticmethod
    def supported_os():                    # static method — no self, no object needed
        return ["Ubuntu", "Windows", "CentOS"]

    @classmethod
    def from_cloud(cls, provider):         # class method — gets the class, not instance
        types = {"aws": "Xen/KVM", "azure": "Hyper-V", "gcp": "KVM"}
        return cls(types.get(provider, "Unknown"))   # creates object for you


# instance method — needs object first
h = Hypervisor("VMware ESXi")
h.describe()

# static method — call on class directly, no object
print(f"Supported OS: {Hypervisor.supported_os()}")

# class method — creates object via factory pattern
aws_hv  = Hypervisor.from_cloud("aws")
azure_hv = Hypervisor.from_cloud("azure")
aws_hv.describe()
azure_hv.describe()


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 55)
print("  SUMMARY")
print("=" * 55)
print("""
Parameter vs Argument:
  def fn(name, age):   ← name, age are PARAMETERS (in definition)
  fn("Shubham", 30)    ← "Shubham", 30 are ARGUMENTS (passed in)

4 parameter types:
  positional  → must be in order
  keyword     → fn(age=30, name="X") — any order
  default     → fn(name, age=25) — optional
  *args       → variable count positional
  **kwargs    → variable count keyword

Class vs Object:
  class Car:    ← blueprint, no memory
  c = Car()     ← object, real memory allocated

self:
  Always first parameter in instance methods
  Refers to the object calling the method
  Python passes it automatically — you never type it

3 method types:
  instance method  → def fn(self)      needs object
  class method     → def fn(cls)       gets the class
  static method    → def fn()          standalone utility
""")
