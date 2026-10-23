import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { runInNewContext } from 'node:vm';
import ts from 'typescript';
import {
  DIAGNOSTIC_MAX_BYTES,
  diagnosticListener,
  diagnosticObservedVisibility,
  formatDiagnostic,
  formatDiagnosticArtifact,
  formatPriorityDiagnostic,
  logDiagnostic,
  logPriorityDiagnostic,
  redactDiagnosticText,
  writeDiagnosticArtifact,
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

test('P1 diagnostic artifacts retain uncapped safe files and exact correlation unknowns', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'p1-diagnostic-artifact-'));
  const artifactPath = join(directory, 'p1-diagnostic.json');
  const attachments: Array<{ name: string; path: string; contentType: string }> = [];
  const testInfo = {
    outputPath: () => artifactPath,
    attach: async (name: string, options: { path: string; contentType: string }) => { attachments.push({ name, ...options }); },
  };
  const payload = {
    schemaVersion: 1,
    title: 'P1 exact case title',
    status: 'failed',
    expectedStatus: 'passed',
    capturedAt: '2026-10-23T19:12:00.000Z',
    phase: 'afterEach_failure_continuation',
    tuple: { projectId: 'project-safe', timelineId: 'timeline-safe', sourceId: 'UNKNOWN', rightId: 'right-safe' },
    mountedObservations: 'UNKNOWN',
    available: {
      wireHeads: [{ method: 'POST', route: '/api/runtime/v1/projects/:project/timelines/:timeline/commit', status: 200,
        head: { revisionId: 'revision-safe', publicationId: 'publication-safe' }, keyProjection: { present: true, bytes: 36 } }],
      requestProjections: Array.from({ length: 40 }, (_, index) => ({
        index, method: 'POST', route: '/api/runtime/v1/projects/:project/timelines/:timeline/commit', status: 200,
        bodyProjection: { present: true, bytes: 700, sameAsPrevious: index > 0 },
        keyProjection: { present: true, bytes: 36, sameAsPrevious: index > 0 },
        message: `available-${index} ${'x'.repeat(500)}`,
      })),
      errors: { console: [{ message: '{"nested":{"token":"nested-token-secret","cookie":"nested-cookie-secret"}}' }] },
    },
    captureData: 'UNKNOWN',
    unknowns: { mountedDataRef: 'UNKNOWN', callbackPatch: 'UNKNOWN', captureResolution: 'UNKNOWN' },
    losses: { cappedConsole: true, mountedObservations: 'UNKNOWN' },
  };
  let deepAvailable: Record<string, unknown> = { message: 'deep-safe-end' };
  for (let index = 0; index < 12; index += 1) deepAvailable = { available: deepAvailable };
  (payload.available as Record<string, unknown>).available = deepAvailable;

  const fileWritten = await writeDiagnosticArtifact(testInfo, payload);
  assert.equal(fileWritten, true);
  const contents = readFileSync(artifactPath, 'utf8');
  assert.ok(new TextEncoder().encode(contents).length > DIAGNOSTIC_MAX_BYTES);
  const parsed = JSON.parse(contents) as Record<string, any>;
  assert.equal(parsed.title, payload.title);
  assert.equal(parsed.status, payload.status);
  assert.equal(parsed.tuple.timelineId, payload.tuple.timelineId);
  assert.equal(parsed.mountedObservations, 'UNKNOWN');
  assert.equal(contents.includes('deep-safe-end'), true);
  assert.equal(contents.includes('[REDACTED_DEPTH]'), false);
  assert.equal(parsed.available.requestProjections.at(-1).message.startsWith('available-39 '), true);
  assert.equal(parsed.available.requestProjections.at(-1).message.endsWith('[TRUNCATED]'), true);
  assert.equal(contents.includes('nested-token-secret'), false);
  assert.equal(contents.includes('nested-cookie-secret'), false);
  assert.equal(attachments[0].name, 'p1-diagnostic');
  assert.equal(attachments[0].path, artifactPath);
  assert.equal(attachments[0].contentType, 'application/json');

  const capped = formatPriorityDiagnostic('capped console', payload.available);
  assert.ok(new TextEncoder().encode(capped).length <= DIAGNOSTIC_MAX_BYTES);
  assert.doesNotThrow(() => JSON.parse(capped.slice(capped.indexOf('] ') + 2)));
});

test('P1 diagnostic artifact write failure is disposable and cannot replace a test failure', async () => {
  const testInfo = {
    outputPath: () => { throw new Error('output unavailable'); },
    attach: async () => { throw new Error('attach unavailable'); },
  };
  assert.equal(await writeDiagnosticArtifact(testInfo, { title: 'safe', status: 'failed' }), false);
  const original = new Error('original test failure');
  assert.throws(() => { throw original; }, (error) => error === original);
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


test('P1 actual failure packet shapes admit only primitive fields and structural heads', () => {
  const unsafe = { body: { value: 'body-secret' }, principal: { name: 'principal-secret' }, token: 'token-secret' };
  const head = { revisionId: 'revision-safe', publicationId: 'publication-safe', ...unsafe };
  const packet = {
    case: { projectId: unsafe, rightId: 'right-safe' },
    sourceIdentities: { beforeHead: head, splitHead: head, agentHead: head, sourceAsset: 'https://private.example/unsafe-asset-secret?token=asset-token' },
    displayedHead: { runtimeHistoryHead: head, currentWireHeads: [{ head, key: unsafe }] },
    outbox: { owners: [{ acceptedHead: head, pending: { request: { key: unsafe, body: unsafe }, outcome: unsafe } }] },
    sourceWindow: { after: { selectedClip: { identity: { 'data-clip-id': unsafe }, text: unsafe } } },
    ui: { recoveryMessage: unsafe }, errors: { console: [{ message: unsafe, ...unsafe }, { message: '{"principal":{"name":"encoded-principal-secret"}}' }] },
  };
  const lines: string[] = [];
  logDiagnostic('actual detailed packet', packet, (line) => lines.push(line));
  lines.push(formatPriorityDiagnostic('actual priority packet', packet));
  for (const line of lines) {
    for (const secret of ['body-secret', 'principal-secret', 'token-secret', 'encoded-principal-secret', 'unsafe-asset-secret', 'asset-token', '"body"', '"principal"', '"token"']) assert.equal(line.includes(secret), false);
    assert.ok(line.includes('revision-safe'));
    assert.ok(line.includes('UNKNOWN'));
    assert.ok(new TextEncoder().encode(line).length <= DIAGNOSTIC_MAX_BYTES);
  }
  const invalidHead = formatPriorityDiagnostic('head tamper', { displayedHead: { runtimeHistoryHead: { revisionId: unsafe, publicationId: 'https://private.example/token-secret' } } });
  assert.equal(invalidHead.includes('token-secret'), false);
});

test('P1 actual event listeners contain synchronous stubs and rejected response promises', async () => {
  const source = readFileSync(new URL('./three-products.p1-chain.spec.ts', import.meta.url), 'utf8');
  const ast = ts.createSourceFile('p1.ts', source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS);
  const listeners: Array<{ event: string; code: string }> = [];
  const visit = (node: ts.Node) => {
    if (ts.isCallExpression(node) && ts.isPropertyAccessExpression(node.expression)
      && node.expression.expression.getText(ast) === 'page' && node.expression.name.text === 'on') {
      assert.ok(node.arguments[1].getText(ast).startsWith('diagnosticListener('));
      listeners.push({ event: (node.arguments[0] as ts.StringLiteral).text, code: node.arguments[1].getText(ast) });
    }
    ts.forEachChild(node, visit);
  };
  visit(ast);
  assert.equal(listeners.length, 11);
  const path = '/api/runtime/v1/projects/project/timelines/timeline/commit';
  const hostile = new Proxy({}, { get() { throw new Error('event getter failure'); } });
  for (const { code } of listeners) {
    const post = { key: 'key-safe' };
    const record = {};
    const request = { method: () => 'POST', headers: () => ({ 'idempotency-key': 'key-safe' }), url: () => 'http://localhost' + path };
    const listener = runInNewContext(ts.transpileModule(code, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS } }).outputText, {
      diagnosticListener, URL, diagnosticRoute: () => path, diagnosticMethod: (x: unknown) => x, diagnosticStatus: (x: unknown) => x,
      diagnosticHead: () => { throw new Error('head projection failure'); }, classifyDiagnosticError: () => 'unknown',
      redactDiagnosticText, boundedPush: (items: unknown[], item: unknown) => items.push(item),
      trace: { pageErrors: [], consoleErrors: [], requestFailures: [], wireHeads: [] },
      pageErrors: [], consoleErrors: [], runtimeResponses: [], failureSignals: { pageErrors: [], consoleErrors: [], requestFailures: [] },
      posts: [post], legacy: [], readonlyTraffic: [], readonlyByRequest: new Map([[request, record]]), captureReadonlyTraffic: true,
      COMMITS: /\/commit$/, LEGACY_WRITES: /composition-revisions$/,
    }) as (event: unknown) => unknown;
    await assert.doesNotReject(async () => { await listener(hostile); });
    for (const json of [() => { throw new Error('json sync failure'); }, () => Promise.reject(new Error('json async failure')), () => Promise.resolve({})]) {
      await assert.doesNotReject(async () => { await listener({ url: () => 'http://localhost' + path, request: () => request, status: () => 200, json }); });
    }
  }
  await new Promise((resolve) => setImmediate(resolve));
  const original = new Error('original test failure');
  await diagnosticListener(async () => { throw new Error('async event failure'); })();
  await diagnosticListener(() => ({ then() { throw new Error('thenable failure'); } }))();
  assert.throws(() => { diagnosticListener(() => { throw new Error('event failure'); })(); throw original; }, (error) => error === original);
});

test('P1 failure caller never sends an unprojected head or unsafe asset to formatting', () => {
  const source = readFileSync(new URL('./three-products.p1-chain.spec.ts', import.meta.url), 'utf8');
  assert.ok(source.includes("beforeHead: diagnosticHead({ head: before.head }) ?? 'UNKNOWN'"));
  assert.ok(source.includes("runtimeHistoryHead: diagnosticHead({ head: runtimeHistory?.head }) ?? 'UNKNOWN'"));
  assert.ok(source.includes("sourceAsset: 'UNKNOWN'"));
  assert.equal(source.includes('sourceAsset: originalClip.asset'), false);
  assert.equal(source.includes('redactDiagnosticValue('), false);
});


test('P1 detailed failure caller projects hostile heads and an unsafe source asset', async () => {
  const source = readFileSync(new URL('./three-products.p1-chain.spec.ts', import.meta.url), 'utf8');
  const ast = ts.createSourceFile('p1.ts', source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS);
  const functions = ast.statements.filter((node): node is ts.FunctionDeclaration => ts.isFunctionDeclaration(node)
    && ['diagnosticHead', 'captureSecondCaseFailureDiagnostics'].includes(node.name?.text ?? ''));
  assert.equal(functions.length, 2);
  const lines: string[] = [];
  const unsafe = { body: { value: 'caller-body-secret' }, principal: { name: 'caller-principal-secret' }, token: 'caller-token-secret' };
  const head = { revision_id: 'caller-revision', publication_id: 'caller-publication', ...unsafe };
  const locator = { getAttribute: async () => null, isVisible: async () => false, count: async () => 0 };
  const context = {
    DIAGNOSTIC_LIMIT: 40, commandOutboxes: async () => [], summarizeFailureOutboxes: () => [], summarizeOutboxes: () => ({ ownerCount: 0 }),
    diagnosticConnectionState: () => 'unknown', visibleDiagnostic: async () => false, diagnosticVisibleText: async () => null,
    logDiagnostic: (label: string, value: unknown) => logDiagnostic(label, value, (line) => lines.push(line)),
    logPriorityDiagnostic: (label: string, value: unknown) => logPriorityDiagnostic(label, value, (line) => lines.push(line)),
  };
  const code = functions.map((node) => node.getText(ast)).join('\n') + '\ncaptureSecondCaseFailureDiagnostics';
  const capture = runInNewContext(ts.transpileModule(code, { compilerOptions: { target: ts.ScriptTarget.ES2022 } }).outputText, context);
  await capture({
    page: { getByTestId: () => locator, locator: () => locator },
    harness: { seed: { projectId: 'project-safe' }, runtimeJson: async () => ({ body: { head } }) },
    seed: { projectSlug: 'project-safe', timelineId: 'timeline-safe', sourceId: 'source-safe' },
    traffic: { posts: [], readonlyTraffic: [] }, signals: { pageErrors: [], consoleErrors: [], requestFailures: [] },
    before: { head }, originalClip: { id: 'clip-safe', asset: 'https://private.example/unsafe-asset-secret?token=asset-token' },
    rightId: 'right-safe', split: { response: { head } }, agent: { head },
  });
  assert.equal(lines.length, 2);
  const detail = JSON.parse(lines[1].slice(lines[1].indexOf('] ') + 2));
  assert.equal(detail.sourceIdentities.beforeHead.revisionId, 'caller-revision');
  assert.equal(detail.displayedHead.runtimeHistoryHead.publicationId, 'caller-publication');
  assert.equal(detail.sourceIdentities.sourceAsset, 'UNKNOWN');
  for (const secret of ['caller-body-secret', 'caller-principal-secret', 'caller-token-secret', 'unsafe-asset-secret', 'asset-token', '"body"', '"principal"']) {
    for (const line of lines) assert.equal(line.includes(secret), false);
  }
});
