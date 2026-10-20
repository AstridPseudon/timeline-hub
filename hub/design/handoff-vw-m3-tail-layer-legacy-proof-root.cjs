// Execute each revision's actual Root callbacks and tail component. No browser.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const ts = require('/home/user/work/app/node_modules/typescript/lib/typescript.js');
const base = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const worker = `${base}/workers/vw-m3-tail-layer-legacy-proof`;
const evidence = `${base}/design/handoff-vw-m3-tail-layer-legacy-proof`;

function compile(filename, modules) {
  const code = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
    compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.ReactJSX, esModuleInterop: true, allowJs: true}, fileName: filename,
  }).outputText;
  const module = {exports: {}};
  new Function('require', 'module', 'exports', code)(name => {
    assert.ok(name in modules, `Unexpected import: ${name}`);
    return modules[name];
  }, module, module.exports);
  return module.exports;
}

// This is the unchanged duration chunk of the actual locked public12 artifact,
// not a second duration implementation or a stubbed arithmetic return value.
const duration = compile(`${worker}/package-duration-chunk.js`, {});
const nil = () => null;
const Sequence = props => props.children;
const Video = () => null;
const Composition = () => null;
const modules = {
  'react/jsx-runtime': {Fragment: 'Fragment', jsx: (type, props) => ({type, props}),
    jsxs: (type, props) => ({type, props})},
  remotion: {Composition, Sequence, useVideoConfig: () => ({fps: 30})},
  '@remotion/media': {Video},
  '@banodoco/timeline-composition': {...duration, TimelineComposition: nil, DEFAULT_THEME: {}},
  './fonts': {FontProvider: nil}, './ReviewOverlay': {ReviewOverlay: nil},
  './FrameDiagnostics': {FrameDiagnostics: nil}, './BoundsProbe': {BoundsProbe: nil},
  './asset-source': {resolveInvocationAsset: file => file},
  './host-registries': {resolveHostRegistries: () => ({})},
};
function walk(node, visit) {
  if (Array.isArray(node)) return node.forEach(child => walk(child, visit));
  if (!node || typeof node !== 'object') return;
  visit(node);
  if (typeof node.type === 'function') walk(node.type(node.props), visit);
  else walk(node.props?.children, visit);
}

(async () => {
  const summaries = {};
  for (const [label, source] of [['old', `${worker}/old-source`],
    ['new', '/home/user/work/wt/vw-m3-tail-layer-legacy-proof']]) {
    const dataset = JSON.parse(fs.readFileSync(`${evidence}-${label}.json`, 'utf8'));
    const root = compile(`${source}/remotion/src/Root.tsx`, modules).Root();
    const compositions = root.props.children.filter(el => el.type === Composition);
    assert.equal(compositions.length, 2);
    const records = [];
    for (const row of dataset.rows) {
      const metadata = await Promise.all(compositions.map(el => el.props.calculateMetadata({props: row.props})));
      assert.deepEqual(metadata[0], metadata[1]);
      assert.equal(metadata[0].fps, 30);
      const localSeconds = row.props.timeline.metadata?.duration_seconds;
      assert.equal(metadata[0].durationInFrames, row.window === null && localSeconds !== undefined
        ? Math.round(localSeconds * 30) : 330);
      const sequences = [];
      const videos = [];
      walk(compositions[0].props.component(row.props), el => {
        if (el.type === Sequence) sequences.push(el.props);
        if (el.type === Video) videos.push(el.props);
      });
      assert.equal(sequences.length, 1);
      assert.equal(sequences[0].from, row.render_clip_extent);
      assert.equal(sequences[0].durationInFrames, 330 - row.render_clip_extent);
      assert.equal(videos[0].src, 'tail.mp4');
      assert.equal(videos[0].trimBefore, 300);
      assert.equal(videos[0].trimAfter, 330);
      assert.equal(videos[0].muted, true);
      if (row.case === 'ordinary-full') {
        assert.equal(metadata[0].durationInFrames, 330);
        assert.equal(sequences[0].from, 300);
        assert.equal(sequences[0].durationInFrames, 30);
      }
      // Root does not infer tail ownership from a clip track or Source role.
      // The unchanged source_asset remains sufficient to mount its Video.
      const missing = structuredClone(row.props);
      delete missing.assets.assets.tail;
      let missingVideos = 0;
      walk(compositions[0].props.component(missing), el => {if (el.type === Video) missingVideos++;});
      assert.equal(missingVideos, 0);
      records.push({shape: row.shape, source_role: row.source_role, case: row.case, window: row.window,
        selected_absolute_window: row.selected_absolute_window,
        root_duration: metadata[0].durationInFrames, tail_from: sequences[0].from,
        tail_duration: sequences[0].durationInFrames, trim_before: videos[0].trimBefore,
        trim_after: videos[0].trimAfter,
        duration_boundary: row.render_duration, native_boundary: row.native_argument});
    }
    summaries[label] = records;
    console.log(`${dataset.revision}: ${records.length} real service rows; both Root metadata callbacks + 2D tail tree passed`);
  }
  const pick = (label, shape, name) => summaries[label].find(row => row.shape === shape && row.case === name);
  const mismatch = 'render clock authored_duration_frames must match the authored clip extent';
  for (const label of ['old', 'new']) {
    assert.deepEqual(pick(label, 'empty', 'ordinary-window-300-330').native_boundary,
      {value: '--frames=300-329'});
    assert.deepEqual(pick(label, 'empty', 'top-150-180-supports-True').duration_boundary, {error: mismatch});
  }
  assert.equal(pick('old', 'empty', 'top-150-180-supports-True').tail_from, 1);
  assert.equal(pick('old', 'sparse-middle', 'top-150-180-supports-True').tail_from, 15);
  assert.equal(pick('old', 'empty', 'bottom-285-315-supports-True').tail_from, 15);
  assert.equal(pick('new', 'empty', 'bottom-285-315-supports-True').tail_from, 300);
  assert.deepEqual(pick('new', 'empty', 'bottom-285-315-supports-True').native_boundary,
    {value: '--frames=285-314'});
  // Even a sparse top layer ending at the original extent mounts the tail:
  // successful duration admission alone cannot establish intended ownership.
  assert.deepEqual(pick('new', 'sparse-end', 'top-300-330-supports-True').native_boundary,
    {value: '--frames=300-329'});
  assert.equal(pick('new', 'sparse-end', 'top-300-330-supports-True').tail_from, 300);
  const unchanged = rows => rows.filter(row => row.case.startsWith('ordinary-') || row.case.endsWith('supports-False'));
  assert.deepEqual(unchanged(summaries.old), unchanged(summaries.new));
  console.log(`${unchanged(summaries.old).length} ordinary/full-timeline-only rows unchanged across revisions`);
  fs.writeFileSync(`${evidence}-root-results.json`, JSON.stringify(summaries, null, 2));
})().catch(error => {console.error(error); process.exitCode = 1;});
