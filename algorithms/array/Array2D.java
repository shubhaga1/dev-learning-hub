import java.util.Scanner;

class Array2D {

    public static void main(String[] args) {

        // arr2DBasic();
        arr2DIntermediate();
    }

    static void arr2DIntermediate() {
        int[][] arr = new int[3][];

        try (Scanner in = new Scanner(System.in)) {
            for (int row = 0; row < arr.length; row++) {
                for (int col = 0; col < arr[row].length; col++) {
                    arr[row][col] = in.nextInt();
                }
            }
        }

        for (int row[] : arr) {
            for (int cell : row) {
                System.out.println(cell);
            }
        }

    }

    static void arr2DBasic() {
        int[][] arr = {
                { 1, 2, 3 },
                { 4, 5, 6 },
                { 7, 8, 9 }
        };

        // ── for-each: row by row, then each element ───────────────────────────
        // row is int[] (one row), cell is int (one element)
        System.out.println("for-each:");
        for (int[] row : arr) {
            for (int cell : row) {
                System.out.print(cell + " ");
            }
            System.out.println();
        }

        // ── regular for loop: access by index ─────────────────────────────────
        // useful when you need the index (i, j) to do calculations
        System.out.println("\nfor loop with index:");
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr[i].length; j++) {
                System.out.print("arr[" + i + "][" + j + "]=" + arr[i][j] + "  ");
            }
            System.out.println();
        }

    }
}
