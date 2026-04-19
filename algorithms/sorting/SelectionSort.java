/**
 * SELECTION SORT
 *
 * Strategy: Find minimum in unsorted part, swap it to front. Repeat.
 *
 * Time:  O(n²) always — always scans full remaining array
 * Space: O(1) in-place
 *
 * Only advantage over bubble sort: fewer SWAPS (exactly n-1 swaps)
 * Use when: swap is expensive (e.g. writing to flash memory)
 */
class SelectionSort {

    static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) minIdx = j;
            }
            // swap minimum to position i
            int tmp = arr[minIdx]; arr[minIdx] = arr[i]; arr[i] = tmp;
        }
    }

    public static void main(String[] args) {
        int[] arr = {64, 25, 12, 22, 11};
        System.out.println("Trace on [64, 25, 12, 22, 11]:");
        System.out.println("Pass 1: min=11, swap with 64 → [11, 25, 12, 22, 64]");
        System.out.println("Pass 2: min=12, swap with 25 → [11, 12, 25, 22, 64]");
        System.out.println("Pass 3: min=22, swap with 25 → [11, 12, 22, 25, 64]");
        System.out.println("Pass 4: min=25, already in place");

        selectionSort(arr);
        System.out.print("\nResult: ");
        for (int x : arr) System.out.print(x + " ");

        System.out.println("\n\nSorting algorithm summary:");
        System.out.println("Bubble:    O(n²) time, O(1) space, stable");
        System.out.println("Selection: O(n²) time, O(1) space, NOT stable, min swaps");
        System.out.println("Insertion: O(n²) worst, O(n) best (nearly sorted), stable");
        System.out.println("Merge:     O(n log n), O(n) space, stable");
        System.out.println("Quick:     O(n log n) avg, O(1) space, NOT stable");
        System.out.println("Heap:      O(n log n), O(1) space, NOT stable");
    }
}
