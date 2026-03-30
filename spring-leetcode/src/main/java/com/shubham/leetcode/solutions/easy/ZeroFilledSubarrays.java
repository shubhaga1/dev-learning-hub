package com.shubham.leetcode.solutions.easy;

import org.springframework.stereotype.Component;

/**
 * LeetCode 2348 — Zero Filled Subarrays
 * Difficulty: Easy
 *
 * @Component = Spring manages this class (can inject it anywhere)
 * Without @Component it's just a plain Java class — still works,
 * but Spring won't know about it.
 */
@Component
public class ZeroFilledSubarrays {

    // ============================================================
    // APPROACH 1: Brute Force  O(n²) time | O(1) space
    // ============================================================
    public long zeroFilledSubarrayBrute(int[] nums) {
        long count = 0;

        for (int i = 0; i < nums.length; i++) {
            for (int j = i; j < nums.length; j++) {
                if (nums[j] == 0) {
                    count++;
                } else {
                    break;
                }
            }
        }
        return count;
    }

    // ============================================================
    // APPROACH 2: Optimal  O(n) time | O(1) space
    //
    // Each new zero adds run_length new subarrays
    // ============================================================
    public long zeroFilledSubarray(int[] nums) {
        long count     = 0;
        long runLength = 0;

        for (int num : nums) {
            if (num == 0) {
                runLength++;
                count += runLength;
            } else {
                runLength = 0;
            }
        }
        return count;
    }
}
