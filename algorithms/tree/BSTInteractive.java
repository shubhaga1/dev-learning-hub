import java.util.InputMismatchException;
import java.util.Scanner;

/**
 * BSTInteractive — Build a BST by typing values via keyboard
 *
 * Asks you at each node: add left child? add right child?
 * Then prints the tree inorder (sorted).
 *
 * Good for: understanding how nodes connect, visualising a tree you design.
 *
 * Run: java BSTInteractive
 * Input: integers for values, yes/no for left/right choices
 */
class BSTInteractive {

    Node root;

    class Node {
        int value;
        Node left;
        Node right;

        Node(int value) {
            this.value = value;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        BSTInteractive tree = new BSTInteractive();
        tree.populate(scanner);
        System.out.println("\nTree built. Inorder traversal (sorted):");
        tree.display();
    }

    // Entry point — sets root, then recurses into children
    public void populate(Scanner scanner) {
        System.out.println("Enter root value:");
        root = new Node(readInt(scanner));
        populateNode(root, scanner);
    }

    // Recursively ask for left and right children
    private void populateNode(Node node, Scanner scanner) {
        System.out.println("Add left child for " + node.value + "? (yes/no):");
        if (readBoolean(scanner)) {
            System.out.println("Enter left value:");
            node.left = new Node(readInt(scanner));
            populateNode(node.left, scanner);
        }
        System.out.println("Add right child for " + node.value + "? (yes/no):");
        if (readBoolean(scanner)) {
            System.out.println("Enter right value:");
            node.right = new Node(readInt(scanner));
            populateNode(node.right, scanner);
        }
    }

    // Inorder display — prints sorted since it's a BST
    public void display() {
        display(root, "");
    }

    private void display(Node node, String indent) {
        if (node == null) return;
        display(node.left,  indent + "\t");
        System.out.println(indent + node.value);
        display(node.right, indent + "\t");
    }

    // Safe integer read — retries on invalid input
    private static int readInt(Scanner scanner) {
        while (true) {
            try {
                return scanner.nextInt();
            } catch (InputMismatchException e) {
                System.out.println("Invalid input — enter a number:");
                scanner.nextLine();
            }
        }
    }

    // Safe boolean read — accepts yes/no/true/false/y/n
    private static boolean readBoolean(Scanner scanner) {
        while (true) {
            String input = scanner.next().trim().toLowerCase();
            if (input.equals("true")  || input.equals("yes") || input.equals("y")) return true;
            if (input.equals("false") || input.equals("no")  || input.equals("n")) return false;
            System.out.println("Invalid input — enter yes/no:");
        }
    }
}
