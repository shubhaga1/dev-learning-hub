/**
 * QUICK SORT
 *
 * Strategy: Pick a pivot, partition array so left < pivot < right, recurse.
 *
 * Time:  O(n log n) average, O(n²) worst (sorted input + bad pivot)
 * Space: O(log n) stack frames
 *
 * Best for: General purpose, in-place, cache-friendly
 * Avoid:    Nearly sorted data (use insertion sort there)
 */
class QuickSort {

    // Lomuto partition — pivot = last element
    static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;  // index of smaller element

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
            }
        }
        // place pivot in correct position
        int tmp = arr[i + 1]; arr[i + 1] = arr[high]; arr[high] = tmp;
        return i + 1;
    }

    static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);   // left of pivot
            quickSort(arr, pi + 1, high);  // right of pivot
        }
    }

    public static void main(String[] args) {
        int[] arr = {10, 7, 8, 9, 1, 5};
        quickSort(arr, 0, arr.length - 1);

        System.out.print("Sorted: ");
        for (int x : arr) System.out.print(x + " ");
        // Output: 1 5 7 8 9 10

        // Visualize partition step
        System.out.println("\n\nPartition trace on [3,6,8,10,1,2,1]:");
        System.out.println("pivot=1 (last)");
        System.out.println("Pass through: 3>1 skip, 6>1 skip, 8>1 skip, 10>1 skip, 1<=1 swap");
        System.out.println("Result: [1,1,8,10,6,2,3] — pivot placed at index 1");
    }
}
