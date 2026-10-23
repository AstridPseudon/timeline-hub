import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';

import { ApiError } from '@/integrations/runtime/generated.ts';
import { createCommitOutbox } from '@/tools/video-editor/commands/commitOutbox.ts';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults';

/**
 * Placement publishes through the same canonical commit/outbox path the editor
 * saves with; the old `…/timelines/:ref/save` route is not available.
 */

const PROJECT = 'project-v1';
const TIMELINE = 'timeline-v1';
const SHOT = 'shot-1';

const runtime = vi.hoisted(() => ({
  head: 'rev-1',
  config: null as unknown,
  registry: { assets: {} } as unknown,
  publishes: [] as string[],
  requests: [] as Array<{ body: string; key: string }>,
  replies: new Map<string, unknown>(),
  loseAck: false,
  /** Runs once, before the next publish is checked — simulates a sibling publish. */
  beforePublish: null as null | (() => void),
}));

function canonicalDocument() {
  return { schema_version: 1 as const, project_id: PROJECT, timeline_id: TIMELINE,
    parent_revision: { revision_id: runtime.head, content_digest: 'parent-digest', payload: {
      config: structuredClone(runtime.config), registry: structuredClone(runtime.registry), occurrences: [],
    } }, shot_revisions: [], internal_timeline_revisions: [],
    dependency_manifest: { shots: [], internal_timelines: [], media: [], documents: [] } };
}

function applyChanges(document: any, changes: any[]) {
  const payload = document.parent_revision.payload;
  for (const change of changes) {
    let owner = payload;
    for (const token of change.path.slice(0, -1)) owner = token.startsWith('id:')
      ? owner.find((row: any) => row.id === token.slice(3)) : owner[token];
    const key = change.path[change.path.length - 1];
    if (change.op === 'set') owner[key] = structuredClone(change.value);
    else if (change.op === 'remove') delete owner[key];
    else if (change.op === 'list.insert') {
      const list = owner[key] as any[];
      const index = change.after_id === null ? 0 : list.findIndex((row) => row.id === change.after_id) + 1;
      list.splice(index, 0, structuredClone(change.value));
    } else if (change.op === 'list.remove') {
      const list = owner[key] as any[];
      const index = list.findIndex((row) => row.id === change.id);
      if (index >= 0) list.splice(index, 1);
    }
  }
}

vi.mock('@/integrations/runtime/dataProvider', () => ({
  RuntimeDataProvider: class {
    constructor(readonly options: { projectId: string }) {}
    async loadTimeline(timelineId: string) {
      return {
        config: structuredClone(runtime.config),
        configVersion: 1,
        head: { projectId: this.options.projectId, timelineId, headRevisionId: runtime.head },
      };
    }
    async loadAssetRegistry() {
      return structuredClone(runtime.registry);
    }
    async loadTimelineCommandBasis() {
      return { head: { revisionId: runtime.head, publicationId: `pub-${runtime.head}` }, canonicalDocument: canonicalDocument(), graph: {} };
    }
    async getRecoverableIdentity() {
      return { realmId: 'realm', actorId: 'actor' };
    }
    async commitTimeline(request: any, key: string) {
      const hook = runtime.beforePublish;
      runtime.beforePublish = null;
      hook?.();
      runtime.requests.push({ body: JSON.stringify(request), key });
      const replay = runtime.replies.get(key);
      if (replay) return replay;
      if (request.base_revision_id !== runtime.head) {
        throw new ApiError(409, 'conflict', 'intervening_write', '', { status: 'conflict' });
      }
      const document = canonicalDocument();
      applyChanges(document, request.commands[0].args.changes);
      runtime.head = `rev-${runtime.publishes.length + 2}`;
      document.parent_revision.revision_id = runtime.head;
      runtime.config = structuredClone(document.parent_revision.payload.config);
      runtime.registry = structuredClone(document.parent_revision.payload.registry);
      runtime.publishes.push(runtime.head);
      const accepted = { revisionId: runtime.head, publicationId: `pub-${runtime.head}` };
      const reply = { response: { data: { status: 'accepted', canonical_document: document }, receipt: { receipt_id: accepted.publicationId } },
        accepted, canonicalDocument: document, graph: {}, receipt: { receipt_id: accepted.publicationId } };
      runtime.replies.set(key, reply);
      if (runtime.loseAck) { runtime.loseAck = false; throw new Error('lost acknowledgement'); }
      return reply;
    }
  },
}));

vi.mock('@/tools/video-editor/data/generationAssetResolver', () => ({
  resolveGenerationAsset: async () => ({
    ok: true,
    asset: {
      url: 'http://runtime.test/v1/objects/sha256%3Aabc',
      mimeType: 'image/png',
      entry: { file: 'sha256:abc', type: 'image', media_id: 'sha256:abc' },
    },
  }),
}));

function installV1Fetch() {
  const calls: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = new URL(input instanceof Request ? input.url : String(input), 'http://runtime.test');
    url.pathname = url.pathname.replace(/^\/api\/astrid/, '');
    calls.push(`${init?.method ?? 'GET'} ${url.pathname}`);
    const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), {
      status,
      headers: { 'content-type': 'application/json' },
    });
    if (url.pathname === `/v1/projects/${PROJECT}/timelines`) {
      return json({ items: [{ timeline_id: TIMELINE, name: 'main', is_default: true }] });
    }
    if (url.pathname === `/v1/projects/${PROJECT}/timelines/${TIMELINE}` && (init?.method ?? 'GET') === 'GET') {
      return json({ timeline_id: TIMELINE, config: runtime.config, registry: runtime.registry, config_version: 1 });
    }
    return json({ code: 'not_found', message: `no route ${url.pathname}` }, 404);
  }));
  return calls;
}

async function loadService() {
  return await import('../placementService');
}

describe('placementService under Workspace v1', () => {
  beforeEach(() => {
    runtime.head = 'rev-1';
    runtime.config = createDefaultTimelineConfig();
    runtime.registry = { assets: {} };
    runtime.publishes = [];
    runtime.requests = [];
    runtime.replies = new Map();
    runtime.loseAck = false;
    runtime.beforePublish = null;
    vi.stubGlobal('indexedDB', createFakeIndexedDB());
    vi.stubGlobal('navigator', { locks: { request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}) } });
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('places a generation by publishing a new head revision', async () => {
    const calls = installV1Fetch();
    const { placeGeneration } = await loadService();

    const placed = await placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId: 'gen-1' });

    expect(placed.timelineFrame).toBe(0);
    expect(runtime.publishes).toEqual(['rev-2']);
    const config = runtime.config as { clips: Array<{ id: string }>; pinnedShotGroups?: Array<{ shotId: string }> };
    expect(config.clips.map((clip) => clip.id)).toEqual([`clip-${placed.entryId}`]);
    expect(config.pinnedShotGroups?.[0]?.shotId).toBe(SHOT);
    expect(calls.some((call) => call.endsWith('/save'))).toBe(false);
  });

  it('retains a refused placement intent after a stale-head conflict', async () => {
    installV1Fetch();
    const { placeGeneration } = await loadService();
    // A sibling publish lands between placement's read and its publish.
    runtime.beforePublish = () => {
      const sibling = structuredClone(runtime.config) as { clips: unknown[] };
      sibling.clips = [{ id: 'sibling', track: 'V1', at: 0, hold: 1 }];
      runtime.config = sibling;
      runtime.head = 'rev-sibling';
    };

    await expect(placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId: 'gen-1' }))
      .rejects.toMatchObject({ code: 'timeline_version_conflict' });
    expect(runtime.publishes).toHaveLength(0);
    const outboxes = createCommitOutbox({ indexedDB: globalThis.indexedDB });
    const [saved] = await outboxes.list({ realmId: 'realm', actorId: 'actor', projectId: PROJECT, timelineId: TIMELINE });
    expect(saved?.pending?.outcome?.kind).toBe('rejected');
  });

  it('surfaces the conflict when the head stays stale', async () => {
    installV1Fetch();
    const { placeGeneration } = await loadService();
    const bump = () => { runtime.head = `${runtime.head}x`; runtime.beforePublish = bump; };
    runtime.beforePublish = bump;

    await expect(placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId: 'gen-1' }))
      .rejects.toMatchObject({ code: 'timeline_version_conflict' });
    expect(runtime.publishes).toHaveLength(0);
  });

  it('retries an unknown acknowledgement with the exact durable request and key', async () => {
    installV1Fetch();
    const { placeGeneration } = await loadService();
    runtime.loseAck = true;
    await expect(placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId: 'gen-1' })).rejects.toThrow('unacknowledged');
    await placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId: 'gen-1' });
    expect(runtime.requests).toHaveLength(2);
    expect(runtime.requests[1]).toEqual(runtime.requests[0]);
  });
});
