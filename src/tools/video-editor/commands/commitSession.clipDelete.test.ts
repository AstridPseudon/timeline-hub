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
import { environment, document, scope } from './__tests__/commitSessionEnvironment.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { createTimelineCommandSession, type TimelineCommandSession } from './commitSession.ts';
import { AuthoredState, ClipMoveError, copy } from './clipMovePrimitives.ts';
import { executeClipDelete } from './clipDeleteCapture.ts';
import { executeClipMove } from './clipMoveCapture.ts';
import { finishTrackLabel, type TrackLabelArgs } from './trackLabelCapture.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from './trackLabelGesture.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';
import { captureClipDeleteEdit, projectClipDeletePreview, submitClipDeleteEdit } from './clipDeleteGesture.ts';

import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';

function projectedDisplay(env: Awaited<ReturnType<typeof environment>>): TimelineData {
  const composition = createShotCompositionAdapter({ load: async () => env.initial.graph }).prepare(env.initial.graph);
  const { config } = projectCanonicalComposition(composition, { ...env.current().resolvedConfig,
    clips: structuredClone(env.initial.canonicalDocument.parent_revision.payload.clips) as TimelineData['config']['clips'],
  });
  return { ...env.current(), config, resolvedConfig: config };
}

const survivor: Record<string, JSON> = { id: 'caller-reserved', track: 'V1', clipType: 'text', at: 0.017, hold: 1.013,
  from: null, sourceURL: null, speed: null, params: { text: 'First' },
  app: { astrid: { on: null, opaque: ['caller-reserved', false] }, 'org.example': { literal: null } },
  opaque: { id: 'caller-reserved', ordered: [null, false, 0, {}, []] } };
const bytes = (value: unknown) => new TextEncoder().encode(JSON.stringify(value));
type Call = { method: string; path: string; key?: string; body?: CommitRequest; bodyBytes?: number[] };

// Fake unit transport with local native replay: App queue/preview proof only, never Runtime acceptance.
async function setup(raw = document()) {
  let server = copy(raw);
  const clips = [...server.parent_revision.payload.clips as Record<string, JSON>[], copy(survivor)];
  server.parent_revision.payload.clips = clips;
  server.parent_revision.payload.config = { ...server.parent_revision.payload.config as object, clips: copy(clips) };
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
      runtime_epoch: 1, runtime_instance_id: 'parent-delete-unit' });
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
        if (command.op === 'clip.delete') result = executeClipDelete(bundle, command);
        else if (command.op === 'clip.move') result = executeClipMove(bundle, command);
        else if (command.op === 'track.set') result = finishTrackLabel({ bundle, command }, command.args as TrackLabelArgs);
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
    baseUrl: `http://parent-delete-unit-${crypto.randomUUID()}.test`, token: 'unit', transport });
  const initial = await provider.loadTimelineCommandBasis(scope.timelineId);
  const display = (basis: TimelineCommandBasis): TimelineData => {
    const parent = basis.canonicalDocument.parent_revision.payload;
    const config = { ...parent.config as object, clips: parent.clips } as TimelineConfig;
    return assembleTimelineData({ config, configVersion: 1, registry: { assets: {} }, assetMap: {},
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
  const apply = (patch: Parameters<typeof projectClipDeletePreview>[0]) => {
    const next = projectClipDeletePreview(patch, current) ?? compileTimelinePatch(patch, current).nextData;
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

function remove(env: Awaited<ReturnType<typeof setup>>, session: TimelineCommandSession) {
  const captured = captureClipDeleteEdit(session.clipDeletePort, env.current(), 'x', 'parent');
  const command = session.clipDeletePort.finish(captured.basis).command;
  submitClipDeleteEdit(captured);
  return command;
}

describe('parent-only deletion on the existing durable session', () => {
  it('keeps mixed commands, original JSON guards, bytes and retry identity across lost ACK and reload', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    submitClipMove(captureClipMove(session.port, env.current(), 'x'), 2.017);
    const label = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    submitTrackLabelEdit(label, { values: { label: 'Picture 🦊 é' }, clear: [] });
    const localSurvivors = copy(env.current().config.clips.filter((clip) => clip.id !== 'x'));
    const command = remove(env, session);
    const originalRow = (command.expect!['parent/clip:x::'] as { state: 'present'; value: JSON }).value;
    expect(originalRow).toMatchObject({ id: 'x', track: 'V1', at: 61 / 30, hold: 1,
      text: { content: 'keep' }, app: { opaque: null } });
    expect(env.current().config.clips).toEqual(localSurvivors);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const first = copy(env.commits()[0]);
    expect(stored.intents).toHaveLength(3);
    expect(stored.intents[0].basis).toEqual({ head: env.initial.head });
    for (let index = 1; index < stored.intents.length; index++) {
      expect(stored.intents[index].basis).toEqual({ after: stored.intents[index - 1].id });
    }
    const commands = stored.intents.map((intent) => (intent.payload as unknown as { commands: EditCommand[] }).commands);
    expect(commands.map(([cmd]) => cmd.op)).toEqual(['clip.move', 'track.set', 'clip.delete']);
    expect(commands[2]).toEqual([command]);
    const deleted = stored.intents[2].payload as unknown as { before: Parameters<typeof executeClipDelete>[0] };
    expect(originalRow).toEqual(new AuthoredState(deleted.before).entity('parent/clip:x'));
    expect(JSON.parse(stored.pending!.request.body)).toEqual(first.body);
    expect(Array.from(new TextEncoder().encode(stored.pending!.request.body))).toEqual(first.bodyBytes);
    expect(stored.pending!.request.key).toBe(first.key);
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    expect(reopened.getState().status).toBe('recovery');
    expect(env.commits()).toHaveLength(1);
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.commits()).toHaveLength(4);
    expect(env.commits()[1]).toEqual(first);
    for (let index = 2; index < 4; index++) {
      expect(env.commits()[index].body).toMatchObject({ base_revision_id: `r${index - 1}`,
        base_publication_id: `p${index - 1}`, commands: commands[index - 1] });
    }
    expect(new Set(env.commits().map((call) => call.key)).size).toBe(3);
    expect(env.server().parent_revision.payload.clips).toEqual([survivor]);
    expect((env.server().parent_revision.payload.config as Record<string, JSON>).clips).toEqual([survivor]);
    expect(env.server().parent_revision.payload.registry).toEqual(env.initial.canonicalDocument.parent_revision.payload.registry);
    expect(env.server().dependency_manifest).toEqual(env.initial.canonicalDocument.dependency_manifest);
    expect(env.current().config.clips).toEqual([survivor]);
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake')).toEqual(env.commits());
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    await reopened.dispose();
  });

  it('retains a refused delete and the original local draft when a target changes after the unacked prefix', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    submitClipMove(captureClipMove(session.port, env.current(), 'x'), 2.017);
    const command = remove(env, session);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const original = copy(stored.intents[1].payload);
    const localDraft = copy(env.current().config.clips);
    env.external((raw) => {
      const clips = raw.parent_revision.payload.clips as Record<string, JSON>[];
      clips[0].opaque = { remote: [null, false] };
      (raw.parent_revision.payload.config as Record<string, JSON>).clips = copy(clips);
    });
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(stored.ownerId);
    expect(reopened.getState().status).toBe('conflict');
    const [refused] = await env.outboxes.list(scope);
    expect(refused.intents).toHaveLength(1);
    expect(refused.intents[0].payload).toEqual(original);
    expect(refused.pending!.outcome!.kind).toBe('rejected');
    expect(env.commits()[2].body!.commands).toEqual([command]);
    expect(env.current().config.clips).toEqual(localDraft);
    expect((env.server().parent_revision.payload.clips as Record<string, JSON>[])[0].opaque).toEqual({ remote: [null, false] });
    const calls = copy(env.commits());
    await reopened.retry();
    expect(env.commits()).toEqual(calls);
    await expect(reopened.flush()).rejects.toThrow();
    await reopened.dispose();
  });

  it.each(['transition', 'relation', 'group', 'children'])('atomically refuses %s and preserves earlier local draft', async (kind) => {
    const raw = document();
    const clips = raw.parent_revision.payload.clips as Record<string, JSON>[];
    if (kind === 'transition') clips[0].transition = { id: 'fade' };
    if (kind === 'relation') clips[0].app = { astrid: { on: 'word:1' } };
    if (kind === 'children') clips[0].children = [];
    if (kind === 'group') (raw.parent_revision.payload.config as Record<string, JSON>).pinnedShotGroups = [{ id: 'g', clipIds: ['x'] }];
    const env = await setup(raw);
    const session = await env.mount();
    env.loseAck();
    submitTrackLabelEdit(captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1'),
      { values: { label: 'Earlier local draft' }, clear: [] });
    const before = copy(env.current());
    expect(() => captureClipDeleteEdit(session.clipDeletePort, env.current(), 'x', 'parent')).toThrow();
    expect(env.current()).toEqual(before);
    expect(env.previews).toHaveBeenCalledTimes(1);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect((stored.intents[0].payload as unknown as { commands: EditCommand[] }).commands[0].op).toBe('track.set');
    expect(env.commits()).toHaveLength(1);
    await session.dispose();
  });

  it('fences changed previews, stale captures, duplicate submit and wrong display heads', async () => {
    const env = await setup();
    const session = await env.mount();
    const current = env.current();
    expect(() => session.clipDeletePort.capture({ clipId: 'x', ownerRef: 'parent', current: { ...current,
      head: { ...current.head!, headPublicationId: 'wrong' } } })).toThrow('raw authoring basis');
    const capture = captureClipDeleteEdit(session.clipDeletePort, current, 'x', 'parent');
    const ready = session.clipDeletePort.finish(capture.basis);
    expect(() => session.clipDeletePort.submit({ ...ready, preview: { version: 1, source: 'parentclip.delete',
      operations: [{ op: 'clip.remove', target: survivor.id as string }] } })).toThrow('exact same-clip');
    expect(env.current()).toBe(current);
    expect(env.previews).not.toHaveBeenCalled();
    env.loseAck();
    submitClipDeleteEdit(capture);
    expect(() => session.clipDeletePort.finish(capture.basis)).toThrow('Timeline changed');
    expect(() => submitClipDeleteEdit(capture)).toThrow();
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(1);
    await session.dispose();
  });
});

describe('explicit raw parent ownership', () => {
  it.each([null, false, {}, { clipRef: 'occurrence:occ-0/clip:child-title' }, 'complete-projected'] as const)(
    'uses the whole raw parent row despite same-ID child and opaque canonical metadata %j', async (canonical) => {
      const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
        { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
      const seed = await environment(raw);
      const projected = projectedDisplay(seed).resolvedConfig.clips.find((clip) => clip.id === 'occ-0:child-title')!;
      const parent = (raw.parent_revision.payload.clips as Record<string, JSON>[])[0];
      parent.id = 'child-title';
      parent.app = { keep: null, canonical: canonical === 'complete-projected' ? copy(projected.app!.canonical) as JSON : canonical };
      (raw.parent_revision.payload.config as Record<string, JSON>).clips = [copy(parent)];
      raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
      const env = await environment(raw);
      const session = await env.mount();
      const current = projectedDisplay(env);
      const basis = captureClipDeleteEdit(session.clipDeletePort, current, 'child-title', 'parent').basis;
      const result = session.clipDeletePort.finish(JSON.parse(JSON.stringify(basis)));
      expect(result.command.select).toBe('parent/clip:child-title');
      expect(result.command.expect!['parent/clip:child-title::']).toEqual({ state: 'present', value: parent });
      const native = executeClipDelete(basis.bundle as Parameters<typeof executeClipDelete>[0], result.command);
      expect(new AuthoredState(native.bundle).entity('parent/clip:child-title', true)).toBeUndefined();
      expect(native.bundle.shots).toEqual((basis.bundle as Parameters<typeof executeClipDelete>[0]).shots);
      expect(native.bundle.placements).toEqual((basis.bundle as Parameters<typeof executeClipDelete>[0]).placements);
      expect(env.previews).not.toHaveBeenCalled();
      expect(env.commits()).toHaveLength(0);
      await session.dispose();
    });

  it('requires an explicit parent request when the sole displayed row is a same-ID projected child', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const parent = (raw.parent_revision.payload.clips as Record<string, JSON>[])[0];
    parent.id = 'occ-0:child-title';
    (raw.parent_revision.payload.config as Record<string, JSON>).clips = [copy(parent)];
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const env = await environment(raw);
    const session = await env.mount();
    const display = projectedDisplay(env);
    const child = display.resolvedConfig.clips.find((clip) => clip.id === parent.id && clip.app?.canonical)!;
    const current = { ...display, resolvedConfig: { ...display.resolvedConfig, clips: [child] } };
    const before = copy(current);
    const outboxes = await env.outboxes.list(scope);
    const capture = session.clipDeletePort.capture;
    // Simulate an untyped caller handing over only the projected display ID.
    expect(() => capture({ clipId: child.id, current } as Parameters<typeof capture>[0])).toThrow('raw parent');
    expect(() => capture({ clipId: child.id, current, ownerRef: 'occurrence:occ-0' } as unknown as Parameters<typeof capture>[0])).toThrow('raw parent');
    expect(current).toEqual(before);
    expect(await env.outboxes.list(scope)).toEqual(outboxes);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    const explicit = capture({ clipId: parent.id as string, current, ownerRef: 'parent' });
    expect(session.clipDeletePort.finish(explicit).command.select).toBe(`parent/clip:${parent.id}`);
    await session.dispose();
  });
});
