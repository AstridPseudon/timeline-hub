import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync } from 'node:fs';
import { test } from 'node:test';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import type { Request, Response } from '@playwright/test';
import { ElementApplyDiagnosticCollector, installElementApplyDiagnostic, readElementApplyUiState, retainElementApplyDiagnostic, serializeElementApplyDiagnostic, type ElementApplyDiagnosticArtifact } from './p2-element-diagnostic.ts';

function applyBody(intent = 'timeline.apply_element'): Record<string, unknown> {
  const changes = [{ op: 'list.insert', ref: 'parent', path: ['config', 'clips'], before: { state: 'absent' }, id: 'element-1', value: { id: 'element-1' }, order_before: [], after_id: null }];
  return {
    api_version: 1, project_id: 'private-project', timeline_id: 'private-timeline', base_revision_id: 'private-revision', base_publication_id: 'private-publication',
    commands: [{ schema_version: 1, op: 'doc.patch', version: '1', select: null, created: ['parent/clip:element-1'], args: { changes } }],
    label: 'Edit timeline', merge: 'atomic', reads: [], dry_run: false, source: { via: 'app' },
    steps: [{ id: 'private-step', label: 'Edit timeline', intent, tags: [], command_ordinals: [0], patch: changes, reads: [] }],
  };
}

function request(failure?: string, kind: 'target' | 'unrelated' = 'target', route = '/v1'): Request {
  return {
    method: () => 'POST',
    url: () => `https://runtime.invalid${route}/projects/private/timelines/private/commit?secret=private`,
    headers: () => ({ 'idempotency-key': 'private-key', authorization: 'Bearer private' }),
    failure: () => failure ? { errorText: failure } : null,
    postDataJSON: () => kind === 'target' ? applyBody() : { ...applyBody('other.operation'), authorization: 'Bearer body-secret' },
  } as unknown as Request;
}

function response(source: Request, status: number): Response {
  return { request: () => source, status: () => status } as unknown as Response;
}

function stages(collector: ElementApplyDiagnosticCollector): string[] {
  return collector.snapshot().events.map((event) => event.stage);
}

function installerPage(): { page: unknown; emit(event: string, value?: unknown): void; apply(): void } {
  const listeners = new Map<string, Array<(value?: unknown) => void>>();
  let exposed: (() => void) | undefined;
  let releaseExpose: (() => void) | undefined;
  const page = {
    on(event: string, listener: (value?: unknown) => void) {
      listeners.set(event, [...(listeners.get(event) ?? []), listener]);
    },
    exposeFunction(_name: string, callback: () => void) {
      exposed = callback;
      return new Promise<void>((resolve) => { releaseExpose = resolve; });
    },
    addInitScript: async () => {},
  };
  return {
    page,
    emit(event, value) { for (const listener of listeners.get(event) ?? []) listener(value); },
    apply() { exposed?.(); releaseExpose?.(); },
  };
}

test('accepted Apply records the real boundary, scoped request and response in order', () => {
  const collector = new ElementApplyDiagnosticCollector();
  const post = request();
  collector.recordApplyClick();
  collector.recordRequest(post);
  collector.recordResponse(response(post, 200));
  assert.deepEqual(stages(collector), ['apply-click', 'request-start', 'response']);
  const snapshot = collector.snapshot();
  assert.equal(snapshot.terminal, 'accepted');
  assert.equal(snapshot.events[1]?.request, 'scoped-commit');
  assert.equal(snapshot.events[1]?.idempotencyKey, 'present');
  assert.equal(snapshot.events[2]?.responseStatus, 200);
  assert.equal(snapshot.events[2]?.terminal, 'accepted');
  assert.doesNotMatch(JSON.stringify(snapshot), /runtime\.invalid|private-key|Bearer|authorization|secret/);
});

test('the installer retains a fast target POST before the expose callback and ignores an unrelated commit', async () => {
  const collector = new ElementApplyDiagnosticCollector();
  const mock = installerPage();
  const install = installElementApplyDiagnostic(mock.page as never, collector);
  const target = request(undefined, 'target', '/api/runtime/v1');
  mock.emit('request', target);
  mock.emit('request', request(undefined, 'unrelated', '/api/runtime/v1'));
  mock.emit('response', response(target, 201));
  mock.apply();
  await install;
  mock.emit('close');
  assert.deepEqual(stages(collector), ['apply-click', 'request-start', 'response', 'page-close']);
  assert.equal(collector.snapshot().terminal, 'accepted');
  assert.equal(collector.snapshot().events[1]?.request, 'scoped-commit');
});

test('the installed target failure remains failed through page close', async () => {
  const collector = new ElementApplyDiagnosticCollector();
  const mock = installerPage();
  const install = installElementApplyDiagnostic(mock.page as never, collector);
  mock.apply();
  const target = request('net::ERR_FAILED', 'target', '/api/runtime/v1');
  mock.emit('request', target);
  mock.emit('requestfailed', target);
  await install;
  mock.emit('close');
  assert.deepEqual(stages(collector), ['apply-click', 'request-start', 'request-failed', 'page-close']);
  assert.equal(collector.snapshot().terminal, 'failed');
});

test('an error response is terminal failed and is not relabeled as accepted', () => {
  const collector = new ElementApplyDiagnosticCollector();
  const post = request();
  collector.recordApplyClick();
  collector.recordRequest(post);
  collector.recordResponse(response(post, 409));
  const event = collector.snapshot().events.at(-1);
  assert.equal(event?.stage, 'response');
  assert.equal(event?.response, 'failure');
  assert.equal(event?.terminal, 'failed');
  assert.equal(collector.snapshot().terminal, 'failed');
});

test('request abort records aborted even when no response exists', () => {
  const collector = new ElementApplyDiagnosticCollector();
  const post = request('net::ERR_ABORTED');
  collector.recordApplyClick();
  collector.recordRequest(post);
  collector.recordRequestFailed(post);
  const event = collector.snapshot().events.at(-1);
  assert.equal(event?.stage, 'request-failed');
  assert.equal(event?.failure, 'aborted');
  assert.equal(event?.terminal, 'aborted');
  assert.equal(collector.snapshot().pageClosed, false);
});

test('page close retains pending versus unknown without inventing a response', () => {
  const pending = new ElementApplyDiagnosticCollector();
  const post = request();
  pending.recordApplyClick();
  pending.recordRequest(post);
  pending.recordPageClose();
  assert.equal(pending.snapshot().terminal, 'aborted');
  assert.equal(pending.snapshot().events.at(-1)?.stage, 'page-close');
  assert.equal(pending.snapshot().events.at(-1)?.responseStatus, 'UNKNOWN');

  const unknown = new ElementApplyDiagnosticCollector();
  unknown.recordApplyClick();
  unknown.recordPageClose();
  assert.equal(unknown.snapshot().terminal, 'unknown');
  assert.equal(unknown.snapshot().events.at(-1)?.terminal, 'unknown');
});

test('the retained writer emits bounded JSON for a failed page close', async () => {
  const directory = mkdtempSync(join(process.env.TMPDIR ?? tmpdir(), 'p2-element-diagnostic-'));
  const output = join(directory, 'p2-element-apply-diagnostic.json');
  const collector = new ElementApplyDiagnosticCollector();
  collector.recordApplyClick();
  collector.recordPageClose();
  const attached: string[] = [];
  const retained = await retainElementApplyDiagnostic({
    outputPath(name) { assert.equal(name, 'p2-element-apply-diagnostic.json'); return output; },
    async attach(name, options) { attached.push(name); assert.equal(options.contentType, 'application/json'); },
  }, undefined, collector, 'failed');
  assert.equal(retained, true);
  assert.deepEqual(attached, ['p2-element-apply-diagnostic.json']);
  const artifact = JSON.parse(readFileSync(output, 'utf8')) as ElementApplyDiagnosticArtifact;
  assert.equal(artifact.status, 'observed');
  assert.equal(artifact.lifecycle.testOutcome, 'failed');
  assert.equal(artifact.lifecycle.pageClosed, true);
  assert.equal((artifact.diagnostic as Exclude<ElementApplyDiagnosticArtifact['diagnostic'], 'UNKNOWN'>).events.at(-1)?.terminal, 'unknown');
  assert.ok(readFileSync(output, 'utf8').length < 24 * 1024);
});

test('the retained writer keeps real allowlisted page state and redacts malicious fields', async () => {
  const priorDocument = (globalThis as { document?: unknown }).document;
  (globalThis as { document?: unknown }).document = {
    querySelector(selector: string) {
      if (selector === '[data-testid="runtime-connection-status"]') return { getAttribute: () => 'connected' };
      if (selector === '[role="dialog"]') return { querySelector: () => ({ textContent: 'Applied private DOM text' }) };
      return null;
    },
  };
  try {
    assert.deepEqual(readElementApplyUiState(), { stage: 'retained', connection: 'connected', dialog: 'present', status: 'applied' });
  } finally {
    if (priorDocument === undefined) delete (globalThis as { document?: unknown }).document;
    else (globalThis as { document?: unknown }).document = priorDocument;
  }
  const directory = mkdtempSync(join(process.env.TMPDIR ?? tmpdir(), 'p2-element-diagnostic-ui-'));
  const output = join(directory, 'p2-element-apply-diagnostic.json');
  const collector = new ElementApplyDiagnosticCollector();
  collector.recordApplyClick();
  const retained = await retainElementApplyDiagnostic({
    outputPath() { return output; },
    async attach() {},
  }, { evaluate: async () => ({ stage: 'retained', connection: 'connected', dialog: 'present', status: 'applied', authorization: 'Bearer secret', domText: 'private DOM text' }) }, collector, 'passed');
  assert.equal(retained, true);
  const serialized = readFileSync(output, 'utf8');
  assert.doesNotMatch(serialized, /Bearer secret|private DOM text|authorization|domText/);
  assert.match(serialized, /"connection":"connected"/);
});

test('the collector caps retained events at its bound', () => {
  const collector = new ElementApplyDiagnosticCollector();
  for (let index = 0; index < 40; index += 1) collector.recordApplyClick();
  const events = collector.snapshot().events;
  assert.equal(events.length, 24);
  assert.equal(events.at(-1)?.sequence, 24);
});

test('an attachment failure is reported instead of success', async () => {
  const directory = mkdtempSync(join(process.env.TMPDIR ?? tmpdir(), 'p2-element-diagnostic-attach-'));
  const collector = new ElementApplyDiagnosticCollector();
  collector.recordApplyClick();
  const retained = await retainElementApplyDiagnostic({
    outputPath() { return join(directory, 'p2-element-apply-diagnostic.json'); },
    async attach() { throw new Error('attachment failed'); },
  }, undefined, collector, 'failed');
  assert.equal(retained, false);
});

test('serialization falls back to the safe loss marker when supplied data exceeds the bound', () => {
  const artifact = {
    version: 1 as const,
    kind: 'p2-element-apply-lifecycle' as const,
    status: 'observed' as const,
    lifecycle: { testOutcome: 'failed' as const, beforePageClose: true, pageClosed: false },
    diagnostic: 'x'.repeat(100_000) as 'UNKNOWN',
    losses: { write: false, events: false, ui: false },
  } satisfies ElementApplyDiagnosticArtifact;
  const serialized = serializeElementApplyDiagnostic(artifact);
  assert.match(serialized, /"diagnostic":"UNKNOWN"/);
  assert.ok(Buffer.byteLength(serialized) < 24 * 1024);
});
