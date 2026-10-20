import { finishClipParams, type ClipParamsArgs } from '../clipParamsCapture.ts';
import { vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { CanonicalDocument, CommitAcceptedMutation, CommitRequest, Transport } from '@/integrations/runtime/generated.ts';
import { buildTimelineData } from '../../lib/timeline-data.ts';
import type { TimelineCommandBasis } from '../../data/DataProvider.ts';
import { createCommitOutbox } from '../commitOutbox.ts';
import { createTimelineCommandSession } from '../commitSession.ts';
import { captureClipMove, submitClipMove } from '../semanticGestures.ts';
import { authoringBundleFromDocument } from '../authoringBundle.ts';
import { ClipMoveError, executeClipMove } from '../clipMoveCapture.ts';
import { finishTrackLabel, type TrackLabelArgs } from '../trackLabelCapture.ts';
import { executeClipTrim } from '../clipTrimCapture.ts';
import { executeClipDelete } from '../clipDeleteCapture.ts';
import { executeClipSetBatch } from '../clipScalarCapture.ts';
import type { AssetRegistry } from '../../types/index.ts';
import trimFixture from '../fixtures/recipe_m2_clip_trim.json';

const projectId = 'project-commit', timelineId = 'timeline-commit';
export const scope = { projectId, timelineId, realmId: 'realm-1', actorId: 'actor-1' };
const h0 = { revisionId: 'r0', publicationId: 'p0' };
const bytes = (value: unknown) => new TextEncoder().encode(JSON.stringify(value));
const deferred = () => {
  let resolve!: () => void;
  const promise = new Promise<void>((done) => { resolve = done; });
  return { promise, resolve };
};
export function document(at = 1, revision = 'r0'): CanonicalDocument {
  const raw = acceptedCommit({ revision_id: revision, publication_id: 'p0' }, { revision_id: 'initial', publication_id: 'initial' }).data.canonical_document;
  const clips = [{ id: 'x', track: 'V1', at, hold: 1, text: { content: 'keep' }, app: { opaque: null } }];
  raw.parent_revision.payload = { config: { output: { fps: 30, resolution: '1920x1080' },
    tracks: [{ id: 'V1', kind: 'visual' }], clips: structuredClone(clips), bundle: null },
  tracks: [{ id: 'V1', kind: 'visual' }], registry: { assets: {} }, clips, occurrences: [], opaque: { absent: null } };
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  return raw;
}
export function trimDocument(): CanonicalDocument {
  const raw = document();
  const clips = [{ id: 'x', track: 'V1', asset: 'picture', clipType: 'media', at: 1, hold: 17,
    from: 2, to: 6, speed: 2, app: { astrid: { for: 19, until: null, opaque: [null, false] },
      'org.example': { literal: 'x', clear: null } }, unknown: { keep: [null, false, 0] } },
  { id: 'other', track: 'V1', at: 25, hold: 1, app: { opaque: [null, false] } }];
  raw.parent_revision.payload.clips = structuredClone(clips);
  raw.parent_revision.payload.config = { ...raw.parent_revision.payload.config as object, clips };
  raw.parent_revision.payload.registry = structuredClone(trimFixture.input.parent_revision.payload.registry);
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  return raw;
}
function storage() {
  const held = new Set<string>();
  const factory = createFakeIndexedDB();
  const outbox = createCommitOutbox({ indexedDB: factory, exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  return { outbox, factory };
}
export async function environment(initialDocument = document()) {
  let serverDocument = structuredClone(initialDocument);
  let serverHead = h0;
  let fault: 'lost' | 'busy' | 'conflict' | 'unavailable' | 'refused' | 'validation' | 'authorization' | null = null;
  let pause: ReturnType<typeof deferred> | null = null;
  const calls: { path: string; method: string; body?: CommitRequest; bodyBytes?: number[]; key?: string }[] = [];
  const accepted = new Map<string, CommitAcceptedMutation>();
  const previousDocuments = new Map<string, CanonicalDocument>();
  const transport: Transport = async (method, path, headers, body) => {
    const request = body ? JSON.parse(new TextDecoder().decode(body)) as CommitRequest : undefined;
    const key = headers['Idempotency-Key'];
    calls.push({ path, method, body: request, bodyBytes: ArrayBuffer.isView(body) ? Array.from(body) : undefined, key });
    const ok = (value: unknown) => ({ status: 200, headers: {}, body: bytes(value) });
    if (path === '/v1/health') return ok({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_instance_id: 'instance-session' });
    if (path === '/v1/handshake') return ok({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, actor_id: 'actor-1', realm_id: 'realm-1', scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'], capabilities: ['execution_binding.targeted.v1'] });
    if (path === '/v1/realm') return ok({ realm_id: 'realm-1' });
    if (path.endsWith('/commits?limit=50')) return ok({ items: [], next_cursor: null, head: { revision_id: serverHead.revisionId, publication_id: serverHead.publicationId } });
    if (path.includes('/composition-revisions/')) return ok({ project_id: projectId, timeline_id: timelineId,
      ...serverDocument.parent_revision, dependency_manifest: serverDocument.dependency_manifest });
    if (path.includes('/shots/') && path.includes('/revisions/')) {
      const shot = serverDocument.shot_revisions.find((image) => path.endsWith(`/shots/${image.shot_id}/revisions/${image.revision_id}`));
      if (!shot) throw new Error(`Unpinned shot read ${path}`);
      return ok({ project_id: projectId, ...shot });
    }
    if (path.includes('/timelines/') && path.includes('/revisions/')) {
      const internal = serverDocument.internal_timeline_revisions.find((image) => path.endsWith(`/timelines/${image.timeline_id}/revisions/${image.revision_id}`));
      if (!internal) throw new Error(`Unpinned internal read ${path}`);
      return ok({ project_id: projectId, ...internal });
    }
    if (!path.endsWith('/commit') || !request || !key) throw new Error(`Unexpected HTTP ${method} ${path}`);
    if (pause) await pause.promise;
    if (fault === 'busy' || fault === 'conflict' || fault === 'unavailable') return {
      status: fault === 'unavailable' ? 503 : 409, headers: {}, body: bytes({
        code: fault === 'unavailable' ? 'not_ready' : 'conflict', message: fault,
        details: { status: fault === 'conflict' ? 'conflict' : 'refused', reason: fault === 'busy' ? 'head_busy' : fault },
      }),
    };
    if (fault === 'refused' || fault === 'validation' || fault === 'authorization') return {
      status: fault === 'refused' ? 409 : fault === 'validation' ? 422 : 403, headers: {},
      body: bytes({ code: fault, message: 'conflict in request',
        details: fault === 'refused' ? { status: 'refused' } : {} }),
    };
    let response = accepted.get(key);
    if (!response) {
      const next = `r${accepted.size + 1}`, publication = `p${accepted.size + 1}`;
      response = acceptedCommit({ revision_id: next, publication_id: publication },
        { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, { commands: request.commands });
      response.data.previous_revision_id = serverHead.revisionId;
      response.data.previous_publication_id = serverHead.publicationId;
      const before = structuredClone(serverDocument);
      if (['clip.move', 'track.set', 'clip.trim', 'clip.set-params', 'clip.set', 'clip.delete'].includes(request.commands[0].op)) {
        let result;
        try {
          const bundle = await authoringBundleFromDocument(serverDocument);
          result = request.commands[0].op === 'clip.delete' ? executeClipDelete(bundle, request.commands[0])
            : request.commands[0].op === 'clip.move' ? executeClipMove(bundle, request.commands[0])
            : request.commands[0].op === 'clip.trim' ? executeClipTrim(bundle, request.commands[0])
            : request.commands[0].op === 'clip.set' ? executeClipSetBatch(bundle, request.commands)
            : request.commands[0].op === 'track.set'
              ? finishTrackLabel({ bundle, command: request.commands[0] }, request.commands[0].args as TrackLabelArgs)
              : finishClipParams({ bundle, command: request.commands[0] }, request.commands[0].args as ClipParamsArgs);
        }
        catch (error) {
          if (!(error instanceof ClipMoveError) || !['capture_mismatch', 'identity_conflict'].includes(error.kind)) throw error;
          // Guard failures cross the HTTP boundary as typed conflicts, not uncertain transport errors.
          return { status: 409, headers: {}, body: bytes({ code: 'conflict', message: error.message,
            details: { status: 'conflict', reason: error.kind } }) };
        }
        const payload = { ...result.bundle.parent, occurrences: [] };
        const revision = fixtureDigest(payload) === serverDocument.parent_revision.content_digest ? serverDocument.parent_revision.revision_id : next;
        serverDocument = { ...serverDocument, parent_revision: { revision_id: revision, content_digest: fixtureDigest(payload), payload } };
      } else if (request.commands[0].op === 'timeline.inverse') {
        const publications = request.commands[0].args.publications as string[];
        const restored = structuredClone(previousDocuments.get(publications[0])!);
        restored.parent_revision.revision_id = next;
        serverDocument = restored;
      } else throw new Error(`Unsupported test command ${request.commands[0].op}`);
      previousDocuments.set(publication, before);
      response.data.accepted_revision_id = serverDocument.parent_revision.revision_id;
      response.data.canonical_document = serverDocument;
      response.data.document_digest = fixtureDigest(serverDocument);
      response.receipt.result = response.data;
      response.receipt.idempotency_key = key;
      accepted.set(key, response);
      serverHead = { revisionId: serverDocument.parent_revision.revision_id, publicationId: publication };
    }
    if (fault === 'lost') { fault = null; throw new Error('lost acknowledgement'); }
    return ok(response);
  };
  const provider = new RuntimeDataProvider({ projectId, baseUrl: `http://session-${crypto.randomUUID()}.test`, token: 'token', transport });
  const initial = await provider.loadTimelineCommandBasis(timelineId);
  let current = await buildTimelineData(serverDocument.parent_revision.payload.config as never,
    serverDocument.parent_revision.payload.registry as AssetRegistry, undefined, 1, undefined,
    { projectId, timelineId, headRevisionId: 'r0', headPublicationId: 'p0' });
  const projected: TimelineCommandBasis[] = [];
  const previews = vi.fn();
  const { outbox: outboxes, factory } = storage();
  const mount = (basis = initial) => createTimelineCommandSession({ initial: basis, scope, outboxes,
    loadLatest: () => provider.loadTimelineCommandBasis(timelineId),
    send: (request, key) => provider.commitTimeline(request, key), preview: previews,
    project: async (basis) => {
      projected.push(basis);
      const parent = basis.canonicalDocument.parent_revision.payload;
      current = await buildTimelineData({ ...parent.config as object, clips: parent.clips } as never, parent.registry as AssetRegistry, undefined,
        1, undefined, { projectId, timelineId, headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId });
    }, changed: () => {},
  });
  const move = (session: Awaited<ReturnType<typeof mount>>, on: number) => submitClipMove(captureClipMove(session.port, current, 'x'), on);
  return { provider, initial, outboxes, factory, current: () => current, calls, projected, mount, move, previews,
    setFault: (value: typeof fault) => { fault = value; },
    pause: () => { pause = deferred(); return pause; },
    external: async (change: (document: CanonicalDocument) => void) => {
      change(serverDocument);
      serverDocument.parent_revision.revision_id = `external-${serverHead.revisionId}`;
      serverDocument.parent_revision.content_digest = fixtureDigest(serverDocument.parent_revision.payload);
      serverHead = { revisionId: serverDocument.parent_revision.revision_id, publicationId: `external-${serverHead.publicationId}` };
      return provider.loadTimelineCommandBasis(timelineId);
    },
    commits: () => calls.filter((call) => call.path.endsWith('/commit')) };
}
