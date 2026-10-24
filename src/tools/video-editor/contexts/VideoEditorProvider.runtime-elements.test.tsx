// @vitest-environment jsdom
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { AgentChatProvider, useAgentChatBridge } from '@/shared/contexts/AgentChatContext';
import { systemResetSelectionForProjectChange } from '@/shared/state/selectionStore';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata';
import { RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture';
import type { CommitRequest } from '@/integrations/runtime/generated';
import { createDefaultTimelineConfig } from '../lib/defaults';
import { createCommitOutbox } from '../commands/commitOutbox';
import { useTimelineEditorData, useTimelineEditorOps } from '../hooks/timelineStore';
import { ElementsLibraryPanel } from '../components/ElementsLibraryPanel';
import VideoEditorPage from '../pages/VideoEditorPage';

// Keep the routed page, provider, queries, save hook, session and adapter real.
// Only unrelated page chrome and the rendering surface are replaced.
vi.mock('@/shared/hooks/useHomeNavigation', () => ({ useHomeNavigation: () => ({ targetPath: '/tools/video-editor' }) }));
vi.mock('@/shared/components/AppHeader', () => ({ AppHeader: () => null }));
vi.mock('@/shared/components/ProjectHeaderActions', () => ({ ProjectHeaderActions: () => null }));
vi.mock('@/shared/components/ProjectTimelineSelectors', () => ({ ProjectTimelinePicker: () => null }));
vi.mock('../tour/runner/useEditorTourHost', () => ({ useEditorTourHost: () => {} }));
vi.mock('../dev/localExtensions', () => ({ devLocalExtensions: [] }));
vi.mock('../hooks/useEffects', () => ({ useEffects: () => ({ data: [] }) }));
vi.mock('../hooks/useFinalVideoAvailable', () => ({ useFinalVideoAvailable: () => ({ finalVideoMap: new Map() }) }));
vi.mock('../compositions/TimelineRenderer', () => ({ invalidateReferencedTimelineCache: vi.fn() }));
vi.mock('../components/AstridVideoEditorShell', () => ({ AstridVideoEditorShell: () => <ElementSurface /> }));

function ElementSurface() {
  const data = useTimelineEditorData();
  const ops = useTimelineEditorOps();
  const { editorContext } = useAgentChatBridge();
  return <>
    <button onClick={() => ops.selectClip('parent')}>Select parent</button>
    <span data-testid="loaded-clips">{data.resolvedConfig?.clips.length}</span>
    <span data-testid="adapter-ready">{String(Boolean(editorContext?.elementOperationAdapter))}</span>
    <ElementsLibraryPanel open onOpenChange={() => {}} onOpenCreationPrompt={() => {}} />
  </>;
}

function deferred() {
  let resolve!: () => void;
  const promise = new Promise<void>(done => { resolve = done; });
  return { promise, resolve };
}

const projectId = 'project-runtime-elements';
const timelineId = 'timeline-runtime-elements';
const scope = `/v1/projects/${projectId}/timelines/${timelineId}`;
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
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  if (locksDescriptor) Object.defineProperty(navigator, 'locks', locksDescriptor);
  else Reflect.deleteProperty(navigator, 'locks');
});

async function mountRuntimePage(hold: 'history' | 'commit' | 'refresh') {
  const history = deferred();
  const acknowledgement = deferred();
  const refresh = deferred();
  const config = { ...createDefaultTimelineConfig(),
    tracks: [{ id: 'V1', kind: 'visual' as const, label: 'Picture' }],
    clips: [{ id: 'parent', track: 'V1', at: 0, hold: 2, text: { content: 'Keep me' } }],
  };
  const initial = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
    { revision_id: 'r0', publication_id: 'p0' }, { projectId, timelineId }).data.canonical_document;
  initial.parent_revision.payload = { config, clips: config.clips, registry: { assets: {} }, occurrences: [] };
  initial.parent_revision.content_digest = fixtureDigest(initial.parent_revision.payload);
  let document = structuredClone(initial);
  let publicationId = 'p0';
  const calls: string[] = [];
  const commits: Array<{ request: CommitRequest; key: string }> = [];
  const unexpected: string[] = [];
  const json = (value: unknown) => new Response(JSON.stringify(value), { status: 200 });
  vi.stubGlobal('fetch', vi.fn<typeof fetch>(async (input, init) => {
    const url = new URL(String(input), window.location.origin);
    const path = url.pathname.replace(/^\/api\/(runtime|astrid)/, '');
    calls.push(`${init?.method ?? 'GET'} ${path}${url.search}`);
    if (path === '/runtime-config/v1/workspace.json') return new Response(null, { status: 404 });
    if (path === '/v1/health') return json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      runtime_epoch: 1, runtime_session_id: 'session', runtime_instance_id: 'instance-runtime-elements' });
    if (path === '/v1/handshake') return json({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      session_id: 'session', actor_id: 'actor', realm_id: 'realm', scopes: RUNTIME_CLIENT_SCOPES,
      capabilities: ['execution_binding.targeted.v1'] });
    if (path === '/v1/realm') return json({ realm_id: 'realm', display_name: 'Elements fixture', version: 1,
      created_at: '2026-10-24T00:00:00Z' });
    const project = { project_id: projectId, slug: 'element-project', name: 'Element project', metadata: {} };
    const timeline = { project_id: projectId, timeline_id: timelineId, name: 'Main timeline', slug: 'main',
      head_revision_id: document.parent_revision.revision_id, head_publication_id: publicationId };
    if (path === '/v1/projects') return json({ items: [project], next_cursor: null });
    if (path === `/v1/projects/${projectId}`) return json(project);
    if (path === `/v1/projects/${projectId}/timelines`) return json({ items: [timeline], next_cursor: null });
    if (path === scope) return json(timeline);
    if (path === `${scope}/inspect`) {
      if (commits.length && hold === 'refresh') await refresh.promise;
      return json({ project_id: projectId, timeline_id: timelineId, representation: 'canonical_head',
        authority: 'runtime_parent_composition', is_current_head: true,
        revision_id: document.parent_revision.revision_id, head_revision_id: document.parent_revision.revision_id });
    }
    if (path === `${scope}/commits`) {
      if (hold === 'history') await history.promise;
      return json({ items: [], next_cursor: null, head: { revision_id: document.parent_revision.revision_id, publication_id: publicationId } });
    }
    if (path === `${scope}/composition-revisions`) return json({ items: [], next_cursor: null });
    if (path === `${scope}/composition-revisions/${document.parent_revision.revision_id}`) return json({
      project_id: projectId, timeline_id: timelineId, ...document.parent_revision, dependency_manifest: document.dependency_manifest,
    });
    if (path.startsWith(`/v1/projects/${projectId}/documents`)) return json({ items: [], next_cursor: null });
    if (path === `${scope}/commit` && init?.method === 'POST') {
      const request = JSON.parse(new TextDecoder().decode(init.body as Uint8Array)) as CommitRequest;
      const key = new Headers(init.headers).get('Idempotency-Key')!;
      commits.push({ request, key });
      if (hold === 'commit') await acknowledgement.promise;
      const overlay = request.commands[0].args.changes as Array<{ value: unknown }>;
      const next = structuredClone(initial);
      next.parent_revision.payload.config.clips.push(overlay[0].value);
      next.parent_revision.payload.clips = structuredClone(next.parent_revision.payload.config.clips);
      next.parent_revision.revision_id = 'r1';
      next.parent_revision.content_digest = fixtureDigest(next.parent_revision.payload);
      const response = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' },
        { revision_id: 'r0', publication_id: 'p0' }, { projectId, timelineId, commands: request.commands });
      Object.assign(response.data, { canonical_document: next, document_digest: fixtureDigest(next),
        merge_mode: request.merge, steps: request.steps, label: request.label, source: request.source });
      response.receipt.idempotency_key = key;
      response.receipt.result = response.data;
      document = next;
      publicationId = 'p1';
      return json(response);
    }
    unexpected.push(`${init?.method ?? 'GET'} ${path}${url.search}`);
    throw new Error(`Unexpected page read: ${unexpected.at(-1)}`);
  }));
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const view = render(<MemoryRouter initialEntries={[`/tools/video-editor?project=${projectId}&timeline=${timelineId}`]}>
    <QueryClientProvider client={client}><AgentChatProvider><VideoEditorPage /></AgentChatProvider></QueryClientProvider>
  </MemoryRouter>);
  await waitFor(() => expect(screen.getByTestId('loaded-clips').textContent).toBe('1'));
  await waitFor(() => expect(screen.getByTestId('adapter-ready').textContent).toBe('true'));
  fireEvent.click(screen.getByRole('button', { name: 'Select parent', hidden: true }));
  fireEvent.change(screen.getByPlaceholderText('Search elements'), { target: { value: 'am-burst' } });
  expect(screen.getByText('AM Burst', { exact: true })).toBeDefined();
  return { view, client, calls, commits, unexpected, history, acknowledgement, refresh };
}

describe('routed element save with the class Runtime provider', () => {
  it.each(['history', 'commit', 'refresh'] as const)('settles the catalog gesture after the pending %s response resolves', async hold => {
    const mounted = await mountRuntimePage(hold);
    try {
      fireEvent.click(screen.getByRole('button', { name: 'Apply', exact: true }));
      await waitFor(() => expect(mounted.calls.some(call => call.includes(`${scope}/commits?`))).toBe(true));
      if (hold !== 'history') {
        await waitFor(() => expect(mounted.commits).toHaveLength(1));
        if (hold === 'refresh') await waitFor(() => expect(screen.getByTestId('loaded-clips').textContent).toBe('2'));
      } else expect(mounted.commits).toHaveLength(0);
      expect(screen.getByRole('button', { name: 'Applying…' })).toHaveProperty('disabled', true);
      expect(screen.queryByRole('status')).toBeNull();
      const outboxes = createCommitOutbox({ indexedDB, exclusiveLock: async (_key, work) => work() });
      if (hold === 'commit') {
        const [pending] = await outboxes.list({ realmId: 'realm', actorId: 'actor', projectId, timelineId });
        expect(pending.pending?.request.key).toBe(mounted.commits[0].key);
        expect(pending.pending?.request.body).toBe(JSON.stringify(mounted.commits[0].request));
        expect(pending.intents[0].basis).toEqual({ head: { revisionId: 'r0', publicationId: 'p0' } });
        expect(pending.accepted).toBeUndefined();
      }
      await act(async () => { mounted.history.resolve(); mounted.acknowledgement.resolve(); mounted.refresh.resolve(); });
      await waitFor(() => expect(screen.getByRole('status').textContent).toContain('applied'));
      expect(mounted.commits).toHaveLength(1);
      const [{ request, key }] = mounted.commits;
      expect(request).toMatchObject({ api_version: 1, project_id: projectId, timeline_id: timelineId,
        base_revision_id: 'r0', base_publication_id: 'p0', merge: 'atomic', dry_run: false,
        source: { via: 'app' }, commands: [{ op: 'doc.patch' }],
        steps: [{ command_ordinals: [0], intent: 'timeline.apply_element' }], reads: expect.any(Array) });
      expect(request.steps![0].patch).toEqual(request.commands[0].args.changes);
      expect(key).toEqual(expect.any(String));
      const [stored] = await outboxes.list({ realmId: 'realm', actorId: 'actor', projectId, timelineId });
      expect(stored.intents).toHaveLength(0);
      expect(stored.accepted?.head).toEqual({ revisionId: 'r1', publicationId: 'p1' });
      expect(mounted.unexpected).toEqual([]);
    } finally {
      mounted.history.resolve(); mounted.acknowledgement.resolve(); mounted.refresh.resolve();
      mounted.view.unmount(); mounted.client.clear();
    }
  });
});
