/**
 * toString() — How Java prints objects
 *
 * Every class in Java silently extends Object:
 *   class Node { ... }
 *   is actually:
 *   class Node extends Object { ... }
 *
 * Object has a default toString():
 *   public String toString() {
 *       return getClass().getName() + "@" + Integer.toHexString(hashCode());
 *   }
 *   → prints: "NodeBasic$Node@7852e922"
 *     NodeBasic$Node = class name ($ = nested inside NodeBasic)
 *     7852e922       = hashCode() as hex (memory address by default)
 *
 * When you @Override toString() → Java uses YOUR version instead of Object's.
 *
 * toString() is called AUTOMATICALLY when:
 *   System.out.println(obj)       → Java calls obj.toString() internally
 *   "Value: " + obj               → Java calls obj.toString() for concatenation
 *   String.valueOf(obj)           → calls toString()
 */
class ToStringDemo {

    // ── Without toString ──────────────────────────────────────────────────────
    static class BadPoint {
        int x, y;
        BadPoint(int x, int y) { this.x = x; this.y = y; }
        // No toString — inherits Object's default
    }

    // ── With toString ─────────────────────────────────────────────────────────
    static class GoodPoint {
        int x, y;
        GoodPoint(int x, int y) { this.x = x; this.y = y; }

        @Override
        public String toString() {
            return "Point(" + x + ", " + y + ")";
        }
    }

    // ── With full Object contract ─────────────────────────────────────────────
    static class Product {
        String name;
        double price;

        Product(String name, double price) {
            this.name = name;
            this.price = price;
        }

        @Override
        public String toString() {
            return "Product{name='" + name + "', price=" + price + "}";
        }

        // equals() — when are two objects "the same"?
        // Default Object.equals() checks reference (same memory address)
        // Override to check by value:
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;               // same reference
            if (!(o instanceof Product)) return false; // wrong type
            Product other = (Product) o;
            return name.equals(other.name) && price == other.price;
        }

        // hashCode() — must override when you override equals()
        // Rule: if a.equals(b) → a.hashCode() == b.hashCode()
        @Override
        public int hashCode() {
            return name.hashCode() * 31 + Double.hashCode(price);
        }
    }

    public static void main(String[] args) {

        // ── Without toString ──────────────────────────────────────────────────
        BadPoint bp = new BadPoint(3, 4);
        System.out.println("Without toString: " + bp);
        // → ToStringDemo$BadPoint@<hex>   ← useless

        // ── With toString ─────────────────────────────────────────────────────
        GoodPoint gp = new GoodPoint(3, 4);
        System.out.println("With toString:    " + gp);
        // → Point(3, 4)   ← readable

        // ── toString called automatically ─────────────────────────────────────
        GoodPoint p = new GoodPoint(10, 20);
        System.out.println(p);                   // auto-calls p.toString()
        System.out.println("Pos: " + p);         // auto-calls p.toString()
        System.out.println(String.valueOf(p));    // auto-calls p.toString()

        // ── equals: default vs overridden ─────────────────────────────────────
        Product p1 = new Product("Laptop", 999.0);
        Product p2 = new Product("Laptop", 999.0);
        Product p3 = p1;  // same reference

        System.out.println("\np1 == p2 (reference): " + (p1 == p2));        // false — different objects
        System.out.println("p1.equals(p2):         " + p1.equals(p2));     // true  — same values
        System.out.println("p1 == p3 (reference):  " + (p1 == p3));        // true  — same reference

        System.out.println("\nProduct: " + p1);
        // → Product{name='Laptop', price=999.0}

        // ── The Object chain ─────────────────────────────────────────────────
        System.out.println("\nEvery object has these from Object:");
        System.out.println("hashCode: " + p1.hashCode());
        System.out.println("class:    " + p1.getClass().getName());
    }
}
