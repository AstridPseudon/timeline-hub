import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {mkdir, writeFile} from 'node:fs/promises';
import {join} from 'node:path';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';

const root = process.cwd() + '/remotion';
const output = process.env.RENDERLANE_OUTPUT;
const browserExecutable = process.env.ASTRID_REMOTION_BROWSER_EXECUTABLE;
await mkdir(output, {recursive: true});
const inputProps = {
  timeline: {
    theme: 'banodoco-default',
    theme_overrides: {visual: {canvas: {width: 160, height: 90, fps: 10}}},
    tracks: [{id: 'v1', kind: 'visual', label: 'Title'}],
    clips: [{id: 'title', track: 'v1', at: 0, hold: 0.6, clipType: 'text',
      text: {content: 'Central render proof', fontSize: 20, color: '#ffffff'}}],
  },
  assets: {assets: {}},
};
const serveUrl = await bundle({entryPoint: join(root, 'src/index.ts'), enableCaching: false,
  webpackOverride: remotionPrimitiveAliasesFor(root)});
const composition = await selectComposition({serveUrl, id: 'TimelineComposition', inputProps, browserExecutable});
console.log('Agent native Remotion browser launched: ' + composition.id);
await renderStill({serveUrl, composition, inputProps, browserExecutable,
  output: join(output, 'frame.png'), frame: 1, imageFormat: 'png'});
await renderMedia({serveUrl, composition, inputProps, browserExecutable,
  outputLocation: join(output, 'video.mp4'), codec: 'h264', concurrency: 1});
await writeFile(join(output, 'props.json'), JSON.stringify(inputProps, null, 2));
console.log('Agent native Remotion MP4 + still: 1 passed (environment smoke; host acceptance follows)');
