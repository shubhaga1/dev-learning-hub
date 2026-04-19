
/**
 * StaticVsInstance — When to use static vs instance variables/methods
 *
 * Rule: ask "should every object have its own copy?"
 *   Yes → instance variable
 *   No  → static variable (shared across all objects)
 *
 * Key learnings:
 *   1. Instance variables: one per object, accessed via 'this'
 *   2. Static variables: one per class, shared across all objects
 *   3. Static methods: can't access instance variables — no 'this'
 *   4. Instance methods: can access both instance and static members
 */
class StaticVsInstance {

    // ── Instance variables — each object gets its own copy ───────────────────
    double balance;
    String owner;

    // ── Static variables — shared across ALL objects of this class ───────────
    static double interestRate = 0.05;   // same rate for every account
    static int totalAccounts   = 0;      // count of all BankAccount objects ever created

    StaticVsInstance(String owner, double balance) {
        this.owner   = owner;
        this.balance = balance;
        totalAccounts++;                 // increment shared counter on every new object
    }

    // ── Instance method — has 'this', can read instance variables ─────────────
    void showBalance() {
        System.out.println(owner + " balance: " + balance
                         + "  (rate: " + interestRate + ")");
    }

    // ── Static method — no 'this', cannot access balance or owner ─────────────
    // Good for: utilities, factories, counters that don't belong to one object
    static void showTotalAccounts() {
        System.out.println("Total accounts created: " + totalAccounts);
        // System.out.println(balance);  // ✗ compile error — no instance context
    }

    // ── Static method trying to access instance variable — BROKEN ─────────────
    // Uncomment to see compile error:
    // static void broken() {
    //     System.out.println(balance);  // ERROR: non-static variable balance
    // }                                 // cannot be referenced from a static context

    public static void main(String[] args) {
        StaticVsInstance a = new StaticVsInstance("Alice", 1000);
        StaticVsInstance b = new StaticVsInstance("Bob",   5000);
        StaticVsInstance c = new StaticVsInstance("Carol", 2500);

        // Each object has its own balance
        a.showBalance();   // Alice balance: 1000.0  (rate: 0.05)
        b.showBalance();   // Bob   balance: 5000.0  (rate: 0.05)
        c.showBalance();   // Carol balance: 2500.0  (rate: 0.05)

        // Shared counter — call on class, not object
        StaticVsInstance.showTotalAccounts();  // Total accounts created: 3

        // Changing static variable affects ALL objects
        System.out.println("\n-- Rate changed to 0.07 --");
        interestRate = 0.07;
        a.showBalance();   // Alice balance: 1000.0  (rate: 0.07) ← picked up new rate
        b.showBalance();   // Bob   balance: 5000.0  (rate: 0.07) ← same

        // Changing instance variable affects only that object
        System.out.println("\n-- Alice deposit 500 --");
        a.balance += 500;
        a.showBalance();   // Alice balance: 1500.0
        b.showBalance();   // Bob   balance: 5000.0  ← unchanged
    }
}
