import java.util.ArrayList;
import java.util.Stack;

/**
 * Next Smaller Element — for each element find the next smaller to its right.
 * If none exists, answer is -1.
 * Approach: traverse right to left, use stack to track candidates.
 */
class NextSmallerElement {

    static ArrayList<Integer> nextSmaller(ArrayList<Integer> arr, int n) {
        Stack<Integer> stack = new Stack<>();  // was 's' — undefined variable
        stack.push(-1);                        // sentinel for "no smaller element"
        ArrayList<Integer> ans = new ArrayList<>();

        for (int i = n - 1; i >= 0; i--) {
            int curr = arr.get(i);             // ArrayList uses .get(), not arr[i]
            while (stack.peek() >= curr) {     // peek() not top()
                stack.pop();
            }
            ans.add(0, stack.peek());          // insert at front to maintain order
            stack.push(curr);
        }
        return ans;
    }

    public static void main(String[] args) {
        ArrayList<Integer> arr = new ArrayList<>();
        arr.add(5); arr.add(3); arr.add(1); arr.add(4); arr.add(6);

        ArrayList<Integer> result = nextSmaller(arr, arr.size());
        System.out.println("Input:  " + arr);
        System.out.println("Output: " + result);  // [3, 1, -1, -1, -1]
    }
}
