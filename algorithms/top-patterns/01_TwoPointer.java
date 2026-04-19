package top_patterns;

import java.util.*;

/**
 * TWO-POINTER PATTERN
 *
 * CORE IDEA: place two index variables and move them toward each other
 *            (or at different speeds) to avoid the O(n²) brute-force nested loop.
 *
 * THREE VARIANTS:
 *   1. OPPOSITE ENDS   left=0, right=n-1, squeeze inward  → sorted array problems
 *   2. SAME DIRECTION  slow/fast both start at 0           → partition / in-place
 *   3. SLIDING         see 02_SlidingWindow.java
 *
 * TIME:  O(n)  — each element visited at most once
 * SPACE: O(1)  — no extra array, just two indices
 *
 * PROBLEMS COVERED HERE:
 *   1. Two Sum (sorted input)              — opposite ends
 *   2. Container With Most Water           — opposite ends
 *   3. Move Zeros                          — slow/fast (same direction)
 *   4. 3Sum                                — sort + opposite ends inside outer loop
 */
class TwoPointer {

    // ── 1. TWO SUM (sorted array) ─────────────────────────────────────────────
    // Find two indices whose values sum to target. Array is already sorted.
    // Brute force: O(n²).  Two-pointer: O(n).
    //
    //  [2, 7, 11, 15]  target=9
    //   L            R   2+15=17 too big  → R--
    //   L        R       2+11=13 too big  → R--
    //   L    R            2+7=9  FOUND ✅
    static int[] twoSumSorted(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int sum = nums[left] + nums[right];
            if      (sum == target) return new int[]{left + 1, right + 1}; // 1-indexed
            else if (sum < target)  left++;
            else                    right--;
        }
        return new int[]{-1, -1};
    }

    // ── 2. CONTAINER WITH MOST WATER ─────────────────────────────────────────
    // heights[] — vertical lines. Pick two lines, max water = min(h[l],h[r])*(r-l).
    // Greedy: always move the SHORTER side inward (moving taller can only decrease area).
    //
    //  [1, 8, 6, 2, 5, 4, 8, 3, 7]
    //   L                          R
    //   min(1,7)=1 * 8 = 8  → move L (height 1 is shorter)
    //   ...
    //   [8, ..., 7]  min(8,7)*1 = 7
    //   best = 49 (heights[1]=8 and heights[8]=7, width=6 → 7*7=49)
    static int maxWater(int[] h) {
        int left = 0, right = h.length - 1, best = 0;
        while (left < right) {
            int area = Math.min(h[left], h[right]) * (right - left);
            best = Math.max(best, area);
            if (h[left] < h[right]) left++;   // shorter side can't improve — move it
            else                    right--;
        }
        return best;
    }

    // ── 3. MOVE ZEROS ─────────────────────────────────────────────────────────
    // Move all 0s to the end, keep non-zero order, in-place O(1) space.
    // slow = "boundary of non-zero section"
    // fast = "scanner looking for non-zero values"
    //
    //  [0, 1, 0, 3, 12]
    //   s
    //   f  → 1 is non-zero: swap nums[slow] and nums[fast], slow++
    //  [1, 0, 0, 3, 12]
    //      s  f → 0 is zero: fast++ only
    //  [1, 0, 0, 3, 12]
    //      s     f → 3 is non-zero: swap, slow++
    //  [1, 3, 0, 0, 12]  ...
    static void moveZeros(int[] nums) {
        int slow = 0;                           // next position for a non-zero
        for (int fast = 0; fast < nums.length; fast++) {
            if (nums[fast] != 0) {
                int tmp = nums[slow];           // swap non-zero to front
                nums[slow] = nums[fast];
                nums[fast] = tmp;
                slow++;
            }
            // fast always advances; slow only advances when we place a non-zero
        }
    }

    // ── 4. 3SUM ───────────────────────────────────────────────────────────────
    // Find all unique triplets [a,b,c] where a+b+c = 0.
    // Key insight: sort first, then for each nums[i], run two-pointer on the rest.
    // Skip duplicates to avoid repeated triplets.
    //
    //  sorted: [-4, -1, -1, 0, 1, 2]
    //  i=0 (-4): L=-1 R=2  sum=-3 → L++
    //            L=-1 R=1  sum=-4 → L++
    //            L=0  R=1  sum=-3 → L++  (L≥R, done)
    //  i=1 (-1): L=-1 R=2  sum=0  FOUND [-1,-1,2] ✅
    //            skip dup, L=0 R=1  sum=0  FOUND [-1,0,1] ✅
    //  i=2 (-1): duplicate of i=1 → skip
    static List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> result = new ArrayList<>();

        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;  // skip outer duplicate
            if (nums[i] > 0) break;                          // sorted: no triplet possible

            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left]  == nums[left  + 1]) left++;  // skip dup
                    while (left < right && nums[right] == nums[right - 1]) right--; // skip dup
                    left++; right--;
                } else if (sum < 0) left++;
                else                right--;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        // 1. Two Sum (sorted)
        System.out.println("Two Sum sorted [2,7,11,15] target=9: "
            + Arrays.toString(twoSumSorted(new int[]{2, 7, 11, 15}, 9)));  // [1, 2]

        // 2. Container With Most Water
        System.out.println("Max water [1,8,6,2,5,4,8,3,7]: "
            + maxWater(new int[]{1, 8, 6, 2, 5, 4, 8, 3, 7}));            // 49

        // 3. Move Zeros
        int[] arr = {0, 1, 0, 3, 12};
        moveZeros(arr);
        System.out.println("Move zeros: " + Arrays.toString(arr));         // [1,3,12,0,0]

        // 4. 3Sum
        System.out.println("3Sum [-1,0,1,2,-1,-4]: "
            + threeSum(new int[]{-1, 0, 1, 2, -1, -4}));                  // [[-1,-1,2],[-1,0,1]]

        System.out.println("""

        PATTERN TEMPLATE (opposite ends):
          int left = 0, right = n - 1;
          while (left < right) {
              if (condition met)  { capture answer; left++; right--; }
              else if (too small) { left++;  }
              else                { right--; }
          }

        PATTERN TEMPLATE (same direction / partition):
          int slow = 0;
          for (int fast = 0; fast < n; fast++) {
              if (nums[fast] meets condition) {
                  swap(slow, fast);
                  slow++;
              }
          }

        WHEN TO REACH FOR TWO-POINTER:
          - Input is sorted (or can be sorted cheaply)
          - Looking for a pair/triplet that satisfies a sum condition
          - In-place partition (move zeros, remove duplicates)
          - "Most water" / "closest pair" style optimisation
        """);
    }
}
