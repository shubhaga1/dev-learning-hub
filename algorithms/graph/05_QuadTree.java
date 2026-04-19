import java.util.*;

/**
 * QUADTREE — 2D Spatial Index
 *
 * PROBLEM: Given 1M drivers on a map, find the 5 nearest to a rider in <100ms.
 * NAIVE:   Check all 1M drivers → O(n) — too slow at scale.
 * SOLUTION: QuadTree — divide space into 4, skip quadrants that are too far.
 *
 * HOW IT WORKS:
 *   1. Start with one rectangle covering the whole map.
 *   2. When a cell has > MAX_POINTS, split it into 4 equal quadrants.
 *   3. To query: only look into quadrants that OVERLAP your search area.
 *
 *   Visual split (cell with 5 points, MAX=4):
 *
 *   Before split:         After split:
 *   ┌──────────┐         ┌────┬────┐
 *   │  * * *   │         │ NW │ NE │
 *   │    *  *  │   →     ├────┼────┤
 *   │          │         │ SW │ SE │
 *   └──────────┘         └────┴────┘
 *
 * TIME:  O(log n) average query
 * SPACE: O(n)
 *
 * Run: javac 05_QuadTree.java && java QuadTree
 */
class QuadTree {

    // ─── Point ────────────────────────────────────────────────────────────────
    static class Point {
        double x, y;
        String id;

        Point(double x, double y, String id) {
            this.x  = x;
            this.y  = y;
            this.id = id;
        }

        double distanceTo(Point other) {
            double dx = this.x - other.x;
            double dy = this.y - other.y;
            return Math.sqrt(dx * dx + dy * dy);
        }

        @Override
        public String toString() {
            return id + "(" + String.format("%.2f", x) + "," + String.format("%.2f", y) + ")";
        }
    }

    // ─── Rectangle (bounding box of each node) ────────────────────────────────
    static class Rect {
        double cx, cy;   // center x, y
        double hw, hh;   // half-width, half-height

        Rect(double cx, double cy, double hw, double hh) {
            this.cx = cx; this.cy = cy;
            this.hw = hw; this.hh = hh;
        }

        boolean contains(Point p) {
            return p.x >= cx - hw && p.x <= cx + hw &&
                   p.y >= cy - hh && p.y <= cy + hh;
        }

        boolean intersects(Rect other) {
            return !(other.cx - other.hw > cx + hw ||
                     other.cx + other.hw < cx - hw ||
                     other.cy - other.hh > cy + hh ||
                     other.cy + other.hh < cy - hh);
        }

        @Override
        public String toString() {
            return String.format("Rect(cx=%.1f,cy=%.1f,hw=%.1f,hh=%.1f)", cx, cy, hw, hh);
        }
    }

    // ─── QuadTree Node ────────────────────────────────────────────────────────
    static class QTNode {
        static final int MAX_POINTS = 4;

        Rect        boundary;
        List<Point> points   = new ArrayList<>();
        boolean     divided  = false;

        // Four children — named by compass direction
        QTNode ne, nw, se, sw;

        QTNode(Rect boundary) {
            this.boundary = boundary;
        }

        // ── Insert ────────────────────────────────────────────────────────────
        boolean insert(Point p) {
            if (!boundary.contains(p)) return false; // outside this node

            if (!divided) {
                if (points.size() < MAX_POINTS) {
                    points.add(p);
                    return true;
                }
                subdivide(); // at capacity — split into 4
            }

            // Try inserting into one of the 4 children
            return ne.insert(p) || nw.insert(p) || se.insert(p) || sw.insert(p);
        }

        // ── Split this node into 4 quadrants ──────────────────────────────────
        void subdivide() {
            double cx = boundary.cx, cy = boundary.cy;
            double hw = boundary.hw / 2, hh = boundary.hh / 2;

            ne = new QTNode(new Rect(cx + hw, cy - hh, hw, hh)); // top-right
            nw = new QTNode(new Rect(cx - hw, cy - hh, hw, hh)); // top-left
            se = new QTNode(new Rect(cx + hw, cy + hh, hw, hh)); // bottom-right
            sw = new QTNode(new Rect(cx - hw, cy + hh, hw, hh)); // bottom-left

            divided = true;

            // Re-insert existing points into children
            for (Point existing : points) {
                ne.insert(existing); nw.insert(existing);
                se.insert(existing); sw.insert(existing);
            }
            points.clear(); // parent no longer holds points
        }

        // ── Range query — find all points inside a rectangle ──────────────────
        List<Point> query(Rect range, List<Point> found) {
            if (!boundary.intersects(range)) return found; // skip — no overlap

            if (!divided) {
                for (Point p : points) {
                    if (range.contains(p)) found.add(p);
                }
            } else {
                ne.query(range, found); nw.query(range, found);
                se.query(range, found); sw.query(range, found);
            }
            return found;
        }

        // ── Stats ─────────────────────────────────────────────────────────────
        int countNodes() {
            if (!divided) return 1;
            return 1 + ne.countNodes() + nw.countNodes() + se.countNodes() + sw.countNodes();
        }

        int depth() {
            if (!divided) return 0;
            return 1 + Math.max(Math.max(ne.depth(), nw.depth()),
                                Math.max(se.depth(), sw.depth()));
        }

        // Print tree structure for learning
        void print(String indent) {
            System.out.println(indent + boundary + " points=" + points.size());
            if (divided) {
                ne.print(indent + "  NE ");
                nw.print(indent + "  NW ");
                se.print(indent + "  SE ");
                sw.print(indent + "  SW ");
            }
        }
    }

    // ─── QuadTree (wraps root node) ───────────────────────────────────────────
    static class QTree {
        QTNode root;

        QTree(double width, double height) {
            // Center at 0,0 — world spans [-width/2..width/2, -height/2..height/2]
            root = new QTNode(new Rect(0, 0, width / 2, height / 2));
        }

        void insert(Point p) { root.insert(p); }

        // Find points in a rectangle area
        List<Point> query(Rect range) {
            return root.query(range, new ArrayList<>());
        }

        // Find N nearest points to a location
        List<Point> nearestN(Point target, int n, double initialRadius) {
            double radius = initialRadius;
            List<Point> result;

            // Expand search radius until we have at least n results
            do {
                Rect searchBox = new Rect(target.x, target.y, radius, radius);
                result = query(searchBox);
                radius *= 2;
            } while (result.size() < n && radius < 1000);

            // Sort by actual distance, take top n
            result.sort(Comparator.comparingDouble(p -> p.distanceTo(target)));
            return result.subList(0, Math.min(n, result.size()));
        }

        void printTree() { root.print(""); }
        int  nodes()     { return root.countNodes(); }
        int  depth()     { return root.depth(); }
    }

    // ─── Demo ─────────────────────────────────────────────────────────────────
    public static void main(String[] args) {

        // ── 1. Build tree ─────────────────────────────────────────────────────
        System.out.println("=== 1. INSERT DRIVERS (Mumbai coordinates) ===");

        // Using simplified coords: x=lng offset, y=lat offset from centre
        QTree qt = new QTree(2.0, 2.0); // covers roughly ±1 degree around centre

        List<Point> drivers = Arrays.asList(
            new Point( 0.08,  0.00, "D1-Bandra"  ),
            new Point(-0.05, -0.10, "D2-Dadar"   ),
            new Point( 0.07,  0.14, "D3-Andheri" ),
            new Point(-0.05, -0.09, "D4-Worli"   ),
            new Point( 0.20,  0.14, "D5-Powai"   ),
            new Point(-0.05, -0.17, "D6-Parel"   ),
            new Point(-0.07,  0.04, "D7-Khar"    ),
            new Point( 0.10,  0.18, "D8-Goregaon")
        );

        for (Point d : drivers) {
            qt.insert(d);
            System.out.println("  Inserted " + d);
        }

        System.out.println("\nTree stats:");
        System.out.println("  Total nodes: " + qt.nodes());
        System.out.println("  Tree depth:  " + qt.depth());

        // ── 2. Print tree structure ───────────────────────────────────────────
        System.out.println("\n=== 2. TREE STRUCTURE (see splits) ===");
        qt.printTree();

        // ── 3. Range query ────────────────────────────────────────────────────
        System.out.println("\n=== 3. RANGE QUERY — drivers in search box ===");
        Rect searchBox = new Rect(0.0, 0.0, 0.15, 0.15); // ±0.15 degrees around centre
        List<Point> found = qt.query(searchBox);
        System.out.println("Search box: " + searchBox);
        System.out.println("Found " + found.size() + " drivers:");
        found.forEach(p -> System.out.println("  → " + p));

        // ── 4. Nearest N drivers ──────────────────────────────────────────────
        System.out.println("\n=== 4. NEAREST 3 DRIVERS to user ===");
        Point user = new Point(0.0, -0.08, "User");
        System.out.println("User location: " + user);

        List<Point> nearest = qt.nearestN(user, 3, 0.2);
        System.out.println("Top 3 nearest:");
        nearest.forEach(p ->
            System.out.printf("  → %-15s  distance=%.4f%n", p, p.distanceTo(user))
        );

        // ── 5. Performance: naive vs QuadTree ────────────────────────────────
        System.out.println("\n=== 5. PERFORMANCE — 50,000 drivers ===");
        QTree bigTree = new QTree(360, 180); // full world
        Random rnd    = new Random(42);
        int    N      = 50_000;

        List<Point> allPoints = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            Point p = new Point(rnd.nextDouble() * 360 - 180,
                                rnd.nextDouble() * 180 - 90,
                                "d" + i);
            bigTree.insert(p);
            allPoints.add(p);
        }

        Point queryPoint = new Point(72.88, -19.08, "Rider");
        Rect  queryBox   = new Rect(72.88, -19.08, 5, 5);

        // Naive
        long t1 = System.nanoTime();
        long naiveCount = allPoints.stream()
            .filter(p -> Math.abs(p.x - queryPoint.x) <= 5 &&
                         Math.abs(p.y - queryPoint.y) <= 5)
            .count();
        long naiveMs = (System.nanoTime() - t1) / 1_000_000;

        // QuadTree
        long t2 = System.nanoTime();
        List<Point> qtResult = bigTree.query(queryBox);
        long qtMs = (System.nanoTime() - t2) / 1_000_000;

        System.out.printf("  Naive scan:  %dms  (checked all %,d drivers, found %d)%n",
                          naiveMs, N, naiveCount);
        System.out.printf("  QuadTree:    %dms  (skipped far quadrants, found %d)%n",
                          qtMs, qtResult.size());
        System.out.printf("  Speedup:     ~%dx%n", naiveMs > 0 ? naiveMs / Math.max(1, qtMs) : 1);

        System.out.println("""

        KEY POINTS:
          1. subdivide() splits when node has > MAX_POINTS — never before
          2. query() skips entire subtrees when bounding box doesn't intersect
          3. Points re-inserted into children after split (not just pointers moved)
          4. nearestN() uses expanding radius — start small, double until enough found

        LIMITS OF QUADTREE:
          - Clustered data: one quadrant keeps splitting (deep, unbalanced)
          - Flat 2D only: distortion near poles for global maps
          - Not persistent: lives in memory, rebuild on restart
          → For production: Redis GEO (distributed) or PostGIS R-Tree (polygon support)
        """);
    }
}
