package dfs;

import java.util.*;

/**
 * DFS 3/4 — CYCLE DETECTION in a Directed Graph
 *
 * WHY visited alone is NOT enough for cycle detection:
 *
 *   graph:  a → b,  c → b   (no cycle — b reachable from two nodes)
 *
 *   DFS from a: visit a, visit b (mark visited), done.
 *   DFS from c: visit c, try b → visited! → if we return true here, FALSE POSITIVE.
 *
 *   visited = "we've been here before in any DFS call"
 *   That is NOT a cycle — b was just reachable from two different sources.
 *
 * WHAT you actually need — TWO sets:
 *
 *   visited  = nodes fully explored (DFS subtree complete)
 *   inStack  = nodes on the CURRENT recursion path (ancestors in call stack)
 *
 *   A cycle exists when you reach a node that is ALREADY in inStack.
 *   That means there's a back edge → you found a loop.
 *
 * Visual:
 *   a → b → c → a     (cycle: a appears in inStack when reached from c)
 *             ↑
 *          back edge
 *
 *   inStack at that moment: {a, b, c}
 *   trying to visit a again → a in inStack → CYCLE DETECTED
 *
 * Color analogy (classic):
 *   WHITE = unvisited
 *   GRAY  = in inStack (currently being explored)
 *   BLACK = fully done (in visited, removed from inStack)
 *   Back edge = going from GRAY to GRAY → cycle
 */
class CycleDetectionDFS {

    // Public entry — checks all nodes (graph may be disconnected)
    static boolean hasCycle(Map<String, List<String>> graph) {
        Set<String> visited = new HashSet<>();
        Set<String> inStack = new HashSet<>();

        for (String node : graph.keySet()) {
            if (!visited.contains(node)) {                     // unvisited component
                if (dfs(node, graph, visited, inStack)) return true;
            }
        }
        return false;
    }

    // Returns true if a cycle is found starting from `node`
    private static boolean dfs(String node, Map<String, List<String>> graph,
                                Set<String> visited, Set<String> inStack) {

        visited.add(node);   // mark fully-visited (won't reprocess this component)
        inStack.add(node);   // mark on current path  ← entering this recursion frame

        for (String neighbour : graph.getOrDefault(node, Collections.emptyList())) {
            if (inStack.contains(neighbour)) return true;   // back edge → CYCLE
            if (!visited.contains(neighbour)) {             // unvisited → keep going
                if (dfs(neighbour, graph, visited, inStack)) return true;
            }
            // visited but NOT in inStack → already fully explored, safe to skip
        }

        inStack.remove(node);  // leaving this recursion frame → backtrack
        //                        ↑ critical: inStack only holds current PATH, not all visited
        return false;
    }

    public static void main(String[] args) {

        // ── Graph WITH cycle: a → b → c → a ─────────────────────────────────
        Map<String, List<String>> cyclic = new HashMap<>();
        cyclic.put("a", Arrays.asList("b"));
        cyclic.put("b", Arrays.asList("c"));
        cyclic.put("c", Arrays.asList("a"));   // back edge to a → cycle

        System.out.println("Cyclic graph (a→b→c→a) : " + hasCycle(cyclic));   // true

        // ── DAG — no cycle ───────────────────────────────────────────────────
        Map<String, List<String>> dag = new HashMap<>();
        dag.put("a", Arrays.asList("b", "c"));
        dag.put("b", Arrays.asList("d"));
        dag.put("c", Arrays.asList("d"));      // d reachable from both b and c — NOT a cycle
        dag.put("d", Collections.emptyList());

        System.out.println("DAG        (a→b→d, a→c→d) : " + hasCycle(dag));  // false

        // ── Trace for cyclic graph ────────────────────────────────────────────
        System.out.println("""

          Trace (cyclic graph a→b→c→a):

          dfs(a)  visited={a}  inStack={a}
            dfs(b)  visited={a,b}  inStack={a,b}
              dfs(c)  visited={a,b,c}  inStack={a,b,c}
                neighbour=a → inStack.contains(a) = true → CYCLE DETECTED ✓

          Trace (DAG a→b→d, a→c→d):

          dfs(a)  inStack={a}
            dfs(b)  inStack={a,b}
              dfs(d)  inStack={a,b,d}
              ← d done, inStack={a,b}
            ← b done, inStack={a}
            dfs(c)  inStack={a,c}
              neighbour=d → visited=true, inStack=false → skip (already fully explored)
            ← c done, inStack={a}
          ← a done, inStack={}   → no cycle found
          """);
    }
}
