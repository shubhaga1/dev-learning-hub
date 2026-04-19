/**
 * Simple server that accidentally serves .map files publicly
 * This is what happened in the Anthropic April Fools scenario
 *
 * Run: node server.js
 * Then visit:
 *   http://localhost:3000/bundle.js      ← minified (unreadable)
 *   http://localhost:3000/bundle.js.map  ← FULL SOURCE exposed!
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const server = http.createServer((req, res) => {
    const filePath = path.join(__dirname, 'dist', req.url === '/' ? 'index.html' : req.url);

    fs.readFile(filePath, (err, data) => {
        if (err) {
            // Serve a helpful index
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(`
                <h2>Source Map Leak POC</h2>
                <p>Try these URLs to see the attack:</p>
                <ul>
                    <li><a href="/bundle.js">/bundle.js</a> — minified (unreadable)</li>
                    <li><a href="/bundle.js.map">/bundle.js.map</a> — ⚠️ FULL SOURCE EXPOSED</li>
                </ul>
                <p>In production, the .map file should never be served publicly.</p>
            `);
            return;
        }

        const ext = path.extname(filePath);
        const contentType = ext === '.map' ? 'application/json' : 'application/javascript';
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(data);
    });
});

server.listen(PORT, () => {
    console.log(`\nServer running at http://localhost:${PORT}`);
    console.log('\nTry:');
    console.log(`  http://localhost:${PORT}/bundle.js      ← minified`);
    console.log(`  http://localhost:${PORT}/bundle.js.map  ← FULL SOURCE LEAKED\n`);
});
