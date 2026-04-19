// https://leetcode.com/problems/valid-palindrome/description/

class ValidPalindrome {

    static boolean isPalindrome(String s) {
        // keep only alphanumeric chars, lowercase
        StringBuilder sb = new StringBuilder();
        for (char ch : s.toCharArray()) {
            if (Character.isLetterOrDigit(ch)) sb.append(Character.toLowerCase(ch));
        }
        return check(sb.toString(), 0, sb.length() - 1);
    }

    static boolean check(String s, int i, int j) {
        if (i >= j) return true;                      // base case — pointers crossed
        if (s.charAt(i) != s.charAt(j)) return false; // mismatch
        return check(s, i + 1, j - 1);               // recurse inward
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("A man, a plan, a canal: Panama")); // true
        System.out.println(isPalindrome("race a car"));                      // false
        System.out.println(isPalindrome(" "));                               // true
    }
}
