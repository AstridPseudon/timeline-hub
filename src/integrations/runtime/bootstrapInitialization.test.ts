import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import type { MutationReceipt, MutationResult } from './generated.ts';
import type { CanonicalDocument, CommitRequest, JSON } from './timeline-commit-types.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '@/tools/video-editor/data/DataProvider.ts';
import { createCommitOutbox, type ClaimedOutbox } from '@/tools/video-editor/commands/commitOutbox.ts';
import fixture from '@/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json';
import { reserveBootstrapInitialization, resumeBootstrapInitialization } from './bootstrapInitialization.ts';
import { acceptedCommit, fixtureDigest } from './__tests__/timelineCommitFixture.ts';
import { ApiError } from './generated.ts';

const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project-1', timelineId: 'main' };
const h0 = { revisionId: 'parent-0', publicationId: 'bootstrap-p0' };
const key = 'astrid-first-timeline-project-1';
const document = (parent = fixture.bundle.parent, revision = h0.revisionId): CanonicalDocument => ({
  schema_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
  parent_revision: { revision_id: revision, content_digest: fixtureDigest({ ...parent, occurrences: [] }), payload: { ...parent, occurrences: [] } },
  shot_revisions: [], internal_timeline_revisions: [], dependency_manifest: { shots: [], internal_timelines: [], media: [], documents: [] },
});
function receipt(kind: string, id: string, idempotencyKey: string, result: unknown): MutationReceipt {
  return { receipt_id: id, command_kind: kind, idempotency_key: idempotencyKey, request_hash: 'request-hash',
    project_id: scope.projectId, project_seq: [1, 1], event_ids: ['event'], result, created_at: '2026-10-20T00:00:00Z' };
}
function initialBasis(): TimelineCommandBasis {
  const canonicalDocument = document();
  const publication = { project_id: scope.projectId, timeline_id: scope.timelineId, revision_id: h0.revisionId,
    old_head: null, new_head: h0.revisionId,
    content_digest: canonicalDocument.parent_revision.content_digest, payload: canonicalDocument.parent_revision.payload };
  return { head: h0, canonicalDocument, history: { head: { revision_id: h0.revisionId, publication_id: h0.publicationId }, next_cursor: null,
    items: [{ publication_id: h0.publicationId, revision_id: h0.revisionId, previous: null,
      receipt: receipt('parent_composition.publish', h0.publicationId, 'bootstrap:main', publication), intent: 'bootstrap',
      records: null, provider_version: null, compiler_version: null, publisher: null }] } };
}
function environment() {
  const factory = createFakeIndexedDB();
  const open = () => createCommitOutbox({ indexedDB: factory, exclusiveLock: async (_name, work) => work() });
  let basis = initialBasis();
  const created = { project_id: scope.projectId, timeline_id: scope.timelineId, archived: false,
    head_revision_id: h0.revisionId, head_publication_id: h0.publicationId };
  const createResult = () => Object.defineProperty({ ...created }, 'receipt', {
    value: receipt('timeline.create', 'create-receipt', key, created), enumerable: false,
  }) as MutationResult<Record<string, unknown>>;
  const createTimeline = vi.fn(async (_project: string, _timeline: string, _key: string, _name?: string) => createResult());
  const loadLatest = vi.fn(async () => structuredClone(basis));
  const commitTimeline = vi.fn(async (body: CommitRequest, commitKey: string): Promise<TimelineCommitResult> => {
    const response = acceptedCommit({ revision_id: 'initialized', publication_id: 'init-p1' },
      { revision_id: h0.revisionId, publication_id: h0.publicationId }, { projectId: scope.projectId, timelineId: scope.timelineId, commands: body.commands });
    const canonicalDocument = document(fixture.after_bundle.parent as typeof fixture.bundle.parent, 'initialized');
    response.data.canonical_document = canonicalDocument;
    response.data.document_digest = fixtureDigest(canonicalDocument);
    response.receipt.idempotency_key = commitKey;
    basis = { head: { revisionId: 'initialized', publicationId: 'init-p1' }, canonicalDocument };
    return { response, accepted: basis.head, canonicalDocument, graph: {}, receipt: response.receipt };
  });
  return { open, ports: { createTimeline, loadLatest, commitTimeline }, createResult,
    setBasis: (next: TimelineCommandBasis) => { basis = next; } };
}

describe('source-only create then native initialization', () => {
  it('reserves identity/defaults before POST, captures sequentially at H0, then reloads the initialized basis', async () => {
    const env = environment();
    await env.open().create(scope, async (box) => {
      await reserveBootstrapInitialization(box, 'Main', key);
      const before = await box.read();
      expect(env.ports.createTimeline).not.toHaveBeenCalled();
      expect(before.pending!.request).toEqual({ method: 'POST', path: '/v1/projects/project-1/timelines',
        body: JSON.stringify({ timeline_id: 'main', name: 'Main' }), key });
      env.ports.createTimeline.mockImplementationOnce(async () => {
        expect((await box.read()).pending).toEqual(before.pending);
        return env.createResult();
      });
      env.ports.commitTimeline.mockImplementationOnce(async (body, commitKey) => {
        const pending = (await box.read()).pending!;
        expect(pending.request.body).toBe(JSON.stringify(body));
        expect(pending.request.key).toBe(commitKey);
        expect(body).toEqual({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
          base_revision_id: h0.revisionId, base_publication_id: h0.publicationId, commands: fixture.commands, source: { via: 'app' } });
        return env.ports.commitTimeline.getMockImplementation()!(body, commitKey);
      });
      const result = await resumeBootstrapInitialization(box, env.ports);
      expect(result.canonicalDocument.parent_revision.payload).toEqual({ ...fixture.after_bundle.parent, occurrences: [] });
      expect((await box.read()).intents).toEqual([]);
    });
  });

  it('reopens the owner before first POST and after create loses its ACK, retaining exact identity and inputs', async () => {
    const env = environment();
    let owner = '';
    await env.open().create(scope, async (box, id) => { owner = id; await reserveBootstrapInitialization(box, 'Main', key); });
    env.ports.createTimeline.mockRejectedValueOnce(new Error('create ACK lost'));
    await env.open().recover(scope, owner, async (box) => {
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('create ACK lost');
    });
    const durable = (await env.open().list(scope))[0];
    expect(durable.pending?.request.key).toBe(key);
    await env.open().recover(scope, owner, async (box) => { await resumeBootstrapInitialization(box, env.ports); });
    expect(env.ports.createTimeline.mock.calls).toEqual([
      [scope.projectId, scope.timelineId, key, 'Main'], [scope.projectId, scope.timelineId, key, 'Main'],
    ]);
    expect(env.ports.commitTimeline).toHaveBeenCalledTimes(1);
  });

  it('discovers a reserved random additional timeline after restart without a remembered URL, ID or owner', async () => {
    const env = environment();
    const additional = { ...scope, timelineId: crypto.randomUUID() };
    const createKey = `astrid-timeline-create-${additional.projectId}-${additional.timelineId}`;
    await env.open().create(additional, async (box) => {
      await reserveBootstrapInitialization(box, 'Timeline 2', createKey);
    });
    const projectScope = { realmId: scope.realmId, actorId: scope.actorId, projectId: scope.projectId };
    expect(await env.open().list({ ...projectScope, actorId: 'other' })).toEqual([]);
    expect(await env.open().list({ ...projectScope, realmId: 'other' })).toEqual([]);
    expect(await env.open().list({ ...projectScope, projectId: 'other' })).toEqual([]);
    const [saved] = await env.open().list(projectScope);
    expect(saved.scope).toEqual(additional);
    expect(saved.intents[0].payload).toMatchObject({ name: 'Timeline 2', slug: 'timeline-2' });
    env.ports.createTimeline.mockRejectedValueOnce(new Error('ACK lost'));
    await env.open().recover(saved.scope, saved.ownerId, async (box) => {
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('ACK lost');
    });
    expect(env.ports.createTimeline).toHaveBeenCalledWith(scope.projectId, additional.timelineId, createKey, 'Timeline 2');
    expect((await env.open().list(projectScope))[0].pending!.request).toEqual(saved.pending!.request);
  });

  it('retains create ACK/defaults if history loading crashes before capture, then resumes without another create', async () => {
    const env = environment();
    let owner = '';
    env.ports.loadLatest.mockRejectedValueOnce(new Error('read interrupted'));
    await env.open().create(scope, async (box, id) => {
      owner = id;
      await reserveBootstrapInitialization(box, 'Main', key, null);
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('read interrupted');
      expect((await box.read()).accepted?.creation?.request.body).toBe('{"timeline_id":"main"}');
      expect((await box.read()).accepted?.value).toMatchObject({ receipt: { command_kind: 'timeline.create' } });
    });
    await env.open().recover(scope, owner, async (box) => { await resumeBootstrapInitialization(box, env.ports); });
    expect(env.ports.createTimeline).toHaveBeenCalledTimes(1);
    expect(env.ports.createTimeline).toHaveBeenCalledWith(scope.projectId, scope.timelineId, key, undefined);
  });

  it('reopens after capture is durable but before commit reservation without recapturing on a newer head', async () => {
    const env = environment();
    let owner = '';
    await env.open().create(scope, async (box, id) => {
      owner = id;
      await reserveBootstrapInitialization(box, 'Main', key);
      const dispatch = box.dispatch.bind(box);
      let calls = 0;
      box.dispatch = async (...args) => {
        if (++calls === 2) throw new Error('process stopped before init dispatch');
        return dispatch(...args);
      };
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('process stopped');
      const record = await box.read();
      expect(record.pending).toBeUndefined();
      expect(record.intents[0].payload).toEqual({ kind: 'timeline-init', commands: fixture.commands });
      expect(record.intents[0].readyBase).toEqual(h0);
    });
    env.ports.loadLatest.mockClear();
    const commit = env.ports.commitTimeline.getMockImplementation()!;
    env.ports.commitTimeline.mockImplementation(async (...args) => {
      expect(env.ports.loadLatest).not.toHaveBeenCalled();
      return commit(...args);
    });
    await env.open().recover(scope, owner, async (box) => { await resumeBootstrapInitialization(box, env.ports); });
    expect(env.ports.createTimeline).toHaveBeenCalledTimes(1);
  });

  it('reopens after init ACK is durable but display reload crashes, without another initialization', async () => {
    const env = environment();
    let owner = '';
    env.ports.loadLatest.mockResolvedValueOnce(initialBasis()).mockRejectedValueOnce(new Error('reload interrupted'));
    await env.open().create(scope, async (box, id) => {
      owner = id;
      await reserveBootstrapInitialization(box, 'Main', key);
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('reload interrupted');
      expect((await box.read()).accepted?.value).toMatchObject({ kind: 'timeline-initialized' });
      expect((await box.read()).intents).toEqual([]);
    });
    const later = { head: { revisionId: 'undo-r3', publicationId: 'undo-p3' }, canonicalDocument: document() };
    env.setBasis(later);
    await env.open().recover(scope, owner, async (box) => { expect(await resumeBootstrapInitialization(box, env.ports)).toEqual(later); });
    expect(env.ports.createTimeline).toHaveBeenCalledTimes(1);
    expect(env.ports.commitTimeline).toHaveBeenCalledTimes(1);
  });

  it('retries init after accepted/lost ACK and restart with identical request/key, without reading or recapturing today’s head', async () => {
    const env = environment();
    let owner = '';
    const commit = env.ports.commitTimeline.getMockImplementation()!;
    env.ports.commitTimeline.mockImplementationOnce(async (body, commitKey) => { await commit(body, commitKey); throw new Error('init ACK lost'); });
    await env.open().create(scope, async (box, id) => {
      owner = id;
      await reserveBootstrapInitialization(box, 'Main', key);
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('init ACK lost');
    });
    const original = (await env.open().list(scope))[0];
    const later = { head: { revisionId: 'edited-then-undone', publicationId: 'undo-p3' }, canonicalDocument: document() };
    env.setBasis(later);
    env.ports.loadLatest.mockClear();
    env.ports.commitTimeline.mockImplementation(async () => {
      expect(env.ports.loadLatest).not.toHaveBeenCalled();
      expect((await env.open().list(scope))[0].pending!.request).toEqual(original.pending!.request);
      // Exact replay returns the historical acceptance, never today's head.
      const result = await commit(...env.ports.commitTimeline.mock.calls[0]);
      env.setBasis(later);
      return result;
    });
    await env.open().recover(scope, owner, async (box) => {
      expect(await resumeBootstrapInitialization(box, env.ports)).toEqual(later);
    });
    expect(env.ports.commitTimeline.mock.calls[1]).toEqual(env.ports.commitTimeline.mock.calls[0]);
    expect(env.ports.createTimeline).toHaveBeenCalledTimes(1);
    expect(env.ports.loadLatest).toHaveBeenCalledTimes(1);
    await env.open().recover(scope, owner, async (box) => {
      expect(await resumeBootstrapInitialization(box, env.ports)).toEqual(later);
    });
    expect(env.ports.commitTimeline).toHaveBeenCalledTimes(2);
  });

  it.each(['advanced', 'publication', 'extra-history', 'cursor', 'receipt', 'scope', 'opaque', 'manifest', 'no-history'])('retains the draft and refuses fresh capture for %s even if displayed empty bytes match', async (fault) => {
    const env = environment();
    const basis = initialBasis();
    if (fault === 'advanced') basis.head = { revisionId: h0.revisionId, publicationId: 'undo-p3' };
    if (fault === 'publication') basis.history!.items[0].receipt.receipt_id = 'create-receipt';
    if (fault === 'extra-history') basis.history!.items.push(structuredClone(basis.history!.items[0]));
    if (fault === 'cursor') basis.history!.next_cursor = 'more-history';
    if (fault === 'receipt') basis.history!.items[0].receipt.project_id = 'other-project';
    if (fault === 'scope') basis.canonicalDocument.timeline_id = 'other-timeline';
    if (fault === 'opaque') {
      basis.canonicalDocument.parent_revision.payload.opaque = [null, { order: [3, 1, 2] }];
      const result = basis.history!.items[0].receipt.result as { payload: unknown };
      result.payload = structuredClone(basis.canonicalDocument.parent_revision.payload);
    }
    if (fault === 'manifest') basis.canonicalDocument.dependency_manifest.media.push({ media_id: 'media', content_digest: 'digest' });
    if (fault === 'no-history') delete basis.history;
    env.setBasis(basis);
    await env.open().create(scope, async (box) => {
      await reserveBootstrapInitialization(box, 'Main', key);
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow(/bootstrap|pristine/);
      expect((await box.read()).accepted?.creation).toBeDefined();
      expect(env.ports.commitTimeline).not.toHaveBeenCalled();
      expect(await env.ports.loadLatest(scope.timelineId)).toEqual(basis);
    });
  });

  it('does not fabricate H0 when the provider returns a headless create, and retains the exact flight', async () => {
    const env = environment();
    env.ports.createTimeline.mockResolvedValueOnce(Object.assign(env.createResult(), { head_publication_id: null }));
    await env.open().create(scope, async (box) => {
      await reserveBootstrapInitialization(box, 'Main', key);
      const original = await box.read();
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('tracked timeline');
      expect((await box.read()).pending!.request).toEqual(original.pending!.request);
      expect((await box.read()).accepted).toBeUndefined();
      expect(env.ports.loadLatest).not.toHaveBeenCalled();
      expect(env.ports.commitTimeline).not.toHaveBeenCalled();
    });
  });

  it('retains original native commands on a definitive intervening-write conflict', async () => {
    const env = environment();
    env.ports.commitTimeline.mockRejectedValueOnce(new ApiError(409, 'conflict', 'intervening_write', '', { status: 'conflict' }));
    await env.open().create(scope, async (box) => {
      await reserveBootstrapInitialization(box, 'Main', key);
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('intervening_write');
      const record = await box.read();
      expect((record.intents[0].payload as { commands: JSON }).commands).toEqual(fixture.commands);
      expect(record.intents[0].readyBase).toEqual(h0);
      expect(record.pending?.outcome?.kind).toBe('rejected');
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('rejected prefix');
      expect(env.ports.commitTimeline).toHaveBeenCalledTimes(1);
    });
  });

  it('retains an uncertain init flight when its returned receipt belongs to a different request', async () => {
    const env = environment();
    const commit = env.ports.commitTimeline.getMockImplementation()!;
    env.ports.commitTimeline.mockImplementationOnce(async (...args) => {
      const result = await commit(...args);
      result.response.receipt.idempotency_key = 'another-request';
      return result;
    });
    await env.open().create(scope, async (box) => {
      await reserveBootstrapInitialization(box, 'Main', key);
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('receipt does not match');
      const record = await box.read();
      expect(record.pending?.outcome?.kind).toBe('retry');
      expect(record.intents).toHaveLength(1);
      expect(record.accepted?.head).toEqual(h0);
    });
  });

  it('refuses unsupported names and owners without a reserved initialization', async () => {
    const env = environment();
    await env.open().create(scope, async (box: ClaimedOutbox) => {
      await expect(reserveBootstrapInitialization(box, '', key)).rejects.toThrow('nonempty');
      await expect(reserveBootstrapInitialization(box, 'x'.repeat(121), key)).rejects.toThrow('nonempty');
      await expect(resumeBootstrapInitialization(box, env.ports)).rejects.toThrow('No acknowledged');
      expect(env.ports.createTimeline).not.toHaveBeenCalled();
    });
  });
});
