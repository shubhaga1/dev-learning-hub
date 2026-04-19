
import java.util.ArrayList;
import java.util.List;

/**
 * Q1: Single Responsibility — each method should do ONE thing
 *
 * Level 1 → obvious god method
 * Level 2 → hidden second responsibility
 * Level 3 → side effect buried in a calculation
 * Level 4 → output + business logic tangled together
 *
 * Rule: if you need "and" to describe what a method does, split it.
 */
class Q1_MethodDoesOneThing {

    // ── Level 1: Obvious — method does 3 things ────────────────────────────────

    // BAD: validates, saves, and sends email in one method
    static void registerUser_BAD(String name, String email) {
        if (name == null || email == null) {
            System.out.println("Invalid input");
            return;
        }
        System.out.println("Saving user: " + name);   // save
        System.out.println("Sending welcome email to: " + email);  // notify
    }

    // GOOD: each step is its own method
    static boolean isValid(String name, String email) { return name != null && email != null; }
    static void save(String name)        { System.out.println("Saving: " + name); }
    static void sendWelcome(String email){ System.out.println("Email: " + email); }

    static void registerUser_GOOD(String name, String email) {
        if (!isValid(name, email)) return;
        save(name);
        sendWelcome(email);
    }

    // ── Level 2: Hidden — prints AND returns ──────────────────────────────────

    // BAD: calculates sum but also prints — caller can't reuse without side effect
    static int sumAndPrint_BAD(int[] nums) {
        int sum = 0;
        for (int n : nums) sum += n;
        System.out.println("Sum is: " + sum);  // side effect hidden in calculation
        return sum;
    }

    // GOOD: calculate only — caller decides whether to print
    static int sum_GOOD(int[] nums) {
        int total = 0;
        for (int n : nums) total += n;
        return total;
    }

    // ── Level 3: Subtle — modifies list while filtering ───────────────────────

    // BAD: filters evens AND removes them from original list
    static List<Integer> filterEvens_BAD(List<Integer> numbers) {
        List<Integer> evens = new ArrayList<>();
        for (Integer n : numbers) {
            if (n % 2 == 0) {
                evens.add(n);
                numbers.remove(n);   // ← hidden mutation of input! ConcurrentModificationException too
            }
        }
        return evens;
    }

    // GOOD: only filters — never touches the original
    static List<Integer> filterEvens_GOOD(List<Integer> numbers) {
        List<Integer> evens = new ArrayList<>();
        for (Integer n : numbers) {
            if (n % 2 == 0) evens.add(n);
        }
        return evens;
    }

    // ── Level 4: Tricky — business logic mixed with formatting ────────────────

    // BAD: calculates discount AND formats the display string
    static String getDiscountedPrice_BAD(double price, String userType) {
        double discount = userType.equals("VIP") ? 0.2 : 0.05;
        double finalPrice = price - (price * discount);
        return String.format("Price for %s: $%.2f (%.0f%% off)", userType, finalPrice, discount * 100);
    }

    // GOOD: calculation and formatting are separate concerns
    static double applyDiscount(double price, String userType) {
        double discount = userType.equals("VIP") ? 0.2 : 0.05;
        return price - (price * discount);
    }

    static String formatPrice(double price, String userType, double originalPrice) {
        double discount = (originalPrice - price) / originalPrice;
        return String.format("Price for %s: $%.2f (%.0f%% off)", userType, price, discount * 100);
    }

    public static void main(String[] args) {
        System.out.println("=== Level 1 ===");
        registerUser_BAD("Alice", "alice@example.com");
        System.out.println("---");
        registerUser_GOOD("Alice", "alice@example.com");

        System.out.println("\n=== Level 2 ===");
        int[] nums = {1, 2, 3, 4, 5};
        sumAndPrint_BAD(nums);                           // prints as side effect
        System.out.println("Sum: " + sum_GOOD(nums));   // caller controls output

        System.out.println("\n=== Level 3 ===");
        List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4, 5));
        List<Integer> evens = filterEvens_GOOD(list);
        System.out.println("Evens: " + evens + ", original: " + list);  // original untouched

        System.out.println("\n=== Level 4 ===");
        double original = 100.0;
        double discounted = applyDiscount(original, "VIP");
        System.out.println(formatPrice(discounted, "VIP", original));
    }
}
