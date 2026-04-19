import java.util.Arrays;

/**
 * LeetCode 53 - Maximum Subarray
 * https://leetcode.com/problems/maximum-subarray/
 *
 * Find the contiguous subarray with the largest sum.
 *
 * Input:  nums = [-2,1,-3,4,-1,2,1,-5,4]
 * Output: 6  // subarray [4,-1,2,1]
 *
 * Approach: Kadane's Algorithm — reset running sum when it goes negative
 * Time: O(n)  Space: O(1)
 */
class MaxSubArray {
    public static void main(String[] args) {
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("Input:  " + Arrays.toString(nums));
        System.out.println("Output: " + new MaxSubArray().maxSubArray(nums)); // 6
    }

    public int maxSubArray(int[] nums) {
        int maxSum = Integer.MIN_VALUE;
        int currentSum = 0;

        for (int i = 0; i < nums.length; i++) {
            currentSum += nums[i];

            if (currentSum > maxSum) {
                maxSum = currentSum;
            }

            if (currentSum < 0) {
                currentSum = 0;
            }
        }

        return maxSum;
    }
}
