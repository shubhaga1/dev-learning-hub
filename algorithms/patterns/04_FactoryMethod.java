/**
 * Pattern 4 — Factory Method
 * Venkat: "The 'new' keyword tightly couples you to a concrete class. Factory methods decouple."
 *
 * Problem with 'new':
 *   Animal a = new Dog();    // caller decides the type — tight coupling
 *
 * Factory method: let a method or interface decide what to create
 *   Animal a = Animal.create("dog");   // caller asks, factory decides
 *
 * Modern Java: use static factory methods + default interface methods
 */
class FactoryMethod {

    // ── TIGHT COUPLING with 'new' — BAD ──────────────────────────────────────

    static class CreditCardPaymentBAD {
        void pay(double amount) { System.out.println("Credit card: " + amount); }
    }
    static class UpiPaymentBAD {
        void pay(double amount) { System.out.println("UPI: " + amount); }
    }
    // Caller must know which class to instantiate — if you add WalletPayment, caller changes too

    // ── FACTORY METHOD — GOOD ────────────────────────────────────────────────

    interface Payment {
        void pay(double amount);

        // Static factory method ON the interface — caller never uses 'new'
        static Payment of(String type) {
            return switch (type.toLowerCase()) {
                case "credit" -> amount -> System.out.println("  Credit card: ₹" + amount);
                case "upi"    -> amount -> System.out.println("  UPI: ₹" + amount);
                case "wallet" -> amount -> System.out.println("  Wallet: ₹" + amount);
                default       -> throw new IllegalArgumentException("Unknown: " + type);
            };
        }

        // Default method — shared behaviour without forcing subclasses to implement
        default void payWithTax(double amount, double taxPct) {
            pay(amount * (1 + taxPct / 100));
        }
    }

    // ── ABSTRACT FACTORY — for families of objects ────────────────────────────

    interface Button {
        void render();
    }
    interface Checkbox {
        void render();
    }

    interface UIFactory {
        Button  createButton();
        Checkbox createCheckbox();

        static UIFactory forTheme(String theme) {
            return switch (theme) {
                case "dark"  -> new DarkThemeFactory();
                case "light" -> new LightThemeFactory();
                default      -> throw new IllegalArgumentException("Unknown theme: " + theme);
            };
        }
    }

    static class DarkThemeFactory implements UIFactory {
        public Button   createButton()   { return () -> System.out.println("  [Dark Button]"); }
        public Checkbox createCheckbox() { return () -> System.out.println("  [Dark Checkbox]"); }
    }

    static class LightThemeFactory implements UIFactory {
        public Button   createButton()   { return () -> System.out.println("  [Light Button]"); }
        public Checkbox createCheckbox() { return () -> System.out.println("  [Light Checkbox]"); }
    }

    public static void main(String[] args) {
        // ── Factory method on interface ───────────────────────────────────────
        System.out.println("Payment factory:");
        Payment.of("credit").pay(500);
        Payment.of("upi").pay(200);
        Payment.of("wallet").pay(150);

        System.out.println("\nWith tax (default method):");
        Payment.of("credit").payWithTax(1000, 18);   // GST 18%

        // Adding a new payment type = add one line in the switch — caller code unchanged

        // ── Abstract factory ──────────────────────────────────────────────────
        System.out.println("\nUI Factory — dark theme:");
        UIFactory darkUI = UIFactory.forTheme("dark");
        darkUI.createButton().render();
        darkUI.createCheckbox().render();

        System.out.println("\nUI Factory — light theme:");
        UIFactory lightUI = UIFactory.forTheme("light");
        lightUI.createButton().render();
        lightUI.createCheckbox().render();
    }
}
