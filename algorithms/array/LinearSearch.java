/**
 * Linear Search — search in array and in String
 *
 * Time: O(n) — checks every element until found
 * Use when: array is unsorted, or small size
 */
class LinearSearchDemo {

    // ── Search in int array ───────────────────────────────────────────────────
    static int searchArray(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i;   // return index when found
        }
        return -1;                            // -1 means not found
    }

    // ── Search in String array ────────────────────────────────────────────────
    static int searchStringArray(String[] arr, String target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i].equals(target)) return i;   // equals() for String, not ==
        }
        return -1;
    }

    // ── Search character in a String ──────────────────────────────────────────
    static int searchInString(String s, char target) {
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == target) return i;  // charAt() to get char at index
        }
        return -1;
    }

    // ── Search substring in a String ──────────────────────────────────────────
    static int searchSubstring(String s, String target) {
        // built-in: s.indexOf(target) does the same thing
        for (int i = 0; i <= s.length() - target.length(); i++) {
            if (s.substring(i, i + target.length()).equals(target)) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] nums = {5, 3, 8, 1, 9, 2};
        System.out.println("Search 8 in array:        index " + searchArray(nums, 8));   // 2
        System.out.println("Search 7 in array:        index " + searchArray(nums, 7));   // -1

        String[] words = {"apple", "banana", "mango", "grape"};
        System.out.println("Search mango in strings:  index " + searchStringArray(words, "mango"));  // 2

        String sentence = "hello world";
        System.out.println("Search 'w' in string:     index " + searchInString(sentence, 'w'));      // 6
        System.out.println("Search 'world' in string: index " + searchSubstring(sentence, "world")); // 6
        System.out.println("Built-in indexOf:         index " + sentence.indexOf("world"));          // 6
    }
}
