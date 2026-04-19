/**
 * Map Iteration — all the ways to loop over a Map
 * Run: node 03_map_iteration.js
 */

const scores = new Map([
    ['Alice', 95],
    ['Bob',   80],
    ['Charlie', 88],
    ['Diana',   72],
]);

// ─── 1. for...of entries (most common) ───────────────────────────────────────
console.log('--- for...of entries (destructured) ---');
for (const [name, score] of scores) {
    console.log(`${name}: ${score}`);
}

// ─── 2. forEach ──────────────────────────────────────────────────────────────
console.log('\n--- forEach ---');
scores.forEach((value, key) => {           // NOTE: value first, key second!
    console.log(`${key}: ${value}`);
});

// ─── 3. keys() only ──────────────────────────────────────────────────────────
console.log('\n--- keys() ---');
for (const name of scores.keys()) {
    console.log(name);
}

// ─── 4. values() only ────────────────────────────────────────────────────────
console.log('\n--- values() ---');
for (const score of scores.values()) {
    console.log(score);
}

// ─── 5. entries() explicitly ─────────────────────────────────────────────────
console.log('\n--- entries() ---');
for (const entry of scores.entries()) {
    console.log(entry); // [ 'Alice', 95 ]
}

// ─── 6. Spread to array ──────────────────────────────────────────────────────
console.log('\n--- spread to array ---');
const allEntries = [...scores];          // array of [key, value] pairs
const allKeys    = [...scores.keys()];
const allValues  = [...scores.values()];
console.log(allEntries);
console.log(allKeys);
console.log(allValues);

// ─── 7. Convert Map → Object ─────────────────────────────────────────────────
console.log('\n--- Map → Object (for JSON) ---');
const obj = Object.fromEntries(scores);
console.log(obj);
console.log(JSON.stringify(obj)); // Maps don't JSON.stringify directly

// ─── 8. Convert Object → Map ─────────────────────────────────────────────────
console.log('\n--- Object → Map ---');
const data = { x: 10, y: 20, z: 30 };
const mapFromObj = new Map(Object.entries(data));
console.log(mapFromObj);
