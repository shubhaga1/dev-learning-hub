import java.util.*;
import java.util.function.*;

/**
 * WHY ? super K AND ? extends V — instead of just K and V
 *
 * Short answer:
 *   Using K and V directly = RIGID — only exact type accepted
 *   Using wildcards        = FLEXIBLE — accepts related types too
 *
 * This file shows exactly what BREAKS when you use K/V directly
 * and WHY the wildcard version is more useful.
 *
 * Run: javac 04_WhyWildcards.java && java WhyWildcards
 */
class WhyWildcards {

    // Type hierarchy:
    //   Object → Animal → Dog → GoldenRetriever
    static class Animal  { public String toString() { return "Animal"; } }
    static class Dog extends Animal { public String toString() { return "Dog"; } }
    static class GoldenRetriever extends Dog { public String toString() { return "Golden"; } }

    // ─── SCENARIO: Map.computeIfAbsent ───────────────────────────────────────
    // Real signature:  V computeIfAbsent(K key, Function<? super K, ? extends V> fn)
    // Simplified:
    //   Version A — rigid:    Function<K, V>              ← what if we used K and V directly
    //   Version B — flexible: Function<? super K, ? extends V>  ← actual Java
    //
    // Let's build BOTH and see what breaks with Version A

    // ─── VERSION A: rigid Function<K, V> ────────────────────────────────────
    static <K, V> V computeRigid(Map<K, V> map, K key, Function<K, V> fn) {
        if (!map.containsKey(key)) {
            map.put(key, fn.apply(key));
        }
        return map.get(key);
    }

    // ─── VERSION B: flexible Function<? super K, ? extends V> ────────────────
    static <K, V> V computeFlexible(Map<K, V> map, K key, Function<? super K, ? extends V> fn) {
        if (!map.containsKey(key)) {
            map.put(key, fn.apply(key));
        }
        return map.get(key);
    }

    // ─── 1. Basic case — both work the same ──────────────────────────────────
    static void basicCase() {
        System.out.println("=== 1. BASIC CASE — both work ===");

        Map<String, List<Integer>> map1 = new HashMap<>();
        Map<String, List<Integer>> map2 = new HashMap<>();

        // Rigid — works here because types match exactly
        computeRigid(map1, "a", k -> new ArrayList<>());
        map1.get("a").add(1);
        System.out.println("Rigid:    " + map1);

        // Flexible — also works
        computeFlexible(map2, "a", k -> new ArrayList<>());
        map2.get("a").add(1);
        System.out.println("Flexible: " + map2);
    }

    // ─── 2. ? extends V — why it matters ─────────────────────────────────────
    // Map<String, List<Integer>>  → V = List<Integer>
    // Lambda returns ArrayList<Integer>  → ArrayList IS-A List
    //
    // Rigid Function<K, V> = Function<String, List<Integer>>
    //   → lambda must return exactly List<Integer>
    //
    // Flexible Function<? super K, ? extends V> = Function<?, ? extends List<Integer>>
    //   → lambda can return ArrayList<Integer>, LinkedList<Integer>, any subclass
    static void extendsVDemo() {
        System.out.println("\n=== 2. ? extends V — return a SUBCLASS of V ===");

        Map<String, List<Integer>> map = new HashMap<>();

        // ✅ Flexible: lambda returns ArrayList — which extends List
        computeFlexible(map, "nums", k -> new ArrayList<Integer>());
        //                                      ↑ ArrayList<Integer> satisfies ? extends List<Integer>

        // With rigid, this ALSO compiles in this case because Java infers the types.
        // But watch what happens with a more specific return type:

        // Imagine you have a method that returns a specialized list:
        Function<String, ArrayList<Integer>> specialFn = k -> {
            ArrayList<Integer> list = new ArrayList<>();
            list.add(42);
            return list;
        };

        // Rigid:    computeRigid(map, "x", specialFn);    // ❌ COMPILE ERROR
        //           expected Function<String, List<Integer>>
        //           got     Function<String, ArrayList<Integer>>

        // Flexible: ✅ works — ArrayList IS-A List, ? extends List accepts it
        computeFlexible(map, "x", specialFn);

        System.out.println("Flexible accepts ArrayList<> for List<> slot: " + map);
        System.out.println("→ ? extends V = 'return V or anything more specific'");
    }

    // ─── 3. ? super K — why it matters ───────────────────────────────────────
    // Map<Dog, String>  → K = Dog
    //
    // Rigid Function<K, V> = Function<Dog, String>
    //   → lambda input MUST be Dog
    //
    // Flexible Function<? super K, ...> = Function<? super Dog, ...>
    //   → lambda input can be Dog OR Animal OR Object
    //   → this means you can reuse a general-purpose lambda for many map types
    static void superKDemo() {
        System.out.println("\n=== 3. ? super K — pass a MORE GENERAL function ===");

        Map<Dog, String> dogMap = new HashMap<>();

        // A general function that works on ANY Animal
        Function<Animal, String> describeAnimal = a -> "Described: " + a.toString();

        // Rigid:    computeRigid(dogMap, new Dog(), describeAnimal);
        //           ❌ COMPILE ERROR: expected Function<Dog, String>
        //                             got     Function<Animal, String>
        //           Even though Animal is broader and can handle Dog!

        // Flexible: ✅ ? super Dog accepts Function<Animal,...> and Function<Object,...>
        computeFlexible(dogMap, new Dog(), describeAnimal);
        computeFlexible(dogMap, new GoldenRetriever(), describeAnimal); // GoldenRetriever IS-A Dog, works as K

        System.out.println("dogMap: " + dogMap);
        System.out.println("→ ? super K = 'accept a function that handles K or anything broader'");

        // Why is this useful? Reuse one function across multiple map types:
        Map<GoldenRetriever, String> goldenMap = new HashMap<>();
        Function<Object, String> toStringFn = obj -> "obj:" + obj;

        // toStringFn works for any key type — reusable
        computeFlexible(goldenMap, new GoldenRetriever(), toStringFn);
        computeFlexible(dogMap,    new Dog(),             toStringFn);
        System.out.println("Reused same Function<Object,String> on two different maps: ✅");
    }

    // ─── 4. Side by side — rigid vs flexible ─────────────────────────────────
    static void sideBySide() {
        System.out.println("\n=== 4. SIDE BY SIDE — what each rejects ===");

        Map<Dog, List<Integer>> map = new HashMap<>();

        Function<Dog,    ArrayList<Integer>> exact    = d -> new ArrayList<>(); // exact types
        Function<Animal, ArrayList<Integer>> broaderK = a -> new ArrayList<>(); // broader K
        Function<Dog,    ArrayList<Integer>> subV     = d -> new ArrayList<>(); // sub of V (ArrayList < List)
        Function<Animal, ArrayList<Integer>> both     = a -> new ArrayList<>(); // broader K + sub V

        System.out.println("Testing Function against computeRigid(Map<Dog,List<Integer>>):");
        System.out.println("  Function<Dog,    ArrayList<Integer>> exact    → ✅ works (exact match for K, ArrayList inferred as List)");
        // computeRigid(map, new Dog(), exact);    ← actually works because of type inference

        System.out.println("  Function<Animal, ArrayList<Integer>> broaderK → ❌ rigid rejects broader input");
        System.out.println("  Function<Dog,    ArrayList<Integer>> subV      → ❌ rigid rejects subtype return");
        System.out.println("  Function<Animal, ArrayList<Integer>> both      → ❌ rigid rejects both");

        System.out.println("\nTesting against computeFlexible(Map<Dog,List<Integer>>):");
        computeFlexible(map, new Dog(), exact);
        computeFlexible(map, new Dog(), broaderK);  // ✅ ? super Dog accepts Animal
        computeFlexible(map, new Dog(), subV);       // ✅ ? extends List accepts ArrayList
        computeFlexible(map, new Dog(), both);       // ✅ both wildcards together
        System.out.println("  All 4 variants accepted by flexible version ✅");
    }

    // ─── 5. Real world — why this matters in practice ─────────────────────────
    static void realWorld() {
        System.out.println("\n=== 5. REAL WORLD — building a graph ===");

        Map<Integer, List<Integer>> graph = new HashMap<>();

        // The lambda  k -> new ArrayList<>()  returns ArrayList, not List
        // That's why computeIfAbsent needs ? extends V — to accept ArrayList for List slot
        int[] nodes = {1, 2, 3, 4, 5};
        int[][] edges = {{1,2}, {1,4}, {2,3}, {3,4}, {4,5}};

        for (int[] e : edges) {
            // Two computeIfAbsent calls — one per direction (undirected graph)
            graph.computeIfAbsent(e[0], k -> new ArrayList<>()).add(e[1]);
            graph.computeIfAbsent(e[1], k -> new ArrayList<>()).add(e[0]);
        }

        System.out.println("Graph adjacency list:");
        for (int node : nodes) {
            System.out.println("  " + node + " → " + graph.getOrDefault(node, List.of()));
        }

        // k -> new ArrayList<>()
        // k  = the missing key passed to you (you can use it or ignore it)
        // -> new ArrayList<>()  = what to store as value when key is absent
        System.out.println("\nLambda breakdown: k -> new ArrayList<>()");
        System.out.println("  k           = the key (Integer) — passed in but not used here");
        System.out.println("  new ArrayList<>() = value to insert when key missing");
        System.out.println("  Returns ArrayList — satisfies ? extends List because ArrayList IS-A List");
    }

    public static void main(String[] args) {
        basicCase();
        extendsVDemo();
        superKDemo();
        sideBySide();
        realWorld();

        System.out.println("""

        FINAL SUMMARY:
        ┌─────────────────────────────────────────────────────────────────┐
        │  Function<K, V>                 RIGID                           │
        │    → lambda input  must be exactly K                            │
        │    → lambda output must be exactly V                            │
        │                                                                 │
        │  Function<? super K, ? extends V>  FLEXIBLE                    │
        │    ? super K  → lambda can accept K, Animal, Object (broader)   │
        │    ? extends V → lambda can return ArrayList, LinkedList (sub)  │
        │                                                                 │
        │  Why Java chose flexible:                                       │
        │    Reuse one Function across many map types                     │
        │    Return specific subclass (ArrayList) for abstract slot (List)│
        └─────────────────────────────────────────────────────────────────┘
        """);
    }
}
