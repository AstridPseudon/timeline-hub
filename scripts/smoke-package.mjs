// Installs the actual tarball in isolation; no source aliases or installed edits.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {dirname, join, resolve} from 'node:path';

const tarball = resolve(process.argv[2] ?? 'banodoco-timeline-composition-0.0.10.tgz');
const files = execFileSync('tar', ['-tzf', tarball], {encoding: 'utf8'}).trim().split('\n');
assert.ok(files.every(file => /^package\/(?:dist\/.*\.(?:js|d\.ts)|package\.json|README\.md|LICENSE)$/.test(file)),
  'Tarball contains source, scripts, tests or other unexpected files');
const temporary = mkdtempSync(join(tmpdir(), 'composition-consumer-'));
const run = (command, args) => execFileSync(command, args, {cwd: temporary, stdio: 'inherit'});
try {
  writeFileSync(join(temporary, 'package.json'), JSON.stringify({private: true, type: 'module', dependencies: {
    '@banodoco/timeline-composition': `file:${tarball}`,
    react: '18.3.1', 'react-dom': '18.3.1', remotion: '4.0.509',
    '@remotion/media': '4.0.509', '@remotion/layout-utils': '4.0.509',
  }, devDependencies: {typescript: '5.9.3', '@types/react': '18.3.31', '@types/react-dom': '18.3.7'}}));
  run('npm', ['install', '--no-audit', '--no-fund']);
  const installed = join(temporary, 'node_modules', '@banodoco', 'timeline-composition');
  const snapshot = () => {
    const hash = createHash('sha256');
    const visit = directory => {
      for (const entry of readdirSync(directory, {withFileTypes: true}).sort((a, b) => a.name.localeCompare(b.name))) {
        const path = join(directory, entry.name);
        if (entry.isDirectory()) visit(path);
        else hash.update(path.slice(installed.length)).update(readFileSync(path));
      }
    };
    visit(installed);
    return hash.digest('hex');
  };
  const before = snapshot();
  const entries = JSON.parse(readFileSync(join(installed, 'package.json'), 'utf8')).exports;
  for (const [name, entry] of Object.entries(entries)) {
    if (name === './package.json') continue;
    assert.equal(entry.import, entry.default);
    assert.ok(entry.import.startsWith('./dist/'));
    assert.ok(entry.types.endsWith('.d.ts'));
  }
  // Every emitted import is local built code or an exact external peer. Inspect
  // the evaluator's transitive graph separately: it must have no runtime peers.
  const inspect = (path, pure = false, seen = new Set()) => {
    if (seen.has(path)) return;
    seen.add(path);
    const source = readFileSync(path, 'utf8');
    for (const match of source.matchAll(/(?:from\s*|import\s*\()(['"])([^'"]+)\1/g)) {
      const specifier = match[2];
      if (specifier.startsWith('.')) {
        assert.ok(specifier.endsWith('.js'), `Non-ESM import: ${specifier}`);
        const target = resolve(dirname(path), specifier);
        assert.ok(target.startsWith(installed + '/dist/'));
        inspect(target, pure, seen);
      } else {
        assert.ok(!pure, `Pure evaluation imports ${specifier}`);
        assert.match(specifier, /^(?:react(?:\/.*)?|react-dom(?:\/.*)?|remotion|@remotion\/(?:media|layout-utils))$/);
      }
    }
  };
  inspect(join(installed, 'dist', 'evaluation.js'), true);
  for (const file of readdirSync(join(installed, 'dist')).filter(file => file.endsWith('.js'))) {
    inspect(join(installed, 'dist', file));
  }
  writeFileSync(join(temporary, 'smoke.mjs'), `
import assert from 'node:assert/strict';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {createRequire} from 'node:module';
import {realpathSync} from 'node:fs';
import {Internals} from 'remotion';
const root = await import('@banodoco/timeline-composition');
const evaluation = await import('@banodoco/timeline-composition/evaluation');
assert.strictEqual(root.querySceneOcclusion, evaluation.querySceneOcclusion);
const api = await import('@banodoco/timeline-composition/theme-api');
const helpers = await import('@banodoco/timeline-composition/registries');
const themes = await import('@banodoco/timeline-composition/registry.generated');
for (const name of ['effects', 'animations', 'transitions']) await import('@banodoco/timeline-composition/' + name + '.generated');
assert.strictEqual(root.ThemeProvider, api.ThemeProvider);
assert.strictEqual(root.useTheme, api.useTheme);
assert.strictEqual(root.ElementRegistryProvider, helpers.ElementRegistryProvider);
const require = createRequire(import.meta.url);
const packageRequire = createRequire(import.meta.resolve('@banodoco/timeline-composition'));
for (const peer of ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']) {
  assert.equal(realpathSync(require.resolve(peer + '/package.json')), realpathSync(packageRequire.resolve(peer + '/package.json')));
}
assert.equal(evaluation.queryTrackFrame(evaluation.prepareTrack([{start: 0, duration: 30}], []), 0).layers.length, 1);
const faded = {id: 'faded', track: 'visual', at: 0, hold: 2, speed: 2, opacity: .4,
  effects: [{fade_in: .4}, {fade_out: .4}]};
assert.equal(evaluation.clipOpacity(faded, 6, 30), .2);
assert.equal(evaluation.clipOpacity(faded, 30, 30), 0);
assert.equal(evaluation.clipOpacity({...faded, opacity: 0}, 12, 30), 0);
assert.equal(evaluation.clipOpacity({...faded, effects: {fade_in: .4}}, 42, 30), .4);
const spans = [{start: 60, duration: 30}, {start: 90, duration: 30}];
const native = evaluation.prepareTrack(spans, [{T: 12, kind: 'dip', align: 'end', incomingPolicy: 'preroll-crossfade'}]);
assert.deepEqual(evaluation.queryTrackFrame(native, 84).layers.map(layer => [layer.contentFrame, layer.opacity]), [[24, 1], [6, .5]]);
assert.equal(evaluation.queryTrackFrame(native, 90).layers[0].contentFrame, 12);
assert.deepEqual(evaluation.queryTrackFrame(native, 120).layers, []);
const legacy = evaluation.prepareTrack(spans, [{T: 12, kind: 'dip', align: 'end'}]);
assert.deepEqual(evaluation.queryTrackFrame(legacy, 84).layers.map(layer => [layer.contentFrame, layer.opacity]), [[24, 0], [0, 0]]);
const theme = {...themes.BUNDLED_THEMES['2rp'], visual: {...themes.BUNDLED_THEMES['2rp'].visual,
  color: {fg: '#123456', bg: '#010203', accent: '#abcdef'}}};
const track = {id: 'visual', kind: 'visual', label: 'Visual'};
const clip = {id: 'card', track: 'visual', at: 0, hold: 2, clipType: 'resource-card', params: {title: 'Bundled resource', entrance: [], exit: []}};
const assets = {assets: {}};
const Custom = Object.assign(() => createElement('strong', null, 'host:' + api.useTheme().color.fg), {
  prepareSceneCapability: context => {
    assert.ok(Object.hasOwn(context, 'assetEntry'));
    assert.equal(context.assetEntry, undefined);
    return {identity: 'host@1', frame: contentFrame => ({presence: 'present', opaqueSupport: 'none',
      bounds: {status: 'known', rect: {x: 0, y: 0, width: 100, height: 100}},
      diagnostics: {motion: {zoom: 1 + contentFrame / 100},
        face: {status: 'known', rect: {x: contentFrame, y: 0, width: 20, height: 30}},
        mouth: {status: 'unknown', reason: 'Not declared by this fixture'},
        text: {bounds: {status: 'unknown', reason: 'Fonts not admitted'}}}})};
  }});
const registries = {effects: {'resource-card': Custom}};
const prepare = maps => root.prepareCompositionScene([{track, clips: [clip]}], assets, 30, root.toRuntimeTheme(theme),
  1920, 1080, undefined, undefined, {}, '', {}, maps);
assert.equal(evaluation.querySceneFrame(prepare(registries), 0).layers[0].visible, true);
const declared = evaluation.querySceneFrame(prepare(registries), 12);
assert.equal(declared.layers[0].diagnostics.motion.zoom, 1.12);
assert.equal(declared.layers[0].diagnostics.face.rect.x, 12);
assert.equal(declared.layers[0].diagnostics.text.bounds.status, 'unknown');
assert.deepEqual(evaluation.querySceneOcclusion(declared, 'card', .9), {status: 'known', occluderId: null, fraction: 0});
const opaque = {effects: {'resource-card': Object.assign(() => null, {prepareSceneCapability: () => ({identity: 'solid@1',
  frame: () => ({presence: 'present', opaqueSupport: 'rect', bounds: {status: 'known', rect: {x: 0, y: 0, width: 100, height: 100}}})})})}};
const stack = root.prepareCompositionScene([{track, clips: [clip, {...clip, id: 'upper'}]}], assets, 30,
  root.toRuntimeTheme(theme), 1920, 1080, undefined, undefined, {}, '', {}, opaque);
assert.deepEqual(evaluation.querySceneOcclusion(evaluation.querySceneFrame(stack, 0), 'card', .98),
  {status: 'known', occluderId: 'upper', fraction: 1});
assert.equal(evaluation.querySceneFrame(prepare(), 0).layers[0].visible, 'unknown');
const render = maps => {
  const composition = {id: 'test', width: 1920, height: 1080, fps: 30, durationInFrames: 60,
    defaultProps: {}, folderName: null, parentFolderName: null, component: () => null,
    nonce: [], schema: null, calculateMetadata: null, stack: null};
  return renderToStaticMarkup(createElement(Internals.CompositionManager.Provider, {value: {
    compositions: [composition], currentCompositionMetadata: null, folders: [], canvasContent: {type: 'composition', compositionId: 'test'},
  }}, createElement(Internals.TimelineContext.Provider, {value: {frame: {test: 24}, playing: false,
    imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
    createElement(Internals.CanUseRemotionHooksProvider, null, createElement(root.TimelineComposition, {
      timeline: {theme: '2rp', tracks: [track], clips: [clip]}, assets, theme, registries: maps})))));
};
assert.match(render(), /Bundled resource/);
assert.match(render(), /rgb\\(18, 52, 86\\)|#123456/);
assert.match(render(registries), /host:#123456/);
const CustomAnimation = ({progress, easing}) => ({content: 'host:' + progress + ':' + easing});
for (const id of ['project-sweep', 'type-on']) {
  const maps = durationFrames => ({animations: {[id]: CustomAnimation},
    animationDefaults: {[id]: {durationFrames, startFrame: 'host-owned'}},
    animationMeta: {[id]: {kind: 'hook', supportsEasing: true}}});
  const animate = registries => api.composeAnimations({clip, refs: {id, easing: 'ease-in'}, phase: 'entrance',
    content: 'original', theme: root.toRuntimeTheme(theme), fps: 30, elapsedFrames: 25, registries});
  assert.equal(animate(maps(100)), 'host:0.0625:in');
  assert.equal(animate(maps(50)), 'host:0.25:in');
  assert.equal(animate(maps(100)), 'host:0.0625:in');
  assert.throws(() => animate({...maps(100), animationMeta: {[id]: {kind: 'hook'}}}), /cannot consume explicit easing/);
}
assert.equal(themes.BUNDLED_THEME_VERSIONS['2rp'], '0.1.0');
console.log('Plain Node ESM, bundled render, scoped host capability/override and shared theme/peer identity passed');
`);
  run(process.execPath, ['smoke.mjs']);
  writeFileSync(join(temporary, 'consumer.ts'), `
import {TimelineComposition, prepareCompositionScene, type TimelineClip, type TrackDefinition, type CompositionRegistries, type TransitionReferenceObject} from '@banodoco/timeline-composition';
import {clipOpacity, prepareTrack, queryTrackFrame, querySceneOcclusion, declareAppTransition, type SceneFrame, type SceneOcclusion,
  type ComponentDiagnostics, type ComponentFrameSupport, type TransitionSpec, type IncomingTransitionPolicy, type ComponentCapabilityContext} from '@banodoco/timeline-composition/evaluation';
import {composeAnimations, type EffectProps, type RuntimeTheme, type HookAnimationProps} from '@banodoco/timeline-composition/theme-api';
import {resolveElementRegistries} from '@banodoco/timeline-composition/registries';
import {EFFECT_REGISTRY} from '@banodoco/timeline-composition/effects.generated';
import {THEME_PACKAGE_REGISTRY} from '@banodoco/timeline-composition/registry.generated';
import {ANIMATION_META} from '@banodoco/timeline-composition/animations.generated';
import {TRANSITION_META} from '@banodoco/timeline-composition/transitions.generated';
const host: CompositionRegistries = {effects: {custom: (_props: EffectProps<{title: string}>) => null}};
host.animations = {custom: (props: HookAnimationProps) => ({content: props.progress})};
host.animationMeta = {custom: {kind: 'hook', supportsEasing: true}};
const resolved = (theme: RuntimeTheme) => resolveElementRegistries(theme, host);
const clip: TimelineClip = {id: 'x', at: 0, hold: 1, track: 'v', clipType: 'custom'};
const opacity: number = clipOpacity(clip, 6, 30);
const incomingPolicy: IncomingTransitionPolicy = 'preroll-crossfade';
const transition: TransitionReferenceObject = {id: 'fade', durationFrames: 12, align: 'end', incomingPolicy};
const spec: TransitionSpec = {T: 12, kind: 'dip', align: 'end', incomingPolicy};
const contentFrame: number = queryTrackFrame(prepareTrack([{start: 0, duration: 30}], [spec]), 0).layers[0].contentFrame;
declareAppTransition('v', 'x', {type: 'fade', duration: .4, incomingPolicy}, 30, 'timeline-composition');
const selectedFile = (context: ComponentCapabilityContext): string | undefined => context.assetEntry?.file;
const occlusion = (answer: SceneFrame): SceneOcclusion => querySceneOcclusion(answer, 'x', .90);
const diagnostics: ComponentDiagnostics = {motion: {zoom: 1.2}, face: {status: 'unknown', reason: 'No face declaration'},
  text: {bounds: {status: 'known', rect: {x: 0, y: 0, width: 100, height: 50}}, minPx: 24}};
const support: ComponentFrameSupport = {presence: 'present', opaqueSupport: 'none', bounds: {status: 'unknown', reason: 'Glyphs'}, diagnostics};
void [opacity, transition, contentFrame, selectedFile, occlusion, support];
void [TimelineComposition, prepareCompositionScene, prepareTrack, composeAnimations, resolved, clip, EFFECT_REGISTRY,
  THEME_PACKAGE_REGISTRY, ANIMATION_META, TRANSITION_META];
`);
  run(process.execPath, ['node_modules/typescript/bin/tsc', '--noEmit', '--strict', '--skipLibCheck',
    '--module', 'NodeNext', '--moduleResolution', 'NodeNext', '--target', 'ES2022', 'consumer.ts']);
  run('npm', ['ls', 'react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils', '@banodoco/timeline-composition']);
  assert.equal(snapshot(), before, 'Consumer modified the installed package');
  const lock = JSON.parse(readFileSync(join(temporary, 'package-lock.json'), 'utf8'));
  console.log('Installed integrity:', lock.packages['node_modules/@banodoco/timeline-composition'].integrity);
  console.log('Package smoke passed; installed files unchanged.');
} finally {
  rmSync(temporary, {recursive: true, force: true});
}
