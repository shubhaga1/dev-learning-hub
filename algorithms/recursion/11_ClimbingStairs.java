import java.util.HashMap;
import java.util.Map;

// https://leetcode.com/problems/climbing-stairs/description/

class ClimbingStairs {

    // count ways to reach step n — can take 1 or 2 steps at a time
    static int climbStairs(int n, Map<Integer, Integer> memo) {
        if (n == 0 || n == 1) return 1;              // base case

        if (!memo.containsKey(n)) {
            memo.put(n, climbStairs(n - 1, memo) + climbStairs(n - 2, memo));
        }
        return memo.get(n);
    }

    public static void main(String[] args) {
        Map<Integer, Integer> memo = new HashMap<>();
        int n = 5;
        System.out.println("Ways to climb " + n + " stairs: " + climbStairs(n, memo));  // 8
    }
}
