import java.util.Arrays;

/**
 * LeetCode 2348 - Number of Zero-Filled Subarrays
 * https://leetcode.com/problems/number-of-zero-filled-subarrays/
 *
 * Count all subarrays filled with 0s.
 *
 * Input:  nums = [1,3,0,0,2,0,0,4]
 * Output: 6  // [0],[0],[0,0],[0],[0],[0,0]
 *
 * Approach: For each run of k consecutive zeros, it contributes k*(k+1)/2 subarrays
 * Time: O(n)  Space: O(1)
 */
class ZeroFilledSubarray {
    public static void main(String[] args) {
        int[] nums = {1, 3, 0, 0, 2, 0, 0, 4};
        System.out.println("Input:  " + Arrays.toString(nums));
        System.out.println("Output: " + new ZeroFilledSubarray().zeroFilledSubarray(nums)); // 6
    }

    public int zeroFilledSubarray(int[] nums) {
        int n = nums.length;
        int ans = 0;
        int count = 0; // count of consecutive zeros

        for (int i = 0; i < n; i++) {
            if (nums[i] == 0) {
                count++;
            } else {
                ans += (count * (count + 1)) / 2;
                count = 0;
            }
        }
        if (count != 0) {
            ans += (count * (count + 1)) / 2;
        }
        return ans;
    }
}
