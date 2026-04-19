/**
 * CUSTOM QUEUE — Linked List Implementation
 *
 * Why build from scratch?
 *   Java's LinkedList/ArrayDeque hide how queues actually work.
 *   Understanding the pointer mechanics matters for interviews.
 *
 * Structure:
 *   head → [10] → [20] → [30] → null   ← tail
 *   add() inserts at tail, remove() takes from head.
 *   Both O(1) — no shifting, no traversal.
 *
 * Edge cases:
 *   - Empty queue: head = tail = null
 *   - Single element: after remove(), both become null
 */

class CustomQueueLinkedList {

    // ── Node ─────────────────────────────────────────────────────────────────
    static class Node {
        int val;
        Node next;
        Node(int val) { this.val = val; }
    }

    // ── Queue internals ───────────────────────────────────────────────────────
    Node head;   // front — dequeue from here
    Node tail;   // rear  — enqueue to here
    int size;

    // add O(1) — insert at tail
    void add(int val) {
        Node node = new Node(val);
        if (tail != null) tail.next = node;
        tail = node;
        if (head == null) head = node;   // first element: head = tail
        size++;
    }

    // remove O(1) — take from head
    int remove() {
        if (head == null) throw new RuntimeException("Queue is empty");
        int val = head.val;
        head = head.next;
        if (head == null) tail = null;   // queue became empty — clear tail too
        size--;
        return val;
    }

    int peek()    { if (head == null) throw new RuntimeException("Empty"); return head.val; }
    int size()    { return size; }
    boolean isEmpty() { return size == 0; }

    // traverse without losing data — peek/remove/add trick
    void print() {
        int n = size;
        System.out.print("Queue: ");
        for (int i = 0; i < n; i++) {
            int val = remove();
            System.out.print(val + " ");
            add(val);                    // put it back at rear
        }
        System.out.println();
    }

    // ── main ─────────────────────────────────────────────────────────────────
    public static void main(String[] args) {
        CustomQueueLinkedList q = new CustomQueueLinkedList();

        System.out.println("=== Custom Queue — Linked List ===");

        q.add(10); q.add(20); q.add(30); q.add(40);
        q.print();                          // Queue: 10 20 30 40

        System.out.println("peek: " + q.peek());        // 10
        System.out.println("remove: " + q.remove());    // 10
        System.out.println("remove: " + q.remove());    // 20
        q.print();                          // Queue: 30 40

        q.add(50);
        q.print();                          // Queue: 30 40 50

        // empty it out
        while (!q.isEmpty()) System.out.print(q.remove() + " ");
        System.out.println("\nSize after draining: " + q.size());

        // edge case — remove from empty
        try {
            q.remove();
        } catch (RuntimeException e) {
            System.out.println("Caught: " + e.getMessage());  // Queue is empty
        }
    }
}
