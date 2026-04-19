
/**
 * Q2: Base Cases — always at the top, always complete
 *
 * Level 1 → missing base case entirely (infinite loop)
 * Level 2 → base case at the bottom (confusing, hard to read)
 * Level 3 → base case uses || when && is needed (classic maze bug)
 * Level 4 → multiple base cases, one is shadowed / unreachable
 *
 * Rule: base cases are the EXIT — put them first so reader sees
 *       "when do we stop?" before "what do we do?".
 */
class Q2_BaseCases {

    // ── Level 1: Missing base case → StackOverflowError ─────────────────────

    // BAD: no base case — runs forever
    static int factorial_BAD(int n) {
        return n * factorial_BAD(n - 1);  // never stops
    }

    // GOOD: base case first
    static int factorial_GOOD(int n) {
        if (n == 0) return 1;             // base case — stop here
        return n * factorial_GOOD(n - 1);
    }

    // ── Level 2: Base case buried at the bottom ──────────────────────────────

    // BAD: reader must scroll to the bottom to understand when it stops
    static int sum_BAD(int n) {
        int result = n + sum_BAD(n - 1);  // recursive call before base case — confusing
        if (n == 0) return 0;             // base case at the bottom — too late, never reached
        return result;
    }

    // GOOD: exit condition is the first thing you see
    static int sum_GOOD(int n) {
        if (n == 0) return 0;             // base case — stop
        return n + sum_GOOD(n - 1);
    }

    // ── Level 3: || vs && — classic maze bug ─────────────────────────────────

    // BAD: stops as soon as EITHER row OR col reaches 1
    // misses paths along the edge — prints incomplete paths
    static void mazePaths_BAD(String path, int row, int col) {
        if (row == 1 || col == 1) {       // ← BUG: stops too early on edges
            System.out.println(path);
            return;
        }
        if (row > 1) mazePaths_BAD(path + "D", row - 1, col);
        if (col > 1) mazePaths_BAD(path + "R", row, col - 1);
    }

    // GOOD: stop only when BOTH reach 1 — the actual destination
    static void mazePaths_GOOD(String path, int row, int col) {
        if (row == 1 && col == 1) {       // ← reached the corner — done
            System.out.println(path);
            return;
        }
        if (row > 1) mazePaths_GOOD(path + "D", row - 1, col);
        if (col > 1) mazePaths_GOOD(path + "R", row, col - 1);
    }

    // ── Level 4: Shadowed base case — one is unreachable ─────────────────────

    // BAD: second base case (n < 0) is shadowed by first — n==0 catches everything
    static int countdown_BAD(int n) {
        if (n == 0) return 0;             // catches n=0
        if (n < 0)  return -1;           // ← DEAD CODE: n<0 never reached because
                                          //   negative input goes to n==0 first? No —
                                          //   actually n<0 IS reachable, but order is wrong
                                          //   — should guard for n<0 FIRST
        return n + countdown_BAD(n - 1);
    }

    // GOOD: most restrictive guard first — negative before zero
    static int countdown_GOOD(int n) {
        if (n < 0)  return -1;           // guard: invalid input
        if (n == 0) return 0;            // base case: done
        return n + countdown_GOOD(n - 1);
    }

    public static void main(String[] args) {
        System.out.println("=== Level 1: factorial ===");
        // factorial_BAD(5);  // ← uncomment to see StackOverflowError
        System.out.println("5! = " + factorial_GOOD(5));  // 120

        System.out.println("\n=== Level 2: sum ===");
        System.out.println("sum(5) = " + sum_GOOD(5));    // 15

        System.out.println("\n=== Level 3: maze || vs && ===");
        System.out.println("BAD paths (stops early on edges):");
        mazePaths_BAD("", 2, 2);
        System.out.println("GOOD paths (all 6):");
        mazePaths_GOOD("", 3, 3);

        System.out.println("\n=== Level 4: shadowed base case ===");
        System.out.println("countdown_BAD(-1): " + countdown_BAD(-1));
        System.out.println("countdown_GOOD(-1): " + countdown_GOOD(-1));
    }
}
