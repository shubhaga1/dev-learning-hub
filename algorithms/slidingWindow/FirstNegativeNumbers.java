import java.util.ArrayList;

public class FirstNegativeNumbers {

    public static ArrayList<Integer> findFirstNegativeNumbers(int[] arr, int k) {
        ArrayList<Integer> result = new ArrayList<>(); // ArrayList to store the first negative numbers in each window
        ArrayList<Integer> ans = new ArrayList<>(); // ArrayList to store the final result
        
        int i = 0; // Start of the window
        int j = 0; // End of the window
        
        while (j < arr.length) {
            if (arr[j] < 0) {
                result.add(arr[j]); // Add the negative number to the result
            }
            j++;
            
            if (j - i + 1 >= k) {
                if (!result.isEmpty()){
                    ans.add(result.get(0)); // Add the first negative number to the final result
                }
                i++;
            
                if (!result.isEmpty() && arr[i-1] == result.get(0)) {
                    result.remove(0); // Remove the first negative number from the result if it is the next element in the window
                }
            }
        }
        
        return ans; 
    }

    public static void main(String[] args) {
        int[] arr = {2, -3, 4, -1, -2, 1, 5, -3};
        int k = 3;

        ArrayList<Integer> result = findFirstNegativeNumbers(arr, k);
        System.out.println("First negative numbers in each window:");
        for (int num : result) {
            System.out.print(num + " ");
        }
        // First negative numbers in each window:
            // -3 -3 -1 -1 -2 -3 
    }
}
