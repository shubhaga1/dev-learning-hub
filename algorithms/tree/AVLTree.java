/**
 * AVL TREE — Self-Balancing BST
 *
 * Problem with BST: inserting sorted data → O(n) height (linked list shape)
 * AVL fix: after every insert/delete, rebalance if |left height - right height| > 1
 *
 * Balance factor = height(left) - height(right)
 *   -1, 0, +1  → balanced
 *   +2          → left-heavy  → right rotation (or left-right)
 *   -2          → right-heavy → left rotation (or right-left)
 *
 * Rotations:
 *   LL case (inserted left-left)  → right rotate
 *   RR case (inserted right-right)→ left rotate
 *   LR case (inserted left-right) → left rotate child, then right rotate root
 *   RL case (inserted right-left) → right rotate child, then left rotate root
 *
 * Time: O(log n) insert/delete/search — guaranteed, not average
 */
class AVLTree {

    static class Node {
        int val, height;
        Node left, right;
        Node(int v) { val = v; height = 1; }
    }

    static int height(Node n) { return n == null ? 0 : n.height; }

    static int balanceFactor(Node n) {
        return n == null ? 0 : height(n.left) - height(n.right);
    }

    static void updateHeight(Node n) {
        n.height = 1 + Math.max(height(n.left), height(n.right));
    }

    // LL case: right rotate
    static Node rotateRight(Node y) {
        Node x  = y.left;
        Node T2 = x.right;
        x.right = y;
        y.left  = T2;
        updateHeight(y);
        updateHeight(x);
        return x;  // x is new root
    }

    // RR case: left rotate
    static Node rotateLeft(Node x) {
        Node y  = x.right;
        Node T2 = y.left;
        y.left  = x;
        x.right = T2;
        updateHeight(x);
        updateHeight(y);
        return y;  // y is new root
    }

    static Node insert(Node node, int val) {
        // 1. Normal BST insert
        if (node == null) return new Node(val);
        if (val < node.val) node.left  = insert(node.left,  val);
        else if (val > node.val) node.right = insert(node.right, val);
        else return node;  // duplicates not allowed

        // 2. Update height
        updateHeight(node);

        // 3. Get balance factor and fix if needed
        int bf = balanceFactor(node);

        // LL case
        if (bf > 1 && val < node.left.val)  return rotateRight(node);
        // RR case
        if (bf < -1 && val > node.right.val) return rotateLeft(node);
        // LR case
        if (bf > 1 && val > node.left.val) {
            node.left = rotateLeft(node.left);
            return rotateRight(node);
        }
        // RL case
        if (bf < -1 && val < node.right.val) {
            node.right = rotateRight(node.right);
            return rotateLeft(node);
        }
        return node;
    }

    static void inorder(Node n) {
        if (n == null) return;
        inorder(n.left);
        System.out.print(n.val + "(h=" + n.height + ") ");
        inorder(n.right);
    }

    public static void main(String[] args) {
        System.out.println("Insert 10, 20, 30 into plain BST → degenerates to linked list");
        System.out.println("Insert 10, 20, 30 into AVL → auto-rotates to balanced tree\n");

        Node root = null;
        for (int v : new int[]{10, 20, 30, 40, 50, 25}) {
            root = insert(root, v);
        }

        System.out.print("Inorder (should be sorted): ");
        inorder(root);
        System.out.println("\nRoot: " + root.val + " (balanced tree)");
    }
}
