import java.util.*;

/**
 * FIRST NEGATIVE INTEGER IN EVERY WINDOW OF SIZE K
 *
 * Problem: given array and window size k, for each window of k elements,
 * find the FIRST negative number. If none, output 0.
 *
 * Example:
 *   arr = [-3, 5, -2, 7, -1, 4]   k=3
 *   Window [-3,  5, -2] → -3
 *   Window [ 5, -2,  7] → -2
 *   Window [-2,  7, -1] → -2
 *   Window [ 7, -1,  4] → -1
 *
 * ── Brute Force O(n×k) ────────────────────────────────────────────────────
 *   For each window start i, scan from i to i+k-1 to find first negative.
 *   Redundant: re-scans same elements as window slides by 1.
 *
 * ── Optimized with Queue O(n) ─────────────────────────────────────────────
 *   Queue stores INDICES of negative numbers inside the current window.
 *   Slide the window:
 *     1. Remove front if it's outside the window (index < i)
 *     2. Add current index if arr[j] is negative
 *     3. Answer = arr[queue.front()] if queue non-empty, else 0
 *
 *   Key insight: we never need to scan back — the queue always holds
 *   indices of negatives in order, oldest at front.
 *
 * Dry run — arr=[-3,5,-2,7,-1,4], k=3:
 *   j=0: -3 negative → q=[0]
 *   j=1:  5 skip
 *   j=2: -2 negative → q=[0,2]   window i=0: front=0 ≥ 0 → ans=-3
 *   j=3:  7 skip     → i=1: front=0 < 1 → remove → q=[2] → ans=arr[2]=-2
 *   j=4: -1 negative → q=[2,4]   i=2: front=2 ≥ 2 → ans=arr[2]=-2
 *   j=5:  4 skip     → i=3: front=2 < 3 → remove → q=[4] → ans=arr[4]=-1
 */

class FirstNegativeInWindow {

    // ── Brute Force O(n×k) ────────────────────────────────────────────────
    static int[] bruteForce(int[] arr, int k) {
        int n = arr.length;
        int[] result = new int[n - k + 1];
        for (int i = 0; i <= n - k; i++) {
            result[i] = 0;                         // default: no negative found
            for (int j = i; j < i + k; j++) {
                if (arr[j] < 0) { result[i] = arr[j]; break; }
            }
        }
        return result;
    }

    // ── Queue Optimized O(n) ──────────────────────────────────────────────
    static int[] optimized(int[] arr, int k) {
        int n = arr.length;
        int[] result = new int[n - k + 1];
        Deque<Integer> q = new ArrayDeque<>();  // stores indices of negatives

        // fill first window
        for (int j = 0; j < k; j++) {
            if (arr[j] < 0) q.addLast(j);
        }

        // slide window — i is the left boundary of the window
        for (int i = 0; i <= n - k; i++) {
            // answer for current window
            result[i] = q.isEmpty() ? 0 : arr[q.peekFirst()];

            // slide: add next element (j = right boundary + 1)
            int j = i + k;
            if (j < n && arr[j] < 0) q.addLast(j);

            // remove front if it's falling out of next window
            if (!q.isEmpty() && q.peekFirst() <= i) q.pollFirst();
        }
        return result;
    }

    public static void main(String[] args) {
        int[][] tests = {
            {-3, 5, -2, 7, -1, 4},
            { 1, 2, 3, 4},            // no negatives → all 0
            {-1,-2,-3,-4},            // all negative → first of each window
            {12, -1, -7, 8, -15, 30, 16, 28}
        };
        int[] ks = {3, 2, 2, 3};

        for (int t = 0; t < tests.length; t++) {
            int[] arr = tests[t];
            int k = ks[t];
            System.out.println("arr=" + Arrays.toString(arr) + "  k=" + k);
            System.out.println("  brute:     " + Arrays.toString(bruteForce(arr, k)));
            System.out.println("  optimized: " + Arrays.toString(optimized(arr, k)));
            System.out.println();
        }

        // ── Complexity recap ─────────────────────────────────────────────
        System.out.println("Brute force:  O(n×k) — scans k elements per window");
        System.out.println("Queue based:  O(n)   — each index added/removed at most once");
        System.out.println("Space:        O(k)   — queue holds at most k indices");
    }
}
