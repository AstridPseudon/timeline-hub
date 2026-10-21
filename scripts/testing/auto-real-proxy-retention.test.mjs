import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import test from 'node:test';
import { recordFailureEvidence, sanitizeHttpFailureFacts } from './auto-real-proxy-main95.mjs';

test('sanitizes HTTP failure facts to path, status, and validated fields', () => {
  assert.deepEqual(sanitizeHttpFailureFacts([
    {
      method: 'GET', url: '/runtime/v1/tasks?token=do-not-retain', status: 503,
      code: 'operation_unavailable', type: 'proxy', location: '/v1/tasks',
      message: 'full response body', headers: { authorization: 'Bearer secret' },
    },
    { method: 'POST', path: '/v1/commit', status: 200, code: 'not-a-failure' },
    { method: 'GET', path: '/v1/bad?secret=1', status: 503, code: 'contains spaces' },
  ]), [
    { method: 'GET', path: '/runtime/v1/tasks', status: 503, code: 'operation_unavailable', type: 'proxy', location: '/v1/tasks' },
    { method: 'GET', path: '/v1/bad', status: 503 },
  ]);
});

test('planted 503 survives owned-root cleanup while the parent keeps its failure status', () => {
  const root = mkdtempSync(path.join(os.tmpdir(), 'auto-real-proxy-retention-'));
  const runRoot = path.join(root, 'run');
  const recordRoot = path.join(root, 'record');
  const browserOutput = path.join(runRoot, 'browser-artifacts', 'failed-test');
  mkdirSync(browserOutput, { recursive: true });
  writeFileSync(path.join(browserOutput, 'auto-http-failures.json'), JSON.stringify({ httpFailures: [{
    method: 'GET', path: '/runtime/v1/tasks?credential=secret', status: 503,
    code: 'operation_unavailable', type: 'proxy', location: '/v1/tasks',
    message: 'full body must not be retained', headers: { authorization: 'Bearer secret' },
  }] }));
  writeFileSync(path.join(browserOutput, 'trace.zip'), 'small trace placeholder');

  const moduleUrl = pathToFileURL(path.resolve('scripts/testing/auto-real-proxy-main95.mjs')).href;
  const child = spawnSync(process.execPath, ['--input-type=module', '--eval', [
    `import { recordFailureEvidence } from ${JSON.stringify(moduleUrl)};`,
    `import { rmSync } from 'node:fs';`,
    `recordFailureEvidence(${JSON.stringify(runRoot)}, ${JSON.stringify(recordRoot)}, 97);`,
    `rmSync(${JSON.stringify(runRoot)}, { recursive: true, force: true });`,
    'process.exitCode = 97;',
  ].join('\n')], { encoding: 'utf8' });
  try {
    assert.equal(child.status, 97, child.stderr);
    assert.equal(readFileSync(path.join(recordRoot, 'runner-result.json'), 'utf8').includes('"status":97'), true);
    const evidence = JSON.parse(readFileSync(path.join(recordRoot, 'auto-http-failures.json'), 'utf8'));
    assert.deepEqual(evidence.failures, [{ method: 'GET', path: '/runtime/v1/tasks', status: 503, code: 'operation_unavailable', type: 'proxy', location: '/v1/tasks' }]);
    assert.deepEqual(JSON.parse(readFileSync(path.join(recordRoot, 'trace-presence.json'), 'utf8')), { present: true, bytes: 23 });
    assert.equal(readFileSync(path.join(recordRoot, 'auto-http-failures.json'), 'utf8').includes('secret'), false);
    assert.equal(readFileSync(path.join(recordRoot, 'auto-http-failures.json'), 'utf8').includes('message'), false);
    assert.equal(readFileSync(path.join(recordRoot, 'auto-http-failures.json'), 'utf8').includes('headers'), false);
    assert.equal(readFileSync(path.join(recordRoot, 'runner-result.json'), 'utf8').includes('evidence_recorded_before_cleanup'), true);
    assert.equal(existsSync(runRoot), false);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
