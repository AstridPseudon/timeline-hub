// Actual registered Root and component bodies. SSR is supporting evidence;
// the separately granted frames runner supplies all decoded pixels.
import assert from 'node:assert/strict';
import path from 'node:path';
import {readFileSync, writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {build} from 'esbuild';
import {createElement as h} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Composition, Internals} from 'remotion';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';

const project = process.cwd();
const old = process.argv[2] === 'main';
const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
const result = await build({stdin: {contents: `
export {Root} from './src/Root';
${old ? "export {EFFECT_REGISTRY} from './node_modules/@banodoco/timeline-composition/typescript/src/effects.generated';"
  : "export {resolveHostRegistries} from './src/host-registries'; export {prepareHostScene} from './src/host-scene'; export {querySceneFrame} from '@banodoco/timeline-composition/evaluation';"}
`, resolveDir: project}, bundle: true, write: false, metafile: true,
platform: 'node', format: 'esm', jsx: 'automatic',
nodePaths: [path.join(project, 'node_modules')], logLevel: 'silent', plugins: [{name: 'actual-host-aliases', setup(builder) {
  builder.onResolve({filter: /^[^./]/}, async args => {
    if (args.pluginData?.resolving) return;
    const alias = Object.keys(aliases).find(key => args.path === key || args.path.startsWith(`${key}/`));
    if (alias) return builder.resolve(path.join(aliases[alias], args.path.slice(alias.length)),
      {kind: args.kind, resolveDir: project});
    if (args.path.startsWith('@banodoco/')) return;
    const resolved = await builder.resolve(args.path, {kind: args.kind, resolveDir: args.resolveDir,
      pluginData: {resolving: true}});
    if (resolved.errors.length) return {errors: resolved.errors};
    return {path: path.isAbsolute(resolved.path) ? pathToFileURL(resolved.path).href : resolved.path, external: true};
  });
}}]});
const host = await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`);
const selected = host.Root().props.children.find(child => child.type === Composition
  && child.props.id === 'TimelineComposition');
assert.ok(selected, 'normal Root must register the composition');
const props = JSON.parse(readFileSync('props.json', 'utf8'));
const basis = {width: 1920, height: 1080, fps: 30, durationInFrames: 45};
assert.deepEqual(await selected.props.calculateMetadata({props}), basis);
const metadata = {...basis, id: 'TimelineComposition', component: selected.props.component,
  defaultProps: selected.props.defaultProps, folderName: null, parentFolderName: null,
  nonce: [], schema: null, calculateMetadata: null, stack: null};
const ssr = (component, input, frame) => renderToStaticMarkup(h(Internals.CompositionManager.Provider, {value: {
  compositions: [metadata], currentCompositionMetadata: null, folders: [],
  canvasContent: {type: 'composition', compositionId: metadata.id},
}}, h(Internals.TimelineContext.Provider, {value: {frame: {[metadata.id]: frame},
  playing: false, imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
  h(Internals.CanUseRemotionHooksProvider, null, h(component, input)))));
const html = {};
for (let frame = 0; frame < 45; frame++) html[frame] = ssr(selected.props.component, props, frame);
const effects = old ? host.EFFECT_REGISTRY : host.resolveHostRegistries(props.theme).effects;
const bodies = {};
for (const clip of props.timeline.clips) {
  assert.ok(effects[clip.clipType], `actual discovered ${clip.clipType}`);
  bodies[clip.id] = Array.from({length: 30}, (_, frame) => ssr(effects[clip.clipType],
    {clip, params: clip.params, fps: 30, theme: props.theme,
      assetEntry: clip.asset ? props.assets.assets[clip.asset] : undefined}, frame));
}
let answers = null;
if (!old) {
  const scene = host.prepareHostScene(props, basis,
    Object.fromEntries(props.timeline.clips.map(clip => [clip.id, 'picture'])));
  answers = Array.from({length: 46}, (_, frame) => host.querySceneFrame(scene, frame));
}
writeFileSync('inspection.json', JSON.stringify({props, html, bodies, answers,
  inputs: Object.keys(result.metafile.inputs).filter(file => file !== '<stdin>')}));
