import java.util.function.Supplier;

/**
 * Pattern 5 — Lazy Evaluation
 * Venkat: "Java is eager by default — it evaluates arguments immediately.
 *          Laziness defers computation until the result is actually needed."
 *
 * Use Supplier<T> to wrap a computation without executing it.
 * The computation only runs when you call supplier.get().
 *
 * When to use:
 *   - Expensive computation that may not be needed
 *   - Database/API call that should only happen if a condition is met
 *   - Logging messages that should not build the string unless log level allows
 */
class LazyEvaluation {

    // ── EAGER — always computes, even when not needed ─────────────────────────

    static String expensiveOperation() {
        System.out.println("  [computing expensive result...]");
        return "result";
    }

    static void logIfDebugEager(boolean debug, String message) {
        // message is evaluated BEFORE entering this method
        // even if debug=false, the string was already built
        if (debug) System.out.println("DEBUG: " + message);
    }

    // ── LAZY — wraps in Supplier, defers until needed ─────────────────────────

    static void logIfDebugLazy(boolean debug, Supplier<String> messageSupplier) {
        if (debug) System.out.println("DEBUG: " + messageSupplier.get());
        // get() only called when debug is true
    }

    // ── Lazy<T> wrapper — compute once, cache result ──────────────────────────

    static class Lazy<T> {
        private final Supplier<T> supplier;
        private T value;
        private boolean computed = false;

        Lazy(Supplier<T> supplier) {
            this.supplier = supplier;
        }

        T get() {
            if (!computed) {
                System.out.println("  [first access — computing now]");
                value    = supplier.get();
                computed = true;
            } else {
                System.out.println("  [returning cached value]");
            }
            return value;
        }
    }

    // ── Real example: config loaded lazily ───────────────────────────────────

    static class AppConfig {
        private final Lazy<String> dbUrl = new Lazy<>(() -> {
            System.out.println("  [connecting to config server...]");
            return "jdbc:mysql://prod-db:3306/app";
        });

        String getDbUrl() { return dbUrl.get(); }
    }

    public static void main(String[] args) {
        // ── Eager logging — string built even if not printed ──────────────────
        System.out.println("Eager log (debug=false):");
        logIfDebugEager(false, "Value = " + expensiveOperation());  // computed anyway!

        // ── Lazy logging — string only built if needed ────────────────────────
        System.out.println("\nLazy log (debug=false):");
        logIfDebugLazy(false, () -> "Value = " + expensiveOperation());  // NOT computed

        System.out.println("\nLazy log (debug=true):");
        logIfDebugLazy(true,  () -> "Value = " + expensiveOperation());  // computed here

        // ── Lazy<T> wrapper — compute once, cache ────────────────────────────
        System.out.println("\nLazy<T> wrapper:");
        Lazy<String> lazyValue = new Lazy<>(() -> {
            System.out.println("  [running computation]");
            return "expensive-result";
        });

        System.out.println("Before first access — nothing computed yet");
        System.out.println("First  get: " + lazyValue.get());  // computes
        System.out.println("Second get: " + lazyValue.get());  // cached

        // ── Config loaded only when needed ────────────────────────────────────
        System.out.println("\nLazy config:");
        AppConfig config = new AppConfig();
        System.out.println("Config object created — DB not connected yet");
        System.out.println("URL: " + config.getDbUrl());   // connects here
        System.out.println("URL: " + config.getDbUrl());   // cached
    }
}
