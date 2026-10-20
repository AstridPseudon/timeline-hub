const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {test} = require('node:test');
const ts = require('typescript');

// Load Root.tsx in-process with the same transpile/stub shape as bounds.test.cjs.
// The registered calculateMetadata callbacks remain Root's implementation; only
// React, Remotion and Composition package imports are replaced.
const src = process.env.ROOT_SOURCE_DIR
  ? path.resolve(process.env.ROOT_SOURCE_DIR)
  : path.resolve(__dirname, '..', 'src');

const compileRoot = () => {
  const registered = [];
  const Composition = (props) => {
    registered.push(props);
    return null;
  };
  const modules = {
    'react': {},
    'react/jsx-runtime': {
      Fragment: 'Fragment',
      jsx: (type, props) => ({type, props}),
      jsxs: (type, props) => ({type, props}),
    },
    'remotion': {
      Composition,
      Sequence: () => null,
      useVideoConfig: () => ({width: 1920, height: 1080, fps: 30}),
    },
    '@remotion/media': {Video: () => null},
    '@banodoco/timeline-composition': {
      DEFAULT_THEME: {},
      TimelineComposition: () => null,
      getTimelineDurationInFrames: (timeline) => timeline.__testDurationInFrames ?? 1,
    },
    './ThreeTimelineComposition': {ThreeTimelineComposition: () => null},
    './fonts': {FontProvider: () => null},
    './host-registries': {resolveHostRegistries: () => ({})},
    './ReviewOverlay': {ReviewOverlay: () => null},
    './BoundsProbe': {BoundsProbe: () => null},
    './FrameDiagnostics': {FrameDiagnostics: () => null},
    './asset-source': {resolveInvocationAsset: (file) => file},
  };
  const filename = path.join(src, 'Root.tsx');
  const code = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.ReactJSX,
      esModuleInterop: true,
    },
  }).outputText;
  const mod = {exports: {}};
  const requireStub = (name) => {
    if (!(name in modules)) throw new Error(`Root.tsx imported an unstubbed module: ${name}`);
    return modules[name];
  };
  new Function('require', 'module', 'exports', code)(requireStub, mod, mod.exports);

  const walkTree = (node) => {
    if (node == null || typeof node !== 'object') return;
    if (Array.isArray(node)) {
      node.forEach(walkTree);
      return;
    }
    if (node.type === Composition) return node.type(node.props);
    if (typeof node.type === 'function') {
      walkTree(node.type(node.props));
      return;
    }
    walkTree(node.props && node.props.children);
  };
  walkTree(mod.exports.Root());
  assert.equal(registered.length, 2);
  assert.deepEqual(registered.map(({id}) => id), [
    'TimelineComposition',
    'ThreeTimelineComposition',
  ]);
  assert.ok(registered.every(({calculateMetadata}) => typeof calculateMetadata === 'function'));
  return registered;
};

const assets = {assets: {}};
const timelineWithDuration = (duration, extra = {}) => ({
  theme: 'banodoco-default',
  theme_overrides: {},
  clips: [],
  __testDurationInFrames: duration,
  ...extra,
});
const propsFor = (timeline, extra = {}) => ({timeline, assets, ...extra});

const metadataFor = async (props) => {
  const registrations = compileRoot();
  return Promise.all(registrations.map(({calculateMetadata}) => calculateMetadata({props})));
};

const assertSameMetadata = (metadata, expected) => {
  assert.equal(metadata.length, 2);
  metadata.forEach((value) => assert.deepEqual(value, expected));
};


test('both callbacks retain 300/600 frames for identical empty/sparse layers at rational FPS', async () => {
 for (const local of [1,31]) for (const total of [300,600]) {
  const fps=30000/1001;
  const timeline=timelineWithDuration(local,{clips:local===1?[]:[{id:'early'}],theme_overrides:{visual:{canvas:{width:320,height:180,fps}}}});
  assertSameMetadata(await metadataFor(propsFor(timeline,{astridCompositionDurationInFrames:total})),{width:320,height:180,fps,durationInFrames:total});
 }
});
test('boolean retained extents refuse', async () => {
 for(const value of [true,false]) await assert.rejects(()=>metadataFor(propsFor(timelineWithDuration(1),{astridCompositionDurationInFrames:value})));
});
