/**
 * STREAMS — Java 8
 *
 * Stream = pipeline of operations on a collection.
 * Does NOT modify the original collection.
 * Lazy: intermediate ops run only when terminal op is called.
 *
 * Pipeline:
 *   Source        → filter/map/sorted (intermediate, lazy)
 *                 → collect/count/reduce (terminal, triggers execution)
 *
 * Intermediate:  filter, map, flatMap, sorted, distinct, limit, skip, peek
 * Terminal:      collect, count, reduce, forEach, findFirst, anyMatch, toList
 */
import java.util.*;
import java.util.stream.*;

class Streams {

    public static void main(String[] args) {

        List<String> names = List.of("Alice", "Bob", "Charlie", "Diana", "Eve", "Alice");

        // ── filter + map + collect ────────────────────────────────────────────
        List<String> result = names.stream()
            .filter(n -> n.length() > 3)         // keep names longer than 3
            .map(String::toUpperCase)             // ALICE, CHARLIE, DIANA
            .distinct()                           // remove duplicates
            .sorted()                             // alphabetical
            .collect(Collectors.toList());

        System.out.println("Filtered & mapped: " + result);
        // [ALICE, CHARLIE, DIANA]

        // ── count ─────────────────────────────────────────────────────────────
        long count = names.stream().filter(n -> n.startsWith("A")).count();
        System.out.println("Names starting with A: " + count);  // 2 (Alice appears twice)

        // ── reduce — aggregate to single value ────────────────────────────────
        List<Integer> nums = List.of(1, 2, 3, 4, 5);
        int sum = nums.stream().reduce(0, Integer::sum);
        System.out.println("Sum: " + sum);  // 15

        // ── groupingBy — like SQL GROUP BY ────────────────────────────────────
        List<String> words = List.of("apple", "ant", "banana", "avocado", "blueberry");
        Map<Character, List<String>> grouped = words.stream()
            .collect(Collectors.groupingBy(w -> w.charAt(0)));
        System.out.println("Grouped by first letter: " + grouped);
        // {a=[apple, ant, avocado], b=[banana, blueberry]}

        // ── flatMap — flatten nested lists ────────────────────────────────────
        List<List<Integer>> nested = List.of(List.of(1,2), List.of(3,4), List.of(5));
        List<Integer> flat = nested.stream()
            .flatMap(Collection::stream)
            .collect(Collectors.toList());
        System.out.println("Flattened: " + flat);  // [1, 2, 3, 4, 5]

        // ── anyMatch / allMatch / noneMatch ───────────────────────────────────
        boolean anyLong  = names.stream().anyMatch(n -> n.length() > 6);  // true (Charlie)
        boolean allShort = names.stream().allMatch(n -> n.length() < 10); // true
        System.out.println("Any name > 6 chars: " + anyLong);
        System.out.println("All names < 10 chars: " + allShort);

        // ── min / max ─────────────────────────────────────────────────────────
        Optional<String> shortest = names.stream().min(Comparator.comparingInt(String::length));
        System.out.println("Shortest name: " + shortest.orElse("none"));  // Bob

        // ── joining — like String.join but via stream ─────────────────────────
        String joined = names.stream().distinct().collect(Collectors.joining(", ", "[", "]"));
        System.out.println("Joined: " + joined);  // [Alice, Bob, Charlie, Diana, Eve]

        // ── Stream.of, IntStream, range ───────────────────────────────────────
        int sumRange = IntStream.rangeClosed(1, 100).sum();  // 1+2+...+100
        System.out.println("Sum 1 to 100: " + sumRange);    // 5050

        // ── peek — debug without breaking chain ───────────────────────────────
        List<String> debugResult = names.stream()
            .peek(n -> System.out.print("before: " + n + " "))
            .filter(n -> n.length() > 3)
            .peek(n -> System.out.print("after: " + n + " "))
            .collect(Collectors.toList());
        System.out.println();
    }
}
