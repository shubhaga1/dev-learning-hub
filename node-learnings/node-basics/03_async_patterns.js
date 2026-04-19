/**
 * Node.js Async Patterns — callbacks → promises → async/await
 * Run: node 03_async_patterns.js
 */

// ─── 1. Callback style (old Node way) ────────────────────────────────────────
console.log('=== 1. CALLBACKS ===');

function fetchUserCallback(id, callback) {
    setTimeout(() => {
        if (id <= 0) return callback(new Error('Invalid ID'));
        callback(null, { id, name: 'Shubham' }); // error-first convention
    }, 100);
}

fetchUserCallback(1, (err, user) => {
    if (err) return console.error('Error:', err.message);
    console.log('Callback result:', user);
});

// Callback hell — deeply nested, hard to read
fetchUserCallback(1, (err, user) => {
    fetchUserCallback(2, (err2, user2) => {
        fetchUserCallback(3, (err3, user3) => {
            console.log('Deeply nested callback hell ↑ avoid this');
        });
    });
});

// ─── 2. Promises ─────────────────────────────────────────────────────────────
console.log('\n=== 2. PROMISES ===');

function fetchUserPromise(id) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (id <= 0) reject(new Error('Invalid ID'));
            else resolve({ id, name: 'Shubham' });
        }, 100);
    });
}

fetchUserPromise(1)
    .then(user => console.log('Promise result:', user))
    .catch(err  => console.error('Promise error:', err.message));

// Chaining — flat instead of nested
fetchUserPromise(1)
    .then(user => fetchUserPromise(user.id + 1)) // chain
    .then(user => fetchUserPromise(user.id + 1)) // chain
    .then(user => console.log('Final chained user:', user))
    .catch(err => console.error(err.message));

// ─── 3. async / await ────────────────────────────────────────────────────────
// async/await is just promises with cleaner syntax — same thing underneath

async function main() {
    console.log('\n=== 3. ASYNC/AWAIT ===');

    // Basic
    const user = await fetchUserPromise(1);
    console.log('Await result:', user);

    // Error handling with try/catch
    try {
        await fetchUserPromise(-1);  // will reject
    } catch (err) {
        console.log('Caught error:', err.message);
    }

    // ─── 4. Parallel vs Sequential ───────────────────────────────────────────
    console.log('\n=== 4. PARALLEL vs SEQUENTIAL ===');

    console.time('sequential');
    const u1 = await fetchUserPromise(1);  // wait 100ms
    const u2 = await fetchUserPromise(2);  // wait another 100ms
    console.timeEnd('sequential');         // ~200ms total

    console.time('parallel');
    const [p1, p2] = await Promise.all([
        fetchUserPromise(1),               // both start at same time
        fetchUserPromise(2),
    ]);
    console.timeEnd('parallel');           // ~100ms total

    console.log('Sequential:', u1, u2);
    console.log('Parallel:  ', p1, p2);

    // ─── 5. Promise.allSettled ───────────────────────────────────────────────
    console.log('\n=== 5. PROMISE.ALLSETTLED ===');
    // Unlike Promise.all, doesn't fail if one rejects
    const results = await Promise.allSettled([
        fetchUserPromise(1),
        fetchUserPromise(-1), // this will reject
        fetchUserPromise(3),
    ]);

    results.forEach(result => {
        if (result.status === 'fulfilled') console.log('✅', result.value);
        else                               console.log('❌', result.reason.message);
    });
}

main();
