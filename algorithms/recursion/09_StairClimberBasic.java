/**
 * StairClimberBasic — count ways to climb n stairs, taking 1 or 2 steps
 * Same as Fibonacci sequence: ways(n) = ways(n-1) + ways(n-2)
 */
class StairClimberBasic {

    static int countDistinctWays(int n) {
        if (n <= 0) return 0;                         // invalid input
        if (n == 1) return 1;                         // only one way: {1}
        if (n == 2) return 2;                         // two ways: {1,1} or {2}

        return countDistinctWays(n - 1) + countDistinctWays(n - 2);
    }

    public static void main(String[] args) {
        int n = 5;
        System.out.println("Distinct ways to climb " + n + " stairs: " + countDistinctWays(n));  // 8
    }
}
