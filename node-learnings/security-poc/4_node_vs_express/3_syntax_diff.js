/**
 * POC 4c: Side-by-side syntax comparison (no npm install needed)
 *
 * Shows the SAME 4 tasks in Node http vs Express style.
 * Run: node 3_syntax_diff.js
 */

const comparisons = [
    {
        task: "Start a server on port 3000",
        node: `const http = require('http');
const server = http.createServer((req, res) => { /* handler */ });
server.listen(3000);`,
        express: `const express = require('express');
const app = express();
app.listen(3000);`,
    },
    {
        task: "GET /hello → return JSON",
        node: `if (req.method === 'GET' && req.url === '/hello') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message: 'hi' }));
}`,
        express: `app.get('/hello', (req, res) => {
    res.json({ message: 'hi' });
});`,
    },
    {
        task: "URL param  GET /user/:id",
        node: `// manual string split — fragile
const id = req.url.split('/')[2];`,
        express: `// named param — clean and safe
app.get('/user/:id', (req, res) => {
    const { id } = req.params;
});`,
    },
    {
        task: "Read POST JSON body",
        node: `let body = '';
req.on('data', chunk => { body += chunk.toString(); });
req.on('end', () => {
    const data = JSON.parse(body);   // error handling needed too
});`,
        express: `app.use(express.json());          // one middleware line
app.post('/data', (req, res) => {
    const data = req.body;           // already parsed
});`,
    },
    {
        task: "404 Not Found handler",
        node: `// at the END of your if/else chain:
} else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
}`,
        express: `// middleware runs if no route matched:
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});`,
    },
];

// ─── Print comparison ────────────────────────────────────────────────────────
const W = 70;
console.log('='.repeat(W * 2 + 7));
console.log('  Node.js (http module)'.padEnd(W) + ' │  ' + 'Express (framework on top of Node)');
console.log('  Zero dependencies'.padEnd(W) + ' │  ' + 'npm install express');
console.log('='.repeat(W * 2 + 7));

for (const { task, node, express } of comparisons) {
    console.log(`\n📌 Task: ${task}`);
    console.log('-'.repeat(W * 2 + 7));

    const nodeLines    = node.split('\n');
    const expressLines = express.split('\n');
    const maxLen = Math.max(nodeLines.length, expressLines.length);

    for (let i = 0; i < maxLen; i++) {
        const left  = (nodeLines[i]    || '').padEnd(W);
        const right = expressLines[i] || '';
        console.log(`  ${left} │  ${right}`);
    }
}

console.log('\n' + '='.repeat(W * 2 + 7));
console.log('SUMMARY:');
console.log('='.repeat(W * 2 + 7));
console.log('• Node http   = low-level, built-in, verbose — you control everything');
console.log('• Express     = thin wrapper, cleaner API, same Node underneath');
console.log('• Express adds: routing, middleware, params, json helpers');
console.log('• When to use Node http: tiny scripts, zero-dependency CLIs');
console.log('• When to use Express:   any real web server / API');
console.log('• Other frameworks (same idea): Fastify, Koa, Hapi');
