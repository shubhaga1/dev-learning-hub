/**
 * ANNOTATIONS — Java
 *
 * Annotation = metadata attached to code. Does NOT execute by itself.
 * It's a label that tells the compiler, JVM, or a framework something about your code.
 *
 * Three levels of use:
 *   1. Compiler instructions  (@Override, @SuppressWarnings, @Deprecated)
 *   2. Runtime processing     (Spring @Autowired, JUnit @Test, Sling @Model)
 *   3. Code generation        (Lombok @Data, @Builder)
 *
 * Who reads annotations?
 *   Compiler  → at compile time (javac)
 *   JVM       → at class load time
 *   Framework → at runtime via Reflection API
 */

import java.lang.annotation.*;
import java.lang.reflect.Method;

class AnnotationsDemo {

    // ── Built-in Java annotations ─────────────────────────────────────────────

    static class Animal {
        public String sound() { return "..."; }

        @Deprecated  // tells compiler "don't use this method, it's old"
        public String oldSound() { return "..."; }
    }

    static class Dog extends Animal {

        @Override  // tells COMPILER: "this must exist in parent class"
        public String sound() { return "Woof"; }
        // If you typo: "soound()" → compiler error immediately
        // Without @Override: no error, but parent method not overridden (silent bug)

        @SuppressWarnings({"unchecked", "rawtypes"})  // silence unchecked + raw type warnings
        public void riskyMethod() {
            java.util.List list = new java.util.ArrayList();  // raw type — causes unchecked warning
            list.add("item");
        }
    }

    // ── Custom annotation — how annotations are BUILT ─────────────────────────

    // Step 1: define the annotation
    @Retention(RetentionPolicy.RUNTIME)  // keep annotation info at runtime
    @Target(ElementType.METHOD)          // only allowed on methods
    @interface RunTest {
        String description() default "no description";
        int priority() default 1;
    }

    // Step 2: use the annotation
    static class MathUtils {

        @RunTest(description = "checks addition", priority = 1)
        public static boolean testAdd() {
            int sum = 2 + 2;
            return sum == 4;
        }

        @RunTest(description = "checks subtraction", priority = 2)
        public static boolean testSubtract() {
            int diff = 5 - 3;
            return diff == 2;
        }

        public static boolean helperMethod() {  // no @RunTest — will be skipped
            return true;
        }
    }

    // Step 3: framework reads annotation at runtime using Reflection
    static void runAnnotatedTests(Class<?> clazz) throws Exception {
        System.out.println("\nRunning tests in: " + clazz.getSimpleName());
        for (Method method : clazz.getDeclaredMethods()) {
            if (method.isAnnotationPresent(RunTest.class)) {
                RunTest annotation = method.getAnnotation(RunTest.class);
                boolean result = (boolean) method.invoke(null);  // call the method
                System.out.printf("  [P%d] %-20s → %s  (%s)%n",
                    annotation.priority(),
                    method.getName(),
                    result ? "PASS" : "FAIL",
                    annotation.description()
                );
            }
        }
    }

    // ── @Retention values ─────────────────────────────────────────────────────
    /*
     * RetentionPolicy.SOURCE   → exists only in .java, stripped by compiler
     *                            (e.g. @SuppressWarnings, @Override)
     * RetentionPolicy.CLASS    → kept in .class file, not at runtime (default)
     * RetentionPolicy.RUNTIME  → kept at runtime, readable via Reflection
     *                            (e.g. @Test, @Autowired, @Model)
     */

    // ── @Target values ────────────────────────────────────────────────────────
    /*
     * ElementType.TYPE         → class, interface, enum
     * ElementType.METHOD       → methods
     * ElementType.FIELD        → fields/variables
     * ElementType.PARAMETER    → method parameters
     * ElementType.CONSTRUCTOR  → constructors
     */

    // ── How frameworks use annotations (simplified Spring-like example) ────────
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.FIELD)
    @interface Inject { }  // like Spring's @Autowired

    static class Engine {
        public String start() { return "Engine started"; }
    }

    static class Car {
        @Inject
        Engine engine;  // framework will inject this
    }

    // Simulate what Spring does internally:
    static void injectDependencies(Object obj) throws Exception {
        for (var field : obj.getClass().getDeclaredFields()) {
            if (field.isAnnotationPresent(Inject.class)) {
                field.setAccessible(true);
                Object dependency = field.getType().getDeclaredConstructor().newInstance();
                field.set(obj, dependency);
                System.out.println("Injected: " + field.getType().getSimpleName() + " into " + obj.getClass().getSimpleName());
            }
        }
    }

    public static void main(String[] args) throws Exception {

        // ── Built-in: @Override in action ────────────────────────────────────
        Dog dog = new Dog();
        System.out.println("Dog sound: " + dog.sound());  // Woof (overridden)

        Animal a = new Dog();
        System.out.println("Animal ref, Dog obj: " + a.sound());  // Woof — polymorphism

        // ── @Deprecated usage ─────────────────────────────────────────────────
        Dog d = new Dog();
        d.oldSound();  // compiler shows warning: "oldSound() is deprecated"

        // ── Custom annotation + Reflection ────────────────────────────────────
        runAnnotatedTests(MathUtils.class);
        // → [P1] testAdd    → PASS  (checks addition)
        // → [P2] testSubtract → PASS (checks subtraction)
        // helperMethod is skipped — no @RunTest annotation

        // ── Dependency injection via annotation ────────────────────────────────
        Car car = new Car();
        System.out.println("\nBefore inject: car.engine = " + car.engine);  // null
        injectDependencies(car);
        System.out.println("After inject:  " + car.engine.start());         // Engine started

        // ── Key insight ───────────────────────────────────────────────────────
        System.out.println("""

        Annotation is just a LABEL. It does nothing by itself.
        Someone has to READ it:
          @Override      → compiler reads it
          @Test          → JUnit reads it at runtime via Reflection
          @Autowired     → Spring reads it at runtime via Reflection
          @Model         → Sling reads it at runtime via Reflection
          @RunTest above → our runAnnotatedTests() reads it via Reflection
        """);
    }
}
