// @vitest-environment jsdom
import React, { useLayoutEffect, useRef } from 'react';
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { DocumentPin, HistoryEntry, HistoryPage, CommitRequest } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { TimelineCommandBasis } from '@/tools/video-editor/data/DataProvider.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { TimelineStoreProvider, createTimelineStore, type TimelineStoreApi } from '@/tools/video-editor/hooks/timelineStore.ts';
import { useTimelineSave } from '@/tools/video-editor/hooks/useTimelineSave.ts';
import { createInteractionState } from '@/tools/video-editor/lib/interaction-state.ts';
import { AstridElementParams } from './AstridElementParams.tsx';
import { document as commandDocument, environment, scope } from '@/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts';

const descriptor = {
  id: 'v3-glow', kind: 'effect' as const, packId: 'astrid-v3', revision: 'rev-7',
  componentPath: 'packs/v3/glow',
  schema: { title: 'Glow', properties: { amount: { type: 'number', title: 'Amount' } } },
};
const pin: DocumentPin = { document_id: 'pack-document', version: 1, content_digest: `sha256:${'a'.repeat(64)}` };
const object = { object_id: `sha256:${'b'.repeat(64)}`, digest: `sha256:${'b'.repeat(64)}`, size: 12, media_type: 'application/json' as const };
const select = 'parent/clip:clip-v3-glow';

function selectedDocument() {
  const document = commandDocument();
  const clip = {
    id: 'clip-v3-glow', track: 'V1', at: 0, hold: 2, clipType: 'effect-layer',
    elementRef: { packId: descriptor.packId, id: descriptor.id, kind: descriptor.kind, revision: descriptor.revision },
    params: { amount: 0 },
  };
  document.parent_revision.payload.config = { ...document.parent_revision.payload.config, clips: [clip] };
  document.parent_revision.payload.clips = [clip];
  document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
  return document;
}

function historyBasis(canonicalDocument: TimelineCommandBasis['canonicalDocument']): TimelineCommandBasis {
  const root = {
    publication_id: 'p0', revision_id: 'r0', previous: null, receipt: {}, intent: 'bootstrap', records: null,
    provider_version: null, compiler_version: null, publisher: 'agent-1',
  } satisfies Partial<HistoryEntry>;
  const element = { packId: descriptor.packId, id: descriptor.id, kind: descriptor.kind, revision: descriptor.revision };
  const selected = {
    publication_id: 'p1', revision_id: 'r1', previous: { publication_id: 'p0', revision_id: 'r0' },
    receipt: {}, intent: 'recorded', provider_version: null, compiler_version: null, publisher: 'agent-1',
    records: {
      schema_version: 1, undo_of: [], restored_from: null,
      commands: [{
        ordinal: 0,
        command: { schema_version: 1, op: 'clip.set-element', version: '1', select,
          args: { elementRef: element, schema_source: pin } },
        writes: [], reads: [], selections: [], created: [], derived_writes: [],
        bindings: [
          { key: 'scalar.target', ref: select, policy: 'fixed', dependencies: ['scalar.images'] },
          { key: 'params.element', ref: select, policy: 'fixed', dependencies: ['params.schema', 'params.snapshot'] },
        ],
        dependencies: [
          { key: 'params.schema', kind: 'source', pin, policy: 'exact' },
          { key: 'params.snapshot', kind: 'entity', pin: { source: pin, element, object }, policy: 'exact' },
        ],
      }],
    },
  } satisfies Partial<HistoryEntry>;
  const history: HistoryPage = {
    items: [root, selected] as HistoryEntry[], next_cursor: null, head: { revision_id: 'r1', publication_id: 'p1' },
  };
  const document = structuredClone(canonicalDocument);
  document.parent_revision.revision_id = 'r1';
  document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
  return { head: { revisionId: 'r1', publicationId: 'p1' }, canonicalDocument: document, history };
}

function MountedForm({
  provider,
  store,
  initial,
  latest,
  onChange,
}: {
  provider: Awaited<ReturnType<typeof environment>>['provider'];
  store: TimelineStoreApi;
  initial: TimelineData;
  latest: React.MutableRefObject<ReturnType<typeof useTimelineSave> | undefined>;
  onChange: () => void;
}) {
  const queries = { timelineQuery: { data: initial, isLoading: false }, assetRegistryQuery: { data: initial.registry } };
  const save = useTimelineSave(queries, provider, { current: createInteractionState() }, store, initial as never);
  latest.current = save;
  useLayoutEffect(() => {
    store.getState().syncSlices({
      data: { ...store.getState().data, data: save.data, resolvedConfig: save.data?.resolvedConfig ?? null, dataRef: save.dataRef },
      ops: { ...store.getState().ops, selectedParam: save.commands.clipParamsPort },
    });
  }, [save, store]);
  const clip = save.data?.resolvedConfig.clips[0] ?? null;
  return <AstridElementParams clip={clip} registry={{}} onChange={onChange} />;
}

function runtime(provider: Awaited<ReturnType<typeof environment>>['provider']): VideoEditorRuntimeContextValue {
  return {
    provider, timelineId: scope.timelineId, astridElementHost: { descriptors: [descriptor] },
    project: { projectId: scope.projectId }, shots: { canonicalDraft: null },
    assetResolver: { resolveAssetUrl: async (value: string) => value },
  } as unknown as VideoEditorRuntimeContextValue;
}

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe('AstridElementParams mounted command-session path', () => {
  it('uses the production selected carrier, retains exact inputs, and preserves a draft when its basis changes during an async read', async () => {
    const env = await environment(selectedDocument());
    vi.stubGlobal('indexedDB', env.factory);
    vi.stubGlobal('navigator', { locks: { request: async (_key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => work({ name: 'test' }) } });
    const basis = historyBasis(env.initial.canonicalDocument);
    vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockResolvedValue(basis);
    const verified = {
      pin,
      document: {
        kind: 'astrid.project-pack', project_id: scope.projectId, document_id: pin.document_id, version: pin.version,
        content: {
          schema: 'astrid.project-pack/v1', source_binding_key: 'project-packs', pack_id: descriptor.packId,
          relative_manifest: `${scope.realmId}/${scope.projectId}/packs/${descriptor.packId}/pack.yaml`,
          admissions: [{ id: descriptor.id, kind: descriptor.kind, revision: descriptor.revision, snapshot_object: object }],
        },
      },
    };
    const client = env.provider.paramReadClient!;
    vi.spyOn(client, 'getProjectVerifiedDocument').mockResolvedValue(verified);
    vi.spyOn(client, 'getProjectVerifiedDocumentObject').mockResolvedValue({ ...object, bytes_base64: 'e30=' });
    const requests: CommitRequest[] = [];
    vi.spyOn(env.provider, 'commitTimeline').mockImplementation(async (request) => {
      requests.push(request);
      const response = acceptedCommit({ revision_id: 'r2', publication_id: 'p2' }, { revision_id: 'r1', publication_id: 'p1' }, { commands: request.commands });
      return {
        response,
        accepted: { revisionId: 'r2', publicationId: 'p2' },
        canonicalDocument: basis.canonicalDocument,
        graph: {},
        receipt: response.receipt,
      };
    });
    const store = createTimelineStore();
    store.getState().setMounted(true);
    const latest: React.MutableRefObject<ReturnType<typeof useTimelineSave> | undefined> = { current: undefined };
    const onChange = vi.fn();
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
    render(
      <QueryClientProvider client={queryClient}>
        <VideoEditorRuntimeProvider value={runtime(env.provider)}>
          <TimelineStoreProvider store={store}>
            <MountedForm provider={env.provider} store={store} initial={env.current()} latest={latest} onChange={onChange} />
          </TimelineStoreProvider>
        </VideoEditorRuntimeProvider>
      </QueryClientProvider>,
    );
    await waitFor(() => expect(latest.current?.commands.clipParamsPort).toBeDefined());
    const input = await screen.findByLabelText('Amount');
    fireEvent.change(input, { target: { value: '1' } });
    await waitFor(() => expect(requests).toHaveLength(1));
    expect(requests[0].commands).toHaveLength(1);
    expect(requests[0].commands[0]).toMatchObject({ op: 'clip.set-params', select, args: { values: { amount: 1 }, clear: [], schema_source: pin } });
    expect(onChange).not.toHaveBeenCalled();
    expect(client.getProjectVerifiedDocument).toHaveBeenCalledTimes(1);
    expect(client.getProjectVerifiedDocumentObject).toHaveBeenCalledTimes(1);
    expect(client.getProjectVerifiedDocument).toHaveBeenCalledWith(scope.projectId, pin);
    expect(client.getProjectVerifiedDocumentObject).toHaveBeenCalledWith(scope.projectId, pin, object.object_id);
    const [outbox] = await env.outboxes.list(scope);
    expect(outbox.intents).toHaveLength(0);
    expect(requests.flatMap((request) => request.commands).every((command) => command.op === 'clip.set-params')).toBe(true);
  });

  it('refuses a mounted edit whose retained read completes after the command session is gone', async () => {
    const env = await environment(selectedDocument());
    vi.stubGlobal('indexedDB', env.factory);
    vi.stubGlobal('navigator', { locks: { request: async (_key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => work({ name: 'test' }) } });
    const basis = historyBasis(env.initial.canonicalDocument);
    vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockResolvedValue(basis);
    const verified = {
      pin,
      document: {
        kind: 'astrid.project-pack', project_id: scope.projectId, document_id: pin.document_id, version: pin.version,
        content: {
          schema: 'astrid.project-pack/v1', source_binding_key: 'project-packs', pack_id: descriptor.packId,
          relative_manifest: `${scope.realmId}/${scope.projectId}/packs/${descriptor.packId}/pack.yaml`,
          admissions: [{ id: descriptor.id, kind: descriptor.kind, revision: descriptor.revision, snapshot_object: object }],
        },
      },
    };
    let release!: (value: typeof verified) => void;
    const client = env.provider.paramReadClient!;
    vi.spyOn(client, 'getProjectVerifiedDocument').mockImplementation(() => new Promise((resolve) => { release = resolve; }));
    vi.spyOn(client, 'getProjectVerifiedDocumentObject').mockResolvedValue({ ...object, bytes_base64: 'e30=' });
    const commit = vi.spyOn(env.provider, 'commitTimeline');
    const store = createTimelineStore();
    store.getState().setMounted(true);
    const latest: React.MutableRefObject<ReturnType<typeof useTimelineSave> | undefined> = { current: undefined };
    const onChange = vi.fn();
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
    const view = render(
      <QueryClientProvider client={queryClient}>
        <VideoEditorRuntimeProvider value={runtime(env.provider)}>
          <TimelineStoreProvider store={store}>
            <MountedForm provider={env.provider} store={store} initial={env.current()} latest={latest} onChange={onChange} />
          </TimelineStoreProvider>
        </VideoEditorRuntimeProvider>
      </QueryClientProvider>,
    );
    await waitFor(() => expect(latest.current?.commands.clipParamsPort).toBeDefined());
    fireEvent.change(await screen.findByLabelText('Amount'), { target: { value: '2' } });
    await waitFor(() => expect(client.getProjectVerifiedDocument).toHaveBeenCalledTimes(1));
    view.unmount();
    await act(async () => { release(verified); await Promise.resolve(); });
    expect(onChange).not.toHaveBeenCalled();
    expect(commit).not.toHaveBeenCalled();
  });
});
