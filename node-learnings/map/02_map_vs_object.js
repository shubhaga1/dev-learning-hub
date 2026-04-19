/**
 * Map vs Object — when to use which
 * Run: node 02_map_vs_object.js
 */

// ─── KEY TYPE ────────────────────────────────────────────────────────────────
console.log('=== KEY TYPE ===');

// Object: keys are always strings (or Symbols)
const obj = {};
obj[42] = 'number key';
obj[true] = 'boolean key';
console.log(Object.keys(obj)); // ['42', 'true'] — converted to string!

// Map: keys stay as their actual type
const map = new Map();
map.set(42, 'number key');
map.set(true, 'boolean key');
for (const [k, v] of map) {
    console.log(typeof k, k, '->', v); // number 42 / boolean true
}

// ─── SIZE ────────────────────────────────────────────────────────────────────
console.log('\n=== SIZE ===');
const o = { a: 1, b: 2, c: 3 };
const m = new Map([['a', 1], ['b', 2], ['c', 3]]);

console.log('Object size:', Object.keys(o).length); // must use Object.keys
console.log('Map size:   ', m.size);                // built-in .size

// ─── INSERTION ORDER ─────────────────────────────────────────────────────────
console.log('\n=== INSERTION ORDER ===');
// Both preserve order today, but Map GUARANTEES it
const scores = new Map();
scores.set('Alice', 95);
scores.set('Bob', 80);
scores.set('Charlie', 88);
// always comes out in the order you put it in
for (const [name, score] of scores) {
    console.log(name, score);
}

// ─── PROTOTYPE POLLUTION ─────────────────────────────────────────────────────
console.log('\n=== PROTOTYPE POLLUTION ===');
const config = {};
// Danger: 'constructor', 'toString', '__proto__' are inherited from Object
console.log('constructor' in config); // true  ← inherited, not yours!

const safeConfig = new Map();
console.log(safeConfig.has('constructor')); // false ← Map is clean

// ─── PERFORMANCE ─────────────────────────────────────────────────────────────
console.log('\n=== PERFORMANCE (frequent add/delete) ===');
// Map is optimized for frequent insertions and deletions
// Object is fine for mostly-read data with string keys

const N = 100_000;
console.time('Map insert+delete');
const perf = new Map();
for (let i = 0; i < N; i++) perf.set(i, i);
for (let i = 0; i < N; i++) perf.delete(i);
console.timeEnd('Map insert+delete');

console.time('Object insert+delete');
const perfObj = {};
for (let i = 0; i < N; i++) perfObj[i] = i;
for (let i = 0; i < N; i++) delete perfObj[i];
console.timeEnd('Object insert+delete');

// ─── WHEN TO USE WHAT ────────────────────────────────────────────────────────
console.log(`
SUMMARY — use Map when:
  ✅ Keys are not strings (numbers, objects, booleans)
  ✅ Frequent add/delete operations
  ✅ Need .size without Object.keys()
  ✅ Need to avoid prototype key collisions

Use Object when:
  ✅ Simple config / data shapes (JSON-like)
  ✅ Keys are strings
  ✅ Passing to JSON.stringify (Map doesn't serialize)
  ✅ Destructuring: const { a, b } = obj
`);
