
import java.util.ArrayList;
import java.util.List;

/**
 * Q3: Comments — explain WHY, not WHAT
 *
 * Level 1 → commenting the obvious (insults the reader)
 * Level 2 → missing the important WHY (comment explains what, not why)
 * Level 3 → outdated comment that contradicts the code
 * Level 4 → good comment: explains non-obvious business logic
 *
 * Rule: if removing the comment makes the code no harder to understand,
 *       the comment shouldn't be there.
 */
class Q3_Comments {

    // ── Level 1: Commenting the obvious ──────────────────────────────────────

    // BAD: every line narrated — adds noise, no value
    static int add_BAD(int a, int b) {
        int result = a + b;   // add a and b
        return result;        // return the result
    }

    // GOOD: no comment needed — the code IS the documentation
    static int add_GOOD(int a, int b) {
        return a + b;
    }

    // ── Level 2: Comment says WHAT, not WHY ──────────────────────────────────

    // BAD: comment describes the operation, not the reason
    static List<Integer> getActiveUsers_BAD(List<Integer> userIds) {
        List<Integer> result = new ArrayList<>();
        for (int id : userIds) {
            if (id > 1000) {          // check if id > 1000
                result.add(id);
            }
        }
        return result;
    }

    // GOOD: comment explains the business rule behind the magic number
    static List<Integer> getActiveUsers_GOOD(List<Integer> userIds) {
        List<Integer> result = new ArrayList<>();
        for (int id : userIds) {
            if (id > 1000) {          // legacy users (id ≤ 1000) were migrated to v2 system
                result.add(id);       // and must not appear in v1 active user lists
            }
        }
        return result;
    }

    // ── Level 3: Outdated comment — lies to the reader ───────────────────────

    // BAD: comment says "ascending" but code sorts descending — comment was never updated
    static void sort_BAD(int[] arr) {
        // sort in ascending order
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[i] < arr[j]) {   // ← descending, not ascending
                    int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
                }
            }
        }
    }

    // GOOD: comment matches reality, or better — name makes it obvious
    static void sortDescending_GOOD(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[i] < arr[j]) {
                    int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
                }
            }
        }
    }

    // ── Level 4: Good comment — explains non-obvious logic ───────────────────

    // GOOD: without the comment, the +1 looks like a bug
    static int binarySearchInsertionPoint(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;   // avoids int overflow vs (lo+hi)/2
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return lo;   // lo is the insertion point when target is not found
    }

    // GOOD: explains the off-by-one that every developer trips over
    static int lastIndex(int[] arr) {
        return arr.length - 1;   // -1 because arrays are 0-indexed: arr[length] is out of bounds
    }

    public static void main(String[] args) {
        System.out.println("=== Level 1: add ===");
        System.out.println(add_GOOD(3, 4));

        System.out.println("\n=== Level 2: active users ===");
        List<Integer> users = List.of(500, 1001, 1500, 200, 2000);
        System.out.println("Active: " + getActiveUsers_GOOD(users));

        System.out.println("\n=== Level 3: sort ===");
        int[] arr = {3, 1, 4, 1, 5, 9};
        sortDescending_GOOD(arr);
        System.out.print("Sorted desc: ");
        for (int n : arr) System.out.print(n + " ");
        System.out.println();

        System.out.println("\n=== Level 4: binary search ===");
        int[] sorted = {1, 3, 5, 7, 9};
        System.out.println("Insert point for 6: " + binarySearchInsertionPoint(sorted, 6));  // 3
        System.out.println("Last index: " + lastIndex(sorted));  // 4
    }
}
