import java.util.Stack;

/**
 * Valid Parentheses — check if brackets are correctly matched and nested.
 * Approach: push opening brackets, pop and match on closing brackets.
 */
class ValidParentheses {

    static boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();

        for (char c : s.toCharArray()) {          // c not ch — loop variable is c
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else {
                if (stack.empty()) return false;
                char top = stack.peek();           // peek() not top()
                if ((c == ')' && top == '(') ||
                    (c == '}' && top == '{') ||
                    (c == ']' && top == '[')) {
                    stack.pop();                   // pop from stack, not s.pop()
                } else {
                    return false;
                }
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println("()[]{}  valid: " + isValid("()[]{}"));   // true
        System.out.println("([)]    valid: " + isValid("([)]"));      // false
        System.out.println("{[()]}  valid: " + isValid("{[()]}"));    // true
    }
}
