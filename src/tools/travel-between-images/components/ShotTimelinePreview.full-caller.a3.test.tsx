// @vitest-environment jsdom
import React from 'react';
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
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { Transport } from '@/integrations/runtime/generated.ts';
import type { CanonicalDocument, CommitRequest, MediaSelection } from '@/integrations/runtime/timeline-commit-types.ts';
import { createShotCompositionAdapter } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { ShotTimelinePreview } from './ShotTimelinePreview.tsx';

const projectId = 'project-001';
const timelineId = 'document-primary';
const occurrenceId = 'occ-1';
const baseRevisionId = fixture.primary_timeline.head.revision_id;
const basePublicationId = 'pub-a3-base';

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
  return graph;
}

function canonicalDocument(graph: ReturnType<typeof graphWithSharedOccupiedRawV2>, revisionId = baseRevisionId): CanonicalDocument {
  const assets: Record<string, Record<string, string>> = Object.fromEntries(
    graph.shot_revisions.flatMap((shot) => shot.assets.map((asset) => [asset.asset_id, {
      file: asset.object_id, media_id: asset.object_id, type: asset.media_type,
    }])),
  );
  const parentPayload = {
    config: { ...graph.parent_composition.config, registry: { assets } },
    occurrences: graph.occurrences.filter((occurrence) => occurrence.occurrence_id === 'occ-1' || occurrence.occurrence_id === 'occ-2').map((occurrence) => ({
      occurrence_id: occurrence.occurrence_id, shot_id: occurrence.shot_id, shot_revision_id: occurrence.revision_id,
    })),
  };
  const shotRevisions = graph.shot_revisions.map((shot) => ({
    shot_id: shot.shot_id, revision_id: shot.revision_id,
    internal_timeline_revision_id: shot.internal_timeline_revision.revision_id,
    content_digest: shot.content_digest,
    payload: {
      name: `${shot.shot_id}-${shot.revision_id}`,
      internal_timeline_revision_id: shot.internal_timeline_revision.revision_id,
      timing: shot.timing, assets: shot.assets, dependencies: shot.dependencies,
      generation_inputs: shot.generation_inputs, provenance: shot.provenance,
    },
  }));
  const internalRevisions = graph.shot_revisions.map((shot) => ({
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
      media: [], documents: [],
    },
  } as CanonicalDocument;
}

function authoritativeAddedDocument(
  graph: ReturnType<typeof graphWithSharedOccupiedRawV2>,
  request: CommitRequest,
): CanonicalDocument {
  const document = canonicalDocument(graph, 'rev-a3-accepted');
  const forkShotId = String(request.commands[0]?.args.shot_id);
  const forkRevisionId = 'rev-a3-fork';
  const forkInternalRevisionId = 'timeline-a3-fork';
  const sourceOccurrence = (document.parent_revision.payload as { occurrences: Array<{ occurrence_id: string; shot_id: string; shot_revision_id: string }> }).occurrences.find((occurrence) => occurrence.occurrence_id === occurrenceId)!;
  const sourceShot = document.shot_revisions.find((shot) => shot.shot_id === sourceOccurrence.shot_id && shot.revision_id === sourceOccurrence.shot_revision_id)!;
  const sourceInternal = document.internal_timeline_revisions.find((internal) => internal.revision_id === sourceShot.internal_timeline_revision_id)!;
  const mediaCommand = request.commands[1]!;
  const row = mediaCommand.args.row as { id: string; clipType: string; track: string; at: number; hold: number; asset: string };
  const media = mediaCommand.args.media as MediaSelection;
  const forkInternalPayload = structuredClone(sourceInternal.payload) as { clips: Record<string, unknown>[]; [key: string]: unknown };
  forkInternalPayload.clips = [...forkInternalPayload.clips, {
    id: row.id, clip_type: row.clipType, track: row.track, at_ms: row.at * 1000,
    duration_ms: row.hold * 1000, asset_id: row.asset,
  }];
  const forkInternal = {
    timeline_id: `timeline-${forkShotId}`, revision_id: forkInternalRevisionId,
    content_digest: fixtureDigest(forkInternalPayload), payload: forkInternalPayload,
  };
  const forkShotPayload = structuredClone(sourceShot.payload) as Record<string, unknown>;
  forkShotPayload.internal_timeline_revision_id = forkInternalRevisionId;
  forkShotPayload.assets = [...(forkShotPayload.assets as unknown[]), {
    asset_id: media.asset, object_id: media.object_id, media_type: 'image/png',
    digest: fixtureDigest(media.object_id), scope: { project_id: projectId, shot_id: forkShotId }, role: 'source',
  }];
  const forkShot = {
    shot_id: forkShotId, revision_id: forkRevisionId, internal_timeline_revision_id: forkInternalRevisionId,
    content_digest: fixtureDigest(forkShotPayload), payload: forkShotPayload,
  };
  document.shot_revisions.push(forkShot);
  document.internal_timeline_revisions.push(forkInternal);
  const parentPayload = document.parent_revision.payload as { config: { registry: { assets: Record<string, unknown> } }; occurrences: Record<string, unknown>[] };
  const occurrence = parentPayload.occurrences.find((candidate) => candidate.occurrence_id === occurrenceId)!;
  occurrence.shot_id = forkShotId;
  occurrence.shot_revision_id = forkRevisionId;
  parentPayload.config.registry.assets[media.asset] = {
    file: media.object_id, media_id: media.object_id, type: 'image/png',
    generationId: 'generation-local0', variantId: 'variant-local0',
  };
  document.parent_revision.content_digest = fixtureDigest(parentPayload);
  document.dependency_manifest.shots.push({
    shot_id: forkShotId, revision_id: forkRevisionId, internal_timeline_revision_id: forkInternalRevisionId,
    content_digest: forkShot.content_digest,
  });
  document.dependency_manifest.internal_timelines.push({
    timeline_id: forkInternal.timeline_id, revision_id: forkInternalRevisionId, content_digest: forkInternal.content_digest,
  });
  document.dependency_manifest.media.push({ media_id: fixtureDigest(media.object_id), content_digest: fixtureDigest(media.object_id) });
  return document;
}

function wrapper() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <MemoryRouter><QueryClientProvider client={queryClient}><AgentChatProvider>{children}</AgentChatProvider></QueryClientProvider></MemoryRouter>
  );
}

function runtimeTransport(calls: TransportCall[], graph: ReturnType<typeof graphWithSharedOccupiedRawV2>, status: 'accepted' | 'merged'): Transport {
  return async (method, path, headers, body) => {
    const isMediaImport = path.endsWith('/media-imports');
    const rawBody = !isMediaImport && body instanceof Blob ? await body.text() : !isMediaImport && body ? new TextDecoder().decode(body) : undefined;
    const parsedBody = rawBody ? JSON.parse(rawBody) : undefined;
    calls.push({ method, path, headers, ...(parsedBody === undefined ? {} : { body: parsedBody }) });
    if (path === '/v1/health') return response({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_session_id: 'session-a3', runtime_instance_id: 'instance-a3' });
    if (path === '/v1/handshake') return response({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 'session-a3', actor_id: 'actor-a3', realm_id: 'realm-a3', scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'], capabilities: ['execution_binding.targeted.v1'] });
    if (path === '/v1/realm') return response({ realm_id: 'realm-a3', display_name: 'A3 fixture', version: 1, created_at: '2026-10-24T00:00:00Z' });
    if (method === 'POST' && path === `/v1/projects/${projectId}/media-imports`) return response({ data: { provider: 'runtime', project: projectId, import_operation_id: 'import-local0', status: 'completed', task_id: null, generation_id: 'generation-local0', variant_id: 'variant-local0', asset_id: 'asset-local0', entry: { object_id: 'object-local0', media_type: 'image/png', size: 1234, filename: 'local0.png' }, provenance: { source: 'external_upload', origin: 'imported', actor_id: 'actor-a3' }, actor_id: 'actor-a3', duration_seconds: null }, receipt: { receipt_id: 'receipt-import-local0', command_kind: 'media.import', idempotency_key: headers['Idempotency-Key'] } }, 201);
    if (method === 'GET' && path.startsWith(`/v1/projects/${projectId}/media-selection?`)) return response({ asset: 'asset-local0', generation_id: 'generation-local0', variant_id: 'variant-local0', object_id: 'object-local0', catalog_digest: 'sha256:catalog-local0' } satisfies MediaSelection);
    if (method === 'POST' && path === `/v1/projects/${projectId}/timelines/${timelineId}/commit`) {
      const request = parsedBody as CommitRequest;
      const document = authoritativeAddedDocument(graph, request);
      const result = acceptedCommit({ revision_id: document.parent_revision.revision_id, publication_id: 'pub-a3-accepted' }, { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, { projectId, timelineId, commands: request.commands });
      const sourceRevisionId = (document.parent_revision.payload as { occurrences: Array<{ occurrence_id: string; shot_revision_id: string }> }).occurrences.find((occurrence) => occurrence.occurrence_id === occurrenceId)!.shot_revision_id;
      const effects = [{ op: 'set', ref: 'parent', path: ['occurrences', 'occurrence_id:occ-1', 'shot_revision_id'], before: { state: 'present', value: sourceRevisionId }, value: 'rev-a3-fork' }];
      const dependencies = request.reads ?? [{ kind: 'scope', ref: `internal-revision:${baseRevisionId}`, path: [] }];
      Object.assign(result.data, { status, canonical_document: document, document_digest: fixtureDigest(document), base_revision_id: request.base_revision_id, base_publication_id: request.base_publication_id, previous_revision_id: status === 'merged' ? 'rev-intervening' : request.base_revision_id, previous_publication_id: status === 'merged' ? 'pub-intervening' : request.base_publication_id, accepted_revision_id: document.parent_revision.revision_id, rebased_onto: status === 'merged' ? { revision_id: 'rev-intervening', publication_id: 'pub-intervening' } : null, commands: request.commands, steps: [{ ...request.steps![0], patch: effects, dependencies }], merge_mode: request.merge, publisher: 'actor-a3', source: { via: 'app' }, label: 'Edit shot timeline' });
      result.receipt.idempotency_key = headers['Idempotency-Key']!;
      result.receipt.request_hash = fixtureDigest({ operation: 'commitTimeline', path, publisher: 'actor-a3', request }).slice(7);
      result.receipt.result = result.data;
      return response(result);
    }
    throw new Error(`Unexpected Runtime request: ${method} ${path}`);
  };
}

describe('A3 mounted popup full caller', () => {
  beforeEach(() => {
    resetFakeIndexedDB();
    Object.defineProperty(globalThis, 'indexedDB', { configurable: true, value: createFakeIndexedDB() });
    Object.defineProperty(navigator, 'locks', { configurable: true, value: { request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}) } });
  });

  it.each(['accepted', 'merged'] as const)('carries a real mounted shared-child add through the %s v2 commit transport', async (status) => {
    const graph = graphWithSharedOccupiedRawV2();
    const composition = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() }).prepare(graph);
    const before = canonicalDocument(graph);
    const calls: TransportCall[] = [];
    const runtimeClient = new AstridRuntimeClient({ baseUrl: 'http://runtime.test', token: 'runtime-token', transport: runtimeTransport(calls, graph, status) });
    const runtime = new RuntimeDataProvider({ projectId, runtimeClient });
    const initial = { head: { revisionId: baseRevisionId, publicationId: basePublicationId }, canonicalDocument: before, graph };
    vi.spyOn(runtime, 'loadTimelineCommandBasis').mockResolvedValue(initial);
    vi.spyOn(runtime, 'getRecoverableIdentity').mockResolvedValue({ actorId: 'actor-a3', realmId: 'realm-a3' });
    const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
    const view = render(<ShotTimelinePreview composition={composition} occurrenceId={occurrenceId} shotCompositionAdapter={adapter} timelineDataProvider={runtime} />, { wrapper: wrapper() });
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
      expect(importCall).toMatchObject({ method: 'POST', headers: { 'Content-Type': 'image/png', 'X-Original-Name': 'local0.png' } });
      expect(selectionCall.method).toBe('GET');
      expect(commitCall.headers['Idempotency-Key']).toMatch(/^[0-9a-f-]{36}$/);
      expect(request).toMatchObject({ api_version: 1, project_id: projectId, timeline_id: timelineId, base_revision_id: baseRevisionId, base_publication_id: basePublicationId, label: 'Edit shot timeline', merge: 'fields', dry_run: false, source: { via: 'app' } });
      expect(request.commands).toHaveLength(2);
      const forkShotId = String(request.commands[0].args.shot_id);
      expect(request.commands[0]).toEqual({ schema_version: 1, op: 'occurrence.fork', version: '1', select: `occurrence:${occurrenceId}`, args: { shot_id: forkShotId }, intent: { ownership: 'occurrence' }, created: [`shot:${forkShotId}`] });
      expect(request.commands[1]).toEqual({ schema_version: 1, op: 'occurrence.add-media', version: '1', select: `occurrence:${occurrenceId}`, args: { row: { id: 'clip-0', clipType: 'hold', track: 'V2', at: 0, hold: 5, opacity: 1, asset: 'asset-local0' }, media: { asset: 'asset-local0', generation_id: 'generation-local0', variant_id: 'variant-local0', object_id: 'object-local0', catalog_digest: 'sha256:catalog-local0' } }, intent: { ownership: 'occurrence' }, created: [`occurrence:${occurrenceId}/asset:asset-local0`, `occurrence:${occurrenceId}/clip:clip-0`] });
      expect(request.steps).toHaveLength(1);
      expect(request.steps?.[0]?.patch).toEqual([]);
      expect(request.reads).toBeUndefined();
      const commitResponse = (await runtime.commitTimeline(request, commitCall.headers['Idempotency-Key'])).response;
      expect(commitResponse.data).toMatchObject({ status, canonical_document: { parent_revision: { payload: { occurrences: expect.arrayContaining([expect.objectContaining({ occurrence_id: occurrenceId, shot_revision_id: 'rev-a3-fork' })]) } } }, document_digest: expect.stringMatching(/^sha256:/), merge_mode: 'fields', accepted_revision_id: 'rev-a3-accepted', publisher: 'actor-a3' });
      expect(commitResponse.data.steps?.[0]?.dependencies).toEqual([{ kind: 'scope', ref: `internal-revision:${baseRevisionId}`, path: [] }]);
      const internalRevisions = commitResponse.data.canonical_document.internal_timeline_revisions as Array<{ payload: { clips: Array<{ id: string; asset_id?: string }> } }>;
      expect(internalRevisions.some((internal) => internal.payload.clips.some((clip) => clip.id === 'clip-0' && clip.asset_id === 'asset-local0'))).toBe(true);
    } finally { view.unmount(); }
  });
});
