import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { createCommitOutbox, toOutboxJson } from '../commands/commitOutbox.ts';
import { createLocalSaveSession } from '../commands/localSaveSession.ts';
import { createDefaultTimelineConfig } from '../lib/defaults.ts';
import { createTimelineLocalSaveHandoff, type TimelineSaveSource } from './timelineLocalSaveHandoff.ts';

async function environment(children = false) {
  const head = { projectId: 'project-commit', timelineId: 'timeline-commit', headRevisionId: 'r0', headPublicationId: 'p0' };
  const source: TimelineSaveSource = { config: createDefaultTimelineConfig(), registry: { assets: {} }, head };
  const document = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' }, { children }).data.canonical_document;
  const { output: _derived, ...config } = source.config;
  document.parent_revision.payload = { ...document.parent_revision.payload, config, clips: [], registry: source.registry };
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
