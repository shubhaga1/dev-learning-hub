/**
 * CTCI 1.1 - Is Unique
 * Cracking the Coding Interview, Chapter 1
 *
 * Check if a string has all unique characters. Two approaches shown.
 *
 * Input:  "hello"  → false  (l repeats)
 * Input:  "world"  → true
 *
 * Approach 1: Boolean array — O(n) time, O(1) space (128-char ASCII)
 * Approach 2: Bit vector — O(n) time, O(1) space, uses single int as bitmask
 */
class IsUnique {
    public static void main(String[] args) {
        String s1 = "hello";
        String s2 = "world";
        System.out.println("\"" + s1 + "\" unique (bit vector): " + isUniqueCharsBV(s1)); // false
        System.out.println("\"" + s2 + "\" unique (bit vector): " + isUniqueCharsBV(s2)); // true
        System.out.println("\"" + s1 + "\" unique (bool array): " + isUniqueChars(s1));   // false
        System.out.println("\"" + s2 + "\" unique (bool array): " + isUniqueChars(s2));   // true
    }

    // Bit vector: each bit position represents a character, 1 = seen
    private static boolean isUniqueCharsBV(String inputString) {
        int checker = 0;
        for (int i = 0; i < inputString.length(); i++) {
            int val = inputString.charAt(i);
            if ((checker & (1 << val)) > 0) {
                return false;
            }
            checker = checker | (1 << val);
        }
        return true;
    }

    // Boolean array: index = ASCII value, true = seen
    private static boolean isUniqueChars(String str) {
        if (str.length() > 128) {
            return false;
        }
        boolean[] charSet = new boolean[128];
        for (int i = 0; i < str.length(); i++) {
            int charValue = str.charAt(i);
            if (charSet[charValue]) {
                return false;
            }
            charSet[charValue] = true;
        }
        return true;
    }
}
