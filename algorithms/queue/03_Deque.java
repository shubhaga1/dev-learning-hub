import java.util.*;

/**
 * DEQUE — Double-Ended Queue (pronounced "deck")
 *
 * Mental model: a train — you can board/exit from EITHER end.
 *
 * Java: ArrayDeque implements Deque<E>
 *
 * Operations:
 *   addFirst(x)  / offerFirst(x)  → add to FRONT
 *   addLast(x)   / offerLast(x)   → add to BACK
 *   removeFirst() / pollFirst()    → remove from FRONT
 *   removeLast()  / pollLast()     → remove from BACK
 *   peekFirst()                    → look at FRONT
 *   peekLast()                     → look at BACK
 *
 * Deque is used as:
 *   Stack → addFirst / removeFirst  (LIFO from front)
 *   Queue → addLast  / removeFirst  (FIFO — add back, remove front)
 *
 * WHERE Deque appears in interviews:
 *   Sliding Window Maximum (hard — Google, Amazon, Facebook)
 *   Monotonic Deque problems
 *   Implement stack with queue / queue with stack
 *   BFS with priority from both ends
 */
class DequeDemo {

    // ── 1. Deque API demo ─────────────────────────────────────────────────────
    static void dequeApiDemo() {
        System.out.println("=== 1. Deque API ===");
        ArrayDeque<Integer> dq = new ArrayDeque<>();

        dq.addLast(10);     // [10]
        dq.addLast(20);     // [10, 20]
        dq.addFirst(5);     // [5, 10, 20]
        System.out.println("Deque: " + dq);          // [5, 10, 20]

        System.out.println("peekFirst: " + dq.peekFirst());   // 5
        System.out.println("peekLast:  " + dq.peekLast());    // 20

        System.out.println("pollFirst: " + dq.pollFirst());   // 5
        System.out.println("pollLast:  " + dq.pollLast());    // 20
        System.out.println("After: " + dq);                   // [10]
    }

    // ── 2. Sliding Window Maximum (Google, Amazon #1 Deque problem) ───────────
    /**
     * Given array nums and window size k, find max in every window.
     *
     * nums = [1,3,-1,-3,5,3,6,7], k = 3
     * Windows:
     *   [1  3  -1] → 3
     *   [3  -1 -3] → 3
     *   [-1 -3  5] → 5
     *   [-3  5  3] → 5
     *   [5   3  6] → 6
     *   [3   6  7] → 7
     * Output: [3,3,5,5,6,7]
     *
     * APPROACH — Monotonic Decreasing Deque:
     *   Deque stores INDICES (not values).
     *   Deque front = index of max in current window.
     *   Invariant: values at deque indices are always DECREASING front→back.
     *
     *   For each element:
     *   1. Remove indices outside window from FRONT (too old)
     *   2. Remove indices from BACK whose values <= current (useless — current is better)
     *   3. Add current index to BACK
     *   4. Front of deque = max of current window
     *
     * WHY this is O(n): each index added once, removed once → amortized O(1)
     */
    static int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] result = new int[n - k + 1];
        ArrayDeque<Integer> dq = new ArrayDeque<>();   // stores indices

        for (int i = 0; i < n; i++) {
            // Remove indices that are outside the current window
            while (!dq.isEmpty() && dq.peekFirst() < i - k + 1) {
                dq.pollFirst();
            }

            // Remove indices from back whose values are <= current
            // They can never be max while current element exists in window
            while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) {
                dq.pollLast();
            }

            dq.addLast(i);

            // Window is fully formed starting at index k-1
            if (i >= k - 1) {
                result[i - k + 1] = nums[dq.peekFirst()];
            }
        }
        return result;
    }

    // ── 3. First Negative in Every Window (Amazon) ────────────────────────────
    /**
     * For each window of size k, find first negative number.
     * If no negative, output 0.
     *
     * [-8, 2, 3, -6, 10], k=2
     * [-8, 2]   → -8
     * [2,  3]   →  0
     * [3, -6]   → -6
     * [-6, 10]  → -6
     * Output: [-8, 0, -6, -6]
     *
     * Deque stores indices of NEGATIVE numbers in current window.
     */
    static int[] firstNegativeInWindow(int[] nums, int k) {
        int n = nums.length;
        int[] result = new int[n - k + 1];
        ArrayDeque<Integer> dq = new ArrayDeque<>();  // indices of negatives

        for (int i = 0; i < n; i++) {
            // Add current index if negative
            if (nums[i] < 0) dq.addLast(i);

            // Remove front if it's outside current window
            while (!dq.isEmpty() && dq.peekFirst() < i - k + 1) {
                dq.pollFirst();
            }

            // Record result once window is fully formed
            if (i >= k - 1) {
                result[i - k + 1] = dq.isEmpty() ? 0 : nums[dq.peekFirst()];
            }
        }
        return result;
    }

    // ── 4. Deque as Stack and Queue ───────────────────────────────────────────
    static void dequeAsStackAndQueue() {
        System.out.println("\n=== 4. Deque as Stack and Queue ===");

        // As Stack (LIFO) — push/pop from front
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        stack.addFirst(1); stack.addFirst(2); stack.addFirst(3);
        System.out.print("Stack pop order: ");
        while (!stack.isEmpty()) System.out.print(stack.pollFirst() + " ");  // 3 2 1
        System.out.println();

        // As Queue (FIFO) — add to back, remove from front
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.addLast(1); queue.addLast(2); queue.addLast(3);
        System.out.print("Queue poll order: ");
        while (!queue.isEmpty()) System.out.print(queue.pollFirst() + " ");  // 1 2 3
        System.out.println();
    }

    // ── Main ──────────────────────────────────────────────────────────────────
    public static void main(String[] args) {
        dequeApiDemo();

        System.out.println("\n=== 2. Sliding Window Maximum ===");
        int[] nums = {1, 3, -1, -3, 5, 3, 6, 7};
        System.out.println(Arrays.toString(maxSlidingWindow(nums, 3)));
        // [3, 3, 5, 5, 6, 7]

        System.out.println("\n=== 3. First Negative in Window ===");
        int[] arr = {-8, 2, 3, -6, 10};
        System.out.println(Arrays.toString(firstNegativeInWindow(arr, 2)));
        // [-8, 0, -6, -6]

        dequeAsStackAndQueue();
    }
}
