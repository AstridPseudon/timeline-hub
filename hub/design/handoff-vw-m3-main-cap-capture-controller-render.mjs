// Central-only use of the existing bundler/renderer. No replacement Root or evaluator.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const orch = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const worker = 'vw-m3-main-cap-capture-controller';
const own = `${orch}/workers/${worker}`;
const prefix = `${orch}/design/handoff-${worker}-`;
const fixture = `${orch}/design/handoff-vw-m3-main-image-cap-source-vector-`;
const suite = 'e2e-viewing-main6-image-cap-three-stills';
const graph = '/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules';
const browserExecutable = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const floor = 10n * 1024n ** 3n;
const stage = process.argv[2];
const check = (condition, message) => {
  if (!condition) throw new Error(message);
};
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const digest = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const realParents = (file) => {
  for (let current = file; current !== path.dirname(current); current = path.dirname(current)) {
    if (fs.existsSync(current)) check(!fs.lstatSync(current).isSymbolicLink(), `symlink parent: ${current}`);
  }
};
const guard = () => {
  for (const file of [`${orch}/QUIET.md`, `${orch}/managers/viewing/QUIET.md`]) {
    check(!fs.existsSync(file), 'QUIET active');
  }
  const stat = fs.statfsSync(own, {bigint: true});
  check(stat.bavail * stat.bsize >= floor, 'disk below required 10 GiB reserve');
};
const service = process.env.MAIN_CAP_SERVICE_RESULT;
check(typeof service === 'string' && path.dirname(service) === `${orch}/tests`, 'central-service-only renderer');
check(fs.readFileSync(`${service}/status`, 'utf8').trim() === 'running', 'central service is not running');
const request = fs.readFileSync(`${service}/request`, 'utf8').split('\n');
check(request.includes(`target=${worker}`) && request.includes(`suite=${suite}`), 'wrong central request');
const suiteLine = `agent ${suite} /home/user/work/venv-agent/bin/python ${prefix}controller.py capture`;
check(fs.readFileSync(`${own}/CAPTURE-GRANT.txt`, 'utf8').trim() === suiteLine, 'manager grant differs');
check(fs.readFileSync(`${orch}/tests/suites.conf`, 'utf8').split('\n').filter((line) => line === suiteLine).length === 1,
  'manager suite absent/different/duplicated');
check(stage === `${own}/capture-stage`, 'unowned stage');
realParents(stage);
guard();
const root = `${stage}/main/remotion`;
const prepared = read(`${prefix}preflight.json`);
for (const [name, hash] of Object.entries(prepared.source.source_files)) {
  const file = `${stage}/main/${name}`;
  realParents(file);
  check(digest(file) === hash, `staged source changed: ${name}`);
}
for (const [name, hash] of Object.entries(prepared.source.seven_expected_output_hashes)) {
  check(digest(`${stage}/replayed-${name}`) === hash, `raw closure replay changed: ${name}`);
  check(digest(`${fixture}${name}`) === hash, `fixture changed: ${name}`);
}
for (const [name, hash] of Object.entries(prepared.graph_before.six_peer_hashes)) {
  check(digest(`${graph}/${name}`) === hash, `peer changed: ${name}`);
}
const inputProps = read(`${stage}/replayed-main-props-static-analog.json`);
check(inputProps.assets.assets['image-occurrence:image'].file === 'image-cap.png', 'wrong static-public analog');
check(digest(`${root}/public/image-cap.png`) === digest(`${fixture}image.png`), 'wrong public image');
const requirePeer = createRequire(`${graph}/@remotion/renderer/package.json`);
const {bundle} = requirePeer(`${graph}/@remotion/bundler`);
const {openBrowser, selectComposition, renderStill} = requirePeer(`${graph}/@remotion/renderer`);
const {remotionPrimitiveAliasesFor} = await import(pathToFileURL(`${root}/webpack-alias.mjs`).href);
const aliases = remotionPrimitiveAliasesFor(root);
const cache = `${root}/node_modules/.cache/webpack`;
realParents(cache);
check(fs.statSync(cache).isDirectory(), 'private webpack cache missing');
const watchdog = setInterval(guard, 500);
let browser;
try {
  const serveUrl = await bundle({
    entryPoint: `${root}/src/index.ts`,
    rootDir: root,
    publicDir: `${root}/public`,
    outDir: `${stage}/bundle`,
    enableCaching: true,
    symlinkPublicDir: false,
    // Webpack's cache is rooted at this private project/node_modules/.cache.
    // MAIN's original alias function and original generated registries are retained.
    webpackOverride: (configuration) => {
      const configured = aliases(configuration);
      configured.resolve.modules = [`${root}/node_modules`, ...(configured.resolve.modules ?? [])];
      return configured;
    },
  });
  guard();
  browser = await openBrowser('chrome', {
    browserExecutable,
    chromeMode: 'headless-shell',
    logLevel: 'error',
    chromiumOptions: {gl: 'swiftshader'},
  });
  const common = {
    serveUrl, inputProps, puppeteerInstance: browser, browserExecutable,
    chromeMode: 'headless-shell', chromiumOptions: {gl: 'swiftshader'},
    logLevel: 'error', timeoutInMilliseconds: 120000,
    onBrowserLog: (entry) => console.log(JSON.stringify({browserLog: entry})),
  };
  const composition = await selectComposition({...common, id: 'TimelineComposition'});
  const metadata = Object.fromEntries(['id', 'width', 'height', 'fps', 'durationInFrames']
    .map((name) => [name, composition[name]]));
  fs.writeFileSync(`${prefix}metadata.json`, `${JSON.stringify({
    ...metadata, binding: 'static-public executable analog; original MAIN Root',
  }, null, 2)}\n`, {flag: 'wx'});
  check(metadata.width === 1920 && metadata.height === 1080 && metadata.fps === 30
    && metadata.durationInFrames === 120, `unexpected original MAIN metadata: ${JSON.stringify(metadata)}`);
  for (const frame of [90, 105, 119]) {
    guard();
    check(frame >= 0 && frame < composition.durationInFrames, 'invalid excluded-end frame');
    const output = `${prefix}frame-${frame}.png`;
    realParents(output);
    check(!fs.existsSync(output), `refusing PNG replacement: ${output}`);
    await renderStill({...common, composition, frame, output, imageFormat: 'png', overwrite: false, scale: 1});
    console.log(JSON.stringify({frame, png_sha256: digest(output), bytes: fs.statSync(output).size}));
  }
} finally {
  if (browser) await browser.close({silent: true});
  clearInterval(watchdog);
}
guard();
