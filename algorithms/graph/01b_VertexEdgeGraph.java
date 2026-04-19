import java.util.*;

/**
 * VERTEX + EDGE + GRAPH — OOP model of a graph
 *
 * 01_GraphBasics.java used plain integers as nodes.
 * This file models graph using proper classes so you can
 * attach real data (label, weight) to each node and edge.
 *
 *   Vertex = a node (city, person, server)
 *   Edge   = a connection between two vertices, with optional weight
 *   Graph  = contains all vertices + adjacency list of edges
 */

// ── Vertex — one node in the graph ───────────────────────────────────────────
class Vertex {
    int    id;
    String label;

    Vertex(int id, String label) {
        this.id    = id;
        this.label = label;
    }

    public String toString() { return label; }
}

// ── Edge — a directed connection from one vertex to another ──────────────────
class Edge {
    Vertex from;
    Vertex to;
    int    weight;   // distance / cost — use 1 if graph is unweighted

    Edge(Vertex from, Vertex to, int weight) {
        this.from   = from;
        this.to     = to;
        this.weight = weight;
    }

    public String toString() {
        return from.label + " →[" + weight + "]→ " + to.label;
    }
}

// ── Graph — adjacency list: each vertex → its outgoing edges ─────────────────
class Graph {
    Map<Vertex, List<Edge>> adjList = new HashMap<>();

    void addVertex(Vertex v) {
        adjList.putIfAbsent(v, new ArrayList<>());   // register vertex with empty list
    }

    // directed edge: from → to only
    void addEdge(Vertex from, Vertex to, int weight) {
        adjList.computeIfAbsent(from, k -> new ArrayList<>())
               .add(new Edge(from, to, weight));
    }

    // undirected edge: from ↔ to (add both directions)
    void addUndirectedEdge(Vertex from, Vertex to, int weight) {
        addEdge(from, to, weight);
        addEdge(to, from, weight);
    }

    List<Edge> neighbors(Vertex v) {
        return adjList.getOrDefault(v, new ArrayList<>());
    }

    void print() {
        for (Map.Entry<Vertex, List<Edge>> entry : adjList.entrySet()) {
            System.out.print("  " + entry.getKey().label + " → ");
            for (Edge e : entry.getValue()) {
                System.out.print(e.to.label + "(w=" + e.weight + ")  ");
            }
            System.out.println();
        }
    }
}

// ── Main ──────────────────────────────────────────────────────────────────────
class VertexEdgeGraph {
    public static void main(String[] args) {

        // ── Build vertices ────────────────────────────────────────────────────
        Vertex mumbai  = new Vertex(1, "Mumbai");
        Vertex delhi   = new Vertex(2, "Delhi");
        Vertex chennai = new Vertex(3, "Chennai");
        Vertex kolkata = new Vertex(4, "Kolkata");

        // ── Build graph ───────────────────────────────────────────────────────
        Graph g = new Graph();
        g.addUndirectedEdge(mumbai,  delhi,   1400);
        g.addUndirectedEdge(mumbai,  chennai, 1300);
        g.addUndirectedEdge(delhi,   kolkata, 1500);
        g.addUndirectedEdge(chennai, kolkata, 1700);

        System.out.println("=== Adjacency List ===");
        g.print();

        // ── What lives in memory ──────────────────────────────────────────────
        System.out.println("\n=== Memory structure ===");
        System.out.println("""
          adjList (Map<Vertex, List<Edge>>)
          ├── Vertex(Mumbai)  → [ Edge(Mumbai→Delhi,1400),   Edge(Mumbai→Chennai,1300) ]
          ├── Vertex(Delhi)   → [ Edge(Delhi→Mumbai,1400),   Edge(Delhi→Kolkata,1500)  ]
          ├── Vertex(Chennai) → [ Edge(Chennai→Mumbai,1300), Edge(Chennai→Kolkata,1700)]
          └── Vertex(Kolkata) → [ Edge(Kolkata→Delhi,1500),  Edge(Kolkata→Chennai,1700)]
          """);

        // ── Access neighbors of one vertex ────────────────────────────────────
        System.out.println("=== Neighbors of Mumbai ===");
        for (Edge e : g.neighbors(mumbai)) {
            System.out.println("  " + e);   // calls Edge.toString()
        }
    }
}
