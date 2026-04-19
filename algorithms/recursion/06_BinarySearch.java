/**
 * Binary Search — recursive
 * Requires a SORTED array. Halves search space each call.
 * Time: O(log n)  Space: O(log n) call stack
 */
class BinarySearch {

    static int search(int[] arr, int target, int start, int end) {
        if (start > end) return -1;                   // base case — not found

        int mid = start + (end - start) / 2;          // avoids int overflow vs (start+end)/2

        if (arr[mid] == target) return mid;
        if (target < arr[mid])  return search(arr, target, start, mid - 1);  // go left
        return search(arr, target, mid + 1, end);      // go right
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 14, 32, 55, 66, 78};       // must be sorted — was unsorted before, binary search won't work on unsorted arrays
        System.out.println("Index of 14: " + search(arr, 14, 0, arr.length - 1));  // 2
        System.out.println("Index of  8: " + search(arr,  8, 0, arr.length - 1));  // -1
    }
}
