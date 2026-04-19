/**
 * HEAP SORT
 *
 * Strategy: Build max-heap, repeatedly extract max to end of array.
 *
 * Time:  O(n log n) always — no worst case
 * Space: O(1) — in-place, no extra arrays
 *
 * Heap property: parent >= both children (max-heap)
 * Index math:    parent = (i-1)/2, left = 2i+1, right = 2i+2
 *
 * Not stable — relative order of equal elements not preserved.
 * Good when: guaranteed O(n log n) matters more than cache performance.
 */
class HeapSort {

    // Maintain max-heap property for subtree rooted at i
    static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int left    = 2 * i + 1;
        int right   = 2 * i + 2;

        if (left  < n && arr[left]  > arr[largest]) largest = left;
        if (right < n && arr[right] > arr[largest]) largest = right;

        if (largest != i) {
            int tmp = arr[i]; arr[i] = arr[largest]; arr[largest] = tmp;
            heapify(arr, n, largest);  // fix the swapped child
        }
    }

    static void heapSort(int[] arr) {
        int n = arr.length;

        // Phase 1: build max-heap (bottom-up, start from last non-leaf)
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }

        // Phase 2: extract max one by one, shrink heap
        for (int i = n - 1; i > 0; i--) {
            int tmp = arr[0]; arr[0] = arr[i]; arr[i] = tmp;  // move max to end
            heapify(arr, i, 0);                                 // re-heapify reduced heap
        }
    }

    public static void main(String[] args) {
        int[] arr = {12, 11, 13, 5, 6, 7};
        System.out.println("Before: 12 11 13 5 6 7");
        heapSort(arr);
        System.out.print("After:  ");
        for (int x : arr) System.out.print(x + " ");
        // Output: 5 6 7 11 12 13

        System.out.println("\n\nComparison:");
        System.out.println("Merge sort:  O(n log n) but O(n) extra space");
        System.out.println("Heap sort:   O(n log n) and O(1) space — wins on memory");
        System.out.println("Quick sort:  O(n log n) avg but O(n²) worst case");
    }
}
