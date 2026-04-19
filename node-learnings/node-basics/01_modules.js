/**
 * Node.js Modules — require vs import
 * Run: node 01_modules.js
 */

// ─── Built-in modules (no install needed) ────────────────────────────────────
const os   = require('os');    // operating system info
const path = require('path');  // file path utilities
const fs   = require('fs');    // file system

// os module
console.log('=== OS MODULE ===');
console.log('Platform:  ', os.platform());   // darwin / linux / win32
console.log('CPU cores: ', os.cpus().length);
console.log('Free mem:  ', (os.freemem() / 1024 / 1024).toFixed(0) + ' MB');
console.log('Home dir:  ', os.homedir());

// path module
console.log('\n=== PATH MODULE ===');
const filePath = '/Users/shubham/projects/app/src/index.js';
console.log('dirname:  ', path.dirname(filePath));   // /Users/shubham/projects/app/src
console.log('basename: ', path.basename(filePath));  // index.js
console.log('extname:  ', path.extname(filePath));   // .js
console.log('join:     ', path.join('src', 'utils', 'helper.js')); // src/utils/helper.js
console.log('resolve:  ', path.resolve('src', 'index.js')); // absolute path

// ─── __dirname and __filename ─────────────────────────────────────────────────
console.log('\n=== __dirname / __filename ===');
console.log('__dirname: ', __dirname);   // directory of THIS file
console.log('__filename:', __filename);  // full path of THIS file

// ─── Module system ───────────────────────────────────────────────────────────
console.log('\n=== MODULE SYSTEM ===');
// CommonJS (default in Node)
//   require()         → load a module
//   module.exports    → what you expose
//   exports.foo = ... → shorthand

// ES Modules (modern, needs "type": "module" in package.json)
//   import fs from 'fs'
//   export function foo() {}

// Mixing them causes errors — stick to one style per project
console.log('module.id:      ', module.id);
console.log('module.filename:', module.filename);
console.log('module.loaded:  ', module.loaded);  // false while executing, true after
