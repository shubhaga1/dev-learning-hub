package com.shubham.leetcode.solutions.easy;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Unit tests for ZeroFilledSubarrays
 * Run: mvn test
 */
class ZeroFilledSubarraysTest {

    private ZeroFilledSubarrays solution;

    @BeforeEach
    void setUp() {
        solution = new ZeroFilledSubarrays();
    }

    @Test
    void testExampleFromProblem() {
        assertEquals(6, solution.zeroFilledSubarray(new int[]{1, 3, 0, 0, 2, 0, 0, 4}));
    }

    @Test
    void testAllZeros() {
        assertEquals(10, solution.zeroFilledSubarray(new int[]{0, 0, 0, 0}));
    }

    @Test
    void testSingleZero() {
        assertEquals(1, solution.zeroFilledSubarray(new int[]{0}));
    }

    @Test
    void testNoZeros() {
        assertEquals(0, solution.zeroFilledSubarray(new int[]{1, 2, 3}));
    }

    @Test
    void testTwoSeparateZeros() {
        assertEquals(2, solution.zeroFilledSubarray(new int[]{0, 1, 0}));
    }

    @Test
    void testBruteMatchesOptimal() {
        int[] nums = {1, 3, 0, 0, 2, 0, 0, 4};
        assertEquals(
            solution.zeroFilledSubarrayBrute(nums),
            solution.zeroFilledSubarray(nums)
        );
    }
}
