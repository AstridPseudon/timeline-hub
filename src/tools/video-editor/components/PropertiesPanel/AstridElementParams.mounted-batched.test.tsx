// @vitest-environment jsdom
import { useState } from 'react';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import type { ClipSetParamsArgs, DocumentPin, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import type { WorkspaceClient } from '@/integrations/runtime/generated.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { document, environment, scope } from '@/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts';
import { createTimelineCommandSession, type CommandSessionState } from '@/tools/video-editor/commands/commitSession.ts';
import { buildTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { compileTimelinePatch } from '@/tools/video-editor/lib/timeline-patch.ts';
import { useTimelineOps } from '@/tools/video-editor/hooks/useTimelineOps.ts';
import type { AstridElementDescriptor } from '@/tools/video-editor/runtime/astrid-element-host.ts';
import { AstridElementParams } from '@/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx';
import { captureClipMove, submitClipMove } from '@/tools/video-editor/commands/semanticGestures.ts';
import { useTimelineCommandSession } from '@/tools/video-editor/hooks/useTimelineCommandSession.ts';
import { useTimelineCommit } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import { createTimelineStore } from '@/tools/video-editor/hooks/timelineStore.ts';
import { TimelineEventBus } from '@/tools/video-editor/hooks/useTimelineEventBus.ts';

const host = vi.hoisted(() => ({ descriptors: [] as AstridElementDescriptor[] }));
vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', async (importOriginal) => ({
  ...await importOriginal<typeof import('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx')>(),
  useVideoEditorRuntime: () => ({ astridElementHost: host }),
}));
const releases: (() => void)[] = [];
const sessions: Awaited<ReturnType<typeof createTimelineCommandSession>>[] = [];
afterEach(async () => {
  releases.splice(0).forEach((release) => release());
  cleanup();
  for (const session of sessions.splice(0)) await session.dispose();
  vi.unstubAllGlobals();
});

async function setup(extraProperties: Record<string, unknown> = {}) {
  const reference = { packId: 'test_pack', id: 'reveal', kind: 'effect' as const, revision: `sha256:${'1'.repeat(64)}` };
  host.descriptors = [{ ...reference, componentPath: 'fixture', schema: {
    properties: { seed: { type: 'number', title: 'Seed', maximum: 10 }, text: { type: 'string', title: 'Text' }, ...extraProperties },
  } }];
  // Synthetic exact read specimens and normal-port transport. This is not native validation.
  const bytes = Buffer.from(JSON.stringify({ schema: host.descriptors[0].schema }));
  const digest = fixtureDigest({ snapshot: bytes.toString('base64') });
  const object = { object_id: digest, digest, size: bytes.length, media_type: 'application/json' as const };
  const snapshot: VerifiedDocumentObject = { ...object, bytes_base64: bytes.toString('base64') };
  const content = { schema: 'astrid.project-pack/v1', source_binding_key: 'project-packs', pack_id: reference.packId,
    relative_manifest: `${scope.realmId}/${scope.projectId}/packs/${reference.packId}/pack.yaml`,
    admissions: [{ ...reference, snapshot_object: object }] };
  const pin: DocumentPin = { document_id: 'retained-v1', version: 1, content_digest: fixtureDigest(content) };
  const verified: VerifiedDocument = { pin, document: { document_id: pin.document_id, project_id: scope.projectId,
    kind: 'astrid.project-pack', version: 1, content } };
  const raw = document();
  for (const clips of [raw.parent_revision.payload.clips, raw.parent_revision.payload.config.clips]) {
    Object.assign(clips[0], { clipType: 'text', elementRef: reference, params: { seed: 4, text: 'original', opaque: [null, false] } });
  }
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  const env = await environment(raw, (before, command) => {
    const next = structuredClone(before), args = command.args as ClipSetParamsArgs;
    const row = next.parent_revision.payload.clips[0];
    row.params = { ...row.params, ...args.values };
    for (const key of args.clear) delete row.params[key];
    next.parent_revision.payload.config.clips = structuredClone(next.parent_revision.payload.clips);
    return next;
  });
  const reads = {
    getProjectVerifiedDocument: vi.fn<WorkspaceClient['getProjectVerifiedDocument']>(async () => verified),
    getProjectVerifiedDocumentObject: vi.fn<WorkspaceClient['getProjectVerifiedDocumentObject']>(async () => snapshot),
  };
  const dataRef = { current: env.current() };
  let notifyState: ((state: CommandSessionState) => void) | undefined;
  let notifyData: ((data: TimelineData) => void) | undefined;
  const session = await createTimelineCommandSession({ scope, initial: env.initial, outboxes: env.outboxes,
    loadLatest: () => env.provider.loadTimelineCommandBasis(scope.timelineId),
    send: (request, key) => env.provider.commitTimeline(request, key), paramReadClient: reads,
    changed: (state) => notifyState?.(state),
    preview: (patch) => {
      dataRef.current = compileTimelinePatch(patch, dataRef.current).nextData!;
      notifyData?.(dataRef.current);
    },
    project: async (basis, previews) => {
      const parent = basis.canonicalDocument.parent_revision.payload;
      let next = await buildTimelineData({ ...parent.config as object, clips: parent.clips } as never,
        { assets: {} }, undefined, 1, undefined, { projectId: scope.projectId, timelineId: scope.timelineId,
          headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId });
      for (const patch of previews) next = compileTimelinePatch(patch, next).nextData!;
      dataRef.current = next;
      notifyData?.(next);
    },
  });
  sessions.push(session);
  const legacy = vi.fn();
  let ops: ReturnType<typeof useTimelineOps>;
  function Harness({ retainedPin = pin }: { retainedPin?: DocumentPin }) {
    const [state, setState] = useState(session.getState());
    const [data, setData] = useState(dataRef.current);
    notifyState = setState;
    notifyData = setData;
    ops = useTimelineOps({ dataRef, commitData: legacy, clipParamsPort: session.clipParamsPort,
      createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [] });
    return <AstridElementParams clip={data.resolvedConfig.clips[0]} registry={{}} onChange={legacy}
      retainedDocumentPin={retainedPin} timelineOps={ops} commandState={state} />;
  }
  const view = render(<Harness />);
  const pause = () => { const held = env.pause(); releases.push(held.resolve); return held; };
  const edit = (value: string) => fireEvent.change(screen.getByLabelText('Seed'), { target: { value } });
  const apply = () => fireEvent.click(screen.getByRole('button', { name: 'Apply parameters' }));
  return { env, pin, reads, session, dataRef, view, Harness, legacy, pause, edit, apply, getOps: () => ops };
}

async function hooked(f: Awaited<ReturnType<typeof setup>>, form = false) {
  f.view.unmount();
  await f.session.dispose();
  vi.stubGlobal('indexedDB', f.env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _opts: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const initial = f.dataRef.current;
  const eventBus = new TimelineEventBus();
  const lastSavedSignatureRef = { current: initial.stableSignature };
  const configVersionRef = { current: initial.configVersion };
  const headRevisionRef = { current: initial.head };
  const snapshotWriteBlockedRef = { current: false };
  const store = createTimelineStore();
  const useMounted = () => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
    const commands = useTimelineCommandSession({ provider: f.env.provider, timelineId: scope.timelineId,
      commit, legacyClean: () => true, resolveAssetUrl: async (file) => file, loaded: undefined,
      snapshotWriteBlockedRef, headRevisionRef, configVersionRef, lastSavedSignatureRef, store,
      shots: { canonicalDraft: null } as never, paramReadClient: f.reads });
    const ops = useTimelineOps({ dataRef: commit.dataRef, commitData: f.legacy, clipParamsPort: commands.clipParamsPort,
      createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [] });
    return { commands, commit, ops };
  };
  let current: ReturnType<typeof useMounted>;
  function Mounted() {
    current = useMounted();
    const data = current.commit.data;
    return form && data && current.commands.clipParamsPort
      ? <AstridElementParams clip={data.resolvedConfig.clips[0]} registry={{}} onChange={f.legacy}
        retainedDocumentPin={f.pin} timelineOps={current.ops} commandState={current.commands.state} /> : null;
  }
  const view = render(<Mounted />);
  const hook = { result: { get current() { return current; } }, unmount: view.unmount };
  await waitFor(() => expect(hook.result.current.commands.clipParamsPort).toBeDefined());
  return hook;
}

it('retires accepted fields when a PARAM and its ordinary suffix finish within one act', async () => {
  const f = await setup(), held = f.pause();
  f.edit('8'); f.apply();
  await waitFor(() => expect(f.env.commits()).toHaveLength(1));
  act(() => f.env.move(f.session, 5));
  await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
  await act(async () => { held.resolve(); await f.session.flush(); });
  expect(f.env.commits()).toHaveLength(2);
  expect(screen.getByLabelText('Seed accepted value').textContent).toBe('8');
  expect(screen.getByRole('button', { name: 'Apply parameters' })).toBeDisabled();
});

it('forwards submitted input through the actual mounted command-session wrapper', async () => {
  const f = await setup();
  const hook = await hooked(f);
  try {
    f.env.setFault('refused');
    await act(async () => { await hook.result.current.ops.setClipParams!('x', { values: { seed: 16 }, clear: [], schema_source: f.pin }); });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('error'));
    expect(hook.result.current.ops.getSubmittedClipParams!('x')).toMatchObject({ accepted: false, args: { values: { seed: 16 }, schema_source: f.pin } });
  } finally { hook.unmount(); }
});

it('restores durable refused16 in the actual form from the mounted command-session wrapper', async () => {
  const f = await setup();
  const hook = await hooked(f);
  try {
    f.env.setFault('refused');
    await act(async () => { await hook.result.current.ops.setClipParams!('x', { values: { seed: 16 }, clear: [], schema_source: f.pin }); });
    await waitFor(() => expect(hook.result.current.commands.state.status).toBe('error'));
    const data = hook.result.current.commit.data!;
    const saved = await f.env.outboxes.list(scope);
    const original = JSON.stringify(saved);
    const reads = f.reads.getProjectVerifiedDocument.mock.calls.length;
    render(<AstridElementParams clip={data.resolvedConfig.clips[0]} registry={{}} onChange={f.legacy}
      retainedDocumentPin={f.pin} timelineOps={hook.result.current.ops} commandState={hook.result.current.commands.state} />);
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    const input = hook.result.current.ops.getSubmittedClipParams!('x')!;
    const refused = saved.find(box => box.intents.length)!;
    expect(input.basis).toEqual((refused.intents[0].payload as unknown as { selectedParams: { basis: object } }).selectedParams.basis);
    expect(input.args.schema_source).toEqual(f.pin);
    expect(JSON.stringify(await f.env.outboxes.list(scope))).toBe(original);
    expect(f.reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(reads);
    expect(f.env.commits()).toHaveLength(1);
    expect(f.legacy).not.toHaveBeenCalled();
  } finally { hook.unmount(); }
});


it('does not resend an already accepted PARAM field with a later unrelated field after batched ACKs', async () => {
  const f = await setup(), held = f.pause();
  f.edit('8'); f.apply();
  await waitFor(() => expect(f.env.commits()).toHaveLength(1));
  act(() => f.env.move(f.session, 5));
  await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
  await act(async () => { held.resolve(); await f.session.flush(); });
  const remote = await f.env.external(raw => {
    for (const clips of [raw.parent_revision.payload.clips, raw.parent_revision.payload.config.clips]) clips[0].params.seed = 9;
  });
  act(() => f.session.observe(remote));
  await waitFor(() => expect(screen.getByLabelText('Seed accepted value').textContent).toBe('9'));
  fireEvent.change(screen.getByLabelText('Text'), { target: { value: '"new"' } });
  f.apply();
  await waitFor(() => expect(f.env.commits()).toHaveLength(3));
  await act(async () => { await f.session.flush(); });
  expect(f.env.commits()[2].body!.commands[0].args).toEqual({ values: { text: 'new' }, clear: [], schema_source: f.pin });
});

it('follows accepted params after PARAM acknowledgement and inverse complete in one render batch', async () => {
  const f = await setup(), held = f.pause();
  f.edit('8'); f.apply();
  await waitFor(() => expect(f.env.commits()).toHaveLength(1));
  await act(async () => { held.resolve(); await f.session.flush(); await f.session.undo(); await f.session.flush(); });
  expect(f.env.commits().map(call => call.body!.commands[0].op)).toEqual(['clip.set-params', 'timeline.inverse']);
  expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
  expect(screen.getByLabelText('Seed')).toHaveValue('4');
});

it('keeps unsubmitted dirty16 on an equal-head observation without any read or send', async () => {
  const f = await setup();
  f.edit('16');
  act(() => { f.session.observe(f.env.initial); });
  expect(screen.getByLabelText('Seed')).toHaveValue('16');
  expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
  expect(f.env.commits()).toHaveLength(0);
  expect(f.reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
});

it('keeps the retained submission snapshot read-only through repeated reads and disposal', async () => {
  const f = await setup();
  f.env.setFault('refused'); f.edit('16'); f.apply();
  await waitFor(() => expect(f.env.commits()).toHaveLength(1));
  await act(async () => { await expect(f.session.flush()).rejects.toThrow(); });
  const before = JSON.stringify(await f.env.outboxes.list(scope));
  const readCount = f.reads.getProjectVerifiedDocument.mock.calls.length;
  const input = f.getOps().getSubmittedClipParams!('x')!;
  expect(input.accepted).toBe(false);
  expect(input.args.schema_source).toEqual(f.pin);
  expect(Object.isFrozen(input)).toBe(true);
  expect(Object.isFrozen(input.args.values)).toBe(true);
  for (let i = 0; i < 3; i++) expect(f.getOps().getSubmittedClipParams!('x')).toEqual(input);
  await f.session.dispose();
  expect(f.getOps().getSubmittedClipParams!('x')).toEqual(input);
  expect(JSON.stringify(await f.env.outboxes.list(scope))).toBe(before);
  expect(f.reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(readCount);
  expect(f.env.commits()).toHaveLength(1);
});

it('keeps exact outcomes for multiple PARAMs, an ordinary suffix, and a cancelled same-value PARAM', async () => {
  const f = await setup(), held = f.pause();
  f.edit('8'); f.apply();
  await waitFor(() => expect(f.env.commits()).toHaveLength(1));
  const first = f.getOps().getSubmittedClipParams!('x')!;
  expect(first.accepted).toBe(false);
  await act(async () => {
    await f.getOps().setClipParams!('x', { values: { seed: 8 }, clear: [], schema_source: f.pin });
  });
  const cancelled = f.getOps().getSubmittedClipParams!('x')!;
  expect(cancelled.id).not.toBe(first.id);
  await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
  await act(async () => {
    held.resolve();
    await expect(f.session.flush()).rejects.toThrow('accepted original basis');
  });
  expect(first.accepted).toBe(true);
  expect(cancelled.accepted).toBe(false);
  expect(f.env.commits()).toHaveLength(1);
  await act(async () => { await f.session.undo(); });
  expect(cancelled.accepted).toBe(false);

  const secondHeld = f.pause();
  await act(async () => {
    await f.getOps().setClipParams!('x', { values: { seed: 8 }, clear: [], schema_source: f.pin });
  });
  await waitFor(() => expect(f.env.commits()).toHaveLength(2));
  const second = f.getOps().getSubmittedClipParams!('x')!;
  expect(second.id).not.toBe(cancelled.id);
  expect(second.accepted).toBe(false);
  act(() => submitClipMove(captureClipMove(f.session.port, f.dataRef.current, 'x'), 5));
  await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
  await act(async () => { secondHeld.resolve(); await f.session.flush(); });
  expect(f.env.commits().map(call => call.body!.commands[0].op)).toEqual(['clip.set-params', 'clip.set-params', 'clip.move']);
  expect(first.accepted).toBe(true);
  expect(second.accepted).toBe(true);
  expect(cancelled.accepted).toBe(false);
  expect(f.dataRef.current.config.clips[0].params.seed).toBe(8);
});

it('keeps cancelled raw16 dirty through another PARAM and ordinary ACK in one batch', async () => {
  const f = await setup(), held = f.pause();
  act(() => f.env.move(f.session, 5));
  await waitFor(() => expect(f.env.commits()).toHaveLength(1));
  f.edit('16'); f.apply();
  await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
  const cancelled = f.getOps().getSubmittedClipParams!('x')!;
  await act(async () => {
    held.resolve();
    await expect(f.session.flush()).rejects.toThrow('accepted original basis');
    await f.session.undo();
  });
  expect(cancelled.accepted).toBe(false);
  const nextHeld = f.pause();
  await act(async () => {
    await f.getOps().setClipParams!('x', { values: { text: 'elsewhere' }, clear: [], schema_source: f.pin });
  });
  await waitFor(() => expect(f.env.commits()).toHaveLength(2));
  act(() => submitClipMove(captureClipMove(f.session.port, f.dataRef.current, 'x'), 6));
  await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
  await act(async () => { nextHeld.resolve(); await f.session.flush(); });
  expect(cancelled.accepted).toBe(false);
  expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
  expect(screen.getByLabelText('Seed')).toHaveValue('16');
  expect(screen.getByRole('button', { name: 'Apply parameters' })).toBeEnabled();
  expect(f.env.commits().map(call => call.body!.commands[0].op)).toEqual(['clip.move', 'clip.set-params', 'clip.move']);
});

it('retires an accepted field through the mounted hook and form when ordinary ACKs coalesce', async () => {
  const f = await setup();
  const hook = await hooked(f, true), held = f.pause();
  try {
    f.edit('8'); f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    act(() => submitClipMove(captureClipMove(hook.result.current.commands.port,
      hook.result.current.commit.dataRef.current!, 'x'), 5));
    await waitFor(async () => expect((await f.env.outboxes.list(scope)).find(box => box.intents.length)?.intents).toHaveLength(2));
    await act(async () => { held.resolve(); await hook.result.current.commands.flush(); });
    expect(f.env.commits()).toHaveLength(2);
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('8');
    expect(screen.getByRole('button', { name: 'Apply parameters' })).toBeDisabled();
    expect(f.legacy).not.toHaveBeenCalled();
  } finally { hook.unmount(); }
});
