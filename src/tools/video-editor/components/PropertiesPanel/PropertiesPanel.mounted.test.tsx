// @vitest-environment jsdom
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { AgentChatProvider, useAgentChatBridge, useAgentChatRegistry } from '@/shared/contexts/AgentChatContext';
import { systemResetSelectionForProjectChange } from '@/shared/state/selectionStore';
import { toast } from '@/shared/components/ui/runtime/sonner';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture';
import { ApiError } from '@/integrations/runtime/generated';
import { VideoEditorProvider } from '../../contexts/VideoEditorProvider';
import { useVideoEditorRuntime } from '../../contexts/VideoEditorRuntimeContext';
import { useTimelineEditorData, useTimelineEditorOps } from '../../hooks/timelineStore';
import { createDefaultTimelineConfig } from '../../lib/defaults';
import { buildTimelineData } from '../../lib/timeline-data';
import { createCommitOutbox } from '../../commands/commitOutbox';
import { INSTALLED_ASTRID_ELEMENT_HOST } from '../../runtime/astrid-element-components';
import type { DataProvider } from '../../data/DataProvider';
import { PropertiesPanel } from './PropertiesPanel';

vi.mock('../../hooks/useEffects.ts', () => ({ useEffects: () => ({ data: [] }) }));
vi.mock('../../hooks/useFinalVideoAvailable.ts', () => ({ useFinalVideoAvailable: () => ({ finalVideoMap: new Map() }) }));
vi.mock('../../compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));
vi.mock('@/integrations/runtime/generated-contract-metadata.ts', async original => ({
  ...await original<typeof import('@/integrations/runtime/generated-contract-metadata.ts')>(),
  SCHEMA_DIGEST: 'sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c',
}));

const scope = { projectId: 'project-commit', timelineId: 'timeline-commit', actorId: 'actor', realmId: 'realm' };
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
  vi.unstubAllGlobals();
  if (locksDescriptor) Object.defineProperty(navigator, 'locks', locksDescriptor);
  else Reflect.deleteProperty(navigator, 'locks');
});

it.each(['valid', 'dependent', 'conflict', 'missing', 'copied', 'forged', 'wrong editor', 'stale', 'closed'] as const)(
  'actual property form preserves mounted save ownership: %s', async control => {
    const descriptor = INSTALLED_ASTRID_ELEMENT_HOST.descriptors.find(entry => entry.id === 'text-card' && entry.packId === 'rendering')!;
    const elementRef = { id: descriptor.id, kind: descriptor.kind, packId: descriptor.packId, revision: descriptor.revision };
    const config = { ...createDefaultTimelineConfig(), clips: [
      { id: 'authored', track: 'V1', at: 0, hold: 2, clipType: 'hold', elementRef,
        params: { content: 'Before', future: { keep: [null, false] } } },
      { id: 'sibling', track: 'V1', at: 2, hold: 2, opaque: { keep: null } },
    ] };
    const registry = { assets: {} };
    const document = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' }, { revision_id: 'r0', publication_id: 'p0' },
      { children: true }).data.canonical_document;
    document.parent_revision.payload = { ...document.parent_revision.payload, config, clips: structuredClone(config.clips), registry, opaque: { keep: null } };
    document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
    const head = { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: 'r0', headPublicationId: 'p0' };
    const data = await buildTimelineData(config, registry, async file => file, 1, undefined, head);
    const basis = { head: { revisionId: 'r0', publicationId: 'p0' }, canonicalDocument: document };
    // Hold the ACK so the persisted pending request can be inspected directly.
    let acknowledge!: () => void;
    const response = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' }, { revision_id: 'r0', publication_id: 'p0' });
    const canonical = structuredClone(document);
    canonical.parent_revision.revision_id = 'r1';
    const nextConfig = { ...config, clips: config.clips.map(clip => clip.id === 'authored'
      ? { ...clip, params: { ...clip.params, content: 'After' } } : clip) };
    canonical.parent_revision.payload = { ...canonical.parent_revision.payload, config: nextConfig, clips: structuredClone(nextConfig.clips) };
    canonical.parent_revision.content_digest = fixtureDigest(canonical.parent_revision.payload);
    response.data.canonical_document = canonical;
    const send = vi.fn<NonNullable<DataProvider['commitTimeline']>>(() => new Promise(resolve => {
      acknowledge = () => resolve({ response, accepted: { revisionId: 'r1', publicationId: 'p1' }, canonicalDocument: canonical, graph: {}, receipt: response.receipt });
    }));
    if (control === 'conflict') send.mockRejectedValueOnce(new ApiError(409, 'conflict', 'Property changed', '', {
      status: 'conflict', reason: 'field_changed', head: basis.head,
    }));
    const finalDocument = structuredClone(canonical);
    finalDocument.parent_revision.revision_id = 'r2';
    const finalConfig = { ...nextConfig, clips: nextConfig.clips.map(clip => clip.id === 'authored'
      ? { ...clip, params: { ...clip.params, content: 'Final' } } : clip) };
    finalDocument.parent_revision.payload = { ...finalDocument.parent_revision.payload, config: finalConfig, clips: structuredClone(finalConfig.clips) };
    finalDocument.parent_revision.content_digest = fixtureDigest(finalDocument.parent_revision.payload);
    const legacy = vi.fn(async () => { throw new Error('Legacy writer'); });
    const provider: DataProvider = {
      persistenceEnabled: true, loadTimeline: vi.fn(async () => ({ config, configVersion: 1, head })),
      loadAssetRegistry: vi.fn(async () => registry), resolveAssetUrl: vi.fn(async file => file), saveTimeline: legacy,
      loadTimelineCommandBasis: vi.fn(async () => basis), commitTimeline: send,
      getRecoverableIdentity: vi.fn(async () => ({ actorId: scope.actorId, realmId: scope.realmId })),
    };
    let editor!: ReturnType<typeof useTimelineEditorData>;
    let ops!: ReturnType<typeof useTimelineEditorOps>;
    let chat!: ReturnType<typeof useAgentChatBridge>;
    let registrations!: ReturnType<typeof useAgentChatRegistry>;
    let otherOps!: ReturnType<typeof useTimelineEditorOps>;
    let otherRuntime!: ReturnType<typeof useVideoEditorRuntime>;
    function Capture() {
      editor = useTimelineEditorData(); ops = useTimelineEditorOps();
      chat = useAgentChatBridge(); registrations = useAgentChatRegistry();
      return <PropertiesPanel />;
    }
    function OtherEditor() {
      otherOps = useTimelineEditorOps(); otherRuntime = useVideoEditorRuntime();
      return null;
    }
    const otherProvider = { ...provider, persistenceEnabled: false, loadTimelineCommandBasis: undefined,
      commitTimeline: undefined, getRecoverableIdentity: undefined };
    const errors = vi.spyOn(toast, 'error');
    const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
    const view = render(<MemoryRouter><QueryClientProvider client={client}><AgentChatProvider>
      <VideoEditorProvider dataProvider={provider} projectId={scope.projectId} projectSlug={scope.projectId}
        timelineId={scope.timelineId} userId={null} initialTimelineData={data}><Capture /></VideoEditorProvider>
      {control === 'wrong editor' && <VideoEditorProvider dataProvider={otherProvider} projectId={scope.projectId}
        projectSlug={scope.projectId} timelineId={scope.timelineId} userId={null} initialTimelineData={data}><OtherEditor /></VideoEditorProvider>}
    </AgentChatProvider></QueryClientProvider></MemoryRouter>);
    try {
      await waitFor(() => expect(chat.editorContext?.elementOperationAdapter).toBeDefined());
      await act(async () => { ops.selectClip('authored'); });
      await waitFor(() => expect(chat.editorContext?.elementContext?.selectedClips[0]?.id).toBe('authored'));
      await waitFor(async () => expect(await createCommitOutbox().list(scope)).toHaveLength(1));
      const owner = chat.editorContext!;
      expect(editor.data?.head).toEqual(head);
      expect(owner.timelineSummary?.configVersion).toBe(editor.data?.configVersion);
      expect(owner.elementContext?.selectedClips[0]).toMatchObject({ id: 'authored', trackId: 'V1', scope: 'parent-timeline',
        elementRef, params: config.clips[0].params });
      if (control !== 'valid' && control !== 'dependent' && control !== 'conflict' && control !== 'closed') {
        let source = owner;
        if (control === 'missing') source = { ...owner, elementOperationAdapter: undefined, elementContext: undefined };
        if (control === 'copied') source = { ...owner, elementContext: structuredClone(owner.elementContext) };
        if (control === 'forged') source = { ...owner, elementContext: structuredClone(owner.elementContext), elementOperationAdapter: undefined };
        if (control === 'wrong editor') {
          await act(async () => { otherOps.selectClip('authored'); registrations.activate(otherRuntime.agentSelectionOwner); });
          await waitFor(() => expect(chat.editorContext?.elementContext?.selectedClips[0]?.id).toBe('authored'));
          expect(chat.editorContext?.elementOperationAdapter).not.toBe(owner.elementOperationAdapter);
          expect(chat.editorContext?.elementContext).toEqual(owner.elementContext);
        }
        if (control === 'stale') {
          await act(async () => { ops.selectClip('sibling'); });
          await act(async () => { ops.selectClip('authored'); });
          await waitFor(() => expect(chat.editorContext?.elementContext).not.toBe(owner.elementContext));
        }
        if (control !== 'wrong editor') act(() => { registrations.register({ timelineId: scope.timelineId, editorContext: source }, 'attack'); registrations.activate('attack'); });
      }
      fireEvent.change(screen.getByLabelText('Content'), { target: { value: 'After' } });
      if (control === 'closed') view.unmount();
      if (control === 'conflict') {
        await waitFor(() => expect(send).toHaveBeenCalledOnce());
        await waitFor(() => expect(errors).toHaveBeenCalled());
        expect(editor.data?.config.clips[0].params?.content).toBe('Before');
        const [retained] = await createCommitOutbox().list(scope);
        expect(retained.intents).toHaveLength(1);
        expect(legacy).not.toHaveBeenCalled();
        return;
      }
      if (control === 'valid' || control === 'dependent') {
        await waitFor(() => { expect(errors.mock.calls).toEqual([]); expect(send).toHaveBeenCalledOnce(); });
        const [stored] = await createCommitOutbox().list(scope);
        expect(stored.intents).toHaveLength(1);
        expect(stored.pending?.request.key).toBe(send.mock.calls[0][1]);
        expect(send.mock.calls[0][0]).toMatchObject({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
          base_revision_id: 'r0', base_publication_id: 'p0', merge: 'atomic', dry_run: false,
          commands: [{ op: 'doc.patch' }], steps: [{ command_ordinals: [0] }] });
        const request = send.mock.calls[0][0];
        expect(request.commands[0].args.changes).toEqual([
          { op: 'set', ref: 'parent', path: ['clips', 'id:authored', 'params', 'content'],
            before: { state: 'present', value: 'Before' }, value: 'After' },
        ]);
        expect(request.reads).toContainEqual({ kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:authored', 'params'],
          state: { state: 'present', value: config.clips[0].params } });
        expect(request.steps?.[0]).toMatchObject({ intent: 'timeline.update_element', tags: [], patch: request.commands[0].args.changes, reads: request.reads });
        expect(request.source).toEqual({ via: 'app' });
        if (control === 'dependent') {
          await waitFor(() => expect(chat.editorContext?.elementContext?.selectedClips[0]?.params?.content).toBe('After'));
          const finalResponse = acceptedCommit({ revision_id: 'r2', publication_id: 'p2' }, { revision_id: 'r1', publication_id: 'p1' });
          finalResponse.data.canonical_document = finalDocument;
          send.mockImplementationOnce(async () => ({ response: finalResponse, accepted: { revisionId: 'r2', publicationId: 'p2' },
            canonicalDocument: finalDocument, graph: {}, receipt: finalResponse.receipt }));
          fireEvent.change(screen.getByLabelText('Content'), { target: { value: 'Final' } });
          await waitFor(async () => expect((await createCommitOutbox().list(scope))[0].intents).toHaveLength(2));
          const [chained] = await createCommitOutbox().list(scope);
          expect(chained.intents[1].basis).toEqual({ after: chained.intents[0].id });
          expect(send).toHaveBeenCalledOnce();
        }
        await act(async () => { acknowledge(); });
        await waitFor(() => expect(editor.data?.head?.headRevisionId).toBe(control === 'dependent' ? 'r2' : 'r1'));
        expect(editor.data?.config.clips[0].params).toEqual({ content: control === 'dependent' ? 'Final' : 'After', future: { keep: [null, false] } });
        expect(editor.data?.config.clips[1]).toEqual(data.config.clips[1]);
        const [accepted] = await createCommitOutbox().list(scope);
        expect(accepted.accepted?.value).toMatchObject({ canonicalDocument: control === 'dependent' ? finalDocument : canonical });
        if (control === 'dependent') {
          expect(send.mock.calls[1][0]).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
            commands: [{ args: { changes: [{ op: 'set', ref: 'parent', path: ['clips', 'id:authored', 'params', 'content'],
              before: { state: 'present', value: 'After' }, value: 'Final' }] } }] });
        }
        expect(canonical.shot_revisions).toEqual(document.shot_revisions);
      } else {
        await waitFor(() => expect(errors).toHaveBeenCalledWith(control === 'missing'
          ? 'Element parameter ownership changed or is unavailable; reload the timeline before editing.'
          : control === 'closed'
            ? 'The captured editor was closed or replaced. Reopen the current timeline and recover the draft before applying it.'
            : 'Element parameter editor owner changed or is unavailable; draft retained'));
        expect(send).not.toHaveBeenCalled();
        const [stored] = await createCommitOutbox().list(scope);
        expect(stored.intents).toEqual([]);
        expect(stored.pending).toBeUndefined();
        expect(editor.data?.config.clips[0].params?.content).toBe('Before');
      }
      expect(legacy).not.toHaveBeenCalled();
    } finally {
      if (acknowledge) await act(async () => { acknowledge(); });
      view.unmount(); client.clear();
    }
  });
