/**
 * Rat in a Maze — find all paths from (0,0) to (n-1,n-1)
 *
 * Rules:
 *   - 1 = open cell, 0 = blocked cell
 *   - Moves allowed: Down, Left, Right, Up (alphabetical)
 *   - Cannot revisit a cell in the same path
 *
 * Approach: backtracking
 *   - Mark cell as visited before recursing
 *   - Unmark (backtrack) after recursing
 */
class RatInAMaze {

    static int n;
    static int[][] maze;
    static boolean[][] visited;

    static int[] dr = {1,  0, 0, -1};   // Down, Left, Right, Up — row deltas
    static int[] dc = {0, -1, 1,  0};   // Down, Left, Right, Up — col deltas
    static char[] dir = {'D', 'L', 'R', 'U'};

    static void solve(int row, int col, String path) {
        if (row == n - 1 && col == n - 1) {
            System.out.println(path);    // reached destination
            return;
        }

        for (int i = 0; i < 4; i++) {
            int nr = row + dr[i];
            int nc = col + dc[i];

            if (nr >= 0 && nc >= 0 && nr < n && nc < n
                    && maze[nr][nc] == 1 && !visited[nr][nc]) {
                visited[nr][nc] = true;
                solve(nr, nc, path + dir[i]);
                visited[nr][nc] = false;  // backtrack
            }
        }
    }

    public static void main(String[] args) {
        n = 4;
        maze = new int[][] {
            {1, 0, 0, 0},
            {1, 1, 0, 1},
            {1, 1, 0, 0},
            {0, 1, 1, 1}
        };

        visited = new boolean[n][n];
        visited[0][0] = true;

        System.out.println("All paths from (0,0) to (" + (n-1) + "," + (n-1) + "):");
        solve(0, 0, "");
    }
}
