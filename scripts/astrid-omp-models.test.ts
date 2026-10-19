import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, chmodSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { getAstridOmpModelCatalog, OmpModelSelectionError, projectSafeOmpUsage, setAstridOmpDefaultModel } from './astrid-omp-models.ts';

function fakeOmp(directory: string): string {
  const packageRoot = join(directory, 'node_modules', '@oh-my-pi', 'pi-coding-agent');
  const executable = join(packageRoot, 'dist', 'cli.js');
  mkdirSync(join(packageRoot, 'dist'), { recursive: true });
  const script = `#!/usr/bin/env node
const fs = require('node:fs');
const args = process.argv.slice(2).filter(arg => !arg.startsWith('--profile='));
if (args[0] === 'models' && args[1] === 'ls') {
  process.stdout.write(JSON.stringify({models:[{provider:'openai',id:'gpt-4.1',selector:'openai/gpt-4.1',name:'GPT 4.1'}]}));
} else if (args[0] === 'config' && args[1] === 'get') {
  process.stdout.write(JSON.stringify({key:'modelRoles',value:{default:'openai/gpt-4.1',smol:'openai/gpt-4.1-mini',slow:'anthropic/claude-opus'}}));
} else if (args[0] === 'config' && args[1] === 'set') {
  fs.writeFileSync(process.env.OMP_FAKE_CONFIG_PATH, args[3]);
} else if (args[0] === 'usage') {
  if (process.env.OMP_FAKE_USAGE_FAIL) { process.stderr.write('private-account diagnostic'); process.exit(8); }
  process.stdout.write(JSON.stringify({reports:[{provider:'openai',email:'person@example.com',metadata:{accountId:'secret-account'},limits:[{id:'secret-limit-id',label:'plan detail',scope:{accountId:'secret-account'},amount:{used:12,limit:100,remaining:88,usedFraction:0.12,unit:'requests'},window:{durationMs:3600000,resetsAt:123456,status:'bad'},status:'ok'}]}],accountsWithoutUsage:[{provider:'anthropic',email:'hidden@example.com'}]}));
} else {
  process.stderr.write('credential-secret-should-never-escape');
  process.exit(7);
}
`;
  writeFileSync(executable, script, { mode: 0o755 });
  chmodSync(executable, 0o755);
  return executable;
}

function fakeBun(directory: string): string {
  const executable = join(directory, 'fake-bun');
  writeFileSync(executable, `#!/usr/bin/env node\nprocess.stdout.write(require('node:fs').readFileSync(process.env.OMP_FAKE_METADATA_PATH, 'utf8'));\n`, { mode: 0o755 });
  chmodSync(executable, 0o755);
  return executable;
}

function writeMetadata(directory: string): string {
  const metadataPath = join(directory, 'metadata.json');
  writeFileSync(metadataPath, JSON.stringify({
    providers: [
      { id: 'openai', name: 'OpenAI', models: [{ id: 'gpt-old', name: 'Old GPT' }, { id: 'gpt-4.1', name: 'Bundled GPT' }] },
      { id: 'anthropic', name: 'Anthropic', models: [{ id: 'claude-sonnet', name: 'Claude Sonnet' }] },
    ],
    loginProviders: [
      { id: 'openai-codex', name: 'ChatGPT Plus/Pro (Codex Subscription)' },
      { id: 'ollama', name: 'Ollama' },
      { id: 'openai', name: 'OpenAI' },
    ],
  }));
  return metadataPath;
}

test('OMP model catalog exposes only a safe provider/model projection', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-omp-models-'));
  try {
    const command = fakeOmp(directory);
    const bunCommand = fakeBun(directory);
    process.env.OMP_FAKE_METADATA_PATH = writeMetadata(directory);
    const catalog = await getAstridOmpModelCatalog({ command, bunCommand, cwd: directory, profile: 'work' });
    assert.deepEqual(catalog, {
      providers: [
        { id: 'anthropic', name: 'Anthropic', signedIn: true, models: [] },
        { id: 'openai-codex', name: 'ChatGPT Plus/Pro (Codex Subscription)', signedIn: false, models: [] },
        { id: 'ollama', name: 'Ollama', signedIn: false, models: [] },
        { id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-4.1', name: 'GPT 4.1' }], usage: { limits: [{ unit: 'requests', used: 12, limit: 100, remaining: 88, usedFraction: 0.12, durationMs: 3600000, resetsAt: 123456, status: 'ok' }] } },
      ],
      currentModel: 'openai/gpt-4.1',
    });
    const openai = catalog.providers.find(provider => provider.id === 'openai');
    assert.deepEqual(openai?.usage, {
      limits: [{ unit: 'requests', used: 12, limit: 100, remaining: 88, usedFraction: 0.12, durationMs: 3600000, resetsAt: 123456, status: 'ok' }],
    });
    assert.equal('usage' in catalog, false);
    const safeJson = JSON.stringify(catalog);
    for (const secret of ['credential', 'email', 'secret-account', 'secret-limit-id', 'hidden@example.com', 'plan detail']) {
      assert.equal(safeJson.includes(secret), false);
    }
  } finally {
    delete process.env.OMP_FAKE_METADATA_PATH;
    rmSync(directory, { recursive: true, force: true });
  }
});

test('usage projection rejects malformed numeric usage values and usage command errors are omitted', async () => {
  assert.throws(() => projectSafeOmpUsage({ reports: [{ provider: 'openai', limits: [{ amount: { used: 'secret-account' } }] }], accountsWithoutUsage: [] }), /unexpected shape/);
  const directory = mkdtempSync(join(tmpdir(), 'astrid-omp-usage-error-'));
  try {
    const command = fakeOmp(directory);
    const bunCommand = fakeBun(directory);
    process.env.OMP_FAKE_METADATA_PATH = writeMetadata(directory);
    process.env.OMP_FAKE_USAGE_FAIL = '1';
    const catalog = await getAstridOmpModelCatalog({ command, bunCommand, cwd: directory });
    assert.equal(catalog.providers.find(provider => provider.id === 'openai')?.usage, undefined);
  } finally {
    delete process.env.OMP_FAKE_METADATA_PATH;
    delete process.env.OMP_FAKE_USAGE_FAIL;
    rmSync(directory, { recursive: true, force: true });
  }
});

test('OMP model switch preserves other role assignments and writes the selected default selector', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-omp-models-'));
  try {
    const command = fakeOmp(directory);
    const configPath = join(directory, 'config.json');
    process.env.OMP_FAKE_CONFIG_PATH = configPath;
    const currentModel = await setAstridOmpDefaultModel({ command, cwd: directory }, 'openai/gpt-4.1');
    assert.equal(currentModel, 'openai/gpt-4.1');
    assert.deepEqual(JSON.parse(readFileSync(configPath, 'utf8')), {
      smol: 'openai/gpt-4.1-mini', slow: 'anthropic/claude-opus', default: 'openai/gpt-4.1',
    });
  } finally {
    delete process.env.OMP_FAKE_CONFIG_PATH;
    rmSync(directory, { recursive: true, force: true });
  }
});

test('invalid model selectors use a typed selection error', async () => {
  await assert.rejects(setAstridOmpDefaultModel({ command: '/missing/omp', cwd: '/tmp' }, 'not-a-selector'), OmpModelSelectionError);
});

test('OMP command failures do not expose stderr details', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-omp-models-'));
  try {
    const command = join(directory, 'failing-omp');
    writeFileSync(command, '#!/bin/sh\nprintf credential-secret-should-never-escape >&2\nexit 9\n', { mode: 0o755 });
    chmodSync(command, 0o755);
    await assert.rejects(getAstridOmpModelCatalog({ command, cwd: directory }), error => {
      assert.equal((error as Error).message, 'OMP model operation failed');
      assert.equal((error as Error).message.includes('credential'), false);
      return true;
    });
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});
