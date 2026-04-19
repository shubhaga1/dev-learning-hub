import java.util.*;

/**
 * GRAPH BASICS — What is a graph and how to represent it
 *
 * A Graph = Nodes (vertices) + Edges (connections between them)
 *
 * Real examples:
 *   Cities connected by roads         → nodes=cities,  edges=roads
 *   People connected by friendships   → nodes=people,  edges=friendships
 *   Courses with prerequisites        → nodes=courses, edges=prerequisites
 *
 * Two types:
 *   Undirected: A—B means A→B AND B→A  (friendship)
 *   Directed:   A→B means A→B only     (Instagram follow)
 *
 * Two ways to represent:
 *   1. Adjacency Matrix  → 2D array  → fast to check edge, wastes space
 *   2. Adjacency List   → Map/List  → memory efficient, used in most problems
 *
 * Run: javac 01_GraphBasics.java && java GraphBasics
 */
class GraphBasics {

    // ─── Representation 1: Adjacency Matrix ──────────────────────────────────
    // matrix[i][j] = 1 means there is an edge from node i to node j
    // Space: O(V²) — bad for sparse graphs (few edges)
    static void adjacencyMatrix() {
        System.out.println("=== ADJACENCY MATRIX ===");

        // Graph:  0—1—2
        //         |   |
        //         3———4
        int[][] matrix = {
            //  0  1  2  3  4
                {0, 1, 0, 1, 0},  // node 0 connects to 1, 3
                {1, 0, 1, 0, 0},  // node 1 connects to 0, 2
                {0, 1, 0, 0, 1},  // node 2 connects to 1, 4
                {1, 0, 0, 0, 1},  // node 3 connects to 0, 4
                {0, 0, 1, 1, 0},  // node 4 connects to 2, 3
        };

        // Print
        System.out.print("  ");
        for (int i = 0; i < matrix.length; i++) System.out.print(i + " ");
        System.out.println();
        for (int i = 0; i < matrix.length; i++) {
            System.out.print(i + " ");
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }

        // Check if edge exists: O(1)
        System.out.println("Edge 0→1 exists: " + (matrix[0][1] == 1)); // true
        System.out.println("Edge 0→2 exists: " + (matrix[0][2] == 1)); // false
    }

    // ─── Representation 2: Adjacency List ────────────────────────────────────
    // Map<node, List<neighbors>>
    // Space: O(V + E) — efficient, used in BFS/DFS
    static Map<Integer, List<Integer>> buildAdjacencyList() {
        System.out.println("\n=== ADJACENCY LIST ===");

        // Same graph:  0—1—2
        //              |   |
        //              3———4
        Map<Integer, List<Integer>> graph = new HashMap<>();

        // Add edges (undirected — add both directions)
        // Each addEdge call adds ONE edge (two directions internally)
        // To get node 0 → [1, 3], you need TWO separate addEdge calls:
        addEdge(graph, 0, 1);   // node 0 connects to 1  →  0:[1],  1:[0]
        addEdge(graph, 0, 3);   // node 0 connects to 3  →  0:[1,3], 3:[0]
        addEdge(graph, 1, 2);
        addEdge(graph, 2, 4);
        addEdge(graph, 3, 4);

        // What addEdge does under the hood (two lines per edge):
        // graph.computeIfAbsent(0, k -> new ArrayList<>()).add(1);  ← 0 → 1
        // graph.computeIfAbsent(1, k -> new ArrayList<>()).add(0);  ← 1 → 0

        // Print
        for (int node : graph.keySet()) {
            System.out.println("Node " + node + " → " + graph.get(node));
        }

        return graph;
    }

    static void addEdge(Map<Integer, List<Integer>> graph, int u, int v) {
        graph.computeIfAbsent(u, k -> new ArrayList<>()).add(v);
        graph.computeIfAbsent(v, k -> new ArrayList<>()).add(u); // remove for directed
    }

    // ─── Graph Terminology ────────────────────────────────────────────────────
    static void terminology() {
        System.out.println("\n=== KEY TERMS ===");
        System.out.println("""
            Vertex / Node   = a point in the graph (city, person, course)
            Edge            = connection between two nodes
            Degree          = number of edges a node has
            Path            = sequence of nodes connected by edges
            Cycle           = path that starts and ends at same node
            Connected graph = every node reachable from every other node
            Weighted graph  = edges have a cost/distance (roads with km)
            Directed graph  = edges have direction (A→B but not B→A)
            """);
    }

    // ─── When to use what ────────────────────────────────────────────────────
    static void whenToUse() {
        System.out.println("=== WHEN TO USE WHICH ===");
        System.out.println("""
            Adjacency MATRIX:
              ✅ Dense graph (many edges)
              ✅ Need to check if specific edge exists in O(1)
              ❌ Wastes memory for sparse graphs (V² space)

            Adjacency LIST:
              ✅ Sparse graph (few edges — most real problems)
              ✅ Need to iterate over neighbors (BFS/DFS)
              ✅ Memory efficient: O(V + E)
              ❌ Checking if edge exists is O(degree)

            → In 99% of coding problems: use Adjacency List
            """);
    }

    public static void main(String[] args) {
        adjacencyMatrix();
        buildAdjacencyList();
        terminology();
        whenToUse();
    }
}
