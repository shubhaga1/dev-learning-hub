
class StairClimber {
    public static int countDistinctWays(int n, int[] steps) {
        int[] dp = new int[n + 1];
        dp[0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int step : steps) {
                if (i >= step) {
                    dp[i] += dp[i - step];
                }
            }
        }

        return dp[n];
    }

    public static void main(String[] args) {
        int n = 5;
        int[] steps = {1, 2};

        int distinctWays = countDistinctWays(n, steps);
        System.out.println("Distinct ways to climb the stair: " + distinctWays); // ans 8
    }
}
