import java.util.Stack;

/**
 * Delete middle element of a stack using recursion.
 * Middle = size/2 index (0-based from bottom)
 */
class DeleteMiddleElementInStack {

    static void deleteMiddle(Stack<Integer> stack, int count, int size) {
        if (count == size / 2) {
            stack.pop();    // remove middle element
            return;
        }
        int num = stack.peek();  // peek() not top() — Java Stack uses peek()
        stack.pop();
        deleteMiddle(stack, count + 1, size);
        stack.push(num);        // restore elements above middle on the way back
    }

    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();
        stack.push(1);
        stack.push(2);
        stack.push(3);
        stack.push(4);
        stack.push(5);

        System.out.println("Original: " + stack);
        deleteMiddle(stack, 0, stack.size());   // pass size before recursion changes it
        System.out.println("After deleting middle: " + stack);  // [1, 2, 4, 5]
    }
}
