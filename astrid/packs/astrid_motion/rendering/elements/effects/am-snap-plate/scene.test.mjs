import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createRequire} from 'node:module';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
Error.stackTraceLimit = 2;
const [project, root] = process.argv.slice(2);
const require = createRequire(path.join(project, 'package.json'));
const {build} = require('esbuild');
const selectedAssetContext = require('@banodoco/timeline-composition/package.json').version !== '0.0.8';
const {createElement: h} = require('react');
const {renderToStaticMarkup} = require('react-dom/server');
const {Internals} = await import(pathToFileURL(require.resolve('remotion')));
const {querySceneFrame} = await import(pathToFileURL(require.resolve('@banodoco/timeline-composition/evaluation')));
const {DEFAULT_THEME} = await import(pathToFileURL(require.resolve('@banodoco/timeline-composition')));
const effects = path.join(root, 'astrid/packs/astrid_motion/rendering/elements/effects');
const ids = ['am-snap-plate', 'am-footage', 'am-type', 'am-sprite'];
const source = ids.map((id, i) => `export {default as c${i}} from ${JSON.stringify(path.join(effects, id, 'component.tsx'))};`).join('\n');
const result = await build({stdin: {contents: source, resolveDir: root}, bundle: true, write: false,
  platform: 'node', format: 'esm', jsx: 'automatic', nodePaths: [path.join(project, 'node_modules')],
  plugins: [{name: 'installed-packages', setup(builder) {
    builder.onResolve({filter: /^[^./]/}, args => ({path: pathToFileURL(require.resolve(args.path)).href, external: true}));
  }}]});
const components = await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`);
const [Plate, Footage, Type, Sprite] = ids.map((_, i) => components[`c${i}`]);
const basis = {width: 1920, height: 1080, fps: 30};
const clip = (clipType, params = {}, extra = {}) => ({id: 'c', track: 'plate', at: 0, hold: 1, clipType, params, ...extra});
const context = c => ({clip: c, ...basis, rendererIdentity: 'locked-ssr', fontDigests: {Gelasio: 'digest'}});
const support = (Component, c, frame = 0) => Component.prepareSceneCapability(context(c)).frame(frame);
const ssr = (Component, c, frame = 0, assetEntry) => renderToStaticMarkup(
  h(Internals.CompositionManager.Provider, {value: {
    compositions: [{id: 'am', component: Component, defaultProps: {}}],
    canvasContent: {type: 'composition', compositionId: 'am'},
    currentCompositionMetadata: {...basis, durationInFrames: 90, props: {}}, folders: [],
  }}, h(Internals.TimelineContext.Provider, {value: {frame: {am: frame}, playing: false,
    imperativePlaying: {current: false}, rootId: 'am', playbackRate: 1, audioAndVideoTags: {current: []}}},
  h(Internals.CanUseRemotionHooks.Provider, {value: true},
    h(Component, {clip: c, params: c.params, fps: 30, assetEntry})))));
const full = {x: 0, y: 0, width: 1920, height: 1080};

test('snap plate absence and actual background precedence, including transparent CSS', () => {
  for (const params of [{}, {fill: '   '}, {background: '#123456'}, {src: ' '}]) {
    const c = clip('am-snap-plate', params);
    assert.equal(ssr(Plate, c), '');
    assert.equal(support(Plate, c).presence, 'absent');
  }
  for (const frame of [0, 1, 5, 6, 23, 24, 29]) {
    const c = clip('am-snap-plate', {fill: 'paper', enter: 'blockWipe', exitWipe: 'blockWipe'});
    const markup = ssr(Plate, c, frame);
    assert.match(markup, /overflow:hidden;background-color:#F7F4ED/);
    assert.deepEqual(support(Plate, c, frame).bounds.rect, full);
    assert.equal(support(Plate, c, frame).opaqueSupport, 'rect');
  }
  const image = clip('am-snap-plate', {src: '/plate.png', zoom: 2, focus: {x: 160, y: 90}});
  assert.match(ssr(Plate, image), /left:-960px;top:-540px;width:3840px;height:2160px/);
  assert.equal(support(Plate, image).opaqueSupport, 'rect'); // actual default paper behind the image
  for (const background of ['transparent', '#fff8', '#ffffff80', 'rgba(0,0,0,0.5)', 'var(--field)', 'invalid']) {
    assert.equal(support(Plate, clip('am-snap-plate', {fill: 'paper', background})).opaqueSupport, 'unknown');
  }
  assert.equal(support(Plate, clip('am-snap-plate', {}, {asset: 'P'})).presence, 'unknown');
  assert.equal(ssr(Plate, image, 0, {file: ' '}), ''); // selected blank asset suppresses params.src
});

test('footage inset preserves its outer field, actual cover rect and slot card', () => {
  const c = clip('am-footage', {src: '/still.png', sourceSize: '100x100',
    inset: {x: 1200, y: 600, w: 576, h: 324, radius: 0, shadow: false, border: '#123456'}});
  const markup = ssr(Footage, c);
  assert.match(markup, /background:#1F1F1F;overflow:hidden/);
  assert.match(markup, /left:1200px;top:600px;width:576px;height:324px;overflow:hidden;border-radius:0;box-shadow:0 0 0 1px #123456;background:#1F1F1F/);
  assert.match(markup, /left:0;top:-126px;width:576px;height:576px/);
  assert.deepEqual(support(Footage, c).bounds.rect, full);
  assert.equal(support(Footage, c).opaqueSupport, 'rect');
  const isolated = clip('am-footage', {...c.params, background: 'transparent',
    inset: {...c.params.inset, border: undefined}});
  assert.deepEqual(support(Footage, isolated).bounds.rect, {x: 1200, y: 600, width: 576, height: 324});
  assert.equal(support(Footage, isolated).opaqueSupport, 'unknown');
  assert.match(ssr(Footage, isolated), /background:transparent;overflow:hidden/);
  for (const params of [{placeholder: true}, {guides: true}, {inset: {...isolated.params.inset, shadow: true}},
    {inset: {...isolated.params.inset, border: '#123456'}}]) {
    assert.deepEqual(support(Footage, {...isolated, params: {...isolated.params, ...params}}).bounds.rect, full);
  }
  const slot = clip('am-footage', {slot: 'A', spec: 'medium'});
  assert.match(ssr(Footage, slot), /SLOT A/);
  assert.equal(support(Footage, slot).opaqueSupport, 'rect');
  assert.equal(support(Footage, clip('am-footage', {background: 'transparent'})).opaqueSupport, 'unknown');
});

test('type keeps actual reveals/styles and reports unknown font layout', () => {
  assert.equal(ssr(Type, clip('am-type', {text: '  '})), '');
  assert.equal(support(Type, clip('am-type')).presence, 'absent');
  const c = clip('am-type', {text: 'One two.', italicWord: 'two', underlineWord: 'two', x: 320, y: 40, width: 800});
  assert.match(ssr(Type, c, 0), /left:320px;top:40px;width:800px;overflow:hidden/);
  assert.match(ssr(Type, c, 0), /transform:translateY\(100%\)/);
  assert.match(ssr(Type, c, 7), /overflow:hidden/);
  assert.match(ssr(Type, c, 8), /overflow:visible/);
  assert.doesNotMatch(ssr(Type, c, 8), /translateY/);
  assert.match(ssr(Type, c, 6), /font-style:italic;color:#A94714/);
  for (const frame of [0, 1, 2, 6, 8, 29]) {
    const s = support(Type, c, frame);
    assert.equal(s.presence, 'unknown');
    assert.equal(s.opaqueSupport, 'unknown');
    assert.equal(s.bounds.status, 'unknown');
    assert.match(s.bounds.reason, /actual font layout/);
  }
  for (const color of ['transparent', 'rgba(0,0,0,0)', '#00000000']) {
    assert.equal(support(Type, clip('am-type', {text: 'A', color})).presence, 'unknown');
  }
  const typed = clip('am-type', {text: 'AB', reveal: 'type', font: 'label'});
  assert.match(ssr(Type, typed, 1), /opacity:0[^>]*>B/);
  assert.doesNotMatch(ssr(Type, typed, 2), /opacity:0/);
});

test('sprite uses the actual held pose, blink, shadow and outline; media bounds stay unknown', () => {
  assert.equal(ssr(Sprite, clip('am-sprite')), '');
  assert.equal(support(Sprite, clip('am-sprite')).presence, 'absent');
  const c = clip('am-sprite', {src: '/sprite.png', x: 10, y: 20, scale: 6,
    keyframes: [{frame: 2, x: 30, y: 40, flipX: true}], enter: 'stamp', blinkAt: 4,
    shadow: {w: 10, h: 1}, outline: {px: 2, pulse: 2}});
  assert.match(ssr(Sprite, c, 0, {resolution: '16x24'}), /left:60px;top:114px;transform:scale\(6\)/);
  assert.match(ssr(Sprite, c, 0, {resolution: '16x24'}), /width:60px;height:6px;background:#1F1F1F/);
  assert.match(ssr(Sprite, c, 1), /display:none/);
  assert.equal(support(Sprite, c, 1).presence, 'absent');
  assert.match(ssr(Sprite, c, 2), /left:180px;top:240px;transform:scale\(6\)/);
  assert.match(ssr(Sprite, c, 2), /scaleX\(-1\)/);
  assert.match(ssr(Sprite, c, 2), /drop-shadow\(3px 0 0 #ED6B23\)/);
  for (const f of [4, 5]) assert.equal(support(Sprite, c, f).presence, 'absent');
  assert.equal(support(Sprite, c, 6).presence, 'present');
  assert.equal(support(Sprite, c, 6).bounds.status, 'unknown');
  const slide = clip('am-sprite', {src: '/sprite.png', enter: 'slideIn', x: 40});
  for (const [f, left] of [[0, 96], [1, 96], [2, 132], [7, 204], [8, 240]]) {
    assert.match(ssr(Sprite, slide, f), new RegExp(`left:${left}px;top:0;`));
  }
  assert.equal(support(Sprite, clip('am-sprite', {frames: {frameWidth: 16, frameHeight: 24, count: 2, fps: 12}}, {asset: 'P'})).presence, 'unknown');
});

const {loadHostScene} = await import(pathToFileURL(path.join(project, 'native-scene.mjs')));
const prepare = await loadHostScene(project);
const scene = (clips, options = {}) => prepare({timeline: {tracks: [{id: 'plate', kind: 'visual'}], clips},
  theme: DEFAULT_THEME, assets: {assets: {P: {file: '/plate.png', type: 'image', resolution: '320x180'}}}, ...options}, basis, {});

test('ordinary generated host maps expose real support and public half-open coverage', () => {
  const known = scene([clip('am-snap-plate', {fill: 'paper'})]);
  assert.equal(querySceneFrame(known, 0).coverage, 'COVERED');
  assert.equal(querySceneFrame(known, 29).coverage, 'COVERED');
  assert.equal(querySceneFrame(known, 30).coverage, 'GAP');
  assert.equal(querySceneFrame(scene([clip('am-snap-plate')]), 0).layers[0].visible, false);
  assert.equal(querySceneFrame(scene([clip('am-footage', {inset: {x: 1200, y: 600, w: 576, h: 324}})]), 0).coverage, 'COVERED');
  for (const c of [clip('am-type', {text: 'Actual metrics needed'}), clip('am-sprite', {src: '/sprite.png'}),
    clip('am-footage', {background: 'transparent'})]) {
    assert.equal(querySceneFrame(scene([c]), 0).coverage, 'UNKNOWN');
  }
});

test('actual public selected-asset context keeps old omission distinct from selected absence', () => {
  const managed = querySceneFrame(scene([clip('am-snap-plate', {}, {asset: 'P'})]), 0);
  assert.equal(managed.coverage, selectedAssetContext ? 'COVERED' : 'UNKNOWN');
  const missing = querySceneFrame(scene([clip('am-snap-plate', {}, {asset: 'missing'})]), 0);
  assert.equal(missing.layers[0].visible, selectedAssetContext ? false : 'unknown');
  const fallback = querySceneFrame(scene([clip('am-snap-plate', {src: '/fallback.png'}, {asset: 'missing'})]), 0);
  assert.equal(fallback.coverage, selectedAssetContext ? 'COVERED' : 'UNKNOWN');
  const blank = querySceneFrame(scene([clip('am-snap-plate', {src: '/fallback.png'}, {asset: 'P'})],
    {assets: {assets: {P: {file: ' ', resolution: '320x180', type: 'image'}}}}), 0);
  assert.equal(blank.layers[0].visible, selectedAssetContext ? false : 'unknown');
  const missingSprite = querySceneFrame(scene([clip('am-sprite', {}, {asset: 'missing'})]), 0);
  assert.equal(missingSprite.layers[0].visible, selectedAssetContext ? false : 'unknown');
  const inset = querySceneFrame(scene([clip('am-footage', {background: 'transparent',
    inset: {x: 1200, y: 600, w: 576, h: 324, shadow: false}}, {asset: 'P'})]), 0);
  assert.deepEqual(inset.layers[0].bounds.rect, selectedAssetContext
    ? {x: 1200, y: 600, width: 576, height: 324} : full);
  assert.equal(inset.coverage, 'UNKNOWN');
});

test('strip frame bounds use drawn frame dimensions and separate shadow rows, never media alpha', () => {
  const c = clip('am-sprite', {src: '/sheet.png', x: 10, y: 20, scale: 6,
    frames: {frameWidth: 16, frameHeight: 24, count: 2, fps: 12},
    shadow: {groundY: 44, w: 40, h: 1, dx: -20}, outline: {px: 3}});
  assert.match(ssr(Sprite, c), /left:-132px;top:264px;width:240px;height:6px/);
  assert.match(ssr(Sprite, c), /width:16px;height:24px;overflow:hidden/);
  const s = support(Sprite, c);
  assert.deepEqual(s.bounds.rect, {x: -132, y: 120, width: 288, height: 150});
  assert.equal(s.opaqueSupport, 'unknown');
  const layer = querySceneFrame(scene([c]), 0).layers[0];
  assert.deepEqual(layer.bounds, s.bounds);
  assert.equal(layer.opacity, null);
});

test('public remapped speed drives the same stepped sprite visibility clock', () => {
  const c = clip('am-sprite', {src: '/sprite.png', enter: 'stamp'}, {speed: 0.5});
  const prepared = scene([c]);
  for (const [frame, absent] of [[0, false], [1, false], [2, true], [3, true], [4, false]]) {
    const layer = querySceneFrame(prepared, frame).layers[0];
    assert.equal(layer.visible === false, absent);
    assert.match(ssr(Sprite, c, Math.floor(frame * 0.5)), absent ? /display:none/ : /display:block/);
  }
  assert.throws(() => scene([], {timeline: {clips: [], tracks: [], app: {astrid_render_clock: {}}}}), /RenderClockTail/);
});
