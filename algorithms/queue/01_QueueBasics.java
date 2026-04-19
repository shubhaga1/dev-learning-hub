import java.util.*;

/**
 * QUEUE — First In First Out (FIFO)
 *
 * Mental model: ticket counter — first person in line gets served first.
 *
 * Java interfaces:
 *   Queue<E>  — standard FIFO queue
 *   Deque<E>  — double-ended queue (can add/remove from both ends)
 *               ArrayDeque implements both Queue and Deque
 *
 * Key operations:
 *   offer(x)  → add to back  (returns false if full, doesn't throw)
 *   poll()    → remove from front (returns null if empty, doesn't throw)
 *   peek()    → look at front (returns null if empty)
 *
 *   add(x)    → like offer but throws if full
 *   remove()  → like poll but throws if empty
 *   element() → like peek but throws if empty
 *
 * WHY ArrayDeque over LinkedList?
 *   LinkedList: extra memory per node (pointer overhead)
 *   ArrayDeque: array-backed, cache-friendly, faster in practice
 *   Rule: always use ArrayDeque unless you need null elements
 *
 * WHERE queues appear in interviews:
 *   BFS (tree level order, shortest path in grid)
 *   Sliding window problems (Deque for monotonic window)
 *   Producer-consumer simulation
 *   Task scheduling
 */
class QueueBasics {

    // ── 1. Queue API demo ─────────────────────────────────────────────────────
    static void queueApiDemo() {
        System.out.println("=== 1. Queue API ===");
        Queue<Integer> queue = new ArrayDeque<>();

        queue.offer(10);
        queue.offer(20);
        queue.offer(30);
        System.out.println("Queue after 3 offers: " + queue);   // [10, 20, 30]

        System.out.println("peek():  " + queue.peek());          // 10 — front, not removed
        System.out.println("poll():  " + queue.poll());          // 10 — removed
        System.out.println("After poll: " + queue);             // [20, 30]
        System.out.println("size():  " + queue.size());
        System.out.println("isEmpty: " + queue.isEmpty());
    }

    // ── 2. BFS — Level Order Traversal (Amazon/Google very common) ────────────
    /**
     * Level order traversal using a Queue.
     * Pattern: process node → enqueue its children → repeat.
     *
     * Input tree:
     *       1
     *      / \
     *     2   3
     *    / \   \
     *   4   5   6
     *
     * Output: [[1], [2,3], [4,5,6]]
     */
    static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();     // snapshot size BEFORE processing level
            List<Integer> level = new ArrayList<>();

            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);

                if (node.left  != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            result.add(level);
        }
        return result;
    }

    // ── 3. BFS in Grid — Shortest Path (Amazon/Google) ───────────────────────
    /**
     * Find shortest path from top-left (0,0) to bottom-right (n-1,m-1).
     * 0 = open, 1 = wall.
     * Returns number of steps, or -1 if no path.
     *
     * BFS guarantees shortest path in unweighted graphs.
     * (DFS would find A path but not necessarily shortest.)
     */
    static int shortestPath(int[][] grid) {
        int n = grid.length, m = grid[0].length;
        if (grid[0][0] == 1 || grid[n-1][m-1] == 1) return -1;

        int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
        boolean[][] visited = new boolean[n][m];

        Queue<int[]> queue = new ArrayDeque<>();
        queue.offer(new int[]{0, 0});
        visited[0][0] = true;
        int steps = 0;

        while (!queue.isEmpty()) {
            int size = queue.size();
            steps++;

            for (int i = 0; i < size; i++) {
                int[] curr = queue.poll();
                int r = curr[0], c = curr[1];

                if (r == n-1 && c == m-1) return steps;

                for (int[] d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < m
                            && !visited[nr][nc] && grid[nr][nc] == 0) {
                        visited[nr][nc] = true;
                        queue.offer(new int[]{nr, nc});
                    }
                }
            }
        }
        return -1;
    }

    // ── 4. Implement Queue using Two Stacks (Amazon classic) ─────────────────
    /**
     * Queue using two stacks.
     * Key insight: reverse a stack by pushing into another stack.
     *
     * inbox  = newly added items (top = most recent)
     * outbox = ready to serve (top = oldest)
     *
     * Transfer inbox → outbox ONLY when outbox is empty.
     * Amortized O(1) per operation.
     */
    static class MyQueue {
        private Stack<Integer> inbox  = new Stack<>();  // for push
        private Stack<Integer> outbox = new Stack<>();  // for pop/peek

        void push(int x) {
            inbox.push(x);
        }

        int pop() {
            refill();
            return outbox.pop();
        }

        int peek() {
            refill();
            return outbox.peek();
        }

        boolean isEmpty() {
            return inbox.isEmpty() && outbox.isEmpty();
        }

        // Transfer only when outbox empty — keeps order stable
        private void refill() {
            if (outbox.isEmpty()) {
                while (!inbox.isEmpty()) {
                    outbox.push(inbox.pop());
                }
            }
        }
    }

    // ── Helper: build tree ────────────────────────────────────────────────────
    static class TreeNode {
        int val; TreeNode left, right;
        TreeNode(int v) { val = v; }
    }

    static TreeNode buildTree() {
        TreeNode root = new TreeNode(1);
        root.left  = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left  = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.right = new TreeNode(6);
        return root;
    }

    // ── Main ──────────────────────────────────────────────────────────────────
    public static void main(String[] args) {
        queueApiDemo();

        System.out.println("\n=== 2. BFS Level Order ===");
        System.out.println(levelOrder(buildTree()));   // [[1], [2, 3], [4, 5, 6]]

        System.out.println("\n=== 3. Shortest Path in Grid ===");
        int[][] grid = {
            {0, 0, 1, 0},
            {0, 0, 0, 1},
            {1, 0, 0, 0}
        };
        System.out.println("Steps: " + shortestPath(grid));   // 6

        System.out.println("\n=== 4. Queue using Two Stacks ===");
        MyQueue q = new MyQueue();
        q.push(1); q.push(2); q.push(3);
        System.out.println("peek: " + q.peek());   // 1
        System.out.println("pop:  " + q.pop());    // 1
        System.out.println("pop:  " + q.pop());    // 2
        q.push(4);
        System.out.println("pop:  " + q.pop());    // 3
        System.out.println("pop:  " + q.pop());    // 4
    }
}
