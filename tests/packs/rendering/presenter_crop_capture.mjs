// Central-only: four real stills of the same registered presenter used by SSR.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import {basis, defaultParams, defaultPropsFor, eraseRegion, params, prepareRoot, propsFor, seriesInspection} from './presenter_crop_geometry.mjs';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';

assert.equal(process.env.VIEWING_CROP_CENTRAL, '1');
const browserExecutable = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const output = process.argv[2];
assert.ok(path.isAbsolute(output));
const mode = process.argv[3] ?? 'explicit';
assert.ok(mode === 'explicit' || mode === 'default');
const frames = [0, 3, 4, 5];
const props = mode === 'default' ? defaultPropsFor() : propsFor(params);
if (mode === 'default') {
  assert.deepEqual(props.timeline.clips[0].params, defaultParams);
  assert.equal(Object.hasOwn(props.timeline.clips[0].params, 'mouth'), false);
}
// Fixed component-zero ROI, retained for every PNG. No per-PNG ROI query.
const scene = prepareRoot(props, basis, {});
const zero = seriesInspection(scene, props);
assert.equal(zero.frame, 0);
if (mode === 'explicit') {
  assert.deepEqual(props.timeline.clips[0].params, {mouth: {x: 151, y: 104, w: 19},
    words: [[.1, .4]], chrome: 'none', blinkEvery: 0, seed: 7});
}
const rows = [{...zero, erase: eraseRegion(props.timeline.clips[0].params, 0, basis.fps)}];
const buildDir = path.join(output, 'bundle');
const serveUrl = await bundle({entryPoint: path.join(process.cwd(), 'presenter_crop_entry.mjs'),
  outDir: buildDir, webpackOverride: remotionPrimitiveAliasesFor(process.cwd()),
  enableCaching: false});
let browser;
try {
  browser = await openBrowser('chrome', {browserExecutable, logLevel: 'error'});
  const composition = await selectComposition({serveUrl, id: 'presenter-crop', inputProps: props,
    puppeteerInstance: browser, browserExecutable, logLevel: 'error'});
  assert.deepEqual([composition.width, composition.height, composition.fps, composition.durationInFrames],
    [1920, 1080, 30, 60]);
  for (const frame of frames) await renderStill({serveUrl, composition, inputProps: props,
    frame, imageFormat: 'png', output: path.join(output, `frame-${frame}.png`),
    scale: 1 / 3, puppeteerInstance: browser, browserExecutable, logLevel: 'error'});
  fs.writeFileSync(path.join(output, 'inspection.json'), JSON.stringify({
    basis, frames, props, rows, size: [640, 360], scale: 1 / 3,
  }));
} finally {
  if (browser) await browser.close({silent: true});
  fs.rmSync(buildDir, {recursive: true, force: true});
}
