
/**
 * JavaPassByValueDemo — Why void recursive insert is broken
 *
 * Java passes object references BY VALUE.
 * Assigning to a local parameter does NOT update the caller's variable.
 *
 * Run this to see the difference live.
 */
class JavaPassByValueDemo {

    static class Box {
        int value;
        Box(int v) { this.value = v; }
    }

    // ── BROKEN: void — assignment to local param is lost ─────────────────────
    static void tryAssign(Box b) {
        b = new Box(99);   // only changes local 'b' — caller's variable unchanged
    }

    // ── WORKS: return the new object back to caller ───────────────────────────
    static Box assign(Box b) {
        b = new Box(99);
        return b;          // caller receives the new Box and can use it
    }

    // ── WORKS: mutate the object itself (not the reference) ───────────────────
    static void mutate(Box b) {
        b.value = 99;      // modifies the object b points to — caller sees change
    }

    public static void main(String[] args) {
        Box box;

        // Case 1 — void, reassign param — BROKEN
        box = new Box(1);
        tryAssign(box);
        System.out.println("After tryAssign : " + box.value);  // 1 — unchanged

        // Case 2 — return new object — WORKS
        box = new Box(1);
        box = assign(box);
        System.out.println("After assign    : " + box.value);  // 99 — updated

        // Case 3 — mutate the object — WORKS
        box = new Box(1);
        mutate(box);
        System.out.println("After mutate    : " + box.value);  // 99 — updated
    }
}
