/**
 * Map Real-World Use Cases
 * Run: node 04_map_real_world.js
 */

// ─── 1. Frequency Counter (classic interview problem) ────────────────────────
console.log('=== 1. FREQUENCY COUNTER ===');

function wordFrequency(text) {
    const freq = new Map();
    for (const word of text.toLowerCase().split(/\s+/)) {
        freq.set(word, (freq.get(word) || 0) + 1);
    }
    return freq;
}

const freq = wordFrequency('the quick brown fox jumps over the lazy dog the');
// Sort by frequency
const sorted = [...freq.entries()].sort((a, b) => b[1] - a[1]);
sorted.forEach(([word, count]) => console.log(`  ${word}: ${count}`));

// ─── 2. Cache / Memoization ──────────────────────────────────────────────────
console.log('\n=== 2. MEMOIZATION CACHE ===');

function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            console.log(`  cache hit for args: ${key}`);
            return cache.get(key);
        }
        const result = fn(...args);
        cache.set(key, result);
        return result;
    };
}

const expensiveFib = memoize(function fib(n) {
    if (n <= 1) return n;
    return expensiveFib(n - 1) + expensiveFib(n - 2);
});

console.log(expensiveFib(10)); // computed
console.log(expensiveFib(10)); // cache hit

// ─── 3. Group by (like SQL GROUP BY) ─────────────────────────────────────────
console.log('\n=== 3. GROUP BY ===');

const users = [
    { name: 'Alice',   dept: 'Engineering' },
    { name: 'Bob',     dept: 'Marketing' },
    { name: 'Charlie', dept: 'Engineering' },
    { name: 'Diana',   dept: 'Marketing' },
    { name: 'Eve',     dept: 'Engineering' },
];

function groupBy(arr, key) {
    const groups = new Map();
    for (const item of arr) {
        const group = item[key];
        if (!groups.has(group)) groups.set(group, []);
        groups.get(group).push(item.name);
    }
    return groups;
}

const byDept = groupBy(users, 'dept');
for (const [dept, names] of byDept) {
    console.log(`  ${dept}: ${names.join(', ')}`);
}

// ─── 4. Two-Sum (interview classic — O(n) with Map) ──────────────────────────
console.log('\n=== 4. TWO SUM — O(n) ===');

function twoSum(nums, target) {
    const seen = new Map(); // value → index
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return null;
}

console.log(twoSum([2, 7, 11, 15], 9));  // [0, 1]
console.log(twoSum([3, 2, 4], 6));        // [1, 2]

// ─── 5. Adjacency list (graph) ───────────────────────────────────────────────
console.log('\n=== 5. GRAPH ADJACENCY LIST ===');

const graph = new Map();
function addEdge(from, to) {
    if (!graph.has(from)) graph.set(from, []);
    if (!graph.has(to))   graph.set(to, []);
    graph.get(from).push(to);
    graph.get(to).push(from);
}

addEdge('A', 'B');
addEdge('A', 'C');
addEdge('B', 'D');

for (const [node, neighbors] of graph) {
    console.log(`  ${node} → ${neighbors.join(', ')}`);
}
