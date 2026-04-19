/**
 * DigitProduct — multiply all digits of a number recursively
 * 1234 → 1 * 2 * 3 * 4 = 24
 */
class DigitProduct {

    static int product(int num) {
        if (num % 10 == num) return num;              // single digit — base case
        return (num % 10) * product(num / 10);        // last digit * product of rest
    }

    public static void main(String[] args) {
        System.out.println("Product of digits of 1234: " + product(1234));  // 24
        System.out.println("Product of digits of 236:  " + product(236));   // 36
    }
}
