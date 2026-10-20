// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, expect, it, vi } from 'vitest';
import { document, environment, scope } from '../commands/__tests__/commitSessionEnvironment.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import type { ClipSetParamsArgs, DocumentPin, JSON, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import type { CommitRequest, Transport } from '@/integrations/runtime/generated.ts';
import { createCommitOutbox } from '../commands/commitOutbox.ts';
import { useTimelineSave } from './useTimelineSave.ts';
import { useTimelineOps } from './useTimelineOps.ts';
import { createTimelineStore } from './timelineStore.ts';
import { createInteractionState } from '../lib/interaction-state.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

async function setup() {
  // Synthetic HTTP authority: this tests authenticated forwarding, not native schema validation.
  const selected = { packId: 'test_pack', id: 'reveal', kind: 'effect', revision: `sha256:${'1'.repeat(64)}` };
  const bytes = Buffer.from(JSON.stringify({ schema: { properties: { seed: { maximum: 10 } } } }));
  const digest = fixtureDigest({ maximum: 10 });
  const descriptor = { object_id: digest, digest, size: bytes.length, media_type: 'application/json' as const };
  const snapshot: VerifiedDocumentObject = { ...descriptor, bytes_base64: bytes.toString('base64') };
  const content = { schema: 'astrid.project-pack/v1', source_binding_key: 'project-packs', pack_id: selected.packId,
    relative_manifest: `${scope.realmId}/${scope.projectId}/packs/${selected.packId}/pack.yaml`,
    admissions: [{ id: selected.id, kind: selected.kind, revision: selected.revision, snapshot_object: descriptor }] };
  const pin: DocumentPin = { document_id: 'retained-v1', version: 1, content_digest: fixtureDigest(content) };
  const verified: VerifiedDocument = { pin, document: { document_id: pin.document_id, project_id: scope.projectId,
    kind: 'astrid.project-pack', version: pin.version, content } };
  const raw = document();
  for (const clips of [raw.parent_revision.payload.clips as object[],
    (raw.parent_revision.payload.config as { clips: object[] }).clips]) {
    Object.assign(clips[0], { clipType: 'text', elementRef: selected,
      params: { seed: 4, remove: null, opaque: [null, false, {}] } });
  }
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  const env = await environment(raw, (before, command) => {
    const next = structuredClone(before), args = command.args as ClipSetParamsArgs;
    const clips = next.parent_revision.payload.clips as { params: Record<string, JSON> }[];
    clips[0].params = { ...clips[0].params, ...args.values };
    for (const key of args.clear) delete clips[0].params[key];
    (next.parent_revision.payload.config as { clips: JSON }).clips = structuredClone(clips);
    return next;
  });
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const calls: { path: string; headers: Record<string, string>; request?: CommitRequest }[] = [];
  const reads = vi.fn(async (path: string) => path.includes('/document-inputs/') ? verified : snapshot);
  const wireCommits = () => calls.filter((call) => call.path.endsWith('/commit'));
  const transport: Transport = async (method, path, headers, body) => {
    const request = body ? JSON.parse(new TextDecoder().decode(body)) as CommitRequest : undefined;
    calls.push({ path, headers, request });
    const response = (value: unknown, status = 200) => ({ status, headers: {}, body: new TextEncoder().encode(JSON.stringify(value)) });
    if (path.includes('/document-inputs/') || path.includes('/document-objects/')) return response(await reads(path));
    const command = request?.commands?.[0];
    if (path.endsWith('/commit') && command?.op === 'clip.set-params' && (command.args as ClipSetParamsArgs).values.seed === 16) {
      return response({ code: 'validation', message: 'seed exceeds retained maximum 10', details: {} }, 422);
    }
    return env.transport(method, path, headers, body);
  };
  const provider = new RuntimeDataProvider({ projectId: scope.projectId, baseUrl: `http://bridge-${crypto.randomUUID()}.test`,
    token: 'existing-provider-token', transport });
  const store = createTimelineStore(), interaction = { current: createInteractionState() };
  const queries = { timelineQuery: { data: undefined, isLoading: false }, assetRegistryQuery: { data: undefined } };
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const runtime = { provider, timelineId: scope.timelineId, shots: { canonicalDraft: null },
    assetResolver: { resolveAssetUrl: async (file: string) => file } } as unknown as VideoEditorRuntimeContextValue;
  const wrapper = ({ children }: { children: React.ReactNode }) => <QueryClientProvider client={queryClient}>
    <VideoEditorRuntimeProvider value={runtime}>{children}</VideoEditorRuntimeProvider>
  </QueryClientProvider>;
  const hook = renderHook(({ provider }) => {
    const save = useTimelineSave(queries as never, provider, interaction, store, env.current());
    const ops = useTimelineOps({ dataRef: save.dataRef, commitData: save.commitData,
      clipParamsPort: save.commands.clipParamsPort, createManualCheckpoint: async () => {},
      jumpToCheckpoint: () => {}, checkpoints: [] });
    return { save, ops };
  }, { wrapper, initialProps: { provider } });
  await waitFor(() => expect(hook.result.current.save.commands.state.status).toBe('saved'));
  await waitFor(() => expect(hook.result.current.save.commands.clipParamsPort).toBeDefined());
  const params = () => hook.result.current.save.dataRef.current?.resolvedConfig.clips[0].params;
  const close = () => { hook.unmount(); queryClient.clear(); };
  return { env, pin, snapshot, verified, provider, transport, reads, calls, wireCommits, hook, params, close };
}

it('reads the given exact pin through the provider session and displays only the accepted result', async () => {
  const f = await setup();
  try {
    const pause = f.env.pause();
    const args = { values: { seed: 8, literal: [null, false, '', {}] }, clear: ['remove'], schema_source: structuredClone(f.pin) };
    const original = structuredClone(args);
    await act(async () => { await f.hook.result.current.ops.setClipParams!('x', args); });
    args.schema_source.version = 2;
    args.values.seed = 16;
    await waitFor(() => expect(f.wireCommits()).toHaveLength(1));
    expect(f.hook.result.current.save.commands.state.status).toBe('pending');
    expect(f.params()).toEqual({ seed: 4, remove: null, opaque: [null, false, {}] });
    const readCalls = f.calls.filter((call) => call.path.includes('/verified?'));
    expect(readCalls).toHaveLength(2);
    for (const call of readCalls) {
      const url = new URL(call.path, 'http://test');
      expect(url.pathname).toContain(`/projects/${scope.projectId}/`);
      expect(Object.fromEntries(url.searchParams)).toMatchObject({ ...f.pin, version: '1' });
      expect(call.headers.Authorization).toBe('Bearer existing-provider-token');
    }
    expect(new URL(readCalls[1].path, 'http://test').searchParams.get('object_id')).toBe(f.snapshot.object_id);
    expect(f.calls.filter((call) => call.path === '/v1/handshake')).toHaveLength(1);
    expect(f.calls.filter((call) => call.path === '/v1/realm')).toHaveLength(1);
    expect(f.wireCommits()[0].request!.commands[0].args).toEqual(original);
    pause.resolve();
    await act(async () => { await f.hook.result.current.save.commands.flush(); });
    expect(f.params()).toEqual({ seed: 8, literal: original.values.literal, opaque: [null, false, {}] });
    expect(f.hook.result.current.save.commands.state.status).toBe('saved');
    expect(f.calls.every((call) => !call.path.includes('/documents/'))).toBe(true);
  } finally { f.close(); }
});

it('sends literal16 to the server and preserves the refused draft, original pin and accepted4', async () => {
  const f = await setup();
  try {
    const args = { values: { seed: 16 }, clear: ['remove'], schema_source: f.pin };
    await act(async () => { await f.hook.result.current.ops.setClipParams!('x', args); });
    await act(async () => { await expect(f.hook.result.current.save.commands.flush()).rejects.toThrow('maximum 10'); });
    expect(f.wireCommits()).toHaveLength(1);
    expect(f.wireCommits()[0].request!.commands[0].args).toEqual(args);
    expect(f.hook.result.current.save.commands.state).toMatchObject({ status: 'error', error: expect.stringContaining('maximum 10') });
    expect(f.params()).toEqual({ seed: 4, remove: null, opaque: [null, false, {}] });
    const outbox = createCommitOutbox({ indexedDB: f.env.factory });
    const [saved] = await outbox.list(scope);
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ args }], selectedParams: {
      schema_inputs: [[f.verified, { [f.snapshot.object_id]: f.snapshot }]], realm_id: scope.realmId } });
    expect(f.env.commits()).toHaveLength(0);
  } finally { f.close(); }
});

it.each(['document', 'object'] as const)('refuses an unavailable exact %s read without a latest fallback or commit', async (stage) => {
  const f = await setup();
  try {
    f.reads.mockImplementation(async (path) => {
      if (path.includes(stage === 'document' ? '/document-inputs/' : '/document-objects/')) throw new Error('exact read unavailable');
      return f.verified;
    });
    await act(async () => {
      await expect(f.hook.result.current.ops.setClipParams!('x', { values: { seed: 8 }, clear: [], schema_source: f.pin }))
        .rejects.toThrow('exact read unavailable');
    });
    expect(f.params()?.seed).toBe(4);
    expect(f.wireCommits()).toHaveLength(0);
    expect(f.calls.every((call) => !call.path.includes('/documents/'))).toBe(true);
  } finally { f.close(); }
});

it.each(['dispose', 'client', 'project'] as const)('refuses a late retained read after %s changes', async (change) => {
  const f = await setup();
  try {
    let release!: () => void;
    f.reads.mockImplementationOnce(async () => {
      await new Promise<void>((resolve) => { release = resolve; });
      return f.verified;
    });
    const editing = f.hook.result.current.ops.setClipParams!('x', { values: { seed: 8 }, clear: [], schema_source: f.pin });
    const outcome = editing.catch((error: unknown) => error);
    await waitFor(() => expect(release).toBeDefined());
    if (change === 'dispose') f.hook.unmount();
    else f.hook.rerender({ provider: new RuntimeDataProvider({ projectId: change === 'project' ? 'another-project' : scope.projectId,
      baseUrl: `http://replacement-${crypto.randomUUID()}.test`, token: 'replacement', transport: f.transport }) });
    await act(async () => { release(); expect(await outcome).toBeInstanceOf(Error); });
    expect(f.params()?.seed).toBe(4);
    expect(f.wireCommits()).toHaveLength(0);
  } finally { f.close(); }
});

it('refuses either cross-project read before sending traffic', async () => {
  const f = await setup();
  try {
    const count = f.calls.length;
    expect(() => f.provider.paramReadClient.getProjectVerifiedDocument('other', f.pin)).toThrow('another project');
    expect(() => f.provider.paramReadClient.getProjectVerifiedDocumentObject('other', f.pin, f.snapshot.object_id)).toThrow('another project');
    expect(f.calls).toHaveLength(count);
  } finally { f.close(); }
});
