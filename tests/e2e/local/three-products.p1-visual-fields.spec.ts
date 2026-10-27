import { test, expect } from '@playwright/test';
import { createServer } from 'vite';
import { createRequire } from 'node:module';
import { mkdir, writeFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { join } from 'node:path';

// The real preview and installed export are sampled at the same frames. All
// files and the Vite cache live in Playwright's private result directory.
test('visual fields draw in preview and installed export', async ({ page }, testInfo) => {
  test.setTimeout(300_000);
  const root = process.cwd();
  const dir = testInfo.outputPath('visual-fields');
  await mkdir(dir, { recursive: true });
  const peers = '/home/user/work/runtimes/agent-remotion-0013/node_modules';
  const require = createRequire(join(peers, '../package.json'));
  const { bundle } = require('@remotion/bundler');
  const { renderStill, selectComposition } = require('@remotion/renderer');
  const appImport = (path: string) => JSON.stringify(join(root, path));
  await writeFile(join(dir, 'index.html'), '<html><body style="margin:0"><div id="player"></div><script type="module" src="./preview.tsx"></script></body></html>');
  await writeFile(join(dir, 'preview.tsx'), `
import React, {createRef} from 'react';
import {createRoot} from 'react-dom/client';
import {Player} from '@remotion/player';
import {TimelineRenderer} from ${appImport('src/tools/video-editor/compositions/TimelineRenderer.tsx')};
import {INSTALLED_ASTRID_ELEMENT_HOST} from ${appImport('src/tools/video-editor/runtime/astrid-element-components.tsx')};
import {resolveTimelineConfig} from ${appImport('src/tools/video-editor/lib/config-utils.ts')};
const root = createRoot(document.getElementById('player'));
window.drawFixture = async config => {
  const resolved = await resolveTimelineConfig(config, config.registry, async file => file);
  const ref = createRef();
  const Component = () => <TimelineRenderer config={resolved} astridElementHost={INSTALLED_ASTRID_ELEMENT_HOST}/>;
  root.render(<Player ref={ref} component={Component} inputProps={{}} durationInFrames={60} fps={30}
    compositionWidth={160} compositionHeight={90} controls={false} style={{width:160,height:90}}/>);
  for (let i=0; !ref.current && i<100; i++) await new Promise(r=>setTimeout(r, 20));
  if (!ref.current) throw Error('Player did not mount');
  window.seekFixture = async frame => {
    ref.current.seekTo(frame);
    await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
    await Promise.all([...document.querySelectorAll('img')].map(img=>img.decode()));
    return ref.current.getCurrentFrame();
  };
};
window.fixtureReady = true;
`);
  await writeFile(join(dir, 'export.tsx'), `
import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {TimelineComposition, compileCanonicalTransitions, DEFAULT_THEME, toRuntimeTheme} from '@banodoco/timeline-composition';
const Draw = props => {
  const tracks = props.timeline.tracks.filter(t => t.type === 'video').map(track => ({track, clips: props.timeline.clips.filter(c => c.track === track.id)}));
  const compiledTransitions = compileCanonicalTransitions(tracks, 30, toRuntimeTheme(DEFAULT_THEME));
  return <TimelineComposition {...props} compiledTransitions={compiledTransitions}/>;
};
registerRoot(() => <Composition id="Fields" component={Draw} durationInFrames={60} fps={30} width={160} height={90} defaultProps={{timeline:{tracks:[],clips:[]},assets:{}}}/>);
`);
  const server = await createServer({
    configFile: join(root, 'config/vite/vite.config.ts'), cacheDir: join(dir, 'vite-cache'),
    server: { host: '127.0.0.1', port: 0, fs: { allow: [root, dir] } },
    plugins: [{ name: 'visual-field-solid', configureServer(vite) {
      vite.middlewares.use('/solid.svg', (req, res) => {
        res.setHeader('Content-Type', 'image/svg+xml');
        const color = req.url?.includes('second') ? '#3080d0' : '#e85030';
        res.end(`<svg xmlns="http://www.w3.org/2000/svg" width="160" height="90"><rect width="160" height="90" fill="${color}"/></svg>`);
      });
    } }],
  });
  let serveUrl: string;
  try {
    await server.listen();
    const address = server.httpServer!.address();
    if (!address || typeof address === 'string') throw new Error('Vite did not bind');
    const origin = `http://127.0.0.1:${address.port}`;
    await page.setViewportSize({ width: 160, height: 90 });
    await page.goto(`${origin}/@fs${dir}/index.html`);
    await page.waitForFunction(() => (window as any).fixtureReady);
    serveUrl = await bundle({ entryPoint: join(dir, 'export.tsx'), enableCaching: false,
      webpackOverride: (config: any) => ({ ...config, resolve: { ...config.resolve, alias: { ...config.resolve?.alias,
        react: join(root, 'node_modules/react'), 'react-dom': join(root, 'node_modules/react-dom'),
        remotion: join(root, 'node_modules/remotion'),
        '@banodoco/timeline-composition': join(root, 'node_modules/@banodoco/timeline-composition'),
      } } }),
    });
    const browserExecutable = process.env.ASTRID_REMOTION_BROWSER_EXECUTABLE;
    const composition = await selectComposition({ serveUrl, id: 'Fields', browserExecutable });
    const cases = [
      ['fade-exit', 'exit', { id: 'fade', durationFrames: 8 }, [20, 25, 29]],
      ['slide-up-exit', 'exit', { type: 'slide-up', duration: 8 / 30 }, [20, 25, 29]],
      ['fade-entrance-step', 'entrance', { id: 'fade', durationFrames: 8, easing: 'step' }, [0, 4, 9]],
      ['fade-up-entrance', 'entrance', { type: 'fade-up', duration: 8 / 30, params: { easing: 'ease-in' } }, [0, 4, 9]],
      ['scale-in-entrance', 'entrance', { id: 'scale-in' }, [0, 4, 9]],
      ['fade-transition', 'transition', { id: 'fade', durationFrames: 8 }, [21, 25, 30]],
      ['fade-transition-default', 'transition', { id: 'fade' }, [21, 25, 30]],
      ['cross-fade-transition-explicit', 'transition', { id: 'cross-fade', durationFrames: 8 }, [21, 25, 30]],
      ['cross-fade-transition', 'transition', { type: 'crossfade' }, [21, 25, 30]],
      ['effects-object', 'effects', { fade_in: 8 / 30 }, [0, 4, 9]],
      ['effects-array', 'effects', [{ fade_in: 8 / 30 }], [0, 4, 9]],
    ] as const;
    const captures: object[] = [];
    for (const [name, field, reference, frames] of cases) {
      const track = { id: 'picture', type: 'video', fit: 'contain' };
      const clips = [
        { id: 'first', track: 'picture', clipType: 'media', at: 0, hold: 1, asset: 'solid', ...(field !== 'transition' ? { [field]: reference } : {}) },
        { id: 'second', track: 'picture', clipType: 'media', at: 1, hold: 1, asset: 'second', ...(field === 'transition' ? { transition: reference } : {}) },
      ];
      const config = { output: { resolution: '160x90', fps: 30, file: 'fixture.mp4' }, tracks: [track], clips,
        registry: { assets: { solid: { file: `${origin}/solid.svg`, type: 'image/svg+xml' },
          second: { file: `${origin}/solid.svg?second`, type: 'image/svg+xml' } } } };
      const baseline = { ...config, clips: clips.map(clip => {
        const copy = { ...clip } as Record<string, unknown>;
        delete copy[field];
        return copy;
      }) };
      await page.evaluate(async value => (window as any).drawFixture(value), baseline);
      await page.evaluate(async f => (window as any).seekFixture(f), frames[1]);
      const baselinePath = join(dir, `${name}-baseline.png`);
      await page.locator('#player').screenshot({ path: baselinePath });
      await page.evaluate(async config => (window as any).drawFixture(config), config);
      for (const frame of frames) {
        expect(await page.evaluate(async f => (window as any).seekFixture(f), frame)).toBe(frame);
        const preview = join(dir, `${name}-${frame}-preview.png`);
        const exported = join(dir, `${name}-${frame}-export.png`);
        await page.locator('#player').screenshot({ path: preview });
        await renderStill({ composition, serveUrl, browserExecutable, frame, output: exported, imageFormat: 'png',
          inputProps: { timeline: config, assets: config.registry } });
        const rgb = (path: string) => execFileSync('ffmpeg', ['-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']);
        const left = rgb(preview), right = rgb(exported);
        expect(left.length).toBe(right.length);
        if (frame === frames[1]) expect(left.equals(rgb(baselinePath)), `${name} must change the drawing`).toBe(false);
        let max = 0, total = 0;
        for (let i = 0; i < left.length; i++) { const delta = Math.abs(left[i] - right[i]); max = Math.max(max, delta); total += delta; }
        captures.push({ name, frame, max, mean: total / left.length });
      }
    }
    await writeFile(join(dir, 'manifest.json'), JSON.stringify(captures, null, 2));
    expect(captures.every((item: any) => item.max <= 2 && item.mean <= 0.25)).toBe(true);
  } finally {
    await server.close();
  }
});
