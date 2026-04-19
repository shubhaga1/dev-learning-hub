import java.util.*;

/**
 * QUEUE ↔ STACK CONVERSIONS
 *
 * Two classic interview problems that test understanding of FIFO vs LIFO.
 *
 * ── Problem A: Queue using 2 Stacks ───────────────────────────────────────
 *
 *   Two stacks: inbox (for push) and outbox (for pop).
 *   Key insight: pushing twice reverses order twice = original order (FIFO).
 *
 *   add(x):    push x onto inbox                              → O(1)
 *   remove():  if outbox empty, drain inbox → outbox first    → O(n) amortized O(1)
 *              then pop from outbox
 *
 *   Dry run — add(1), add(2), add(3), remove(), remove():
 *     inbox: [1,2,3]  outbox: []
 *     remove() → outbox empty → drain: inbox→outbox: [3,2,1]
 *     pop outbox: 1 ✅  (correct FIFO order)
 *     pop outbox: 2 ✅
 *
 * ── Problem B: Stack using 1 Queue ────────────────────────────────────────
 *
 *   On every push, rotate the queue so new element ends up at front.
 *
 *   push(x):   add x, then rotate all previous elements behind it  → O(n)
 *   pop():     remove from front                                    → O(1)
 *
 *   Dry run — push(1), push(2), push(3):
 *     push(1): queue=[1]
 *     push(2): add 2 → [1,2], rotate 1 → [2,1]  ← 2 is now at front (top)
 *     push(3): add 3 → [2,1,3], rotate 2 → [3,2,1]
 *     pop() → 3 ✅ (LIFO)
 */

// ─────────────────────────────────────────────────────────────
// A: Queue using 2 Stacks
// ─────────────────────────────────────────────────────────────
class QueueUsingStacks {

    Stack<Integer> inbox  = new Stack<>();  // all new elements go here
    Stack<Integer> outbox = new Stack<>();  // elements ready to be dequeued

    // O(1) always
    void add(int val) {
        inbox.push(val);
    }

    // O(n) worst case, amortized O(1) — each element moves inbox→outbox exactly once
    int remove() {
        if (outbox.isEmpty()) {
            // drain inbox into outbox — this reverses order (FIFO restored)
            while (!inbox.isEmpty()) outbox.push(inbox.pop());
        }
        if (outbox.isEmpty()) throw new RuntimeException("Queue is empty");
        return outbox.pop();
    }

    int peek() {
        if (outbox.isEmpty()) {
            while (!inbox.isEmpty()) outbox.push(inbox.pop());
        }
        if (outbox.isEmpty()) throw new RuntimeException("Queue is empty");
        return outbox.peek();
    }

    boolean isEmpty() { return inbox.isEmpty() && outbox.isEmpty(); }
}

// ─────────────────────────────────────────────────────────────
// B: Stack using 1 Queue
// ─────────────────────────────────────────────────────────────
class StackUsingQueue {

    Queue<Integer> q = new LinkedList<>();

    // O(n) — rotate all existing elements behind the new one
    void push(int val) {
        q.add(val);
        // rotate: move all elements that were in queue before this push to the back
        int rotations = q.size() - 1;
        for (int i = 0; i < rotations; i++) {
            q.add(q.remove());
        }
        // now: new element is at front (top of stack)
    }

    int pop()  { if (q.isEmpty()) throw new RuntimeException("Stack is empty"); return q.remove(); }
    int peek() { if (q.isEmpty()) throw new RuntimeException("Stack is empty"); return q.peek(); }
    boolean isEmpty() { return q.isEmpty(); }
}

// ─────────────────────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────────────────────
class QueueStackConversions {

    public static void main(String[] args) {

        // ── Test A: Queue using Stacks ────────────────────────────────────
        System.out.println("=== Queue using 2 Stacks ===");
        QueueUsingStacks queue = new QueueUsingStacks();

        queue.add(1); queue.add(2); queue.add(3);
        System.out.println("peek: " + queue.peek());       // 1 (FIFO front)
        System.out.println("remove: " + queue.remove());   // 1
        System.out.println("remove: " + queue.remove());   // 2
        queue.add(4);
        System.out.println("remove: " + queue.remove());   // 3 (not 4 — FIFO preserved)
        System.out.println("remove: " + queue.remove());   // 4

        // ── Test B: Stack using Queue ─────────────────────────────────────
        System.out.println("\n=== Stack using 1 Queue ===");
        StackUsingQueue stack = new StackUsingQueue();

        stack.push(1); stack.push(2); stack.push(3);
        System.out.println("peek: " + stack.peek());      // 3 (LIFO top)
        System.out.println("pop: " + stack.pop());        // 3
        System.out.println("pop: " + stack.pop());        // 2
        stack.push(4);
        System.out.println("pop: " + stack.pop());        // 4 (last pushed = first out)
        System.out.println("pop: " + stack.pop());        // 1
    }
}
