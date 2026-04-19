import java.util.*;

/**
 * QUEUE INTERVIEW PATTERNS — Amazon & Google cheat sheet
 *
 * Pattern recognition:
 *   "level by level"           → BFS Queue
 *   "shortest path"            → BFS Queue
 *   "top K / kth largest"      → PriorityQueue (min heap size k)
 *   "sliding window max/min"   → Monotonic Deque
 *   "merge sorted lists"       → PriorityQueue
 *   "schedule by priority"     → PriorityQueue
 *   "rotting oranges / islands" → BFS Queue (multi-source)
 *
 * AMAZON MOST ASKED:
 *   - Kth Largest Element
 *   - Top K Frequent Elements
 *   - Sliding Window Maximum
 *   - Merge K Sorted Lists
 *   - Meeting Rooms II
 *   - Rotting Oranges (multi-source BFS)
 *
 * GOOGLE MOST ASKED:
 *   - Sliding Window Maximum
 *   - Merge K Sorted Lists
 *   - Word Ladder (BFS)
 *   - Trapping Rain Water (Deque/Stack)
 *   - Task Scheduler (PriorityQueue)
 */
class InterviewPatterns {

    // ── 1. Rotting Oranges — Multi-source BFS (Amazon, Google) ───────────────
    /**
     * Grid: 0=empty, 1=fresh, 2=rotten.
     * Every minute, rotten orange infects adjacent fresh oranges.
     * Return min minutes to rot all oranges, or -1 if impossible.
     *
     * KEY INSIGHT: Multi-source BFS — start ALL rotten oranges simultaneously.
     * This is NOT single-source BFS. All rotten oranges are in the queue at t=0.
     *
     * [[2,1,1],[1,1,0],[0,1,1]] → 4
     */
    static int orangesRotting(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        Queue<int[]> queue = new ArrayDeque<>();
        int freshCount = 0;

        // Seed: ALL rotten oranges start at time 0
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) queue.offer(new int[]{r, c});
                if (grid[r][c] == 1) freshCount++;
            }
        }

        if (freshCount == 0) return 0;   // nothing to rot

        int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
        int minutes = 0;

        while (!queue.isEmpty() && freshCount > 0) {
            minutes++;
            int size = queue.size();

            for (int i = 0; i < size; i++) {
                int[] curr = queue.poll();
                for (int[] d : dirs) {
                    int nr = curr[0] + d[0], nc = curr[1] + d[1];
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                            && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2;   // infect
                        freshCount--;
                        queue.offer(new int[]{nr, nc});
                    }
                }
            }
        }
        return freshCount == 0 ? minutes : -1;
    }

    // ── 2. Task Scheduler (Amazon, Google) ────────────────────────────────────
    /**
     * Given tasks (chars), cooldown n between same tasks.
     * Return minimum time to finish all tasks.
     *
     * tasks = ['A','A','A','B','B','B'], n = 2
     * Order: A B idle A B idle A B → 8
     *
     * Greedy + MaxHeap:
     *   Always execute most frequent remaining task.
     *   If no task available within cooldown → idle.
     *
     * Time: O(t log t)  where t = unique tasks
     */
    static int leastInterval(char[] tasks, int n) {
        // Count frequencies
        int[] freq = new int[26];
        for (char t : tasks) freq[t - 'A']++;

        // Max heap — always pick most frequent task
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        for (int f : freq) if (f > 0) maxHeap.offer(f);

        int time = 0;
        // Queue holds (remaining_count, available_at_time) for cooling tasks
        Queue<int[]> cooldown = new ArrayDeque<>();

        while (!maxHeap.isEmpty() || !cooldown.isEmpty()) {
            time++;

            if (!maxHeap.isEmpty()) {
                int remaining = maxHeap.poll() - 1;
                if (remaining > 0) {
                    cooldown.offer(new int[]{remaining, time + n});  // available after cooldown
                }
            }

            // Release tasks whose cooldown has expired
            if (!cooldown.isEmpty() && cooldown.peek()[1] == time) {
                maxHeap.offer(cooldown.poll()[0]);
            }
        }
        return time;
    }

    // ── 3. Design Hit Counter (Amazon system design) ──────────────────────────
    /**
     * Count hits received in past 5 minutes (300 seconds).
     * hit(timestamp) — record a hit.
     * getHits(timestamp) — return hits in [timestamp-299, timestamp].
     *
     * Queue approach: store each hit timestamp, expire old ones.
     * Time: O(1) amortized  Space: O(hits in window)
     */
    static class HitCounter {
        private Queue<Integer> hits = new ArrayDeque<>();

        void hit(int timestamp) {
            hits.offer(timestamp);
        }

        int getHits(int timestamp) {
            // Remove hits outside the 300-second window
            while (!hits.isEmpty() && hits.peek() <= timestamp - 300) {
                hits.poll();
            }
            return hits.size();
        }
    }

    // ── 4. Number of Islands — BFS version (Amazon, Google) ──────────────────
    /**
     * Count islands in grid (1=land, 0=water).
     * BFS from each unvisited land cell, mark all connected land as visited.
     *
     * Time: O(rows × cols)
     */
    static int numIslands(char[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int islands = 0;
        int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1') {
                    islands++;
                    // BFS to mark entire island as visited
                    Queue<int[]> queue = new ArrayDeque<>();
                    queue.offer(new int[]{r, c});
                    grid[r][c] = '0';   // mark visited by setting to water

                    while (!queue.isEmpty()) {
                        int[] curr = queue.poll();
                        for (int[] d : dirs) {
                            int nr = curr[0]+d[0], nc = curr[1]+d[1];
                            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                                    && grid[nr][nc] == '1') {
                                grid[nr][nc] = '0';
                                queue.offer(new int[]{nr, nc});
                            }
                        }
                    }
                }
            }
        }
        return islands;
    }

    // ── 5. Quick Pattern Reference ────────────────────────────────────────────
    static void printPatterns() {
        System.out.println("""
        ╔══════════════════════════════════════════════════════════════╗
        ║           QUEUE PATTERN CHEAT SHEET                         ║
        ╠══════════════════════════════════════════════════════════════╣
        ║ Pattern               Structure          Key operation       ║
        ║──────────────────────────────────────────────────────────── ║
        ║ Level order BFS       Queue              poll + offer kids   ║
        ║ Shortest path grid    Queue              BFS with visited[]  ║
        ║ Multi-source BFS      Queue (all seeds)  seed all at once    ║
        ║ Kth largest           MinHeap (size k)   keep k, poll small  ║
        ║ Top K frequent        MinHeap (size k)   freq comparator     ║
        ║ Merge K sorted        MinHeap             poll min, push next ║
        ║ Sliding window max    Monotonic Deque    pollLast if smaller  ║
        ║ Task scheduler        MaxHeap + Cooldown  pick most frequent  ║
        ╚══════════════════════════════════════════════════════════════╝
        """);
    }

    // ── Main ──────────────────────────────────────────────────────────────────
    public static void main(String[] args) {
        System.out.println("=== 1. Rotting Oranges ===");
        int[][] grid = {{2,1,1},{1,1,0},{0,1,1}};
        System.out.println("Minutes: " + orangesRotting(grid));  // 4

        System.out.println("\n=== 2. Task Scheduler ===");
        char[] tasks = {'A','A','A','B','B','B'};
        System.out.println("Min time: " + leastInterval(tasks, 2));  // 8

        System.out.println("\n=== 3. Hit Counter ===");
        HitCounter counter = new HitCounter();
        counter.hit(1); counter.hit(2); counter.hit(3);
        System.out.println("Hits at t=4:   " + counter.getHits(4));    // 3
        counter.hit(300);
        System.out.println("Hits at t=300: " + counter.getHits(300));  // 4
        System.out.println("Hits at t=301: " + counter.getHits(301));  // 3 (t=1 expired)

        System.out.println("\n=== 4. Number of Islands ===");
        char[][] islandGrid = {
            {'1','1','0','0','0'},
            {'1','1','0','0','0'},
            {'0','0','1','0','0'},
            {'0','0','0','1','1'}
        };
        System.out.println("Islands: " + numIslands(islandGrid));  // 3

        System.out.println("\n=== 5. Interview Patterns ===");
        printPatterns();
    }
}
