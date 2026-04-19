import java.util.*;

/**
 * AUTOBOXING & UNBOXING — primitive vs wrapper class
 *
 * Java has 8 primitives: int, double, boolean, char, long, float, byte, short
 * Each has an object wrapper:  Integer, Double, Boolean, Character, Long...
 *
 * Primitives:
 *   - stored directly in memory (fast, no overhead)
 *   - cannot be null
 *   - cannot be used in generics (List<int> won't compile)
 *
 * Wrappers:
 *   - objects on the heap (small overhead)
 *   - CAN be null
 *   - required for generics, collections, lambdas
 *
 * AUTOBOXING  = Java silently converts primitive → wrapper
 * UNBOXING    = Java silently converts wrapper  → primitive
 */
class AutoboxingDemo {

    public static void main(String[] args) {

        // ── Autoboxing: primitive → wrapper (Java does it for you) ───────────
        System.out.println("=== Autoboxing (primitive → wrapper) ===");

        int raw = 42;
        Integer boxed = raw;          // autoboxing — Java calls Integer.valueOf(42)
        System.out.println(boxed);    // 42

        // common place you see autoboxing — adding int to a List
        List<Integer> list = new ArrayList<>();
        list.add(10);                 // autoboxing: int 10 → Integer object
        list.add(20);
        list.add(30);
        System.out.println(list);     // [10, 20, 30]

        // ── Unboxing: wrapper → primitive (Java does it for you) ─────────────
        System.out.println("\n=== Unboxing (wrapper → primitive) ===");

        Integer wrapped = 99;
        int unwrapped = wrapped;           // unboxing — Java calls wrapped.intValue()
        System.out.println(unwrapped);     // 99

        // common place you see unboxing — reading from a list into an int
        int first = list.get(0);           // unboxing: Integer → int
        System.out.println("first: " + first); // 10

        // arithmetic also triggers unboxing
        Integer a = 10;
        Integer b = 20;
        int sum = a + b;               // both unboxed to int before adding
        System.out.println("sum: " + sum); // 30

        // ── The null trap — why null + unboxing = crash ───────────────────────
        System.out.println("\n=== Null trap ===");

        // Integer CAN hold null — it's an object
        Integer maybeNull = null;
        System.out.println("Integer null: " + maybeNull); // null — fine

        // unboxing null crashes at runtime
        try {
            System.out.println(maybeNull + 0);  // force unboxing — NPE before result prints
        } catch (NullPointerException e) {
            System.out.println("NPE caught — can't unbox null into int");
        }

        // real-world version of this bug: map returns null for missing key
        Map<String, Integer> scores = new HashMap<>();
        scores.put("Alice", 95);

        // WRONG — if key missing, get() returns null → unboxing → NPE
        try {
            System.out.println(scores.get("Bob") + 0);  // force unboxing — NPE
        } catch (NullPointerException e) {
            System.out.println("NPE: Bob not in map, get() returned null");
        }

        // RIGHT — use getOrDefault to avoid null
        int bobScore = scores.getOrDefault("Bob", 0);  // ✅ returns 0 if missing
        System.out.println("Bob score (safe): " + bobScore); // 0

        // ── Why Function<String, Integer> not Function<String, int> ──────────
        System.out.println("\n=== Generics need wrappers, not primitives ===");

        // int is a primitive — Java generics don't accept primitives
        // Function<String, int>     ← won't compile
        // Function<String, Integer> ← compiles — Integer is an object

        // this is the same reason List<Integer> not List<int>
        // Map<Integer, Integer> not Map<int, int>

        // autoboxing makes it seamless — you write int values, Java boxes them
        Map<Integer, Integer> freq = new HashMap<>();
        for (int n : new int[]{1, 2, 2, 3, 1, 1}) {
            freq.put(n, freq.getOrDefault(n, 0) + 1);
            // n is int    → autoboxed to Integer as map key
            // getOrDefault returns Integer → unboxed to int for +1
            // result int  → autoboxed back to Integer as map value
        }
        System.out.println("frequency map: " + freq); // {1=3, 2=2, 3=1}
    }
}
