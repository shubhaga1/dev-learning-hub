class BST {

    Node root;
    static final boolean DEBUG = true;   // set false to silence debug output


    public static void main(String[] args) {
        BST bst = new BST();
        System.out.println("=== Inserting: 5 3 7 1 4 6 8 ===");
        for (int v : new int[]{5, 3, 7, 1, 4, 6, 8}) {
            bst.insert(v);
        }
        System.out.println("\nRoot: " + bst.root.value);  // 5
        bst.display();
        System.out.println("\nisTreeBalanced: " + bst.isTreeBalanced());
        System.out.println("\n=== Tree shape (visual) ===");
        bst.printTree(bst.root, "", true);
    }

    public void insert(int value) {
        root = insert(value, root);
    }

    public Node insert(int value, Node node) {
        if (node == null) {
            return new Node(value);
        }


        if (value < node.value) {
            node.left = insert(value, node.left);
        }

        if (value > node.value) {
            node.right = insert(value, node.right);
        }

        node.height = Math.max(height(node.left), height(node.right)) + 1;

        return node;
    }

    public void display() {
        System.out.print("Inorder   : "); inorder(root);   System.out.println();
        System.out.print("Preorder  : "); preorder(root);  System.out.println();
        System.out.print("Postorder : "); postorder(root); System.out.println();
    }

    private void inorder(Node node) {
        if (node == null) return;
        inorder(node.left);
        System.out.print(node.value + " ");
        inorder(node.right);
    }

    private void preorder(Node node) {
        if (node == null) return;
        System.out.print(node.value + " ");
        preorder(node.left);
        preorder(node.right);
    }

    private void postorder(Node node) {
        if (node == null) return;
        postorder(node.left);
        postorder(node.right);
        System.out.print(node.value + " ");
    }

    int height(Node node) {
        if (node == null) return 0;
        return node.height;
    }

    // prints the tree sideways — right branch on top, left on bottom
    void printTree(Node node, String prefix, boolean isRight) {
        if (node == null) return;
        printTree(node.right, prefix + (isRight ? "    " : "│   "), true);
        System.out.println(prefix + (isRight ? "┌── " : "└── ") + node.value + " (h=" + node.height + ")");
        printTree(node.left,  prefix + (isRight ? "│   " : "    "), false);
    }

    public boolean isTreeBalanced(){
        return isTreeBalanced(root);
    }

    public boolean isTreeBalanced(Node node){
        if (node == null) {
            return true;
        }

        return Math.abs((height(node.left))-height(node.right)) <=1 && isTreeBalanced(node.left) && isTreeBalanced(node.right);
    }

    class Node {
        int value;
        Node left;
        Node right;
        int height;

        Node(int value) {
            this.value = value;
        }
    }
}
