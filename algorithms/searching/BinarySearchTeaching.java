import java.util.Arrays;
import java.util.Scanner;

class BinarySearchTeaching {

    public static void main(String[] args) {
        int[] ar = {6, 4, 7, 8, 2, 3};
        Arrays.sort(ar);                              // binary search requires sorted array
        System.out.println("Enter value you need to check");
        try (Scanner sc = new Scanner(System.in)) {
            int find = sc.nextInt();
            int result = binary(ar, 0, ar.length - 1, find);
            if (result == -1) System.out.println(find + " not found");
            else System.out.println(find + " found at index " + result);
        }
    }

    // O(log n) — halves search space each call
    public static int binary(int[] ar, int l, int h, int find) {
        if (l > h) return -1;                         // base case — not found

        int mid = l + (h - l) / 2;                   // avoids overflow vs (l+h)/2

        if (find == ar[mid]) return mid;              // found
        if (find > ar[mid])  return binary(ar, mid + 1, h, find);    // go right
        return binary(ar, l, mid - 1, find);          // go left
    }
}
