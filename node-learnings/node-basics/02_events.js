/**
 * Node.js EventEmitter — the backbone of Node's async model
 * Everything in Node (HTTP, streams, fs) is built on this.
 * Run: node 02_events.js
 */

const EventEmitter = require('events');

// ─── Basic usage ─────────────────────────────────────────────────────────────
console.log('=== BASIC EVENTS ===');

const emitter = new EventEmitter();

// Register listener
emitter.on('greet', (name) => {
    console.log(`Hello, ${name}!`);
});

// Fire the event
emitter.emit('greet', 'Shubham');  // Hello, Shubham!
emitter.emit('greet', 'Alice');    // Hello, Alice!

// ─── once() — fires only one time ────────────────────────────────────────────
console.log('\n=== ONCE ===');

emitter.once('login', (user) => {
    console.log(`${user} logged in`);  // runs once, then removed
});

emitter.emit('login', 'Shubham');  // fires
emitter.emit('login', 'Alice');    // ignored — listener already removed

// ─── Multiple listeners ───────────────────────────────────────────────────────
console.log('\n=== MULTIPLE LISTENERS ===');

emitter.on('data', (chunk) => console.log('Listener 1:', chunk));
emitter.on('data', (chunk) => console.log('Listener 2:', chunk));

emitter.emit('data', 'hello');  // both fire

// ─── Remove listener ─────────────────────────────────────────────────────────
console.log('\n=== REMOVE LISTENER ===');

function onPing() { console.log('pong'); }

emitter.on('ping', onPing);
emitter.emit('ping');         // pong
emitter.off('ping', onPing);  // remove it
emitter.emit('ping');         // nothing

// ─── Custom class extending EventEmitter ─────────────────────────────────────
console.log('\n=== CUSTOM CLASS ===');

class OrderSystem extends EventEmitter {
    placeOrder(item) {
        console.log(`Order placed: ${item}`);
        this.emit('order:placed', { item, time: new Date().toISOString() });
    }

    shipOrder(item) {
        console.log(`Order shipped: ${item}`);
        this.emit('order:shipped', { item });
    }
}

const orders = new OrderSystem();

orders.on('order:placed', (data) => {
    console.log(`  → Email sent for: ${data.item}`);
});

orders.on('order:placed', (data) => {
    console.log(`  → Inventory updated for: ${data.item}`);
});

orders.on('order:shipped', (data) => {
    console.log(`  → Tracking created for: ${data.item}`);
});

orders.placeOrder('MacBook');
orders.shipOrder('MacBook');

// ─── Error events (special) ───────────────────────────────────────────────────
console.log('\n=== ERROR EVENT ===');
// 'error' is special — if no listener, Node crashes with unhandled error

emitter.on('error', (err) => {
    console.log('Handled error:', err.message);
});

emitter.emit('error', new Error('Something went wrong'));
// Without the listener above, this would crash the process
