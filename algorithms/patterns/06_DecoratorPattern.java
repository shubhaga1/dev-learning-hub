import java.util.function.Function;

/**
 * Pattern 6 — Decorator Pattern with Function Composition
 * Venkat: "Traditional decorators are complex. With lambdas, composing functions IS the decorator."
 *
 * Decorator adds behaviour to an object without modifying it.
 * Traditional: class wraps class wraps class (Java I/O InputStream hell)
 * Modern:      compose Function<T,T> — each step transforms and passes forward
 *
 * Function.andThen(f) = apply this, then apply f
 * Function.compose(f) = apply f first, then apply this
 */
class DecoratorPattern {

    // ── TRADITIONAL — class wraps class wraps class ───────────────────────────

    interface TextProcessor {
        String process(String text);
    }

    static class PlainText implements TextProcessor {
        public String process(String text) { return text; }
    }

    static class TrimDecorator implements TextProcessor {
        private final TextProcessor wrapped;
        TrimDecorator(TextProcessor t) { this.wrapped = t; }
        public String process(String text) { return wrapped.process(text).trim(); }
    }

    static class UpperCaseDecorator implements TextProcessor {
        private final TextProcessor wrapped;
        UpperCaseDecorator(TextProcessor t) { this.wrapped = t; }
        public String process(String text) { return wrapped.process(text).toUpperCase(); }
    }

    static class LogDecorator implements TextProcessor {
        private final TextProcessor wrapped;
        LogDecorator(TextProcessor t) { this.wrapped = t; }
        public String process(String text) {
            String result = wrapped.process(text);
            System.out.println("  [log] processed: " + result);
            return result;
        }
    }

    // ── MODERN — compose functions, no extra classes needed ───────────────────

    static Function<String, String> trim      = String::trim;
    static Function<String, String> upperCase = String::toUpperCase;
    static Function<String, String> log       = text -> {
        System.out.println("  [log] " + text);
        return text;
    };
    static Function<String, String> addBrackets = text -> "[" + text + "]";

    // ── Image filter example (from Venkat's colour filter demo) ──────────────

    record Colour(int r, int g, int b) {
        @Override public String toString() { return "RGB(" + r + "," + g + "," + b + ")"; }
    }

    static Function<Colour, Colour> brighten = c ->
        new Colour(Math.min(255, c.r() + 30), Math.min(255, c.g() + 30), Math.min(255, c.b() + 30));

    static Function<Colour, Colour> grayscale = c -> {
        int avg = (c.r() + c.g() + c.b()) / 3;
        return new Colour(avg, avg, avg);
    };

    static Function<Colour, Colour> invertRed = c ->
        new Colour(255 - c.r(), c.g(), c.b());

    public static void main(String[] args) {
        // ── Traditional (nested constructors — the "I/O stream problem") ─────
        System.out.println("Traditional decorator:");
        TextProcessor pipeline = new LogDecorator(
                                    new UpperCaseDecorator(
                                        new TrimDecorator(
                                            new PlainText())));
        pipeline.process("  hello world  ");

        // ── Modern — compose functions ────────────────────────────────────────
        System.out.println("\nFunction composition:");
        Function<String, String> textPipeline =
            trim.andThen(upperCase).andThen(addBrackets).andThen(log);

        String result = textPipeline.apply("  hello world  ");
        System.out.println("  Result: " + result);

        // Mix and match without new classes
        Function<String, String> simpleClean = trim.andThen(upperCase);
        System.out.println("  Simple: " + simpleClean.apply("  venkat  "));

        // ── Colour filter pipeline ────────────────────────────────────────────
        System.out.println("\nColour filter pipeline:");
        Colour original = new Colour(100, 150, 200);
        System.out.println("  Original : " + original);

        Function<Colour, Colour> filter = brighten.andThen(grayscale);
        System.out.println("  Brighten + Grayscale : " + filter.apply(original));

        Function<Colour, Colour> filterB = brighten.andThen(invertRed);
        System.out.println("  Brighten + InvertRed : " + filterB.apply(original));

        // Add a new filter = one more andThen — no new class, no modification
        Function<Colour, Colour> fullFilter = brighten.andThen(grayscale).andThen(invertRed);
        System.out.println("  Full pipeline        : " + fullFilter.apply(original));
    }
}
