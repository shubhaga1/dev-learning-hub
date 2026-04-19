package dfs;

import java.util.*;

/**
 * DFS 2/4 — DIRECTED GRAPH + isVisited (recursive)
 *
 * Why directed graphs NEED visited:
 *   In a tree every node has exactly one parent → only one path to reach it.
 *   In a directed graph the same node can be reached via MULTIPLE paths.
 *   Without visited, you'd process that node once per path — wrong output + infinite loop on cycles.
 *
 * Graph used (adjacency list):
 *
 *   a ──→ b ──→ d
 *         │     ↑
 *         ↓     │
 *         c ────┘
 *
 *   a → [b]
 *   b → [c, d]    ← b can reach d directly AND via c
 *   c → [d]       ← c also points to d
 *   d → []        ← sink node (no outgoing edges)
 *
 * Without visited: d would be processed TWICE (once via b→c→d, once via b→d).
 * With    visited: second attempt to enter d is blocked.
 *
 * Expected DFS order from "a": a b c d
 */
class DirectedGraphDFS {

    // Public entry point — hides the visited set from callers
    static List<String> dfs(String start, Map<String, List<String>> graph) {
        return dfs(start, graph, new HashSet<>());
    }

    // Private recursive worker
    private static List<String> dfs(String node, Map<String, List<String>> graph, Set<String> visited) {
        if (visited.contains(node)) return new ArrayList<>(); // already explored — skip

        visited.add(node);   // mark BEFORE visiting neighbours — blocks re-entry via other paths

        List<String> result = new ArrayList<>();
        result.add(node);    // record this node

        // visit each neighbour in order
        for (String neighbour : graph.getOrDefault(node, Collections.emptyList())) {
            result.addAll(dfs(neighbour, graph, visited));
        }

        return result;
        // ← backtrack: call returns, caller continues with next neighbour
    }

    public static void main(String[] args) {
        // Build directed graph as adjacency list
        Map<String, List<String>> graph = new HashMap<>();
        graph.put("a", Arrays.asList("b"));
        graph.put("b", Arrays.asList("c", "d")); // b → c and b → d
        graph.put("c", Arrays.asList("d"));       // c → d  (d reachable from 2 paths)
        graph.put("d", Collections.emptyList());  // sink

        System.out.println("DFS from a : " + dfs("a", graph));  // [a, b, c, d]

        // ── What happens at node d ──────────────────────────────────────────
        System.out.println("""

          Trace (visited set shown after each step):

          dfs(a)  visited={a}
            dfs(b)  visited={a,b}
              dfs(c)  visited={a,b,c}
                dfs(d)  visited={a,b,c,d}   ← d added here
                ← return [d]
              ← return [c, d]
              dfs(d)  → visited.contains(d) = true → SKIP  ← key line
            ← return [b, c, d]
          ← return [a, b, c, d]

          Without visited: d would appear twice → [a, b, c, d, d]
          """);

        // ── Cycle example — visited prevents infinite loop ──────────────────
        Map<String, List<String>> cyclic = new HashMap<>();
        cyclic.put("x", Arrays.asList("y"));
        cyclic.put("y", Arrays.asList("z"));
        cyclic.put("z", Arrays.asList("x")); // cycle: x→y→z→x

        System.out.println("DFS on cycle (x→y→z→x) : " + dfs("x", cyclic)); // [x, y, z]
        // Without visited this would recurse forever (stack overflow)
    }
}
