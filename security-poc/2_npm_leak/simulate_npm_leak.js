/**
 * POC 2: npm accidental file leak
 *
 * When you run `npm publish`, npm includes ALL files by default.
 * Without .npmignore, sensitive files get published to npmjs.com — publicly.
 *
 * Run: node simulate_npm_leak.js
 */

const fs = require('fs');
const path = require('path');

// Simulate what files npm would publish WITHOUT .npmignore
const allFiles = [
    'index.js',           // ✅ intended
    'package.json',       // ✅ intended
    'README.md',          // ✅ intended
    '.env',               // ❌ LEAKED — API keys, DB passwords
    '.env.production',    // ❌ LEAKED
    'config/secrets.js',  // ❌ LEAKED
    'bundle.js.map',      // ❌ LEAKED — full source code
    'internal/pricing.js',// ❌ LEAKED — business logic
    'tests/',             // ⚠️  unnecessary but not secret
    '.github/',           // ⚠️  unnecessary
];

// What .npmignore should contain to prevent leaks
const npmignoreContent = `
# Secrets — NEVER publish these
.env
.env.*
config/secrets.js
internal/

# Source maps — contain full readable source
*.map

# Dev files — not needed by consumers
tests/
.github/
*.test.js
`;

console.log("=".repeat(60));
console.log("WITHOUT .npmignore — npm publishes EVERYTHING:");
console.log("=".repeat(60));
allFiles.forEach(f => {
    const leaked = ['.env', '.env.production', 'config/secrets.js', 'bundle.js.map', 'internal/pricing.js'];
    const icon = leaked.includes(f) ? '❌ LEAKED' : '✅ ok    ';
    console.log(`  ${icon}  ${f}`);
});

console.log("\n" + "=".repeat(60));
console.log("WITH .npmignore — only safe files published:");
console.log("=".repeat(60));
const safeFiles = ['index.js', 'package.json', 'README.md'];
safeFiles.forEach(f => console.log(`  ✅ ok      ${f}`));

console.log("\n" + "=".repeat(60));
console.log(".npmignore contents (what to always add):");
console.log("=".repeat(60));
console.log(npmignoreContent);

console.log("=".repeat(60));
console.log("Real incident pattern (what happened in the article):");
console.log("=".repeat(60));
console.log("1. Developer runs:  npm publish");
console.log("2. Build output includes:  bundle.js.map  (57MB file)");
console.log("3. No .npmignore → file goes to npmjs.com publicly");
console.log("4. Anyone runs:    npm install your-package");
console.log("5. They get:       node_modules/your-package/bundle.js.map");
console.log("6. They open it:   full TypeScript source code");
console.log("\n✅ Fix: Add *.map to .npmignore before every publish");
