import java.util.List;
import java.util.function.Predicate;

/**
 * Pattern 3 — Strategy Pattern with Lambdas
 * Venkat: "Lambdas ARE the strategy. You don't need a class hierarchy anymore."
 *
 * Traditional: create interface + concrete class per strategy → verbose
 * Modern:      pass a lambda — the lambda IS the strategy
 *
 * Functional interface = any interface with exactly one abstract method
 * Predicate<T>, Function<T,R>, Consumer<T> are built-in strategy interfaces
 */
class StrategyPattern {

    // ── TRADITIONAL — one class per strategy ─────────────────────────────────

    interface DiscountStrategy {
        double apply(double price);
    }

    static class NoDiscount implements DiscountStrategy {
        public double apply(double price) { return price; }
    }

    static class TenPercentOff implements DiscountStrategy {
        public double apply(double price) { return price * 0.9; }
    }

    // With traditional approach you need a new class for every new discount

    // ── MODERN — lambda IS the strategy ──────────────────────────────────────

    static double checkout(double price, DiscountStrategy strategy) {
        return strategy.apply(price);
    }

    // ── PREDICATE STRATEGY — filter employees ─────────────────────────────────

    record Employee(String name, String dept, double salary) {}

    static List<Employee> filter(List<Employee> employees, Predicate<Employee> criteria) {
        return employees.stream().filter(criteria).toList();
    }

    public static void main(String[] args) {
        // ── Traditional ──────────────────────────────────────────────────────
        System.out.println("Traditional strategy:");
        System.out.println("  No discount:    " + checkout(100, new NoDiscount()));
        System.out.println("  10% off:        " + checkout(100, new TenPercentOff()));

        // ── Lambda — no class needed ──────────────────────────────────────────
        System.out.println("\nLambda strategy:");
        System.out.println("  No discount:    " + checkout(100, price -> price));
        System.out.println("  10% off:        " + checkout(100, price -> price * 0.9));
        System.out.println("  Flat 20 off:    " + checkout(100, price -> price - 20));
        System.out.println("  Member price:   " + checkout(100, price -> price * 0.75));
        // No new class required — just a new lambda

        // ── Predicate strategy ────────────────────────────────────────────────
        List<Employee> employees = List.of(
            new Employee("Alice",  "IT",  95000),
            new Employee("Bob",    "HR",  60000),
            new Employee("Carol",  "IT",  120000),
            new Employee("Dave",   "Finance", 80000)
        );

        System.out.println("\nIT employees over 90k:");
        filter(employees,
               emp -> emp.dept().equals("IT") && emp.salary() > 90000)
            .forEach(e -> System.out.println("  " + e.name() + " - " + e.salary()));

        System.out.println("\nAll HR:");
        filter(employees, emp -> emp.dept().equals("HR"))
            .forEach(e -> System.out.println("  " + e.name()));

        // Strategies can be stored and reused
        Predicate<Employee> highEarner = emp -> emp.salary() > 100000;
        Predicate<Employee> itDept     = emp -> emp.dept().equals("IT");

        System.out.println("\nHigh-earning IT employees:");
        filter(employees, highEarner.and(itDept))
            .forEach(e -> System.out.println("  " + e.name()));
    }
}
