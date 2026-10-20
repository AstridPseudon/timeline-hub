// Actual discovered AM presenter through the native host and registered SSR.
// These inspect markup and declared regions, never decoded pixels or lip-sync statistics.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {build} from 'esbuild';
import {createElement as h} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';
import {DEFAULT_THEME, TimelineComposition, compileCanonicalTransitions, toRuntimeTheme, prepareCompositionScene, getTimelineDurationInFrames} from '@banodoco/timeline-composition';
import {querySceneFrame} from '@banodoco/timeline-composition/evaluation';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';
import {foldSceneMotion, loadHostScene} from './native-scene.mjs';

Error.stackTraceLimit = 0;
const project = process.cwd();
const presenter = '../astrid/packs/astrid_motion/rendering/elements/effects/am-presenter';
const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
const bundle = await build({stdin: {contents: `
export {resolveHostRegistries} from './src/host-registries';
export * from '${presenter}/motion';
export * from '${presenter}/presenter-core';
export {default as Presenter} from '${presenter}/component';`, resolveDir: project},
bundle: true, write: false, platform: 'node', format: 'esm', jsx: 'automatic',
nodePaths: [path.join(project, 'node_modules')], logLevel: 'silent',
plugins: [{name: 'renderer-aliases', setup(builder) {
  builder.onResolve({filter: /^[^./]/}, async args => {
    if (args.pluginData?.resolvingPackage) return;
    const alias = Object.keys(aliases).find(key => args.path === key || args.path.startsWith(`${key}/`));
    if (alias) return builder.resolve(path.join(aliases[alias], args.path.slice(alias.length).split('?')[0]),
      {kind: args.kind, resolveDir: project});
    const resolved = await builder.resolve(args.path, {kind: args.kind, resolveDir: args.resolveDir,
      pluginData: {resolvingPackage: true}});
    if (resolved.errors.length) return {errors: resolved.errors};
    return {path: path.isAbsolute(resolved.path) ? pathToFileURL(resolved.path).href : resolved.path, external: true};
  });
}}]});
const source = await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString('base64')}`);
const prepareHostScene = await loadHostScene(project);
const basis = {width: 1920, height: 1080, fps: 30};
const theme = DEFAULT_THEME;
const runtimeTheme = toRuntimeTheme(theme);
const registries = source.resolveHostRegistries(runtimeTheme);
const owner = {kind: 'effect', id: 'am-presenter', packId: 'astrid_motion'};
const clip = (params = {}, extra = {}) => ({id: 'presenter', track: 'overlay', clipType: 'am-presenter',
  at: 0, hold: 2, params, elementRef: owner, ...extra});
const propsFor = (clips, b = basis) => {
  const timeline = {tracks: [...new Set(clips.map(c => c.track))].reverse().map(id => ({id, kind: 'visual'})), clips};
  const tracks = [...timeline.tracks].reverse().map(track => ({track, clips: clips.filter(c => c.track === track.id)}));
  return {timeline, theme, assets: {assets: {}},
    compiledTransitions: compileCanonicalTransitions(tracks, b.fps, runtimeTheme, registries)};
};
const render = (props, frame, b = basis, selectedRegistries = registries, Component = TimelineComposition) => {
  const metadata = {id: 'presenter', component: Component, defaultProps: {}, ...b,
    durationInFrames: 300, folderName: null, parentFolderName: null, nonce: [], schema: null,
    calculateMetadata: null, stack: null};
  return renderToStaticMarkup(h(Internals.CompositionManager.Provider, {value: {
    compositions: [metadata], currentCompositionMetadata: null, folders: [],
    canvasContent: {type: 'composition', compositionId: 'presenter'},
  }}, h(Internals.TimelineContext.Provider, {value: {frame: {presenter: frame}, playing: false,
    imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
  h(Internals.CanUseRemotionHooksProvider, null, h(Component, {...props, registries: selectedRegistries})))));
};
const query = (c, frame, b = basis) => {
  const props = propsFor([c], b);
  return querySceneFrame(prepareHostScene(props, b, {}), frame).layers[0];
};
const words = [[0, .2], [.3, .5], [.8, 1], [1.3, 1.5]];
const snapshots = () => {
  const cases = {
    defaults: {},
    empty: {chrome: 'none', blinkEvery: 0},
    poses: {words, chrome: 'none', blinkEvery: 0},
    clamps: {zoom: 99, focus: {x: -100, y: 999}, mouth: {x: -20, y: 900, w: 0}, words, bob: 9},
    malformed: {mouth: {x: 'bad', y: null, w: 900}, eyes: [null, {x: -1, y: 999, w: 0}],
      words: [null, [], [1, 0], ['0', 1], [.4, .6], [0, .2]], seed: -8.7},
    focus: {zoom: 2, focus: {x: 180.6, y: 110.2}, words, mouth: {x: 155.8, y: 107.2, w: 21.6}},
    push: {zoom: 1, push: {to: 3.5, frames: 28, at: 2}, focus: {x: 191.2, y: 110.4}, words},
    punch: {zoom: 3, punchAt: [1, 10], words},
    bob: {bob: 1, words: [[0, .1], [.2, .3], [.4, .5], [.6, .7]], seed: 9},
    mosaic: {words, mosaicIn: {frames: 8}, mosaicOut: {frames: 8}},
    chrome: {words, chrome: 'label', label: 'Take', chip: {text: 'one', swapTo: 'two', swapAt: 2}},
  };
  return Object.fromEntries([30, 24000 / 1001].flatMap(fps => Object.entries(cases).map(([name, params]) => {
    const b = {...basis, fps};
    const props = propsFor([clip(params)], b);
    return [`${fps}:${name}`, [0, 1, 2, 3, 5, 6, 7, 8, 10, 15, 29, 47, 59].map(frame =>
      createHash('sha256').update(render(props, frame, b)).digest('hex'))];
  })));
};

const mode = process.argv[2];
if (mode === 'snapshots') {
  console.log(JSON.stringify(snapshots()));
} else {
  assert.ok(['states', 'geometry', 'unknowns', 'clock', 'registration', 'exact-fold'].includes(mode));
  const {MOUTH_LEVEL, motionAt, presenterAt, mouthStateAt} = source;
  const support = (c, frame, b = basis) => source.Presenter.prepareSceneCapability({clip: c, ...b,
    rendererIdentity: 'registered-ssr', fontDigests: {}}).frame(frame);
  const drawnOverlay = (c, frame, b = basis) => render({clip: c, params: c.params, fps: b.fps}, frame, b,
    registries, source.Presenter);
  const px = value => value === 0 ? '0' : `${value}px`;
  const geometry = (c, frame, fps, rect) => {
    const {left: x, top: y, width, height} = source.pixelGeometry(rect, presenterAt(c.params, frame, fps).view);
    return {x, y, width, height};
  };
  const erase = (c, frame, fps) => geometry(c, frame, fps, source.mouthEraseRect(source.mouthAnchor(c.params)));
  const inspection = (c, frame, fps) => geometry(c, frame, fps, source.mouthInspectionRect(c.params));
  const eraseStyle = rect => `position:absolute;left:${px(rect.x)};top:${px(rect.y)};width:${px(rect.width)};height:${px(rect.height)};background:`;
  const assertMotion = (c, frame, b = basis, layer = query(c, frame, b), supplied = frame) => {
    assert.deepEqual(layer.diagnostics.motion, motionAt(c.params, supplied, b.fps));
    const state = mouthStateAt(presenterAt(c.params, supplied, b.fps).timing, supplied);
    assert.equal(layer.diagnostics.motion.mouth, MOUTH_LEVEL[state]);
    return state;
  };

  if (mode === 'exact-fold') {
    const {repeated, samples} = JSON.parse(process.argv[3]);
    const fps = 30000 / 1001;
    const b = {...basis, fps};
    assert.equal(repeated.length, 2);
    const identity = c => c.app.astrid_shot_composition;
    assert.equal(identity(repeated[0]).source_clip_id, identity(repeated[1]).source_clip_id);
    assert.notEqual(identity(repeated[0]).occurrence_id, identity(repeated[1]).occurrence_id);
    const ids = new Map(repeated.map(c => [identity(c).occurrence_id, c.id]));
    // Keep the projector's exact occurrence IDs, even though times, labels and
    // source IDs coincide. These are synthetic authored inputs, not certified media.
    for (const [i, c] of repeated.entries()) Object.assign(c, {
      track: c.id, clipType: 'am-presenter', elementRef: owner, at: 0, from: 7,
      hold: (i === 0 ? 301 : 150.5) / fps, speed: i === 0 ? 1 : .5,
      params: {words: [[180 / fps, 183 / fps]], seed: 7, chrome: 'none', blinkEvery: 0},
    });
    const outgoing = clip({}, {id: 'out', track: 'transition', hold: 100 / fps});
    const incoming = clip({words: [[0, 6 / fps]], seed: 7, chrome: 'none', blinkEvery: 0},
      {id: 'in', track: 'transition', at: 100 / fps, from: 17, hold: 12 / fps, speed: 2,
        transition: {type: 'fade', duration: 6 / fps}});
    const props = propsFor([...repeated, outgoing, incoming], b);
    const original = JSON.stringify(props);
    // One actual host/public preparation for every selection and fact below.
    const scene = prepareHostScene(props, b, {});
    const observed = new Map();
    const firstId = ids.get(identity(repeated[0]).occurrence_id);
    const secondId = ids.get(identity(repeated[1]).occurrence_id);
    const request = {ranges: [[0, 301]], maxFrames: 301,
      clipIds: [secondId, 'in', firstId], keys: ['mouth', 'not-published']};
    const folded = foldSceneMotion(scene, (sameScene, frame) => {
      assert.equal(sameScene, scene);
      assert.equal(frame, observed.size);
      const answer = querySceneFrame(sameScene, frame);
      observed.set(frame, answer);
      return answer;
    }, request);
    assert.equal(observed.size, 301);
    assert.equal(folded.totalFrames, 301);
    assert.equal(JSON.stringify(props), original);
    assert.equal(scene.assets, props.assets);
    const counts = new Map(folded.counts.map(row => [`${row.clipId}:${row.key}`, row]));
    const expected = (clipId, key, values, unknownFrames = 0, absentFrames = 0) => {
      assert.deepEqual(counts.get(`${clipId}:${key}`), {
        clipId, key, values: values.map(([value, count]) => ({value, count})),
        unknownFrames, absentFrames, totalFrames: 301,
      });
    };
    expected(firstId, 'mouth', [[MOUTH_LEVEL.closed, 299], [MOUTH_LEVEL.half, 1], [MOUTH_LEVEL.open, 1]]);
    expected(secondId, 'mouth', [[MOUTH_LEVEL.closed, 301]]);
    expected('in', 'mouth', [[MOUTH_LEVEL.closed, 10], [MOUTH_LEVEL.half, 1], [MOUTH_LEVEL.open, 1]], 0, 289);
    expected(firstId, 'not-published', [], 301);
    expected(secondId, 'not-published', [], 301);
    expected('in', 'not-published', [], 12, 289);
    for (const row of folded.counts) assert.equal(row.values.reduce((n, v) => n + v.count, 0)
      + row.unknownFrames + row.absentFrames, row.totalFrames);
    const layer = (id, frame) => observed.get(frame).layers.find(l => l.clipId === id);
    assert.equal(samples.length, 60);
    for (const f of samples) assert.equal(layer(firstId, f).diagnostics.motion.mouth, MOUTH_LEVEL.closed);
    for (const f of [180, 181, 182]) assert.ok(!samples.includes(f));
    // Labels apply only to the resolved presenter, via its existing codebook.
    const labels = new Map(Object.entries(MOUTH_LEVEL).map(([label, value]) => [value, label]));
    assert.deepEqual(counts.get(`${firstId}:mouth`).values.map(({value, count}) =>
      ({label: labels.get(value), count})), [
      {label: 'closed', count: 299}, {label: 'half', count: 1}, {label: 'open', count: 1},
    ]);
    assert.equal(layer('in', 93), undefined);
    assert.equal(layer('in', 94).contentFrame, 0); // incoming preroll before authored at=100
    assert.equal(layer('in', 99).contentFrame, 5);
    assert.ok(layer('in', 105));
    assert.equal(layer('in', 106), undefined); // half-open end
    assert.equal(layer(firstId, 181).contentFrame, 181); // from=7 is not a second clock
    assert.equal(layer(secondId, 181).contentFrame, 181);
    // No source-ID fallback and no implicit/excessive frame allowance.
    const noQuery = () => assert.fail('invalid request must refuse before querying');
    for (const change of [{clipIds: [identity(repeated[0]).source_clip_id]},
      {maxFrames: undefined}, {maxFrames: 300}, {maxFrames: 3601}]) {
      assert.throws(() => foldSceneMotion(scene, noQuery, {...request, ...change}), /scene_motion_/);
    }
  }

  if (mode === 'states') {
    assert.deepEqual(MOUTH_LEVEL, {closed: 0, half: .5, open: 1});
    const seen = new Set();
    const inputs = [undefined, null, [], 'bad', [null, [], [1], [2, 1], ['0', 1], [0, null]],
      [[.8, 1], [0, .1], [.2, .3]], [[-.1, .1], [.1001, .101]], [[.1, .10001]],
      [[0, .1], [.2, .3]], [[0, .1], [.3, .4]], [[0, .1], [.22, .3]]];
    for (const fps of [30, 24000 / 1001, 30000 / 1001]) {
      const b = {...basis, fps};
      for (const words of inputs) for (const seed of [0, 7, -8.7]) {
        const c = clip({words, seed, chrome: 'none', blinkEvery: 0});
        const props = propsFor([c], b);
        const scene = prepareHostScene(props, b, {});
        for (let frame = 0; frame < Math.round(fps * 1.5); frame++) {
          const layer = querySceneFrame(scene, frame).layers[0];
          const state = assertMotion(c, frame, b, layer);
          seen.add(state);
          const html = render(props, frame, b);
          assert.ok(html.includes(drawnOverlay(c, frame, b)), `registered drawing ${fps}:${frame}`);
          assert.deepEqual(layer.diagnostics.mouth.rect, inspection(c, frame, fps));
          const mouth = erase(c, frame, fps);
          assert.equal(html.includes(eraseStyle(mouth) + '#EDB98E'), state !== 'closed');
        }
      }
    }
    assert.deepEqual([...seen].sort(), ['closed', 'half', 'open']);
    // Actual rounded onset/end and the <= .12 second gap hold are retained.
    const held = clip({words: [[.1, .2], [.3, .4]], seed: 7});
    assert.equal(query(held, 2).diagnostics.motion.mouth, 0);
    const last = query(held, 5).diagnostics.motion.mouth;
    for (const f of [6, 7, 8]) assert.equal(query(held, f).diagnostics.motion.mouth, last);
    assert.equal(query(held, 12).diagnostics.motion.mouth, 0);
    const long = clip({words: [[.1, .2], [.4, .5]], seed: 7});
    for (const f of [6, 7, 8, 9, 10, 11]) assert.equal(query(long, f).diagnostics.motion.mouth, 0);
  }

  if (mode === 'geometry') {
    const inputs = [{}, {mouth: {x: 151}}, {mouth: {x: 151, y: 104}}, {mouth: null}, {mouth: {x: -20, y: 999, w: 0}},
      {mouth: {x: 999, y: -1, w: 99}}, {mouth: {x: 152.5, y: 103.7, w: 20.6}},
      {zoom: 2, focus: {x: 190.4, y: 120.7}},
      {zoom: 99, focus: {x: -100, y: 999}},
      {push: {to: 3.5, frames: 28, at: 2}, focus: {x: 191.2, y: 110.4}},
      {zoom: 3, punchAt: [1, 10]}, {bob: 1, seed: 9}];
    for (const fps of [30, 24000 / 1001]) for (const params of inputs) {
      const b = {...basis, fps};
      const c = clip({words, chrome: 'none', blinkEvery: 0, ...params});
      const props = propsFor([c], b);
      const scene = prepareHostScene(props, b, {});
      for (const frame of [0, 1, 2, 3, 5, 6, 7, 8, 10, 15, 29]) {
        const layer = querySceneFrame(scene, frame).layers[0];
        assertMotion(c, frame, b, layer);
        assert.deepEqual(layer.diagnostics.mouth, support(c, frame, b).diagnostics.mouth);
        assert.equal(layer.diagnostics.mouth.status, 'known');
        const state = mouthStateAt(presenterAt(c.params, frame, fps).timing, frame);
        const html = render(props, frame, b);
        assert.deepEqual(layer.diagnostics.mouth.rect, inspection(c, frame, fps));
        if (state !== 'closed') assert.ok(html.includes(eraseStyle(erase(c, frame, fps)) + '#EDB98E'));
        assert.equal(layer.visible, 'unknown');
        assert.equal(layer.opaqueSupport, 'none');
        assert.equal(layer.diagnostics.face, undefined);
        assert.equal(layer.diagnostics.text, undefined);
      }
    }
    assert.deepEqual(query(clip(), 0).diagnostics.mouth.rect, {x: 894, y: 606, width: 138, height: 48});
    assert.deepEqual(query(clip({mouth: {x: -1, y: 999, w: 0}}), 0).diagnostics.mouth.rect,
      {x: -12, y: 1056, width: 30, height: 48});
    const small = {...basis, width: 960, height: 540};
    const layer = query(clip(), 0, small);
    // Logical overlay pixels are not rescaled to an invented 320x180 viewport.
    assert.deepEqual(layer.diagnostics.mouth.rect, {x: 894, y: 606, width: 138, height: 48});
    assert.deepEqual(layer.bounds.rect, {x: 0, y: 0, width: 960, height: 540});
  }

  if (mode === 'unknowns') {
    const c = clip({chrome: 'none', blinkEvery: 0});
    const props = propsFor([c]); // deliberately no plate, no assets
    assert.equal(render(props, 0).includes('<img'), false);
    assert.equal(drawnOverlay(c, 0), '<div style="position:absolute;inset:0;overflow:hidden;pointer-events:none"></div>');
    const s = support(c, 0);
    assert.equal(s.presence, 'unknown');
    assert.equal(s.opaqueSupport, 'none');
    assert.equal(s.diagnostics.mouth.status, 'known'); // footprint, not occupied pixels
    assert.equal(querySceneFrame(prepareHostScene(props, basis, {}), 0).coverage, 'UNKNOWN');
    for (const missing of [{asset: 'missing'}, {params: {...c.params, src: '/not-a-presenter-asset.png'}}]) {
      const other = {...c, ...missing};
      assert.deepEqual(support(other, 0), s);
      assert.equal(query(other, 0).diagnostics.face, undefined);
    }
    for (const ramps of [{mosaicIn: {frames: 8}}, {mosaicOut: {frames: 8}},
      {mosaicIn: {frames: 8, steps: [48, 6]}}]) {
      const m = clip({...ramps, words, chrome: 'none', blinkEvery: 0});
      for (const frame of [0, 1, 3, 4, 6, 7, 8, 52, 53, 54, 55, 56, 57, 58, 59]) {
        const layer = query(m, frame);
        assertMotion(m, frame, basis, layer);
        const direct = support(m, frame);
        assert.deepEqual(layer.diagnostics.mouth, direct.diagnostics.mouth);
        if (layer.diagnostics.mouth.status === 'unknown') {
          assert.match(layer.diagnostics.mouth.reason, /mosaic/);
          assert.equal(drawnOverlay(m, frame), drawnOverlay(c, 0));
        }
      }
    }
    assert.equal(query(clip({mosaicIn: {frames: 8}}), 0).diagnostics.mouth.status, 'unknown');
    assert.equal(query(clip({mosaicIn: {frames: 8}}), 6).diagnostics.mouth.status, 'known');
    for (const extra of [{cropLeft: .1}, {entrance: 'fade-up'}, {exit: 'fade-up'},
      {modifiers: [{id: 'unknown', element: {packId: 'missing', kind: 'modifier', id: 'missing'}, params: {}}]}]) {
      const outer = query({...c, ...extra}, 2);
      assert.equal(outer.diagnostics.mouth.status, 'unknown');
      assertMotion({...c, ...extra}, 2, basis, outer);
    }
  }

  if (mode === 'clock') {
    for (const fps of [30, 24000 / 1001]) for (const speed of [.5, 1, 2]) {
      const b = {...basis, fps};
      const outgoing = clip({chrome: 'none'}, {id: 'out', hold: 1});
      const incoming = clip({words, bob: 1, punchAt: [2, 8], chrome: 'none', blinkEvery: 0},
        {id: 'in', at: 1, from: 17, to: 18, hold: 1, speed, transition: {type: 'fade', duration: .4}});
      const props = propsFor([outgoing, incoming], b);
      const scene = prepareHostScene(props, b, {});
      let preroll = false;
      let remapDistinguished = speed === 1;
      const end = getTimelineDurationInFrames(props.timeline, fps);
      for (let frame = 0; frame <= end; frame++) {
        const row = querySceneFrame(scene, frame);
        const html = render(props, frame, b);
        for (const c of [outgoing, incoming]) {
          const layer = row.layers.find(l => l.clipId === c.id);
          assert.equal(html.includes(`data-clip-id="${c.id}"`), Boolean(layer));
          if (!layer) continue;
          const supplied = Math.floor(layer.contentFrame * (c.speed ?? 1));
          assertMotion(c, frame, b, layer, supplied);
          assert.ok(html.includes(drawnOverlay(c, supplied, b)), `actual draw clock ${fps}:${speed}:${frame}`);
          if (c === incoming && frame < Math.round(c.at * fps)) preroll = true;
          if (c === incoming && supplied !== layer.contentFrame
            && motionAt(c.params, supplied, fps).mouth !== motionAt(c.params, layer.contentFrame, fps).mouth) remapDistinguished = true;
        }
      }
      assert.equal(preroll, true);
      assert.equal(remapDistinguished, true);
      assert.ok(querySceneFrame(scene, end - 1).layers.some(layer => layer.clipId === 'in'));
      assert.equal(querySceneFrame(scene, end).layers.length, 0);
    }
  }

  if (mode === 'registration') {
    const c = clip();
    assert.equal(query(c, 0).diagnostics.motion.mouth, 0);
    assert.deepEqual(query({...c, elementRef: undefined}, 2).diagnostics, query(c, 2).diagnostics);
    assert.throws(() => query({...c, elementRef: {...owner, packId: 'missing'}}, 0), /Unknown effect owner/);
    const foreign = clip({tag: 'foreign', value: .5}, {elementRef: {...owner, packId: 'probe'}});
    const f = query(foreign, 2);
    assert.deepEqual(f.diagnostics.motion, {mouth: .5, clock: 2});
    assert.equal(f.diagnostics.mouth, undefined);
    assert.match(render(propsFor([foreign]), 2), /data-probe="foreign"/);
    assert.equal(render(propsFor([foreign]), 2).includes('PLACEHOLDER'), false);
    for (const value of [.25, -1, 2, Number.NaN, Number.POSITIVE_INFINITY]) {
      const other = {...foreign, params: {tag: 'foreign', value}};
      const layer = query(other, 0);
      const motion = layer.diagnostics.motion;
      assert.equal(motion?.mouth, Number.isFinite(value) ? value : undefined);
      if (!Number.isFinite(value)) assert.ok(layer.findings.some(f => f.code === 'invalid-component-diagnostics'));
      // Public scalar sanitizing does not invent a valid closed pose.
      assert.notEqual(motion?.mouth, MOUTH_LEVEL.closed);
    }
    const extension = {...foreign, clipType: 'presenter-probe', elementRef: {kind: 'effect', id: 'presenter-probe', packId: 'probe'}};
    assert.deepEqual(query(extension, 2).diagnostics.motion, {mouth: .5, clock: 2});
    assert.match(render(propsFor([extension]), 2), /data-probe="foreign"/);
    // Public prepare, not a host-specific special case, can prepare the same
    // resolved registered component alongside extension maps.
    const props = propsFor([c, {...extension, id: 'extension'}]);
    const tracks = props.timeline.tracks.map(track => ({track, clips: props.timeline.clips.filter(c => c.track === track.id)}));
    const scene = prepareCompositionScene(tracks, props.assets, 30, runtimeTheme, 1920, 1080,
      undefined, undefined, {}, '', {}, registries, props.compiledTransitions);
    assert.equal(querySceneFrame(scene, 2).layers.length, 2);
  }
  console.log(JSON.stringify({ok: true, case: mode}));
}
