// @vitest-environment jsdom
import { useState } from 'react';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { ClipSetParamsArgs, DocumentPin, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import type { WorkspaceClient } from '@/integrations/runtime/generated.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { document, environment, scope } from '../../commands/__tests__/commitSessionEnvironment.ts';
import { createTimelineCommandSession, type CommandSessionState } from '../../commands/commitSession.ts';
import { buildTimelineData, type TimelineData } from '../../lib/timeline-data.ts';
import { compileTimelinePatch } from '../../lib/timeline-patch.ts';
import { useTimelineOps } from '../../hooks/useTimelineOps.ts';
import type { AstridElementDescriptor } from '../../runtime/astrid-element-host.ts';
import { AstridElementParams } from './AstridElementParams.tsx';

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

async function setup() {
  const reference = { packId: 'test_pack', id: 'reveal', kind: 'effect' as const, revision: `sha256:${'1'.repeat(64)}` };
  host.descriptors = [{ ...reference, componentPath: 'fixture', schema: {
    properties: { seed: { type: 'number', title: 'Seed', maximum: 10 }, text: { type: 'string', title: 'Text' } },
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

describe('selected PARAM actual controlled form -> TimelineOps -> command session', () => {
  it('keeps the accepted 4 visible while 8 is pending, then projects 8 and preserves a newer input draft', async () => {
    const f = await setup(), held = f.pause();
    f.edit('8');
    expect(screen.getByRole('status', { name: 'Parameter command status' }).textContent).toContain('Draft parameters');
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    expect(screen.getByRole('status', { name: 'Parameter command status' }).textContent).toContain('PENDING');
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    f.edit('9');
    held.resolve();
    await act(async () => { await f.session.flush(); });
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('8');
    expect(screen.getByLabelText('Seed')).toHaveValue('9');
    expect(screen.getByRole('status', { name: 'Parameter command status' }).textContent).toContain('Draft parameters');
    expect(f.dataRef.current.config.clips[0].params).toEqual({ seed: 8, text: 'original', opaque: [null, false] });
    expect(f.env.commits()[0].body).toMatchObject({ base_revision_id: 'r0', commands: [{ op: 'clip.set-params',
      select: 'parent/clip:x', args: { values: { seed: 8 }, clear: [], schema_source: f.pin } }] });
    const [saved] = await f.env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(0);
    expect(f.reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(1);
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it.each(['refused', 'validation', 'conflict'] as const)('sends raw16 under V1 despite V2 hints, retaining the draft on %s', async (fault) => {
    const f = await setup(), held = f.pause();
    host.descriptors[0] = { ...host.descriptors[0], schema: { properties: { seed: { type: 'number', title: 'Seed', maximum: 20 } } } };
    f.view.rerender(<f.Harness />);
    f.env.setFault(fault);
    f.edit('16');
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    expect(f.env.commits()[0].body!.commands[0].args).toEqual({ values: { seed: 16 }, clear: [], schema_source: f.pin });
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    held.resolve();
    await act(async () => { await expect(f.session.flush()).rejects.toThrow(); });
    expect(screen.getByRole('alert')).toBeTruthy();
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    const [saved] = await f.env.outboxes.list(scope);
    expect(saved.intents[0].payload).toMatchObject({ after: null, commands: [{ args: { values: { seed: 16 }, schema_source: f.pin } }],
      selectedParams: { basis: { acceptedBasisAvailable: true }, schema_inputs: [[expect.anything(), expect.anything()]] } });
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('keeps invalid JSON visible and accepts a corrected literal with explicit clear through the same controls', async () => {
    const f = await setup();
    f.edit('[');
    f.apply();
    await waitFor(() => expect(screen.getByRole('alert')).toBeTruthy());
    expect(screen.getByLabelText('Seed')).toHaveValue('[');
    expect(f.env.commits()).toHaveLength(0);
    f.edit('8');
    fireEvent.change(screen.getByLabelText('Text'), { target: { value: '' } });
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    await act(async () => { await f.session.flush(); });
    expect(f.env.commits()[0].body!.commands[0].args).toEqual({ values: { seed: 8 }, clear: ['text'], schema_source: f.pin });
    expect(screen.getByLabelText('Text accepted value').textContent).toBe('absent');
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('refuses a changed retained pin without losing the raw draft', async () => {
    const f = await setup();
    f.edit('16');
    f.view.rerender(<f.Harness retainedPin={{ ...f.pin, version: 2 }} />);
    f.apply();
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('pin changed'));
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(f.env.commits()).toHaveLength(0);
    expect(f.reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
  });

  it('retains V1 controls and the input draft when live pack hints are removed', async () => {
    const f = await setup(), held = f.pause();
    f.edit('8');
    host.descriptors = [];
    f.view.rerender(<f.Harness />);
    expect(screen.getByLabelText('Seed')).toHaveValue('8');
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    expect(f.env.commits()[0].body!.commands[0].args.schema_source).toEqual(f.pin);
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    held.resolve();
    await act(async () => { await f.session.flush(); });
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('8');
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('keeps the input draft on an operational retained-read error and permits a corrected retry', async () => {
    const f = await setup();
    f.reads.getProjectVerifiedDocument.mockRejectedValueOnce(new Error('retained read unavailable'));
    f.edit('8');
    f.apply();
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('retained read unavailable'));
    expect(screen.getByLabelText('Seed')).toHaveValue('8');
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    expect(f.env.commits()).toHaveLength(0);
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    await act(async () => { await f.session.flush(); });
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('8');
  });

  it.each([
    { values: [], clear: [] },
    { values: { seed: Infinity }, clear: [] },
    { values: { seed: 8 }, clear: ['seed'] },
    { values: { seed: 8 }, clear: [], extra: 'invented' },
  ])('rejects structural SDK command input before retained reads: %j', async (input) => {
    const f = await setup();
    await expect(f.getOps().setClipParams!('x', { ...input, schema_source: f.pin } as ClipSetParamsArgs)).rejects.toThrow();
    expect(f.env.commits()).toHaveLength(0);
    expect(f.reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('preserves the draft when its captured basis changes during retained reads', async () => {
    const f = await setup();
    let release!: () => void;
    const read = new Promise<void>((resolve) => { release = resolve; });
    releases.push(release);
    const original = f.reads.getProjectVerifiedDocument.getMockImplementation()!;
    f.reads.getProjectVerifiedDocument.mockImplementation(async (...args) => { await read; return original(...args); });
    f.edit('16');
    f.apply();
    await waitFor(() => expect(f.reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(1));
    const held = f.pause();
    act(() => { f.env.move(f.session, 5); });
    await act(async () => { release(); await read; });
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('capture changed'));
    expect(screen.getByLabelText('Seed')).toHaveValue('16');
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    held.resolve();
    await act(async () => { await f.session.flush(); });
    expect(f.env.commits().map((call) => call.body!.commands[0].op)).toEqual(['clip.move']);
  });

  it('cancels an unfinished retained read when the form closes', async () => {
    const f = await setup();
    let release!: () => void;
    const read = new Promise<void>((resolve) => { release = resolve; });
    releases.push(release);
    const original = f.reads.getProjectVerifiedDocument.getMockImplementation()!;
    f.reads.getProjectVerifiedDocument.mockImplementation(async (...args) => { await read; return original(...args); });
    f.edit('8');
    f.apply();
    await waitFor(() => expect(f.reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(1));
    f.view.unmount();
    await act(async () => { release(); await read; });
    await waitFor(() => expect(f.reads.getProjectVerifiedDocumentObject).toHaveBeenCalledTimes(1));
    expect(f.env.commits()).toHaveLength(0);
    expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(0);
  });

  it('retains an originally dirty basis as unsent after the ordinary predecessor ACK', async () => {
    const f = await setup(), held = f.pause();
    act(() => { f.env.move(f.session, 5); });
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    f.edit('8');
    f.apply();
    await waitFor(async () => expect((await f.env.outboxes.list(scope))[0].intents).toHaveLength(2));
    held.resolve();
    await act(async () => { await expect(f.session.flush()).rejects.toThrow('PENDING an accepted original basis'); });
    expect(screen.getByRole('status', { name: 'Parameter command status' }).textContent).toContain('PENDING an accepted original basis');
    expect(screen.getByLabelText('Seed')).toHaveValue('8');
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('4');
    const [saved] = await f.env.outboxes.list(scope);
    expect(saved.intents[0].payload).toMatchObject({ selectedParams: { basis: { acceptedBasisAvailable: false } } });
    expect(f.env.commits()).toHaveLength(1);
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('preserves native args and the original pin across asynchronous SDK input reads', async () => {
    const f = await setup(), held = f.pause();
    const args: ClipSetParamsArgs = { values: { seed: 16, expression: 'ƒ(16)' }, clear: [], schema_source: structuredClone(f.pin) };
    let submitted!: Promise<void>;
    act(() => { submitted = f.getOps().setClipParams!('x', args); });
    args.values.seed = 8;
    args.schema_source!.version = 2;
    await act(async () => { await submitted; });
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    expect(f.env.commits()[0].body!.commands[0].args).toEqual({ values: { seed: 16, expression: 'ƒ(16)' }, clear: [], schema_source: f.pin });
    held.resolve();
    await act(async () => { await f.session.flush(); });
    expect(f.legacy).not.toHaveBeenCalled();
  });

  it('clears accepted draft fields so a later unrelated parameter edit cannot resend stale values', async () => {
    const f = await setup();
    f.edit('8');
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(1));
    await act(async () => { await f.session.flush(); });
    const latest = await f.env.external((raw) => {
      for (const clips of [raw.parent_revision.payload.clips, raw.parent_revision.payload.config.clips]) clips[0].params.seed = 9;
    });
    act(() => { f.session.observe(latest); });
    await waitFor(() => expect(screen.getByLabelText('Seed')).toHaveValue('9'));
    fireEvent.change(screen.getByLabelText('Text'), { target: { value: '"new text"' } });
    f.apply();
    await waitFor(() => expect(f.env.commits()).toHaveLength(2));
    await act(async () => { await f.session.flush(); });
    expect(f.env.commits()[1].body!.commands[0].args).toEqual({ values: { text: 'new text' }, clear: [], schema_source: f.pin });
    expect(screen.getByLabelText('Seed accepted value').textContent).toBe('9');
    expect(f.legacy).not.toHaveBeenCalled();
  });
});
