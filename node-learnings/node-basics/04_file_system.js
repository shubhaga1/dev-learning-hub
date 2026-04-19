/**
 * Node.js File System — read, write, append, delete
 * Run: node 04_file_system.js
 */

const fs   = require('fs');
const path = require('path');
const fsPromises = require('fs').promises; // promise-based version

const TEMP = path.join(__dirname, 'temp');

async function main() {

    // ─── Setup: create temp dir ───────────────────────────────────────────────
    if (!fs.existsSync(TEMP)) fs.mkdirSync(TEMP);

    // ─── 1. Write a file ─────────────────────────────────────────────────────
    console.log('=== WRITE ===');
    await fsPromises.writeFile(
        path.join(TEMP, 'hello.txt'),
        'Hello, Node.js!\nLine 2\nLine 3\n'
    );
    console.log('File written');

    // ─── 2. Read a file ──────────────────────────────────────────────────────
    console.log('\n=== READ ===');
    const content = await fsPromises.readFile(path.join(TEMP, 'hello.txt'), 'utf8');
    console.log(content);

    // ─── 3. Append to file ───────────────────────────────────────────────────
    console.log('=== APPEND ===');
    await fsPromises.appendFile(path.join(TEMP, 'hello.txt'), 'Line 4 (appended)\n');
    const after = await fsPromises.readFile(path.join(TEMP, 'hello.txt'), 'utf8');
    console.log(after);

    // ─── 4. Check if file exists ──────────────────────────────────────────────
    console.log('=== EXISTS ===');
    try {
        await fsPromises.access(path.join(TEMP, 'hello.txt'));
        console.log('hello.txt exists');
    } catch {
        console.log('hello.txt does not exist');
    }

    // ─── 5. File stats ────────────────────────────────────────────────────────
    console.log('\n=== STATS ===');
    const stats = await fsPromises.stat(path.join(TEMP, 'hello.txt'));
    console.log('Size:     ', stats.size, 'bytes');
    console.log('Is file:  ', stats.isFile());
    console.log('Is dir:   ', stats.isDirectory());
    console.log('Modified: ', stats.mtime);

    // ─── 6. List directory ────────────────────────────────────────────────────
    console.log('\n=== LIST DIR ===');
    await fsPromises.writeFile(path.join(TEMP, 'other.txt'), 'another file');
    const files = await fsPromises.readdir(TEMP);
    console.log('Files in temp/:', files);

    // ─── 7. Rename / move ────────────────────────────────────────────────────
    console.log('\n=== RENAME ===');
    await fsPromises.rename(
        path.join(TEMP, 'other.txt'),
        path.join(TEMP, 'renamed.txt')
    );
    console.log('Renamed other.txt → renamed.txt');
    console.log('Files now:', await fsPromises.readdir(TEMP));

    // ─── 8. Delete file ───────────────────────────────────────────────────────
    console.log('\n=== DELETE ===');
    await fsPromises.unlink(path.join(TEMP, 'hello.txt'));
    await fsPromises.unlink(path.join(TEMP, 'renamed.txt'));
    fs.rmdirSync(TEMP); // remove temp dir
    console.log('Files deleted, temp/ removed');

    // ─── Sync vs Async ────────────────────────────────────────────────────────
    console.log(`
SYNC vs ASYNC:
  fs.readFileSync()   → blocks the thread — ok for startup/scripts
  fs.readFile()       → callback style
  fs.promises.readFile() → async/await — use this in servers

  Rule: NEVER use Sync methods inside a running HTTP server.
  It blocks ALL requests while the file is being read.
    `);
}

main().catch(console.error);
