
import java.util.ArrayList;

/**
 * Maze — Approach 1: Pure Recursion
 *
 * Question: how many ways can you go from (3,3) to (1,1)?
 * Moves allowed: UP (row-1) or LEFT (col-1) only.
 *
 * Key idea:
 *   ways(row, col) = ways(row-1, col) + ways(row, col-1)
 *   Base case: (1,1) = 1 way (you're already there)
 *
 * Problem: same subproblems computed repeatedly → see Maze2Memoization for fix
 */
class Maze1Recursive {

    // Count: how many paths exist from (row,col) to (1,1)?
    static int count(int row, int col) {
        if (row == 1 && col == 1) return 1;  // reached — 1 valid path
        if (row < 1  || col < 1)  return 0;  // out of bounds — dead end

        return count(row - 1, col)            // move up
             + count(row, col - 1);           // move left
    }

    // Print: what are the actual paths?
    // p builds the path string as we go: D = up (row-1), R = left (col-1)
    static void printPaths(String p, int row, int col) {
        if (row == 1 && col == 1) {
            System.out.println(p);            // print completed path
            return;
        }

        if (row > 1) printPaths(p + "D", row - 1, col);  // move up
        if (col > 1) printPaths(p + "R", row, col - 1);  // move left
    }

    // Collect: return all paths as a list — useful when you need to process them further
    // Same logic as printPaths but bubbles results up via ArrayList instead of printing
    static ArrayList<String> collectPaths(String p, int row, int col) {
        ArrayList<String> result = new ArrayList<>();

        if (row == 1 && col == 1) {
            result.add(p);            // store completed path
            return result;
        }

        if (row > 1) result.addAll(collectPaths(p + "D", row - 1, col));  // merge up paths
        if (col > 1) result.addAll(collectPaths(p + "R", row, col - 1));  // merge left paths

        return result;
    }

    // Collect with diagonal move (V = move up-left diagonally)
    static ArrayList<String> collectPathsDiagnal(String p, int row, int col) {
        ArrayList<String> result = new ArrayList<>();

        if (row == 1 && col == 1) {
            result.add(p);
            return result;
        }

        if (row > 1)            result.addAll(collectPathsDiagnal(p + "D", row - 1, col));      // up
        if (row > 1 && col > 1) result.addAll(collectPathsDiagnal(p + "V", row - 1, col - 1)); // diagonal
        if (col > 1)            result.addAll(collectPathsDiagnal(p + "R", row, col - 1));      // left

        return result;
    }

    // Print a single path visually on the grid
    // * = cell on the path,  . = not visited
    static void printVisual(String path, int rows, int cols) {
        boolean[][] visited = new boolean[rows + 1][cols + 1];
        int r = rows, c = cols;
        visited[r][c] = true;                       // mark start

        for (char move : path.toCharArray()) {
            if      (move == 'D') r--;              // move up
            else if (move == 'R') c--;              // move left
            else if (move == 'V') { r--; c--; }    // move diagonal
            visited[r][c] = true;
        }

        System.out.println("Path: " + path);
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= cols; j++) {
                System.out.print(visited[i][j] ? " * " : " . ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void main(String[] args) {
        int row = 3, col = 3;

        System.out.println("=== Without diagonal (D=up, R=left) ===\n");
        for (String path : collectPaths("", row, col)) {
            printVisual(path, row, col);
        }

        System.out.println("=== With diagonal (D=up, R=left, V=diagonal) ===\n");
        ArrayList<String> diagonalPaths = collectPathsDiagnal("", row, col);
        for (String path : diagonalPaths) {
            printVisual(path, row, col);
        }
        System.out.println("Total diagonal paths: " + diagonalPaths.size());
    }
}
