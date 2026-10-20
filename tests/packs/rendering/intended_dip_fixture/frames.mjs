// One central browser, two actual bundles, all 45 frames each. No source swap.
import assert from 'node:assert/strict';
import path from 'node:path';
import {readFileSync, writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import {exposeDeclaredImages} from './bundle-assets.mjs';

assert.equal(process.env.VIEWING_INTENDED_DIP_CENTRAL, '1', 'central grant required');
const browserExecutable = process.env.ASTRID_REMOTION_BROWSER_EXECUTABLE;
assert.ok(browserExecutable, 'existing browser required');
const projects = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const bundles = [];
for (const project of projects) {
  const {remotionPrimitiveAliasesFor} = await import(pathToFileURL(path.join(project, 'webpack-alias.mjs')).href);
  bundles.push(await bundle({entryPoint: path.join(project, 'src/index.ts'), rootDir: project,
    publicDir: path.join(project, 'public'), outDir: path.join(project, 'frame-bundle'),
    enableCaching: false, webpackOverride: remotionPrimitiveAliasesFor(project)}));
  exposeDeclaredImages(bundles.at(-1));
}
const browser = await openBrowser('chrome', {browserExecutable,
  chromiumOptions: {gl: 'swangle'},
  onBrowserDownload: () => {throw new Error('browser download forbidden');}});
const observations = [];
try {
  for (let index = 0; index < projects.length; index++) {
    const project = projects[index];
    const inputProps = JSON.parse(readFileSync(path.join(project, 'props.json'), 'utf8'));
    const errors = [];
    const onBrowserLog = entry => {if (entry.type === 'error') errors.push(entry.text);};
    const composition = await selectComposition({serveUrl: bundles[index], id: 'TimelineComposition',
      inputProps, puppeteerInstance: browser, onBrowserLog});
    assert.deepEqual([composition.width, composition.height, composition.fps, composition.durationInFrames],
      [1920, 1080, 30, 45]);
    const frames = [];
    for (let frame = 0; frame < 45; frame++) {
      await renderStill({serveUrl: bundles[index], composition, inputProps,
        puppeteerInstance: browser, frame, imageFormat: 'png',
        output: path.join(project, `frame-${frame}.png`), onBrowserLog,
        chromiumOptions: {gl: 'swangle'},
        onDownload: () => {throw new Error('unexpected remote media download');}});
      frames.push(frame);
    }
    observations.push({compositionId: composition.id, inputProps, frames, errors});
    assert.deepEqual(errors, []);
  }
} finally {
  await browser.close({silent: true});
  writeFileSync(process.argv[3], JSON.stringify(observations));
}
