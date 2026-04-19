/**
 * Pattern 8 — Sealed Classes and Interfaces
 * Venkat: "Sealed types give you controlled extension. You decide who can implement you."
 *
 * Problem without sealed:
 *   Any class in any package can implement your interface — you lose control
 *
 * With sealed:
 *   Only the classes you permit can implement/extend
 *   Compiler knows ALL subtypes → exhaustive pattern matching
 *   No default case needed in switch (compiler warns if you miss a type)
 *
 * Requires: Java 17+
 * Use case: payment types, shapes, AST nodes, result types (Success/Failure)
 */
class SealedClasses {

    // ── SEALED INTERFACE — only these 3 can implement Payment ─────────────────

    sealed interface Payment permits CreditCard, UpiPayment, WalletPayment {
        double amount();
        String description();
    }

    record CreditCard(double amount, String cardLast4) implements Payment {
        public String description() { return "Credit card ending " + cardLast4; }
    }

    record UpiPayment(double amount, String upiId) implements Payment {
        public String description() { return "UPI: " + upiId; }
    }

    record WalletPayment(double amount, String walletName) implements Payment {
        public String description() { return walletName + " wallet"; }
    }

    // Process — exhaustive switch, no default needed, compiler checks all cases
    static String processPayment(Payment payment) {
        return switch (payment) {
            case CreditCard  c -> "Charging ₹" + c.amount() + " to " + c.description();
            case UpiPayment  u -> "UPI request ₹" + u.amount() + " to " + u.description();
            case WalletPayment w -> "Debiting ₹" + w.amount() + " from " + w.description();
            // No default needed — sealed means compiler knows this is exhaustive
        };
    }

    // ── SEALED HIERARCHY — Shape ───────────────────────────────────────────────

    sealed interface Shape permits Circle, Rectangle, Triangle {
        double area();
    }

    record Circle(double radius) implements Shape {
        public double area() { return Math.PI * radius * radius; }
    }

    record Rectangle(double width, double height) implements Shape {
        public double area() { return width * height; }
    }

    record Triangle(double base, double height) implements Shape {
        public double area() { return 0.5 * base * height; }
    }

    static String describe(Shape shape) {
        return switch (shape) {
            case Circle    c -> "Circle r=" + c.radius()   + " area=" + String.format("%.2f", c.area());
            case Rectangle r -> "Rect " + r.width() + "x" + r.height() + " area=" + r.area();
            case Triangle  t -> "Triangle b=" + t.base() + " h=" + t.height() + " area=" + t.area();
        };
    }

    // ── RESULT TYPE — Success or Failure (replaces exception-driven flow) ──────

    sealed interface Result<T> permits Result.Success, Result.Failure {
        record Success<T>(T value) implements Result<T> {}
        record Failure<T>(String error) implements Result<T> {}
    }

    static Result<Integer> divide(int a, int b) {
        if (b == 0) return new Result.Failure<>("Cannot divide by zero");
        return new Result.Success<>(a / b);
    }

    public static void main(String[] args) {
        // ── Payment sealed interface ───────────────────────────────────────────
        System.out.println("Sealed Payment types:");
        java.util.List<Payment> payments = java.util.List.of(
            new CreditCard(1500, "4242"),
            new UpiPayment(300, "user@paytm"),
            new WalletPayment(200, "PhonePe")
        );
        payments.forEach(p -> System.out.println("  " + processPayment(p)));

        // ── Shape hierarchy ───────────────────────────────────────────────────
        System.out.println("\nSealed Shape hierarchy:");
        java.util.List<Shape> shapes = java.util.List.of(
            new Circle(5),
            new Rectangle(4, 6),
            new Triangle(3, 8)
        );
        shapes.forEach(s -> System.out.println("  " + describe(s)));

        // ── Result type — no exceptions in normal flow ────────────────────────
        System.out.println("\nSealed Result type:");
        switch (divide(10, 2)) {
            case Result.Success<Integer>  s -> System.out.println("  Result: " + s.value());
            case Result.Failure<Integer>  f -> System.out.println("  Error:  " + f.error());
        }

        switch (divide(10, 0)) {
            case Result.Success<Integer>  s -> System.out.println("  Result: " + s.value());
            case Result.Failure<Integer>  f -> System.out.println("  Error:  " + f.error());
        }
    }
}
