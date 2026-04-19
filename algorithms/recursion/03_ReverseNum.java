/**
 * ReverseNum — reverse digits of a number recursively
 * 1234 → 4321
 */
class ReverseNum {

    static int reversed = 0;

    static void reverse(int n) {
        if (n == 0) return;                           // base case
        reversed = reversed * 10 + n % 10;           // append last digit
        reverse(n / 10);                              // recurse on remaining digits
    }

    public static void main(String[] args) {
        int num = 1234;
        reverse(num);                                 // was never called before — bug fixed
        System.out.println("Reversed: " + reversed); // 4321

        // reset for second call
        reversed = 0;
        reverse(5678);
        System.out.println("Reversed: " + reversed); // 8765
    }
}
