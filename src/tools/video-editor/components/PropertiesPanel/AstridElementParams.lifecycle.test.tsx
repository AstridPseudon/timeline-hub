// @vitest-environment jsdom
import { useState } from 'react';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
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

const host = vi.hoisted(() => ({ descriptors: [] as AstridElementDescriptor[] }));
vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useVideoEditorRuntime: () => ({ astridElementHost: host }),
}));
const releases: (() => void)[] = [];
const sessions: Awaited<ReturnType<typeof createTimelineCommandSession>>[] = [];
afterEach(async () => {
  releases.splice(0).forEach((release) => release());
  cleanup();
  for (const session of sessions.splice(0)) await session.dispose();
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


describe('independent actual ingress behavior checks', () => {
  it('keeps raw16 in the form after explicitly cancelling its unsent original-basis command', async () => {
    const f = await setup(), held = f.pause();
    act(() => { f.env.move(f.session, 5); });
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    f.edit('16'); f.apply();
    await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
    held.resolve();
    await act(async () => { await expect(f.session.flush()).rejects.toThrow('accepted original basis'); });
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    await act(async () => { await f.session.undo(); });
    expect(f.session.getState().status).toBe('saved');
    expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(0);
    expect(f.env.commits()).toHaveLength(1);
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('keeps a raw draft across ordinary ACK, blur and refocus without submitting a PARAM', async () => {
    const f = await setup(), held = f.pause();
    f.edit('16');
    fireEvent.focus(screen.getByLabelText('Seed'));
    fireEvent.blur(screen.getByLabelText('Seed'));
    fireEvent.focus(screen.getByLabelText('Seed'));
    fireEvent.blur(screen.getByLabelText('Seed'));
    act(() => { f.env.move(f.session, 5); });
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    held.resolve();
    await act(async () => { await f.session.flush(); });
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    expect(f.env.commits().map(call => call.body!.commands[0].op)).toEqual(['clip.move']);
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('refuses the entire compound draft on invalid JSON, then preserves null separately from blank clear', async () => {
    const f = await setup();
    f.edit('8');
    fireEvent.change(screen.getByLabelText('Text'), { target: { value: '[' } });
    f.apply();
    await waitFor(() => expect(screen.getByRole('alert')).toBeTruthy());
    expect(f.env.commits()).toHaveLength(0);
    expect(f.reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
    expect(screen.getByLabelText('Seed')).toHaveValue('8');
    fireEvent.change(screen.getByLabelText('Text'), { target: { value: 'null' } });
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    await act(async () => { await f.session.flush(); });
    expect(f.env.commits()[0].body!.commands[0].args).toEqual({ values: { seed: 8, text: null }, clear: [], schema_source: f.pin });
    expect(f.dataRef.current.config.clips[0].params).toEqual({ seed: 8, text: null, opaque: [null, false] });
    fireEvent.change(screen.getByLabelText('Text'), { target: { value: '' } });
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(2));
    await act(async () => { await f.session.flush(); });
    expect(f.env.commits()[1].body!.commands[0].args).toEqual({ values: {}, clear: ['text'], schema_source: f.pin });
    expect(f.dataRef.current.config.clips[0].params).toEqual({ seed: 8, opaque: [null, false] });
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('sends prototype-looking JSON property names and nested unknown/asset values unchanged', async () => {
    const f = await setup(JSON.parse('{"__proto__":{"title":"Prototype"},"constructor":{"title":"Constructor"},"asset":{"title":"Asset"}}'));
    fireEvent.change(screen.getByLabelText('Prototype'), { target: { value: '{"polluted":true}' } });
    fireEvent.change(screen.getByLabelText('Constructor'), { target: { value: 'null' } });
    const asset = { asset: 'not-in-registry', pack: 'unknown-owner', nested: [null, false, { foreign: 16 }] };
    fireEvent.change(screen.getByLabelText('Asset'), { target: { value: JSON.stringify(asset) } });
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    await act(async () => { await f.session.flush(); });
    const values = f.env.commits()[0].body!.commands[0].args.values as Record<string, unknown>;
    expect(Object.hasOwn(values, '__proto__')).toBe(true);
    expect(values.__proto__).toEqual({ polluted: true });
    expect(Object.hasOwn(values, 'constructor')).toBe(true);
    expect(values.constructor).toBe(null);
    expect(values.asset).toEqual(asset);
    expect(Object.prototype).not.toHaveProperty('polluted');
    expect(f.dataRef.current.config.clips[0].params.opaque).toEqual([null, false]);
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('shows absent prototype-looking parameters as absent rather than inherited object properties', async () => {
    await setup(JSON.parse('{"__proto__":{"title":"Prototype"}}'));
    expect(screen.getByLabelText('Prototype accepted value').textContent).toBe('absent');
    expect(screen.getByLabelText('Prototype')).toHaveValue('');
  });

  it('keeps operational read error and raw16 intact across blur/refocus', async () => {
    const f = await setup();
    f.reads.getProjectVerifiedDocument.mockRejectedValueOnce(new Error('offline exact read'));
    f.edit('16'); f.apply();
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('offline exact read'));
    fireEvent.blur(screen.getByLabelText('Seed'));
    fireEvent.focus(screen.getByLabelText('Seed'));
    fireEvent.blur(screen.getByLabelText('Seed'));
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(screen.getByRole('alert').textContent).toContain('offline exact read');
    expect(f.env.commits()).toHaveLength(0);
  });
});


describe('independent SDK identity and cancellation checks', () => {
  it('refuses an ownerless projected alias without guessing its raw suffix', async () => {
    const f = await setup();
    f.dataRef.current.resolvedConfig.clips[0].id = 'occ:x';
    await expect(f.getOps().setClipParams!('occ:x', { values: { seed: 16 }, clear: [], schema_source: f.pin }))
      .rejects.toThrow('explicit raw ownership');
    expect(f.reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
    expect(f.env.commits()).toHaveLength(0);
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('refuses duplicate displayed clip ids without choosing the first', async () => {
    const f = await setup();
    f.dataRef.current.resolvedConfig.clips.push(structuredClone(f.dataRef.current.resolvedConfig.clips[0]));
    await expect(f.getOps().setClipParams!('x', { values: { seed: 16 }, clear: [], schema_source: f.pin }))
      .rejects.toThrow('unambiguous raw clip identity');
    expect(f.reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
    expect(f.env.commits()).toHaveLength(0);
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('does no capture/read/write work for an already-aborted SDK call', async () => {
    const f = await setup();
    const controller = new AbortController();
    controller.abort();
    await expect(f.getOps().setClipParams!('x', { values: { seed: 16 }, clear: [], schema_source: f.pin }, controller.signal))
      .rejects.toThrow();
    expect(f.reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
    expect(f.env.commits()).toHaveLength(0);
    expect(f.legacy).not.toHaveBeenCalled();
  });
});


describe('independent mounted outbox recovery check', () => {
  it('restores the submitted raw16 field along with the existing durable refusal state', async () => {
    const f = await setup();
    f.env.setFault('refused');
    f.edit('16'); f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    await act(async () => { await expect(f.session.flush()).rejects.toThrow(); });
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    const [saved] = await f.env.outboxes.list(scope);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ args: { values: { seed: 16 }, schema_source: f.pin } }] });
    f.view.unmount();
    await f.session.dispose();
    const reopened = await createTimelineCommandSession({ scope,
      initial: await f.env.provider.loadTimelineCommandBasis(scope.timelineId), outboxes: f.env.outboxes,
      loadLatest: () => f.env.provider.loadTimelineCommandBasis(scope.timelineId),
      send: (request, key) => f.env.provider.commitTimeline(request, key), paramReadClient: f.reads,
      preview: vi.fn(), project: vi.fn(), changed: vi.fn(),
    });
    sessions.push(reopened);
    await reopened.recover(saved.ownerId);
    expect(reopened.getState().status).toBe('error');
    expect((await f.env.outboxes.list(scope))[0].intents[0].payload).toMatchObject({ commands: [{ args: { values: { seed: 16 } } }] });
    function Recovered() {
      const ops = useTimelineOps({ dataRef: f.dataRef, commitData: f.legacy, clipParamsPort: reopened.clipParamsPort,
        createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [] });
      return <AstridElementParams clip={f.dataRef.current.resolvedConfig.clips[0]} registry={{}} onChange={f.legacy}
        retainedDocumentPin={f.pin} timelineOps={ops} commandState={reopened.getState()} />;
    }
    render(<Recovered />);
    expect(screen.getByRole('alert')).toBeTruthy();
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
  });
});


describe('submitted field identity and recovery boundaries', () => {
  it('preserves newer typing even when it returns to the submitted text before ACK', async () => {
    const f = await setup(), held = f.pause();
    f.edit('8'); f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    f.edit('9'); f.edit('8');
    held.resolve();
    await act(async () => { await f.session.flush(); });
    expect(screen.getByLabelText('Seed')).toHaveValue('8');
    expect(screen.getByRole('status', { name: 'Parameter command status' }).textContent).toContain('Draft parameters');
    const latest = await f.env.external((raw) => {
      for (const clips of [raw.parent_revision.payload.clips, raw.parent_revision.payload.config.clips]) clips[0].params.seed = 9;
    });
    act(() => { f.session.observe(latest); });
    await waitFor(() => expect(screen.getByLabelText('Seed accepted value').textContent).toBe('9'));
    expect(screen.getByLabelText('Seed')).toHaveValue('8');
    expect(f.env.commits()).toHaveLength(1);
  });

  it('retires only the accepted PARAM fields across an unrelated queued move', async () => {
    const f = await setup(), held = f.pause();
    f.edit('8'); f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    act(() => { f.env.move(f.session, 5); });
    await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
    held.resolve();
    await waitFor(() => expect(f.env.commits()).toHaveLength(2));
    await act(async () => { await f.session.flush(); });
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('8');
    expect(screen.getByRole('button', { name: 'Apply parameters' })).toBeDisabled();
    fireEvent.change(screen.getByLabelText('Text'), { target: { value: '"new"' } });
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(3));
    await act(async () => { await f.session.flush(); });
    expect(f.env.commits()[2].body!.commands[0].args).toEqual({ values: { text: 'new' }, clear: [], schema_source: f.pin });
  });

  it('rehydrates own empty/prototype/constructor values, null and clears without changing the durable input or request', async () => {
    const properties = JSON.parse('{"":{"title":"Empty"},"__proto__":{"title":"Prototype"},"constructor":{"title":"Constructor"}}');
    const f = await setup(properties);
    expect(screen.getByLabelText('Constructor accepted value').textContent).toBe('absent');
    f.edit('16');
    fireEvent.change(screen.getByLabelText('Empty'), { target: { value: '""' } });
    fireEvent.change(screen.getByLabelText('Prototype'), { target: { value: '{}' } });
    fireEvent.change(screen.getByLabelText('Constructor'), { target: { value: 'null' } });
    fireEvent.change(screen.getByLabelText('Text'), { target: { value: '' } });
    f.env.setFault('refused'); f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    await act(async () => { await expect(f.session.flush()).rejects.toThrow(); });
    const [saved] = await f.env.outboxes.list(scope);
    const original = JSON.stringify({ intents: saved.intents, pending: saved.pending });
    const reads = f.reads.getProjectVerifiedDocument.mock.calls.length;
    f.view.unmount();
    await f.session.dispose();
    const reopened = await createTimelineCommandSession({ scope,
      initial: await f.env.provider.loadTimelineCommandBasis(scope.timelineId), outboxes: f.env.outboxes,
      send: (request, key) => f.env.provider.commitTimeline(request, key), paramReadClient: f.reads,
      preview: vi.fn(), project: vi.fn(), changed: vi.fn(),
    });
    sessions.push(reopened);
    await reopened.recover(saved.ownerId);
    const snapshot = reopened.clipParamsPort.submittedInput!({ clipId: 'x', current: f.dataRef.current })!;
    expect(snapshot).toMatchObject({ accepted: false, args: { schema_source: f.pin },
      basis: (saved.intents[0].payload as unknown as { selectedParams: { basis: object } }).selectedParams.basis });
    expect(Object.isFrozen(snapshot.args.values)).toBe(true);
    function Recovered() {
      const ops = useTimelineOps({ dataRef: f.dataRef, commitData: f.legacy, clipParamsPort: reopened.clipParamsPort,
        createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [] });
      return <AstridElementParams clip={f.dataRef.current.resolvedConfig.clips[0]} registry={{}} onChange={f.legacy}
        retainedDocumentPin={{ ...f.pin, version: 2 }} timelineOps={ops} commandState={reopened.getState()} />;
    }
    render(<Recovered />);
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(screen.getByLabelText('Empty')).toHaveValue('""');
    expect(screen.getByLabelText('Prototype')).toHaveValue('{}');
    expect(screen.getByLabelText('Constructor')).toHaveValue('null');
    expect(screen.getByLabelText('Text')).toHaveValue('');
    f.apply();
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('pin changed'));
    const [recovered] = await f.env.outboxes.list(scope);
    expect(JSON.stringify({ intents: recovered.intents, pending: recovered.pending })).toBe(original);
    expect(f.reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(reads);
    expect(f.env.commits()).toHaveLength(1);
    expect(f.legacy).not.toHaveBeenCalled();
  });
});
