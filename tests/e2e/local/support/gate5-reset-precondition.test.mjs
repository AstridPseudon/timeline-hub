import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { createFakeIndexedDB } from 'fake-indexeddb';
import ts from 'typescript';
import { createCommitOutbox } from '../../../../src/tools/video-editor/commands/commitOutbox.ts';
import { dragTimelineClip } from './app.ts';
import { assertGate5ResetPrecondition } from './gate5-reset-precondition.ts';

// Offline control only: these request/response/outbox objects are mocked and do not prove a browser or Runtime journey.
const base = { revisionId: 'revision-before', publicationId: 'publication-before' };
const scope = { projectId: 'project-f2', timelineId: 'timeline-f2' };
const clipId = 'f2-app-clip';
const trackId = 'V1';
const changes = [{ op: 'set', ref: 'parent', path: ['clips', `id:${clipId}`, 'at'], before: { state: 'present', value: 0 }, value: 5 }];
const reads = [
  ...[['id', clipId], ['track', trackId], ['at', 0], ['clipType', 'media'], ['hold', undefined], ['from', 0], ['to', 3], ['speed', 1], ['asset', 'f2-app']]
    .map(([key, value]) => ({ kind: 'field', ref: 'parent', path: ['config', 'clips', `id:${clipId}`, key], state: value === undefined ? { state: 'absent' } : { state: 'present', value } })),
  { kind: 'field', ref: 'parent', path: ['config', 'output', 'fps'], state: { state: 'present', value: 30 } },
  { kind: 'field', ref: 'parent', path: ['config', 'registry', 'assets', 'f2-app'], state: { state: 'present', value: { file: 'f2-app.png', type: 'image/png' } } },
  { kind: 'field', ref: 'parent', path: ['config', 'tracks', `id:${trackId}`, 'kind'], state: { state: 'present', value: 'visual' } },
  { kind: 'field', ref: 'parent', path: ['config', 'pinnedShotGroups'], state: { state: 'absent' } },
  { kind: 'collection', ref: 'parent', path: ['config', 'clips'], members: ['f2-app-clip', 'f2-transition-clip'], order: ['f2-app-clip', 'f2-transition-clip'] },
  ...[['track', trackId], ['id', 'f2-transition-clip'], ['at', 15], ['track', trackId], ['clipType', 'media'], ['hold', undefined], ['from', 0], ['to', 3], ['speed', 1], ['asset', 'f2-video']]
    .map(([key, value]) => ({ kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:f2-transition-clip', key], state: value === undefined ? { state: 'absent' } : { state: 'present', value } })),
  { kind: 'field', ref: 'parent', path: ['config', 'registry', 'assets', 'f2-video'], state: { state: 'present', value: { file: 'f2-video.mp4', type: 'video/mp4' } } },
];
const command = { schema_version: 1, op: 'doc.patch', version: '1', select: null, created: [], args: { changes } };
const request = {
  api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
  base_revision_id: base.revisionId,
  base_publication_id: base.publicationId,
  commands: [command], label: 'Edit timeline', steps: [{ id: 'setup-step', label: 'Edit timeline', intent: `Move ${clipId} on ${trackId}`, tags: [], command_ordinals: [0], patch: changes, reads }],
  merge: 'fields', reads, dry_run: false, source: { via: 'app' },
};
const responseCommand = { ...command, intent: {}, resolved: [], expect: {}, authorship: {}, reads: [], selections: {}, bindings: {}, created: [] };
const data = {
  status: 'accepted', base_revision_id: base.revisionId, base_publication_id: base.publicationId,
  previous_revision_id: base.revisionId, previous_publication_id: base.publicationId,
  accepted_revision_id: 'revision-after', rebased_onto: null, commands: [responseCommand], document_digest: 'sha256:document', id_map: {},
  provider_version: 'provider-v2', compiler_version: 'compiler-v2', publisher: 'publisher-v2', merge_mode: 'fields', label: request.label, source: request.source,
  steps: [{ ...request.steps[0], patch: [{ ...changes[0], path: ['config', ...changes[0].path] }], dependencies: [] }],
  canonical_document: { schema_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
    parent_revision: { revision_id: 'revision-after', content_digest: 'sha256:parent', payload: { config: { clips: [{ id: clipId, at: 5 }], tracks: [{ id: trackId, kind: 'visual' }], output: { fps: 30 } }, clips: [{ id: clipId, at: 5 }] } },
    shot_revisions: [], internal_timeline_revisions: [], dependency_manifest: { shots: [], internal_timelines: [], media: [], documents: [] } },
};
const response = { data, receipt: { receipt_id: 'publication-after', command_kind: 'timeline.commit', idempotency_key: 'setup-key', request_hash: 'hash', project_id: scope.projectId, project_seq: [1, 1], event_ids: ['event-1'], result: data } };
const settled = [{ pending: null, intents: [] }];
const authoritativeHead = { revision_id: 'revision-after', publication_id: 'publication-after' };
const authoritativeRevision = { project_id: scope.projectId, timeline_id: scope.timelineId, revision_id: 'revision-after', payload: { config: { clips: [{ id: clipId, at: 5 }] }, clips: [{ id: clipId, at: 5 }] } };
const valid = {
  request, requestIdentity: request, responseRequest: request, requestIdempotencyKey: 'setup-key',
  responseStatus: 200, responseBody: response, expectedBase: base, expectedScope: scope,
  clipId, expectedTrackId: trackId, expectedPreviousPosition: 0, expectedPosition: 5, settledOutboxes: settled, authoritativeHead, authoritativeRevision,
};

const responseFor = (nextData) => ({ ...response, data: nextData, receipt: { ...response.receipt, result: nextData } });

test('Gate5 requires the real 0→5 response before the original reset', () => {
  assert.doesNotThrow(() => assertGate5ResetPrecondition(valid));
});

test('the isolated 0-start cannot satisfy a 5→0 reset precondition without a setup mutation', () => {
  const oldStartData = { ...data, canonical_document: { ...data.canonical_document,
    parent_revision: { ...data.canonical_document.parent_revision,
      payload: { ...data.canonical_document.parent_revision.payload,
        config: { ...data.canonical_document.parent_revision.payload.config, clips: [{ id: clipId, at: 0 }] },
        clips: [{ id: clipId, at: 0 }] } } } };
  assert.throws(() => assertGate5ResetPrecondition({
    ...valid, responseStatus: 200, responseBody: { data: oldStartData, receipt: { receipt_id: 'publication-old', result: oldStartData } },
    request: { ...request, commands: [{ ...command, args: { changes: [{ ...changes[0], value: 0 }] } }] },
  }), /requested position mismatch/);
});

test('Gate5 fails closed for non-200, missing response, invalid receipt, and mismatched position', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseStatus: 409 }), /response status 409/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseStatus: undefined, responseBody: undefined }), /response status/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, expectedPosition: 4 }), /requested position mismatch/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: { ...response, receipt: { ...response.receipt, result: {} } } }), /receipt does not match/);
  const mismatchedData = { ...data, canonical_document: { ...data.canonical_document, project_id: scope.projectId, timeline_id: scope.timelineId,
    parent_revision: { ...data.canonical_document.parent_revision, revision_id: 'revision-after',
      payload: { ...data.canonical_document.parent_revision.payload,
        config: { ...data.canonical_document.parent_revision.payload.config, clips: [{ id: clipId, at: 4 }] },
        clips: [{ id: clipId, at: 4 }] } } } };
  assert.throws(() => assertGate5ResetPrecondition({
    ...valid, responseBody: responseFor(mismatchedData),
  }), /canonical position mismatch/);
});

test('Gate5 rejects unrelated responses and wrong scope, head, base, previous, key, or command identity', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseRequest: {} }), /not for the setup request/);
  const wrongScopeRequest = { ...request, project_id: 'other-project' };
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: wrongScopeRequest, requestIdentity: wrongScopeRequest, responseRequest: wrongScopeRequest }), /project scope/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeHead: { revision_id: 'other', publication_id: authoritativeHead.publication_id } }), /authoritative head/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: { ...request, base_revision_id: 'other' }, requestIdentity: request, responseRequest: request }), /base revision/);
  const wrongPrevious = { ...data, previous_revision_id: 'other' };
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: responseFor(wrongPrevious) }), /previous head/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, requestIdempotencyKey: 'other-key' }), /idempotency/);
  const wrongCommand = { ...request, commands: [{ ...command, op: 'track.create' }] };
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: wrongCommand, requestIdentity: wrongCommand, responseRequest: wrongCommand }), /mounted document patch/);
});

test('Gate5 rejects an authoritative readback with the wrong scope or position', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeRevision: { ...authoritativeRevision, timeline_id: 'other-timeline' } }), /authoritative revision scope/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeRevision: { ...authoritativeRevision, payload: { ...authoritativeRevision.payload,
    config: { clips: [{ id: clipId, at: 4 }] }, clips: [{ id: clipId, at: 4 }] } } }), /authoritative position/);
});

test('Gate5 refuses queued and pending records from the real outbox until acknowledgement settles them', async () => {
  const outbox = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (_name, work) => work() });
  await outbox.create({ ...scope, realmId: 'realm', actorId: 'actor' }, async (box) => {
    const check = async () => ({ ...valid, settledOutboxes: [await box.read()] });
    const initial = await check();
    assert.doesNotThrow(() => assertGate5ResetPrecondition(initial));
    const intentId = await box.append({ commands: request.commands }, { head: base });
    const queued = await check();
    assert.equal(queued.settledOutboxes[0].pending, undefined);
    assert.equal(queued.settledOutboxes[0].intents[0].id, intentId);
    assert.throws(() => assertGate5ResetPrecondition(queued), /owner is not settled/);
    await box.dispatch(() => ({ method: 'POST', path: `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}/commit`, body: request }),
      async () => ({ kind: 'retry', error: { code: 'offline-control' } }));
    const pending = await check();
    assert.equal(pending.settledOutboxes[0].pending.intentId, intentId);
    assert.throws(() => assertGate5ResetPrecondition(pending), /owner is still pending/);
    await box.dispatch(() => { throw new Error('An exact pending retry must reuse its request'); },
      async () => ({ kind: 'accepted', head: { revisionId: 'revision-after', publicationId: 'publication-after' }, value: response }));
    const acknowledged = await check();
    assert.doesNotThrow(() => assertGate5ResetPrecondition(acknowledged));
    assert.throws(() => assertGate5ResetPrecondition({ ...acknowledged, settledOutboxes: [...acknowledged.settledOutboxes, ...pending.settledOutboxes] }), /owner is still pending/);
  });
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, settledOutboxes: [] }), /owner is missing/);
});

test('Gate5 refuses a mismatched authoritative publication, revision identity, or project', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeHead: { ...authoritativeHead, publication_id: 'other-publication' } }), /authoritative head mismatch/);
  for (const mismatch of [{ project_id: 'other-project' }, { revision_id: 'other-revision' }]) {
    assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeRevision: { ...authoritativeRevision, ...mismatch } }), /authoritative revision scope mismatch/);
  }
});

test('Gate5 refuses successful HTTP replies with non-accepted outcomes or mismatched response identity', () => {
  for (const status of ['merged', 'rebased', 'conflict', 'invalid', 'preview']) {
    assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: responseFor({ ...data, status }) }), /was not accepted/);
  }
  for (const mismatch of [
    { base_revision_id: 'other-revision' }, { base_publication_id: 'other-publication' },
    { previous_revision_id: 'other-revision' }, { previous_publication_id: 'other-publication' },
    { commands: [{ ...command, args: { changes: [{ ...changes[0], value: 0 }] } }] },
  ]) {
    assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: responseFor({ ...data, ...mismatch }) }), /response (base|previous head|command) mismatch/);
  }
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseStatus: 200, responseBody: undefined }), /response is missing/);
});

test('Gate5 refuses missing or invalid receipts and idempotency keys', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: { data } }), /receipt is missing/);
  for (const [mismatch, error] of [
    [{ receipt_id: '' }, /receipt id is missing/],
    [{ idempotency_key: 'other-key' }, /receipt idempotency mismatch/],
    [{ command_kind: 'timeline.undo' }, /receipt command mismatch/],
    [{ project_id: 'other-project' }, /receipt project mismatch/],
    [{ result: { ...data, accepted_revision_id: 'other-revision' } }, /receipt does not match/],
  ]) {
    assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: { ...response, receipt: { ...response.receipt, ...mismatch } } }), error);
  }
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, requestIdempotencyKey: '' }), /request idempotency key is missing/);
});

test('Gate5 refuses wrong canonical scope, accepted revision, or clip even with a matching receipt', () => {
  for (const mismatch of [{ project_id: 'other-project' }, { timeline_id: 'other-timeline' }]) {
    const canonical_document = { ...data.canonical_document, ...mismatch };
    assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: responseFor({ ...data, canonical_document }) }), /canonical scope mismatch/);
  }
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: responseFor({ ...data, accepted_revision_id: 'other-revision' }) }), /canonical revision mismatch/);
  const canonical_document = { ...data.canonical_document, parent_revision: { ...data.canonical_document.parent_revision,
    payload: { ...data.canonical_document.parent_revision.payload, config: { ...data.canonical_document.parent_revision.payload.config, clips: [{ id: 'other-clip', at: 5 }] }, clips: [{ id: 'other-clip', at: 5 }] } } };
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: responseFor({ ...data, canonical_document }) }), /canonical clip is missing/);
});

test('Gate5 refuses setup requests with the wrong timeline, publication, or target clip', () => {
  for (const [mismatch, error] of [
    [{ timeline_id: 'other-timeline' }, /timeline scope mismatch/],
    [{ base_publication_id: 'other-publication' }, /base publication mismatch/],
    [{ commands: [{ ...command, args: { changes: [{ ...changes[0], path: ['clips', 'id:other-clip', 'at'] }] } }] }, /clip mismatch/],
  ]) {
    assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: { ...request, ...mismatch } }), error);
  }
});

test('Gate5 refuses an authentic-looking setup with wrong before/value, readset, or claims', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: {
    ...request, commands: [{ ...command, args: { changes: [{ ...changes[0], before: { state: 'present', value: 1 } }] } }],
  } }), /previous position/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: {
    ...request, commands: [{ ...command, args: { changes: [{ ...changes[0], value: 4 }] } }],
  } }), /requested position/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: { ...request,
    reads: [{ ...reads[0], path: ['config', 'clips', 'id:other-clip', 'at'] }] } }), /step claims/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: {
    ...request, steps: [{ ...request.steps[0], intent: 'Save local editor changes' }],
  } }), /step claims/);
});

test('the actual Gate5 setup listens before the real drag helper drops, and ignores another POST reply', async () => {
  // Execute the caller's waiter/gesture slice, not a copy of its scheduling logic. Page events and geometry are offline doubles.
  const spec = readFileSync(new URL('../three-products.spec.ts', import.meta.url), 'utf8');
  const start = spec.indexOf('  const preconditionRequest =');
  const end = spec.indexOf('  const setupBody = await setupResponse.json();', start);
  assert.ok(start > 0 && end > start);
  const source = spec.slice(start, end) + '\nreturn { setupRequest, setupResponse };';
  const compiled = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext } }).outputText;
  const run = new (Object.getPrototypeOf(async () => {}).constructor)(
    'page', 'preconditionBase', 'timelineBase', 'harness', 'seed3', 'CEILING', 'dragTimelineClip', 'THREE_PRODUCTS_REFERENCE_AT', compiled);
  const events = new EventEmitter();
  const wait = (event, predicate) => new Promise((resolve, reject) => {
    const listener = async (value) => {
      try {
        if (await predicate(value)) { events.off(event, listener); resolve(value); }
      } catch (error) { reject(error); }
    };
    events.on(event, listener);
  });
  const setupRequest = { method: () => 'POST', url: () => 'https://offline.invalid/api/runtime/v1/projects/project-f2/timelines/timeline-f2/commit', postDataJSON: () => request };
  const wrongMoveRequest = { ...setupRequest, postDataJSON: () => ({ ...request, commands: [{ ...request.commands[0], args: { on: 0 } }] }) };
  const unrelatedRequest = { ...setupRequest }; // An already in-flight POST with identical bytes still has a different identity.
  const setupResponse = { request: () => setupRequest };
  const geometry = (x) => ({ _apiName: 'Locator', _expect: async () => ({ matches: true }), first() { return this; }, boundingBox: async () => ({ x, y: 0, width: 40, height: 20 }) });
  const page = {
    locator: (selector) => geometry(selector.includes('f2-app-clip') ? 0 : 100),
    waitForRequest: (predicate) => wait('request', predicate),
    waitForResponse: (predicate) => wait('response', predicate),
    mouse: {
      move: async () => {}, down: async () => {},
      up: async () => {
        assert.equal(events.listenerCount('response'), 1, 'A fast mounted reply can arrive during mouse.up before dragTimelineClip returns');
        events.emit('request', wrongMoveRequest);
        events.emit('response', { request: () => unrelatedRequest });
        events.emit('request', setupRequest);
        events.emit('response', setupResponse);
      },
    },
  };
  const result = await run(page, { head: { revision_id: base.revisionId, publication_id: base.publicationId } },
    () => '/v1/projects/project-f2/timelines/timeline-f2', {}, { appClipId: 'f2-app-clip', transitionClipId: 'reference' }, {}, dragTimelineClip, 10);
  assert.equal(result.setupRequest, setupRequest);
  assert.equal(result.setupResponse, setupResponse);
});
