import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * ArrayList — all commonly used methods with examples
 *
 * ArrayList vs Array:
 *   Array     → fixed size, fast access, primitives ok
 *   ArrayList → dynamic size, extra methods, only objects (Integer not int)
 */
class ArrayListMethods {

    public static void main(String[] args) {

        // ── Create ────────────────────────────────────────────────────────────
        ArrayList<Integer> list = new ArrayList<>();               // empty
        ArrayList<Integer> fromList = new ArrayList<>(List.of(1, 2, 3)); // from values
        System.out.println("fromList:        " + fromList);   // [1, 2, 3]

        // ── Add ───────────────────────────────────────────────────────────────
        list.add(10);           // add at end          → [10]
        list.add(20);           //                     → [10, 20]
        list.add(30);           //                     → [10, 20, 30]
        list.add(1, 99);        // add at index 1      → [10, 99, 20, 30]
        System.out.println("After add:       " + list);

        // ── Get / Set ─────────────────────────────────────────────────────────
        System.out.println("get(0):          " + list.get(0));     // 10
        list.set(1, 88);        // replace index 1     → [10, 88, 20, 30]
        System.out.println("After set(1,88): " + list);

        // ── Remove ────────────────────────────────────────────────────────────
        list.remove(0);                    // remove by INDEX     → [88, 20, 30]
        list.remove(Integer.valueOf(20));   // remove by VALUE     → [88, 30]
        System.out.println("After remove:    " + list);

        // ── Search ────────────────────────────────────────────────────────────
        list.add(88);                                              // [88, 30, 88]
        System.out.println("contains(88):    " + list.contains(88));    // true
        System.out.println("indexOf(88):     " + list.indexOf(88));     // 0 (first)
        System.out.println("lastIndexOf(88): " + list.lastIndexOf(88)); // 2 (last)

        // ── Size / Empty ──────────────────────────────────────────────────────
        System.out.println("size():          " + list.size());    // 3
        System.out.println("isEmpty():       " + list.isEmpty()); // false

        // ── Sort ──────────────────────────────────────────────────────────────
        ArrayList<Integer> nums = new ArrayList<>(List.of(5, 2, 8, 1, 9));
        Collections.sort(nums);                                    // ascending
        System.out.println("sorted asc:      " + nums);
        Collections.sort(nums, Collections.reverseOrder());        // descending
        System.out.println("sorted desc:     " + nums);

        // ── Iterate ───────────────────────────────────────────────────────────
        System.out.print("for-each:        ");
        for (int n : nums) System.out.print(n + " ");
        System.out.println();

        System.out.print("forEach lambda:  ");
        nums.forEach(n -> System.out.print(n + " "));
        System.out.println();

        // ── SubList ───────────────────────────────────────────────────────────
        List<Integer> sub = nums.subList(1, 3);  // index 1 inclusive to 3 exclusive
        System.out.println("subList(1,3):    " + sub);

        // ── toArray ───────────────────────────────────────────────────────────
        Integer[] arr = nums.toArray(new Integer[0]); // ArrayList → Array
        System.out.println("toArray:         " + Arrays.toString(arr));

        // ── Array → ArrayList ─────────────────────────────────────────────────
        Integer[] raw = {4, 5, 6};
        ArrayList<Integer> backToList = new ArrayList<>(Arrays.asList(raw));
        System.out.println("asList:          " + backToList);

        // ── addAll / removeAll / retainAll ────────────────────────────────────
        ArrayList<Integer> a = new ArrayList<>(List.of(1, 2, 3, 4));
        ArrayList<Integer> b = new ArrayList<>(List.of(3, 4, 5, 6));
        a.addAll(b);                          // merge b into a
        System.out.println("addAll:          " + a);
        a.removeAll(b);                       // remove all elements that exist in b
        System.out.println("removeAll:       " + a);
        ArrayList<Integer> c = new ArrayList<>(List.of(1, 2, 3, 4));
        c.retainAll(b);                       // keep only elements that exist in b
        System.out.println("retainAll:       " + c);

        // ── Clear ─────────────────────────────────────────────────────────────
        c.clear();
        System.out.println("after clear:     " + c + " isEmpty=" + c.isEmpty());
    }
}
