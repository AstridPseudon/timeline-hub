// Same-film D09 public evaluator probe. SSR is supporting evidence only;
// coverage answers come from the public Composition evaluation entry.
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
      {kind: args.kind, resolveDir: args.resolveDir});
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
  'legacy-crossfade': null,
};
const name = process.argv[2];
assert.ok(Object.hasOwn(cases, name));
const suppliedTimeline = cases[name] ? null : JSON.parse(readFileSync(0, 'utf8'));
const clips = cases[name] ?? suppliedTimeline.clips;
const timeline = suppliedTimeline ?? {tracks: [...new Set(clips.map(clip => clip.track))].reverse()
  .map(id => ({id, kind: 'visual'})), clips};
const props = {timeline, theme, assets: {assets: {}}};
if (name === 'incoming-crossfade') {
  props.compiledTransitions = composition.compileCanonicalTransitions([...timeline.tracks].reverse()
    .map(track => ({track, clips: clips.filter(clip => clip.track === track.id)})), 30, toRuntimeTheme(theme), registries);
}
const roles = Object.fromEntries(clips.map(clip => [clip.id, 'picture']));
const scene = prepareHostScene(props, basis, roles);
const metadata = {id: 'd09', component: TimelineComposition, defaultProps: {}, ...basis,
  durationInFrames: 90, folderName: null, parentFolderName: null, nonce: [], schema: null,
  calculateMetadata: null, stack: null};
const ssr = frame => renderToStaticMarkup(h(Internals.CompositionManager.Provider, {value: {
  compositions: [metadata], currentCompositionMetadata: null,
  folders: [], canvasContent: {type: 'composition', compositionId: 'd09'},
}}, h(Internals.TimelineContext.Provider, {value: {frame: {d09: frame}, playing: false,
  imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
  h(Internals.CanUseRemotionHooksProvider, null, h(TimelineComposition, {...props, registries})))));
const end = name === 'legacy-crossfade' ? 45 : 60;
const answers = [];
for (let frame = 0; frame <= end; frame++) {
  const answer = querySceneFrame(scene, frame);
  const markup = ssr(frame);
  for (const clip of timeline.clips) {
    const layer = answer.layers.find(layer => layer.clipId === clip.id);
    assert.equal(markup.includes(`data-clip-id="${clip.id}"`), Boolean(layer), `mount ${clip.id} at ${frame}`);
    if (!layer) continue;
    assert.equal(layer.opaqueSupport, 'rect');
    assert.deepEqual(layer.bounds.rect, {x: 0, y: 0, width: 1920, height: 1080});
    assert.equal(layer.fullFrame, true);
    assert.deepEqual(layer.findings, []);
    if (name === 'legacy-crossfade') assert.ok(markup.includes(`opacity:${layer.opacity}`));
  }
  assert.equal((markup.match(/<img\b/g) ?? []).length, answer.layers.length);
  answers.push(answer);
}
console.log(JSON.stringify({answers: answers.slice(0, -1), after: answers.at(-1),
  props, basis, compiled: props.compiledTransitions !== undefined}));
