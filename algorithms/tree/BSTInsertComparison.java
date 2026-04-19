/**
 * BST with single insert method — to understand why two methods are better
 *
 * Three approaches tried:
 *   1. Caller passes root every time       — works but exposes internals
 *   2. Void recursive (no return)          — broken, tree never builds
 *   3. Iterative (no recursion)            — works but verbose
 */
class BSTInsertComparison {

    Node root;

    class Node {
        int value;
        Node left;
        Node right;

        Node(int value) {
            this.value = value;
        }
    }

    // ── APPROACH 1: Caller passes root — works but ugly ───────────────────────
    // Problem: caller must know about 'root' — internal detail leaked outside
    // bst.insert(5, bst.root) — why should caller care about root?

    public Node insertApproach1(int value, Node node) {
        if (node == null) return new Node(value);
        if (value < node.value) node.left  = insertApproach1(value, node.left);
        if (value > node.value) node.right = insertApproach1(value, node.right);
        return node;
    }

    // ── APPROACH 2: Void recursive — BROKEN ──────────────────────────────────
    // Problem: Java passes object references by value
    // When node==null, you assign a new Node to local variable 'node'
    // but the PARENT's left/right pointer is unchanged — tree never builds

    public void insertApproach2(int value, Node node) {
        if (node == null) {
            node = new Node(value);  // ✗ only changes LOCAL copy of the reference
            return;                  //   parent still points to null
        }
        if (value < node.value) insertApproach2(value, node.left);
        if (value > node.value) insertApproach2(value, node.right);
    }

    // ── APPROACH 3: Iterative — works, single method, no return needed ────────
    // Trade-off: more code, harder to extend (e.g. adding height for AVL)

    public void insertApproach3(int value) {
        if (root == null) {
            root = new Node(value);
            return;
        }
        Node current = root;
        while (true) {
            if (value < current.value) {
                if (current.left == null)  { current.left  = new Node(value); return; }
                current = current.left;
            } else if (value > current.value) {
                if (current.right == null) { current.right = new Node(value); return; }
                current = current.right;
            } else {
                return; // duplicate — ignore
            }
        }
    }

    public static void main(String[] args) {
        int[] values = {5, 3, 7, 1, 4};

        // ── Approach 1 — works, but caller manages root ───────────────────────
        System.out.println("Approach 1 — caller passes root:");
        BSTInsertComparison bst1 = new BSTInsertComparison();
        for (int v : values) {
            bst1.root = bst1.insertApproach1(v, bst1.root);  // caller must do this
        }
        System.out.println("  Root : " + bst1.root.value);           // 5
        System.out.println("  Left : " + bst1.root.left.value);      // 3
        System.out.println("  Right: " + bst1.root.right.value);     // 7

        // ── Approach 2 — void recursive — BROKEN ─────────────────────────────
        System.out.println("\nApproach 2 — void recursive (broken):");
        BSTInsertComparison bst2 = new BSTInsertComparison();
        bst2.root = bst2.new Node(5);         // set root manually first
        bst2.insertApproach2(3, bst2.root);   // tries to insert 3
        bst2.insertApproach2(7, bst2.root);   // tries to insert 7
        System.out.println("  Root : " + bst2.root.value);           // 5
        System.out.println("  Left : " + bst2.root.left);            // null — BROKEN
        System.out.println("  Right: " + bst2.root.right);           // null — BROKEN

        // ── Approach 3 — iterative — works cleanly ────────────────────────────
        System.out.println("\nApproach 3 — iterative (works):");
        BSTInsertComparison bst3 = new BSTInsertComparison();
        for (int v : values) {
            bst3.insertApproach3(v);   // clean — same experience as two-method BST
        }
        System.out.println("  Root : " + bst3.root.value);           // 5
        System.out.println("  Left : " + bst3.root.left.value);      // 3
        System.out.println("  Right: " + bst3.root.right.value);     // 7
    }
}
