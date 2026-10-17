// Consumer regression with real BrowserRunner/Connection/pipe parsing. The
// synthetic child and exit events below are unit controls, never a render proof.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {createRequire} = require('node:module');
const {createHash} = require('node:crypto');
const {EventEmitter} = require('node:events');
const {PassThrough} = require('node:stream');
const {test} = require('node:test');

const root = path.resolve(__dirname, '..');
const reference = process.env.ASTRID_TEST_REMOTION_PROJECT || root;
const upstream = process.env.ASTRID_TEST_REMOTION_UPSTREAM_PROJECT || reference;
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'patches/renderer-4.0.509-retained-transport.json')));
const entry = manifest.files.find((item) => item.path === 'dist/browser/BrowserRunner.js');
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');

function boundary(t, {retained = true, protocolError = false} = {}) {
  const original = fs.readFileSync(path.join(upstream, 'node_modules/@remotion/renderer', entry.path), 'utf8');
  assert.equal(hash(original), entry.before_sha256);
  assert.equal(original.split(entry.before).length, 2);
  const source = original.replace(entry.before, entry.after);
  assert.equal(hash(source), entry.after_sha256);
  const dependency = path.join(reference, 'node_modules/@remotion/renderer', entry.path);
  const realRequire = createRequire(dependency);
  const proc = new EventEmitter();
  proc.pid = 12345; // Synthetic unit identity; no OS process is launched.
  proc.stdout = new PassThrough();
  proc.stderr = new PassThrough();
  proc.stdio = [null, proc.stdout, proc.stderr, new PassThrough(), new PassThrough()];
  const owner = new EventEmitter();
  owner.platform = 'darwin';
  owner.env = retained ? {ASTRID_REMOTION_RETAINED_ENDPOINT: 'unit-control'} : {};
  const commands = [], signals = [];
  owner.kill = (...args) => {signals.push(args); throw new Error('unit-signal-barrier');};
  proc.kill = owner.kill;
  let pending = '';
  proc.stdio[3].on('data', (chunk) => {
    pending += chunk.toString();
    let end;
    while ((end = pending.indexOf('\0')) !== -1) {
      const message = JSON.parse(pending.slice(0, end));
      pending = pending.slice(end + 1);
      commands.push(message);
      queueMicrotask(() => proc.stdio[4].write(JSON.stringify(protocolError
        ? {id: message.id, error: {message: 'unit-CDP-close-refused'}}
        : {id: message.id, result: {}}) + '\0'));
    }
  });
  const exports = {};
  const requireBoundary = (id) => {
    if (id === 'node:child_process') return {spawn: () => proc};
    if (id === './NodeWebSocketTransport') return {NodeWebSocketTransport: {
      create: async () => ({send() {}, close() {}})}};
    if (id === '../delete-directory') return {deleteDirectory() {}};
    return realRequire(id);
  };
  vm.runInNewContext(source, {exports, require: requireBoundary, process: owner,
    Buffer, console, setTimeout, clearTimeout}, {filename: dependency});
  t.after(() => {
    owner.removeAllListeners();
    for (const stream of [proc.stdout, proc.stderr, ...proc.stdio.slice(3)]) stream.destroy();
  });
  return {proc, owner, commands, signals, create: () => exports.makeBrowserRunner({
    executablePath: '/unit/selected-browser',
    processArguments: retained ? ['--remote-debugging-pipe'] : [],
    userDataDir: '/unit/private-browser', logLevel: 'error', indent: false, timeout: 0})};
}

test('retained close sends CDP Browser.close once and waits for child exit without signals', async (t) => {
  const control = boundary(t);
  const runner = await control.create();
  const closing = runner.closeProcess();
  assert.equal(runner.closeProcess(), closing);
  let settled = false;
  closing.then(() => {settled = true;});
  await new Promise(setImmediate);
  assert.deepEqual(control.commands.map((x) => x.method), ['Browser.close']);
  assert.equal(settled, false, 'CDP response alone is not process settlement');
  assert.deepEqual(control.signals, []);
  control.proc.emit('exit', 0);
  await closing;
  assert.equal(settled, true);
  control.owner.emit('exit');
  assert.deepEqual(control.signals, []);
  assert.equal(control.owner.listenerCount('exit'), 0);
});

test('retained protocol failure remains a failure and never grants signal authority', async (t) => {
  const control = boundary(t, {protocolError: true});
  const runner = await control.create();
  await assert.rejects(runner.closeProcess(), /unit-CDP-close-refused/);
  assert.deepEqual(control.signals, []);
  control.owner.emit('exit');
  assert.deepEqual(control.signals, []);
  // Host cancellation/graph settlement remains responsible after a failed
  // protocol close; this unit event is not a cleanup/settlement certificate.
  control.proc.emit('exit', 1);
});

test('legacy browser close retains its existing signal path', async (t) => {
  const control = boundary(t, {retained: false});
  // The legacy websocket waits for the real browser's endpoint announcement.
  const creating = control.create();
  control.proc.stderr.write('DevTools listening on ws://127.0.0.1/unit\n');
  const runner = await creating;
  assert.throws(() => runner.closeProcess(), /unit-signal-barrier/);
  assert.deepEqual(control.signals, [[12345, 0]]);
  assert.deepEqual(control.commands, []);
});
