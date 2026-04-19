import java.util.ArrayList;
import java.util.Collections;

/**
 * ArrayList — max, swap, reverse operations
 */
class ArrayListUtils {

    // ── Max ───────────────────────────────────────────────────────────────────
    static int max(ArrayList<Integer> list) {
        int max = list.get(0);
        for (int n : list) {
            if (n > max) max = n;
        }
        return max;
    }

    // ── Swap two elements by index ────────────────────────────────────────────
    static void swap(ArrayList<Integer> list, int i, int j) {
        int temp = list.get(i);
        list.set(i, list.get(j));
        list.set(j, temp);
    }

    // ── Reverse manually ──────────────────────────────────────────────────────
    static void reverse(ArrayList<Integer> list) {
        int left = 0, right = list.size() - 1;
        while (left < right) {
            swap(list, left, right);
            left++;
            right--;
        }
    }

    public static void main(String[] args) {
        ArrayList<Integer> list = new ArrayList<>();
        list.add(3); list.add(1); list.add(7); list.add(2); list.add(9);

        System.out.println("List:            " + list);
        System.out.println("Max:             " + max(list));                    // 9
        System.out.println("Collections.max: " + Collections.max(list));       // 9 — built-in

        swap(list, 0, 4);
        System.out.println("After swap(0,4): " + list);                        // [9,1,7,2,3]

        reverse(list);
        System.out.println("After reverse:   " + list);                        // [3,2,7,1,9]

        Collections.reverse(list);
        System.out.println("Collections.rev: " + list);                        // [9,1,7,2,3] — built-in
    }
}
