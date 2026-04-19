package dfs;

/**
 * PROOF — JVM call stack has a fixed size limit
 *
 * Every recursive call creates a STACK FRAME on the call stack:
 *   - stores: local variables + return address + parameters
 *   - size per frame: ~100–300 bytes
 *
 * YOUR JVM stack size = 2048 KB = 2 MB  (run: java -XX:+PrintFlagsFinal -version | grep ThreadStackSize)
 *
 * Math:
 *   2MB = 2,097,152 bytes
 *   one frame ≈ ~200 bytes
 *   max depth ≈ 2,097,152 / 200 ≈ ~10,000 frames
 *
 * This class proves it by recursing until crash and printing the depth.
 */
class StackLimitProof {

    static int depth = 0;

    static void recurse() {
        depth++;
        recurse();    // keep going until OS says "no more stack memory"
    }

    public static void main(String[] args) {

        // ── Test 1: default JVM stack ─────────────────────────────────────────
        System.out.println("JVM stack size: 2048 KB (check with: java -XX:+PrintFlagsFinal -version | grep ThreadStackSize)");
        System.out.println("Recursing until crash...\n");

        try {
            recurse();
        } catch (StackOverflowError e) {
            System.out.println("CRASHED at depth: " + depth);
            System.out.println("Each frame ≈ " + (2048 * 1024 / depth) + " bytes");
        }

        // ── What each frame contains ──────────────────────────────────────────
        System.out.println("""

          What one stack frame stores:
            - return address (where to go back after method ends)
            - parameters passed to the method
            - local variables inside the method

          recurse() has:
            - no parameters
            - no local variables
            → smallest possible frame (~100 bytes)
            → that's why it gets so deep before crashing

          A real DFS frame is bigger:
            dfsRecursive(graph, node, visited)
            - graph reference   (8 bytes)
            - node int          (4 bytes)
            - visited reference (8 bytes)
            - return address    (8 bytes)
            + overhead          (~100 bytes)
            → fewer frames fit → crashes sooner
          """);

        // ── How to increase stack size (workaround, not recommended) ──────────
        System.out.println("To increase stack size:");
        System.out.println("  java -Xss4m StackLimitProof   → 4MB stack");
        System.out.println("  java -Xss16m StackLimitProof  → 16MB stack");
        System.out.println("  Real fix: use iterative + explicit Stack<> on heap");
    }
}
