# Node.js Learnings

Hands-on Node.js code — data structures, core concepts, and security POCs.  
Every file runs with just `node filename.js`. No setup needed unless noted.

---

## Folder Structure

```
node-learnings/
├── map/                      JavaScript Map data structure
├── node-basics/              Core Node.js — modules, events, async, file system
└── security-poc/             Real-world security demos (based on April 2025 Anthropic leak article)
    ├── 1_sourcemap_leak/     Source map exposes minified code + secrets
    ├── 2_npm_leak/           npm publish leaks files without .npmignore
    ├── 3_frustration_detector/ Regex-based frustration detection (4 severity levels)
    └── 4_node_vs_express/    Node http module vs Express side-by-side
```

---

## map/

JavaScript `Map` — like an Object, but keys can be any type (numbers, booleans, objects).

| File | Concept |
|---|---|
| `01_map_basics.js` | set, get, has, delete, size, clear, init from array |
| `02_map_vs_object.js` | When to use Map vs Object — key types, size, prototype safety, performance |
| `03_map_iteration.js` | for...of, forEach, keys(), values(), entries(), spread, Map↔Object conversion |
| `04_map_real_world.js` | Frequency counter, memoization cache, group-by, two-sum (O(n)), graph adjacency list |

```bash
node map/01_map_basics.js
node map/02_map_vs_object.js
node map/03_map_iteration.js
node map/04_map_real_world.js
```

**Quick reference:**
```js
const map = new Map();
map.set('key', 'value');           // add
map.get('key');                    // read
map.has('key');                    // → true/false
map.delete('key');                 // remove
map.size;                          // count (NOT .length)

for (const [key, value] of map) { }          // iterate
map.forEach((value, key) => { });            // value first!
Object.fromEntries(map);                     // Map → Object (for JSON)
new Map(Object.entries(obj));               // Object → Map
```

---

## node-basics/

Core Node.js — all built-in modules, zero npm install needed.

| File | Concept |
|---|---|
| `01_modules.js` | require(), built-ins (os, path), `__dirname`/`__filename`, CommonJS vs ESM |
| `02_events.js` | EventEmitter — on, emit, once, off, custom event classes |
| `03_async_patterns.js` | Callbacks → Promises → async/await, Promise.all, Promise.allSettled |
| `04_file_system.js` | Read, write, append, rename, delete, stats, list directory |

```bash
node node-basics/01_modules.js
node node-basics/02_events.js
node node-basics/03_async_patterns.js
node node-basics/04_file_system.js
```

**Key rules:**
```
Async:    Never use fs.readFileSync() inside a running server — blocks all requests
Events:   Always handle the 'error' event or Node crashes on emit
Modules:  require() = CommonJS (default), import = ESM (needs "type":"module" in package.json)
Promise:  Promise.all       → fails fast if ANY reject
          Promise.allSettled → waits for all, reports each result individually
```

---

## security-poc/

POC series inspired by the April 2025 Anthropic source-code leak article.  
Each POC demonstrates a real security mistake developers make.

### 1. Source Map Leak
> `.map` files contain your full original TypeScript source — if served publicly, anyone can read your secrets.

```bash
node security-poc/1_sourcemap_leak/simulate_leak.js
# or run as live server:
node security-poc/1_sourcemap_leak/server.js
# visit http://localhost:3000/bundle.js.map
```

**The lesson:** Add `*.map` to `.gitignore` and never serve them from production.

---

### 2. npm File Leak
> Without `.npmignore`, `npm publish` ships your `.env`, internal configs, and source maps to the public registry.

```bash
node security-poc/2_npm_leak/simulate_npm_leak.js
```

**The lesson:** Always create `.npmignore` before publishing. Block `.env`, `*.map`, `internal/`, `*.test.js`.

---

### 3. Frustration Detector
> Keyword-based regex detects user frustration in real time — 4 severity levels with timestamped log events.

```bash
node security-poc/3_frustration_detector/detector.js
```

**Severity levels:** mild → moderate → high → abandonment  
**The lesson:** Real-time text analysis with regex — same technique used in UX monitoring tools.

---

### 4. Node.js vs Express Syntax
> Side-by-side comparison of the same 5 tasks in raw Node `http` vs Express.

```bash
# Comparison (no install needed)
node security-poc/4_node_vs_express/3_syntax_diff.js

# Live servers
node security-poc/4_node_vs_express/1_node_raw.js      # port 3001
npm install --prefix security-poc/4_node_vs_express
node security-poc/4_node_vs_express/2_express_app.js   # port 3002
```

**The lesson:** Express is just Node's `http` module with cleaner routing, params, middleware, and JSON helpers.

---

## Run everything (no install)

```bash
# Data structures
node map/01_map_basics.js
node map/02_map_vs_object.js
node map/03_map_iteration.js
node map/04_map_real_world.js

# Node core
node node-basics/01_modules.js
node node-basics/02_events.js
node node-basics/03_async_patterns.js
node node-basics/04_file_system.js

# Security POCs
node security-poc/1_sourcemap_leak/simulate_leak.js
node security-poc/2_npm_leak/simulate_npm_leak.js
node security-poc/3_frustration_detector/detector.js
node security-poc/4_node_vs_express/3_syntax_diff.js
```

---

## What's next

- `set/` — JavaScript Set data structure
- `node-basics/` — streams, http module, process & env variables  
- `security-poc/` — JWT misconfiguration, CORS misconfiguration, path traversal
