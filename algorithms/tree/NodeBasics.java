/**
 * NodeBasics — What is a Node?
 *
 * A Node is the building block of every tree.
 * Each node holds a value and pointers to left and right children.
 *
 * Visual:
 *         10          ← root node
 *        /  \
 *       5    15       ← child nodes
 *      / \
 *     3   7           ← leaf nodes (no children)
 *
 * Rule in BST:
 *   left child  < parent
 *   right child > parent
 */
class NodeBasics {

    // static = Node does NOT need an outer NodeBasics instance to exist
    // Without static: new NodeBasics().new Node(10)  ← ugly, broken in main()
    // With static:    new Node(10)                   ← clean
    static class Node {

        int value;   // data this node holds
        Node left;   // pointer to left child  (null = no child)
        Node right;  // pointer to right child (null = no child)

        Node(int val) {
            this.value = val;
            // left and right are null by default — no need to set them
        }

        // toString() is called automatically when you print an object
        // Without it: prints NodeBasics$Node@7852e922  (memory address, useless)
        // With it:    prints Node(10)                  (readable)
        @Override
        public String toString() {
            return "Node(" + value + ")";
        }
    }

    public static void main(String[] args) {

        // Build the tree manually
        Node root        = new Node(10);
        root.left        = new Node(5);
        root.right       = new Node(15);
        root.left.left   = new Node(3);
        root.left.right  = new Node(7);

        System.out.println("Root            : " + root);
        System.out.println("Left child      : " + root.left);
        System.out.println("Right child     : " + root.right);
        System.out.println("Left → Left     : " + root.left.left);
        System.out.println("Left → Right    : " + root.left.right);
        System.out.println("Right has left? : " + (root.right.left == null ? "no — leaf node" : root.right.left));

        // BST property check
        System.out.println("\nBST property:");
        System.out.println("  root.left  < root : " + root.left.value  + " < " + root.value + " = " + (root.left.value  < root.value));
        System.out.println("  root.right > root : " + root.right.value + " > " + root.value + " = " + (root.right.value > root.value));
    }
}
