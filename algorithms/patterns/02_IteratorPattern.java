import java.util.List;
import java.util.stream.Collectors;

/**
 * Pattern 2 — External vs Internal Iterator
 * Venkat: "Internal iteration hands control to the library. You describe WHAT, not HOW."
 *
 * External: for/while loop — you control iteration (can break, continue)
 * Internal: streams — library iterates, you pass behaviour as lambda
 *
 * Anti-pattern: modifying shared state inside a stream (shared mutability = bugs in parallel)
 * Pure function rule: stream operations must NOT mutate external variables
 */
class IteratorPattern {

    public static void main(String[] args) {
        List<String> names = List.of("Alice", "Bob", "Charlie", "Anna", "Dave");

        // ── EXTERNAL — explicit loop, you control ─────────────────────────────
        System.out.println("External iteration:");
        for (String name : names) {
            if (name.startsWith("A")) {
                System.out.println("  " + name.toUpperCase());
            }
        }

        // ── INTERNAL — stream, library controls ──────────────────────────────
        System.out.println("\nInternal iteration (stream):");
        names.stream()
             .filter(name -> name.startsWith("A"))    // describe WHAT to filter
             .map(String::toUpperCase)                 // describe WHAT to transform
             .forEach(name -> System.out.println("  " + name));

        // ── ANTI-PATTERN — shared mutability inside stream ────────────────────
        System.out.println("\nAnti-pattern (shared mutability):");
        List<String> resultBAD = new java.util.ArrayList<>();
        names.stream()
             .filter(n -> n.startsWith("A"))
             .forEach(resultBAD::add);   // ✗ mutating external list — breaks in parallel streams
        System.out.println("  BAD (works, but fragile): " + resultBAD);

        // ── CORRECT — collect into new list ───────────────────────────────────
        List<String> resultGOOD = names.stream()
             .filter(n -> n.startsWith("A"))
             .collect(Collectors.toList());            // ✓ no external mutation
        System.out.println("  GOOD (collect): " + resultGOOD);

        // ── REAL EXAMPLE — transform orders ───────────────────────────────────
        List<Integer> prices = List.of(100, 250, 80, 300, 50);

        double avgExpensive = prices.stream()
             .filter(p -> p > 100)                    // keep expensive items
             .mapToInt(Integer::intValue)
             .average()
             .orElse(0);

        System.out.println("\nAvg price of items > 100: " + avgExpensive);  // 275.0
    }
}
