/**
 * Sudoku Solver — backtracking
 * Try digits 1-9 in each empty cell ('.'), backtrack if invalid.
 */
class Sudoku {

    static boolean isSafe(char[][] board, int row, int col, int number) {
        char ch = (char) (number + '0');

        for (int i = 0; i < 9; i++) {
            if (board[i][col] == ch) return false;    // same column
            if (board[row][i] == ch) return false;    // same row
        }

        // check 3x3 box
        int startRow = 3 * (row / 3);
        int startCol = 3 * (col / 3);
        for (int i = startRow; i < startRow + 3; i++)
            for (int j = startCol; j < startCol + 3; j++)
                if (board[i][j] == ch) return false;

        return true;
    }

    static boolean solve(char[][] board, int row, int col) {
        if (row == 9) return true;                    // all rows filled — solved

        int nextRow = (col == 8) ? row + 1 : row;
        int nextCol = (col == 8) ? 0 : col + 1;

        if (board[row][col] != '.') return solve(board, nextRow, nextCol);  // skip pre-filled

        for (int num = 1; num <= 9; num++) {
            if (isSafe(board, row, col, num)) {
                board[row][col] = (char) (num + '0');
                if (solve(board, nextRow, nextCol)) return true;
                board[row][col] = '.';                // backtrack
            }
        }
        return false;
    }

    static void print(char[][] board) {
        for (char[] row : board) {
            for (char c : row) System.out.print(c + " ");
            System.out.println();
        }
    }

    public static void main(String[] args) {
        char[][] board = {
            {'5','3','.','.','7','.','.','.','.'},
            {'6','.','.','1','9','5','.','.','.'},
            {'.','9','8','.','.','.','.','6','.'},
            {'8','.','.','.','6','.','.','.','3'},
            {'4','.','.','8','.','3','.','.','1'},
            {'7','.','.','.','2','.','.','.','6'},
            {'.','6','.','.','.','.','2','8','.'},
            {'.','.','.','4','1','9','.','.','5'},
            {'.','.','.','.','8','.','.','7','9'}
        };

        if (solve(board, 0, 0)) print(board);
        else System.out.println("No solution");
    }
}
