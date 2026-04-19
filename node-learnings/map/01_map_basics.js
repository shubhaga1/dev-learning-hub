/**
 * Map Basics
 * A Map holds key-value pairs. Unlike Object, keys can be ANY type.
 * Run: node 01_map_basics.js
 */

// ─── Create ──────────────────────────────────────────────────────────────────
const map = new Map();

// set(key, value)
map.set('name', 'Shubham');
map.set('age', 25);
map.set(42, 'number as key');        // number key — Object can't do this cleanly
map.set(true, 'boolean as key');     // boolean key
map.set({ id: 1 }, 'object as key'); // object as key

console.log('--- CREATE ---');
console.log(map);

// ─── Read ────────────────────────────────────────────────────────────────────
console.log('\n--- READ ---');
console.log(map.get('name'));   // 'Shubham'
console.log(map.get(42));       // 'number as key'
console.log(map.get(true));     // 'boolean as key'
console.log(map.get('missing')); // undefined (no error)

// ─── Check ───────────────────────────────────────────────────────────────────
console.log('\n--- HAS ---');
console.log(map.has('name'));   // true
console.log(map.has('email')); // false

// ─── Size ────────────────────────────────────────────────────────────────────
console.log('\n--- SIZE ---');
console.log(map.size); // 5  (use .size not .length)

// ─── Delete ──────────────────────────────────────────────────────────────────
console.log('\n--- DELETE ---');
map.delete('age');
console.log(map.has('age')); // false
console.log(map.size);       // 4

// ─── Clear ───────────────────────────────────────────────────────────────────
const temp = new Map([['a', 1], ['b', 2]]);
temp.clear();
console.log('\nAfter clear:', temp.size); // 0

// ─── Initialize with values ──────────────────────────────────────────────────
console.log('\n--- INIT WITH ARRAY OF PAIRS ---');
const colors = new Map([
    ['red', '#FF0000'],
    ['green', '#00FF00'],
    ['blue', '#0000FF'],
]);
console.log(colors.get('red')); // #FF0000
