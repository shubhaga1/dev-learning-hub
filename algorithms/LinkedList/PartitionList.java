/*
 * Partition a linked list around value x:
 * all nodes < x come before nodes >= x.
 * Input:  1 -> 4 -> 3 -> 2 -> 5 -> 2,  x=3
 * Output: 1 -> 2 -> 2 -> 3 -> 4 -> 5
 */
class PartitionList {

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public ListNode partition(ListNode head, int x) {
        if (head == null || head.next == null) return head;

        ListNode leftDummy  = new ListNode(-1);
        ListNode rightDummy = new ListNode(-1);
        ListNode leftTail   = leftDummy;
        ListNode rightTail  = rightDummy;

        while (head != null) {
            if (head.val < x) { leftTail.next  = head; leftTail  = leftTail.next; }
            else              { rightTail.next = head; rightTail = rightTail.next; }
            head = head.next;
        }

        rightTail.next  = null;
        leftTail.next   = rightDummy.next;
        return leftDummy.next;
    }

    public static void main(String[] args) {
        ListNode head = new ListNode(1);
        head.next = new ListNode(4);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(2);
        head.next.next.next.next = new ListNode(5);
        head.next.next.next.next.next = new ListNode(2);

        ListNode result = new PartitionList().partition(head, 3);
        while (result != null) { System.out.print(result.val + " "); result = result.next; }
        // 1 2 2 3 4 5
    }
}
