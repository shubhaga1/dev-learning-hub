/**
 * LeetCode 2348 — Zero Filled Subarrays (Easy)
 *
 * Count the number of subarrays filled with 0.
 * Input: [1,3,0,0,2,0,0,4] → 6
 *
 * Key insight: a run of k zeros contributes k*(k+1)/2 subarrays.
 * Each new zero in a run adds runLength new subarrays.
 */
class ZeroFilledSubarrays {

    // APPROACH 1: Brute Force — O(n²) time | O(1) space
    static long zeroFilledSubarrayBrute(int[] nums) {
        long count = 0;
        for (int i = 0; i < nums.length; i++) {
            for (int j = i; j < nums.length; j++) {
                if (nums[j] == 0) count++;
                else break;
            }
        }
        return count;
    }

    // APPROACH 2: Optimal — O(n) time | O(1) space
    // Each new zero extends the current run — adds runLength new subarrays
    static long zeroFilledSubarray(int[] nums) {
        long count = 0, runLength = 0;
        for (int num : nums) {
            runLength = (num == 0) ? runLength + 1 : 0;
            count += runLength;
        }
        return count;
    }

    public static void main(String[] args) {
        int[] nums = {1, 3, 0, 0, 2, 0, 0, 4};
        System.out.println("Brute:   " + zeroFilledSubarrayBrute(nums));  // 6
        System.out.println("Optimal: " + zeroFilledSubarray(nums));        // 6

        int[] allZeros = {0, 0, 0, 0};
        System.out.println("All zeros [4]: " + zeroFilledSubarray(allZeros));  // 10
    }
}
