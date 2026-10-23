import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';

import { createFakeRuntimeRouter, type FakeRuntimeRouter } from '@/test/fakeRuntimeRouter.ts';
import { ApiError } from '@/integrations/runtime/generated.ts';
import { createCommitOutbox } from '@/tools/video-editor/commands/commitOutbox.ts';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults';

import {
  batchUpdatePlacementFrames,
  fetchGalleryRows,
  fetchProjectPlacements,
  placeGeneration,
  unplaceGeneration,
} from '../placementService';

/**
 * Placement round-trips over workspace.v1: the timeline list is a `/v1/projects/…`
 * route; placement writes use the Runtime canonical basis and the same
 * LocalSaveSession/doc.patch outbox as the editor. Gallery and generation reads
 * come from the canonical fake router; the Runtime head is the in-memory fake below.
 */

const PROJECT = 'demo-project';
const TIMELINE = 'timeline-v1';
const SHOT = 'shot-e2e-1';
const FAKE_ORIGIN = 'http://bridge.fake';

const runtime = vi.hoisted(() => ({
  head: 'rev-1',
  version: 1,
  config: null as unknown,
  registry: { assets: {} } as unknown,
  publishes: [] as string[],
  commits: [] as Array<{ body: unknown; key: string }>,
  /** Runs once, before the next publish is checked: simulates a sibling publish. */
  beforePublish: null as null | (() => void),
}));

function canonicalDocument() {
  return {
    schema_version: 1 as const,
    project_id: PROJECT,
    timeline_id: TIMELINE,
    parent_revision: { revision_id: runtime.head, content_digest: 'parent-digest', payload: {
      config: structuredClone(runtime.config), registry: structuredClone(runtime.registry), occurrences: [{
        occurrence_id: 'occurrence-1', shot_id: 'shot-child', shot_revision_id: 'shot-r1', revision_id: 'occurrence-r1',
      }],
      opaque: { nested: [null, false] },
    } },
    shot_revisions: [{ shot_id: 'shot-child', revision_id: 'shot-r1', internal_timeline_revision_id: 'internal-r1',
      content_digest: 'shot-digest', payload: { items: [] } }],
    internal_timeline_revisions: [{ timeline_id: 'child-timeline', revision_id: 'internal-r1',
      content_digest: 'internal-digest', payload: { items: [] } }],
    dependency_manifest: {
      shots: [{ shot_id: 'shot-child', revision_id: 'shot-r1', internal_timeline_revision_id: 'internal-r1', content_digest: 'shot-digest' }],
      internal_timelines: [{ timeline_id: 'child-timeline', revision_id: 'internal-r1', content_digest: 'internal-digest' }],
      media: [], documents: [],
    },
  };
}

function container(root: any, path: string[]): { owner: any; key: string } {
  let owner = root;
  for (const token of path.slice(0, -1)) owner = token.startsWith('id:')
    ? owner.find((row: any) => row.id === token.slice(3)) : owner[token];
  return { owner, key: path[path.length - 1]! };
}

function applyChanges(document: any, changes: any[]) {
  const payload = document.parent_revision.payload;
  for (const change of changes) {
    const { owner, key } = container(payload, change.path);
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
    } else if (change.op === 'list.move') {
      const list = owner[key] as any[];
      const index = list.findIndex((row) => row.id === change.id);
      const [row] = list.splice(index, 1);
      const after = change.after_id === null ? -1 : list.findIndex((item) => item.id === change.after_id);
      list.splice(after + 1, 0, row);
    }
  }
}

vi.mock('@/integrations/runtime/dataProvider', () => ({
  RuntimeDataProvider: class {
    constructor(readonly options: { projectId: string }) {}
    async loadTimeline(timelineId: string) {
      return {
        config: structuredClone(runtime.config),
        configVersion: runtime.version,
        head: { projectId: this.options.projectId, timelineId, headRevisionId: runtime.head },
      };
    }
    async loadAssetRegistry() {
      return structuredClone(runtime.registry);
    }
    async loadTimelineCommandBasis() {
      const document = canonicalDocument();
      return { head: { revisionId: runtime.head, publicationId: `pub-${runtime.head}` }, canonicalDocument: document, graph: {} };
    }
    async getRecoverableIdentity() {
      return { realmId: 'realm', actorId: 'actor' };
    }
    async commitTimeline(request: any, key: string) {
      const hook = runtime.beforePublish;
      runtime.beforePublish = null;
      hook?.();
      runtime.commits.push({ body: structuredClone(request), key });
      if (request.base_revision_id !== runtime.head) {
        throw new ApiError(409, 'conflict', 'intervening_write', '', { status: 'conflict' });
      }
      const document = canonicalDocument();
      const nextHead = `rev-${runtime.publishes.length + 2}`;
      applyChanges(document, request.commands[0].args.changes);
      document.parent_revision.revision_id = nextHead;
      runtime.config = structuredClone(document.parent_revision.payload.config);
      runtime.registry = structuredClone(document.parent_revision.payload.registry);
      runtime.version += 1;
      runtime.head = nextHead;
      runtime.publishes.push(runtime.head);
      const accepted = { revisionId: runtime.head, publicationId: `pub-${runtime.head}` };
      return { response: { data: { status: 'accepted', canonical_document: document }, receipt: { receipt_id: accepted.publicationId } },
        accepted, canonicalDocument: document, graph: {}, receipt: { receipt_id: accepted.publicationId } };
    }
  },
}));

function installRuntime(router: FakeRuntimeRouter): string[] {
  const calls: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const raw = input instanceof Request ? input.url : String(input);
    const url = new URL(raw.startsWith(FAKE_ORIGIN) ? raw : `${FAKE_ORIGIN}${raw}`);
    const path = url.pathname.replace(/^\/api\/astrid/, '');
    const method = init?.method ?? 'GET';
    calls.push(`${method} ${path}`);
    const json = (body: unknown) => new Response(JSON.stringify(body), {
      status: 200,
      headers: { 'content-type': 'application/json' },
    });
    if (path === `/v1/projects/${PROJECT}/timelines`) {
      return json({ items: [{ timeline_id: TIMELINE, name: 'main', is_default: true }] });
    }
    return await router.handle(new Request(url, init));
  }));
  return calls;
}

function firstSeededGenerationId(router: FakeRuntimeRouter): string {
  const detail = router.state.galleryDetails[0] as { generation_id: string };
  return detail.generation_id;
}

describe('placementService: CAS round-trips over workspace.v1', () => {
  beforeEach(() => {
    runtime.head = 'rev-1';
    runtime.version = 1;
    runtime.config = createDefaultTimelineConfig();
    runtime.registry = { assets: {} };
    runtime.publishes = [];
    runtime.commits = [];
    runtime.beforePublish = null;
    vi.stubGlobal('indexedDB', createFakeIndexedDB());
    vi.stubGlobal('navigator', { locks: { request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}) } });
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('keeps every raw root at the provider boundary across placement, frame update, pooling and removal', async () => {
    const router = createFakeRuntimeRouter();
    installRuntime(router);
    const generationId = firstSeededGenerationId(router);
    const roots = JSON.parse('{"opaque":{"nested":[null,false,[]]},"nullable":null,"ordered":[3,1,2],"__proto__":{"literal":true},"constructor":{"prototype":0},"prototype":false}');
    runtime.config = { ...createDefaultTimelineConfig(), ...roots };
    const assertRoots = () => {
      for (const [key, value] of Object.entries(roots)) {
        expect(Object.hasOwn(runtime.config as object, key), key).toBe(true);
        expect(Reflect.get(runtime.config as object, key), key).toEqual(value);
      }
      expect(Object.hasOwn(runtime.config as object, 'absent')).toBe(false);
    };
    const placed = await placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId });
    assertRoots();
    await batchUpdatePlacementFrames({ projectSlug: PROJECT, shotId: SHOT, updates: [{ entryId: placed.entryId, timelineFrame: 30 }] });
    assertRoots();
    await unplaceGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId, entryId: placed.entryId, keepAsPooled: true });
    assertRoots();
    await unplaceGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId, entryId: placed.entryId });
    assertRoots();
    expect(runtime.publishes).toHaveLength(4);
  });

  it('places a completed generation into the document and the placement survives a fresh read', async () => {
    const router = createFakeRuntimeRouter();
    const calls = installRuntime(router);
    const generationId = firstSeededGenerationId(router);

    const placed = await placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId });
    expect(placed.timelineFrame).toBe(0);
    expect(runtime.publishes).toEqual(['rev-2']);
    expect(calls.some((call) => call.endsWith('/save'))).toBe(false);

    // Fresh read: what a page load sees after refresh.
    const read = await fetchProjectPlacements(PROJECT);
    const rows = read.byShot.get(SHOT) ?? [];
    expect(rows.map((r) => r.generationId)).toEqual([generationId]);
    expect(rows[0]?.timelineFrame).toBe(0);
    expect(read.config.pinnedShotGroups?.[0]?.shotId).toBe(SHOT);

    // The placed clip is a REAL editor clip on the group track with a registry asset.
    const group = read.config.pinnedShotGroups?.[0];
    const clip = read.config.clips.find((c) => c.id === `clip-${placed.entryId}`);
    expect(clip?.track).toBe(group?.trackId);
    expect(clip?.clipType).toBe('media');
    const asset = read.registry.assets[clip?.asset ?? ''] as { generationId?: string } | undefined;
    expect(asset).toBeDefined();
  });

  it('pooled add keeps membership without a clip; batch update promotes it', async () => {
    const router = createFakeRuntimeRouter();
    installRuntime(router);
    const generationId = firstSeededGenerationId(router);

    const pooled = await placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId, timelineFrame: null });
    let read = await fetchProjectPlacements(PROJECT);
    expect(read.config.clips.find((c) => c.id === `clip-${pooled.entryId}`)).toBeUndefined();
    expect(pooled.timelineFrame).toBeNull();

    const [promoted] = await batchUpdatePlacementFrames({
      projectSlug: PROJECT,
      shotId: SHOT,
      updates: [{ entryId: pooled.entryId, timelineFrame: 3 }],
    });
    expect(promoted.timelineFrame).toBe(3);
    read = await fetchProjectPlacements(PROJECT);
    expect(read.config.clips.some((c) => c.source_uuid === pooled.entryId)).toBe(true);
  });

  it('unplacing with keepAsPooled drops the clip but keeps membership', async () => {
    const router = createFakeRuntimeRouter();
    installRuntime(router);
    const generationId = firstSeededGenerationId(router);

    const placed = await placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId });
    await unplaceGeneration({
      projectSlug: PROJECT,
      shotId: SHOT,
      entryId: placed.entryId,
      generationId,
      keepAsPooled: true,
    });

    const read = await fetchProjectPlacements(PROJECT);
    expect(read.config.clips.some((c) => c.source_uuid === placed.entryId)).toBe(false);
    expect(read.byShot.get(SHOT)?.[0]?.timelineFrame).toBeNull();
  });

  it('retains the original durable intent when a concurrent publish is refused', async () => {
    const router = createFakeRuntimeRouter();
    installRuntime(router);
    const generationId = firstSeededGenerationId(router);

    // A sibling publish lands after our load and before our publish.
    runtime.beforePublish = () => {
      const sibling = structuredClone(runtime.config) as { clips: unknown[] };
      sibling.clips = [{ id: 'sibling', track: 'V1', at: 0, hold: 1 }];
      runtime.config = sibling;
      runtime.head = 'rev-sibling';
    };

    await expect(placeGeneration({ projectSlug: PROJECT, shotId: SHOT, generationId }))
      .rejects.toMatchObject({ code: 'timeline_version_conflict' });
    expect(runtime.publishes).toHaveLength(0);
    const outboxes = createCommitOutbox({ indexedDB: globalThis.indexedDB });
    const [saved] = await outboxes.list({ realmId: 'realm', actorId: 'actor', projectId: PROJECT, timelineId: TIMELINE });
    expect(saved?.pending?.outcome?.kind).toBe('rejected');
    expect(saved?.intents[0]?.payload).toMatchObject({ documentIntent: { roots: [{ ref: 'parent' }] } });
  });

  it('gallery rows walk the R12 pages for the merge view', async () => {
    const router = createFakeRuntimeRouter();
    installRuntime(router);
    const rows = await fetchGalleryRows(PROJECT);
    expect(rows.length).toBeGreaterThan(0);
    expect(rows[0]?.primaryMediaId).toBeTruthy();
  });
});
