// @vitest-environment jsdom
import React from 'react';
import { execFileSync } from 'node:child_process';
import { AgentChatProvider } from '@/shared/contexts/AgentChatContext.tsx';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import fixture from '@/tools/video-editor/data/shotComposition.fixture.json';
import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { Transport } from '@/integrations/runtime/generated.ts';
import type { CanonicalDocument, CommitAcceptedMutation, CommitRequest, MediaSelection } from '@/integrations/runtime/timeline-commit-types.ts';
import { createCommitOutbox } from '@/tools/video-editor/commands/commitOutbox.ts';
import { createShotCompositionAdapter } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { ShotTimelinePreview } from './ShotTimelinePreview.tsx';

// The media renderer needs a browser Player; editor preparation, commands and saves stay mounted.
vi.mock('@/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx', () => ({
  RemotionPreview: () => null,
}));

const projectId = 'project-001';
const timelineId = 'document-primary';
const occurrenceId = 'occ-1';
const baseRevisionId = fixture.primary_timeline.head.revision_id;
const basePublicationId = 'pub-a3-base';
const uuid = '00000000-0000-4000-8000-000000000001';
const objectId = `sha256:${'4'.repeat(64)}`;
const catalogDigest = `sha256:${'5'.repeat(64)}`;

type TransportCall = { method: string; path: string; headers: Record<string, string>; body?: unknown };

function json(value: unknown): Uint8Array {
  return new TextEncoder().encode(JSON.stringify(value));
}

function response(value: unknown, status = 200) {
  return { status, headers: { 'Content-Type': 'application/json' }, body: json(value) };
}

function graphWithSharedOccupiedRawV2() {
  const graph = structuredClone(fixture);
  const shared = graph.shot_revisions.find((shot) => shot.shot_id === 'shot-alpha' && shot.revision_id === 'rev-a')!;
  shared.assets.push({
    asset_id: 'alpha-audio', object_id: 'object-alpha-audio', media_type: 'audio/mpeg',
    digest: 'sha256:3333333333333333333333333333333333333333333333333333333333333333',
    scope: { project_id: projectId, shot_id: 'shot-alpha' }, role: 'source',
  });
  shared.internal_timeline_revision.timeline.tracks.unshift({ id: 'V2', kind: 'visual', label: 'Raw V2' });
  shared.internal_timeline_revision.timeline.clips.push({
    id: 'raw-v2-occupied', clip_type: 'media', track: 'V2', at_ms: 6_000, duration_ms: 1_000,
    asset_id: 'alpha-image', app: { seedRegistry: { local0: true } },
  });
  const revisionIds = new Map(graph.shot_revisions.map((shot) => [
    `${shot.shot_id}/${shot.revision_id}`, `${shot.shot_id}-${shot.revision_id}`,
  ]));
  for (const shot of graph.shot_revisions) {
    const oldRevisionId = shot.revision_id;
    shot.revision_id = revisionIds.get(`${shot.shot_id}/${oldRevisionId}`)!;
    for (const dependency of shot.dependencies) {
      dependency.revision_id = revisionIds.get(`${dependency.shot_id}/${dependency.revision_id}`) ?? dependency.revision_id;
    }
  }
  for (const occurrence of graph.occurrences) {
    const oldRevisionId = occurrence.revision_id;
    const nextRevisionId = revisionIds.get(`${occurrence.shot_id}/${oldRevisionId}`)!;
    occurrence.stable_deep_link = occurrence.stable_deep_link.replace(`/revision/${oldRevisionId}/`, `/revision/${nextRevisionId}/`);
    occurrence.revision_id = nextRevisionId;
  }
  // Enclose both the existing raw V2 clip at 6s and the requested 5s birth.
  for (const occurrence of graph.occurrences) occurrence.duration_ms = 8000;
  for (const shot of graph.shot_revisions) {
    for (const asset of shot.assets) asset.object_id = asset.digest;
    for (const input of shot.generation_inputs) input.object_id = input.digest;
    const timeline = shot.internal_timeline_revision.timeline as Record<string, unknown>;
    timeline.output = { fps: 30 };
    timeline.meta = { 'org.example.popup': { nullable: null, opaque: ['raw-v2-occupied', false] } };
    const occupied = shot.internal_timeline_revision.timeline.clips.find((clip) => clip.id === 'raw-v2-occupied');
    if (occupied) Object.assign(occupied, { params: null });
    for (const clip of shot.internal_timeline_revision.timeline.clips) {
      const raw = clip as Record<string, unknown>;
      Object.assign(raw, { at: clip.at_ms / 1000, hold: clip.duration_ms / 1000, clipType: clip.clip_type, asset: clip.asset_id });
      delete raw.at_ms;
      delete raw.duration_ms;
      delete raw.clip_type;
      delete raw.asset_id;
    }
    timeline.registry = { assets: Object.fromEntries(shot.assets.map((asset) => [asset.asset_id, {
      media_id: asset.digest, type: asset.media_type.split('/')[0],
    }])) };
    shot.internal_timeline_revision.content_digest = fixtureDigest(timeline);
    shot.timing.duration_ms = 8000;
  }
  return graph;
}

function canonicalDocument(graph: ReturnType<typeof graphWithSharedOccupiedRawV2>, revisionId = baseRevisionId): CanonicalDocument {
  const assets: Record<string, Record<string, string>> = Object.fromEntries(
    graph.shot_revisions.flatMap((shot) => shot.assets.map((asset) => [asset.asset_id, {
      media_id: asset.digest, type: asset.media_type.split('/')[0],
    }])),
  );
  const parentPayload = {
    config: { ...graph.parent_composition.config, output: { fps: 30 }, tracks: [], clips: [] },
    registry: { assets }, clips: [],
    occurrences: graph.occurrences.map((occurrence) => ({
      occurrence_id: occurrence.occurrence_id, shot_id: occurrence.shot_id, shot_revision_id: occurrence.revision_id,
      duration_ms: occurrence.duration_ms, placement_opaque: { preserved: [null, false] },
      stable_deep_link: occurrence.stable_deep_link, output_identity: occurrence.output_identity,
      placement: { start_ms: occurrence.at_ms, track: 'V1' }, source_offset: 0, speed: 1,
    })),
  };
  const sourceShots = graph.shot_revisions.filter((shot) => parentPayload.occurrences.some((occurrence) => occurrence.shot_id === shot.shot_id && occurrence.shot_revision_id === shot.revision_id));
  const shotRevisions = [...sourceShots].sort((a, b) => a.shot_id.localeCompare(b.shot_id) || a.revision_id.localeCompare(b.revision_id)).map((shot) => ({
    shot_id: shot.shot_id, revision_id: shot.revision_id,
    internal_timeline_revision_id: shot.internal_timeline_revision.revision_id,
    content_digest: fixtureDigest({
      name: `${shot.shot_id}-${shot.revision_id}`, internal_timeline_revision_id: shot.internal_timeline_revision.revision_id,
      timing: shot.timing, assets: shot.assets, dependencies: shot.dependencies,
      generation_inputs: shot.generation_inputs, provenance: shot.provenance,
    }),
    payload: {
      name: `${shot.shot_id}-${shot.revision_id}`,
      internal_timeline_revision_id: shot.internal_timeline_revision.revision_id,
      timing: shot.timing, assets: shot.assets, dependencies: shot.dependencies,
      generation_inputs: shot.generation_inputs, provenance: shot.provenance,
    },
  }));
  const internalRevisions = [...sourceShots].sort((a, b) => `timeline-${a.shot_id}-${a.revision_id}`.localeCompare(`timeline-${b.shot_id}-${b.revision_id}`)).map((shot) => ({
    timeline_id: `timeline-${shot.shot_id}-${shot.revision_id}`,
    revision_id: shot.internal_timeline_revision.revision_id,
    content_digest: shot.internal_timeline_revision.content_digest,
    payload: shot.internal_timeline_revision.timeline,
  }));
  return {
    schema_version: 1, project_id: projectId, timeline_id: timelineId,
    parent_revision: { revision_id: revisionId, content_digest: fixtureDigest(parentPayload), payload: parentPayload },
    shot_revisions: shotRevisions,
    internal_timeline_revisions: internalRevisions,
    dependency_manifest: {
      shots: shotRevisions.map(({ payload: _payload, ...pin }) => pin),
      internal_timelines: internalRevisions.map(({ payload: _payload, ...pin }) => pin),
      media: [...new Set(graph.shot_revisions.flatMap((shot) => shot.assets.map((asset) => asset.digest)))].sort().map((media_id) => ({ media_id, content_digest: media_id })), documents: [],
    },
  } as CanonicalDocument;
}

function expectedRequest(): CommitRequest {
  return {
    api_version: 1, project_id: projectId, timeline_id: timelineId,
    base_revision_id: baseRevisionId, base_publication_id: basePublicationId,
    label: 'Edit shot timeline', merge: 'fields', dry_run: false, source: { via: 'app' },
    commands: [
      { schema_version: 1, op: 'occurrence.fork', version: '1', select: `occurrence:${occurrenceId}`,
        args: { shot_id: `shot-fork-${uuid}` }, intent: { ownership: 'occurrence' }, created: [`shot:shot-fork-${uuid}`] },
      { schema_version: 1, op: 'occurrence.add-media', version: '1', select: `occurrence:${occurrenceId}`,
        args: { row: { id: 'clip-0', clipType: 'hold', track: 'V2', at: 0, hold: 5, opacity: 1, asset: 'asset-local0' },
          media: { asset: 'asset-local0', generation_id: 'generation-local0', variant_id: 'variant-local0', object_id: objectId, catalog_digest: catalogDigest } },
        intent: { ownership: 'occurrence' }, created: [`occurrence:${occurrenceId}/asset:asset-local0`, `occurrence:${occurrenceId}/clip:clip-0`] },
    ],
    steps: [{ id: uuid, label: 'Edit shot timeline', intent: 'Edit shot timeline', tags: [], command_ordinals: [0, 1], patch: [] }],
  };
}

function providerFixture(document: CanonicalDocument, status: 'accepted' | 'merged') {
  // Public source only; no Runtime service, database, acceptance port or wire capture.
  // Override the checkout/interpreter for another exact qualified source environment.
  return JSON.parse(execFileSync(process.env.A3_AGENT_PYTHON ?? '/home/user/work/venv-agent/bin/python',
    ['src/tools/travel-between-images/components/popupAuthorityFixture.py'], {
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: `${process.env.A3_AGENT_SOURCE ?? '/home/user/work/agent'}:${process.env.A3_RUNTIME_SOURCE ?? '/home/user/work/runtime'}` },
      input: JSON.stringify({ document, request: expectedRequest(), status }), encoding: 'utf8',
    })) as {
      document: CanonicalDocument; commands: CommitRequest['commands']; steps: NonNullable<CommitAcceptedMutation['data']['steps']>;
      records: Array<{ command: unknown; reads: unknown[]; bindings: unknown[]; created: unknown[] }>;
      previous: { revision_id: string; publication_id: string }; merge_mode: 'fields'; document_digest: string; provider_version: string; compiler_version: string;
    };
}

function authoritativeResponse(facts: ReturnType<typeof providerFixture>, status: 'accepted' | 'merged'): CommitAcceptedMutation {
  const previous = facts.previous;
  const data: CommitAcceptedMutation['data'] = {
    status, base_revision_id: baseRevisionId, base_publication_id: basePublicationId,
    previous_revision_id: previous.revision_id, previous_publication_id: previous.publication_id,
    accepted_revision_id: facts.document.parent_revision.revision_id,
    canonical_document: facts.document, document_digest: facts.document_digest,
    id_map: {}, commands: facts.commands, steps: facts.steps, merge_mode: facts.merge_mode,
    rebased_onto: status === 'merged' ? previous : null, label: 'Edit shot timeline',
    publisher: 'actor-a3', source: { via: 'app' }, provider_version: facts.provider_version, compiler_version: facts.compiler_version,
  };
  return { data, receipt: {
    receipt_id: 'pub-a3-accepted', command_kind: 'timeline.commit', idempotency_key: uuid,
    request_hash: fixtureDigest({ operation: 'commitTimeline', path: `/v1/projects/${projectId}/timelines/${timelineId}/commit`, publisher: 'actor-a3', request: expectedRequest() }).slice(7),
    project_id: projectId, project_seq: [1, 1], event_ids: ['event-a3'], result: data, created_at: '2026-10-24T00:00:00Z',
  } };
}

function wrapper() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <MemoryRouter><QueryClientProvider client={queryClient}><AgentChatProvider>{children}</AgentChatProvider></QueryClientProvider></MemoryRouter>
  );
}

function runtimeTransport(calls: TransportCall[], reply: () => CommitAcceptedMutation): Transport {
  return async (method, path, headers, body) => {
    const isMediaImport = path.endsWith('/media-imports');
    const rawBody = !isMediaImport && body instanceof Blob ? await body.text() : !isMediaImport && body ? new TextDecoder().decode(body) : undefined;
    const parsedBody = rawBody ? JSON.parse(rawBody) : undefined;
    calls.push({ method, path, headers, ...(parsedBody === undefined ? {} : { body: parsedBody }) });
    if (path === '/v1/health') return response({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_session_id: 'session-a3', runtime_instance_id: 'instance-a3' });
    if (path === '/v1/handshake') return response({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 'session-a3', actor_id: 'actor-a3', realm_id: 'realm-a3', scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'], capabilities: ['execution_binding.targeted.v1'] });
    if (path === '/v1/realm') return response({ realm_id: 'realm-a3', display_name: 'A3 fixture', version: 1, created_at: '2026-10-24T00:00:00Z' });
    if (method === 'POST' && path === `/v1/projects/${projectId}/media-imports`) return response({ data: { provider: 'runtime', project: projectId, import_operation_id: 'import-local0', status: 'completed', task_id: null, generation_id: 'generation-local0', variant_id: 'variant-local0', asset_id: 'asset-local0', entry: { object_id: objectId, media_type: 'image/png', size: 1234, filename: 'local0.png' }, provenance: { source: 'external_upload', origin: 'imported', actor_id: 'actor-a3' }, actor_id: 'actor-a3', duration_seconds: null }, receipt: { receipt_id: 'receipt-import-local0', command_kind: 'media.import', idempotency_key: headers['Idempotency-Key'] } }, 201);
    if (method === 'GET' && path.startsWith(`/v1/projects/${projectId}/media-selection?`)) return response({ asset: 'asset-local0', generation_id: 'generation-local0', variant_id: 'variant-local0', object_id: objectId, catalog_digest: catalogDigest } satisfies MediaSelection);
    if (method === 'POST' && path === `/v1/projects/${projectId}/timelines/${timelineId}/commit`) {
      expect(headers['Idempotency-Key']).toBe(uuid);
      expect(parsedBody).toEqual(expectedRequest());
      return response(structuredClone(reply()));
    }
    throw new Error(`Unexpected Runtime request: ${method} ${path}`);
  };
}

describe('A3 mounted popup full caller', () => {
  beforeEach(() => {
    vi.spyOn(crypto, 'randomUUID').mockReturnValue(uuid);
    resetFakeIndexedDB();
    Object.defineProperty(globalThis, 'indexedDB', { configurable: true, value: createFakeIndexedDB() });
    Object.defineProperty(navigator, 'locks', { configurable: true, value: { request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}) } });
  });

  it.each(['accepted', 'merged'] as const)('carries a real mounted shared-child add through the %s v2 commit transport', async (status) => {
    const graph = graphWithSharedOccupiedRawV2();
    const before = canonicalDocument(graph);
    for (const shot of before.shot_revisions) graph.shot_revisions.find((candidate) => candidate.revision_id === shot.revision_id)!.content_digest = shot.content_digest;
    const composition = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() }).prepare(graph);
    let facts!: ReturnType<typeof providerFixture>;
    let reply!: CommitAcceptedMutation;
    let fixtureFailure: unknown;
    const calls: TransportCall[] = [];
    const runtimeClient = new AstridRuntimeClient({ baseUrl: 'http://runtime.test', token: 'runtime-token', transport: runtimeTransport(calls, () => {
      try {
        facts = providerFixture(before, status);
        reply = authoritativeResponse(facts, status);
        return reply;
      } catch (error) { fixtureFailure = error; throw error; }
    }) });
    const runtime = new RuntimeDataProvider({ projectId, runtimeClient });
    const initial = { head: { revisionId: baseRevisionId, publicationId: basePublicationId }, canonicalDocument: before, graph };
    vi.spyOn(runtime, 'loadTimelineCommandBasis').mockResolvedValue(initial);
    vi.spyOn(runtime, 'getRecoverableIdentity').mockResolvedValue({ actorId: 'actor-a3', realmId: 'realm-a3' });
    const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
    const published = vi.fn();
    const commit = vi.spyOn(runtime, 'commitTimeline');
    const view = render(<ShotTimelinePreview composition={composition} occurrenceId={occurrenceId} shotCompositionAdapter={adapter} timelineDataProvider={runtime} onCanonicalCompositionPublished={published} />, { wrapper: wrapper() });
    try {
      await waitFor(() => expect(screen.getByRole('region', { name: 'Shot timeline' })).toHaveAttribute('data-shot-timeline-status', 'ready'));
      fireEvent.click(document.querySelector('[data-track-id="V2"]')!);
      fireEvent.click(screen.getByRole('button', { name: 'Add media' }));
      fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), { target: { files: [new File([new Uint8Array(1234)], 'local0.png', { type: 'image/png' })] } });
      await waitFor(() => expect(document.querySelector('[data-shot-timeline-canvas="true"]')).toHaveAttribute('data-shot-timeline-clip-assets', expect.stringContaining('clip-0:V2:0')));
      await waitFor(() => expect(calls.some((call) => call.path.endsWith('/commit'))).toBe(true), { timeout: 15_000 });
      const importCall = calls.find((call) => call.path.endsWith('/media-imports'))!;
      const selectionCall = calls.find((call) => call.path.includes('/media-selection?'))!;
      const commitCall = calls.find((call) => call.path.endsWith('/commit'))!;
      const request = commitCall.body as CommitRequest;
      if (fixtureFailure) throw fixtureFailure;
      expect(importCall).toMatchObject({ method: 'POST', headers: { 'Content-Type': 'image/png', 'X-Original-Name': 'local0.png' } });
      expect(selectionCall.method).toBe('GET');
      expect(commitCall.headers['Idempotency-Key']).toMatch(/^[0-9a-f-]{36}$/);
      expect(request).toMatchObject({ api_version: 1, project_id: projectId, timeline_id: timelineId, base_revision_id: baseRevisionId, base_publication_id: basePublicationId, label: 'Edit shot timeline', merge: 'fields', dry_run: false, source: { via: 'app' } });
      expect(request.commands).toHaveLength(2);
      const forkShotId = String(request.commands[0].args.shot_id);
      expect(request.commands[0]).toEqual({ schema_version: 1, op: 'occurrence.fork', version: '1', select: `occurrence:${occurrenceId}`, args: { shot_id: forkShotId }, intent: { ownership: 'occurrence' }, created: [`shot:${forkShotId}`] });
      expect(request.commands[1]).toEqual({ schema_version: 1, op: 'occurrence.add-media', version: '1', select: `occurrence:${occurrenceId}`, args: { row: { id: 'clip-0', clipType: 'hold', track: 'V2', at: 0, hold: 5, opacity: 1, asset: 'asset-local0' }, media: { asset: 'asset-local0', generation_id: 'generation-local0', variant_id: 'variant-local0', object_id: objectId, catalog_digest: catalogDigest } }, intent: { ownership: 'occurrence' }, created: [`occurrence:${occurrenceId}/asset:asset-local0`, `occurrence:${occurrenceId}/clip:clip-0`] });
      expect(request.steps).toHaveLength(1);
      expect(request.steps?.[0]?.patch).toEqual([]);
      expect(request.reads).toBeUndefined();
      expect(commit).toHaveBeenCalledTimes(1);
      const commitResponse = (await commit.mock.results[0].value).response;
      await waitFor(() => expect(published).toHaveBeenCalled());
      expect(commitResponse.data).toMatchObject({ status, canonical_document: { parent_revision: { payload: { occurrences: expect.arrayContaining([expect.objectContaining({ occurrence_id: occurrenceId, shot_id: `shot-fork-${uuid}` })]) } } }, document_digest: expect.stringMatching(/^sha256:/), merge_mode: 'fields', accepted_revision_id: facts.document.parent_revision.revision_id, publisher: 'actor-a3' });
      expect(commitResponse).toEqual(reply);
      expect(commitResponse.data.commands).toEqual(facts.records.map((record) => record.command));
      expect(commitResponse.data.steps?.[0]?.dependencies.length).toBeGreaterThan(0);
      expect(facts.records.every((record) => record.reads.length && record.bindings.length && record.created.length)).toBe(true);
      expect(published.mock.calls.at(-1)?.[0].headRevisionId).toBe(facts.document.parent_revision.revision_id);
      const owners = await createCommitOutbox().list({ realmId: 'realm-a3', actorId: 'actor-a3', projectId, timelineId });
      expect(owners).toHaveLength(1);
      expect(owners[0].intents).toEqual([]);
      expect(owners[0].pending).toBeUndefined();
      expect(owners[0].accepted).toMatchObject({ head: { revisionId: facts.document.parent_revision.revision_id, publicationId: 'pub-a3-accepted' },
        value: { canonicalDocument: facts.document, response: reply } });
      const internalRevisions = commitResponse.data.canonical_document.internal_timeline_revisions as Array<{ payload: { clips: Array<{ id: string; asset_id?: string }> } }>;
      expect(internalRevisions.some((internal) => internal.payload.clips.some((clip) => clip.id === 'clip-0' && (clip as unknown as { asset: string }).asset === 'asset-local0'))).toBe(true);
    } finally { view.unmount(); }
  });
});
