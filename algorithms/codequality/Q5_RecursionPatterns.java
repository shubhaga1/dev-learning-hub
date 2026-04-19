
/**
 * Q5: Recursion Patterns — common mistakes
 *
 * Level 1 → base case wrong — off by one
 * Level 2 → recursive call not moving toward base case (infinite loop)
 * Level 3 → base case incomplete — misses a case (negative, null, empty)
 * Level 4 → redundant recomputation — should memoize
 *
 * Rule: at every recursive call, ask:
 *   1. Am I closer to the base case? (convergence)
 *   2. Have I covered ALL ways the base case can be reached?
 */
class Q5_RecursionPatterns {

    // ── Level 1: Off-by-one base case ────────────────────────────────────────

    // BAD: base case is n == 1, misses n == 0 → factorial(0) recurses forever
    static int factorial_BAD(int n) {
        if (n == 1) return 1;            // misses n=0 case
        return n * factorial_BAD(n - 1);
    }

    // GOOD: base case covers n==0 (math definition: 0! = 1)
    static int factorial_GOOD(int n) {
        if (n == 0) return 1;
        return n * factorial_GOOD(n - 1);
    }

    // ── Level 2: Not moving toward base case → infinite loop ─────────────────

    // BAD: calls itself with same n — never reaches n==0
    static int sum_BAD(int n) {
        if (n == 0) return 0;
        return n + sum_BAD(n);           // ← should be n-1, not n
    }

    // GOOD: each call reduces n by 1
    static int sum_GOOD(int n) {
        if (n == 0) return 0;
        return n + sum_GOOD(n - 1);     // moves toward base case
    }

    // ── Level 3: Incomplete base case — missing edge ──────────────────────────

    // BAD: doesn't handle null or empty string — throws NPE or wrong answer
    static boolean isPalindrome_BAD(String s) {
        if (s.length() == 1) return true;                      // misses empty string ""
        if (s.charAt(0) != s.charAt(s.length() - 1)) return false;
        return isPalindrome_BAD(s.substring(1, s.length() - 1));
    }

    // GOOD: handles both length 0 (even palindrome) and length 1 (odd palindrome)
    static boolean isPalindrome_GOOD(String s) {
        if (s == null)       return false;    // null guard
        if (s.length() <= 1) return true;     // "" and single char are palindromes
        if (s.charAt(0) != s.charAt(s.length() - 1)) return false;
        return isPalindrome_GOOD(s.substring(1, s.length() - 1));
    }

    // ── Level 4: Redundant recomputation — fibonacci without memo ────────────

    // BAD: fib(40) computes fib(39) and fib(38), fib(39) computes fib(38) again...
    // exponential time — fib(50) takes minutes
    static long fib_BAD(int n) {
        if (n <= 1) return n;
        return fib_BAD(n - 1) + fib_BAD(n - 2);   // fib(n-2) computed twice
    }

    // GOOD: memoize — compute each value once, reuse
    static long[] memo = new long[100];

    static long fib_GOOD(int n) {
        if (n <= 1) return n;
        if (memo[n] != 0) return memo[n];          // already computed — return cached
        memo[n] = fib_GOOD(n - 1) + fib_GOOD(n - 2);
        return memo[n];
    }

    public static void main(String[] args) {
        System.out.println("=== Level 1: off-by-one base case ===");
        // factorial_BAD(0);  // ← uncomment to see StackOverflowError
        System.out.println("0! = " + factorial_GOOD(0));  // 1
        System.out.println("5! = " + factorial_GOOD(5));  // 120

        System.out.println("\n=== Level 2: not converging ===");
        // sum_BAD(5);  // ← uncomment to see StackOverflowError
        System.out.println("sum(5) = " + sum_GOOD(5));    // 15

        System.out.println("\n=== Level 3: incomplete base case ===");
        // isPalindrome_BAD("abba");  // fine
        // isPalindrome_BAD("racecar");  // odd length — "" → NPE on length 0
        System.out.println("racecar: " + isPalindrome_GOOD("racecar"));   // true
        System.out.println("abba: "    + isPalindrome_GOOD("abba"));      // true
        System.out.println("hello: "   + isPalindrome_GOOD("hello"));     // false
        System.out.println("a: "       + isPalindrome_GOOD("a"));         // true (single char)
        System.out.println("empty: "   + isPalindrome_GOOD(""));          // true

        System.out.println("\n=== Level 4: redundant recomputation ===");
        long start = System.currentTimeMillis();
        System.out.println("fib_BAD(40) = "  + fib_BAD(40));
        System.out.println("BAD time: " + (System.currentTimeMillis() - start) + "ms");

        start = System.currentTimeMillis();
        System.out.println("fib_GOOD(40) = " + fib_GOOD(40));
        System.out.println("GOOD time: " + (System.currentTimeMillis() - start) + "ms");
    }
}
