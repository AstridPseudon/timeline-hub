// @vitest-environment jsdom
import { act, render, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { AgentChatProvider } from '@/shared/contexts/AgentChatContext';
import { toast } from '@/shared/components/ui/runtime/sonner';
import { systemResetSelectionForProjectChange } from '@/shared/state/selectionStore';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture';
import type { MediaSelection } from '@/integrations/runtime/timeline-commit-types';
import type { DataProvider, TimelineCommandBasis } from '../data/DataProvider';
import type { AssetRegistry, TimelineClip, TimelineConfig } from '../types';
import { createDefaultTimelineConfig } from '../lib/defaults';
import { buildTimelineData } from '../lib/timeline-data';
import { MEDIA_COMMAND_DESCRIPTORS, PLACE_PREPARED_MEDIA_COMMAND_DESCRIPTOR } from '../commands/media';
import { useTimelineChromeContext, useTimelineEditorData } from '../hooks/timelineStore';
import { VideoEditorProvider } from './VideoEditorProvider';
import { ADD_GENERATION_QUERY_PARAM, readPendingAdds, writePendingAdds } from '@/domains/media-lightbox/hooks/addToVideoEditorConstants';

vi.mock('../hooks/useEffects.ts', () => ({ useEffects: () => ({ data: [] }) }));
vi.mock('../hooks/useFinalVideoAvailable.ts', () => ({ useFinalVideoAvailable: () => ({ finalVideoMap: new Map() }) }));
vi.mock('../compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));

const projectId = 'project-staging';
const timelineId = 'timeline-staging';
const locksDescriptor = Object.getOwnPropertyDescriptor(navigator, 'locks');
beforeEach(() => {
  vi.stubGlobal('indexedDB', createFakeIndexedDB());
  localStorage.clear();
  systemResetSelectionForProjectChange();
  Object.defineProperty(navigator, 'locks', { configurable: true, value: {
    request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}),
  } });
});
afterEach(() => {
  vi.restoreAllMocks();
  if (locksDescriptor) Object.defineProperty(navigator, 'locks', locksDescriptor);
  else Reflect.deleteProperty(navigator, 'locks');
});

async function mountStaged(ids: string[], selectionRead?: (selection: MediaSelection) => Promise<MediaSelection>, stage = true) {
  const config = { ...createDefaultTimelineConfig(),
    tracks: [{ id: 'V1', kind: 'visual' as const, label: 'Picture' }],
    clips: [{ id: 'existing', track: 'V1', at: 0, hold: 2, text: { content: 'Keep me' } }],
  };
  const base = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
    { revision_id: 'r0', publication_id: 'p0' }, { projectId, timelineId }).data.canonical_document;
  base.parent_revision.payload = { config, clips: config.clips, registry: { assets: {} }, occurrences: [] };
  base.parent_revision.content_digest = fixtureDigest(base.parent_revision.payload);
  let basis: TimelineCommandBasis = { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: base };
  const initialData = await buildTimelineData(config, { assets: {} }, async file => file, 1, undefined,
    { projectId, timelineId, headRevisionId: 'r0', headPublicationId: 'p0' });
  let editor!: ReturnType<typeof useTimelineEditorData>;
  let chrome!: ReturnType<typeof useTimelineChromeContext>;
  let location!: ReturnType<typeof useLocation>;
  function Consumer() {
    editor = useTimelineEditorData();
    chrome = useTimelineChromeContext();
    location = useLocation();
    return <span>{editor.resolvedConfig?.clips.length}</span>;
  }
  const selections = new Map<string, MediaSelection>();
  const calls: string[] = [];
  let release!: () => void;
  const ready = new Promise<void>(resolve => { release = resolve; });
  const runtime = new RuntimeDataProvider({ projectId, baseUrl: 'http://runtime.test', token: 'fixture-token',
    transport: async (_method, path) => {
      calls.push(path);
      const json = (value: unknown) => ({ status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(value)) });
      if (path === '/v1/health') return json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
        runtime_epoch: 1, runtime_session_id: 'session', runtime_instance_id: 'instance-staging' });
      if (path === '/v1/handshake') return json({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
        session_id: 'session', actor_id: 'actor', realm_id: 'realm',
        scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'],
        capabilities: ['execution_binding.targeted.v1'] });
      if (path === '/v1/realm') return json({ realm_id: 'realm', display_name: 'Staging fixture', version: 1,
        created_at: '2026-10-24T00:00:00Z' });
      const generationId = ids.find(id => path === `/v1/generations/${id}` || path.startsWith(`/v1/generations/${id}/variants?`));
      if (generationId) {
        await ready;
        if (path.endsWith(`/generations/${generationId}`)) return json({ generation_id: generationId, project_id: projectId,
          type: 'image', status: 'completed', metadata: { name: `Name ${generationId}`, prompt: 'Preserve prompt' },
          version: 1, created_at: '2026-10-24T00:00:00Z', updated_at: '2026-10-24T00:00:00Z' });
        return json({ items: [{ variant_id: `variant-${generationId}`, generation_id: generationId,
          object_id: `sha256:${'a'.repeat(64)}`, variant_type: 'original', metadata: { is_primary: true, media_type: 'image/png' },
          created_at: '2026-10-24T00:00:00Z' }], next_cursor: null });
      }
      if (path.startsWith(`/v1/projects/${projectId}/media-selection?`)) {
        const query = new URLSearchParams(path.split('?')[1]);
        const selection = { asset: query.get('asset')!, generation_id: query.get('generation_id')!, variant_id: query.get('variant_id')!,
          object_id: `sha256:${'a'.repeat(64)}`, catalog_digest: `sha256:${'b'.repeat(64)}` };
        selections.set(selection.generation_id, selection);
        return json(selectionRead ? await selectionRead(selection) : selection);
      }
      throw new Error(`Unexpected Runtime read: ${path}`);
    },
  });
  const preparedAssets: AssetRegistry['assets'] = {};
  const commit = vi.fn<NonNullable<DataProvider['commitTimeline']>>(async (request, key) => {
    const revision = `r${commit.mock.calls.length}`;
    const response = acceptedCommit({ revision_id: revision, publication_id: `p-${revision}` },
      { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, { projectId, timelineId, commands: request.commands });
    const document = structuredClone(basis.canonicalDocument);
    const current = editor.dataRef.current!;
    Object.assign(preparedAssets, structuredClone(current.registry.assets));
    const payload = document.parent_revision.payload;
    const nextConfig = payload.config as unknown as TimelineConfig;
    const registry = payload.registry as unknown as AssetRegistry;
    for (const command of request.commands) {
      expect(command.op).toBe('clip.add-media');
      nextConfig.clips.push(structuredClone(command.args.row) as unknown as TimelineClip);
      const asset = (command.args.media as unknown as MediaSelection).asset;
      registry.assets[asset] = structuredClone(preparedAssets[asset]);
    }
    payload.clips = structuredClone(nextConfig.clips);
    document.parent_revision.revision_id = revision;
    document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
    response.data.canonical_document = document;
    response.data.document_digest = fixtureDigest(document);
    Object.assign(response.data, { status: 'accepted', merge_mode: request.merge, steps: request.steps, label: request.label, source: request.source });
    response.receipt.idempotency_key = key;
    response.receipt.result = response.data;
    basis = { head: { revisionId: revision, publicationId: `p-${revision}` }, canonicalDocument: document };
    return { response, accepted: basis.head, canonicalDocument: document, graph: {}, receipt: response.receipt };
  });
  const provider: DataProvider & Pick<RuntimeDataProvider, 'getProjectMediaSelection'> = {
    loadTimeline: vi.fn(async () => ({ config, configVersion: 1, head: initialData.head })),
    loadAssetRegistry: vi.fn(async () => ({ assets: {} })), resolveAssetUrl: async file => file,
    saveTimeline: vi.fn(), loadTimelineCommandBasis: vi.fn(async () => structuredClone(basis)),
    getRecoverableIdentity: async () => ({ realmId: 'realm', actorId: 'actor' }), commitTimeline: commit,
    loadGenerationForLightbox: runtime.loadGenerationForLightbox.bind(runtime),
    getProjectMediaSelection: runtime.getProjectMediaSelection.bind(runtime),
  };
  if (stage) writePendingAdds(ids);
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const view = render(<MemoryRouter initialEntries={[`/?timeline=${timelineId}&${ADD_GENERATION_QUERY_PARAM}=${ids[0]}`]}>
    <QueryClientProvider client={client}><AgentChatProvider>
      <VideoEditorProvider dataProvider={provider} projectId={projectId} timelineId={timelineId} userId={null} initialTimelineData={initialData}>
        <Consumer />
      </VideoEditorProvider>
    </AgentChatProvider></QueryClientProvider>
  </MemoryRouter>);
  return { view, commit, provider, calls, selections, release, getEditor: () => editor, getChrome: () => chrome, getLocation: () => location };
}

describe('mounted provider staged generation persistence', () => {
  it('drains URL and staged images once, in timeline order, through prepared media and the v2 outbox', async () => {
    const descriptors = [...MEDIA_COMMAND_DESCRIPTORS, PLACE_PREPARED_MEDIA_COMMAND_DESCRIPTOR];
    const executions = descriptors.flatMap(descriptor => [vi.spyOn(descriptor, 'apply'), vi.spyOn(descriptor, 'dryRun')]);
    const mounted = await mountStaged(['first', 'second']);
    try {
      await act(async () => { mounted.release(); });
      await waitFor(() => expect(readPendingAdds()).toEqual([]));
      const clips = mounted.getEditor().dataRef.current!.config.clips;
      expect(clips).toEqual([
        expect.objectContaining({ id: 'existing', at: 0, hold: 2, text: { content: 'Keep me' } }),
        expect.objectContaining({ asset: 'variant-first', at: 2, hold: 5, track: 'V1' }),
        expect.objectContaining({ asset: 'variant-second', at: 7, hold: 5, track: 'V1' }),
      ]);
      expect(mounted.getEditor().selectedClipId).toBe(clips[2].id);
      expect(mounted.getEditor().selectedTrackId).toBe('V1');
      expect(mounted.getEditor().dataRef.current!.registry.assets['variant-first']).toMatchObject({
        generationId: 'first', variantId: 'variant-first', name: 'Name first', prompt: 'Preserve prompt', type: 'image/png',
      });
      await act(async () => { await mounted.getChrome().flushPendingSave(); });
      expect(mounted.commit).toHaveBeenCalled();
      const requests = mounted.commit.mock.calls.map(([request]) => request);
      expect(requests.flatMap(request => request.commands).map(command => command.op)).toEqual(['clip.add-media', 'clip.add-media']);
      expect(requests.flatMap(request => request.commands).map(command => command.args.media)).toEqual([
        mounted.selections.get('first'), mounted.selections.get('second'),
      ]);
      for (const [request, key] of mounted.commit.mock.calls) {
        expect(request).toMatchObject({ api_version: 1, project_id: projectId, timeline_id: timelineId,
          base_revision_id: expect.any(String), base_publication_id: expect.any(String), merge: 'fields', dry_run: false, source: { via: 'app' } });
        expect(request.commands.every(command => JSON.stringify(command.intent) === '{}')).toBe(true);
        expect(key).toEqual(expect.any(String));
      }
      expect(mounted.provider.saveTimeline).not.toHaveBeenCalled();
      expect(mounted.calls.filter(path => path === '/v1/generations/first')).toHaveLength(1);
      expect(mounted.calls.filter(path => path === '/v1/generations/second')).toHaveLength(1);
      expect(new URLSearchParams(mounted.getLocation().search).has(ADD_GENERATION_QUERY_PARAM)).toBe(false);
      executions.forEach(execution => expect(execution).not.toHaveBeenCalled());
      expect(mounted.getEditor().dataRef.current?.config.clips).toEqual(clips);
    } finally { mounted.view.unmount(); }
  });

  it.each(['asset', 'generation_id', 'variant_id', 'object_id'] as const)('refuses a mismatched Runtime %s before placement', async field => {
    const notice = vi.spyOn(toast, 'error');
    const mounted = await mountStaged(['first'], async selection => ({ ...selection, [field]: 'mismatched' }));
    try {
      await act(async () => { mounted.release(); });
      await waitFor(() => expect(readPendingAdds()).toEqual([]));
      expect(mounted.getEditor().dataRef.current?.config.clips).toHaveLength(1);
      expect(mounted.getEditor().dataRef.current?.registry.assets).toEqual({});
      expect(mounted.commit).not.toHaveBeenCalled();
      expect(notice).toHaveBeenCalledWith('Runtime media selection does not match the loaded generation. Import the media again.');
    } finally { mounted.view.unmount(); }
  });

  it('retains a staged item when the provider unmounts during selection so another mount can retry', async () => {
    let resolveSelection!: (selection: MediaSelection) => void;
    let captured!: MediaSelection;
    const mounted = await mountStaged(['first'], selection => {
      captured = selection;
      return new Promise(resolve => { resolveSelection = resolve; });
    });
    await act(async () => { mounted.release(); });
    await waitFor(() => expect(resolveSelection).toBeDefined());
    mounted.view.unmount();
    await act(async () => { resolveSelection(captured); });
    expect(readPendingAdds()).toEqual(['first']);
    expect(mounted.commit).not.toHaveBeenCalled();
    const retry = await mountStaged(['first'], undefined, false);
    try {
      await act(async () => { retry.release(); });
      await waitFor(() => expect(readPendingAdds()).toEqual([]));
      expect(retry.getEditor().dataRef.current?.config.clips).toHaveLength(2);
      await act(async () => { await retry.getChrome().flushPendingSave(); });
      expect(retry.commit).toHaveBeenCalledOnce();
    } finally { retry.view.unmount(); }
  });
});
