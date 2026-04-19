/**
 * DEFAULT METHODS IN INTERFACES
 *
 * Before Java 8: interfaces = only abstract methods (no body)
 * Java 8+: interfaces can have DEFAULT methods with a real body
 *
 * WHY IT EXISTS:
 *   Java added new methods to Map, List etc. in Java 8.
 *   If those were abstract, every existing class would break.
 *   default = "here's a free implementation — override if you want"
 *
 * Run: javac 01_DefaultMethods.java && java DefaultMethods
 */
class DefaultMethods {

    // ─── 1. Basic default method ──────────────────────────────────────────────
    interface Greeter {

        // abstract — MUST be implemented
        String getName();

        // default — has a body, CAN be overridden but doesn't have to be
        default void greet() {
            System.out.println("Hello, " + getName() + "!");
        }

        // another default
        default void greetFormal() {
            System.out.println("Good day, " + getName() + ". How do you do?");
        }
    }

    // Uses default greet() — doesn't override it
    static class SimpleGreeter implements Greeter {
        public String getName() { return "Shubham"; }
        // greet() and greetFormal() come for free from interface
    }

    // Overrides greet() with custom behaviour
    static class LoudGreeter implements Greeter {
        public String getName() { return "Shubham"; }

        @Override
        public void greet() {
            System.out.println("HEY " + getName().toUpperCase() + "!!!");
        }
        // greetFormal() still comes from default
    }

    // ─── 2. Why default — the real reason (adding to existing interface) ──────
    interface Vehicle {
        String getType();

        // Added in "version 2" of this interface — default so old classes don't break
        default String getFuelType() {
            return "petrol";  // sensible default
        }

        default void describe() {
            System.out.println(getType() + " runs on " + getFuelType());
        }
    }

    // Old class — written before getFuelType() existed, still works fine
    static class Car implements Vehicle {
        public String getType() { return "Car"; }
        // getFuelType() not implemented — uses default "petrol"
    }

    // New class — overrides the default
    static class ElectricCar implements Vehicle {
        public String getType() { return "Electric Car"; }

        @Override
        public String getFuelType() { return "electricity"; }  // override default
    }

    // ─── 3. Two interfaces, same default method — conflict ───────────────────
    // If two interfaces have the same default method, class MUST override it
    interface A {
        default void hello() { System.out.println("Hello from A"); }
    }

    interface B {
        default void hello() { System.out.println("Hello from B"); }
    }

    static class C implements A, B {
        @Override
        public void hello() {
            A.super.hello();  // explicitly choose A's version
            // OR: B.super.hello();
            // OR: write your own
            System.out.println("(resolved conflict in C)");
        }
    }

    // ─── 4. default vs abstract vs static in interface ───────────────────────
    interface MathOps {
        // abstract — must implement
        int compute(int a, int b);

        // default — optional override, has 'this' / can call other methods
        default int computeAndDouble(int a, int b) {
            return compute(a, b) * 2;
        }

        // static — belongs to the interface itself, not to implementing class
        // called as MathOps.description(), not obj.description()
        static String description() {
            return "I am a MathOps interface";
        }
    }

    static class Adder implements MathOps {
        public int compute(int a, int b) { return a + b; }
        // computeAndDouble() comes free from default
    }

    public static void main(String[] args) {

        System.out.println("=== 1. BASIC DEFAULT METHOD ===");
        SimpleGreeter simple = new SimpleGreeter();
        simple.greet();          // uses default
        simple.greetFormal();    // uses default

        LoudGreeter loud = new LoudGreeter();
        loud.greet();            // uses override
        loud.greetFormal();      // still uses default

        System.out.println("\n=== 2. WHY DEFAULT EXISTS (backward compatibility) ===");
        Car car         = new Car();
        ElectricCar ev  = new ElectricCar();
        car.describe();          // Car runs on petrol    (default)
        ev.describe();           // Electric Car runs on electricity (overridden)

        System.out.println("\n=== 3. CONFLICT — two interfaces same default ===");
        new C().hello();

        System.out.println("\n=== 4. default vs abstract vs static ===");
        Adder adder = new Adder();
        System.out.println("compute(3,4)          = " + adder.compute(3, 4));           // abstract
        System.out.println("computeAndDouble(3,4) = " + adder.computeAndDouble(3, 4));  // default
        System.out.println("MathOps.description() = " + MathOps.description());         // static

        System.out.println("""

        SUMMARY:
          abstract  = no body, MUST implement in class
          default   = has body, CAN override, uses 'this', called on instance
          static    = has body, CANNOT override, called on interface name
        """);
    }
}
