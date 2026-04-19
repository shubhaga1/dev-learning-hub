package top_patterns;

import java.util.*;

/**
 * SLIDING WINDOW PATTERN
 *
 * CORE IDEA: maintain a "window" [left, right] over the array/string.
 *            Expand right to grow, shrink left when constraint is violated.
 *            Avoids recomputing the whole window — O(n) instead of O(n²).
 *
 * TWO VARIANTS:
 *   1. FIXED SIZE   — window size k is given. Slide one step at a time.
 *   2. VARIABLE SIZE — grow until constraint breaks, shrink until valid again.
 *
 * KEY INSIGHT: each element enters the window once (right++) and
 *              leaves once (left++). Total work = O(2n) = O(n).
 *
 * PROBLEMS COVERED:
 *   1. Max sum subarray of size k          — fixed window
 *   2. Longest substring, no repeats       — variable window + HashSet
 *   3. Min size subarray with sum ≥ target  — variable window + shrink
 *   4. Longest substring with k distinct   — variable window + HashMap
 */
class SlidingWindow {

    // ── 1. MAX SUM SUBARRAY OF SIZE K (fixed window) ─────────────────────────
    // Add new right element, remove old left element once window is full.
    //
    //  k=3, [2, 1, 5, 1, 3, 2]
    //  i=0: sum=2
    //  i=1: sum=3
    //  i=2: sum=8  → window full, record 8
    //  i=3: sum=8-2+1=7  (remove nums[0]=2, add nums[3]=1)
    //  i=4: sum=7-1+3=9  → record 9
    //  i=5: sum=9-5+2=6
    //  answer = 9
    static int maxSumFixed(int[] nums, int k) {
        int windowSum = 0, maxSum = 0;
        for (int i = 0; i < nums.length; i++) {
            windowSum += nums[i];                     // expand right
            if (i >= k) windowSum -= nums[i - k];     // shrink left once full
            if (i >= k - 1) maxSum = Math.max(maxSum, windowSum);
        }
        return maxSum;
    }

    // ── 2. LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS (variable) ─────────
    // Grow right. When a duplicate enters, shrink left until it's gone.
    // HashSet tracks what's in the window.
    //
    //  "abcabcbb"
    //  → expand: a b c          window={a,b,c}  len=3
    //  → 'a' seen: shrink until 'a' removed: remove 'a', left=1
    //  → expand: a b c          window={b,c,a}  len=3
    //  → 'b' seen: shrink: remove 'b', left=2
    //  → expand: b c            window={c,a,b}  len=3
    //  → 'c' seen ...
    //  answer = 3  ("abc")
    static int lengthOfLongestSubstring(String s) {
        Set<Character> window = new HashSet<>();
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            while (window.contains(c)) {             // duplicate: shrink from left
                window.remove(s.charAt(left++));
            }
            window.add(c);                           // now safe to add
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    // ── 3. MIN SIZE SUBARRAY SUM ≥ TARGET (variable) ─────────────────────────
    // Grow right until sum >= target. Then shrink left as long as sum stays valid.
    // Record the minimum window length each time constraint is satisfied.
    //
    //  target=7, [2,3,1,2,4,3]
    //  expand to [2,3,1,2] sum=8 ≥ 7  → len=4, shrink: remove 2 → sum=6 < 7
    //  expand to [3,1,2,4] sum=10 ≥ 7 → len=4, shrink: remove 3 → [1,2,4] sum=7 → len=3
    //  shrink: remove 1 → [2,4] sum=6 < 7
    //  expand to [2,4,3]  sum=9 ≥ 7   → len=3, shrink: remove 2 → [4,3] sum=7 → len=2 ✅
    //  answer = 2  (subarray [4,3])
    static int minSubarrayLen(int target, int[] nums) {
        int left = 0, sum = 0, best = Integer.MAX_VALUE;
        for (int right = 0; right < nums.length; right++) {
            sum += nums[right];                      // expand
            while (sum >= target) {                  // valid: try to shrink
                best = Math.min(best, right - left + 1);
                sum -= nums[left++];
            }
        }
        return best == Integer.MAX_VALUE ? 0 : best;
    }

    // ── 4. LONGEST SUBSTRING WITH AT MOST K DISTINCT CHARACTERS (variable) ───
    // HashMap counts frequency of each char in window.
    // When map.size() > k, shrink left until exactly k distinct chars remain.
    //
    //  k=2, "eceba"
    //  expand: e  c  →  map={e:1,c:1}  size=2  len=2
    //  expand: e  →  map={e:2,c:1}  size=2  len=3
    //  expand: b  →  map={e:2,c:1,b:1}  size=3 > 2  shrink:
    //    remove e → {e:1,c:1,b:1} still 3, remove e again → {c:1,b:1} size=2
    //    left=2, window="eb"  len=2
    //  expand: a  → map={c:1,b:1,a:1} size=3 > 2  shrink: ...
    //  answer = 3  ("ece")
    static int longestKDistinct(String s, int k) {
        Map<Character, Integer> freq = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            freq.merge(s.charAt(right), 1, Integer::sum);    // expand
            while (freq.size() > k) {                        // too many distinct: shrink
                char lc = s.charAt(left++);
                freq.merge(lc, -1, Integer::sum);
                if (freq.get(lc) == 0) freq.remove(lc);
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println("Max sum k=3 [2,1,5,1,3,2]:  "
            + maxSumFixed(new int[]{2, 1, 5, 1, 3, 2}, 3));           // 9

        System.out.println("Longest no-repeat 'abcabcbb': "
            + lengthOfLongestSubstring("abcabcbb"));                   // 3

        System.out.println("Min subarray sum≥7 [2,3,1,2,4,3]: "
            + minSubarrayLen(7, new int[]{2, 3, 1, 2, 4, 3}));        // 2

        System.out.println("Longest k=2 distinct 'eceba': "
            + longestKDistinct("eceba", 2));                           // 3

        System.out.println("""

        FIXED WINDOW template:
          for (int i = 0; i < n; i++) {
              windowSum += nums[i];                 // add right
              if (i >= k) windowSum -= nums[i - k]; // remove left
              if (i >= k - 1) update answer;
          }

        VARIABLE WINDOW template:
          int left = 0;
          Map/Set window = ...;
          for (int right = 0; right < n; right++) {
              add s[right] to window;               // expand
              while (window violates constraint) {
                  remove s[left] from window;       // shrink
                  left++;
              }
              update answer with (right - left + 1);
          }

        WHEN TO REACH FOR SLIDING WINDOW:
          - "longest/shortest subarray/substring that satisfies X"
          - "max/min sum of subarray of size k"
          - X involves counting chars, sum, distinct elements in a range
          - Key signal: contiguous window, not arbitrary subset
        """);
    }
}
