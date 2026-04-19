
class BinarySearchIterative {

    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 7, 9, 11, 15, 20, 34};  // must be sorted for binary search

        int target = 11;
        int result = binarySearch(arr, target, 0, arr.length - 1);

        if (result != -1) {
            System.out.println("Found " + target + " at index " + result);
        } else {
            System.out.println(target + " not found");
        }
    }

    // returns index of target, or -1 if not found
    static int binarySearch(int[] arr, int target, int start, int end) {
        if (start > end) {
            return -1;  // base case — search space exhausted
        }

        int mid = start + (end - start) / 2;  // safe mid (avoids overflow)

        System.out.println("Searching: start=" + start + " mid=" + mid + " end=" + end + " → arr[mid]=" + arr[mid]);

        if (arr[mid] == target) {
            return mid;                                   // found
        } else if (arr[mid] < target) {
            System.out.println("  → go RIGHT (target is bigger)");
            return binarySearch(arr, target, mid + 1, end);   // go right
        } else {
            System.out.println("  → go LEFT (target is smaller)");
            return binarySearch(arr, target, start, mid - 1); // go left
        }
    }
}