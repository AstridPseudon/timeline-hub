import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  createD21Environment,
  observeD21Harness,
  observeD21Page,
  recordD21Readiness,
  serializeD21Environment,
} from './d21-environment.ts';

test('the safe projector does not carry a secret canary from malformed endpoint input', () => {
  const artifact = createD21Environment();
  observeD21Harness(artifact, {
    runtimeUrl: 'http://127.0.0.1:17340/v1?canary=do-not-export',
    doorBase: 'http://127.0.0.1:17340/api/runtime',
    doorPrefix: '/api/runtime',
    editorOrigin: 'https://astrid.test:443',
    productCredentialPresent: true,
    authoringProfile: 'UNKNOWN',
  });
  observeD21Page(artifact, { url: 'not a URL' });
  const text = serializeD21Environment(artifact);
  assert.doesNotMatch(text, /do-not-export|canary/);
  assert.equal(artifact.backend.host.observation, 'UNKNOWN');
  assert.equal(artifact.editor.origin.observation, 'UNKNOWN');
});

test('safe observations retain public endpoint facts and never URL queries', () => {
  const artifact = createD21Environment();
  observeD21Harness(artifact, {
    runtimeUrl: 'http://127.0.0.1:19001',
    doorBase: 'http://127.0.0.1:19002/api/runtime',
    doorPrefix: '/api/runtime',
    editorOrigin: 'https://astrid.test:19003',
    productCredentialPresent: false,
    authoringProfile: 'astrid',
    agentCommit: '079580ca46af77e0292d49dc34386b25c8391f99',
    runtimeCommit: '2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d',
  });
  observeD21Page(artifact, { url: 'https://astrid.test:19003/tools/video-editor?private=1#fragment' });
  assert.deepEqual(artifact.backend.port, { observation: 'OBSERVED', value: 19001 });
  assert.deepEqual(artifact.door.port, { observation: 'OBSERVED', value: 19002 });
  assert.deepEqual(artifact.editor.path, { observation: 'OBSERVED', value: '/tools/video-editor' });
  assert.equal(artifact.provider.attached.observation, 'UNKNOWN');
  assert.equal(artifact.provider.sourceObserved.observation, 'DECLARED');
  assert.equal(artifact.sourceCommits.launcher.value?.length, 2);
  assert.doesNotMatch(serializeD21Environment(artifact), /private|fragment/);
});

test('lifecycle projection distinguishes declared launch facts from observed process facts', () => {
  const artifact = createD21Environment();
  observeD21Harness(artifact, {
    runtimeUrl: 'http://127.0.0.1:19001',
    doorBase: 'http://127.0.0.1:19002/api/runtime',
    doorPrefix: '/api/runtime',
    editorOrigin: 'https://astrid.test:19003',
    productCredentialPresent: true,
    authoringProfile: 'astrid',
    lifecycle: {
      startedAt: '2026-10-23T20:00:00.000Z',
      readyAt: '2026-10-23T20:00:01.000Z',
      launchInterpreter: '/approved/python',
      launchModule: 'runtime_protocol.cli',
      launchProfile: 'astrid',
      actualInterpreter: '/proc/123/exe',
      actualModule: 'runtime_protocol.cli',
      doorOriginEquality: true,
    },
  });
  assert.deepEqual(artifact.backend.launch.module, { observation: 'DECLARED', value: 'runtime_protocol.cli' });
  assert.deepEqual(artifact.backend.launch.profile, { observation: 'DECLARED', value: 'astrid' });
  assert.deepEqual(artifact.backend.process.module, { observation: 'OBSERVED', value: 'runtime_protocol.cli' });
  assert.deepEqual(artifact.door.allowedOriginEquality, { observation: 'OBSERVED', value: true });
  assert.equal(artifact.provider.attached.observation, 'UNKNOWN');
  assert.doesNotMatch(serializeD21Environment(artifact), /stdout|--root|credential|token/);
});

test('startup failure and observed signal exit remain finite facts', () => {
  const artifact = createD21Environment();
  observeD21Harness(artifact, {
    runtimeUrl: 'http://127.0.0.1:19001',
    doorBase: 'http://127.0.0.1:19002/api/runtime',
    doorPrefix: '/api/runtime',
    editorOrigin: 'https://astrid.test:19003',
    productCredentialPresent: false,
    authoringProfile: 'UNKNOWN',
    lifecycle: {
      startedAt: '2026-10-23T20:00:00.000Z',
      launchInterpreter: '/approved/python',
      launchModule: 'runtime_protocol.cli',
      launchProfile: 'neutral',
      exitCode: null,
      exitedAt: '2026-10-23T20:00:00.500Z',
      failure: { code: 'startup_failed', class: 'startup', stage: 'health' },
    },
  });
  assert.deepEqual(artifact.backend.error, { observation: 'OBSERVED', value: { code: 'startup_failed', class: 'startup', stage: 'health' } });
  assert.deepEqual(artifact.backend.exit, { observation: 'OBSERVED', value: null });
  assert.deepEqual(artifact.backend.exitAt, { observation: 'OBSERVED', value: '2026-10-23T20:00:00.500Z' });
  assert.equal(artifact.backend.process.module.observation, 'UNKNOWN');
});

test('unknown provider and owner observations stay unknown, including a connected-false control', () => {
  const artifact = createD21Environment();
  recordD21Readiness(artifact, false, 'UNKNOWN');
  assert.equal(artifact.readiness.connected.value, false);
  assert.equal(artifact.readiness.freshSettledOwner.observation, 'UNKNOWN');
  assert.equal(artifact.status, 'failed');
  assert.equal(createD21Environment().provider.attached.observation, 'UNKNOWN');
});

test('the bounded serializer rejects oversized output instead of truncating JSON', () => {
  const artifact = createD21Environment();
  artifact.stages.push(...Array.from({ length: 8 }, (_, index) => ({
    name: `stage-${index}`,
    startedAt: '2026-10-23T00:00:00.000Z',
    completedAt: '2026-10-23T00:00:01.000Z',
    result: 'FAILED' as const,
  })));
  artifact.backend.imports.daemon.modules = { observation: 'OBSERVED', value: Array.from({ length: 5000 }, () => 'module') };
  assert.throws(() => serializeD21Environment(artifact), /32KiB/);
});
