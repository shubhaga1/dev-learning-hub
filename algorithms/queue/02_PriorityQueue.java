import java.util.*;

/**
 * PRIORITY QUEUE — always gives you the highest-priority element first.
 *
 * Mental model: emergency room — most critical patient seen first, not FIFO.
 *
 * Java PriorityQueue:
 *   Default = MIN heap (smallest element at top)
 *   Max heap = reverse with: new PriorityQueue<>(Collections.reverseOrder())
 *
 * Internals (Min Heap):
 *   Binary tree stored in array. Parent always <= children.
 *   Insert: add at end, bubble UP  → O(log n)
 *   Poll:   remove root, bubble DOWN → O(log n)
 *   Peek:   just look at index 0    → O(1)
 *
 *        1         ← root (minimum)
 *       / \
 *      3   2
 *     / \   \
 *    7   4   5
 *
 * WHERE PriorityQueue appears in interviews:
 *   Top K frequent elements (Amazon, Google)
 *   Merge K sorted lists   (Amazon, Google)
 *   Kth largest/smallest   (Amazon very common)
 *   Task scheduler
 *   Dijkstra shortest path
 *   Meeting rooms
 */
class PriorityQueueProblems {

    // ── 1. PQ API demo ────────────────────────────────────────────────────────
    static void pqApiDemo() {
        System.out.println("=== 1. PriorityQueue API ===");

        // Min heap (default)
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.offer(5); minHeap.offer(1); minHeap.offer(3);
        System.out.println("Min heap poll order: " + minHeap.poll() + ", "
                + minHeap.poll() + ", " + minHeap.poll());   // 1, 3, 5

        // Max heap
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.offer(5); maxHeap.offer(1); maxHeap.offer(3);
        System.out.println("Max heap poll order: " + maxHeap.poll() + ", "
                + maxHeap.poll() + ", " + maxHeap.poll());   // 5, 3, 1

        // Custom comparator — by string length
        PriorityQueue<String> byLength = new PriorityQueue<>(
                Comparator.comparingInt(String::length));
        byLength.offer("banana"); byLength.offer("fig"); byLength.offer("apple");
        System.out.println("By length: " + byLength.poll() + ", "
                + byLength.poll() + ", " + byLength.poll());  // fig, apple, banana
    }

    // ── 2. Kth Largest Element (Amazon #1 most asked) ─────────────────────────
    /**
     * Find kth largest in unsorted array.
     *
     * Approach: min heap of size k.
     *   - Keep only k largest seen so far.
     *   - Heap top = kth largest (smallest of the top-k).
     *
     * [3,2,1,5,6,4], k=2 → answer: 5
     *
     * Time: O(n log k)   Space: O(k)
     * Better than sorting: O(n log n)
     */
    static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();

        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();    // remove smallest — keep only top k
            }
        }
        return minHeap.peek();     // smallest of top-k = kth largest
    }

    // ── 3. Top K Frequent Elements (Amazon, Google) ───────────────────────────
    /**
     * [1,1,1,2,2,3], k=2 → [1, 2]   (most frequent elements)
     *
     * Approach:
     *   1. Count frequencies with HashMap
     *   2. Min heap of size k — keyed by frequency
     *   3. Heap top = kth most frequent (prune less frequent)
     *
     * Time: O(n log k)
     */
    static int[] topKFrequent(int[] nums, int k) {
        // Step 1: count frequencies
        Map<Integer, Integer> freq = new HashMap<>();
        for (int n : nums) freq.merge(n, 1, Integer::sum);

        // Step 2: min heap ordered by frequency
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(
                Comparator.comparingInt(freq::get));   // compare by frequency value

        for (int num : freq.keySet()) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();    // remove least frequent
            }
        }

        // Step 3: extract result
        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = minHeap.poll();
        return result;
    }

    // ── 4. Merge K Sorted Lists (Google, Amazon) ──────────────────────────────
    /**
     * Merge k sorted linked lists into one sorted list.
     *
     * Naive: merge two at a time → O(nk) time
     * Better: use min heap of size k → O(n log k)
     *
     * Approach:
     *   1. Push head of each list into min heap (ordered by node value)
     *   2. Poll min node → add to result → push its next into heap
     *   3. Repeat until heap empty
     *
     * [1→4→5]
     * [1→3→4]  →  1→1→2→3→4→4→5→6
     * [2→6]
     */
    static ListNode mergeKLists(ListNode[] lists) {
        // Min heap: compare nodes by value
        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
                Comparator.comparingInt(n -> n.val));

        // Seed heap with head of each list
        for (ListNode head : lists) {
            if (head != null) minHeap.offer(head);
        }

        ListNode dummy = new ListNode(0);   // dummy head simplifies edge cases
        ListNode curr = dummy;

        while (!minHeap.isEmpty()) {
            ListNode smallest = minHeap.poll();
            curr.next = smallest;
            curr = curr.next;

            if (smallest.next != null) {
                minHeap.offer(smallest.next);   // push next node of this list
            }
        }
        return dummy.next;
    }

    // ── 5. Meeting Rooms II — Min Rooms Needed (Amazon) ──────────────────────
    /**
     * Given meetings as [start, end] intervals, find min meeting rooms needed.
     *
     * [0,30],[5,10],[15,20] → 2 rooms
     *
     * Approach:
     *   Sort by start time.
     *   Min heap of end times (when does earliest meeting finish?).
     *   If next meeting starts after earliest end → reuse that room (poll, push new end).
     *   Otherwise → need new room (just push new end).
     *
     * Time: O(n log n)  Space: O(n)
     */
    static int minMeetingRooms(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));  // sort by start

        PriorityQueue<Integer> endTimes = new PriorityQueue<>();     // min heap of end times

        for (int[] meeting : intervals) {
            int start = meeting[0], end = meeting[1];

            if (!endTimes.isEmpty() && endTimes.peek() <= start) {
                endTimes.poll();    // free up the room that finished earliest
            }
            endTimes.offer(end);    // assign this meeting to a room
        }
        return endTimes.size();     // rooms still occupied = min rooms needed
    }

    // ── Helper classes ────────────────────────────────────────────────────────
    static class ListNode {
        int val; ListNode next;
        ListNode(int v) { val = v; }
    }

    static ListNode buildList(int... vals) {
        ListNode dummy = new ListNode(0), curr = dummy;
        for (int v : vals) { curr.next = new ListNode(v); curr = curr.next; }
        return dummy.next;
    }

    static String listToString(ListNode head) {
        StringBuilder sb = new StringBuilder();
        while (head != null) { sb.append(head.val).append("→"); head = head.next; }
        return sb.length() > 0 ? sb.substring(0, sb.length()-1) : "null";
    }

    // ── Main ──────────────────────────────────────────────────────────────────
    public static void main(String[] args) {
        pqApiDemo();

        System.out.println("\n=== 2. Kth Largest ===");
        System.out.println(findKthLargest(new int[]{3,2,1,5,6,4}, 2));  // 5
        System.out.println(findKthLargest(new int[]{3,2,3,1,2,4,5,5,6}, 4));  // 4

        System.out.println("\n=== 3. Top K Frequent ===");
        System.out.println(Arrays.toString(topKFrequent(new int[]{1,1,1,2,2,3}, 2)));  // [1,2]

        System.out.println("\n=== 4. Merge K Sorted Lists ===");
        ListNode[] lists = {
            buildList(1, 4, 5),
            buildList(1, 3, 4),
            buildList(2, 6)
        };
        System.out.println(listToString(mergeKLists(lists)));  // 1→1→2→3→4→4→5→6

        System.out.println("\n=== 5. Meeting Rooms II ===");
        int[][] meetings = {{0,30},{5,10},{15,20}};
        System.out.println("Min rooms: " + minMeetingRooms(meetings));  // 2
    }
}
