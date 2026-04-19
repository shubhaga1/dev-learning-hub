package dfs;

import java.util.*;

/**
 * DFS 1b/4 — RECURSIVE + isVisited
 *
 * Same tree traversal as 01_Recursive.java, but now with an explicit
 * visited set. In a tree this is optional (no cycles), but in a GRAPH
 * the same node can be reached via multiple paths — without visited you'd
 * loop forever.
 *
 * Rule: always mark a node visited BEFORE recursing into its neighbours.
 *       If you mark it AFTER, another path can sneak in and process it twice.
 *
 * Tree used:
 *       a
 *      / \
 *     b   c
 *    / \   \
 *   d   e   f
 *
 * Expected output: a b d e c f  (unchanged — visited doesn't reorder a tree)
 */
class DFSRecursiveWithVisited {

    static class Node {
        String val;
        Node left, right;
        Node(String val)                        { this.val = val; }
        Node(String val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static List<String> dfs(Node node, Set<String> visited) {
        if (node == null) return new ArrayList<>();               // base case: no node
        if (visited.contains(node.val)) return new ArrayList<>(); // already explored — skip

        visited.add(node.val);   // mark BEFORE recursing so no other path re-enters this node

        List<String> result = new ArrayList<>();
        result.add(node.val);                        // 1. record current node

        result.addAll(dfs(node.left, visited));      // 2. recurse left
        result.addAll(dfs(node.right, visited));     // 3. recurse right

        return result;
    }

    public static void main(String[] args) {
        Node root = new Node("a",
                        new Node("b",
                            new Node("d"),
                            new Node("e")),
                        new Node("c",
                            null,
                            new Node("f")));

        // pass a fresh HashSet — one per traversal, not shared across calls
        List<String> result = dfs(root, new HashSet<>());
        System.out.println("DFS result : " + result);   // [a, b, d, e, c, f]
        System.out.println("size       : " + result.size());

        // null root — returns [] not null
        List<String> empty = dfs(null, new HashSet<>());
        System.out.println("null root  : " + empty);    // []
    }
}
