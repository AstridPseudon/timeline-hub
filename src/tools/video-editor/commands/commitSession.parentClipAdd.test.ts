import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { CanonicalDocument, CommitAcceptedMutation, CommitRequest, Transport } from '@/integrations/runtime/generated.ts';
import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineCommandBasis } from '../data/DataProvider.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import type { TimelineConfig } from '../types/index.ts';
import { document, scope } from './__tests__/commitSessionEnvironment.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { createTimelineCommandSession, type TimelineCommandSession } from './commitSession.ts';
import { ClipMoveError, copy } from './clipMovePrimitives.ts';
import { executeParentClipAdd } from './parentClipAddCapture.ts';
import { captureParentClipAddEdit, projectParentClipAddPreview, submitParentClipAddEdit } from './parentClipAddGesture.ts';
import { executeClipSet } from './clipScalarCapture.ts';
import { captureClipScalarEdit, submitClipScalarEdit } from './clipScalarGesture.ts';

const row: Record<string, JSON> = { id: 'caller-reserved', track: 'V1', clipType: 'text', at: 0.017, hold: 1.013,
  from: null, sourceURL: null, speed: null, params: { text: 'First' },
  app: { astrid: { on: null, opaque: ['caller-reserved', false] }, 'org.example': { literal: null } },
  opaque: { id: 'caller-reserved', ordered: [null, false, 0, {}, []] } };
const bytes = (value: unknown) => new TextEncoder().encode(JSON.stringify(value));
type Call = { method: string; path: string; key?: string; body?: CommitRequest; bodyBytes?: number[] };

// Fake unit transport with local native replay: App queue/preview proof only, never Runtime acceptance.
async function setup() {
  let server = document();
  server.parent_revision.payload.clips = [];
  server.parent_revision.payload.config = { ...server.parent_revision.payload.config as object, clips: [] };
  server.parent_revision.content_digest = fixtureDigest(server.parent_revision.payload);
  let head = { revisionId: 'r0', publicationId: 'p0' };
  let loseAck = false;
  const calls: Call[] = [];
  const accepted = new Map<string, { request: CommitRequest; response: CommitAcceptedMutation }>();
  const transport: Transport = async (method, path, headers, body) => {
    // TextEncoder's bytes may belong to a different realm from jsdom's Uint8Array.
    const wire = body && ArrayBuffer.isView(body) ? new Uint8Array(body.buffer, body.byteOffset, body.byteLength) : undefined;
    if (body && !wire) throw new Error('Unit transport requires bytes');
    const request = wire ? JSON.parse(new TextDecoder().decode(wire)) as CommitRequest : undefined;
    const key = headers['Idempotency-Key'];
    calls.push({ method, path, key, body: request, bodyBytes: wire ? Array.from(wire) : undefined });
    const ok = (value: unknown) => ({ status: 200, headers: {}, body: bytes(value) });
    if (path === '/v1/health') return ok({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      runtime_epoch: 1, runtime_instance_id: 'parent-add-unit' });
    if (path === '/v1/handshake') return ok({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      actor_id: scope.actorId, realm_id: scope.realmId,
      scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'],
      capabilities: ['execution_binding.targeted.v1'] });
    if (path === '/v1/realm') return ok({ realm_id: scope.realmId });
    if (path.endsWith('/commits?limit=50')) return ok({ items: [], next_cursor: null,
      head: { revision_id: head.revisionId, publication_id: head.publicationId } });
    if (path.includes('/composition-revisions/')) return ok({ project_id: scope.projectId, timeline_id: scope.timelineId,
      ...server.parent_revision, dependency_manifest: server.dependency_manifest });
    if (method !== 'POST' || !path.endsWith('/commit') || !request || !key) throw new Error(`Unexpected HTTP ${method} ${path}`);
    let saved = accepted.get(key);
    if (saved && JSON.stringify(saved.request) !== JSON.stringify(request)) throw new Error('Changed exact retry');
    if (!saved) {
      let result;
      try {
        const bundle = await authoringBundleFromDocument(server);
        const command = request.commands[0];
        if (command.op === 'clip.add') result = executeParentClipAdd(bundle, command);
        else if (command.op === 'clip.set') result = executeClipSet(bundle, command);
        else throw new Error(`Unsupported fake command ${command.op}`);
      } catch (error) {
        if (!(error instanceof ClipMoveError)) throw error;
        return { status: 409, headers: {}, body: bytes({ code: 'conflict', message: error.message,
          details: { status: 'conflict', reason: error.kind } }) };
      }
      const revision = `r${accepted.size + 1}`, publication = `p${accepted.size + 1}`;
      const payload = { ...result.bundle.parent, occurrences: copy(server.parent_revision.payload.occurrences) };
      const next: CanonicalDocument = { ...server, parent_revision: {
        revision_id: revision, content_digest: fixtureDigest(payload), payload } };
      const response = acceptedCommit({ revision_id: revision, publication_id: publication },
        { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, { commands: request.commands });
      Object.assign(response.data, { previous_revision_id: head.revisionId, previous_publication_id: head.publicationId,
        canonical_document: copy(next), document_digest: fixtureDigest(next) });
      response.receipt.result = response.data;
      response.receipt.idempotency_key = key;
      saved = { request: copy(request), response: copy(response) };
      accepted.set(key, saved);
      server = next;
      head = { revisionId: revision, publicationId: publication };
    }
    if (loseAck) { loseAck = false; throw new Error('lost acknowledgement'); }
    return ok(saved.response);
  };
  const provider = new RuntimeDataProvider({ projectId: scope.projectId,
    baseUrl: `http://parent-add-unit-${crypto.randomUUID()}.test`, token: 'unit', transport });
  const initial = await provider.loadTimelineCommandBasis(scope.timelineId);
  const display = (basis: TimelineCommandBasis): TimelineData => {
    const parent = basis.canonicalDocument.parent_revision.payload;
    const config = { ...parent.config as object, clips: parent.clips } as TimelineConfig;
    return assembleTimelineData({ config, configVersion: 1, registry: { assets: {} }, assetMap: {}, output: config.output,
      resolvedConfig: { ...config, tracks: config.tracks ?? [], registry: {} },
      head: { projectId: scope.projectId, timelineId: scope.timelineId,
        headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId } });
  };
  let current = display(initial);
  const held = new Set<string>();
  const outboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  const apply = (patch: Parameters<typeof projectParentClipAddPreview>[0]) => {
    const next = projectParentClipAddPreview(patch, current) ?? compileTimelinePatch(patch, current).nextData;
    if (!next) throw new Error('Unit preview unavailable');
    current = next;
  };
  const previews = vi.fn(apply);
  const mount = (basis = initial) => createTimelineCommandSession({ initial: basis, scope, outboxes,
    send: (request, key) => provider.commitTimeline(request, key), preview: previews, changed: () => {},
    project: async (acceptedBasis, patches) => { current = display(acceptedBasis); patches.forEach(apply); } });
  return { initial, outboxes, provider, mount, previews, current: () => current, server: () => server,
    loseAck: () => { loseAck = true; }, calls, commits: () => calls.filter((call) => call.path.endsWith('/commit')),
    external: (change: (raw: CanonicalDocument) => void) => {
      server = copy(server);
      change(server);
      server.parent_revision.revision_id = 'external-r1';
      server.parent_revision.content_digest = fixtureDigest(server.parent_revision.payload);
      head = { revisionId: 'external-r1', publicationId: 'external-p1' };
    } };
}

function add(env: Awaited<ReturnType<typeof setup>>, session: TimelineCommandSession) {
  const captured = captureParentClipAddEdit(session.parentClipAddPort, env.current(), copy(row));
  const finished = session.parentClipAddPort.finish(captured.basis);
  submitParentClipAddEdit(captured);
  return finished.command;
}

describe('native nonmedia parent birth in the one durable session', () => {
  it('queues an ordinary suffix over the reserved ID, reloads and retries identical bytes/key after a lost ACK', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    const command = add(env, session);
    expect(env.current().config.clips).toEqual([row]);
    expect(env.current().resolvedConfig.clips).toEqual([row]);
    expect(Object.hasOwn(env.current().config.clips[0], 'to')).toBe(false);
    const suffix = captureClipScalarEdit(session.clipScalarPort, env.current(), row.id as string, 'parent');
    const finish = vi.spyOn(session.clipScalarPort, 'finish');
    submitClipScalarEdit(suffix, { values: { hold: 2.017 }, clear: [] });
    const suffixCommand: EditCommand = copy(finish.mock.results[0].value.command);
    expect(suffixCommand.expect!['parent/clip:caller-reserved::hold']).toEqual({ state: 'present', value: 1.013 });
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const request = copy(env.commits()[0]);
    expect(env.commits()).toHaveLength(1);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[0].basis).toEqual({ head: env.initial.head });
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    expect(stored.intents.map((intent) => (intent.payload as unknown as { commands: EditCommand[] }).commands))
      .toEqual([[command], [suffixCommand]]);
    expect(command).toMatchObject({ op: 'clip.add', select: 'parent', args: { row }, resolved: [],
      created: ['parent/clip:caller-reserved'], expect: { 'parent/clip:caller-reserved::': { state: 'absent' } },
      selections: [{ key: 'collection.clips', owner: 'parent', members: [], order: [], boundaries: [], policy: 'guard-membership', query_version: 1 }] });
    expect(JSON.parse(stored.pending!.request.body)).toEqual(request.body);
    expect(Array.from(new TextEncoder().encode(stored.pending!.request.body))).toEqual(request.bodyBytes);
    expect(stored.pending!.request.key).toBe(request.key);
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    expect(reopened.getState().status).toBe('recovery');
    expect(env.commits()).toHaveLength(1);
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.commits()).toHaveLength(3);
    expect(env.commits()[1]).toEqual(request);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: [suffixCommand] });
    expect(env.commits()[2].key).not.toBe(request.key);
    const expected = { ...row, hold: 2.017 };
    expect(env.current().config.clips).toEqual([expected]);
    expect(env.server().parent_revision.payload.clips).toEqual([expected]);
    expect((env.server().parent_revision.payload.config as Record<string, JSON>).clips).toEqual([expected]);
    expect(env.server().parent_revision.payload.registry).toEqual(env.initial.canonicalDocument.parent_revision.payload.registry);
    expect(env.server().parent_revision.payload.occurrences).toEqual([]);
    expect(env.server().dependency_manifest).toEqual(env.initial.canonicalDocument.dependency_manifest);
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake')).toEqual(env.commits());
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    await reopened.dispose();
  });

  it('keeps the original suffix and whole-row draft when its original guard is refused after exact recovery', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    add(env, session);
    const suffix = captureClipScalarEdit(session.clipScalarPort, env.current(), row.id as string, 'parent');
    submitClipScalarEdit(suffix, { values: { hold: 2.017 }, clear: [] });
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const original = copy(stored.intents[1].payload);
    env.external((raw) => {
      const clips = raw.parent_revision.payload.clips as Record<string, JSON>[];
      clips[0].hold = 9;
      (raw.parent_revision.payload.config as Record<string, JSON>).clips = copy(clips);
    });
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(stored.ownerId);
    expect(reopened.getState().status).toBe('conflict');
    const [refused] = await env.outboxes.list(scope);
    expect(refused.intents).toHaveLength(1);
    expect(refused.intents[0].payload).toEqual(original);
    expect(refused.pending!.outcome!.kind).toBe('rejected');
    expect(env.current().config.clips).toEqual([{ ...row, hold: 2.017 }]);
    expect((env.server().parent_revision.payload.clips as Record<string, JSON>[])[0].hold).toBe(9);
    const calls = copy(env.commits());
    await reopened.retry();
    expect(env.commits()).toEqual(calls);
    expect(env.commits()[1]).toEqual(env.commits()[0]);
    await expect(reopened.flush()).rejects.toThrow();
    await reopened.dispose();
  });

  it('reserves the explicit birth ID in the same queue and fences stale or altered prepared previews', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    const capture = captureParentClipAddEdit(session.parentClipAddPort, env.current(), copy(row));
    const ready = session.parentClipAddPort.finish(capture.basis);
    expect(() => session.parentClipAddPort.submit({ ...ready, preview: { ...ready.preview, source: 'other' } })).toThrow('exact whole-row');
    session.parentClipAddPort.submit(ready);
    expect(() => captureParentClipAddEdit(session.parentClipAddPort, env.current(), copy(row))).toThrow('already displayed');
    expect(() => session.parentClipAddPort.finish(capture.basis)).toThrow('Timeline changed');
    expect(() => session.parentClipAddPort.submit(ready)).toThrow('not captured');
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(env.commits()).toHaveLength(1);
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(1);
    await session.dispose();
  });

  it('retains the original collection guard and draft when another row is inserted before submission', async () => {
    const env = await setup();
    const session = await env.mount();
    const command = add(env, session);
    env.external((raw) => {
      const clips = [{ id: 'other-author', track: 'V1', clipType: 'text', at: 3, hold: 1 }];
      raw.parent_revision.payload.clips = clips;
      (raw.parent_revision.payload.config as Record<string, JSON>).clips = copy(clips);
    });
    await vi.waitFor(() => expect(session.getState().status).toBe('conflict'));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect((stored.intents[0].payload as unknown as { commands: EditCommand[] }).commands).toEqual([command]);
    expect(stored.pending!.outcome!.kind).toBe('rejected');
    expect(env.current().config.clips).toEqual([row]);
    expect((env.server().parent_revision.payload.clips as Record<string, JSON>[]).map((clip) => clip.id)).toEqual(['other-author']);
    expect(command.selections![0].order).toEqual([]);
    expect(env.commits()).toHaveLength(1);
    await session.dispose();
  });

  it.each(['asset', 'asset_id', 'media_id', 'object_id', 'media', 'IMAGE', 'video', 'audio'])(
    'refuses unsupported %s before preview or traffic', async (unsupported) => {
      const env = await setup();
      const session = await env.mount();
      const invalid = ['asset', 'asset_id', 'media_id', 'object_id'].includes(unsupported)
        ? { ...row, [unsupported]: null } : { ...row, clipType: unsupported };
      expect(() => captureParentClipAddEdit(session.parentClipAddPort, env.current(), invalid)).toThrow('does not support');
      expect(env.previews).not.toHaveBeenCalled();
      expect(env.commits()).toEqual([]);
      expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
      await session.dispose();
    });

  it('refuses a mismatched displayed head without touching the initial projection or ordinary ports', async () => {
    const env = await setup();
    const session = await env.mount();
    const current = env.current();
    expect(() => session.parentClipAddPort.capture({ row, current: { ...current,
      head: { ...current.head!, headRevisionId: 'wrong' } } })).toThrow('raw authoring basis');
    expect(env.current()).toBe(current);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toEqual([]);
    expect(session.trackLabelPort).toBeDefined();
    expect(session.clipParamsPort).toBeDefined();
    expect(session.clipTrimPort).toBeDefined();
    expect(session.port).toBeDefined();
    await session.dispose();
  });
});
