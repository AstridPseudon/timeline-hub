// Offline fixture only. Copies selected App declarations verbatim; never stages an App repo.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';

const proposal = path.dirname(fileURLToPath(import.meta.url));
const orch = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const worker = `${orch}/workers/vw-m3-app-pcm13-implementation-brief`;
const fixture = `${worker}/fixture`;
const deps = `${orch}/workers/vw-m3-app-private12-clean-install/clean-project/node_modules`;
const ref = 'b1ef4b9b910ba72375c34cf319692f90d22edc25';
const require = createRequire(`${deps}/typescript/package.json`);
const ts = require(`${deps}/typescript`);
fs.mkdirSync(`${fixture}/node_modules/@banodoco/timeline-composition`, {recursive: true});
const archive = `${orch}/artifacts/banodoco-timeline-composition-0.0.13.tgz`;
const bytes = fs.readFileSync(archive);
if (createHash('sha256').update(bytes).digest('hex') !== '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738') throw Error('public13 archive mismatch');
// stage.py verifies/extracts the archive and reads Git without Node child processes.
// Real scope directories; only leaf links can point into the read-only graph.
for (const name of fs.readdirSync(deps)) {
  if (name.startsWith('.')) continue;
  if (name.startsWith('@')) {
    fs.mkdirSync(`${fixture}/node_modules/${name}`, {recursive: true});
    for (const leaf of fs.readdirSync(`${deps}/${name}`)) {
      if (name === '@banodoco' && leaf === 'timeline-composition') continue;
      const dest = `${fixture}/node_modules/${name}/${leaf}`;
      if (!fs.existsSync(dest)) fs.symlinkSync(`${deps}/${name}/${leaf}`, dest);
    }
  } else {
    const dest = `${fixture}/node_modules/${name}`;
    if (!fs.existsSync(dest)) fs.symlinkSync(`${deps}/${name}`, dest);
  }
}
const src = (name) => fs.readFileSync(`${fixture}/raw/${name}`, 'utf8');
const put = (name, text) => fs.writeFileSync(`${fixture}/${name}`, text);
const pick = (name, names) => {
  const text = src(name);
  const ast = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, name.endsWith('.tsx') ? ts.ScriptKind.TSX : ts.ScriptKind.TS);
  return names.map(wanted => {
    const statement = ast.statements.find(s => s.name?.text === wanted
      || (ts.isVariableStatement(s) && s.declarationList.declarations.some(d => d.name.text === wanted)));
    if (!statement) throw Error(`missing App declaration ${wanted}`);
    return statement.getText(ast);
  }).join('\n\n');
};
put('baseline.tsx', src('tools/video-editor/compositions/AudioTrack.tsx'));
put('config.ts', [
  pick('tools/video-editor/lib/time-grid.ts', ['secondsToFrames']),
  pick('tools/video-editor/lib/timeline-domain.ts', ['isFiniteNumber', 'isPositiveNumber', 'isHoldLikeClip', 'hasValidNonHoldTrim', 'getCanonicalClipPlaybackRate', 'getConfigTimelineClipSourceDuration', 'getConfigTimelineClipDuration']),
  pick('tools/video-editor/lib/config-utils.ts', ['getClipTimelineDuration', 'getSanitizedMediaTrimProps', 'getSanitizedPlaybackRate', 'getSanitizedVolume', 'getSanitizedMediaSrc', 'getClipDurationInFrames']),
].join('\n\n'));
put('player.ts', "import {getSanitizedPlaybackRate, getClipTimelineDuration} from './config';\n" + pick('tools/video-editor/compositions/playerEvaluation.ts', ['playerEvaluationClip']));
put('bounds.ts', src('tools/video-editor/lib/canonicalRenderBounds.ts'));
put('boundary.tsx', src('tools/video-editor/compositions/MediaErrorBoundary.tsx'));
put('failure.tsx', src('tools/video-editor/compositions/PreviewMediaFailureContext.tsx'));
put('setup.ts', "import '@testing-library/jest-dom/vitest';\n");
// Gateway identity is an explicit mocked host boundary in these offline tests.
put('cors.ts', "export const mediaCrossOrigin = () => undefined;\nexport const mediaFetchCredentials = () => 'same-origin';\n");
const modulesLink = `${proposal}/node_modules`;
if (!fs.existsSync(modulesLink)) fs.symlinkSync(`${fixture}/node_modules`, modulesLink);
// This Composition worktree has the same package name. Resolve the advertised
// subpath from the fixture to avoid the repository's unrelated self-reference.
const publicEvaluation = createRequire(`${fixture}/probe.mjs`).resolve('@banodoco/timeline-composition/evaluation');
const installed = JSON.parse(fs.readFileSync(`${fixture}/node_modules/@banodoco/timeline-composition/package.json`, 'utf8'));
if (installed.version !== '0.0.13' || publicEvaluation !== path.resolve(`${fixture}/node_modules/@banodoco/timeline-composition`, installed.exports['./evaluation'].import)) throw Error('public evaluation resolution mismatch');
const aliases = {
  '@/tools/video-editor/compositions/AudioTrack': process.env.PCM_BASELINE ? `${fixture}/baseline.tsx` : `${proposal}/AudioTrack.tsx`,
  '@/tools/video-editor/compositions/playerEvaluation': `${fixture}/player.ts`,
  '@/tools/video-editor/lib/config-utils': `${fixture}/config.ts`,
  '@/tools/video-editor/lib/canonicalRenderBounds': `${fixture}/bounds.ts`,
  '@/tools/video-editor/compositions/MediaErrorBoundary': `${fixture}/boundary.tsx`,
  '@/tools/video-editor/compositions/PreviewMediaFailureContext': `${fixture}/failure.tsx`,
  '@/shared/lib/media/mediaCrossOrigin': `${fixture}/cors.ts`,
  '@banodoco/timeline-composition/evaluation': publicEvaluation,
};
const alias = Object.entries(aliases).map(([key, replacement]) => ` { find: new RegExp(${JSON.stringify('^' + key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?:\\.tsx?)?$')}), replacement: ${JSON.stringify(replacement)} }`);
for (const key of ['react', 'react-dom', '@testing-library/react', '@testing-library/jest-dom', 'remotion', '@remotion/media', 'vitest']) {
  alias.push(` { find: ${JSON.stringify(key)}, replacement: ${JSON.stringify(`${fixture}/node_modules/${key}`)} }`);
}
put('vitest.config.mjs', `export default {root:${JSON.stringify(proposal)}, cacheDir:${JSON.stringify(`${worker}/cache`)}, resolve:{alias:[${alias.join(',')}]}, test:{environment:'jsdom',globals:true,setupFiles:[${JSON.stringify(`${fixture}/setup.ts`)}],include:['*.test.{ts,tsx}']}};\n`);
console.log(`App ${ref}; public13 9412ae25; ${process.env.PCM_BASELINE ? 'BASELINE' : 'PROPOSAL'} fixture ${fixture}`);
