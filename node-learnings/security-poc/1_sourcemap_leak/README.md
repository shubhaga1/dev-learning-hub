# POC 1: Source Map Leak

## What is a source map?

When you write TypeScript or minified JS, browsers can't read it.
A `.map` file maps the minified code back to original source — used for debugging.

```
bundle.min.js       ← what gets deployed (unreadable)
bundle.min.js.map   ← contains FULL original source code
```

## The Anthropic scenario (April Fools, but the concept is real)

If `bundle.js.map` is accidentally served publicly:
→ Anyone can open Chrome DevTools → Sources → and see your full TypeScript

## How to reproduce this POC

```bash
cd 1_sourcemap_leak
npm install
npm run build          # builds minified JS + leaks the .map file
npm run build:safe     # builds without .map file (production safe)
node server.js         # starts server on port 3000
```

Then open:
- http://localhost:3000/bundle.js        ← minified, unreadable
- http://localhost:3000/bundle.js.map    ← FULL SOURCE exposed!

## The fix

In webpack/esbuild/bun:
```js
// webpack.config.js
devtool: process.env.NODE_ENV === 'production' ? false : 'source-map'
```

Or add to `.gitignore` and never ship `.map` files to production servers.
