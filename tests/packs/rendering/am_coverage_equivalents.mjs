// Actual discovered AM components, their shared draw/capability helpers and the
// Root host registry adapter. SSR checks CSS/mounts, never decoded media pixels.
import assert from 'node:assert/strict';
import path from 'node:path';
import {readFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {build} from 'esbuild';
import {createElement as h} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';
import {DEFAULT_THEME, TimelineComposition, toRuntimeTheme} from '@banodoco/timeline-composition';
import * as composition from '@banodoco/timeline-composition';
import {querySceneFrame} from '@banodoco/timeline-composition/evaluation';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';

Error.stackTraceLimit = 0;
const project = process.cwd();
const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
const bundle = await build({stdin: {contents: `
export {prepareHostScene} from './src/host-scene';
export {resolveHostRegistries} from './src/host-registries';`, resolveDir: project},
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
const {prepareHostScene, resolveHostRegistries} = await import(
  `data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString('base64')}`);
const basis = {width: 1920, height: 1080, fps: 30};
const theme = DEFAULT_THEME;
const registries = resolveHostRegistries(toRuntimeTheme(theme));
const plate = (id, extra = {}) => ({id, track: 'plate', clipType: 'am-snap-plate',
  at: 0, hold: 1, params: {src: `/${id}.png`}, ...extra});
const cases = {
  'incoming-crossfade': [plate('out'), plate('in', {clipType: 'am-footage', at: 1,
    transition: {type: 'fade', duration: .5}})],
  'legacy-crossfade': [plate('out', {effects: {fade_out: .5}}),
    plate('in', {clipType: 'am-footage', track: 'fx', at: .5, effects: {fade_in: .5}})],
  'one-sided-fade': [plate('only', {hold: 2, effects: {fade_in: .5}})],
};
const name = process.argv[2];
assert.ok(Object.hasOwn(cases, name));
const clips = cases[name];
const timeline = process.argv[3] === '--timeline-stdin' ? JSON.parse(readFileSync(0, 'utf8'))
  : {tracks: [...new Set(clips.map(clip => clip.track))].reverse()
    .map(id => ({id, kind: 'visual'})), clips};
const props = {timeline, theme, assets: {assets: {}}};
if (name === 'incoming-crossfade') {
  props.compiledTransitions = composition.compileCanonicalTransitions([...timeline.tracks].reverse()
    .map(track => ({track, clips: clips.filter(clip => clip.track === track.id)})), 30, toRuntimeTheme(theme), registries);
}
const roles = Object.fromEntries(clips.map(clip => [clip.id, 'picture']));
const scene = prepareHostScene(props, basis, roles);
const metadata = {id: 'am', component: TimelineComposition, defaultProps: {}, ...basis,
  durationInFrames: 90, folderName: null, parentFolderName: null, nonce: [], schema: null,
  calculateMetadata: null, stack: null};
const ssr = frame => renderToStaticMarkup(h(Internals.CompositionManager.Provider, {value: {
  compositions: [metadata], currentCompositionMetadata: null, folders: [],
  canvasContent: {type: 'composition', compositionId: 'am'},
}}, h(Internals.TimelineContext.Provider, {value: {frame: {am: frame}, playing: false,
  imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
h(Internals.CanUseRemotionHooksProvider, null, h(TimelineComposition, {...props, registries})))));
const end = name === 'legacy-crossfade' ? 45 : 60;
const answers = [];
const html = {};
for (let frame = 0; frame <= end; frame++) {
  const answer = querySceneFrame(scene, frame);
  const markup = ssr(frame);
  html[frame] = markup;
  for (const clip of timeline.clips) {
    const layer = answer.layers.find(layer => layer.clipId === clip.id);
    assert.equal(markup.includes(`data-clip-id="${clip.id}"`), Boolean(layer), `mount ${clip.id} at ${frame}`);
    if (!layer) continue;
    assert.equal(layer.opaqueSupport, 'rect'); // actual solid field behind undecoded media
    assert.deepEqual(layer.bounds.rect, {x: 0, y: 0, width: 1920, height: 1080});
    assert.equal(layer.fullFrame, true);
    assert.deepEqual(layer.findings, []);
    if (name === 'legacy-crossfade') assert.ok(markup.includes(`opacity:${layer.opacity}`));
  }
  // Remotion's Img omits src during SSR; the real ClipLook wrapper identifies
  // each mounted clip, and its actual component still emits its image node.
  assert.equal((markup.match(/<img\b/g) ?? []).length, answer.layers.length);
  if (name === 'incoming-crossfade' && frame >= 15 && frame < 30) {
    const incoming = answer.layers.find(layer => layer.clipId === 'in');
    assert.ok(markup.includes(`opacity:${incoming.transitionOpacity}`));
    assert.match(markup, /background-color:#F7F4ED/);
    assert.match(markup, /background:#1F1F1F/);
  }
  if (name === 'one-sided-fade' && frame < end) {
    const layer = answer.layers[0];
    assert.ok(markup.includes(`opacity:${layer.opacity}`));
    assert.match(markup, /background-color:#F7F4ED/);
  }
  answers.push(answer);
}
console.log(JSON.stringify({answers: answers.slice(0, -1), after: answers.at(-1), html,
  props, basis, compiled: props.compiledTransitions !== undefined}));
