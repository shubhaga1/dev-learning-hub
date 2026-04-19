
/**
 * Maze — Approach 2: Memoization (Top-Down DP)
 *
 * Problem with Approach 1:
 *   count(2,2) is computed multiple times — once via (3,2) and once via (2,3).
 *   For large grids this explodes exponentially.
 *
 * Fix: store result the first time, return cached value on repeat calls.
 *   memo[row][col] = 0  means "not computed yet"
 *   memo[row][col] > 0  means "already computed — return this"
 *
 * Same recursion as Approach 1, just one extra line: check cache before computing.
 */
class Maze2Memoization {

    static int count(int row, int col, int[][] memo) {
        if (row == 1 && col == 1) return 1;
        if (row < 1  || col < 1)  return 0;

        if (memo[row][col] != 0) return memo[row][col];  // already computed — reuse

        memo[row][col] = count(row - 1, col, memo)
                       + count(row, col - 1, memo);
        return memo[row][col];
    }

    public static void main(String[] args) {
        int row = 3, col = 3;
        int[][] memo = new int[row + 1][col + 1];  // 0-indexed ignored, 1-indexed used

        System.out.println("Total paths (memoized): " + count(row, col, memo));

        // Print what got cached — each cell shows how many paths lead to (1,1)
        System.out.println("\nCache (memo table):");
        for (int r = 1; r <= row; r++) {
            for (int c = 1; c <= col; c++) {
                System.out.printf("%3d", memo[r][c]);
            }
            System.out.println();
        }
        // Note: memo[1][1] stays 0 because base case returns before storing
    }
}
