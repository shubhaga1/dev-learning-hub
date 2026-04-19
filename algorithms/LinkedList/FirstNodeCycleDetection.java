/*
 * Floyd's cycle detection — find the NODE where cycle starts.
 * After slow/fast meet at meetingPoint:
 *   reset slow to head, keep fast at meetingPoint,
 *   move both one step at a time → they meet at cycle start.
 */
class FirstNodeCycleDetection {

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public static ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) return null;

        ListNode slow = head;
        ListNode fast = head;
        boolean hasCycle = false;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) { hasCycle = true; break; }
        }

        if (!hasCycle) return null;

        slow = head; // reset slow to head
        while (slow != fast) {
            slow = slow.next;
            fast = fast.next;
        }
        return slow; // cycle start node
    }

    public static void main(String[] args) {
        ListNode head = new ListNode(3);
        head.next = new ListNode(2);
        head.next.next = new ListNode(0);
        head.next.next.next = new ListNode(-4);
        head.next.next.next.next = head.next; // cycle starts at node(2)

        ListNode cycleNode = detectCycle(head);
        System.out.println("Cycle starts at: " + (cycleNode != null ? cycleNode.val : "none")); // 2
    }
}
