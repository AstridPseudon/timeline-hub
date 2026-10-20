const fs = require('node:fs');
const assert = require('node:assert/strict');
const ts = require('/home/user/work/app/node_modules/typescript');
const [sourcePath, payloadPath] = process.argv.slice(2);
const timeline = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));
let frame = 0;
const LiveSceneClip = () => null;
const nil = () => null;
const jsx = (type, props) => ({type, props});
const modules = {
  'react': {useMemo: fn => fn(), useEffect: nil},
  'react/jsx-runtime': {Fragment: 'Fragment', jsx, jsxs: jsx},
  'remotion': {useCurrentFrame: () => frame, useVideoConfig: () => ({width: 320, height: 180, fps: 30})},
  '@remotion/three': {ThreeCanvas: nil},
  './LiveSceneClip': {LiveSceneClip},
  'three': {},
  '@banodoco/timeline-composition': {DEFAULT_THEME: {visual: {color: {bg: '#050814'}}}, TimelineComposition: nil},
};
const code = ts.transpileModule(fs.readFileSync(sourcePath, 'utf8'), {
  fileName: sourcePath,
  compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.ReactJSX},
}).outputText;
const mod = {exports: {}};
new Function('require', 'module', 'exports', code)(name => {
  assert.ok(name in modules, `Unexpected import: ${name}`);
  return modules[name];
}, mod, mod.exports);
const observations = [];
for (frame = 0; frame <= 30; frame++) {
  const sources = [];
  const backgrounds = [];
  function walk(node) {
    if (Array.isArray(node)) return node.forEach(walk);
    if (!node || typeof node !== 'object') return;
    if (node.type === LiveSceneClip) sources.push(node.props);
    if (node.type === 'div' && node.props?.style?.background) backgrounds.push(node.props.style.background);
    walk(node.props?.children);
  }
  walk(mod.exports.ThreeTimelineComposition({timeline, assets: {assets: {}}, theme: modules['@banodoco/timeline-composition'].DEFAULT_THEME}));
  observations.push({frame, sources, backgrounds});
}
process.stdout.write(JSON.stringify(observations));
