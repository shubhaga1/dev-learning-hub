import java.util.Optional;

/**
 * Pattern 1 — Null vs Optional
 * Venkat: "Null is a code smell. Optional forces you to deal with absence explicitly."
 *
 * BAD : return null when not found → caller forgets null check → NullPointerException
 * GOOD: return Optional<T> → caller must handle absent case → no surprise crashes
 *
 * Rules:
 *   ✓ Return Optional when a method may not find a value
 *   ✗ Never use Optional as a method parameter (use overloading instead)
 *   ✗ Never return Optional<List> — return empty list instead
 *   ✗ Never call optional.get() directly — use orElse / orElseThrow
 */
class NullVsOptional {

    // ── BAD — returns null ────────────────────────────────────────────────────

    static String findUserByIdBAD(int id) {
        if (id == 1) return "Alice";
        return null;                          // caller must remember to null-check
    }

    // ── GOOD — returns Optional ───────────────────────────────────────────────

    static Optional<String> findUserById(int id) {
        if (id == 1) return Optional.of("Alice");
        return Optional.empty();              // explicit: "might not exist"
    }

    // ── GOOD — empty list, not null ───────────────────────────────────────────

    static java.util.List<String> getOrders(int userId) {
        if (userId == 99) return java.util.List.of("Order1", "Order2");
        return java.util.List.of();           // never return null for collections
    }

    public static void main(String[] args) {
        // BAD — caller forgets null check → NPE waiting to happen
        String bad = findUserByIdBAD(99);
        System.out.println("BAD (null): " + bad);  // null — no crash yet
        // bad.toUpperCase();                       // → NullPointerException!

        // GOOD — Optional forces handling
        findUserById(1)
            .map(String::toUpperCase)
            .ifPresent(name -> System.out.println("Found: " + name));  // Found: ALICE

        findUserById(99)
            .ifPresentOrElse(
                name -> System.out.println("Found: " + name),
                ()   -> System.out.println("User not found — handled safely") // ← runs
            );

        // orElse — provide default
        String name = findUserById(99).orElse("Guest");
        System.out.println("With default: " + name);   // Guest

        // orElseThrow — explicit failure
        try {
            findUserById(99).orElseThrow(() -> new RuntimeException("User 99 not found"));
        } catch (RuntimeException e) {
            System.out.println("Caught: " + e.getMessage());
        }

        // empty list — not null
        System.out.println("Orders: " + getOrders(1));  // []
    }
}
