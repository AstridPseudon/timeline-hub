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

type TransportCall = {
  method: string;
  path: string;
  headers: Record<string, string>;
  body?: unknown;
};

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
    asset_id: 'alpha-audio',
    object_id: 'object-alpha-audio',
    media_type: 'audio/mpeg',
    digest: 'sha256:3333333333333333333333333333333333333333333333333333333333333333',
    scope: { project_id: projectId, shot_id: 'shot-alpha' },
    role: 'source',
  });
  shared.internal_timeline_revision.timeline.tracks.unshift({ id: 'V2', kind: 'visual', label: 'Raw V2' });
  shared.internal_timeline_revision.timeline.clips.push({
    id: 'raw-v2-occupied',
    clip_type: 'media',
    track: 'V2',
    at_ms: 6_000,
    duration_ms: 1_000,
    asset_id: 'alpha-image',
    app: { seedRegistry: { local0: true } },
  });
  return graph;
}

function canonicalDocument(graph: ReturnType<typeof graphWithSharedOccupiedRawV2>, revisionId = baseRevisionId): CanonicalDocument {
  const assets: Record<string, Record<string, string>> = Object.fromEntries(
    graph.shot_revisions.flatMap((shot) => shot.assets.map((asset) => [asset.asset_id, {
      file: asset.object_id,
      media_id: asset.object_id,
      type: asset.media_type,
    }])),
  );
  assets['alpha-audio'] = { file: 'object-alpha-audio', media_id: 'object-alpha-audio', type: 'audio/mpeg' };
  const parentPayload = {
    config: {
      ...graph.parent_composition.config,
      registry: {
        assets,
      },
    },
    occurrences: graph.occurrences.map((occurrence) => ({
      occurrence_id: occurrence.occurrence_id,
      shot_id: occurrence.shot_id,
      shot_revision_id: occurrence.revision_id,
    })),
  };
  const shotRevisions = graph.shot_revisions.map((shot) => ({
    shot_id: shot.shot_id,
    revision_id: shot.revision_id,
    internal_timeline_revision_id: shot.internal_timeline_revision.revision_id,
    content_digest: shot.content_digest,
    payload: {
      name: `${shot.shot_id}-${shot.revision_id}`,
      internal_timeline_revision_id: shot.internal_timeline_revision.revision_id,
      timing: shot.timing,
      assets: shot.assets,
      dependencies: shot.dependencies,
      generation_inputs: shot.generation_inputs,
      provenance: shot.provenance,
    },
  }));
  const internalRevisions = graph.shot_revisions.map((shot) => ({
    timeline_id: `timeline-${shot.shot_id}-${shot.revision_id}`,
    revision_id: shot.internal_timeline_revision.revision_id,
    content_digest: shot.internal_timeline_revision.content_digest,
    payload: shot.internal_timeline_revision.timeline,
  }));
  return {
    schema_version: 1,
    project_id: projectId,
    timeline_id: timelineId,
    parent_revision: {
      revision_id: revisionId,
      content_digest: fixtureDigest(parentPayload),
      payload: parentPayload,
    },
    shot_revisions: shotRevisions,
    internal_timeline_revisions: internalRevisions,
    dependency_manifest: {
      shots: shotRevisions.map(({ payload: _payload, ...pin }) => pin),
      internal_timelines: internalRevisions.map(({ payload: _payload, ...pin }) => pin),
      media: [],
      documents: [],
    },
  } as CanonicalDocument;
}

function wrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <MemoryRouter>
      <QueryClientProvider client={queryClient}>
        <AgentChatProvider>{children}</AgentChatProvider>
      </QueryClientProvider>
    </MemoryRouter>
  );
}

function runtimeTransport(calls: TransportCall[], acceptedDocument: CanonicalDocument): Transport {
  return async (method, path, headers, body) => {
    const isMediaImport = path.endsWith('/media-imports');
    const rawBody = !isMediaImport && body instanceof Blob
      ? await body.text()
      : !isMediaImport && body
        ? new TextDecoder().decode(body)
        : undefined;
    const parsedBody = rawBody ? JSON.parse(rawBody) : undefined;
    calls.push({ method, path, headers, ...(parsedBody === undefined ? {} : { body: parsedBody }) });

    if (path === '/v1/health') {
      return response({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
        runtime_epoch: 1, runtime_session_id: 'session-a3', runtime_instance_id: 'instance-a3' });
    }
    if (path === '/v1/handshake') {
      return response({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
        session_id: 'session-a3', actor_id: 'actor-a3', realm_id: 'realm-a3',
        scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'],
        capabilities: ['execution_binding.targeted.v1'] });
    }
    if (path === '/v1/realm') {
      return response({ realm_id: 'realm-a3', display_name: 'A3 fixture', version: 1, created_at: '2026-10-24T00:00:00Z' });
    }
    if (method === 'POST' && path === `/v1/projects/${projectId}/media-imports`) {
      return response({
        data: {
          provider: 'runtime', project: projectId, import_operation_id: 'import-local0', status: 'completed',
          task_id: null, generation_id: 'generation-local0', variant_id: 'variant-local0', asset_id: 'asset-local0',
          entry: { object_id: 'object-local0', media_type: 'image/png', size: 1234, filename: 'local0.png' },
          provenance: { source: 'external_upload', origin: 'imported', actor_id: 'actor-a3' },
          actor_id: 'actor-a3', duration_seconds: null,
        },
        receipt: { receipt_id: 'receipt-import-local0', command_kind: 'media.import', idempotency_key: headers['Idempotency-Key'] },
      }, 201);
    }
    if (method === 'GET' && path.startsWith(`/v1/projects/${projectId}/media-selection?`)) {
      const selection: MediaSelection = {
        asset: 'asset-local0', generation_id: 'generation-local0', variant_id: 'variant-local0',
        object_id: 'object-local0', catalog_digest: 'sha256:catalog-local0',
      };
      return response(selection);
    }
    if (method === 'POST' && path === `/v1/projects/${projectId}/timelines/${timelineId}/commit`) {
      const request = parsedBody as CommitRequest;
      const accepted = acceptedCommit(
        { revision_id: 'rev-a3-accepted', publication_id: 'pub-a3-accepted' },
        { revision_id: request.base_revision_id, publication_id: request.base_publication_id },
        { projectId, timelineId, commands: request.commands },
      );
      accepted.data.canonical_document = acceptedDocument;
      accepted.data.document_digest = fixtureDigest(acceptedDocument);
      Object.assign(accepted.data, {
        status: 'accepted',
        base_revision_id: request.base_revision_id,
        base_publication_id: request.base_publication_id,
        previous_revision_id: request.base_revision_id,
        previous_publication_id: request.base_publication_id,
        accepted_revision_id: acceptedDocument.parent_revision.revision_id,
        rebased_onto: null,
        commands: request.commands,
        steps: request.steps,
        merge_mode: request.merge,
        publisher: 'actor-a3',
      });
      accepted.receipt.idempotency_key = headers['Idempotency-Key']!;
      accepted.receipt.request_hash = fixtureDigest({ operation: 'commitTimeline', path, publisher: 'actor-a3', request }).slice(7);
      accepted.receipt.result = accepted.data;
      return response(accepted);
    }
    throw new Error(`Unexpected Runtime request: ${method} ${path}`);
  };
}

describe('A3 mounted popup full caller witness', () => {
  beforeEach(() => {
    resetFakeIndexedDB();
    Object.defineProperty(globalThis, 'indexedDB', { configurable: true, value: createFakeIndexedDB() });
    Object.defineProperty(navigator, 'locks', { configurable: true, value: {
      request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}),
    } });
  });

  // Remove `fails` once the mounted projection stops exposing derived `assetEntry`
  // fields to serialized existing clips, allowing this unchanged expectation to
  // reach the A2 outbox and Runtime commit assertions below.
  it.fails('carries a real mounted shared-child image add from import through the v2 commit transport', async () => {
    const graph = graphWithSharedOccupiedRawV2();
    const composition = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() }).prepare(graph);
    const before = canonicalDocument(graph);
    const calls: TransportCall[] = [];
    const runtimeClient = new AstridRuntimeClient({
      baseUrl: 'http://runtime.test', token: 'runtime-token',
      transport: runtimeTransport(calls, canonicalDocument(graph, 'rev-a3-accepted')),
    });
    const runtime = new RuntimeDataProvider({ projectId, runtimeClient });
    let commitResult: Awaited<ReturnType<RuntimeDataProvider['commitTimeline']>> | undefined;
    const commit = runtime.commitTimeline.bind(runtime);
    vi.spyOn(runtime, 'commitTimeline').mockImplementation(async (request, key) => {
      commitResult = await commit(request, key);
      return commitResult;
    });
    vi.spyOn(runtime, 'loadTimelineCommandBasis').mockResolvedValue({
      head: { revisionId: baseRevisionId, publicationId: basePublicationId },
      canonicalDocument: before,
      graph,
    });
    const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
    const view = render(
      <ShotTimelinePreview
        composition={composition}
        occurrenceId={occurrenceId}
        shotCompositionAdapter={adapter}
        timelineDataProvider={runtime}
      />,
      { wrapper: wrapper() },
    );

    try {
      await waitFor(() => expect(screen.getByRole('region', { name: 'Shot timeline' })).toHaveAttribute('data-shot-timeline-status', 'ready'));
      const v2 = document.querySelector('[data-track-id="V2"]');
      expect(v2).toBeTruthy();
      fireEvent.click(v2!);

      fireEvent.click(screen.getByRole('button', { name: 'Add media' }));
      fireEvent.change(screen.getByLabelText('Choose media for shot timeline'), {
        target: { files: [new File([new Uint8Array(1234)], 'local0.png', { type: 'image/png' })] },
      });

      await waitFor(() => expect(document.querySelector('[data-shot-timeline-canvas="true"]'))
        .toHaveAttribute('data-shot-timeline-clip-assets', expect.stringContaining('clip-0:V2:0')));
      await waitFor(() => expect(calls.some((call) => call.path.endsWith('/commit'))).toBe(true), { timeout: 15_000 });

      const importCall = calls.find((call) => call.path.endsWith('/media-imports'))!;
      expect(importCall.method).toBe('POST');
      expect(importCall.headers['Content-Type']).toBe('image/png');
      expect(importCall.headers['X-Original-Name']).toBe('local0.png');
      const selectionCall = calls.find((call) => call.path.includes('/media-selection?'))!;
      expect(selectionCall.method).toBe('GET');
      const commitCall = calls.find((call) => call.path.endsWith('/commit'))!;
      const request = commitCall.body as CommitRequest;
      const commitKey = commitCall.headers['Idempotency-Key'];

      expect(commitKey).toMatch(/^astrid\.shot-popup\./);
      expect(request).toMatchObject({
        api_version: 1,
        project_id: projectId,
        timeline_id: timelineId,
        base_revision_id: baseRevisionId,
        base_publication_id: basePublicationId,
        label: 'Add media',
        merge: 'atomic',
        dry_run: false,
        source: { via: 'app' },
      });
      expect(request.commands).toHaveLength(2);
      expect(request.commands[0]).toMatchObject({
        schema_version: 1, op: 'occurrence.fork', version: '1', select: `occurrence:${occurrenceId}`,
        args: { shot_id: expect.any(String) }, intent: { ownership: 'occurrence' }, created: [expect.stringMatching(/^shot:/)],
      });
      expect(request.commands[1]).toMatchObject({
        schema_version: 1, op: 'occurrence.add-media', version: '1', select: `occurrence:${occurrenceId}`,
        args: {
          row: expect.objectContaining({ track: 'V2', asset: 'asset-local0', at: 0, hold: 5, clipType: 'hold' }),
          media: {
            asset: 'asset-local0', generation_id: 'generation-local0', variant_id: 'variant-local0',
            object_id: 'object-local0', catalog_digest: 'sha256:catalog-local0',
          },
        },
        intent: { ownership: 'occurrence' },
        created: [
          `occurrence:${occurrenceId}/asset:asset-local0`,
          `occurrence:${occurrenceId}/clip:clip-0`,
        ],
      });
      expect(request.steps).toEqual(expect.arrayContaining([
        expect.objectContaining({ id: expect.any(String), label: 'Add media', intent: 'Add media', tags: expect.any(Array), command_ordinals: [0, 1] }),
      ]));
      expect(request.reads).toEqual(expect.arrayContaining([
        expect.objectContaining({ ref: 'parent', path: ['occurrences'] }),
      ]));
      expect(request.commands.every((command) => command.op && command.version && command.select !== undefined && command.args)).toBe(true);

      expect(commitResult).toBeDefined();
      expect(commitResult!.response.data).toMatchObject({
        status: 'accepted',
        canonical_document: expect.any(Object),
        document_digest: expect.stringMatching(/^sha256:/),
        id_map: {},
        commands: request.commands,
        steps: request.steps,
        merge_mode: 'atomic',
        base_revision_id: baseRevisionId,
        base_publication_id: basePublicationId,
        previous_revision_id: baseRevisionId,
        previous_publication_id: basePublicationId,
        accepted_revision_id: 'rev-a3-accepted',
        publisher: 'actor-a3',
      });
      expect(commitResult!.receipt).toMatchObject({
        receipt_id: 'pub-a3-accepted', command_kind: 'timeline.commit', idempotency_key: commitKey,
        request_hash: expect.any(String), project_id: projectId, project_seq: expect.any(Array),
        event_ids: expect.any(Array), result: commitResult!.response.data, created_at: expect.any(String),
      });
      expect(commitResult!.accepted).toEqual({ revisionId: 'rev-a3-accepted', publicationId: 'pub-a3-accepted' });
      expect(screen.getByRole('region', { name: 'Shot timeline' })).toHaveAttribute('data-shot-timeline-head-revision-id', 'rev-a3-accepted');
    } finally {
      view.unmount();
    }
  });
});
