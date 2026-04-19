import java.util.Arrays;

/**
 * LeetCode 4 - Median of Two Sorted Arrays
 * https://leetcode.com/problems/median-of-two-sorted-arrays/
 *
 * Find the median of two sorted arrays combined.
 *
 * Input:  nums1 = [1,3], nums2 = [2,3,7]
 * Output: 3.0  // merged = [1,2,3,3,7], median = 3
 *
 * Approach: Merge both arrays, sort, pick middle element(s)
 * Time: O((m+n)log(m+n))  Space: O(m+n)
 */
class MedianArray {
    public static void main(String[] args) {
        int[] nums1 = {1, 3};
        int[] nums2 = {2, 3, 7};
        System.out.println("nums1:  " + Arrays.toString(nums1));
        System.out.println("nums2:  " + Arrays.toString(nums2));
        System.out.println("Output: " + findMedianSortedArrays(nums1, nums2)); // 3.0
    }

    private static double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int[] merged = new int[nums1.length + nums2.length];
        System.arraycopy(nums1, 0, merged, 0, nums1.length);
        System.arraycopy(nums2, 0, merged, nums1.length, nums2.length);
        Arrays.sort(merged);

        int n = merged.length;
        if (n % 2 == 1) {
            return merged[n / 2];
        } else {
            return (merged[n / 2 - 1] + merged[n / 2]) / 2.0;
        }
    }
}
