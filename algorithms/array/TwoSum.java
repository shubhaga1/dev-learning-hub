import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * LeetCode 1 - Two Sum
 * https://leetcode.com/problems/two-sum/
 *
 * Given an array of integers, return indices of the two numbers that add up to target.
 *
 * Input:  nums = [2,7,11,15], target = 9
 * Output: [0,1]  // nums[0] + nums[1] = 9
 *
 * Approach: HashMap — store seen values, check complement on each iteration
 * Time: O(n)  Space: O(n)
 */


class TwoSum {
    
    public static void main(String[] args) {
        int[] nums = { 2, 7, 11, 15 };
        int target = 9;

        int[] results = twoSum(nums, target);
        System.out.println(Arrays.toString(results));
    }

    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> numToIndex = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            if (numToIndex.containsKey(target - nums[i])) {
                return new int[] { numToIndex.get(target - nums[i]), i };
            }
            numToIndex.put(nums[i], i);
        }
        return new int[] {};
    }
}
