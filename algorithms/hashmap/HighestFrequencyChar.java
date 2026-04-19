import java.util.*;

public class HighestFrequencyChar {
    public static char findHighestFrequencyChar(String str) {
        HashMap<Character, Integer> charFrequencyMap = new HashMap<>();

        // Count the frequency of each character in the string
        for (char ch : str.toCharArray()) {
            if (charFrequencyMap.containsKey(ch)) { 
                charFrequencyMap.put(ch, charFrequencyMap.getOrDefault(ch, 0) + 1);
            } else {
                charFrequencyMap.put(ch, 1); // Added missing semicolon
            }
        }

        char maxFrequencyChar = '\0';

        // Find the character with the highest frequency
        for (Character key : charFrequencyMap.keySet()) {
            if (charFrequencyMap.get(key) > charFrequencyMap.get(maxFrequencyChar)) { 
                maxFrequencyChar = key;
            }
        }
        return maxFrequencyChar;
    }

    public static void main(String[] args) {
        String str = "abbcddddddeee";

        char highestFreqChar = findHighestFrequencyChar(str);

        if (highestFreqChar != '\0') {
            System.out.println("Character with the highest frequency: " + highestFreqChar);
        } else {
            System.out.println("No character found.");
        }
    }
}
