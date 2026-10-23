import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { createCommitOutbox, toOutboxJson } from '../commands/commitOutbox.ts';
import { createLocalSaveSession } from '../commands/localSaveSession.ts';
import { createDefaultTimelineConfig, withDefaultTimelineOutput } from '../lib/defaults.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import type { TimelineConfig } from '../types/index.ts';
import { createTimelineLocalSaveHandoff, type TimelineSaveSource } from './timelineLocalSaveHandoff.ts';

async function environment(children = false, raw = false, rawIds = ['authored'], rawApp?: Record<string, unknown>) {
  const head = { projectId: 'project-commit', timelineId: 'timeline-commit', headRevisionId: 'r0', headPublicationId: 'p0' };
  let source: TimelineSaveSource = { config: createDefaultTimelineConfig(), registry: { assets: {} }, head };
  const document = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' }, { children }).data.canonical_document;
  const { output: _derived, ...config } = source.config;
  document.parent_revision.payload = { ...document.parent_revision.payload, config, clips: [], registry: source.registry };
  if (raw) {
    const authored = { ...config, output: { resolution: null, file: null, opaque: { keep: null } }, pinnedShotGroups: null,
      ...Object.fromEntries([['__proto__', { keep: null }], ['constructor', null]]),
      opaque: { keep: [null, false] }, clips: rawIds.map((id, index) => ({ id, track: 'V1', at: index * 2, hold: 2, clipType: null,
        opaque: { keep: null }, ...(rawApp ? { app: rawApp } : {}) })) };
    document.parent_revision.payload.config = authored;
    document.parent_revision.payload.clips = structuredClone(authored.clips);
    const data = await buildTimelineData({ ...authored,
      ...withDefaultTimelineOutput(authored as unknown as TimelineConfig) } as unknown as TimelineConfig, source.registry);
    source = { config: data.config, registry: data.registry, head };
  }
  document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
  const initial = { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: document };
  const scope = { realmId: 'realm', actorId: 'actor', projectId: head.projectId, timelineId: head.timelineId };
  const outboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (_key, work) => work() });
  const send = vi.fn();
  const session = await createLocalSaveSession({ scope, initial, document: toOutboxJson(document), outboxes, send,
    loadLatest: vi.fn(async () => initial), changed: vi.fn(),
    prepareDisplay: vi.fn(async () => { throw new Error('No canonical acceptance expected'); }) });
  const receipt = vi.fn();
  const handoff = createTimelineLocalSaveHandoff({ initial, source, session, adopted: receipt });
  return { source, initial, scope, outboxes, send, session, receipt, handoff };
}

describe('upstream local document handoff', () => {
  it('chains exact trim intent removals without clearing omitted opaque fields or restoring them on a partial edit', async () => {
    const env = await environment(false, true, ['authored'], {
      astrid: { for: 19, until: null, opaque: [null, false] }, 'org.example': { clear: null },
    });
    const moved = structuredClone(env.source);
    moved.config.clips[0].at = 1;
    await env.handoff.capture(moved);
    const trimmed = structuredClone(moved);
    trimmed.config.clips[0].hold = 1;
    trimmed.config.clips[0].app = { astrid: {} };
    await env.handoff.capture(trimmed);
    const expected = structuredClone(env.initial.canonicalDocument);
    for (const clips of [expected.parent_revision.payload.clips,
      (expected.parent_revision.payload.config as Record<string, unknown>).clips] as Record<string, unknown>[][]) {
      clips[0].at = 1;
      clips[0].hold = 1;
      clips[0].app = { astrid: { opaque: [null, false] }, 'org.example': { clear: null } };
    }
    expect(env.session.getDocument()).toEqual(expected);
    await env.handoff.capture(structuredClone(trimmed));
    const partial = structuredClone(trimmed);
    delete partial.config.clips[0].app;
    partial.config.clips[0].at = 2;
    await env.handoff.capture(partial);
    const [owner] = await env.outboxes.list(env.scope);
    expect(owner.intents).toHaveLength(3);
    expect(owner.intents[1].basis).toEqual({ after: owner.intents[0].id });
    expect(owner.intents[1].payload).toMatchObject({ documentIntent: { changes: [
      { op: 'set', ref: 'parent', path: ['clips', 'id:authored', 'hold'], before: { state: 'present', value: 2 }, value: 1 },
      { op: 'remove', ref: 'parent', path: ['clips', 'id:authored', 'app', 'astrid', 'for'], before: { state: 'present', value: 19 } },
      { op: 'remove', ref: 'parent', path: ['clips', 'id:authored', 'app', 'astrid', 'until'], before: { state: 'present', value: null } },
    ] } });
    expect(owner.intents[2].basis).toEqual({ after: owner.intents[1].id });
    expect(owner.intents[2].payload).toMatchObject({ documentIntent: { changes: [
      { op: 'set', ref: 'parent', path: ['clips', 'id:authored', 'at'], before: { state: 'present', value: 1 }, value: 2 },
    ] } });
    expect(env.session.getDocument()).toMatchObject({ parent_revision: { payload: {
      clips: [{ app: { astrid: { opaque: [null, false] }, 'org.example': { clear: null } } }],
    } } });
    await env.session.dispose();
  });

  it.each(['app', 'namespace'] as const)('preserves trim intent when a partial view omits the %s container', async (kind) => {
    const app = { astrid: { for: 19, until: null, opaque: [null, false] }, 'org.example': { clear: null } };
    const env = await environment(false, true, ['authored'], app);
    const next = structuredClone(env.source);
    if (kind === 'app') delete next.config.clips[0].app;
    else next.config.clips[0].app = { 'org.example': { clear: null } };
    next.config.clips[0].hold = 1;
    await env.handoff.capture(next);
    const [owner] = await env.outboxes.list(env.scope);
    expect(owner.intents[0].payload).toMatchObject({ documentIntent: { changes: [
      { op: 'set', ref: 'parent', path: ['clips', 'id:authored', 'hold'], before: { state: 'present', value: 2 }, value: 1 },
    ] } });
    expect(env.session.getDocument()).toMatchObject({ parent_revision: { payload: { clips: [{ app }] } } });
    await env.session.dispose();
  });

  it('keeps raw nulls, absence and opaque own keys through a real upstream projection and dependent edits', async () => {
    const env = await environment(false, true);
    const raw = structuredClone(env.initial.canonicalDocument);
    expect(env.source.config.output.resolution).toBe('1280x720');
    expect(env.source.config.pinnedShotGroups).toBeUndefined();
    expect(env.source.config.clips[0].clipType).toBe('hold');
    await env.handoff.capture(structuredClone(env.source));
    expect(env.session.getDocument()).toEqual(raw);
    expect((await env.outboxes.list(env.scope))[0].intents).toHaveLength(0);
    const moved = structuredClone(env.source);
    moved.config.clips[0].at = 1;
    await env.handoff.capture(moved);
    const trimmed = structuredClone(moved);
    trimmed.config.clips = [{ id: 'authored', track: 'V1', at: 1, hold: 1 }];
    await env.handoff.capture(trimmed);
    const expected = structuredClone(raw);
    for (const clips of [expected.parent_revision.payload.clips,
      (expected.parent_revision.payload.config as Record<string, unknown>).clips] as Record<string, unknown>[][]) {
      clips[0].at = 1;
      clips[0].hold = 1;
    }
    expect(env.session.getDocument()).toEqual(expected);
    const [owner] = await env.outboxes.list(env.scope);
    expect(owner.intents).toHaveLength(2);
    expect(owner.intents[1].basis).toEqual({ after: owner.intents[0].id });
    expect(owner.intents[1].payload).toMatchObject({ documentIntent: { changes: [
      { op: 'set', ref: 'parent', path: ['clips', 'id:authored', 'hold'], before: { state: 'present', value: 2 }, value: 1 },
    ] } });
    expect(owner.intents[1].payload).not.toHaveProperty('documentIntent.reads');
    const rebuilt = structuredClone(env.source);
    rebuilt.config.clips[0].at = 1;
    rebuilt.config.clips[0].hold = 1;
    await env.handoff.capture(rebuilt);
    expect(env.session.getDocument()).toEqual(expected);
    expect((await env.outboxes.list(env.scope))[0].intents).toHaveLength(2);
    await env.session.dispose();
  });

  it('refuses an ambiguous display container clear without changing the raw document or its dependent chain', async () => {
    const env = await environment(false, true);
    const next = structuredClone(env.source);
    next.config.output.resolution = undefined as unknown as string;
    await expect(env.handoff.capture(next)).rejects.toThrow('explicit clear is unavailable');
    expect(env.session.getDocument()).toEqual(env.initial.canonicalDocument);
    expect((await env.outboxes.list(env.scope))[0].intents).toHaveLength(0);
    const valid = structuredClone(env.source);
    valid.config.clips[0].hold = 3;
    await env.handoff.capture(valid);
    expect((await env.outboxes.list(env.scope))[0].intents).toHaveLength(1);
    await env.session.dispose();
  });

  it('refuses repaired display identities rather than using them to identify authored clips', async () => {
    const env = await environment(false, true, ['authored-dup-1', 'authored-dup-2']);
    expect(env.source.config.clips[0].id).toBe('authored');
    await expect(env.handoff.capture(env.source)).rejects.toThrow('authored clips identity changed in projection');
    expect(env.session.getDocument()).toEqual(env.initial.canonicalDocument);
    expect((await env.outboxes.list(env.scope))[0].intents).toHaveLength(0);
    await env.session.dispose();
  });

  it('maps authored source items and registry while preserving opaque parent data and omitting derived output', async () => {
    const env = await environment();
    const next: TimelineSaveSource = structuredClone(env.source);
    next.bundle = { schema_version: 1, itemsBySchemaRef: {} };
    next.registry = { assets: { media: { file: 'media.mp4', type: 'video/mp4' } } };
    await env.handoff.capture(next);
    const candidate = env.session.getDocument();
    expect(candidate).toMatchObject({ parent_revision: { payload: {
      unknown: { nested: ['value', null] }, config: { bundle: next.bundle }, registry: next.registry,
    } } });
    expect(candidate).not.toHaveProperty('parent_revision.payload.config.output');
    next.bundle.itemsBySchemaRef.changed = [];
    expect(env.session.getDocument()).toEqual(candidate);
    await expect(env.handoff.flush()).rejects.toThrow('draft retained');
    expect(env.receipt).not.toHaveBeenCalled();
    expect(env.send).not.toHaveBeenCalled();
    await env.session.dispose();
  });

  it.each(['missing publication', 'refreshed head', 'foreign timeline'] as const)('refuses %s instead of refreshing the authoring basis', async (kind) => {
    const env = await environment();
    const next = structuredClone(env.source);
    if (kind === 'missing publication') delete next.head!.headPublicationId;
    if (kind === 'refreshed head') next.head!.headRevisionId = 'newer-polled-r';
    if (kind === 'foreign timeline') next.head!.timelineId = 'other';
    await expect(env.handoff.capture(next)).rejects.toThrow('original verified authoring head');
    expect((await env.outboxes.list(env.scope))[0].intents).toHaveLength(0);
    expect(env.session.getDocument()).toEqual(env.initial.canonicalDocument);
    await env.session.dispose();
  });

  it('refuses flattened child/occurrence saves without reconstructing or changing the verified closure', async () => {
    const env = await environment(true);
    const next = structuredClone(env.source);
    next.config.clips = [{ id: 'display-child-title', track: 'V1', at: 0, hold: 2 }];
    await expect(env.handoff.capture(next)).rejects.toThrow('child ownership/fork mapping');
    expect(env.session.getDocument()).toEqual(env.initial.canonicalDocument);
    expect((await env.outboxes.list(env.scope))[0].intents).toHaveLength(0);
    await env.session.dispose();
  });

  it('retains source mismatches and invalid values without silently defaulting or laundering them', async () => {
    const env = await environment();
    const mismatch = createTimelineLocalSaveHandoff({ initial: env.initial, source: {
      ...env.source, config: { ...env.source.config, clips: [{ id: 'not-authored', track: 'V1', at: 0, hold: 1 }] },
    }, session: env.session, adopted: env.receipt });
    await expect(mismatch.capture(env.source)).rejects.toThrow('differs from the verified authored parent');
    const bad = structuredClone(env.source);
    bad.config.clips = [{ id: 'bad', track: 'V1', at: 0, hold: NaN }];
    await expect(env.handoff.capture(bad)).rejects.toThrow('finite JSON');
    expect(env.session.getDocument()).toEqual(env.initial.canonicalDocument);
    await env.session.dispose();
  });

  it('encodes explicit transition clearing as guarded removal and retains no-op captures without another intent', async () => {
    const env = await environment();
    const next = structuredClone(env.source);
    next.config.clips = [{ id: 'new', track: 'V1', at: 0, hold: 1, transition: { type: 'fade', duration: 0.1 },
      ...{ opaque: { keep: [null, false] } } }];
    await env.handoff.capture(next);
    await env.handoff.capture(structuredClone(next));
    const cleared = structuredClone(next);
    cleared.config.clips = [{ id: 'new', track: 'V1', at: 0, hold: 1, transition: undefined }];
    await env.handoff.capture(cleared);
    const [stored] = await env.outboxes.list(env.scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[1].payload).toMatchObject({ documentIntent: {
      changes: [{ op: 'remove', ref: 'parent', path: ['clips', 'id:new', 'transition'],
        before: { state: 'present', value: next.config.clips[0].transition } }],
    } });
    expect(env.session.getDocument()).toMatchObject({ parent_revision: { payload: {
      clips: [{ id: 'new', opaque: { keep: [null, false] } }],
    } } });
    await env.session.dispose();
  });
});
