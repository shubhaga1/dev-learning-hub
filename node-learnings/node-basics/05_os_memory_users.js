/**
 * OS Memory & Users — who is on the system, what is using memory
 * Run: node 05_os_memory_users.js
 */

const os   = require('os');
const { execSync } = require('child_process');

// ─── 1. Overall Memory ───────────────────────────────────────────────────────
console.log('=== SYSTEM MEMORY ===');

const totalMem = os.totalmem();
const freeMem  = os.freemem();
const usedMem  = totalMem - freeMem;

function toGB(bytes) { return (bytes / 1024 / 1024 / 1024).toFixed(2) + ' GB'; }
function toMB(bytes) { return (bytes / 1024 / 1024).toFixed(0) + ' MB'; }

console.log('Total:  ', toGB(totalMem));
console.log('Used:   ', toGB(usedMem));
console.log('Free:   ', toGB(freeMem));
console.log('Usage:  ', ((usedMem / totalMem) * 100).toFixed(1) + '%');

// Visual bar
const bar = Math.round((usedMem / totalMem) * 30);
console.log('[' + '█'.repeat(bar) + '░'.repeat(30 - bar) + ']');

// ─── 2. THIS Node process memory ─────────────────────────────────────────────
console.log('\n=== THIS NODE PROCESS (process.memoryUsage()) ===');

const mem = process.memoryUsage();
console.log('rss (total resident):  ', toMB(mem.rss));        // total memory held by process
console.log('heapTotal (allocated): ', toMB(mem.heapTotal));  // V8 heap allocated
console.log('heapUsed (in use):     ', toMB(mem.heapUsed));   // V8 heap actually used
console.log('external (C++ objects):', toMB(mem.external));   // Buffers, native addons

console.log(`
  rss        = everything the process is holding (heap + stack + code)
  heapTotal  = V8 reserved for JS objects
  heapUsed   = how much of that heap is actually used right now
  external   = memory used by C++ objects (like Buffer)
`);

// ─── 3. Top processes by memory (macOS/Linux) ────────────────────────────────
console.log('=== TOP PROCESSES BY MEMORY ===');
try {
    // ps: sort by %MEM descending, show top 10
    const ps = execSync(
        'ps aux --sort=-%mem 2>/dev/null | head -11 || ps aux -m | head -11',
        { encoding: 'utf8' }
    );
    console.log(ps);
} catch {
    // fallback for macOS
    try {
        const ps = execSync(
            "ps aux -m | awk 'NR==1 || NR<=11' | awk '{printf \"%-10s %5s %5s %s\\n\", $1, $3, $4, $11}'",
            { encoding: 'utf8' }
        );
        console.log('USER       %CPU  %MEM  COMMAND');
        console.log(ps);
    } catch (e) {
        console.log('Could not read process list:', e.message);
    }
}

// ─── 4. Users currently logged in ────────────────────────────────────────────
console.log('=== USERS CURRENTLY LOGGED IN ===');
try {
    const who = execSync('who', { encoding: 'utf8' });
    if (who.trim()) {
        console.log(who);
    } else {
        console.log('(no other users logged in)');
    }
} catch (e) {
    console.log('Could not run who:', e.message);
}

// ─── 5. All user accounts on the system ──────────────────────────────────────
console.log('=== ALL USER ACCOUNTS ON THIS MACHINE ===');
try {
    // macOS: dscl . list /Users | grep -v '^_'
    const users = execSync(
        "dscl . list /Users 2>/dev/null | grep -v '^_' || cut -d: -f1 /etc/passwd",
        { encoding: 'utf8' }
    );
    console.log(users.trim());
} catch (e) {
    console.log('Could not list users:', e.message);
}

// ─── 6. Current user info ─────────────────────────────────────────────────────
console.log('=== CURRENT USER (os.userInfo()) ===');
const user = os.userInfo();
console.log('username: ', user.username);
console.log('uid:      ', user.uid);     // user ID (0 = root)
console.log('gid:      ', user.gid);     // group ID
console.log('homedir:  ', user.homedir);
console.log('shell:    ', user.shell);

// ─── 7. CPU info ──────────────────────────────────────────────────────────────
console.log('\n=== CPU ===');
const cpus = os.cpus();
console.log('Model:  ', cpus[0].model);
console.log('Cores:  ', cpus.length);
console.log('Speed:  ', cpus[0].speed, 'MHz');

// CPU usage per core
console.log('\nPer-core times:');
cpus.forEach((cpu, i) => {
    const total  = Object.values(cpu.times).reduce((a, b) => a + b, 0);
    const idle   = cpu.times.idle;
    const used   = ((1 - idle / total) * 100).toFixed(1);
    console.log(`  Core ${i}: ${used}% busy  (user:${cpu.times.user} sys:${cpu.times.sys} idle:${cpu.times.idle})`);
});

// ─── 8. Uptime ────────────────────────────────────────────────────────────────
console.log('\n=== UPTIME ===');
const upSec = os.uptime();
const days  = Math.floor(upSec / 86400);
const hours = Math.floor((upSec % 86400) / 3600);
const mins  = Math.floor((upSec % 3600) / 60);
console.log(`System up: ${days}d ${hours}h ${mins}m`);
console.log(`Node process up: ${(process.uptime()).toFixed(1)}s`);
