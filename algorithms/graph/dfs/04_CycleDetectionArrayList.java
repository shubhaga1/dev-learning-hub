package dfs;

import java.util.*;

/**
 * DFS 4/4 — CYCLE DETECTION using ArrayList adjacency list (integer nodes)
 *
 * Same logic as 03_CycleDetectionDFS.java but graph is represented as:
 *   List<List<Integer>> adj   — index = node, value = list of neighbours
 *
 * This is the standard LeetCode / competitive programming format.
 *
 * Graph (5 nodes, 0-indexed):
 *
 *   0 → 1 → 3
 *   |       ↑
 *   ↓       |
 *   2 ──────┘    ← no cycle (DAG)
 *
 *   Cyclic version adds edge: 3 → 0  (back to start)
 *
 * Two sets (same idea as HashMap version):
 *   visited[]  — node fully explored
 *   inStack[]  — node on current DFS path
 *   Using boolean[] instead of HashSet — faster for integer nodes
 */
class CycleDetectionArrayList {

    static int n; // number of nodes
    static List<List<Integer>> adj;

    // Build adjacency list
    static void buildGraph(int nodes, int[][] edges) {
        n = nodes;
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

        for (int[] edge : edges) {
            adj.get(edge[0]).add(edge[1]); // directed: edge[0] → edge[1]
        }
    }

    // Public entry — iterates all nodes to handle disconnected graphs
    static boolean hasCycle() {
        boolean[] visited = new boolean[n];
        boolean[] inStack = new boolean[n];

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                if (dfs(i, visited, inStack)) return true;
            }
        }
        return false;
    }

    private static boolean dfs(int node, boolean[] visited, boolean[] inStack) {
        visited[node] = true;   // mark fully visited
        inStack[node] = true;   // mark on current path ← entering this frame

        for (int neighbour : adj.get(node)) {
            if (inStack[neighbour]) return true;    // back edge → CYCLE
            if (!visited[neighbour]) {              // unvisited → go deeper
                if (dfs(neighbour, visited, inStack)) return true;
            }
            // visited + not inStack → already fully explored, skip
        }

        inStack[node] = false;  // leaving this frame → backtrack
        return false;
    }

    public static void main(String[] args) {

        // ── DAG — no cycle ───────────────────────────────────────────────────
        //   0→1, 0→2, 1→3, 2→3
        buildGraph(4, new int[][]{{0,1},{0,2},{1,3},{2,3}});
        System.out.println("DAG  (0→1→3, 0→2→3) : " + hasCycle()); // false

        // ── Cyclic — add back edge 3→0 ───────────────────────────────────────
        //   0→1, 1→3, 3→0  (cycle)
        buildGraph(4, new int[][]{{0,1},{0,2},{1,3},{2,3},{3,0}});
        System.out.println("Cyclic (+ edge 3→0) : " + hasCycle()); // true

        // ── Trace ─────────────────────────────────────────────────────────────
        System.out.println("""

          Adjacency list (cyclic):
            0 → [1, 2]
            1 → [3]
            2 → [3]
            3 → [0]       ← back edge

          Trace:
          dfs(0)  inStack=[T,F,F,F]
            dfs(1)  inStack=[T,T,F,F]
              dfs(3)  inStack=[T,T,F,T]
                neighbour=0 → inStack[0]=true → CYCLE ✓

          inStack vs visited:
            visited[i]=true  means: node i fully done, never reprocess
            inStack[i]=true  means: node i is on the current active path
                             → if seen again = back edge = cycle
          """);
    }
}
