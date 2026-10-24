import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync } from 'node:fs';
import { test } from 'node:test';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import type { Request, Response } from '@playwright/test';
import { ElementApplyDiagnosticCollector, retainElementApplyDiagnostic, serializeElementApplyDiagnostic, type ElementApplyDiagnosticArtifact } from './p2-element-diagnostic.ts';

function request(failure?: string): Request {
  return {
    method: () => 'POST',
    url: () => 'https://runtime.invalid/v1/projects/private/timelines/private/commit?secret=private',
    headers: () => ({ 'idempotency-key': 'private-key', authorization: 'Bearer private' }),
    failure: () => failure ? { errorText: failure } : null,
  } as unknown as Request;
}

function response(source: Request, status: number): Response {
  return { request: () => source, status: () => status } as unknown as Response;
}

function stages(collector: ElementApplyDiagnosticCollector): string[] {
  return collector.snapshot().events.map((event) => event.stage);
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
