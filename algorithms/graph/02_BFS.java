import java.util.*;

/**
 * BFS — Breadth First Search
 *
 * IDEA: Visit all neighbors at distance 1 first, then distance 2, then 3...
 *       Like ripples in water — expands level by level.
 *
 * TOOL: Queue (FIFO) — process nodes in the order you discover them
 *
 * USE CASES:
 *   ✅ Shortest path in UNWEIGHTED graph (fewest edges)
 *   ✅ Level order traversal
 *   ✅ Find all nodes reachable from a source
 *   ✅ Check if graph is connected
 *   ✅ "minimum steps" problems
 *
 * TIME:  O(V + E) — visit every vertex and edge once
 * SPACE: O(V)     — queue + visited set
 *
 * Run: javac 02_BFS.java && java BFS
 */
class BFS {

    // ─── Build graph helper ───────────────────────────────────────────────────
    static Map<Integer, List<Integer>> buildGraph() {
        // Graph:   1—2—5
        //          |   |
        //          3—4—6
        Map<Integer, List<Integer>> graph = new HashMap<>();
        int[][] edges = {{1,2},{1,3},{2,5},{3,4},{4,6},{5,6}};
        for (int[] e : edges) {
            graph.computeIfAbsent(e[0], k -> new ArrayList<>()).add(e[1]);
            graph.computeIfAbsent(e[1], k -> new ArrayList<>()).add(e[0]);
        }
        return graph;
    }

    // ─── 1. Basic BFS traversal ───────────────────────────────────────────────
    // Visits every reachable node, prints in BFS order
    static void bfsTraversal(Map<Integer, List<Integer>> graph, int start) {
        System.out.println("=== BFS TRAVERSAL from node " + start + " ===");

        Queue<Integer> queue   = new LinkedList<>();
        Set<Integer>   visited = new HashSet<>();

        queue.add(start);
        visited.add(start);

        while (!queue.isEmpty()) {
            int node = queue.poll();           // take from FRONT
            System.out.print(node + " ");

            for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);     // mark BEFORE adding to queue
                    queue.add(neighbor);       // add to BACK
                }
            }
        }
        System.out.println();
    }

    // ─── 2. BFS level by level ───────────────────────────────────────────────
    // Shows which nodes are at distance 1, 2, 3... from start
    static void bfsLevels(Map<Integer, List<Integer>> graph, int start) {
        System.out.println("\n=== BFS LEVELS from node " + start + " ===");

        Queue<Integer> queue   = new LinkedList<>();
        Set<Integer>   visited = new HashSet<>();

        queue.add(start);
        visited.add(start);
        int level = 0;

        while (!queue.isEmpty()) {
            int size = queue.size(); // number of nodes at THIS level
            System.out.print("Level " + level + ": ");

            for (int i = 0; i < size; i++) {   // process exactly this level
                int node = queue.poll();
                System.out.print(node + " ");

                for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
                    if (!visited.contains(neighbor)) {
                        visited.add(neighbor);
                        queue.add(neighbor);
                    }
                }
            }
            System.out.println();
            level++;
        }
    }

    // ─── 3. BFS shortest path ────────────────────────────────────────────────
    // Returns the shortest path (fewest edges) from start to end
    // Works only for UNWEIGHTED graphs
    static List<Integer> shortestPath(Map<Integer, List<Integer>> graph, int start, int end) {
        System.out.println("\n=== SHORTEST PATH from " + start + " to " + end + " ===");

        Queue<Integer>        queue   = new LinkedList<>();
        Map<Integer, Integer> parent  = new HashMap<>(); // child → parent (to reconstruct path)

        queue.add(start);
        parent.put(start, -1); // start has no parent

        while (!queue.isEmpty()) {
            int node = queue.poll();

            if (node == end) break; // found it — stop early

            for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
                if (!parent.containsKey(neighbor)) { // not visited
                    parent.put(neighbor, node);
                    queue.add(neighbor);
                }
            }
        }

        // Reconstruct path by walking back from end → start via parent map
        if (!parent.containsKey(end)) {
            System.out.println("No path found");
            return new ArrayList<>();
        }

        List<Integer> path = new ArrayList<>();
        for (int cur = end; cur != -1; cur = parent.get(cur)) {
            path.add(cur);
        }
        Collections.reverse(path);
        System.out.println("Path: " + path + "  (length: " + (path.size() - 1) + " edges)");
        return path;
    }

    // ─── 4. BFS shortest distance to all nodes ───────────────────────────────
    static void shortestDistances(Map<Integer, List<Integer>> graph, int start) {
        System.out.println("\n=== SHORTEST DISTANCES from node " + start + " ===");

        Queue<Integer>        queue    = new LinkedList<>();
        Map<Integer, Integer> distance = new HashMap<>();

        queue.add(start);
        distance.put(start, 0);

        while (!queue.isEmpty()) {
            int node = queue.poll();

            for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
                if (!distance.containsKey(neighbor)) {
                    distance.put(neighbor, distance.get(node) + 1);
                    queue.add(neighbor);
                }
            }
        }

        for (int node : distance.keySet()) {
            System.out.println("  Node " + node + " → distance " + distance.get(node));
        }
    }

    // ─── 5. BFS step-by-step trace ───────────────────────────────────────────
    // See exactly what happens inside the queue — good for learning
    static void bfsTrace(Map<Integer, List<Integer>> graph, int start) {
        System.out.println("\n=== BFS INTERNAL TRACE from node " + start + " ===");
        System.out.println("(watching the queue at each step)\n");

        Queue<Integer> queue   = new LinkedList<>();
        Set<Integer>   visited = new HashSet<>();

        queue.add(start);
        visited.add(start);

        while (!queue.isEmpty()) {
            System.out.println("  Queue: " + queue);
            int node = queue.poll();
            System.out.println("  Dequeue → process node " + node);

            for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.add(neighbor);
                    System.out.println("    Enqueue neighbor " + neighbor);
                }
            }
        }
    }

    public static void main(String[] args) {
     //   Map<Integer, List<Integer>> graph = buildGraph();

        Map<Integer, List<Integer>> graph = new HashMap<>();
        
        int[][] edges = {{1,2},{1,3},{2,5},{3,4},{4,6},{5,6}};
       
        for (int[] e : edges) {
            graph.computeIfAbsent(e[0], k -> new ArrayList<>()).add(e[1]);
            graph.computeIfAbsent(e[1], k -> new ArrayList<>()).add(e[0]);
        }

        // bfsTraversal(graph, 1);
        // bfsLevels(graph, 1);
        // shortestPath(graph, 1, 6);
        // shortestPath(graph, 1, 4);
        // shortestDistances(graph, 1);
        // bfsTrace(graph, 1);

        // System.out.println("\n=== KEY POINTS TO REMEMBER ===");
        // System.out.println("""
        //     1. Always mark visited BEFORE adding to queue (not after polling)
        //        → If you mark after polling, same node gets added to queue multiple times

        //     2. Use Queue (LinkedList) — NOT Stack
        //        → Queue = FIFO = level by level = BFS
        //        → Stack = LIFO = deep first = DFS

        //     3. BFS gives shortest path only for UNWEIGHTED graphs
        //        → For weighted graphs → Dijkstra

        //     4. Level trick: int size = queue.size() at start of each level iteration
        //        → This freezes the count of nodes at current level
        //     """);
    }
}
