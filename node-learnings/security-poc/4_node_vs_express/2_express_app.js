/**
 * POC 4b: Express.js Server
 *
 * Express is a framework ON TOP of Node's http module.
 * Same functionality as 1_node_raw.js — but far cleaner syntax.
 *
 * Setup: npm install   (installs express from package.json)
 * Run:   node 2_express_app.js
 * Test:  curl http://localhost:3002/hello
 *        curl http://localhost:3002/user/42
 *        curl -X POST http://localhost:3002/data -H "Content-Type: application/json" -d '{"name":"test"}'
 */

const express = require('express');  // npm install express
const app = express();

// ✅ One line: automatically parses JSON request bodies
app.use(express.json());

// ✅ Clean routing — method + path in one line
app.get('/hello', (req, res) => {

    // ✅ res.json() handles Content-Type + JSON.stringify automatically
    res.json({ message: 'Hello from Express!', server: 'express' });
});

// ✅ :id is a named URL parameter — no manual string splitting
app.get('/user/:id', (req, res) => {
    const { id } = req.params;   // ✅ parsed automatically
    res.json({ id, source: 'express params' });
});

// ✅ POST with body — body already parsed by app.use(express.json()) above
app.post('/data', (req, res) => {
    res.json({ received: req.body });  // ✅ no manual streaming needed
});

// ✅ 404 catch-all with middleware
app.use((req, res) => {
    res.status(404).json({ error: 'Not found', url: req.url });
});

app.listen(3002, () => {
    console.log('\n⚡ Express server — port 3002');
    console.log('Requires: npm install (adds express dependency)\n');
    console.log('Test endpoints:');
    console.log('  curl http://localhost:3002/hello');
    console.log('  curl http://localhost:3002/user/42');
    console.log('  curl -X POST http://localhost:3002/data -H "Content-Type: application/json" -d \'{"name":"test"}\'');
    console.log('  curl http://localhost:3002/unknown\n');
});
