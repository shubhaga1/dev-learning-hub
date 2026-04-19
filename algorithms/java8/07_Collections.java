/**
 * COLLECTIONS — Java 8+ Patterns
 *
 * Key interfaces:
 *   List   → ordered, duplicates allowed   (ArrayList, LinkedList)
 *   Set    → no duplicates                 (HashSet, LinkedHashSet, TreeSet)
 *   Map    → key-value pairs               (HashMap, LinkedHashMap, TreeMap)
 *   Queue  → FIFO                          (ArrayDeque, PriorityQueue)
 *   Deque  → both ends                     (ArrayDeque)
 *
 * Java 8 additions:
 *   Map.getOrDefault, computeIfAbsent, merge, forEach, replaceAll
 *   List.of, Set.of, Map.of (immutable, Java 9+)
 *   removeIf, sort with lambda
 */
import java.util.*;
import java.util.stream.*;

class Collections7 {

    public static void main(String[] args) {

        // ── List ──────────────────────────────────────────────────────────────
        List<String> list = new ArrayList<>(List.of("c", "a", "b", "a"));
        list.sort(Comparator.naturalOrder());            // [a, a, b, c]
        list.removeIf(s -> s.equals("a"));              // [b, c]
        list.replaceAll(String::toUpperCase);            // [B, C]
        System.out.println("List: " + list);

        // ── Set — no duplicates ───────────────────────────────────────────────
        Set<Integer> hashSet   = new HashSet<>(List.of(3, 1, 4, 1, 5));  // unordered, no dups
        Set<Integer> treeSet   = new TreeSet<>(hashSet);                   // sorted
        Set<Integer> linkedSet = new LinkedHashSet<>(List.of(3, 1, 4, 1, 5)); // insertion order
        System.out.println("HashSet:       " + hashSet);    // order varies
        System.out.println("TreeSet:       " + treeSet);    // [1, 3, 4, 5]
        System.out.println("LinkedHashSet: " + linkedSet);  // [3, 1, 4, 5]

        // ── Map patterns ──────────────────────────────────────────────────────
        Map<String, Integer> freq = new HashMap<>();
        String[] words = {"apple","banana","apple","cherry","banana","apple"};

        // Frequency counter — Java 8 style
        for (String w : words) {
            freq.merge(w, 1, Integer::sum);  // if absent put 1, else add 1
        }
        System.out.println("Frequency: " + freq);  // {apple=3, banana=2, cherry=1}

        // getOrDefault — no NPE on missing key
        System.out.println("Date count: " + freq.getOrDefault("date", 0));  // 0

        // computeIfAbsent — build value lazily (used in graph adjacency lists)
        Map<String, List<String>> graph = new HashMap<>();
        graph.computeIfAbsent("A", k -> new ArrayList<>()).add("B");
        graph.computeIfAbsent("A", k -> new ArrayList<>()).add("C");
        graph.computeIfAbsent("B", k -> new ArrayList<>()).add("D");
        System.out.println("Graph: " + graph);  // {A=[B, C], B=[D]}

        // forEach
        freq.forEach((k, v) -> System.out.println(k + " → " + v));

        // sorted by value descending
        freq.entrySet().stream()
            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
            .forEach(e -> System.out.println(e.getKey() + ": " + e.getValue()));

        // ── PriorityQueue — min-heap by default ──────────────────────────────
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.addAll(List.of(5, 1, 3, 2, 4));
        System.out.print("Min-heap poll order: ");
        while (!minHeap.isEmpty()) System.out.print(minHeap.poll() + " ");  // 1 2 3 4 5

        // max-heap
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
        maxHeap.addAll(List.of(5, 1, 3, 2, 4));
        System.out.print("\nMax-heap poll order: ");
        while (!maxHeap.isEmpty()) System.out.print(maxHeap.poll() + " ");  // 5 4 3 2 1

        // ── Deque — stack and queue in one ────────────────────────────────────
        Deque<String> deque = new ArrayDeque<>();
        deque.push("first");   // add to front (stack push)
        deque.push("second");
        deque.offer("last");   // add to back (queue offer)
        System.out.println("\nDeque: " + deque);   // [second, first, last]
        System.out.println("peek front: " + deque.peekFirst());  // second
        System.out.println("peek back:  " + deque.peekLast());   // last
    }
}
