import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {mkdir, writeFile, symlink, readFile, realpath} from 'node:fs/promises';
import {join, resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
import {createServer} from 'vite';
import {chromium} from 'playwright';

const root = process.cwd();
const harness = join(root, '.renderlane');
const output = process.env.RENDERLANE_OUTPUT;
const browserExecutable = process.env.ASTRID_REMOTION_BROWSER_EXECUTABLE;
const peers = '/home/user/work/runtimes/agent-remotion-0013/node_modules';
const require = createRequire(join(peers, '../package.json'));
const {bundle} = require('@remotion/bundler');
const {renderStill, selectComposition} = require('@remotion/renderer');
await mkdir(output, {recursive: true});
assert.equal(await realpath(join(root, 'node_modules')), join(root, 'node_modules'));
for (const name of ['bundler', 'renderer']) {
  await symlink(join(peers, '@remotion', name), join(root, 'node_modules/@remotion', name));
}
await writeFile(join(harness, 'index.html'), '<html><head><style>#player [style*="background-color"]{background-color:#050814!important}</style></head><body style="margin:0"><div id="player" style="width:640px;height:360px"></div><script type="module" src="./preview.tsx"></script></body></html>');
let config;
await writeFile(join(harness, 'preview.tsx'), `
import React, {createRef} from 'react';
import {createRoot} from 'react-dom/client';
import {Player} from '@remotion/player';
import {TimelineRenderer} from '../src/tools/video-editor/compositions/TimelineRenderer.tsx';
import {INSTALLED_ASTRID_ELEMENT_HOST} from '../src/tools/video-editor/runtime/astrid-element-components.tsx';
import {resolveTimelineConfig} from '../src/tools/video-editor/lib/config-utils.ts';
import fixture from '../src/tools/video-editor/data/shotComposition.fixture.json';
import {createShotCompositionAdapter} from '../src/tools/video-editor/data/shotCompositionAdapter.ts';
import {projectCanonicalComposition} from '../src/tools/video-editor/data/shotCompositionProjection.ts';
const standin = structuredClone(fixture);
standin.occurrences = [standin.occurrences[3], standin.occurrences[4]].map((occurrence, index) => ({
  ...occurrence,
  at_ms: 23867 + index * 2500, duration_ms: 2500,
}));
const prepared = createShotCompositionAdapter({load: async () => standin}).prepare(standin);
const projected = projectCanonicalComposition(prepared, {
  output: {resolution: '640x360', fps: 30, file: 'standin.mp4'},
  tracks: [
    {id: 'picture', kind: 'visual', app: {group: {id: 'occ-first', sourceTrack: 'picture'}}},
    {id: 'type', kind: 'visual'},
    {id: 'audio', kind: 'audio'},
  ],
  clips: [{id: 'loose-still', clipType: 'media', track: 'type', at: 23.867, hold: 5, asset: 'lower-still'}],
  registry: {assets: {}},
}).config;
if (!projected.clips.filter(clip => clip.id.startsWith('occ-')).every(clip => clip.app?.canonicalTiming)) {
  throw Error('App canonical projection omitted canonicalTiming on a shot clip');
}
const imageFiles = ['intro-1.jpg', 'intro-3.jpg', 'intro-5.jpg', 'intro-2.jpg', 'intro-4.jpg'];
const assets = {};
const clips = projected.clips.map((clip, index) => {
  const asset = 'standin-' + index;
  assets[asset] = {file: imageFiles[index], type: 'image/jpeg'};
  return {...clip, asset, assetEntry: undefined};
});
const config = {...projected, clips, registry: {assets}};
window.projectedConfig = config;
const resolved = await resolveTimelineConfig(config, config.registry, async file => new URL('/'+file, location.origin).href);
const ref = createRef();
const Component = () => <TimelineRenderer config={resolved} astridElementHost={INSTALLED_ASTRID_ELEMENT_HOST}/>;
createRoot(document.getElementById('player')).render(<Player ref={ref} component={Component} inputProps={{}}
  durationInFrames={870} fps={30} compositionWidth={640} compositionHeight={360} controls={false}
  style={{width:640,height:360,backgroundColor:'#050814'}}/>);
window.seekStandin = async frame => {
  if (!ref.current) throw Error('Player is not mounted');
  ref.current.seekTo(frame);
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  await Promise.all([...document.querySelectorAll('img')].map(img=>img.decode()));
  return ref.current.getCurrentFrame();
};
window.standinReady = true;
`);
await writeFile(join(harness, 'export.tsx'), `
import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {TimelineComposition} from '@banodoco/timeline-composition';
import config from './config.json';
const Root=()=> <Composition id="StandinTimeline" component={TimelineComposition}
  durationInFrames={870} fps={30} width={640} height={360}
  defaultProps={{timeline:config,assets:config.registry}}/>;
registerRoot(Root);
`);
let server;
let browser;
try {
  server = await createServer({
    configFile: join(root, 'config/vite/vite.config.ts'),
    cacheDir: join(harness, 'vite-cache'),
    optimizeDeps: {entries: [join(harness, 'index.html')]},
    server: {host: '127.0.0.1', port: 0},
  });
  await server.listen();
  const address = server.httpServer.address();
  const url = 'http://127.0.0.1:' + address.port + '/.renderlane/index.html';
  console.log('Vite listening: ' + url);
  browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE});
  console.log('preview browser launched: ' + browser.version());
  const page = await browser.newPage({viewport: {width: 640, height: 360}, deviceScaleFactor: 1});
  const errors = [];
  page.on('pageerror', e => {errors.push(e.message); console.error('preview pageerror: ' + e.message)});
  await page.goto(url);
  await page.waitForFunction(() => window.standinReady === true, undefined, {timeout: 120000});
  config = await page.evaluate(() => window.projectedConfig);
  await writeFile(join(harness, 'config.json'), JSON.stringify(config));
  await writeFile(join(output, 'config.json'), JSON.stringify(config, null, 2));
  const serveUrl = await bundle({
    entryPoint: join(harness, 'export.tsx'), publicDir: join(root, 'public'), enableCaching: false,
    webpackOverride: config => ({...config, resolve: {...config.resolve, alias: {...config.resolve?.alias,
      'react': join(root, 'node_modules/react'), 'react-dom': join(root, 'node_modules/react-dom'),
      'remotion': join(root, 'node_modules/remotion'),
      '@banodoco/timeline-composition': join(root, 'node_modules/@banodoco/timeline-composition'),
    }}}),
  });
  const composition = await selectComposition({serveUrl, id: 'StandinTimeline', browserExecutable});
  console.log('Remotion browser launched; composition=' + composition.id);
  const captures = [];
  // Include both transparent windows as well as all five requested stills.
  for (const seconds of [23.9, 24.5, 25, 26, 27.5, 28.7, 28.8]) {
    const frame = Math.round(seconds * 30);
    assert.equal(await page.evaluate(f => window.seekStandin(f), frame), frame);
    const preview = join(output, 'preview-' + frame + '.png');
    const exported = join(output, 'export-' + frame + '.png');
    await page.locator('#player').screenshot({path: preview});
    await renderStill({composition, serveUrl, browserExecutable, frame, output: exported, imageFormat: 'png'});
    const rgb = path => execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], {maxBuffer: 4000000});
    const left = rgb(preview), right = rgb(exported);
    assert.equal(left.length, 640 * 360 * 3); assert.equal(right.length, left.length);
    let max = 0, total = 0, different = 0;
    for (let i = 0; i < left.length; i++) {const d = Math.abs(left[i]-right[i]); max = Math.max(max, d); total += d; if (d) different++;}
    const item = {seconds, frame, preview, exported, maxChannelDelta: max, meanChannelDelta: total/left.length, differingChannels: different};
    captures.push(item);
    console.log(JSON.stringify(item));
  }
  const manifest = {statement: "proof on a stand-in, not the owner's film", captures, errors,
    composition: JSON.parse(await readFile(join(root, 'node_modules/@banodoco/timeline-composition/package.json'))).version};
  await writeFile(join(output, 'manifest.json'), JSON.stringify(manifest, null, 2));
  assert.deepEqual(errors, []);
  assert(captures.every(c => c.maxChannelDelta <= 2 && c.meanChannelDelta <= 0.25), 'preview/export pixel parity failed; see captures/manifest.json');
  console.log('7 passed: real Vite preview / Remotion export still pairs');
} finally {
  if (browser) await browser.close();
  if (server) await server.close();
}
