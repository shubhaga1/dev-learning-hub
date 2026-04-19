/**
 * Why ArrayList.add() is amortised O(1)
 *
 * ArrayList internally uses a plain array.
 * When it fills up → creates 2x size array → copies all elements → O(n) that time.
 * But this doubling happens rarely — so average cost per add is O(1).
 */
class ArrayListAmortised {

    // Simulate ArrayList internals manually
    static int[] data = new int[2];   // start small — capacity 2
    static int size = 0;

    static void add(int value) {
        if (size == data.length) {
            // Array full — double capacity and copy
            int[] newData = new int[data.length * 2];
            for (int i = 0; i < data.length; i++) {
                newData[i] = data[i];
            }
            System.out.println("  *** RESIZE: " + data.length + " → " + newData.length
                             + " (copied " + size + " elements)");
            data = newData;
        }
        data[size++] = value;
    }

    public static void main(String[] args) {
        System.out.println("Adding 10 elements:\n");

        int totalCopies = 0;

        for (int i = 1; i <= 10; i++) {
            int copiesBefore = totalCopies;
            int oldCap = data.length;

            add(i);

            if (data.length != oldCap) totalCopies += size - 1;  // copies = old size

            System.out.println("add(" + i + ")  size=" + size
                             + "  capacity=" + data.length
                             + "  copies this add=" + (totalCopies - copiesBefore));
        }

        System.out.println("\nTotal copies across 10 adds: " + totalCopies);
        System.out.println("Average copies per add:      " + (double) totalCopies / 10 + " ≈ O(1)");

        System.out.println(
            "\nWhy O(1) amortised:\n" +
            "  Resizes happen at size: 2, 4, 8, 16, 32... (powers of 2)\n" +
            "  Copies at each resize:  2, 4, 8, 16...\n" +
            "  Total copies for n adds ≈ 2n  →  2n/n = 2 = O(1) per add\n" +
            "  Each resize doubles capacity so the next resize is far away.\n" +
            "  The rare O(n) resize is spread (amortised) across all cheap O(1) adds."
        );
    }
}
