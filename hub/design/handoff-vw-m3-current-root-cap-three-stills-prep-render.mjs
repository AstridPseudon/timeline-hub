// Central-only, normal current Agent index/Root/renderStill; no replacement component.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const orch = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const worker = 'vw-m3-current-root-cap-three-stills-prep';
const prefix = `${orch}/design/handoff-${worker}-`;
const own = `${orch}/workers/${worker}`;
const graph = '/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules';
const stage = process.argv[2];
const root = `${stage}/agent/remotion`;
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const check = (condition, message) => {if (!condition) throw new Error(message);};
const service = process.env.CURRENT_CAP_SERVICE_RESULT;
check(typeof service === 'string' && path.dirname(service) === `${orch}/tests`, 'central-only renderer');
check(fs.readFileSync(`${service}/status`, 'utf8').trim() === 'running', 'service inactive');
const request = fs.readFileSync(`${service}/request`, 'utf8').split('\n');
check(request.includes(`target=${worker}`) && request.includes('suite=e2e-viewing-current-root-cap-three-stills'), 'wrong request');
check(path.dirname(stage) === '/tmp' && path.basename(stage).startsWith('vw-cap-')
  && fs.realpathSync(stage) === stage && (fs.statSync(stage).mode & 0o777) === 0o700, 'unowned short temp');
const manifest = read(`${prefix}manifest.json`);
const suite = `composition e2e-viewing-current-root-cap-three-stills /home/user/work/venv-agent/bin/python ${prefix}controller.py capture`;
const approved = [suite, `controller_sha256=${sha(`${prefix}controller.py`)}`, `manifest_sha256=${sha(`${prefix}manifest.json`)}`];
check(fs.readFileSync(`${prefix}CAPTURE-GRANT.txt`, 'utf8').trim().split(/\r?\n/).join('\n') === approved.join('\n'), 'exact manager grant required');
for (const [name, hash] of Object.entries(manifest.scripts)) check(sha(`${prefix}${name}`) === hash, `script changed: ${name}`);
for (const [file, hash] of Object.entries(manifest.inputs)) check(sha(file) === hash, `input changed: ${file}`);
for (const [name, hash] of Object.entries({...manifest.observed.source_files, ...manifest.observed.generated})) {
  check(sha(`${stage}/agent/${name}`) === hash, `current Agent source changed: ${name}`);
}
for (const [name, hash] of Object.entries(manifest.observed.public12_members)) {
  check(sha(`${root}/node_modules/@banodoco/timeline-composition/${name}`) === hash, `public12 changed: ${name}`);
}
for (const [name, hash] of Object.entries(manifest.observed.replay)) check(sha(`${stage}/replayed/${name}`) === hash, `replay changed: ${name}`);
for (const [name, hash] of Object.entries(manifest.graph.six_peers)) check(sha(`${graph}/${name}`) === hash, `peer changed: ${name}`);
const guard = () => {
  for (const file of [`${orch}/QUIET.md`, `${orch}/managers/viewing/QUIET.md`]) check(!fs.existsSync(file), 'QUIET active');
  const stat = fs.statfsSync(own, {bigint: true});
  check(stat.bavail * stat.bsize >= 10n * 1024n ** 3n, '10 GiB floor');
};
guard();
const peer = createRequire(`${graph}/@remotion/renderer/package.json`);
const {bundle} = peer(`${graph}/@remotion/bundler`);
const {openBrowser, selectComposition, renderStill} = peer(`${graph}/@remotion/renderer`);
const {remotionPrimitiveAliasesFor} = await import(pathToFileURL(`${root}/webpack-alias.mjs`).href);
const originalAliases = remotionPrimitiveAliasesFor(root);
const inputProps = read(`${stage}/replayed/props.json`);
const browserExecutable = '/opt/google/chrome/chrome';
const watchdog = setInterval(guard, 500);
let browser;
try {
  const serveUrl = await bundle({entryPoint: `${root}/src/index.ts`, rootDir: root,
    publicDir: `${root}/public`, outDir: `${stage}/bundle`, symlinkPublicDir: false, enableCaching: false,
    webpackOverride: (configuration) => {
      const configured = originalAliases(configuration);
      configured.resolve.modules = [`${root}/node_modules`, ...(configured.resolve.modules ?? [])];
      return configured;
    }});
  guard();
  browser = await openBrowser('chrome', {browserExecutable, chromeMode: 'chrome-for-testing',
    logLevel: 'error', chromiumOptions: {gl: 'swiftshader'}});
  const common = {serveUrl, inputProps, puppeteerInstance: browser, browserExecutable,
    chromeMode: 'chrome-for-testing', chromiumOptions: {gl: 'swiftshader'}, logLevel: 'error',
    timeoutInMilliseconds: 120000};
  const composition = await selectComposition({...common, id: 'TimelineComposition'});
  const metadata = Object.fromEntries(['id', 'width', 'height', 'fps', 'durationInFrames'].map((k) => [k, composition[k]]));
  fs.writeFileSync(`${prefix}metadata.json`, JSON.stringify({...metadata,
    claim: 'UNCERTIFIED static compiled current Agent Root reference'}, null, 2) + '\n', {flag: 'wx'});
  check(metadata.width === 1920 && metadata.height === 1080 && metadata.fps === 30
    && metadata.durationInFrames === 120, 'unexpected actual metadata');
  for (const frame of [90, 105, 119]) {
    guard();
    const output = `${prefix}frame-${frame}.png`;
    check(!fs.existsSync(output), 'refuse PNG replacement');
    await renderStill({...common, composition, frame, output, imageFormat: 'png', overwrite: false, scale: 1});
    console.log(JSON.stringify({frame, sha256: sha(output), bytes: fs.statSync(output).size}));
  }
} finally {
  if (browser) await browser.close({silent: true});
  clearInterval(watchdog);
}
guard();
