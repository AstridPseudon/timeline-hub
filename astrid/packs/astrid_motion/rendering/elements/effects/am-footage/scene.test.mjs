import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createRequire} from 'node:module';
import path from 'node:path';

const [project, root] = process.argv.slice(2);
assert(project && root, 'usage: node scene.test.mjs <private-project> <repo-root>');
const {build} = createRequire(path.join(project, 'package.json'))('esbuild');

const source = `export {default as Footage} from ${JSON.stringify(
  path.join(root, 'astrid/packs/astrid_motion/rendering/elements/effects/am-footage/component.tsx'),
)};`;
const bundle = await build({
  stdin: {contents: source, resolveDir: root},
  bundle: true,
  write: false,
  platform: 'node',
  format: 'esm',
  jsx: 'automatic',
  nodePaths: [path.join(project, 'node_modules')],
  logLevel: 'silent',
});
const {Footage} = await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString('base64')}`);

const basis = {width: 1920, height: 1080, fps: 30, rendererIdentity: 'registered-ssr', fontDigests: {}};
const admitted = {
  file: 'http://127.0.0.1:4321/footage.mp4',
  type: 'video/mp4',
  resolution: '1920x1080',
  fps: 30,
  content_sha256: 'sha256:admitted-footage',
};
const clip = (params = {}, extra = {}) => ({
  id: 'footage',
  track: 'picture',
  clipType: 'am-footage',
  at: 0,
  hold: 1,
  params,
  ...extra,
});
const support = (c, extra = {}) => Footage.prepareSceneCapability({
  clip: c,
  ...basis,
  ...extra,
}).frame(0);

test('registered footage reports real full-frame support from admitted media facts', () => {
  const result = support(clip({}, {asset: 'P'}), {assetEntry: admitted});
  assert.equal(typeof Footage.prepareSceneCapability, 'function');
  assert.deepEqual(result.bounds, {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}});
  assert.equal(result.presence, 'present');
  assert.equal(result.opaqueSupport, 'rect');
});

test('declared transparent inset keeps actual layout bounds and unknown media alpha', () => {
  const result = support(clip({background: 'transparent', inset: {
    x: 1200, y: 600, w: 576, h: 324, shadow: false,
  }}, {asset: 'P'}), {assetEntry: admitted});
  assert.deepEqual(result.bounds, {status: 'known', rect: {x: 1200, y: 600, width: 576, height: 324}});
  assert.equal(result.presence, 'present');
  assert.equal(result.opaqueSupport, 'unknown');
});

test('own-entry-undefined media draws the slot field and invalid legacy layout is not geometry proof', () => {
  const missing = support(clip({}, {asset: 'missing'}), {assetEntry: undefined});
  assert.deepEqual(missing, {
    presence: 'present',
    opaqueSupport: 'rect',
    bounds: {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}},
  });

  const legacy = support(clip({x: 1200, y: 600, scale: 0.3}, {asset: 'P'}), {assetEntry: admitted});
  assert.deepEqual(legacy.bounds, {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}});
});

test('blank slot uses full-field support', () => {
  const result = support(clip());
  assert.deepEqual(result, {
    presence: 'present',
    opaqueSupport: 'rect',
    bounds: {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}},
  });
});

test('unresolved transparent inset remains unknown rather than guessing alpha', () => {
  const result = support(clip({background: 'transparent', inset: {
    x: 1200, y: 600, w: 576, h: 324, shadow: false,
  }}, {asset: 'P'}), {assetEntry: {file: admitted.file, type: admitted.type}});
  assert.deepEqual(result.bounds, {status: 'known', rect: {x: 1200, y: 600, width: 576, height: 324}});
  assert.equal(result.presence, 'present');
  assert.equal(result.opaqueSupport, 'unknown');
});
