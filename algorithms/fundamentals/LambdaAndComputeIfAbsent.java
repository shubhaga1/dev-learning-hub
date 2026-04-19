import java.util.*;
import java.util.function.*;

/**
 * LAMBDA + computeIfAbsent — two concepts, one file
 *
 * PART 1: Lambda — what it is
 *   A lambda is a short anonymous function you write inline.
 *   Instead of creating a whole method, you pass behavior as a value.
 *
 *   Syntax:  (parameters) -> body
 *
 * PART 2: computeIfAbsent — what it solves
 *   Map problem: before adding to a list inside a map,
 *   you must check if the key exists first.
 *   computeIfAbsent collapses that check into one line.
 */
class LambdaAndComputeIfAbsent {

    // ── PART 1: Lambda basics ─────────────────────────────────────────────────

    static void part1_lambda() {
        System.out.println("=== PART 1: Lambda ===");

        // Without lambda — you write a full anonymous class
        Runnable withoutLambda = new Runnable() {
            public void run() {
                System.out.println("hello from anonymous class");
            }
        };


        // With lambda — same thing, 1 line
        Runnable withLambda = () -> System.out.println("hello from lambda");

        withoutLambda.run();
        withLambda.run();

        // Lambda with parameter
        // Function<Input, Output> — takes one arg, returns one value
        Function<String, Integer> length = s -> s.length();
        System.out.println("length of 'hello' = " + length.apply("hello")); // 5

        // Lambda with two parameters
        // BiFunction<Input1, Input2, Output>
        BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
        System.out.println("3 + 4 = " + add.apply(3, 4)); // 7

        // The key insight:
        // k -> new ArrayList<>()
        //   k      = the parameter (the missing key)
        //   ->     = "produces"
        //   new ArrayList<>() = the value to create
        Function<Integer, List<Integer>> makeList = k -> new ArrayList<>();
        List<Integer> list = makeList.apply(99); // k=99, returns empty list
        System.out.println("makeList produced: " + list); // []
    }

    // ── PART 2: computeIfAbsent — manual vs shorthand ─────────────────────────

    static void part2_computeIfAbsent() {
        System.out.println("\n=== PART 2: computeIfAbsent ===");

        // Problem: building a map of node → list of neighbors
        // Each time we see a node, we need to add to its list.
        // But the list might not exist yet.

        // ── Manual way (verbose) ──────────────────────────────────────────────
        Map<Integer, List<Integer>> manual = new HashMap<>();

        int node = 1, neighbor = 2;

        if (!manual.containsKey(node)) {         // does key exist?
            manual.put(node, new ArrayList<>()); // no → create empty list
        }
        manual.get(node).add(neighbor);          // now safe to add

        System.out.println("manual result: " + manual); // {1=[2]}

        // ── computeIfAbsent way (same result) ─────────────────────────────────
        Map<Integer, List<Integer>> smart = new HashMap<>();

        // "if key 1 is absent, run the lambda to create the value"
        // returns the existing list OR the newly created one
        smart.computeIfAbsent(1, k -> new ArrayList<>()).add(2);

        System.out.println("smart  result: " + smart);  // {1=[2]}
        System.out.println("same?  " + manual.equals(smart)); // true
    }

    // ── PART 3: apply to the graph problem ───────────────────────────────────

    static void part3_graph() {
        System.out.println("\n=== PART 3: Building graph with computeIfAbsent ===");

        Map<Integer, List<Integer>> graph = new HashMap<>();
        int[][] edges = {{1,2},{1,3},{2,5},{3,4}};

        for (int[] e : edges) {
            // e[0]=from, e[1]=to
            // if from-node list missing → create it, then add to-node
            graph.computeIfAbsent(e[0], k -> new ArrayList<>()).add(e[1]);
            // same in reverse — undirected graph
            graph.computeIfAbsent(e[1], k -> new ArrayList<>()).add(e[0]);
        }

        // print each node and its neighbors
        for (Map.Entry<Integer, List<Integer>> entry : graph.entrySet()) {
            System.out.println("  node " + entry.getKey() + " → " + entry.getValue());
        }
    }

    public static void main(String[] args) {
        part1_lambda();
        part2_computeIfAbsent();
        part3_graph();
    }
}
