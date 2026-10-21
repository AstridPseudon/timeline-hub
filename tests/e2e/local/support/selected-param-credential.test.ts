import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { DirectHarness, selectedParamCliEnv } from './harness.ts';

test('selected Agent child env carries the credential file path, not its token', () => {
  const root = mkdtempSync(path.join(tmpdir(), 'astrid-selected-credential-'));
  try {
    const credentialFile = path.join(root, 'selected-agent-credential.json');
    const token = 'fixture-token-must-not-enter-the-child-env';
    writeFileSync(credentialFile, JSON.stringify({ token, actor_id: 'astrid-selected-param' }), { mode: 0o600 });

    const env = selectedParamCliEnv({
      ASTRID_RUNTIME_CREDENTIAL: token,
      WORKSPACE_RUNTIME_TOKEN_FILE: '/tmp/product-credential.json',
    }, credentialFile);

    assert.equal(env.ASTRID_RUNTIME_CREDENTIAL, credentialFile);
    assert.notEqual(env.ASTRID_RUNTIME_CREDENTIAL, token);
    assert.equal(env.WORKSPACE_RUNTIME_TOKEN_FILE, '/tmp/product-credential.json');
    assert.equal(statSync(credentialFile).mode & 0o777, 0o600);
    assert.deepEqual(JSON.parse(readFileSync(credentialFile, 'utf8')), { token, actor_id: 'astrid-selected-param' });
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('harness cleanup removes the selected credential root after fixture setup failure', async () => {
  const root = mkdtempSync(path.join(tmpdir(), 'astrid-selected-credential-failure-'));
  const harness = new DirectHarness();
  (harness as unknown as { tmp: string }).tmp = root;
  try {
    try {
      throw new Error('fixture setup failed before P1 admission');
    } catch {
      // The fixture owner invokes the same teardown path for setup failures.
    }
  } finally {
    await harness.stop();
  }
  assert.equal(existsSync(root), false);
  await harness.stop();
});
