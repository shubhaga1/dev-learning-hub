import java.util.function.*;
import java.util.*;

/**
 * FUNCTIONAL INTERFACES — Function, Predicate, Consumer, Supplier
 *
 * A functional interface = interface with exactly ONE abstract method.
 * This lets you pass behaviour (code) as a value — using a lambda.
 *
 * The 4 most important ones:
 *   Function<T, R>    → takes T,  returns R      (transform)
 *   Predicate<T>      → takes T,  returns boolean (test/filter)
 *   Consumer<T>       → takes T,  returns nothing (side effect)
 *   Supplier<T>       → takes nothing, returns T  (produce)
 *
 * Run: javac 02_FunctionalInterfaces.java && java FunctionalInterfaces
 */
class FunctionalInterfaces {

    // ─── 1. Function<T, R> — takes T, returns R ──────────────────────────────
    static void functionDemo() {
        System.out.println("=== Function<T, R> — transform ===");

        // Long way: anonymous class
        Function<String, Integer> lengthLong = new Function<String, Integer>() {
            public Integer apply(String s) { return s.length(); }
        };

        // Short way: lambda  (s) -> s.length()
        Function<String, Integer> length = s -> s.length();

        // Even shorter: method reference
        Function<String, Integer> lengthRef = String::length;

        System.out.println(length.apply("Shubham"));    // 7
        System.out.println(lengthRef.apply("Shubham")); // 7

        // Chain functions: andThen
        Function<Integer, Integer> doubleIt = n -> n * 2;
        Function<Integer, Integer> addTen   = n -> n + 10;

        Function<Integer, Integer> doubleThenAdd = doubleIt.andThen(addTen);
        Function<Integer, Integer> addThenDouble = doubleIt.compose(addTen);  // reverse order

        System.out.println("doubleThenAdd(5) = " + doubleThenAdd.apply(5)); // (5*2)+10 = 20
        System.out.println("addThenDouble(5) = " + addThenDouble.apply(5)); // (5+10)*2 = 30
    }

    // ─── 2. Predicate<T> — takes T, returns boolean ──────────────────────────
    static void predicateDemo() {
        System.out.println("\n=== Predicate<T> — test / filter ===");

        Predicate<Integer> isEven    = n -> n % 2 == 0;
        Predicate<Integer> isPositive = n -> n > 0;
        Predicate<String>  isLong    = s -> s.length() > 5;

        System.out.println("isEven(4)     = " + isEven.test(4));      // true
        System.out.println("isEven(7)     = " + isEven.test(7));      // false
        System.out.println("isLong(\"Hi\") = " + isLong.test("Hi"));   // false

        // Combine predicates
        Predicate<Integer> isEvenAndPositive = isEven.and(isPositive);
        Predicate<Integer> isEvenOrPositive  = isEven.or(isPositive);
        Predicate<Integer> isOdd             = isEven.negate();

        System.out.println("isEvenAndPositive(4)  = " + isEvenAndPositive.test(4));   // true
        System.out.println("isEvenAndPositive(-4) = " + isEvenAndPositive.test(-4));  // false
        System.out.println("isOdd(7)              = " + isOdd.test(7));               // true

        // Real use: filter a list manually
        List<Integer> nums = Arrays.asList(1, -2, 3, -4, 5, 6, -7, 8);
        System.out.print("Even positives: ");
        for (int n : nums) {
            if (isEvenAndPositive.test(n)) System.out.print(n + " ");
        }
        System.out.println();
    }

    // ─── 3. Consumer<T> — takes T, returns nothing ───────────────────────────
    static void consumerDemo() {
        System.out.println("\n=== Consumer<T> — side effects ===");

        Consumer<String> print       = s -> System.out.println("  → " + s);
        Consumer<String> printUpper  = s -> System.out.println("  → " + s.toUpperCase());

        print.accept("hello");        // side effect: prints
        printUpper.accept("hello");

        // andThen: chain consumers
        Consumer<String> both = print.andThen(printUpper);
        both.accept("shubham");       // runs print, then printUpper

        // BiConsumer — takes two arguments
        BiConsumer<String, Integer> printWithScore = (name, score) ->
            System.out.println("  " + name + " scored " + score);
        printWithScore.accept("Alice", 95);
    }

    // ─── 4. Supplier<T> — takes nothing, returns T ───────────────────────────
    static void supplierDemo() {
        System.out.println("\n=== Supplier<T> — produce a value ===");

        Supplier<String>  greeting  = () -> "Hello World";
        Supplier<Double>  random    = () -> Math.random();
        Supplier<List<Integer>> newList = () -> new ArrayList<>();

        System.out.println(greeting.get());     // Hello World
        System.out.println(random.get());       // random number
        System.out.println(newList.get());      // []

        // Real use: lazy initialization — only create if needed
        Supplier<String> expensiveOp = () -> {
            // pretend this is slow
            return "result of expensive operation";
        };
        // The code inside doesn't run until .get() is called
        System.out.println(expensiveOp.get());
    }

    // ─── 5. Your own Functional Interface ────────────────────────────────────
    @FunctionalInterface   // annotation ensures only 1 abstract method
    interface Transformer<T> {
        T transform(T input);

        // can still have default methods
        default T transformTwice(T input) {
            return transform(transform(input));
        }
    }

    static void customFunctionalInterface() {
        System.out.println("\n=== Custom @FunctionalInterface ===");

        Transformer<String> shout    = s -> s.toUpperCase() + "!";
        Transformer<Integer> triple  = n -> n * 3;

        System.out.println(shout.transform("hello"));          // HELLO!
        System.out.println(shout.transformTwice("hello"));     // HELLO!!  (default)
        System.out.println(triple.transformTwice(4));          // 4*3*3 = 36
    }

    // ─── 6. Passing functions as arguments ───────────────────────────────────
    // This is what computeIfAbsent does — takes a Function as argument
    static <T> void applyToAll(List<T> list, Consumer<T> action) {
        for (T item : list) {
            action.accept(item);
        }
    }

    static <T, R> List<R> transformAll(List<T> list, Function<T, R> fn) {
        List<R> result = new ArrayList<>();
        for (T item : list) {
            result.add(fn.apply(item));
        }
        return result;
    }

    static void passingFunctions() {
        System.out.println("\n=== Passing functions as arguments ===");

        List<String> names = Arrays.asList("alice", "bob", "charlie");

        // pass a Consumer
        applyToAll(names, s -> System.out.println("  Hello, " + s));

        // pass a Function
        List<Integer> lengths = transformAll(names, String::length);
        System.out.println("Lengths: " + lengths);   // [5, 3, 7]

        List<String> upper = transformAll(names, String::toUpperCase);
        System.out.println("Upper:   " + upper);     // [ALICE, BOB, CHARLIE]
    }

    public static void main(String[] args) {
        functionDemo();
        predicateDemo();
        consumerDemo();
        supplierDemo();
        customFunctionalInterface();
        passingFunctions();

        System.out.println("""

        QUICK REFERENCE:
          Function<T,R>   fn  → fn.apply(value)      → returns R
          Predicate<T>    p   → p.test(value)         → returns boolean
          Consumer<T>     c   → c.accept(value)       → returns void
          Supplier<T>     s   → s.get()               → returns T (no input)

          Combine:
            fn.andThen(fn2)   → fn first, then fn2
            fn.compose(fn2)   → fn2 first, then fn
            p.and(p2)         → both must be true
            p.or(p2)          → either true
            p.negate()        → flip the result
            c.andThen(c2)     → run c then c2
        """);
    }
}
