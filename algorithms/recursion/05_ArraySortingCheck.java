
class ArraySortingCheck {
    public static boolean isSorted(int[] arr) {
        return isSortedRecursive(arr, 0);
    }

    private static boolean isSortedRecursive(int[] arr, int index) {
        if (index >= arr.length - 1) {
            // Base case: If we reach the end of the array, it is sorted
            return true;
        }

        if (arr[index] > arr[index + 1]) {
            // If the current element is greater than the next element, the array is not sorted
            return false;
        }

        // Recursively check the remaining elements
        return isSortedRecursive(arr, index + 1);
    }

    public static void main(String[] args) {
        int[] arr1 = {1, 2, 3, 4, 5};
        int[] arr2 = {1, 3, 2, 4, 5};

        System.out.println("Array 1 is sorted: " + isSorted(arr1));
        System.out.println("Array 2 is sorted: " + isSorted(arr2));
    }
}
