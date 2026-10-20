import React from 'react';
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterAll, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';
import { AstridRuntimeClient, RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from '@/integrations/runtime/contract-metadata';
import { acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture';
import type { CanonicalDocument, ManagedOutput, MediaSelection, Task, Transport } from '@/integrations/runtime/generated';
import { MediaLightbox } from '@/domains/media-lightbox/MediaLightbox';
import fixture from './__fixtures__/runtimeRecoveryGeneration.json';
import { RuntimeRecoveryChooser, type RuntimeRecoveryChooserProps } from './RuntimeRecoveryChooser';
import { freezeRecoveryValue, loadRuntimeRecoveryDestinations, type RuntimeRecoverySource } from './utils/runtimeRecoveryDestinations';

const reads = vi.hoisted(() => ({ transport: vi.fn() }));
vi.mock('@/integrations/runtime/client', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/integrations/runtime/client')>();
  return { ...actual, AstridRuntimeClient: class extends actual.AstridRuntimeClient {
    constructor(options = {}) { super({ ...options, baseUrl: '/chooser-test', transport: reads.transport }); }
  } };
});
// Exercise MediaLightbox dispatch and its real custom overlay seam without
// unrelated media editing hooks. The destination selector itself is real.
vi.mock('@/domains/media-lightbox/ImageLightbox', () => ({ ImageLightbox: (props: { customOverlay?: React.ReactNode }) => <div>{props.customOverlay}</div> }));
vi.mock('@/domains/media-lightbox/VideoLightbox', () => ({ VideoLightbox: (props: { customOverlay?: React.ReactNode }) => <div>{props.customOverlay}</div> }));

const projectId = fixture.task.project_id;
const timelineId = 'explicit-selected-timeline';
let document: CanonicalDocument;
let task: Task;
let output: ManagedOutput;
let selection: MediaSelection;
let timeline: Record<string, unknown>;
let source: RuntimeRecoverySource;
let requests: { method: string; path: string }[];
let delayed: ((path: string) => Promise<void> | undefined) | undefined;
const callback = vi.fn();
const scrollIntoView = Object.getOwnPropertyDescriptor(Element.prototype, 'scrollIntoView');
beforeAll(() => {
  // cmdk calls the browser scroll API, which jsdom does not implement.
  Object.defineProperty(Element.prototype, 'scrollIntoView', { configurable: true, value: vi.fn() });
});
afterAll(() => {
  if (scrollIntoView) Object.defineProperty(Element.prototype, 'scrollIntoView', scrollIntoView);
  else Reflect.deleteProperty(Element.prototype, 'scrollIntoView');
});

const transport: Transport = async (method, path) => {
  requests.push({ method, path });
  await delayed?.(path);
  let body: unknown;
  if (path === '/v1/health') body = { status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_instance_id: 'chooser-instance' };
  else if (path === '/v1/handshake') body = { protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, actor_id: 'chooser-actor', realm_id: 'chooser-realm', scopes: RUNTIME_CLIENT_SCOPES, capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] };
  else if (path === '/v1/realm') body = { realm_id: 'chooser-realm' };
  else if (path.endsWith('/commits?limit=50')) body = { items: [], next_cursor: null, head: { revision_id: 'chosen-head', publication_id: 'chosen-publication' } };
  else if (path.includes('/composition-revisions/')) body = { project_id: projectId, timeline_id: timelineId, ...document.parent_revision, dependency_manifest: document.dependency_manifest };
  else if (path.includes('/shots/') && path.includes('/revisions/')) body = { project_id: projectId, ...document.shot_revisions[0] };
  else if (path.includes('/timelines/') && path.includes('/revisions/')) body = { project_id: projectId, ...document.internal_timeline_revisions[0] };
  else if (path.endsWith(`/timelines/${timelineId}`)) body = timeline;
  else if (path === `/v1/tasks/${fixture.task.task_id}`) body = task;
  else if (path.startsWith('/v1/managed-outputs/')) body = output;
  else if (path.includes('/media-selection?')) body = selection;
  else throw new Error(`Unexpected chooser request: ${method} ${path}`);
  return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(body)) };
};

beforeEach(() => {
  vi.clearAllMocks();
  task = structuredClone(fixture.task) as Task;
  output = structuredClone(fixture.outputs.items[0]) as ManagedOutput;
  selection = structuredClone(fixture.selection);
  source = freezeRecoveryValue(structuredClone({ task, output, mediaTuple: selection }));
  document = acceptedCommit({ revision_id: 'chosen-head', publication_id: 'chosen-publication' },
    { revision_id: 'base', publication_id: 'base-pub' }, { projectId, timelineId, children: true }).data.canonical_document;
  const occurrences = document.parent_revision.payload.occurrences as Record<string, unknown>[];
  occurrences[0].occurrence_id = 'raw occurrence A';
  occurrences[1].occurrence_id = 'raw occurrence B';
  document.internal_timeline_revisions[0].payload.tracks = [{ id: 'raw-child-track', label: 'Child picture', kind: 'visual' }];
  (document.internal_timeline_revisions[0].payload.clips as Record<string, unknown>[])[0].track = 'raw-child-track';
  timeline = { project_id: projectId, timeline_id: timelineId, head_revision_id: 'chosen-head', head_publication_id: 'chosen-publication' };
  requests = [];
  delayed = undefined;
  reads.transport.mockImplementation(transport);
  callback.mockResolvedValue(undefined);
});

function element(props: Partial<RuntimeRecoveryChooserProps> = {}, video = false) {
  return <MediaLightbox media={{ id: selection.generation_id, type: video ? 'video' : 'image', location: video ? 'clip.mp4' : 'image.png' }}
    onClose={vi.fn()} customOverlay={<RuntimeRecoveryChooser projectId={projectId} timelineId={timelineId} source={source} {...props} />} />;
}

async function choose() {
  await screen.findByText('Choose a destination and explicit timing.');
  fireEvent.click(screen.getByRole('combobox'));
  fireEvent.click(await screen.findByText(/Shared shot · raw occurrence B · Child picture$/));
  fireEvent.change(screen.getByLabelText('Timeline start (seconds)'), { target: { value: '3.25' } });
  fireEvent.change(screen.getByLabelText('Source from (seconds)'), { target: { value: '1' } });
  fireEvent.change(screen.getByLabelText('Source to (seconds)'), { target: { value: '2.5' } });
}

function gate() {
  let release!: () => void;
  const promise = new Promise<void>((resolve) => { release = resolve; });
  return { promise, release };
}

it.each(['edit', 'unmount'])('cancels a connected callback before capture on chooser %s', async (change) => {
  const pending = gate();
  callback.mockImplementation(() => pending.promise);
  const mounted = render(element({ onRequestPlacement: callback }));
  await choose();
  fireEvent.click(screen.getByRole('button', { name: 'Request placement' }));
  await waitFor(() => expect(callback).toHaveBeenCalledOnce());
  const signal = callback.mock.calls[0][1] as AbortSignal;
  expect(signal.aborted).toBe(false);
  if (change === 'unmount') mounted.unmount();
  else fireEvent.change(screen.getByLabelText('Timeline start (seconds)'), { target: { value: '4' } });
  expect(signal.aborted).toBe(true);
  await act(async () => { pending.release(); await pending.promise; });
});

describe('Runtime recovery destination reads', () => {
  it('uses the real provider and normal transport; raw child tracks stay distinct from parent lanes and shared shot IDs', async () => {
    const read = await loadRuntimeRecoveryDestinations(new RuntimeDataProvider({ projectId }), new AstridRuntimeClient(), projectId, timelineId);
    expect(read.bindings).toHaveLength(2);
    expect(read.bindings[1]).toMatchObject({ owner: { kind: 'occurrence', occurrenceId: 'raw occurrence B' }, shotId: 'shot-1',
      shotRevisionId: 'shot-r1', internalTimelineId: 'child-timeline', internalRevisionId: 'internal-r1', parentTrackId: 'V1', childTrackId: 'raw-child-track' });
    expect(read.bindings[0].id).not.toBe(read.bindings[1].id);
    expect(Object.isFrozen(read.basis.canonicalDocument)).toBe(true);
    expect(requests.filter(({ method, path }) => method !== 'GET' && path !== '/v1/handshake')).toEqual([]);
    expect(requests.some(({ path }) => path.includes('/composition-revisions/chosen-head'))).toBe(true);
    expect(requests.some(({ path }) => path.includes('/projects/') && !path.includes(encodeURIComponent(projectId)))).toBe(false);
  });

  it.each(['project', 'timeline', 'revision', 'publication', 'manifest', 'shot pin', 'internal pin', 'child tracks', 'parent lane', 'conflicting lane'])('fails closed on %s mismatch', async (kind) => {
    if (kind === 'project') timeline.project_id = 'foreign';
    if (kind === 'timeline') timeline.timeline_id = 'foreign';
    if (kind === 'revision') timeline.head_revision_id = 'new-head';
    if (kind === 'publication') timeline.head_publication_id = 'new-publication';
    if (kind === 'manifest') document.dependency_manifest.shots[0].content_digest = `sha256:${'f'.repeat(64)}`;
    if (kind === 'shot pin') document.shot_revisions[0].payload.internal_timeline_revision_id = 'foreign';
    if (kind === 'internal pin') document.internal_timeline_revisions[0].revision_id = 'foreign';
    if (kind === 'child tracks') delete document.internal_timeline_revisions[0].payload.tracks;
    if (kind === 'parent lane') document.parent_revision.payload.tracks = [];
    if (kind === 'conflicting lane') (document.parent_revision.payload.occurrences as Record<string, unknown>[])[0].track = 'foreign';
    await expect(loadRuntimeRecoveryDestinations(new RuntimeDataProvider({ projectId }), new AstridRuntimeClient(), projectId, timelineId)).rejects.toThrow();
  });

  it('has no fallback options when no child visual tracks are explicitly available', async () => {
    document.internal_timeline_revisions[0].payload.tracks = [{ id: 'audio', kind: 'audio' }];
    const read = await loadRuntimeRecoveryDestinations(new RuntimeDataProvider({ projectId }), new AstridRuntimeClient(), projectId, timelineId);
    expect(read.bindings).toEqual([]);
  });
});

describe('existing lightbox and ShotSelector recovery draft', () => {
  it.each([false, true])('retains a draft with no native callback and performs no placement for video=%s', async (video) => {
    render(element({}, video));
    await choose();
    expect(screen.getByText(/native command service is not connected/)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Request placement' })).not.toBeInTheDocument();
    expect(screen.getByLabelText('Timeline start (seconds)')).toHaveValue(3.25);
    expect(callback).not.toHaveBeenCalled();
    expect(requests.filter(({ method, path }) => method !== 'GET' && path !== '/v1/handshake')).toEqual([]);
  });

  it('captures exact frozen routing data for a supplied callback without claiming accepted placement', async () => {
    render(element({ onRequestPlacement: callback }));
    await screen.findByText('Choose a destination and explicit timing.');
    expect(screen.getByRole('button', { name: 'Request placement' })).toBeDisabled();
    await choose();
    // This capture qualifies routing data only; it is not a native placement.
    fireEvent.click(screen.getByRole('button', { name: 'Request placement' }));
    await waitFor(() => expect(callback).toHaveBeenCalledTimes(1));
    const draft = callback.mock.calls[0][0];
    expect(draft).toMatchObject({ projectId, timelineId, on: 3.25, sourceWindow: { from: 1, to: 2.5 },
      source: { mediaTuple: fixture.selection }, destination: { owner: { occurrenceId: 'raw occurrence B' }, childTrackId: 'raw-child-track' },
      basis: { head: { revisionId: 'chosen-head', publicationId: 'chosen-publication' } } });
    expect(Object.isFrozen(draft.source.mediaTuple)).toBe(true);
    expect(draft.source.mediaTuple.generation_id).not.toBe(output.object_id);
    expect(screen.queryByText(/success|placed successfully/i)).not.toBeInTheDocument();
    expect(screen.getByLabelText('Source to (seconds)')).toHaveValue(2.5);
  });

  it('keyboard selection of duplicate child labels retains the selected raw track binding', async () => {
    document.internal_timeline_revisions[0].payload.tracks = [
      { id: 'raw-child-track', label: 'Picture', kind: 'visual' },
      { id: 'alternate-child-track', label: 'Picture', kind: 'visual' },
    ];
    render(element({ onRequestPlacement: callback }));
    await screen.findByText('Choose a destination and explicit timing.');
    fireEvent.click(screen.getByRole('combobox'));
    const search = await screen.findByPlaceholderText('Search shots...');
    await waitFor(() => expect(screen.getAllByRole('option')[0]).toHaveAttribute('aria-selected', 'true'));
    fireEvent.keyDown(search, { key: 'ArrowDown' });
    fireEvent.keyDown(search, { key: 'Enter' });
    fireEvent.change(screen.getByLabelText('Timeline start (seconds)'), { target: { value: '0' } });
    fireEvent.change(screen.getByLabelText('Source from (seconds)'), { target: { value: '0' } });
    fireEvent.change(screen.getByLabelText('Source to (seconds)'), { target: { value: '1' } });
    fireEvent.click(screen.getByRole('button', { name: 'Request placement' }));
    await waitFor(() => expect(callback).toHaveBeenCalledTimes(1));
    expect(callback.mock.calls[0][0].destination.childTrackId).toBe('alternate-child-track');
  });

  it('keyboard selection of duplicate cross-occurrence names retains the selected raw occurrence binding', async () => {
    const occurrences = document.parent_revision.payload.occurrences as Record<string, unknown>[];
    occurrences[0].occurrence_id = 'Scene';
    occurrences[1].occurrence_id = 'Scene · Main';
    document.internal_timeline_revisions[0].payload.tracks = [
      { id: 'raw-child-track', label: 'Main · Detail', kind: 'visual' },
      { id: 'alternate-child-track', label: 'Detail', kind: 'visual' },
    ];
    render(element({ onRequestPlacement: callback }));
    await screen.findByText('Choose a destination and explicit timing.');
    fireEvent.click(screen.getByRole('combobox'));
    const options = await screen.findAllByRole('option');
    expect(options).toHaveLength(4);
    expect(options[0]).toHaveTextContent('Scene · Main · Detail');
    expect(options[3]).toHaveTextContent('Scene · Main · Detail');
    const search = await screen.findByPlaceholderText('Search shots...');
    await waitFor(() => expect(options[0]).toHaveAttribute('aria-selected', 'true'));
    fireEvent.keyDown(search, { key: 'End' });
    fireEvent.keyDown(search, { key: 'Enter' });
    fireEvent.change(screen.getByLabelText('Timeline start (seconds)'), { target: { value: '0' } });
    fireEvent.change(screen.getByLabelText('Source from (seconds)'), { target: { value: '0' } });
    fireEvent.change(screen.getByLabelText('Source to (seconds)'), { target: { value: '1' } });
    fireEvent.click(screen.getByRole('button', { name: 'Request placement' }));
    await waitFor(() => expect(callback).toHaveBeenCalledTimes(1));
    expect(callback.mock.calls[0][0].destination.owner.occurrenceId).toBe('Scene · Main');
    expect(callback.mock.calls[0][0].destination.childTrackId).toBe('alternate-child-track');
  });

  it.each([null, ''])('asks for explicit timeline selection without reading a default (%s)', async (missing) => {
    render(element({ timelineId: missing }));
    expect(await screen.findByText(/Select a Runtime project and timeline/)).toBeInTheDocument();
    expect(requests).toEqual([]);
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
  });

  it.each(['task', 'output', 'tuple', 'head', 'modern intent', 'callback'])('keeps the draft and refuses a changed %s', async (change) => {
    render(element({ onRequestPlacement: callback }));
    await choose();
    if (change === 'task') task.version++;
    if (change === 'output') output.version++;
    if (change === 'tuple') selection.variant_id = 'latest-variant';
    if (change === 'head') timeline.head_publication_id = 'new-publication';
    if (change === 'modern intent') task.generation_intent = { version: 1 };
    if (change === 'callback') callback.mockRejectedValue(new Error('native unavailable'));
    fireEvent.click(screen.getByRole('button', { name: 'Request placement' }));
    await screen.findByText('Placement unavailable or source changed. Selection draft kept.');
    expect(callback).toHaveBeenCalledTimes(change === 'callback' ? 1 : 0);
    expect(screen.getByLabelText('Source from (seconds)')).toHaveValue(1);
    expect(screen.getByRole('button', { name: 'Request placement' })).toBeDisabled();
  });

  it.each(['project', 'timeline', 'task', 'output', 'unmount', 'selection'])('cancels pending request reads on %s change', async (change) => {
    const rendered = render(element({ onRequestPlacement: callback }));
    await choose();
    const held = gate();
    delayed = (path) => path.startsWith('/v1/managed-outputs/') ? held.promise : undefined;
    const previous = requests.length;
    fireEvent.click(screen.getByRole('button', { name: 'Request placement' }));
    await waitFor(() => expect(requests.slice(previous).some(({ path }) => path.startsWith('/v1/managed-outputs/'))).toBe(true));
    if (change === 'unmount') rendered.unmount();
    else if (change === 'selection') fireEvent.change(screen.getByLabelText('Timeline start (seconds)'), { target: { value: '9' } });
    else if (change === 'task') rendered.rerender(element({ source: { ...source, task: { ...source.task, version: 100 } }, onRequestPlacement: callback }));
    else if (change === 'output') rendered.rerender(element({ source: { ...source, output: { ...source.output, version: 100 } }, onRequestPlacement: callback }));
    else rendered.rerender(element({ [change === 'project' ? 'projectId' : 'timelineId']: null, onRequestPlacement: callback }));
    await act(async () => { held.release(); });
    expect(callback).not.toHaveBeenCalled();
  });

  it('discards a pending initial destination read when the selected timeline changes', async () => {
    const held = gate();
    delayed = (path) => path.includes('/composition-revisions/') ? held.promise : undefined;
    const rendered = render(element());
    await waitFor(() => expect(requests.some(({ path }) => path.includes('/composition-revisions/'))).toBe(true));
    rendered.rerender(element({ timelineId: null }));
    await act(async () => { held.release(); });
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
    expect(screen.getByText(/Select a Runtime project and timeline/)).toBeInTheDocument();
  });
});
