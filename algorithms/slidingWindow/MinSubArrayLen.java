// https://leetcode.com/problems/minimum-size-subarray-sum/description/
// Find minimum length subarray with sum >= target
// Input: target=7, nums=[2,3,1,2,4,3] → Output: 2 (subarray [4,3])

class MinSubArrayLen {  // renamed from Solution — duplicate class name conflict

    static int minSubArrayLen(int target, int[] nums) {
        int i = 0, j = 0;
        int sum = 0, ans = Integer.MAX_VALUE;

        while (j < nums.length) {
            sum += nums[j];
            while (sum >= target) {
                ans = Math.min(ans, j - i + 1);
                sum -= nums[i];
                i++;
            }
            j++;
        }
        return ans == Integer.MAX_VALUE ? 0 : ans;
    }

    public static void main(String[] args) {
        System.out.println(minSubArrayLen(7, new int[]{2, 3, 1, 2, 4, 3}));  // 2
        System.out.println(minSubArrayLen(4, new int[]{1, 4, 4}));            // 1
        System.out.println(minSubArrayLen(11, new int[]{1, 1, 1, 1, 1}));    // 0
    }
}
