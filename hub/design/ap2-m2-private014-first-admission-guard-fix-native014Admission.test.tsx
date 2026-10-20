// @vitest-environment jsdom
import React from 'react';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { act, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { CONTRACT_VERSION } from '@/integrations/runtime/generated-contract-metadata.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { WorkspaceClient, type Transport } from '@/integrations/runtime/generated.ts';
import { VideoEditorRuntimeProvider } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore } from '@/tools/video-editor/hooks/timelineStore.ts';
import { useTimelineSave } from '@/tools/video-editor/hooks/useTimelineSave.ts';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { createInteractionState } from '@/tools/video-editor/lib/interaction-state.ts';
import { createCommitOutbox } from '@/tools/video-editor/commands/commitOutbox.ts';

const trace = vi.hoisted(() => ({ initialReadReady: false }));
vi.mock('@/tools/video-editor/hooks/useTimelineCommandSession.ts', async (importOriginal) => {
  const real = await importOriginal<typeof import('@/tools/video-editor/hooks/useTimelineCommandSession.ts')>();
  return { ...real, useTimelineCommandSession: (options: Parameters<typeof real.useTimelineCommandSession>[0]) => {
    trace.initialReadReady = options.initialReadReady ?? true;
    return real.useTimelineCommandSession(options);
  } };
});
const native = JSON.parse(readFileSync(process.env.NATIVE_ADMISSION_FIXTURE!, 'utf8'));
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

it.each(['neutral', 'authoring'] as const)('traces the first admission guard with native %s responses', async (mode) => {
  expect(CONTRACT_VERSION).toBe('0.2.14');
  expect(RUNTIME_SCHEMA_DIGEST).toBe(native[mode].health.schema_digest);
  vi.stubGlobal('indexedDB', createFakeIndexedDB());
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const calls: string[] = [];
  const generatedHistory = vi.spyOn(WorkspaceClient.prototype, 'listTimelineCommits');
  const transport: Transport = async (method, path) => {
    calls.push(`${method} ${path}`);
    const reply = (body: unknown, status = 200) => ({ status, headers: {}, body: new TextEncoder().encode(JSON.stringify(body)) });
    // RuntimeHandler adds daemon.instance_id to service.health(). This in-process
    // capture supplies the transport instance without starting a live daemon.
    if (path === '/v1/health') return reply({ ...native[mode].health, runtime_instance_id: `offline-${mode}` });
    if (path === '/v1/handshake') return reply(native[mode].handshake);
    if (path === '/v1/realm') return reply(native[mode].realm);
    if (path.endsWith('/commits?limit=50')) return reply(native[mode].history.body, native[mode].history.status);
    if (path.endsWith('/composition-revisions/seed-r1')) return reply(native.parent);
    throw new Error(`Unexpected ${method} ${path}`);
  };
  const provider = new RuntimeDataProvider({ projectId: native.projectId, token: 'offline-product', baseUrl: `http://${mode}.test`, transport });
  const data = await buildTimelineData(native.parent.payload.config, native.parent.payload.registry, undefined, 1, undefined,
    { projectId: native.projectId, timelineId: native.timelineId, headRevisionId: 'seed-r1', headPublicationId: native[mode].head.publication_id });
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const store = createTimelineStore();
  const runtime = { provider, timelineId: native.timelineId, shots: { canonicalDraft: null },
    project: { projectId: native.projectId }, toast: { error: vi.fn() } };
  const wrapper = ({ children }: { children: React.ReactNode }) => React.createElement(QueryClientProvider, { client: queryClient },
    React.createElement(VideoEditorRuntimeProvider, { value: runtime as never }, children));
  const queries = { timelineQuery: { data, isLoading: false }, assetRegistryQuery: { data: data.registry } };
  const interaction = { current: createInteractionState() };
  const hook = renderHook(() => useTimelineSave(queries, provider, interaction, store), { wrapper });
  await waitFor(() => expect(trace.initialReadReady).toBe(true));
  await waitFor(() => expect(hook.result.current.commands.state.status).toBe(mode === 'neutral' ? 'error' : 'saved'));
  expect(hook.result.current.commands.enabled).toBe(true);
  expect(generatedHistory).toHaveBeenCalledWith(native.projectId, native.timelineId, undefined, 50);
  const identity = await provider.getRecoverableIdentity();
  const owners = await createCommitOutbox().list({ ...identity, projectId: native.projectId, timelineId: native.timelineId });
  if (mode === 'neutral') {
    expect(hook.result.current.commands.state.ownerId).toBeNull();
    expect(hook.result.current.commands.state.error).toContain('history_unavailable');
    expect(owners).toEqual([]);
    expect(calls.some(path => path.includes('/composition-revisions/'))).toBe(false);
  } else {
    expect(hook.result.current.commands.state.ownerId).toBeTruthy();
    expect(owners).toHaveLength(1);
    expect(hook.result.current.data?.head?.headPublicationId).toBe(native.authoring.head.publication_id);
    expect(hook.result.current.commands.port).toBeDefined();
    expect(held.size).toBe(1);
  }
  expect(calls.every(path => path.startsWith('GET ') || path === 'POST /v1/handshake')).toBe(true);
  writeFileSync(path.join(path.dirname(process.env.NATIVE_ADMISSION_FIXTURE!), `${mode}-app-trace.json`), JSON.stringify({ mode, contract: CONTRACT_VERSION, schema: RUNTIME_SCHEMA_DIGEST,
    health: native[mode].health.status, handshake: identity, enabled: hook.result.current.commands.enabled,
    recoveryChecked: trace.initialReadReady, rawBundle: native.parent.payload.config.bundle ?? null,
    displayedHead: hook.result.current.data?.head, history: native[mode].history,
    commandState: hook.result.current.commands.state, ownerCount: owners.length, leases: held.size, calls }, null, 2));
  hook.unmount();
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
  queryClient.clear();
});
