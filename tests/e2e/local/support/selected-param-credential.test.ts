import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
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
    }, credentialFile, { runtimeUrl: 'http://127.0.0.1:32101', realmId: 'fixture-realm' });

    assert.equal(env.ASTRID_RUNTIME_CREDENTIAL, credentialFile);
    assert.notEqual(env.ASTRID_RUNTIME_CREDENTIAL, token);
    assert.equal(env.WORKSPACE_RUNTIME_TOKEN_FILE, '/tmp/product-credential.json');
    assert.equal(statSync(credentialFile).mode & 0o777, 0o600);
    assert.deepEqual(JSON.parse(readFileSync(credentialFile, 'utf8')), { token, actor_id: 'astrid-selected-param' });
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test('selected CLI targets the credential issuer after authoring restart despite ambient workspace overrides', async (t) => {
  const harness = new DirectHarness();
  harness.tmp = mkdtempSync(path.join(tmpdir(), 'astrid-selected-binding-'));
  harness.realmId = 'selected-issuer-realm';
  harness.runtimePort = 32102; // The current port, after enableTimelineAuthoring restarts the Runtime.
  const credentialFile = path.join(harness.tmp, 'selected-agent-credential.json');
  try {
    mkdirSync(path.join(harness.supportDir, 'credentials'), { recursive: true });
    writeFileSync(path.join(harness.supportDir, 'credentials', 'owner.token'), 'offline-owner', { mode: 0o600 });
    let issuer = '';
    let actor = '';
    t.mock.method(globalThis, 'fetch', async (url: string, init: RequestInit) => {
      issuer = String(url);
      actor = JSON.parse(init.body as string).actor_id;
      return new Response('{}', { status: 201 });
    });
    await harness.provisionCredential('astrid-selected-param', path.basename(credentialFile));

    const ambient = {
      ASTRID_RUNTIME_ENDPOINT: 'http://127.0.0.1:32100',
      ASTRID_RUNTIME_DATA_ROOT: '/tmp/wrapper/runtime-data',
      ASTRID_RUNTIME_SOURCE_MANIFEST: '/tmp/wrapper/source-manifest.json',
      ASTRID_RUNTIME_DOOR_PORT: '18001',
      ASTRID_TIMELINE_EVAL_ENDPOINT: 'http://127.0.0.1:32100',
      ASTRID_TIMELINE_EVAL_CREDENTIAL: '/tmp/wrapper/other-credential.json',
      ASTRID_TIMELINE_EVAL_REALM_ID: 'wrapper-realm',
      ASTRID_TIMELINE_EVAL_ACTOR_ID: 'wrapper-actor',
      WORKSPACE_RUNTIME_TOKEN_FILE: harness.credentialPath,
    };
    const env = selectedParamCliEnv(ambient, credentialFile, harness);
    assert.equal(`${env.ASTRID_TIMELINE_EVAL_ENDPOINT}/v1/credentials`, issuer);
    assert.equal(env.ASTRID_RUNTIME_ENDPOINT, env.ASTRID_TIMELINE_EVAL_ENDPOINT);
    assert.equal(env.ASTRID_TIMELINE_EVAL_CREDENTIAL, credentialFile);
    assert.equal(env.ASTRID_RUNTIME_CREDENTIAL, credentialFile);
    assert.equal(env.ASTRID_TIMELINE_EVAL_REALM_ID, harness.realmId);
    assert.equal(env.ASTRID_TIMELINE_EVAL_ACTOR_ID, actor);
    assert.equal(statSync(credentialFile).mode & 0o777, 0o600);
    assert.equal(JSON.parse(readFileSync(credentialFile, 'utf8')).actor_id, actor);
    assert.equal(env.WORKSPACE_RUNTIME_TOKEN_FILE, ambient.WORKSPACE_RUNTIME_TOKEN_FILE);
    assert.equal(ambient.ASTRID_TIMELINE_EVAL_REALM_ID, 'wrapper-realm');
  } finally {
    await harness.stop();
  }
  assert.equal(existsSync(credentialFile), false);
  assert.equal(existsSync(harness.tmp), false);
});

test('harness cleanup removes the selected credential root after fixture setup failure', async () => {
  const root = mkdtempSync(path.join(tmpdir(), 'astrid-selected-credential-failure-'));
  const credentialFile = path.join(root, 'selected-agent-credential.json');
  writeFileSync(credentialFile, JSON.stringify({ token: 'offline-unused', actor_id: 'astrid-selected-param' }), { mode: 0o600 });
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
  assert.equal(existsSync(credentialFile), false);
  assert.equal(existsSync(root), false);
  await harness.stop();
});
