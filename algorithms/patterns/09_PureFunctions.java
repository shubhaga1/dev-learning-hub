import java.util.List;
import java.util.stream.Collectors;

/**
 * Pattern 9 — Pure Functions
 * Venkat: "A pure function has no side effects AND doesn't depend on mutable external state.
 *          Both conditions required — violating either makes it impure."
 *
 * Pure function:
 *   1. Same input ALWAYS produces same output
 *   2. Does NOT mutate external state
 *   3. Does NOT read mutable external state
 *
 * Why it matters:
 *   - Safe for parallel streams (no race conditions)
 *   - Testable in isolation (no setup/teardown needed)
 *   - Supports lazy evaluation
 *   - Easy to reason about
 */
class PureFunctions {

    // ── IMPURE — reads external mutable state ─────────────────────────────────

    static double taxRate = 0.18;   // mutable external state

    static double calculateTaxIMPURE(double amount) {
        return amount * taxRate;    // depends on external variable — not pure
        // If taxRate changes, same input gives different output
    }

    // ── IMPURE — mutates external state ──────────────────────────────────────

    static int counter = 0;

    static int nextIdIMPURE() {
        return ++counter;           // mutates external state — not pure
        // Can't call this twice and get same result
    }

    // ── IMPURE — side effect inside stream ───────────────────────────────────

    static List<Integer> doubled = new java.util.ArrayList<>();  // shared list

    static void doubleItemsIMPURE(List<Integer> numbers) {
        numbers.stream()
               .forEach(n -> doubled.add(n * 2));   // ✗ mutating external list
        // Breaks in parallel streams — race condition on 'doubled'
    }

    // ── PURE ─────────────────────────────────────────────────────────────────

    static double calculateTax(double amount, double taxRate) {
        return amount * taxRate;    // all inputs explicit — pure
    }

    static int add(int a, int b) {
        return a + b;               // no state, no side effects — pure
    }

    static String formatName(String first, String last) {
        return last + ", " + first; // transforms input, no external deps — pure
    }

    static List<Integer> doubleItems(List<Integer> numbers) {
        return numbers.stream()
                      .map(n -> n * 2)          // pure lambda — no external mutation
                      .collect(Collectors.toList());  // returns new list
    }

    // ── PURE PIPELINE — chain pure functions ─────────────────────────────────

    record Order(String id, double amount, boolean isPremium) {}

    static double basePrice(Order order) {
        return order.amount();
    }

    static double applyPremiumDiscount(double price, boolean isPremium) {
        return isPremium ? price * 0.9 : price;   // pure
    }

    static double applyTax(double price, double taxRate) {
        return price * (1 + taxRate);             // pure
    }

    static double finalPrice(Order order, double taxRate) {
        return applyTax(
            applyPremiumDiscount(
                basePrice(order),
                order.isPremium()
            ),
            taxRate
        );
        // Entire pipeline is pure — deterministic, testable, parallel-safe
    }

    public static void main(String[] args) {
        // ── Impure demos ──────────────────────────────────────────────────────
        System.out.println("IMPURE functions:");
        System.out.println("  Tax (rate=0.18): " + calculateTaxIMPURE(1000));
        taxRate = 0.28;  // external change
        System.out.println("  Tax (rate=0.28): " + calculateTaxIMPURE(1000));  // different output, same input!

        System.out.println("  ID: " + nextIdIMPURE());  // 1
        System.out.println("  ID: " + nextIdIMPURE());  // 2 — not repeatable

        // ── Pure demos ────────────────────────────────────────────────────────
        System.out.println("\nPURE functions:");
        System.out.println("  Tax @18%: " + calculateTax(1000, 0.18));  // always 180.0
        System.out.println("  Tax @18%: " + calculateTax(1000, 0.18));  // same input, same output
        System.out.println("  Tax @28%: " + calculateTax(1000, 0.28));  // explicit rate

        System.out.println("  " + formatName("Shubham", "Garg"));

        List<Integer> nums = List.of(1, 2, 3, 4, 5);
        System.out.println("  Original:  " + nums);
        System.out.println("  Doubled:   " + doubleItems(nums));
        System.out.println("  Original:  " + nums);  // unchanged — pure function

        // ── Pure pipeline ──────────────────────────────────────────────────────
        System.out.println("\nPure order pricing pipeline:");
        Order regular = new Order("O1", 1000, false);
        Order premium = new Order("O2", 1000, true);

        System.out.printf("  Regular: ₹%.2f%n", finalPrice(regular, 0.18));  // 1180.0
        System.out.printf("  Premium: ₹%.2f%n", finalPrice(premium, 0.18));  // 1062.0 (10% off then 18% tax)
    }
}
