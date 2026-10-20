import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { assertSourceVersionsUnchanged, verifyFileGraph } from './harness';
import { mediaHash } from './media';
import { playerBrowserProfile } from './browser-profile';

async function fixture(files: Record<string, string>): Promise<string> {
  const root = await mkdtemp(join(tmpdir(), 'viewing-parity-graph-'));
  await Promise.all(Object.entries(files).map(async ([path, contents]) => {
    const absolute = join(root, path);
    await mkdir(join(absolute, '..'), { recursive: true });
    await writeFile(absolute, contents);
  }));
  return root;
}

test('verifies independent consumer graphs against frozen file bytes', async () => {
  const app = await fixture({ 'remotion/player.js': 'app-player', 'remotion/audio.js': 'app-audio' });
  const agent = await fixture({ 'remotion/player.js': 'agent-player', 'remotion/audio.js': 'agent-audio' });
  try {
    const appExpected = {
      'remotion/player.js': mediaHash(Buffer.from('app-player')),
      'remotion/audio.js': mediaHash(Buffer.from('app-audio')),
    };
    const agentExpected = {
      'remotion/player.js': mediaHash(Buffer.from('agent-player')),
      'remotion/audio.js': mediaHash(Buffer.from('agent-audio')),
    };
    assert.deepEqual(await verifyFileGraph(app, appExpected, 'App', { exact: true }), appExpected);
    assert.deepEqual(await verifyFileGraph(agent, agentExpected, 'Agent', { exact: true }), agentExpected);
  } finally {
    await Promise.all([rm(app, { recursive: true, force: true }), rm(agent, { recursive: true, force: true })]);
  }
});

test('fails closed when a frozen target is missing', async () => {
  const root = await fixture({ 'remotion/player.js': 'player' });
  try {
    await assert.rejects(
      verifyFileGraph(root, {
        'remotion/player.js': mediaHash(Buffer.from('player')),
        'remotion/audio.js': mediaHash(Buffer.from('audio')),
      }, 'Agent'),
      /Agent: missing or non-regular target remotion\/audio\.js/,
    );
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('fails closed when installed bytes or the exact package set changes', async () => {
  const root = await fixture({ 'remotion/player.js': 'changed', 'remotion/extra.js': 'unexpected' });
  try {
    await assert.rejects(
      verifyFileGraph(root, { 'remotion/player.js': mediaHash(Buffer.from('original')) }, 'App', { exact: true }),
      /App: installed file set differs/,
    );
    await rm(join(root, 'remotion/extra.js'));
    await assert.rejects(
      verifyFileGraph(root, { 'remotion/player.js': mediaHash(Buffer.from('original')) }, 'App'),
      /App: remotion\/player\.js has .* expected/,
    );
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('fails postflight when a declared dependency graph changes', () => {
  const before = {
    compositionFiles: { app: { 'package/index.js': 'sha256:composition' } },
    renderGraphHashes: { app: { 'node_modules/remotion.js': 'sha256:app' } },
    playerBrowser: playerBrowserProfile(),
    exportBrowserHash: 'sha256:export',
  } as const;
  assertSourceVersionsUnchanged(before, before);
  assert.throws(
    () => assertSourceVersionsUnchanged(before, {
      ...before,
      renderGraphHashes: { app: { 'node_modules/remotion.js': 'sha256:changed' } },
    }),
    /source dependency graph changed during browser fixture: renderGraphHashes/,
  );
});

test('fails postflight when the selected browser profile or executable bytes change', () => {
  const before = {
    compositionFiles: {}, renderGraphHashes: {}, playerBrowser: playerBrowserProfile(), exportBrowserHash: 'export',
  };
  for (const after of [
    { ...before, playerBrowser: playerBrowserProfile('native-codec-chrome155') },
    { ...before, playerBrowser: { ...before.playerBrowser, sha256: 'changed' } },
    { ...before, exportBrowserHash: 'changed' },
  ]) {
    assert.throws(() => assertSourceVersionsUnchanged(before, after), /source dependency graph changed/);
  }
});
