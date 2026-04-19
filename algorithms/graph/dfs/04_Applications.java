package dfs;

import java.util.*;

/**
 * DFS 4/4 — APPLICATIONS
 *
 * Three classic problems solved with DFS:
 *   1. Cycle detection   — is there a loop in the graph?
 *   2. All paths         — find every route from A to B
 *   3. Connected components — how many isolated groups exist?
 *
 * All three use the same DFS skeleton — just different tracking.
 */
class DFSApplications {

    static Map<Integer, List<Integer>> buildGraph(int[][] edges) {
        Map<Integer, List<Integer>> g = new HashMap<>();
        for (int[] e : edges) {
            g.computeIfAbsent(e[0], k -> new ArrayList<>()).add(e[1]);
            g.computeIfAbsent(e[1], k -> new ArrayList<>()).add(e[0]);
        }
        return g;
    }

    // ── 1. Cycle detection ────────────────────────────────────────────────────
    // Cycle = we reach a visited node that is NOT our direct parent
    // parent tracking avoids false positive: A—B—A in undirected is not a cycle
    static boolean hasCycle(Map<Integer, List<Integer>> g,
                             int node, int parent, Set<Integer> visited) {
        visited.add(node);
        for (int neighbor : g.getOrDefault(node, new ArrayList<>())) {
            if (!visited.contains(neighbor)) {
                if (hasCycle(g, neighbor, node, visited)) return true;
            } else if (neighbor != parent) {
                return true;   // visited AND not parent → cycle found
            }
        }
        return false;
    }

    // ── 2. All paths from src to dst ──────────────────────────────────────────
    // BACKTRACKING: add node to path → recurse → remove node after returning
    // This lets different paths reuse the same nodes
    static void findAllPaths(Map<Integer, List<Integer>> g, int cur, int dst,
                              List<Integer> path, Set<Integer> visited,
                              List<List<Integer>> result) {
        path.add(cur);
        visited.add(cur);

        if (cur == dst) {
            result.add(new ArrayList<>(path));  // found one complete path
        } else {
            for (int neighbor : g.getOrDefault(cur, new ArrayList<>())) {
                if (!visited.contains(neighbor))
                    findAllPaths(g, neighbor, dst, path, visited, result);
            }
        }
        path.remove(path.size() - 1);  // backtrack — remove current node
        visited.remove(cur);            // backtrack — unmark visited
    }

    // ── 3. Connected components ───────────────────────────────────────────────
    // Component = group of nodes all reachable from each other
    // Start DFS from each unvisited node — each start = one new component
    static int countComponents(Map<Integer, List<Integer>> g,
                                int totalNodes, Set<Integer> visited) {
        int count = 0;
        for (int node = 1; node <= totalNodes; node++) {
            if (!visited.contains(node)) {
                dfsHelper(g, node, visited);
                count++;                        // one full DFS = one component
            }
        }
        return count;
    }

    static void dfsHelper(Map<Integer, List<Integer>> g,
                           int node, Set<Integer> visited) {
        visited.add(node);
        for (int n : g.getOrDefault(node, new ArrayList<>()))
            if (!visited.contains(n)) dfsHelper(g, n, visited);
    }

    public static void main(String[] args) {
        // ── 1. Cycle detection ────────────────────────────────────────────────
        System.out.println("=== 1. Cycle Detection ===");
        Map<Integer, List<Integer>> cyclic = buildGraph(new int[][]{{1,2},{2,3},{3,1}});
        Map<Integer, List<Integer>> tree   = buildGraph(new int[][]{{1,2},{2,3},{3,4}});
        System.out.println("cyclic graph (1-2-3-1): " + hasCycle(cyclic, 1, -1, new HashSet<>()));
        System.out.println("tree   graph (1-2-3-4): " + hasCycle(tree,   1, -1, new HashSet<>()));

        // ── 2. All paths ──────────────────────────────────────────────────────
        System.out.println("\n=== 2. All Paths (1 → 4) ===");
        Map<Integer, List<Integer>> g = buildGraph(new int[][]{{1,2},{1,3},{2,4},{3,4},{2,3}});
        List<List<Integer>> paths = new ArrayList<>();
        findAllPaths(g, 1, 4, new ArrayList<>(), new HashSet<>(), paths);
        paths.forEach(p -> System.out.println("  " + p));

        // ── 3. Connected components ───────────────────────────────────────────
        System.out.println("\n=== 3. Connected Components ===");
        // {1,2,3} connected, {4,5} connected — two separate groups
        Map<Integer, List<Integer>> disc = buildGraph(new int[][]{{1,2},{2,3},{4,5}});
        for (int i = 1; i <= 5; i++) disc.putIfAbsent(i, new ArrayList<>());
        System.out.println("Components: " + countComponents(disc, 5, new HashSet<>()));
    }
}
