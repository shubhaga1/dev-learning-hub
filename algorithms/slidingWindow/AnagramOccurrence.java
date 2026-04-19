import java.util.HashMap;
import java.util.Map;

public class AnagramOccurrence {

    public static boolean isAnagram(String str1, String str2) {
        // Create character count maps for both strings
        Map<Character, Integer> map1 = createCharCountMap(str1);
        Map<Character, Integer> map2 = createCharCountMap(str2);

        // Compare the character count maps
        return map1.equals(map2);
    }

    private static Map<Character, Integer> createCharCountMap(String str) {
        Map<Character, Integer> charCountMap = new HashMap<>();
        for (char ch : str.toCharArray()) {
            charCountMap.put(ch, charCountMap.getOrDefault(ch, 0) + 1);
        }
        return charCountMap;
    }

    public static int countAnagramOccurrences(String mainString, String anagramString) {
        int anagramCount = 0;
        int windowSize = anagramString.length();

        // Check for anagrams in each window
        for (int i = 0; i <= mainString.length() - windowSize; i++) {
            String window = mainString.substring(i, i + windowSize);
            if (isAnagram(window, anagramString)) {
                anagramCount++;
            }
        }

        return anagramCount;
    }

    public static void main(String[] args) {
        String mainString = "cbaebabacd";
        String anagramString = "abc";

        int occurrenceCount = countAnagramOccurrences(mainString, anagramString);
        System.out.println("Anagram occurrences: " + occurrenceCount);
    }
}
