import java.util.function.Consumer;

/**
 * Pattern 7 — Fluent Interface + Execute-Around Method
 * Venkat: "Returning 'this' enables method chaining. Execute-around manages resources safely."
 *
 * Fluent Interface: method chaining by returning 'this' — reads like a sentence
 *   new Pizza().crust("thin").sauce("tomato").cheese("mozzarella").build()
 *
 * Execute-Around: wrap a block of code with setup/teardown — caller provides the block
 *   DB.transaction(conn -> { conn.save(order); conn.save(invoice); });
 *   The method opens and closes the transaction — caller only writes business logic
 */
class FluentAndExecuteAround {

    // ── FLUENT INTERFACE — builder with method chaining ───────────────────────

    static class Pizza {
        private String crust   = "regular";
        private String sauce   = "tomato";
        private String cheese  = "mozzarella";
        private boolean extraCheese = false;

        Pizza crust(String crust)        { this.crust = crust;             return this; }
        Pizza sauce(String sauce)        { this.sauce = sauce;             return this; }
        Pizza cheese(String cheese)      { this.cheese = cheese;           return this; }
        Pizza extraCheese()              { this.extraCheese = true;        return this; }

        Pizza build() { return this; }  // terminal — returns final object

        @Override public String toString() {
            return "Pizza[crust=" + crust + ", sauce=" + sauce +
                   ", cheese=" + cheese + (extraCheese ? " + EXTRA" : "") + "]";
        }
    }

    // ── FLUENT QUERY BUILDER ───────────────────────────────────────────────────

    static class QueryBuilder {
        private String table;
        private String condition = "";
        private int    limit     = 100;
        private String orderBy   = "";

        QueryBuilder from(String table)      { this.table = table;         return this; }
        QueryBuilder where(String condition) { this.condition = condition; return this; }
        QueryBuilder limit(int n)            { this.limit = n;             return this; }
        QueryBuilder orderBy(String col)     { this.orderBy = col;         return this; }

        String build() {
            return "SELECT * FROM " + table
                + (condition.isEmpty() ? "" : " WHERE " + condition)
                + (orderBy.isEmpty()   ? "" : " ORDER BY " + orderBy)
                + " LIMIT " + limit;
        }
    }

    // ── EXECUTE-AROUND — resource management via lambda ───────────────────────

    // Simulated DB connection
    static class DbConnection {
        private final String name;
        DbConnection(String name) { this.name = name; }
        void save(String record)  { System.out.println("  [" + name + "] Saving: " + record); }
        void commit()             { System.out.println("  [" + name + "] COMMIT"); }
        void rollback()           { System.out.println("  [" + name + "] ROLLBACK"); }
    }

    // Execute-around: opens transaction, runs caller's block, commits or rolls back
    static void transaction(Consumer<DbConnection> block) {
        DbConnection conn = new DbConnection("DB");
        System.out.println("  [DB] BEGIN TRANSACTION");
        try {
            block.accept(conn);    // caller provides the business logic
            conn.commit();
        } catch (Exception e) {
            conn.rollback();
            System.out.println("  Error: " + e.getMessage());
        }
    }

    // File resource execute-around
    static void withFile(String fileName, Consumer<String> block) {
        System.out.println("  [File] Opening: " + fileName);
        try {
            block.accept("content of " + fileName);  // caller reads/writes
        } finally {
            System.out.println("  [File] Closing: " + fileName);  // always runs
        }
    }

    public static void main(String[] args) {
        // ── Fluent pizza builder ───────────────────────────────────────────────
        System.out.println("Fluent interface — Pizza:");
        Pizza pizza = new Pizza()
            .crust("thin")
            .sauce("pesto")
            .cheese("parmesan")
            .extraCheese()
            .build();
        System.out.println("  " + pizza);

        // ── Fluent query builder ───────────────────────────────────────────────
        System.out.println("\nFluent query builder:");
        String query = new QueryBuilder()
            .from("orders")
            .where("status = 'pending'")
            .orderBy("created_at DESC")
            .limit(50)
            .build();
        System.out.println("  " + query);

        // ── Execute-around — transaction ──────────────────────────────────────
        System.out.println("\nExecute-around — successful transaction:");
        transaction(conn -> {
            conn.save("Order #1001");
            conn.save("Invoice #501");
            // caller writes only business logic — no begin/commit boilerplate
        });

        System.out.println("\nExecute-around — transaction with error:");
        transaction(conn -> {
            conn.save("Order #1002");
            if (true) throw new RuntimeException("Payment failed");
            conn.save("Invoice #502");  // never reached
        });

        // ── Execute-around — file ─────────────────────────────────────────────
        System.out.println("\nExecute-around — file:");
        withFile("report.txt", content -> {
            System.out.println("  Processing: " + content);
        });
        // file always closed — even if exception thrown inside
    }
}
