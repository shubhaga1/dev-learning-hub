/**
 * POC 4a: Raw Node.js HTTP Server
 *
 * Node.js has a built-in 'http' module — no npm install needed.
 * This is the LOW-LEVEL way: you handle everything manually.
 *
 * Run: node 1_node_raw.js
 * Test: curl http://localhost:3001/hello
 *       curl http://localhost:3001/user/42
 *       curl http://localhost:3001/unknown
 */

const http = require('http');   // built-in, no install

const server = http.createServer((req, res) => {

    // ❌ No routing built in — you manually check URL and method
    if (req.method === 'GET' && req.url === '/hello') {

        // ❌ Must set headers manually every time
        res.writeHead(200, { 'Content-Type': 'application/json' });

        // ❌ Must JSON.stringify manually
        res.end(JSON.stringify({ message: 'Hello from raw Node!', server: 'http module' }));

    } else if (req.method === 'GET' && req.url.startsWith('/user/')) {

        // ❌ Must parse URL params manually
        const id = req.url.split('/')[2];   // fragile
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ id, source: 'manual URL parsing' }));

    } else if (req.method === 'POST' && req.url === '/data') {

        // ❌ Must manually read body chunks (streaming)
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const parsed = JSON.parse(body);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ received: parsed }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid JSON' }));
            }
        });

    } else {
        // ❌ Must handle 404 manually
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found', url: req.url }));
    }
});

server.listen(3001, () => {
    console.log('\n📦 Raw Node.js http server — port 3001');
    console.log('Built-in module, zero dependencies\n');
    console.log('Test endpoints:');
    console.log('  curl http://localhost:3001/hello');
    console.log('  curl http://localhost:3001/user/42');
    console.log('  curl -X POST http://localhost:3001/data -H "Content-Type: application/json" -d \'{"name":"test"}\'');
    console.log('  curl http://localhost:3001/unknown\n');
});
