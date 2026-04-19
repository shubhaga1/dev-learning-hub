import java.util.LinkedList;
import java.util.Queue;

/**
 * Queue Traversal — how to visit all elements without losing them.
 *
 * Problem: Queue has no index (no q.get(i)).
 * You can only see the FRONT via peek().
 *
 * Trick: snapshot size n BEFORE loop, then for each element:
 *   1. peek()  → read front
 *   2. remove() → take it out
 *   3. add()   → put it back at the rear
 *
 * After n iterations, every element has been seen once
 * and the queue is back to its original order.
 *
 * Dry run: [10, 20, 30, 40, 50]  n=5
 *   i=1: peek=10, remove 10, add 10 → [20,30,40,50,10]
 *   i=2: peek=20, remove 20, add 20 → [30,40,50,10,20]
 *   i=3: peek=30, ...               → [40,50,10,20,30]
 *   i=4: peek=40                    → [50,10,20,30,40]
 *   i=5: peek=50                    → [10,20,30,40,50]  ← original order restored
 *
 * Output: 10 20 30 40 50
 */

class TraversalInQueue {

    public static void main(String[] args) {
        Queue<Integer> q = new LinkedList<>();
        q.add(10); q.add(20); q.add(30); q.add(40); q.add(50);

        System.out.print("Queue traversal: testingg 111");

        int n = q.size();                    // snapshot size BEFORE loop
        for (int i = 1; i <= n; i++) {
            System.out.print(q.peek() + " "); // read front
            q.add(q.remove());               // remove from front, add to rear
        }
        System.out.println();

        System.out.println("Queue after traversal: " + q);  // [10,20,30,40,50] — unchanged
    }
}
