import { webcrypto } from 'node:crypto';
import React, { useEffect } from 'react';
import { act, renderHook, waitFor, cleanup } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { createFakeIndexedDB, resetFakeIndexedDB } from 'fake-indexeddb';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { elementReferenceCommand, elementReferenceInverse, isElementReferenceBatch, isElementReferenceInverse } from './elementReferenceHistory.ts';
import { AstridElementOperationAdapter } from '../runtime/element-adapter.ts';
import type { ReighAgentElementContext } from '../runtime/element-contract.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import type { CommitRequest, CommitResult, Transport } from '@/integrations/runtime/generated.ts';
import { RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from '@/integrations/runtime/contract-metadata.ts';
import { VideoEditorRuntimeProvider } from '../contexts/VideoEditorRuntimeContext.tsx';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { TimelineEventBus } from '../hooks/useTimelineEventBus.ts';
import { useTimelineCommit } from '../hooks/useTimelineCommit.ts';
import { useTimelinePersistence } from '../hooks/useTimelinePersistence.ts';
import { useTimelineHistory } from '../hooks/useTimelineHistory.ts';
import { createInteractionState } from '../lib/interaction-state.ts';
import type { TimelineConfig } from '../types/index.ts';

vi.mock('@/tools/video-editor/compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));
const sdk = process.env.W12_SDK_ROOT!;
const python = '/Users/peteromalley/.pyenv/versions/3.11.11/bin/python3.11';
const ref = { id: 'local-glow', kind: 'effect' as const, revision: 'source-r1' };
const context: ReighAgentElementContext = { catalog: [{ ...ref, label: 'Local Glow', placement: 'overlay',
  capabilities: { browserPreview: 'supported', astridExport: 'blocked', workerExport: 'blocked' }, publication: 'published' }],
  legacySequenceResources: [], selectedClips: [], transitionCandidates: [], operations: [] };
function source(payload: unknown): any {
  if (!sdk) throw new Error('W12_SDK_ROOT must bind the admitted SDK receiver');
  return JSON.parse(execFileSync(python, ['-B', `${sdk}/tests/sdk/test_timeline_element_reference.py`], {
    cwd: sdk, env: { ...process.env, PYTHONPATH: `${sdk}:${sdk}/tests/sdk`, PYTHONDONTWRITEBYTECODE: '1', ASTRID_INTERNAL_INVOCATION: '1' },
    input: JSON.stringify(payload), encoding: 'utf8', maxBuffer: 8 * 1024 * 1024,
  }));
}
function configOf(document: any): TimelineConfig {
  return { ...structuredClone(document.parent.config), clips: structuredClone(document.parent.clips) };
}
const json = (v: unknown) => new TextEncoder().encode(JSON.stringify(v));
afterEach(() => { cleanup(); resetFakeIndexedDB(); vi.unstubAllGlobals(); });

async function setup(mode?: string) {
  vi.stubGlobal('crypto', webcrypto);
  vi.stubGlobal('indexedDB', createFakeIndexedDB());
  const before = source({ base: true });
  if (mode === 'draft') delete before.parent.config.app.elements;
  if (mode === 'update' || mode === 'detach') Object.assign(before.parent.clips[0], { elementRef: ref, entrance: { type: ref.id, duration: .4 } });
  let document = structuredClone(before), head = 'parent-r1';
  const requests: CommitRequest[] = [], results: CommitResult[] = [];
  const accepted = new Map<string, CommitResult>(); let lost = false;
  const readbacks: string[] = [];
  const transport: Transport = async (method, path, _headers, bytes) => {
    let value: unknown;
    if (path === '/v1/health') value = { status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1 };
    else if (path === '/v1/handshake') value = { protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 'fixture', actor_id: 'reigh-product-connector', realm_id: 'fixture', scopes: RUNTIME_CLIENT_SCOPES, capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] };
    else if (path === '/v1/realm') value = { realm_id: 'fixture' };
    else if (method === 'POST' && path.endsWith('/commit')) {
      const request = JSON.parse(new TextDecoder().decode(bytes as Uint8Array));
      expect(request.change.commands).toBeDefined();
      expect(request.change.adapter).toBeUndefined();
      requests.push(request);
      const result = accepted.get(request.request_id) ?? source({ before: document, request });
      accepted.set(request.request_id, result);
      document = structuredClone(result.canonical_document); head = result.accepted_revision_id;
      results.push(result);
      if (mode === 'retry' && !lost) { lost = true; throw new TypeError('Lost accepted response'); }
      value = result;
    } else if (method === 'GET' && /\/composition-revisions\/[^/]+$/.test(path)) {
      const revision = path.split('/').pop()!;
      readbacks.push(revision);
      value = { project_id: 'p', timeline_id: 't', revision_id: revision, payload: {
        config: configOf(document), clips: document.parent.clips, registry: document.parent.registry ?? {}, occurrences: [] } };
    } else throw new Error(`Unexpected W12 in-memory transport ${method} ${path}`);
    return { status: 200, headers: {}, body: json(value) };
  };
  const session = new Map<string, string>();
  const provider = new RuntimeDataProvider({ projectId: 'p', baseUrl: 'http://w12.fixture', token: 'synthetic-test-only', transport,
    commitRouting: { enabled: true }, commitSessionStorage: { getItem: key => session.get(key) ?? null, setItem: (key, value) => { session.set(key, value); } } });
  const initial = await buildTimelineData(configOf(before), before.parent.registry ?? {});
  initial.head = { projectId: 'p', timelineId: 't', headRevisionId: head };
  const eventBus = new TimelineEventBus();
  const savedSeqRef = { current: 0 }, configVersionRef = { current: 1 }, headRevisionRef = { current: initial.head };
  const lastSavedSignatureRef = { current: initial.stableSignature }, interactionStateRef = { current: createInteractionState() };
  const query = new QueryClient({ defaultOptions: { mutations: { retry: false }, queries: { retry: false } } });
  const wrapper = ({ children }: { children: React.ReactNode }) => React.createElement(VideoEditorRuntimeProvider, {
    value: { provider, timelineId: 't', project: { projectId: 'p' }, toast: { error: vi.fn(), success: vi.fn(), info: vi.fn() } } as any,
    children: React.createElement(QueryClientProvider, { client: query }, children),
  });
  const hook = renderHook(() => {
    const commit = useTimelineCommit({ eventBus, initialData: initial, lastSavedSignatureRef });
    const persistence = useTimelinePersistence({ provider, assetResolver: provider, timelineId: 't', eventBus, ...commit,
      savedSeqRef, configVersionRef, headRevisionRef, lastSavedSignatureRef, interactionStateRef });
    const history = useTimelineHistory({ ...commit, eventBus, interactionStateRef, pendingOpsRef: { current: 0 } });
    useEffect(() => eventBus.on('scheduleSave', persistence.scheduleSave), [persistence.scheduleSave]);
    useEffect(() => eventBus.on('beforeCommit', history.onBeforeCommit), [history.onBeforeCommit]);
    return { ...commit, persistence, history };
  }, { wrapper });
  const adapter = new AstridElementOperationAdapter(context, {
    get: async () => ({ config: hook.result.current.data!.config, registry: initial.registry, config_version: configVersionRef.current, head: headRevisionRef.current }),
    save: async (_id, input) => {
      const current = hook.result.current.data!;
      const next = await buildTimelineData(input.config as TimelineConfig, initial.registry, undefined, current.configVersion, undefined, current.head);
      act(() => hook.result.current.commitData(next, { save: true, editCommands: input.editCommands }));
      await act(async () => { await hook.result.current.persistence.flushSaveTarget(hook.result.current.persistence.captureSaveTarget()); });
      return { config: configOf(document), registry: initial.registry, config_version: configVersionRef.current, head: headRevisionRef.current };
    },
  }, 'p');
  return { ...hook, adapter, provider, before, requests, results, readbacks, savedSeqRef, getDocument: () => document };
}

describe('W12 element reference public history', () => {
  it.each(['clip', 'overlay', 'update', 'detach', 'draft'] as const)('%s actual adapter typed save/readback whole-document Undo and receipt-derived Redo', async placement => {
    const h = await setup(placement);
    const opaque = structuredClone(h.before.parent.config.app.elements);
    let selected = ref;
    if (placement === 'draft') {
      const draft = await h.adapter.execute({ name: 'elements.create_draft', id: 'draft-owned', kind: 'effect', label: 'Draft', source: 'export default () => null;' });
      await h.adapter.execute({ name: 'elements.validate', draft_id: 'draft-owned' });
      selected = { id: draft.draft!.id, kind: 'effect', revision: draft.draft!.revision };
    }
    await h.adapter.execute(placement === 'update' ? { name: 'timeline.update_element', project: 'p', timeline: 't', expected_version: 1, clip_id: 'owned', params: null, params_mode: 'replace' }
      : placement === 'detach' ? { name: 'timeline.remove_element', project: 'p', timeline: 't', expected_version: 1, clip_id: 'owned' }
      : { name: 'timeline.apply_element', project: 'p', timeline: 't', expected_version: 1, placement: placement === 'draft' ? 'clip' : placement, clip_id: 'owned', element: selected, at: 1.25, duration: .75, params: { gain: .7 } });
    expect(isElementReferenceBatch((h.requests[0].change as any).commands)).toBe(true);
    expect(h.results[0].status).toBe('accepted');
    const accepted = structuredClone(h.getDocument());
    if (placement !== 'draft') expect(accepted.parent.config.app.elements).toEqual(opaque);
    else expect(h.results[0].change.direct_writes.some(w => w.id === 'parent' && w.path === 'config.app.elements')).toBe(true);
    const call = (h.requests[0].change as any).commands[0];
    if (placement === 'overlay') expect(call.created).toEqual(['parent/clip:element-local-glow-1250']);
    await waitFor(() => expect(h.result.current.history.canUndo).toBe(true));
    act(() => h.result.current.history.onRemoteData(h.result.current.data!, h.result.current.data!));
    expect(h.result.current.history.canUndo).toBe(true);
    act(() => h.result.current.history.undo());
    await waitFor(() => expect(h.savedSeqRef.current).toBe(2), { timeout: 60_000 });
    await waitFor(() => expect(h.result.current.history.canRedo).toBe(true));
    expect(h.getDocument()).toEqual(h.before);
    expect(isElementReferenceInverse((h.requests[1].change as any).commands[0])).toBe(true);
    act(() => h.result.current.history.redo());
    await waitFor(() => expect(h.savedSeqRef.current).toBe(3), { timeout: 60_000 });
    expect(h.getDocument()).toEqual(accepted);
    expect(h.readbacks).toContain(h.results[2].accepted_revision_id);
    expect(h.requests.map(row => row.request_id).length).toBe(new Set(h.requests.map(row => row.request_id)).size);
    expect(h.result.current.data!.config.app.elements).toEqual(accepted.parent.config.app.elements);
    if (process.env.W12_EVIDENCE_DIR) writeFileSync(path.join(process.env.W12_EVIDENCE_DIR, `public-history-${placement}.json`), JSON.stringify({ before: h.before, requests: h.requests, results: h.results, readbacks: h.readbacks }, null, 2));
  }, 120_000);

  it('ambiguous accepted response retry retains the exact request/session/allocated overlay identity', async () => {
    const h = await setup('retry');
    const captured = configOf(h.before);
    const adapter = new AstridElementOperationAdapter(context, {
      get: async () => ({ config: captured, registry: h.before.parent.registry ?? {}, config_version: 1, head: { projectId: 'p', timelineId: 't', headRevisionId: 'parent-r1' } }),
      save: async (_id, input) => {
        const result = await h.provider.saveTimelineAtHead!('t', input.config as TimelineConfig, input.head!, input.registry as any, undefined, input.editCommands);
        return { config: configOf(h.getDocument()), registry: h.before.parent.registry ?? {}, config_version: result.configVersion, head: result.head };
      },
    }, 'p');
    const operation = { name: 'timeline.apply_element', project: 'p', timeline: 't', expected_version: 1,
      placement: 'overlay', clip_id: 'owned', element: ref, at: 1.25, duration: .75 };
    await expect(adapter.execute(operation)).rejects.toThrow();
    await adapter.execute(operation);
    expect(h.requests).toHaveLength(2);
    expect(h.requests[0]).toEqual(h.requests[1]);
    expect(h.getDocument().parent.clips.filter((c: any) => c.id === 'element-local-glow-1250')).toHaveLength(1);
    if (process.env.W12_EVIDENCE_DIR) writeFileSync(path.join(process.env.W12_EVIDENCE_DIR, 'retry.json'), JSON.stringify({ requests: h.requests, results: h.results }, null, 2));
  }, 60_000);

  it('receipt adapter refuses missing/extra/tampered direct writes and arms Redo only from accepted inverse', async () => {
    vi.stubGlobal('crypto', webcrypto);
    const before = { clips: [{ id: 'a', at: 0, track: 'V', hold: 1, params: null }], app: { elements: {} } } as TimelineConfig;
    const after = structuredClone(before); after.clips[0].elementRef = ref; after.clips[0].params = { gain: .7 };
    const call = await elementReferenceCommand(before, after, 'a', 'assign', 'replace');
    const writes = ['elementRef', 'params'].map(path => ({ id: 'parent/clip:a', path, before: call.expect![path], after: call.args.fields[path] }));
    const receipt = { status: 'accepted', accepted_publication_id: 'pub', change: { direct_writes: writes } };
    const inverse = elementReferenceInverse([call], receipt)!;
    expect(isElementReferenceInverse(inverse)).toBe(true);
    for (const direct_writes of [writes.slice(1), [...writes, writes[0]], writes.map(w => ({ ...w, after: { state: 'present', value: null } }))]) {
      expect(elementReferenceInverse([call], { ...receipt, change: { direct_writes } })).toBeUndefined();
    }
    expect(elementReferenceInverse([inverse], { ...receipt, accepted_publication_id: 'undo', change: { direct_writes: inverse.args.writes } })).toBeDefined();
    expect(elementReferenceInverse([call], { ...receipt, status: 'no_change' })).toBeUndefined();
  });
  it('public provider rejects an owned incomplete receipt before immutable readback', async () => {
    vi.stubGlobal('crypto', webcrypto);
    const before = { clips: [{ id: 'a', at: 0, track: 'V', hold: 1 }] } as TimelineConfig;
    const after = structuredClone(before); after.clips[0].elementRef = ref;
    const call = await elementReferenceCommand(before, after, 'a', 'assign', 'keep');
    const transport = vi.fn(async () => { throw new Error('must refuse before readback'); });
    const provider = new RuntimeDataProvider({ projectId: 'p', baseUrl: 'http://w12.fixture', token: 'synthetic-test-only', transport });
    await expect((provider as any).readCommittedTimeline('t', { change: { commands: [call] } }, {
      status: 'accepted', accepted_publication_id: 'pub', change: { direct_writes: [] },
    })).rejects.toThrow('complete authored operation');
    expect(transport).not.toHaveBeenCalled();
  });

});
