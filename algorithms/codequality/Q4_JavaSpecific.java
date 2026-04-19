
import java.util.ArrayList;
import java.util.List;

/**
 * Q4: Java-Specific Mistakes
 *
 * Level 1 → magic numbers (no context for what 7, 1000, 26 mean)
 * Level 2 → static when instance is needed (shared state bug)
 * Level 3 → ArrayList where wrong — using List as return type
 * Level 4 → System.out in library method (untestable, uncontrollable output)
 *
 * Rule: Java is explicit — if something looks like a coincidence (a number,
 *       a static, a concrete type), it probably should be named or abstracted.
 */
class Q4_JavaSpecific {

    // ── Level 1: Magic numbers ────────────────────────────────────────────────

    // BAD: what is 26? what is 7? reader has to guess
    static boolean isWeekend_BAD(int day) {
        return day == 6 || day == 7;     // what calendar system? 0-indexed? 1-indexed?
    }

    static char[] trie_BAD = new char[26];  // why 26? only works for lowercase a-z — not obvious

    // GOOD: named constants make intent clear
    static final int SATURDAY = 6;
    static final int SUNDAY   = 7;
    static final int ALPHABET_SIZE = 26;  // lowercase a-z only

    static boolean isWeekend_GOOD(int day) {
        return day == SATURDAY || day == SUNDAY;
    }

    static char[] trie_GOOD = new char[ALPHABET_SIZE];

    // ── Level 2: Static when instance needed — shared state bug ──────────────

    // BAD: counter is static — all Counter objects share the same count
    static class Counter_BAD {
        static int count = 0;   // ← shared across ALL instances

        void increment() { count++; }
        int get()        { return count; }
    }

    // GOOD: count is instance — each Counter has its own
    static class Counter_GOOD {
        int count = 0;          // ← each object has its own copy

        void increment() { count++; }
        int get()        { return count; }
    }

    // ── Level 3: Return concrete type vs interface ────────────────────────────

    // BAD: returning ArrayList forces caller to depend on implementation
    // if you change to LinkedList tomorrow, every caller breaks
    static ArrayList<String> getNames_BAD() {
        ArrayList<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        return names;
    }

    // GOOD: return List (interface) — caller doesn't care how it's stored
    static List<String> getNames_GOOD() {
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        return names;
    }

    // ── Level 4: System.out inside library/helper method ─────────────────────

    // BAD: helper method prints — you can't reuse this in a web server,
    //      can't test it without capturing stdout, can't log to a file
    static int findMax_BAD(int[] arr) {
        int max = arr[0];
        for (int n : arr) {
            if (n > max) max = n;
        }
        System.out.println("Max is: " + max);   // ← side effect in a calculation
        return max;
    }

    // GOOD: method only calculates — caller decides what to do with result
    static int findMax_GOOD(int[] arr) {
        int max = arr[0];
        for (int n : arr) {
            if (n > max) max = n;
        }
        return max;
    }

    public static void main(String[] args) {
        System.out.println("=== Level 1: magic numbers ===");
        System.out.println("Day 6 is weekend: " + isWeekend_GOOD(6));
        System.out.println("Day 3 is weekend: " + isWeekend_GOOD(3));

        System.out.println("\n=== Level 2: static vs instance ===");
        Counter_BAD b1 = new Counter_BAD();
        Counter_BAD b2 = new Counter_BAD();
        b1.increment(); b1.increment();
        b2.increment();
        System.out.println("BAD — b1.count: " + b1.get() + ", b2.count: " + b2.get());
        // Both print 3 — shared state!

        Counter_GOOD g1 = new Counter_GOOD();
        Counter_GOOD g2 = new Counter_GOOD();
        g1.increment(); g1.increment();
        g2.increment();
        System.out.println("GOOD — g1.count: " + g1.get() + ", g2.count: " + g2.get());
        // g1=2, g2=1 — independent

        System.out.println("\n=== Level 3: return type ===");
        List<String> names = getNames_GOOD();   // works with any List implementation
        System.out.println(names);

        System.out.println("\n=== Level 4: System.out in library ===");
        int[] arr = {3, 1, 4, 1, 5, 9};
        // findMax_BAD(arr);               // prints as side effect — hard to test
        int max = findMax_GOOD(arr);
        System.out.println("Max: " + max); // caller controls the output
    }
}
