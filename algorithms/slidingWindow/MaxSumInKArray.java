/**
 * Max Sum of K-size window — Sliding Window
 * Find the maximum sum of any contiguous subarray of size k.
 */
class MaxSumInKArray {

    static int findMaxSum(int[] arr, int k) {
        int sum = 0;  // declared — was missing, causing "cannot be resolved"
        int max = 0;  // declared — was missing

        int i = 0, j = 0;

        while (j < arr.length) {
            sum = sum + arr[j];

            if (j - i + 1 < k) {
                j++;
            } else if (j - i + 1 == k) {
                max = Math.max(max, sum);   // update max
                sum = sum - arr[i];         // slide: remove leftmost element
                i++;
                j++;
            }
        }
        return max;
    }

    public static void main(String[] args) {
        int[] arr = {2, -3, 4, -1, -2, 1, 5, -3};
        int k = 3;
        System.out.println("Max sum of window size " + k + ": " + findMaxSum(arr, k));  // 4
    }
}
