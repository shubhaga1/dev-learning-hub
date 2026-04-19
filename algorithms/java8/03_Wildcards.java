import java.util.*;
import java.util.function.*;

/**
 * WILDCARDS — ? extends T  and  ? super T
 *
 * The ? means "some unknown type". Two flavours:
 *
 *   ? extends T  =  T or any SUBCLASS of T   →  you can READ, not write
 *   ? super T    =  T or any SUPERCLASS of T  →  you can WRITE, not read
 *
 * Memory trick — PECS:
 *   Producer Extends  (you read/GET from it)
 *   Consumer Super    (you write/PUT into it)
 *
 * Real example from Map.computeIfAbsent:
 *   Function<? super K, ? extends V> mappingFunction
 *          └─ accepts K or parent     └─ returns V or subclass
 *
 * Run: javac 03_Wildcards.java && java Wildcards
 */
class Wildcards {

    // Type hierarchy used in examples:
    //   Animal → Dog → GoldenRetriever
    //   Animal → Cat
    static class Animal  { String name() { return "Animal"; } }
    static class Dog extends Animal { String name() { return "Dog"; } }
    static class GoldenRetriever extends Dog { String name() { return "GoldenRetriever"; } }
    static class Cat extends Animal { String name() { return "Cat"; } }

    // ─── 1. No wildcard — rigid ───────────────────────────────────────────────
    static void noWildcard() {
        System.out.println("=== 1. NO WILDCARD — rigid ===");

        List<Dog> dogs = new ArrayList<>();
        dogs.add(new Dog());

        // List<Animal> animals = dogs;  // ❌ COMPILE ERROR — even though Dog IS-A Animal
        // This is correct — if allowed, you could add a Cat to a Dog list via the Animal ref

        List<Dog> exactDogs = dogs;     // ✅ only exact type matches
        System.out.println("Rigid: only List<Dog> = List<Dog>");
    }

    // ─── 2. ? extends — read-only, accepts T and subclasses ──────────────────
    // "I will READ animals from this list — give me a list of Animal or subclass"
    static double averageWeight(List<? extends Animal> animals) {
        // ✅ Can READ — guaranteed to be Animal or subclass
        for (Animal a : animals) {
            System.out.println("  Reading: " + a.name());
        }

        // ❌ Cannot WRITE — compiler doesn't know exact type
        // animals.add(new Dog());   // COMPILE ERROR
        // animals.add(new Animal()); // COMPILE ERROR
        // (what if caller passed List<Cat>? Can't add a Dog to it)

        return 10.0; // placeholder
    }

    // ─── 3. ? super — write-allowed, accepts T and superclasses ─────────────
    // "I will ADD dogs into this list — give me a list of Dog or superclass"
    static void addDogs(List<? super Dog> list) {
        // ✅ Can WRITE Dog (or subclass) — guaranteed list accepts Dog
        list.add(new Dog());
        list.add(new GoldenRetriever()); // GoldenRetriever IS-A Dog — ok

        // ❌ Cannot READ as specific type — only Object guaranteed
        // Dog d = list.get(0);    // COMPILE ERROR — might be List<Animal> or List<Object>
        Object o = list.get(0);    // ✅ Object always works
        System.out.println("  Added and read as Object: " + o.getClass().getSimpleName());
    }

    // ─── 4. computeIfAbsent explained — the real thing ───────────────────────
    // V computeIfAbsent(K key, Function<? super K, ? extends V> mappingFunction)
    //
    // Function<? super K, ? extends V>
    //   → Input:  accepts K or any PARENT of K   (flexible input)
    //   → Output: returns V or any SUBCLASS of V (flexible output)
    //
    // Why ? super K for input?
    //   If K is String, you can pass Function<Object, ...> — works for any key type
    //
    // Why ? extends V for output?
    //   If V is Number, you can pass Function<..., Integer> — Integer IS-A Number
    static void computeIfAbsentExplained() {
        System.out.println("\n=== 4. computeIfAbsent — wildcards in action ===");

        Map<String, List<Integer>> graph = new HashMap<>();

        // The lambda:  k -> new ArrayList<>()
        //   k    = the key (String) passed in if missing
        //   k -> new ArrayList<>()  is a Function<String, ArrayList<Integer>>
        //
        // Why does Function<String, ArrayList<Integer>> satisfy
        //         Function<? super String, ? extends List<Integer>> ?
        //   String IS String          → satisfies ? super String   ✅
        //   ArrayList IS-A List       → satisfies ? extends List   ✅

        graph.computeIfAbsent("node1", k -> new ArrayList<>()).add(42);
        graph.computeIfAbsent("node1", k -> new ArrayList<>()).add(99); // key exists, uses existing list
        graph.computeIfAbsent("node2", k -> new ArrayList<>()).add(7);

        System.out.println("graph: " + graph);

        // Equivalent without computeIfAbsent:
        Map<String, List<Integer>> manual = new HashMap<>();
        String key = "node1";
        if (!manual.containsKey(key)) {
            manual.put(key, new ArrayList<>());
        }
        manual.get(key).add(42);
        System.out.println("manual: " + manual);
    }

    // ─── 5. PECS rule summary with examples ──────────────────────────────────
    static void pecsExamples() {
        System.out.println("\n=== 5. PECS — Producer Extends, Consumer Super ===");

        List<GoldenRetriever> goldens = new ArrayList<>();
        goldens.add(new GoldenRetriever());

        List<Animal> animals = new ArrayList<>();
        List<Object> objects = new ArrayList<>();

        // PRODUCER (you read from it) → use extends
        // "This list produces Animals for me to read"
        averageWeight(goldens);    // ✅ GoldenRetriever extends Animal
        averageWeight(animals);    // ✅ Animal extends Animal (itself)
        // averageWeight(objects); // ❌ Object doesn't extend Animal

        // CONSUMER (you write into it) → use super
        // "This list consumes Dogs — I'll add Dogs into it"
        // addDogs(goldens);  // ❌ COMPILE ERROR — GoldenRetriever is subtype not supertype of Dog
        addDogs(animals);  // ✅ Animal is super of Dog — you can add Dog to Animal list
        addDogs(objects);  // ✅ Object is super of Dog — you can add Dog to Object list

        System.out.println("""
          ? extends T  (Producer Extends):
            ✅ List<Dog>, List<GoldenRetriever> satisfy List<? extends Animal>
            ✅ Read as Animal
            ❌ Cannot add anything (except null)

          ? super T  (Consumer Super):
            ✅ List<Animal>, List<Object> satisfy List<? super Dog>
            ✅ Add Dog or GoldenRetriever
            ❌ Read only as Object
        """);
    }

    // ─── 6. Unbounded wildcard <?> ───────────────────────────────────────────
    static void printList(List<?> list) {
        // ? = any type — most flexible, but can only read as Object
        for (Object item : list) {
            System.out.print(item + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        noWildcard();

        System.out.println("\n=== 2. ? extends — read from list ===");
        List<GoldenRetriever> goldens = List.of(new GoldenRetriever(), new GoldenRetriever());
        averageWeight(goldens);

        System.out.println("\n=== 3. ? super — write into list ===");
        List<Animal> animals = new ArrayList<>();
        addDogs(animals);

        computeIfAbsentExplained();
        pecsExamples();

        System.out.println("=== 6. Unbounded <?> ===");
        printList(List.of(1, 2, 3));
        printList(List.of("a", "b", "c"));
        printList(goldens);

        System.out.println("""
        SUMMARY:
          List<Dog>            exact — only Dog
          List<? extends Dog>  Dog or subclass — read-only
          List<? super Dog>    Dog or superclass — write Dog into it
          List<?>              anything — read-only as Object

          computeIfAbsent key rule:
            Function<? super K, ? extends V>
              ? super K  = accept K or broader type as INPUT  (flexible caller)
              ? extends V = return V or narrower type as OUTPUT (flexible return)
        """);
    }
}
