/**
 * BSTIterative — BST using iterative insert (while loop, no recursion)
 *
 * Covers:
 *   - insert(value)       : while loop walks down to find the right spot
 *   - find(value)         : returns true/false
 *   - traversePreOrder    : root → left → right
 *   - traverseInOrder     : left → root → right  (gives sorted output)
 *   - traverseInOrderDesc : right → root → left  (reverse sorted)
 *   - traversePostOrder   : left → right → root
 *
 * Compare with BST.java which uses recursive insert.
 */
class BSTIterative {

    private Node root;

    private class Node {
        int value;
        Node left;
        Node right;

        Node(int value) {
            this.value = value;
        }
    }

    // Insert using while loop — no recursion needed
    public void insert(int value) {
        Node node = new Node(value);
        if (root == null) {
            root = node;
            return;
        }
        Node current = root;
        while (true) {
            if (value < current.value) {
                if (current.left == null) { current.left = node; break; }
                current = current.left;
            } else {
                if (current.right == null) { current.right = node; break; }
                current = current.right;
            }
        }
    }

    // Find — walk left/right based on value comparison
    public boolean find(int value) {
        Node current = root;
        while (current != null) {
            if (value < current.value)      current = current.left;
            else if (value > current.value) current = current.right;
            else                            return true;
        }
        return false;
    }

    // root → left → right
    public void traversePreOrder() {
        System.out.print("PreOrder   : ");
        preOrder(root);
        System.out.println();
    }
    private void preOrder(Node node) {
        if (node == null) return;
        System.out.print(node.value + " ");
        preOrder(node.left);
        preOrder(node.right);
    }

    // left → root → right  ← always gives sorted (ascending) output in BST
    public void traverseInOrder() {
        System.out.print("InOrder    : ");
        inOrder(root);
        System.out.println();
    }
    private void inOrder(Node node) {
        if (node == null) return;
        inOrder(node.left);
        System.out.print(node.value + " ");
        inOrder(node.right);
    }

    // right → root → left  ← sorted descending
    public void traverseInOrderDesc() {
        System.out.print("InOrderDesc: ");
        inOrderDesc(root);
        System.out.println();
    }
    private void inOrderDesc(Node node) {
        if (node == null) return;
        inOrderDesc(node.right);
        System.out.print(node.value + " ");
        inOrderDesc(node.left);
    }

    // left → right → root
    public void traversePostOrder() {
        System.out.print("PostOrder  : ");
        postOrder(root);
        System.out.println();
    }
    private void postOrder(Node node) {
        if (node == null) return;
        postOrder(node.left);
        postOrder(node.right);
        System.out.print(node.value + " ");
    }

    public static void main(String[] args) {
        BSTIterative tree = new BSTIterative();
        for (int v : new int[]{7, 4, 9, 1, 6, 8, 10}) {
            tree.insert(v);
        }

        System.out.println("Tree built with: 7 4 9 1 6 8 10\n");

        tree.traversePreOrder();
        tree.traverseInOrder();
        tree.traverseInOrderDesc();
        tree.traversePostOrder();

        System.out.println("\nFind 8  : " + tree.find(8));
        System.out.println("Find 99 : " + tree.find(99));
    }
}
