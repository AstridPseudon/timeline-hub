import { test } from 'bun:test';
import assert from 'node:assert/strict';
import { chmodSync, mkdtempSync, readFileSync, realpathSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { getAstridAgentModelCatalog, setAstridAgentDefaultModel } from './astrid-agent-models.ts';

const catalog = {
  schemaVersion: 1,
  currentModel: 'openai/retired-model',
  providers: [
    {
      id: 'openai', name: 'OpenAI', signedIn: true,
      models: [{ id: 'gpt-4.1', name: 'GPT 4.1', selector: 'openai/gpt-4.1' }],
      usage: [{ fetchedAt: 123, limits: [{
        label: 'Monthly', amount: { unit: 'tokens', used: 20, limit: 100, remaining: 80, usedFraction: 0.2, remainingFraction: 0.8 },
        window: { durationMs: 2_592_000_000, resetsAt: 456 }, status: 'warning',
      }] }],
    },
    {
      id: 'local', name: 'Local models', signedIn: false,
      models: [{ id: 'llama', name: 'Llama', selector: 'local/llama' }],
    },
  ],
};

function fakeAstrid(directory: string): { command: string; calls: string; models: string; selection: string } {
  const command = join(directory, 'astrid');
  const calls = join(directory, 'calls.jsonl');
  const models = join(directory, 'models.json');
  const selection = join(directory, 'selection.json');
  writeFileSync(models, JSON.stringify(catalog));
  writeFileSync(selection, JSON.stringify(catalog));
  writeFileSync(command, `#!/usr/bin/env node
const fs = require('node:fs');
fs.appendFileSync(${JSON.stringify(calls)}, JSON.stringify({ argv: process.argv.slice(2), cwd: process.cwd(), profile: process.env.OMP_PROFILE ?? null }) + '\\n');
if (process.env.ASTRID_FAKE_FAIL === '1') {
  process.stderr.write('credential-secret-private diagnostic');
  process.exit(9);
}
if (process.env.ASTRID_FAKE_BAD_JSON === '1') {
  process.stdout.write('{malformed');
} else if (process.argv[2] === 'agent' && process.argv[3] === 'models' && process.argv[4] === '--json') {
  process.stdout.write(fs.readFileSync(${JSON.stringify(models)}, 'utf8'));
} else if (process.argv[2] === 'agent' && process.argv[3] === 'use' && process.argv[5] === '--json') {
  const requested = process.argv[4];
  const response = JSON.parse(fs.readFileSync(${JSON.stringify(selection)}, 'utf8'));
  if (process.env.ASTRID_FAKE_MISMATCH === '1') response.currentModel = 'openai/different-model';
  else response.currentModel = requested;
  process.stdout.write(JSON.stringify(response));
} else {
  process.stderr.write('credential-secret-private diagnostic');
  process.exit(8);
}
`, { mode: 0o755 });
  chmodSync(command, 0o755);
  return { command, calls, models, selection };
}

function readCalls(path: string): unknown[] {
  return readFileSync(path, 'utf8').trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
}

test('agent model catalog maps the CLI response to the safe ACP projection and preserves CLI state', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-agent-models-'));
  try {
    const fake = fakeAstrid(directory);
    const result = await getAstridAgentModelCatalog({ command: fake.command, cwd: directory, profile: 'fixture-profile' });
    assert.deepEqual(result, {
      providers: [
        {
          id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-4.1', name: 'GPT 4.1' }],
          usage: { limits: [{ unit: 'tokens', used: 20, limit: 100, remaining: 80, usedFraction: 0.2, remainingFraction: 0.8, durationMs: 2_592_000_000, resetsAt: 456, status: 'warning' }] },
        },
        { id: 'local', name: 'Local models', signedIn: false, models: [{ id: 'llama', name: 'Llama' }] },
      ],
      currentModel: 'openai/retired-model',
    });
    assert.deepEqual(readCalls(fake.calls), [{
      argv: ['agent', 'models', '--json'], cwd: realpathSync(directory), profile: 'fixture-profile',
    }]);
    const serialized = JSON.stringify(result);
    for (const privateValue of ['selector', 'fetchedAt', 'Monthly']) assert.equal(serialized.includes(privateValue), false);
  } finally {
    delete process.env.ASTRID_FAKE_FAIL;
    delete process.env.ASTRID_FAKE_BAD_JSON;
    delete process.env.ASTRID_FAKE_MISMATCH;
    rmSync(directory, { recursive: true, force: true });
  }
});

test('agent model selection invokes Astrid with the selector and returns its selected model', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-agent-use-'));
  try {
    const fake = fakeAstrid(directory);
    const currentModel = await setAstridAgentDefaultModel({ command: fake.command, cwd: directory, profile: 'fixture-profile' }, 'openai/gpt-4.1');
    assert.equal(currentModel, 'openai/gpt-4.1');
    assert.deepEqual(readCalls(fake.calls), [{
      argv: ['agent', 'use', 'openai/gpt-4.1', '--json'], cwd: realpathSync(directory), profile: 'fixture-profile',
    }]);
  } finally {
    delete process.env.ASTRID_FAKE_MISMATCH;
    rmSync(directory, { recursive: true, force: true });
  }
});

test('agent model adapter rejects unsupported schemas, malformed JSON, mismatched selections, and redacts CLI diagnostics', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'astrid-agent-invalid-'));
  try {
    const fake = fakeAstrid(directory);
    writeFileSync(fake.models, JSON.stringify({ ...catalog, schemaVersion: 2 }));
    await assert.rejects(getAstridAgentModelCatalog({ command: fake.command, cwd: directory }));

    writeFileSync(fake.models, JSON.stringify(catalog));
    process.env.ASTRID_FAKE_BAD_JSON = '1';
    await assert.rejects(getAstridAgentModelCatalog({ command: fake.command, cwd: directory }));
    delete process.env.ASTRID_FAKE_BAD_JSON;

    process.env.ASTRID_FAKE_MISMATCH = '1';
    await assert.rejects(setAstridAgentDefaultModel({ command: fake.command, cwd: directory }, 'openai/gpt-4.1'));
    delete process.env.ASTRID_FAKE_MISMATCH;

    process.env.ASTRID_FAKE_FAIL = '1';
    await assert.rejects(getAstridAgentModelCatalog({ command: fake.command, cwd: directory }), error => {
      assert.equal((error as Error).message.includes('credential-secret-private'), false);
      return true;
    });
    await assert.rejects(setAstridAgentDefaultModel({ command: fake.command, cwd: directory }, 'openai/gpt-4.1'), error => {
      assert.equal((error as Error).message.includes('credential-secret-private'), false);
      return true;
    });
  } finally {
    delete process.env.ASTRID_FAKE_FAIL;
    delete process.env.ASTRID_FAKE_BAD_JSON;
    delete process.env.ASTRID_FAKE_MISMATCH;
    rmSync(directory, { recursive: true, force: true });
  }
});
