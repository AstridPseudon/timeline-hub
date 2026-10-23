import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  DIAGNOSTIC_MAX_BYTES,
  diagnosticObservedVisibility,
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
    basis: [{ baseRevisionId: 'basis-revision', basePublicationId: 'basis-publication', merge: 'fields', reads: readonlyTraffic }],
    displayedHead: { revisionId: 'displayed-revision', publicationId: 'displayed-publication' },
    outbox: {
      summary: { hasPending: true, hasConflict: true },
      owners: [{ ownerId: 'owner-1', pending: { intentId: 'intent-1', outcome: { kind: 'retry' } } }],
    },
    sourceWindow: { rightId: 'right-1', before: { sourceIn: { numericValue: 0 } }, after: { sourceIn: { numericValue: 3 } } },
    ui: { recoveryMessage: 'changes retained' },
    errors: { page: ['network error'] },
  });
  const body = output.slice(output.indexOf('] ') + 2);

  assert.ok(new TextEncoder().encode(output).length <= DIAGNOSTIC_MAX_BYTES);
  assert.doesNotThrow(() => JSON.parse(body));
  assert.equal(body.includes('basis-revision'), true);
  assert.equal(body.includes('basis-publication'), true);
  assert.equal(body.includes('"count":40'), true);
  assert.equal(body.includes('"summarized":true'), true);
  assert.equal(body.includes('"truncated":false'), true);
  assert.equal(body.includes('displayed-revision'), true);
  assert.equal(body.includes('owner-1'), true);
  assert.equal(body.includes('right-1'), true);
  assert.equal(body.includes('numericValue'), true);
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

test('P1 failure continuation keeps the realistic causal core under the byte budget', () => {
  const heads = Array.from({ length: 40 }, (_, index) => ({
    method: 'POST',
    route: '/api/runtime/v1/projects/:project/timelines/:timeline/commit',
    key: `commit-key-${index}`,
    status: index % 2 === 0 ? 200 : 409,
    head: { revisionId: `revision-${index}`, publicationId: `publication-${index}` },
    replyReadFailed: false,
  }));
  const owners = Array.from({ length: 40 }, (_, index) => ({
    ownerId: `owner-${index}`,
    generation: index,
    intentCount: 1,
    pending: {
      intentId: `intent-${index}`,
      request: { method: 'POST', path: '/api/runtime/v1/projects/:project/timelines/:timeline/commit', key: `commit-key-${index}` },
      outcome: { kind: index % 2 === 0 ? 'retry' : 'rejected', status: index % 2 === 0 ? 503 : 409, reason: 'value_conflict' },
    },
    acceptedHead: { revisionId: `accepted-${index}`, publicationId: `publication-${index}` },
  }));
  const readonlyReplies = Array.from({ length: 40 }, (_, index) => ({
    route: '/api/runtime/v1/projects/:project/timelines/:timeline',
    status: 200,
    head: { revisionId: `readonly-${index}`, publicationId: `publication-${index}` },
  }));
  const output = formatPriorityDiagnostic('P1 failure continuation realistic', {
    case: {
      projectId: 'project-realistic', projectSlug: 'project-slug', timelineId: 'timeline-realistic',
      sourceId: 'p1-chain-source', originalClipId: 'p1-chain-source', rightId: 'p1-chain-source-right',
      expectedPostCount: 2, observedPostCount: 2,
    },
    basis: [{ baseRevisionId: 'basis-revision', basePublicationId: 'basis-publication', merge: 'fields', reads: readonlyReplies }],
    displayedHead: {
      providerProjectId: 'project-realistic', providerTimelineId: 'timeline-realistic',
      commitReplies: heads.map(({ head }, index) => ({ index, head })),
      currentWireHeads: heads,
      readonlyReplies,
      runtimeHistoryHead: { revisionId: 'history-revision', publicationId: 'history-publication' },
      historyReadFailed: false,
    },
    outbox: {
      readFailed: false,
      summary: {
        ownerCount: 40, intentLengths: Array(40).fill(1), pendingIntentLengths: Array(40).fill(1),
        outcomeKinds: Array(40).fill('rejected'), hasIdleOwner: false, hasPending: true, hasIntents: true, hasConflict: true,
      },
      owners,
    },
    sourceWindow: {
      rightId: 'p1-chain-source-right',
      before: { sourceIn: { value: '0', numericValue: 0, visible: true } },
      after: { sourceIn: { value: '3', numericValue: 3, visible: true } },
    },
    ui: {
      connectionState: 'connected', runtimePanelVisible: false, recoveryVisible: true,
      recoveryMessage: 'Your changes are retained and need resolution before they can be saved.',
      timelineErrorVisible: false, timelineErrorMessage: 'UNKNOWN', alertCount: 1,
    },
    errors: {
      page: Array.from({ length: 40 }, () => 'network error'),
      console: Array.from({ length: 40 }, () => ({ type: 'error', signal: 'network_error', message: 'network error', location: 'UNKNOWN' })),
      requestFailures: Array.from({ length: 40 }, () => ({ method: 'GET', route: '/api/runtime/v1/projects/:project/timelines/:timeline', error: 'connection reset' })),
    },
  });
  const body = JSON.parse(output.slice(output.indexOf('] ') + 2)) as Record<string, any>;

  assert.ok(new TextEncoder().encode(output).length <= DIAGNOSTIC_MAX_BYTES);
  for (const key of ['case', 'displayedHead', 'outbox', 'sourceWindow', 'ui', 'errors']) assert.ok(body[key]);
  assert.equal(body.case.rightId, 'p1-chain-source-right');
  assert.equal(body.displayedHead.currentWireHeads.count, 40);
  assert.equal(body.displayedHead.readonlyReplies.count, 40);
  assert.equal(body.outbox.owners.count, 40);
  assert.equal(body.errors.page.count, 40);
  assert.equal(body.sourceWindow.after.sourceIn.numericValue, 3);
  assert.equal(body.ui.recoveryVisible, true);
  assert.equal(body.errors.requestFailures.items[0].error, 'connection reset');
});

test('P1 DOM evidence reports only unique attached visibility as observed', () => {
  assert.equal(diagnosticObservedVisibility([]), 'UNKNOWN');
  assert.equal(diagnosticObservedVisibility([{ attached: true, visible: true }, { attached: true, visible: false }]), 'UNKNOWN');
  assert.equal(diagnosticObservedVisibility([{ attached: false, visible: false }]), 'UNKNOWN');
  assert.equal(diagnosticObservedVisibility([{ attached: true, visible: false }]), false);
});

test('P1 priority logging cannot mask the original assertion when formatting or logging throws', () => {
  const original = new Error('original priority assertion');
  const throwingLogger = () => { throw new Error('priority logger failure'); };
  assert.doesNotThrow(() => logPriorityDiagnostic('priority probe', { value: 'safe' }, throwingLogger));
  assert.throws(() => { throw original; }, (error) => error === original);
});
