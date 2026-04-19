import java.util.*;

/**
 * WHY JAVA HITS THE SWEET SPOT — Python vs Java vs Rust/C
 *
 * Three dimensions:
 *   Runtime performance   → how fast code runs
 *   Developer productivity → how fast you write correct code
 *   Maintainability       → how easy to change code without breaking things
 *
 *                    Python    Java     Rust/C
 *   Performance        ❌        ✅        ✅✅
 *   Productivity       ✅✅       ✅        ❌
 *   Maintainability    ❌        ✅✅       ✅
 */
class JavaSweetSpot {

    // ── 1. STATIC TYPING — Java catches bugs at COMPILE time ─────────────────
    //
    // Python (dynamic typing) — bug found at RUNTIME (in production):
    //   def add(a, b): return a + b
    //   add("5", 3)    → crashes at runtime: TypeError
    //   add([1,2], 3)  → crashes at runtime: TypeError
    //
    // Java (static typing) — bug found at COMPILE time (before running):
    static int add(int a, int b) { return a + b; }
    // add("5", 3)   → ❌ won't even compile — caught immediately
    // add(5, 3)     → ✅ guaranteed to work

    // Real impact at Netflix scale:
    //   Python: type bugs slip through to prod → pages oncall at 3am
    //   Java:   compiler rejects type mismatches → never reaches prod

    // ── 2. GENERICS — type safety across collections ──────────────────────────
    //
    // Python list — no guarantee what's inside:
    //   items = [1, "hello", True, None]   → all allowed, chaos
    //   for item in items: item * 2        → crashes on "hello"
    //
    // Java generics — compiler enforces the contract:
    static void genericsDemo() {
        List<Integer> numbers = new ArrayList<>();
        numbers.add(1);
        numbers.add(2);
        // numbers.add("hello");  ← ❌ compile error — caught before running
        int sum = 0;
        for (int n : numbers) sum += n;  // guaranteed safe — no type check needed
        System.out.println("Sum: " + sum);
    }

    // ── 3. MEMORY — Java GC vs C manual management ───────────────────────────
    //
    // C (manual memory) — developer responsible for every allocation:
    //   int* arr = malloc(100 * sizeof(int));  // allocate
    //   // ... use arr ...
    //   free(arr);                             // must free — or memory leak
    //   arr[200] = 5;                          // buffer overflow — silent corruption
    //   free(arr); free(arr);                  // double free — crash
    //
    // Java (GC) — just create objects, JVM cleans up:
    static void memoryDemo() {
        List<String> items = new ArrayList<>();   // allocate
        items.add("Netflix");
        items.add("Streaming");
        // no free() needed — GC reclaims when items goes out of scope
        // no buffer overflow possible — Java checks array bounds
        System.out.println("Items: " + items);
    }
    // Cost: GC pauses (milliseconds) — acceptable for most services
    // Rust avoids GC with ownership rules — zero pauses but complex to write

    // ── 4. JIT — Java warms up and gets FASTER over time ─────────────────────
    //
    // Python: interpreted line by line every run — always same speed
    // C/Rust: compiled to machine code ahead of time — fast from start
    // Java:   starts interpreted → JIT compiles hot paths → FASTER than start
    //
    // JIT = Just In Time compiler
    //   JVM watches which code runs most often (hot paths)
    //   After ~10,000 calls → compiles that method to native machine code
    //   Netflix API handlers called millions/sec → fully JIT-compiled → C-like speed
    static void jitDemo() {
        long start = System.nanoTime();
        long sum = 0;
        for (int i = 0; i < 10_000_000; i++) sum += i;
        long warmEnd = System.nanoTime();

        // run again — JIT has compiled this loop to native code now
        sum = 0;
        for (int i = 0; i < 10_000_000; i++) sum += i;
        long hotEnd = System.nanoTime();

        System.out.printf("Cold run : %,d ns%n", warmEnd - start);
        System.out.printf("Hot run  : %,d ns  ← JIT compiled, faster%n", hotEnd - warmEnd);
        System.out.println("Sum: " + sum);
    }

    // ── 5. SWEET SPOT SUMMARY ─────────────────────────────────────────────────
    static void summary() {
        System.out.println("""
          Python  → great for scripting, ML, quick code
                    ❌ 10–100x slower than Java
                    ❌ type bugs only caught at runtime
                    ❌ GIL limits true parallelism

          Rust/C  → fastest possible, zero GC pauses
                    ❌ manual memory (malloc/free) or ownership rules
                    ❌ 3–5x longer to write the same feature
                    ❌ steep learning curve → slower teams

          Java    → ✅ JIT-compiled → near C speed for hot paths
                    ✅ GC → no manual memory management
                    ✅ static typing → bugs caught at compile time
                    ✅ generics → type-safe collections
                    ✅ massive ecosystem (Spring, Kafka clients, gRPC...)
                    ✅ same jar runs on any OS (JVM portability)

          Netflix chose Java because:
            - API servers handle 10M+ req/sec → need C-like speed
            - 1000s of engineers → need compiler to catch mistakes
            - Microservices → need JVM portability across machines
          """);
    }

    public static void main(String[] args) {
        System.out.println("=== 1. Generics (type safety) ===");
        genericsDemo();

        System.out.println("\n=== 2. Memory (GC) ===");
        memoryDemo();

        System.out.println("\n=== 3. JIT warmup ===");
        jitDemo();

        System.out.println("\n=== 4. Sweet spot summary ===");
        summary();
    }
}
