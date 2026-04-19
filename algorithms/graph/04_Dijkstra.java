import java.util.*;

/**
 * DIJKSTRA'S ALGORITHM — Shortest path in WEIGHTED graph
 *
 * PROBLEM: BFS finds shortest path by number of edges.
 *          But what if edges have different costs (distances, time, price)?
 *          → Dijkstra finds shortest path by TOTAL WEIGHT.
 *
 * IDEA:
 *   Always process the unvisited node with the SMALLEST known distance first.
 *   Use a Priority Queue (min-heap) to always get the cheapest next node.
 *
 * TOOL: Priority Queue (Min-Heap) — always gives smallest distance first
 *
 * LIMITATION: Does NOT work with NEGATIVE weights → use Bellman-Ford instead
 *
 * TIME:  O((V + E) log V)  — each node/edge processed once, PQ operations log V
 * SPACE: O(V)
 *
 * USE CASES:
 *   ✅ GPS / Google Maps shortest route
 *   ✅ Network packet routing
 *   ✅ Cheapest flight path
 *   ✅ Any "minimum cost" path problem with positive weights
 *
 * Run: javac 04_Dijkstra.java && java Dijkstra
 */
class Dijkstra {

    // Edge in a weighted graph: destination + weight
    static class Edge {
        int to, weight;
        Edge(int to, int weight) {
            this.to     = to;
            this.weight = weight;
        }
    }

    // Entry in the priority queue: node + distance from source
    static class Entry implements Comparable<Entry> {
        int node, distance;
        Entry(int node, int distance) {
            this.node     = node;
            this.distance = distance;
        }

        @Override
        public int compareTo(Entry other) {
            return this.distance - other.distance; // min-heap: smaller distance = higher priority
        }
    }

    // Build weighted graph
    static Map<Integer, List<Edge>> buildWeightedGraph() {
        // Graph with weights (distances in km):
        //
        //      1 —(4)— 2
        //      |       |  \
        //     (2)     (1)  (5)
        //      |       |     \
        //      3 —(8)— 4 —(3)— 5
        //       \             /
        //        ——————(6)————
        //
        Map<Integer, List<Edge>> graph = new HashMap<>();
        int[][] edges = {
            {1, 2, 4},   // 1→2 costs 4
            {1, 3, 2},   // 1→3 costs 2
            {2, 4, 1},   // 2→4 costs 1
            {2, 5, 5},   // 2→5 costs 5
            {3, 4, 8},   // 3→4 costs 8
            {3, 5, 6},   // 3→5 costs 6
            {4, 5, 3},   // 4→5 costs 3
        };
        for (int[] e : edges) {
            graph.computeIfAbsent(e[0], k -> new ArrayList<>()).add(new Edge(e[1], e[2]));
            graph.computeIfAbsent(e[1], k -> new ArrayList<>()).add(new Edge(e[0], e[2])); // undirected
        }
        return graph;
    }

    // ─── 1. Dijkstra — shortest distances from source to ALL nodes ────────────
    static int[] dijkstra(Map<Integer, List<Edge>> graph, int source, int totalNodes) {
        int[] dist = new int[totalNodes + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[source] = 0;

        // Min-heap: process node with smallest distance first
        PriorityQueue<Entry> pq = new PriorityQueue<>();
        pq.add(new Entry(source, 0));

        Set<Integer> visited = new HashSet<>();

        while (!pq.isEmpty()) {
            Entry entry = pq.poll();          // get node with SMALLEST distance
            int   node  = entry.node;

            if (visited.contains(node)) continue; // already finalized — skip
            visited.add(node);

            System.out.printf("  Process node %-3d (dist=%d)%n", node, dist[node]);

            for (Edge edge : graph.getOrDefault(node, new ArrayList<>())) {
                int newDist = dist[node] + edge.weight;

                if (newDist < dist[edge.to]) {   // found a shorter path
                    dist[edge.to] = newDist;
                    pq.add(new Entry(edge.to, newDist));
                    System.out.printf("    Update node %d: %d → %d%n", edge.to, dist[edge.to] == newDist ? Integer.MAX_VALUE : dist[edge.to], newDist);
                }
            }
        }
        return dist;
    }

    // ─── 2. Dijkstra — also track the actual path ─────────────────────────────
    static void dijkstraWithPath(Map<Integer, List<Edge>> graph, int source, int target, int totalNodes) {
        int[]   dist   = new int[totalNodes + 1];
        int[]   parent = new int[totalNodes + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        Arrays.fill(parent, -1);
        dist[source] = 0;

        PriorityQueue<Entry> pq      = new PriorityQueue<>();
        Set<Integer>         visited = new HashSet<>();
        pq.add(new Entry(source, 0));

        while (!pq.isEmpty()) {
            Entry entry = pq.poll();
            int   node  = entry.node;

            if (visited.contains(node)) continue;
            visited.add(node);

            for (Edge edge : graph.getOrDefault(node, new ArrayList<>())) {
                int newDist = dist[node] + edge.weight;
                if (newDist < dist[edge.to]) {
                    dist[edge.to]   = newDist;
                    parent[edge.to] = node;      // remember where we came from
                    pq.add(new Entry(edge.to, newDist));
                }
            }
        }

        // Reconstruct path
        List<Integer> path = new ArrayList<>();
        for (int cur = target; cur != -1; cur = parent[cur]) {
            path.add(cur);
        }
        Collections.reverse(path);

        System.out.println("Shortest path " + source + " → " + target + ": " + path);
        System.out.println("Total cost: " + dist[target]);
    }

    // ─── 3. Why BFS fails for weighted graphs ────────────────────────────────
    static void whyNotBFS() {
        System.out.println("\n=== WHY BFS FAILS FOR WEIGHTED GRAPHS ===");
        System.out.println("""
            Graph:  A —(1)— B —(1)— C
                    |               |
                    +——————(100)————+

            BFS says: A→B→C = 2 edges = shortest
            But actual cost A→B→C = 2, while A→C direct = 100

            Here BFS is right because cost 2 < 100.

            Now reverse weights:
            Graph:  A —(100)— B —(100)— C
                    |                   |
                    +———————(1)—————————+

            BFS says: A→B→C = 2 edges = shortest
            But actual cost A→B→C = 200, while A→C = 1

            BFS chose 2 hops but 200 cost — WRONG answer.
            Dijkstra would correctly pick A→C (1 hop, cost 1).
            """);
    }

    // ─── 4. Step-by-step walkthrough ─────────────────────────────────────────
    static void manualWalkthrough() {
        System.out.println("=== DIJKSTRA MANUAL WALKTHROUGH ===");
        System.out.println("""
            Graph: 1—(4)—2, 1—(2)—3, 2—(1)—4, 3—(8)—4, 4—(3)—5
            Source: node 1

            Step 1: dist = [∞, 0, ∞, ∞, ∞, ∞]   PQ: [(1,0)]
            Step 2: Pop (1,0). Neighbors: 2→4, 3→2
                    dist = [∞, 0, 4, 2, ∞, ∞]     PQ: [(3,2),(2,4)]
            Step 3: Pop (3,2). Neighbors: 4→10, 5→8
                    dist = [∞, 0, 4, 2, 10, 8]     PQ: [(2,4),(5,8),(4,10)]
            Step 4: Pop (2,4). Neighbors: 4→5 (4+1=5 < 10, update!)
                    dist = [∞, 0, 4, 2, 5, 8]      PQ: [(4,5),(5,8),(4,10)]
            Step 5: Pop (4,5). Neighbors: 5→8 (5+3=8, no change)
                    dist unchanged
            Step 6: Pop (5,8). Done.

            Final: 1→2=4, 1→3=2, 1→4=5, 1→5=8
            Path to 5: 1→2→4→5 (cost 4+1+3=8)
            """);
    }

    public static void main(String[] args) {
        Map<Integer, List<Edge>> graph = buildWeightedGraph();

        System.out.println("=== DIJKSTRA — Shortest distances from node 1 ===");
        int[] dist = dijkstra(graph, 1, 5);
        System.out.println("\nResults:");
        for (int i = 1; i <= 5; i++) {
            System.out.println("  Node 1 → Node " + i + " = " + dist[i]);
        }

        System.out.println("\n=== DIJKSTRA WITH PATH ===");
        dijkstraWithPath(graph, 1, 5, 5);
        dijkstraWithPath(graph, 1, 4, 5);

        whyNotBFS();
        manualWalkthrough();

        System.out.println("=== KEY POINTS TO REMEMBER ===");
        System.out.println("""
            1. Priority Queue replaces regular Queue from BFS
               → Always processes CHEAPEST node next (greedy)

            2. Skip already-visited nodes when popping from PQ
               → A node can be in PQ multiple times with different distances
               → Only the first pop (smallest distance) is correct

            3. Relaxation: if (dist[node] + weight < dist[neighbor]) → update
               → This is the core of Dijkstra

            4. Does NOT work with negative weights
               → Once a node is finalized, we assume we found the shortest path
               → Negative edge could create a shorter path discovered later

            5. BFS = unweighted shortest path (all edges = 1)
               Dijkstra = weighted shortest path (positive weights only)
               Bellman-Ford = weighted + negative weights allowed
            """);
    }
}
