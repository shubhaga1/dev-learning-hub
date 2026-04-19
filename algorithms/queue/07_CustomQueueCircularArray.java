/**
 * CUSTOM QUEUE — Circular Array Implementation
 *
 * Problem with naive array queue:
 *   [_, _, _, 10, 20, 30]
 *              ↑front      ↑rear
 *   Front keeps shifting right — wasted space at the beginning never reused.
 *
 * Fix — circular array:
 *   rear wraps around to index 0 when it hits the end.
 *   Use modulo: rear = (rear + 1) % capacity
 *
 * Key insight:
 *   Full vs empty both look like front == rear.
 *   Solution: track size separately.
 *
 * Dry run with capacity=4:
 *   add(10): arr[0]=10  front=0 rear=1 size=1
 *   add(20): arr[1]=20  front=0 rear=2 size=2
 *   add(30): arr[2]=30  front=0 rear=3 size=3
 *   add(40): arr[3]=40  front=0 rear=0 size=4  ← rear wraps to 0
 *   remove(): returns 10, front=1 size=3
 *   add(50): arr[0]=50  front=1 rear=1 size=4  ← fills the freed slot
 */

class CustomQueueCircularArray {

    int[] arr;
    int front;    // index to dequeue from
    int rear;     // index to enqueue to (next empty slot)
    int size;
    int capacity;

    CustomQueueCircularArray(int capacity) {
        this.capacity = capacity;
        arr = new int[capacity];
        front = 0;
        rear = 0;
        size = 0;
    }

    // add O(1) — insert at rear, then advance rear circularly
    void add(int val) {
        if (size == capacity) throw new RuntimeException("Queue is full");
        arr[rear] = val;
        rear = (rear + 1) % capacity;   // wrap around
        size++;
    }

    // remove O(1) — take from front, then advance front circularly
    int remove() {
        if (size == 0) throw new RuntimeException("Queue is empty");
        int val = arr[front];
        front = (front + 1) % capacity;  // wrap around
        size--;
        return val;
    }

    int peek()        { if (size == 0) throw new RuntimeException("Empty"); return arr[front]; }
    int size()        { return size; }
    boolean isFull()  { return size == capacity; }
    boolean isEmpty() { return size == 0; }

    void print() {
        System.out.print("Queue (front→rear): ");
        for (int i = 0; i < size; i++) {
            System.out.print(arr[(front + i) % capacity] + " ");
        }
        System.out.println("[front=" + front + " rear=" + rear + " size=" + size + "]");
    }

    // ── main ─────────────────────────────────────────────────────────────────
    public static void main(String[] args) {
        CustomQueueCircularArray q = new CustomQueueCircularArray(4);

        System.out.println("=== Custom Queue — Circular Array (capacity=4) ===");

        q.add(10); q.add(20); q.add(30); q.add(40);
        q.print();
        // Queue (front→rear): 10 20 30 40 [front=0 rear=0 size=4]  ← rear wrapped

        System.out.println("remove: " + q.remove());   // 10
        System.out.println("remove: " + q.remove());   // 20

        q.add(50);   // fills slot 0 (where 10 was)
        q.add(60);   // fills slot 1 (where 20 was)
        q.print();
        // Queue (front→rear): 30 40 50 60 [front=2 rear=2 size=4]

        // full — adding one more throws
        try {
            q.add(70);
        } catch (RuntimeException e) {
            System.out.println("Caught: " + e.getMessage());  // Queue is full
        }

        // drain
        while (!q.isEmpty()) System.out.print(q.remove() + " ");
        System.out.println("\nDrained. size=" + q.size());
    }
}
