import java.util.*;

public class CommonElements {
    public static List<Integer> findCommonElements(int[] arr1, int[] arr2) {
        List<Integer> commonElements = new ArrayList<>();

        // Create a HashMap to store the frequency of elements in arr1
        Map<Integer, Integer> frequencyMap = new HashMap<>();
        for (int num : arr1) {
            frequencyMap.put(num, frequencyMap.getOrDefault(num, 0) + 1);
        }

        // Iterate through arr2 and check if each element is present in the HashMap
        for (int num : arr2) {
            if (frequencyMap.containsKey(num) && frequencyMap.get(num) > 0) {
                commonElements.add(num);
                frequencyMap.put(num, frequencyMap.get(num) - 1);
            }
        }

        return commonElements;
    }

    public static void main(String[] args) {
        int[] arr1 = {2, 4, 6, 8, 10};
        int[] arr2 = {4, 8, 12, 16, 20};

        List<Integer> commonElements = findCommonElements(arr1, arr2);

        if (commonElements.isEmpty()) {
            System.out.println("No common elements found.");
        } else {
            System.out.println("Common elements:");
            for (int num : commonElements) {
                System.out.print(num + " ");
            }
        }
    }
}
