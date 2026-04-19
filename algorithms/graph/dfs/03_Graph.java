package dfs;

import java.util.*;

/**
 * DFS 3/4 — DFS ON A GRAPH (not a tree)
 *
 * KEY DIFFERENCE from tree DFS:
 *   Tree  → no cycles → no visited set needed
 *   Graph → CAN have cycles → MUST track visited nodes
 *
 *   Without visited set on a graph:
 *     1 → 2 → 1 → 2 → 1 ... infinite loop
 *
 * Graph used:
 *   1 — 2 — 5
 *   |       |
 *   3 — 4 — 6
 *
 * Adjacency list (undirected — each edge stored both ways):
 *   1 → [2, 3]
 *   2 → [1, 5]
 *   3 → [1, 4]
 *   4 → [3, 6]
 *   5 → [2, 6]
 *   6 → [4, 5]
 */
class DFSGraph {

    static Map<Integer, List<Integer>> buildGraph() {
        Map<Integer, List<Integer>> graph = new HashMap<>();
        int[][] edges = {{1,2},{1,3},{2,5},{3,4},{4,6},{5,6}};
        for (int[] e : edges) {
            graph.computeIfAbsent(e[0], k -> new ArrayList<>()).add(e[1]);
            graph.computeIfAbsent(e[1], k -> new ArrayList<>()).add(e[0]);
        }
        return graph;
    }

    // ── Recursive — visited set prevents infinite loop ────────────────────────
    static void dfsRecursive(Map<Integer, List<Integer>> graph,
                              int node, Set<Integer> visited) {
        visited.add(node);
        System.out.print(node + " ");

        for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
            if (!visited.contains(neighbor)) {
                dfsRecursive(graph, neighbor, visited);
            }
        }
    }

    // ── Iterative — same visited set logic, explicit stack ────────────────────
    static void dfsIterative(Map<Integer, List<Integer>> graph, int start) {
        Set<Integer>   visited = new HashSet<>();
        Stack<Integer> stack   = new Stack<>();
        stack.push(start);

        while (!stack.isEmpty()) {
            int node = stack.pop();
            if (visited.contains(node)) continue;  // already seen — skip
            visited.add(node);
            System.out.print(node + " ");

            for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
                if (!visited.contains(neighbor)) stack.push(neighbor);
            }
        }
    }

    public static void main(String[] args) {
        Map<Integer, List<Integer>> graph = buildGraph();

        System.out.print("Recursive: ");
        dfsRecursive(graph, 1, new HashSet<>());
        System.out.println();

        System.out.print("Iterative: ");
        dfsIterative(graph, 1);
        System.out.println();

        // ── Why visited set is critical ───────────────────────────────────────
        System.out.println("""
          Without visited set on graph (edge 1—2):
            visit 1 → push 2
            visit 2 → push 1   ← 1 already seen!
            visit 1 → push 2   ← infinite loop

          With visited set:
            visit 1 → mark visited → push neighbors 2, 3
            visit 2 → mark visited → push neighbor 5 (1 already visited → skip)
            visit 5 → mark visited → push neighbor 6 (2 already visited → skip)
            ...no revisits → terminates correctly
          """);
    }
}
