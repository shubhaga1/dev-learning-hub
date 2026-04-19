import java.util.*;

/**
 * CIRCULAR GAME — Josephus Problem
 *
 * Problem: n people numbered 1..n sit in a circle.
 * Starting from person 1, every k-th person is eliminated.
 * Find the last person standing.
 *
 * Example — n=6, k=2:
 *   Circle: [1, 2, 3, 4, 5, 6]
 *   Eliminate 2nd each time:
 *     Round 1: skip 1, eliminate 2 → [3,4,5,6,1]
 *     Round 2: skip 3, eliminate 4 → [5,6,1,3]
 *     Round 3: skip 5, eliminate 6 → [1,3,5]
 *     Round 4: skip 1, eliminate 3 → [5,1]
 *     Round 5: skip 5, eliminate 1 → [5]
 *   Winner: 5
 *
 * ── Queue Approach O(n×k) ─────────────────────────────────────────────────
 *   Load all n people into a queue.
 *   Each round:
 *     - rotate (k-1) people from front to back (they survive this round)
 *     - remove() the k-th person (eliminated)
 *   Repeat until one remains.
 *
 * ── Why queue works ───────────────────────────────────────────────────────
 *   The queue naturally models the circle — after skipping k-1 people,
 *   they go to the back (still alive, just moved around the circle).
 *   The k-th person is dequeued and discarded.
 *
 * ── Bonus: Insert/Remove at arbitrary index ───────────────────────────────
 *   Queue has no random access — simulate by rotating:
 *   insertAt(queue, idx, val):
 *     - rotate idx elements to back (they precede the insertion point)
 *     - add new element
 *     - rotate remaining (n - idx) elements to back (restore order)
 *
 *   removeAt(queue, idx):
 *     - rotate idx elements to back
 *     - remove() the front element
 *     - rotate remaining to restore order
 */

class CircularGame {

    // ── Josephus — queue simulation ───────────────────────────────────────
    static int josephus(int n, int k) {
        Queue<Integer> q = new LinkedList<>();
        for (int i = 1; i <= n; i++) q.add(i);

        System.out.print("Elimination order: ");
        while (q.size() > 1) {
            // rotate k-1 survivors to back
            for (int i = 1; i < k; i++) q.add(q.remove());
            // eliminate k-th
            System.out.print(q.remove() + " ");
        }
        System.out.println();
        return q.peek();
    }

    // ── Insert at arbitrary index O(n) ────────────────────────────────────
    static void insertAt(Queue<Integer> q, int idx, int val) {
        int n = q.size();
        // rotate first idx elements to back (they come before insertion point)
        for (int i = 0; i < idx; i++) q.add(q.remove());
        q.add(val);
        // rotate remaining original elements to restore order
        for (int i = 0; i < n - idx; i++) q.add(q.remove());
    }

    // ── Remove at arbitrary index O(n) ────────────────────────────────────
    static int removeAt(Queue<Integer> q, int idx) {
        int n = q.size();
        // rotate to bring target to front
        for (int i = 0; i < idx; i++) q.add(q.remove());
        int removed = q.remove();
        // restore order of remaining elements
        for (int i = 0; i < n - idx - 1; i++) q.add(q.remove());
        return removed;
    }

    public static void main(String[] args) {

        // ── Josephus tests ─────────────────────────────────────────────────
        System.out.println("=== Circular Game (Josephus Problem) ===\n");

        int[][] tests = {{6, 2}, {5, 2}, {7, 3}};
        for (int[] t : tests) {
            int n = t[0], k = t[1];
            System.out.printf("n=%d k=%d  ", n, k);
            int winner = josephus(n, k);
            System.out.println("Winner: " + winner);
            System.out.println();
        }

        // ── Insert/Remove at index ─────────────────────────────────────────
        System.out.println("=== Insert/Remove at Arbitrary Index ===\n");

        Queue<Integer> q = new LinkedList<>(Arrays.asList(10, 20, 30, 40, 50));
        System.out.println("Initial: " + q);

        insertAt(q, 2, 99);   // insert 99 at index 2 → [10, 20, 99, 30, 40, 50]
        System.out.println("After insertAt(2, 99): " + q);

        int removed = removeAt(q, 4);   // remove index 4 → removes 40
        System.out.println("After removeAt(4): " + q + "  removed=" + removed);

        // ── Complexity recap ─────────────────────────────────────────────
        System.out.println("\nJosephus:     O(n×k) time, O(n) space");
        System.out.println("Insert/Remove at index: O(n) — rotate n elements");
    }
}
