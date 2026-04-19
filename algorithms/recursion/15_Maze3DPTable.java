
/**
 * Maze — Approach 3: Bottom-Up DP Table
 *
 * Instead of starting at (3,3) and recursing down (top-down),
 * start at (1,1) and build up the answer iteratively (bottom-up).
 *
 * Rule:
 *   dp[r][c] = number of ways to reach (r,c) FROM (1,1)
 *   dp[r][c] = dp[r-1][c] + dp[r][c-1]
 *              (came from above) + (came from left)
 *
 * Base cases:
 *   Row 1:  can only be reached by moving right  → all = 1
 *   Col 1:  can only be reached by moving down   → all = 1
 *
 * No recursion, no stack — just a grid fill.
 */
class Maze3DPTable {

    static int count(int rows, int cols) {
        int[][] dp = new int[rows + 1][cols + 1];

        for (int c = 1; c <= cols; c++) dp[1][c] = 1;  // top row — only 1 way
        for (int r = 1; r <= rows; r++) dp[r][1] = 1;  // left col — only 1 way

        for (int r = 2; r <= rows; r++) {
            for (int c = 2; c <= cols; c++) {
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1];
            }
        }

        printTable(dp, rows, cols);
        return dp[rows][cols];
    }

    static void printTable(int[][] dp, int rows, int cols) {
        System.out.println("DP table — each cell = number of paths from (1,1) to that cell:");
        System.out.println("     col1 col2 col3");
        for (int r = 1; r <= rows; r++) {
            System.out.print("row" + r + " ");
            for (int c = 1; c <= cols; c++) {
                System.out.printf("%4d ", dp[r][c]);
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        int rows = 3, cols = 3;
        int total = count(rows, cols);
        System.out.println("\nTotal paths from (1,1) to (" + rows + "," + cols + "): " + total);
    }
}
