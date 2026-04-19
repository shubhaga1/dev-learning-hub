/**
 * LAMBDA EXPRESSIONS — Java 8
 *
 * Lambda = anonymous function. Shorthand for implementing a functional interface.
 *
 * Syntax:
 *   (params) -> expression
 *   (params) -> { statements; }
 *
 * Rules:
 *   - Can only be used where a functional interface is expected
 *   - Can capture effectively-final variables from enclosing scope
 *   - Cannot modify captured local variables
 *
 * Method references (shorthand for lambdas):
 *   ClassName::staticMethod     String::valueOf
 *   instance::method            System.out::println
 *   ClassName::instanceMethod   String::toUpperCase
 *   ClassName::new              ArrayList::new
 */
import java.util.*;
import java.util.function.*;
import java.util.stream.*;

class Lambda {

    @FunctionalInterface
    interface Transformer<T> {
        T transform(T input);
    }

    public static void main(String[] args) {

        // ── Basic lambda syntax ───────────────────────────────────────────────
        Runnable r1 = () -> System.out.println("Hello from lambda");
        r1.run();

        Comparator<String> byLength = (a, b) -> a.length() - b.length();
        List<String> names = new ArrayList<>(List.of("Charlie", "Alice", "Bob", "Diana"));
        names.sort(byLength);
        System.out.println("Sorted by length: " + names);  // [Bob, Alice, Diana, Charlie]

        // ── Custom functional interface ───────────────────────────────────────
        Transformer<String> upper = s -> s.toUpperCase();
        Transformer<String> trim  = s -> s.trim();
        System.out.println(upper.transform("  hello  "));  // "  HELLO  "
        System.out.println(trim.transform("  hello  "));   // "hello"

        // ── Variable capture — must be effectively final ───────────────────────
        String prefix = "Mr. ";  // effectively final (never reassigned)
        Function<String, String> addPrefix = name -> prefix + name;
        System.out.println(addPrefix.apply("Smith"));  // Mr. Smith

        // ── Method references ─────────────────────────────────────────────────
        // Static method reference
        Function<String, Integer> parse = Integer::parseInt;
        System.out.println(parse.apply("42"));  // 42

        // Instance method reference
        List<String> words = List.of("apple", "banana", "cherry");
        words.stream().map(String::toUpperCase).forEach(System.out::println);

        // Constructor reference
        Function<String, StringBuilder> sbFactory = StringBuilder::new;
        StringBuilder sb = sbFactory.apply("hello");
        System.out.println(sb.reverse());  // olleh

        // ── Chaining with andThen / compose ──────────────────────────────────
        Function<Integer, Integer> times2  = x -> x * 2;
        Function<Integer, Integer> plus10  = x -> x + 10;

        // andThen: times2 THEN plus10
        System.out.println(times2.andThen(plus10).apply(5));  // (5*2)+10 = 20

        // compose: plus10 THEN times2
        System.out.println(times2.compose(plus10).apply(5));  // (5+10)*2 = 30

        // ── Predicate chaining ────────────────────────────────────────────────
        Predicate<String> isLong  = s -> s.length() > 5;
        Predicate<String> startsA = s -> s.startsWith("A");

        List<String> data = List.of("Alice", "Anthony", "Bob", "Alexander");
        data.stream()
            .filter(isLong.and(startsA))          // long AND starts with A
            .forEach(System.out::println);          // Anthony, Alexander

        // ── forEach with lambda ───────────────────────────────────────────────
        Map<String, Integer> scores = Map.of("Alice", 90, "Bob", 75, "Carol", 85);
        scores.forEach((name, score) ->
            System.out.println(name + " scored " + score));
    }
}
