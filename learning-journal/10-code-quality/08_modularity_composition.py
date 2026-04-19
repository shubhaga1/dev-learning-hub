"""
LEVEL 8 — Modularity: Composition Over Inheritance
Prefer composing small focused behaviours over deep inheritance chains.
Inheritance = "is-a". Composition = "has-a". Composition is more flexible.
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE — deep inheritance chain
# ─────────────────────────────────────────────────────────

class Animal:
    def breathe(self): print("breathing")

class FlyingAnimal(Animal):
    def fly(self): print("flying")

class SwimmingAnimal(Animal):
    def swim(self): print("swimming")

# Duck can fly AND swim — but Python has no multiple inheritance sanity here
# What about a FlyingSwimmingAnimal? Class explosion begins.
class Duck(FlyingAnimal):
    pass  # can't easily swim without messy multiple inheritance


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] Deep hierarchies are rigid. Adding a new ability means a new class level.
[L2] FlyingSwimmingAnimal or SwimmingRunningAnimal leads to combinatorial explosion.
[L3] Changing a parent class breaks all children — fragile base class problem.
[L4] Hard to reuse a single behaviour (e.g., swimming) without dragging the whole chain.
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE — compose behaviours as capabilities
# ─────────────────────────────────────────────────────────

class FlyBehaviour:
    def fly(self): print("flying with wings")

class SwimBehaviour:
    def swim(self): print("swimming with webbed feet")

class RunBehaviour:
    def run(self): print("running on land")

class Animal:
    def breathe(self): print("breathing")

# Compose exactly the behaviours the animal needs
class Duck(Animal):
    def __init__(self):
        self.fly_ability  = FlyBehaviour()
        self.swim_ability = SwimBehaviour()

    def fly(self):  self.fly_ability.fly()
    def swim(self): self.swim_ability.swim()

class Dog(Animal):
    def __init__(self):
        self.run_ability  = RunBehaviour()
        self.swim_ability = SwimBehaviour()

    def run(self):  self.run_ability.run()
    def swim(self): self.swim_ability.swim()

# Penguin swims but doesn't fly — easy, just don't compose FlyBehaviour
class Penguin(Animal):
    def __init__(self):
        self.swim_ability = SwimBehaviour()

    def swim(self): self.swim_ability.swim()


# ─────────────────────────────────────────────────────────
# 🧪 TEST
# ─────────────────────────────────────────────────────────

duck = Duck()
duck.fly()    # flying with wings
duck.swim()   # swimming with webbed feet

penguin = Penguin()
penguin.swim()         # works
# penguin.fly()        # AttributeError — correct, penguins can't fly
