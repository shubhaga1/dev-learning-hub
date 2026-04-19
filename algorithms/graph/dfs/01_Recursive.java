package dfs;

import java.util.*;

/**
 * DFS 1/4 — RECURSIVE (the natural way)
 *
 * DFS = go as deep as possible down one path before backtracking.
 *
 * RECURSIVE works because a tree is itself recursive:
 *   - a node has a left subtree (also a tree)
 *   - a node has a right subtree (also a tree)
 *   → so the function just calls itself on each subtree
 *
 * The call stack IS the stack — OS manages it for you.
 * Each recursive call = going one level deeper.
 * When call returns = backtracking one level up.
 *
 * Tree used:
 *       a
 *      / \
 *     b   c
 *    / \   \
 *   d   e   f
 *
 * Expected output: a b d e c f
 */
class DFSRecursive {

    static class Node {
        String val;
        Node left, right;
        Node(String val)                        { this.val = val; }
        Node(String val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    // returns List — never null, always a collection (empty list if root is null)
    static List<String> dfs(Node node) {
        if (node == null) return new ArrayList<>();  // empty list, not null
        //                       ↑ caller can safely call .size(), forEach() etc.
        //                         null would crash the caller

        List<String> result = new ArrayList<>();
        result.add(node.val);                        // 1. add current node

        result.addAll(dfs(node.left));               // 2. add all left results
        result.addAll(dfs(node.right));              // 3. add all right results

        return result;
        // ← backtrack happens here automatically when method returns
    }

    public static void main(String[] args) {
        Node root = new Node("a",
                        new Node("b",
                            new Node("d"),
                            new Node("e")),
                        new Node("c",
                            null,
                            new Node("f")));

        List<String> result = dfs(root);
        System.out.println("DFS result : " + result);   // [a, b, d, e, c, f]
        System.out.println("size       : " + result.size());

        // null root — returns [] not null
        List<String> empty = dfs(null);
        System.out.println("null root  : " + empty);    // []  ← safe, not crash

        // ── What the call stack looks like ────────────────────────────────────
        System.out.println("""
          Call stack grows DOWN, unwinds UP:

          dfs(a)
            dfs(b)          ← go left from a
              dfs(d)        ← go left from b
                dfs(null)   ← d.left = null → return
                dfs(null)   ← d.right = null → return
              ← back to b   (d done)
              dfs(e)        ← go right from b
                dfs(null)   ← e.left = null → return
                dfs(null)   ← e.right = null → return
              ← back to b   (e done)
            ← back to a     (b fully done)
            dfs(c)          ← go right from a
              dfs(null)     ← c.left = null → return
              dfs(f)        ← go right from c
              ← back to c
            ← back to a
          done

          Output order: a b d e c f
          """);
    }
}
