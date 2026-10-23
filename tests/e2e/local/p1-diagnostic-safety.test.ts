import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  DIAGNOSTIC_MAX_BYTES,
  formatDiagnostic,
  formatPriorityDiagnostic,
  logDiagnostic,
  logPriorityDiagnostic,
  redactDiagnosticText,
} from './p1-diagnostic-safety.ts';

test('P1 diagnostics redact quoted credential fields before formatting', () => {
  const output = formatDiagnostic('quoted JSON', {
    authorization: 'authorization-secret',
    authToken: 'auth-token-secret',
    headers: { Cookie: 'cookie-secret', token: 'token-secret' },
    raw: '{"authorization":"quoted-authorization","cookie":"quoted-cookie","token":"quoted-token"}',
  });

  assert.equal(output.includes('authorization-secret'), false);
  assert.equal(output.includes('auth-token-secret'), false);
  assert.equal(output.includes('cookie-secret'), false);
  assert.equal(output.includes('token-secret'), false);
  assert.equal(output.includes('quoted-authorization'), false);
  assert.equal(output.includes('quoted-cookie'), false);
  assert.equal(output.includes('quoted-token'), false);
  assert.equal(redactDiagnosticText('{"authorization":{"value":"nested-secret"}}').includes('nested-secret'), false);
});

test('P1 diagnostics bound breadth, depth, arrays, strings, and bytes', () => {
  const broad: Record<string, unknown> = {};
  for (let index = 0; index < 6000; index += 1) broad[`field-${index}`] = 'x'.repeat(500);
  broad.token = 'breadth-secret';
  const deep: Record<string, unknown> = { value: 'deep-secret' };
  let cursor = deep;
  for (let index = 0; index < 30; index += 1) {
    cursor.next = { value: `depth-${index}` };
    cursor = cursor.next as Record<string, unknown>;
  }
  const output = formatDiagnostic('bounds', { broad, deep, array: Array(6000).fill('array-value'), text: 'z'.repeat(20_000) });

  assert.ok(new TextEncoder().encode(output).length <= DIAGNOSTIC_MAX_BYTES);
  assert.equal(output.includes('breadth-secret'), false);
  assert.ok(output.includes('[TRUNCATED]') || output.includes('[TRUNCATED_ARRAY]') || output.includes('[REDACTED_DEPTH]'));
});

test('P1 diagnostics cannot mask the original assertion when the logger throws', () => {
  const original = new Error('original assertion');
  const throwingLogger = () => { throw new Error('logger failure'); };
  let observed: unknown;

  try {
    logDiagnostic('logger probe', { get value() { throw new Error('getter failure'); } }, throwingLogger);
    throw original;
  } catch (error) {
    observed = error;
  }

  assert.strictEqual(observed, original);

  const savedConsoleLog = console.log;
  try {
    console.log = throwingLogger;
    assert.doesNotThrow(() => logDiagnostic('stdout probe', { value: 'safe' }));
  } finally {
    console.log = savedConsoleLog;
  }
});

test('P1 priority diagnostics preserve causal state ahead of oversized readonly traffic', () => {
  const readonlyTraffic = Array.from({ length: 40 }, () => ({ reply: 'x'.repeat(20_000) }));
  const output = formatPriorityDiagnostic('priority', {
    basis: [{ baseRevisionId: 'basis-revision', basePublicationId: 'basis-publication', merge: 'fields' }],
    displayedHead: { revisionId: 'displayed-revision', publicationId: 'displayed-publication' },
    outbox: { summary: { hasPending: true, hasConflict: true } },
    ui: { recoveryMessage: 'changes retained' },
    errors: { page: ['network error'] },
  });
  const body = output.slice(output.indexOf('] ') + 2);

  assert.ok(new TextEncoder().encode(output).length <= DIAGNOSTIC_MAX_BYTES);
  assert.doesNotThrow(() => JSON.parse(body));
  assert.equal(body.includes('basis-revision'), true);
  assert.equal(body.includes('displayed-revision'), true);
  assert.equal(body.includes(readonlyTraffic[0].reply), false);
});

test('P1 priority diagnostics keep an oversized value finite, redacted, and parseable', () => {
  const broad: Record<string, string> = {};
  for (let index = 0; index < 600; index += 1) broad[`field-${index}`] = 'r'.repeat(500);
  const output = formatPriorityDiagnostic('priority', {
    authorization: 'should-not-leak',
    readonly: broad,
  });
  const body = output.slice(output.indexOf('] ') + 2);

  assert.ok(new TextEncoder().encode(output).length <= DIAGNOSTIC_MAX_BYTES);
  assert.deepEqual(JSON.parse(body), { diagnostic: 'priority_over_budget' });
  assert.equal(output.includes('should-not-leak'), false);
});

test('P1 priority logging cannot mask the original assertion when formatting or logging throws', () => {
  const original = new Error('original priority assertion');
  const throwingLogger = () => { throw new Error('priority logger failure'); };
  assert.doesNotThrow(() => logPriorityDiagnostic('priority probe', { value: 'safe' }, throwingLogger));
  assert.throws(() => { throw original; }, (error) => error === original);
});
