/**
 * JVM FLAGS — controlling how the JVM runs your program
 *
 * The JVM has three key memory areas:
 *
 *   ┌─────────────────────────────────────────────┐
 *   │  HEAP (objects live here)                   │  ← -Xms, -Xmx control this
 *   │  String s = new String("hello")             │
 *   │  new ArrayList<>()                          │
 *   │  Stack<Node> stack = new Stack<>()          │
 *   ├─────────────────────────────────────────────┤
 *   │  CALL STACK (one per thread)                │  ← -Xss controls this
 *   │  each method call = one frame pushed here   │
 *   │  method returns  = frame popped             │
 *   ├─────────────────────────────────────────────┤
 *   │  METASPACE (class definitions)              │
 *   │  stores compiled class bytecode             │
 *   └─────────────────────────────────────────────┘
 *
 * FLAGS:
 *   -Xms   initial heap size   (how much heap JVM starts with)
 *   -Xmx   max heap size       (how much heap JVM can grow to)
 *   -Xss   thread stack size   (call stack size per thread)
 *   -XX:+PrintFlagsFinal  print every JVM flag and its value
 *
 * Run: javac JVMFlagsDemo.java && java JVMFlagsDemo
 */
class JVMFlagsDemo {

    public static void main(String[] args) {

        // ── 1. Heap: -Xms and -Xmx ───────────────────────────────────────────
        // Runtime.getRuntime() gives you access to JVM memory info
        Runtime rt = Runtime.getRuntime();

        long maxHeap  = rt.maxMemory();     // -Xmx value  (hard ceiling)
        long totalHeap = rt.totalMemory();  // current heap allocated to JVM (-Xms grows to this)
        long freeHeap  = rt.freeMemory();   // free within current heap
        long usedHeap  = totalHeap - freeHeap;

        System.out.println("=== HEAP (-Xms / -Xmx) ===");
        System.out.printf("  Max heap   (-Xmx) : %6d MB%n", maxHeap   / 1024 / 1024);
        System.out.printf("  Total heap        : %6d MB%n", totalHeap / 1024 / 1024);
        System.out.printf("  Used heap         : %6d MB%n", usedHeap  / 1024 / 1024);
        System.out.printf("  Free heap         : %6d MB%n", freeHeap  / 1024 / 1024);

        System.out.println("""

          -Xms = initial heap size (JVM starts with this much)
          -Xmx = max heap size     (JVM can't grow beyond this)

          If used heap > Xmx → OutOfMemoryError

          Example:
            java -Xms256m -Xmx4g MyClass
              → starts with 256MB heap
              → can grow up to 4GB
              → OutOfMemoryError if it needs more than 4GB
          """);

        // ── 2. Call stack: -Xss ───────────────────────────────────────────────
        System.out.println("=== CALL STACK (-Xss) ===");
        System.out.println("""
          -Xss sets the call stack size PER THREAD.
          Your machine: 2048 KB = 2MB per thread (default on Apple Silicon)

          Every method call = one frame pushed onto call stack:
            frame size depends on local variables + params
            recurse() with no vars ≈ 47 bytes → ~44,000 depth before crash
            dfs(graph, node, visited) ≈ 200 bytes → ~10,000 depth before crash

          java -Xss512k MyClass   → 512KB  (smaller, saves memory for many threads)
          java -Xss4m   MyClass   → 4MB    (bigger, allows deeper recursion)
          java -Xss16m  MyClass   → 16MB   (very deep recursion, rare need)

          Rule: don't increase Xss — fix deep recursion with iterative + Stack<>
          """);

        // ── 3. -XX:+PrintFlagsFinal ───────────────────────────────────────────
        System.out.println("=== -XX:+PrintFlagsFinal ===");
        System.out.println("""
          Prints EVERY JVM internal flag and its current value.
          Run in terminal (not in code):

            java -XX:+PrintFlagsFinal -version 2>&1 | grep ThreadStackSize
            java -XX:+PrintFlagsFinal -version 2>&1 | grep HeapSize

          -XX flag syntax:
            -XX:+FlagName        turn ON  a boolean flag
            -XX:-FlagName        turn OFF a boolean flag
            -XX:FlagName=value   set a numeric/string flag

          Common -XX flags:
            -XX:+PrintFlagsFinal       print all flags
            -XX:+UseG1GC               use G1 garbage collector
            -XX:ThreadStackSize=2048   stack size in KB (same as -Xss2m)
            -XX:MaxHeapSize=4g         same as -Xmx4g
            -XX:InitialHeapSize=256m   same as -Xms256m
          """);

        // ── 4. -X vs -XX ─────────────────────────────────────────────────────
        System.out.println("=== -X vs -XX shorthand ===");
        System.out.println("""
          -X flags   = shorthand for common settings (stable, won't change)
          -XX flags  = advanced/internal flags (may change between JVM versions)

          Shorthand       Full -XX equivalent
          ──────────────  ──────────────────────────────
          -Xss2m          -XX:ThreadStackSize=2048
          -Xmx4g          -XX:MaxHeapSize=4g
          -Xms256m        -XX:InitialHeapSize=256m

          In practice: always use -Xss, -Xmx, -Xms (cleaner)
          Use -XX only when no -X shorthand exists
          """);
    }
}
