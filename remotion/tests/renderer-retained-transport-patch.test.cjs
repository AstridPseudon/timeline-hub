const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {createHash} = require('node:crypto');
const {test} = require('node:test');

const root = path.resolve(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'patches/renderer-4.0.509-retained-transport.json')));
const reference = process.env.ASTRID_TEST_REMOTION_PROJECT || root;
const application = import(pathToFileURL(path.join(root, 'scripts/apply-renderer-retained-transport-patch.mjs')).href);
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
function fixture(t) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'astrid-transport-patch-'));
  t.after(() => fs.rmSync(temporary, {recursive: true, force: true}));
  const renderer = path.join(temporary, 'node_modules/@remotion/renderer');
  fs.mkdirSync(renderer, {recursive: true});
  fs.writeFileSync(path.join(renderer, 'package.json'), JSON.stringify({name: manifest.package, version: manifest.version}));
  for (const entry of manifest.files) {
    let bytes = fs.readFileSync(path.join(reference, 'node_modules/@remotion/renderer', entry.path), 'utf8');
    if (hash(bytes) === entry.after_sha256) bytes = bytes.replace(entry.after, entry.before);
    assert.equal(hash(bytes), entry.before_sha256);
    const filename = path.join(renderer, entry.path);
    fs.mkdirSync(path.dirname(filename), {recursive: true});
    fs.writeFileSync(filename, bytes);
  }
  return {temporary, renderer};
}
test('exact transport patch applies and replays without writes', async (t) => {
  const {temporary, renderer} = fixture(t);
  const {applyRendererRetainedTransportPatch: apply} = await application;
  assert.equal(apply(temporary).patchedFiles, manifest.files.length);
  const before = manifest.files.map((entry) => fs.statSync(path.join(renderer, entry.path)).mtimeMs);
  for (const entry of manifest.files) assert.equal(hash(fs.readFileSync(path.join(renderer, entry.path))), entry.after_sha256);
  assert.equal(apply(temporary).patchedFiles, 0);
  assert.deepEqual(manifest.files.map((entry) => fs.statSync(path.join(renderer, entry.path)).mtimeMs), before);
});
test('drift refuses before any package file changes', async (t) => {
  const {temporary, renderer} = fixture(t);
  const {applyRendererRetainedTransportPatch: apply} = await application;
  const last = path.join(renderer, manifest.files.at(-1).path);
  fs.appendFileSync(last, '\n// unrelated drift\n');
  assert.throws(() => apply(temporary), /Unexpected upstream content/);
  for (const entry of manifest.files.slice(0, -1)) assert.equal(hash(fs.readFileSync(path.join(renderer, entry.path))), entry.before_sha256);
});
test('wrong package version refuses before mutation', async (t) => {
  const {temporary, renderer} = fixture(t);
  const {applyRendererRetainedTransportPatch: apply} = await application;
  fs.writeFileSync(path.join(renderer, 'package.json'), JSON.stringify({name: manifest.package, version: '4.0.508'}));
  assert.throws(() => apply(temporary), /requires/);
  for (const entry of manifest.files) assert.equal(hash(fs.readFileSync(path.join(renderer, entry.path))), entry.before_sha256);
});
test('actual dependency rejects retained metadata before compositor setup', async () => {
  const {serveStatic} = require(path.join(reference, 'node_modules/@remotion/renderer/dist/serve-static.js'));
  const previous = process.env.ASTRID_REMOTION_RETAINED_ENDPOINT;
  try {
    // Invalid cache options also refuse before compositor birth. The retained
    // guard must precede that setup entirely, including its option validation.
    process.env.ASTRID_REMOTION_RETAINED_ENDPOINT = JSON.stringify({fd: 1, host: '127.0.0.1', port: 42, binding: '1'.repeat(64)});
    await assert.rejects(serveStatic(null, {port: 42, offthreadVideoCacheSizeInBytes: -1}), /Invalid retained renderer endpoint/);
    process.env.ASTRID_REMOTION_RETAINED_ENDPOINT = JSON.stringify({fd: 0, host: '127.0.0.1', port: 43, binding: '1'.repeat(64)});
    await assert.rejects(serveStatic(null, {port: 42, offthreadVideoCacheSizeInBytes: -1}), /Retained renderer port differs/);
    process.env.ASTRID_REMOTION_RETAINED_ENDPOINT = '{';
    await assert.rejects(serveStatic(null, {port: 42, offthreadVideoCacheSizeInBytes: -1}), SyntaxError);
  } finally {
    if (previous === undefined) delete process.env.ASTRID_REMOTION_RETAINED_ENDPOINT;
    else process.env.ASTRID_REMOTION_RETAINED_ENDPOINT = previous;
  }
});
