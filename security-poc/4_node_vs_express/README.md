# Node.js vs Express — POC

## The one-line answer

```
Node.js http  =  engine (like a car engine)
Express       =  the full car built on that engine
```

Express is just a library that wraps Node's built-in `http` module to make it easier to use.  
**It is still Node.js underneath.**

---

## Run the POC

```bash
# No install needed — pure Node.js comparison
node 3_syntax_diff.js

# Live Node.js server (no npm install)
node 1_node_raw.js
# → visit http://localhost:3001/hello

# Live Express server (needs npm install first)
npm install
node 2_express_app.js
# → visit http://localhost:3002/hello
```

---

## Side-by-side: same task, different syntax

### 1. Start a server

| Node.js (http) | Express |
|---|---|
| `http.createServer(handler)` | `express()` → `app.listen()` |
| 3 lines | 2 lines |

```js
// Node
const http = require('http');
const server = http.createServer((req, res) => { /* ... */ });
server.listen(3000);

// Express
const express = require('express');
const app = express();
app.listen(3000);
```

---

### 2. GET route returning JSON

```js
// ❌ Node — verbose
if (req.method === 'GET' && req.url === '/hello') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message: 'hi' }));
}

// ✅ Express — clean
app.get('/hello', (req, res) => {
    res.json({ message: 'hi' });    // handles headers + stringify
});
```

---

### 3. URL parameters  `/user/:id`

```js
// ❌ Node — manual, fragile string splitting
const id = req.url.split('/')[2];

// ✅ Express — named params
app.get('/user/:id', (req, res) => {
    const { id } = req.params;      // parsed automatically
});
```

---

### 4. Read POST body (JSON)

```js
// ❌ Node — stream chunks manually
let body = '';
req.on('data', chunk => { body += chunk.toString(); });
req.on('end', () => {
    const data = JSON.parse(body);  // must also catch parse errors
});

// ✅ Express — one middleware line
app.use(express.json());
app.post('/data', (req, res) => {
    const data = req.body;          // already parsed
});
```

---

### 5. 404 Not Found

```js
// ❌ Node — must be at end of if/else chain
} else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
}

// ✅ Express — middleware catches anything unmatched
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});
```

---

## When to use what

| Use Node `http` | Use Express |
|---|---|
| Tiny scripts, CLIs | Any real web server or API |
| Zero dependencies required | Need routing, middleware, params |
| Learning how HTTP works | Building something fast |
| Proxy / tunnel (performance critical) | REST APIs, web apps |

---

## Key concepts Express adds over raw Node

| Feature | Node http | Express |
|---|---|---|
| Routing | Manual if/else | `app.get()`, `app.post()` |
| URL params | `split('/')` hacks | `req.params.id` |
| JSON response | `writeHead` + `JSON.stringify` + `res.end` | `res.json()` |
| JSON body parsing | Manual chunk streaming | `express.json()` middleware |
| Status codes | `res.writeHead(404, ...)` | `res.status(404).json(...)` |
| 404 handler | End of if/else | `app.use()` catch-all |
| Middleware | DIY | `app.use()` pipeline |

---

## Files in this folder

| File | Purpose |
|---|---|
| `1_node_raw.js` | Server using Node's built-in http — no npm install |
| `2_express_app.js` | Same server in Express — run `npm install` first |
| `3_syntax_diff.js` | Side-by-side printed comparison — no install needed |
| `package.json` | Declares `express` dependency |
