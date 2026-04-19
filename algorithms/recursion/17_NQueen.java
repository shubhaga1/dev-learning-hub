/**
 * N-Queens Problem — place N queens on an NxN board so no two attack each other
 *
 * A queen attacks in same row, column, or diagonal.
 *
 * Approach: backtracking
 *   - Place queen row by row
 *   - For each row, try every column
 *   - If safe, place and recurse to next row
 *   - If not safe or no solution found, backtrack (remove queen)
 */
class NQueen {

    static int n;
    static int[] board; // board[row] = col where queen is placed in that row

    static boolean isSafe(int row, int col) {
        for (int r = 0; r < row; r++) {
            int c = board[r];
            if (c == col) return false;               // same column
            if (Math.abs(r - row) == Math.abs(c - col)) return false;  // same diagonal
        }
        return true;
    }

    static void solve(int row) {
        if (row == n) {
            printBoard();
            return;
        }
        for (int col = 0; col < n; col++) {
            if (isSafe(row, col)) {
                board[row] = col;     // place queen
                solve(row + 1);       // recurse to next row
                board[row] = -1;      // backtrack — remove queen
            }
        }
    }

    static void printBoard() {
        System.out.println("Solution:");
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                System.out.print(board[r] == c ? " Q " : " . ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void main(String[] args) {
        n = 4;
        board = new int[n];
        solve(0);
    }
}
