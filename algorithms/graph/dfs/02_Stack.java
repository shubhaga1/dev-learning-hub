package dfs;

import java.util.*;

/**
 * DFS 2/4 — ITERATIVE WITH STACK + StackOverflow proof
 *
 * PROBLEM WITH RECURSIVE:
 *   Each recursive call uses the call stack (OS memory).
 *   Default call stack limit ≈ 5,000–10,000 frames.
 *   A skewed tree of 10,000 nodes has depth 10,000 → CRASH.
 *
 * SOLUTION: use an explicit Stack on the heap (much larger memory).
 *   You manually do what recursion does automatically.
 *
 * WHY push RIGHT before LEFT?
 *   Stack = LIFO. Last pushed = first popped.
 *   Push right → push left → left on TOP → left visited first.
 *   Matches left-to-right natural reading order.
 */
class DFSStack {

    static class Node {
        String val;
        Node left, right;
        Node(String val)                        { this.val = val; }
        Node(String val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static void dfsStack(Node root) {
        if (root == null) return;

        Stack<Node> stack = new Stack<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            Node current = stack.pop();            // take from top
            System.out.print(current.val + " ");

            if (current.right != null) stack.push(current.right);  // push right first
            if (current.left  != null) stack.push(current.left);   // push left last → on top
        }
        System.out.println();
    }

    // ── Stack trace so you can SEE push/pop happening ─────────────────────────
    static void dfsStackWithTrace(Node root) {
        if (root == null) return;
        Stack<Node> stack = new Stack<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            Node current = stack.pop();
            System.out.print("pop=" + current.val + "  stack=");

            if (current.right != null) stack.push(current.right);
            if (current.left  != null) stack.push(current.left);

            System.out.println(stackVals(stack));
        }
    }

    static String stackVals(Stack<Node> s) {
        List<String> vals = new ArrayList<>();
        for (Node n : s) vals.add(n.val);
        return vals.toString() + " ← top is last";
    }

    // ── StackOverflow proof ───────────────────────────────────────────────────
    // Skewed tree: every node only has a right child → depth = n
    static Node buildSkewedTree(int depth) {
        Node root = new Node("0");
        Node cur  = root;
        for (int i = 1; i < depth; i++) {
            cur.right = new Node(String.valueOf(i));
            cur = cur.right;
        }
        return root;
    }

    static void dfsRecursive(Node node) {       // same as 01_Recursive.java
        if (node == null) return;
        dfsRecursive(node.right);               // right-skewed → goes 10000 deep
    }

    public static void main(String[] args) {
        Node root = new Node("a",
                        new Node("b", new Node("d"), new Node("e")),
                        new Node("c", null,          new Node("f")));

        System.out.print("Stack DFS: ");
        dfsStack(root);

        System.out.println("\nStack trace:");
        dfsStackWithTrace(root);

        // ── Prove StackOverflow ───────────────────────────────────────────────
        System.out.println("\n── StackOverflow proof ──");
        Node skewed = buildSkewedTree(15_000);   // 15,000 deep skewed tree

        System.out.print("Iterative on 15,000-deep tree: ");
        dfsStack(skewed);                        // ✅ works — heap stack
        System.out.println("done (no crash)");

        System.out.print("Recursive on 15,000-deep tree: ");
        try {
            dfsRecursive(skewed);                // ❌ StackOverflowError
            System.out.println("done");
        } catch (StackOverflowError e) {
            System.out.println("StackOverflowError! call stack limit hit");
        }
    }
}
