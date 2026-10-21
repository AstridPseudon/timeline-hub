import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { AstridLocalClient } from '@/integrations/astrid/client.ts';
import type { BatchImageGenerationTaskParams } from '@/shared/types/imageGeneration';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { createCommitOutbox, type ClaimedOutbox } from '../commands/commitOutbox.ts';
import { createTimelineCommandSession } from '../commands/commitSession.ts';
import { IMAGE_PLACEMENT_UNAVAILABLE } from '../commands/editorImagePlacement.ts';
import fixture from '../commands/fixtures/authoringBundle.json';
import { EditorImageGeneration } from './EditorImageGeneration.tsx';

let projectId = 'project-main';
let generate: (params: BatchImageGenerationTaskParams) => Promise<string[]>;
vi.mock('@/shared/hooks/useModal', () => ({ useExtraLargeModal: () => ({}) }));
vi.mock('@/shared/components/ImageGenerationForm', () => ({
  ImageGenerationForm: (props: { onGenerate: typeof generate }) => { generate = props.onGenerate; return null; },
}));
vi.mock('@/shared/hooks/settings/useApiKeys', () => ({ useApiKeys: () => ({ getApiKey: vi.fn() }) }));
vi.mock('@/shared/contexts/ProjectContext', () => ({ useProjectSelectionContext: () => ({ selectedProjectId: projectId }) }));
vi.mock('@/shared/hooks/tasks/useTaskPlaceholder', () => ({
  useTaskPlaceholder: () => async ({ create }: { create(): Promise<unknown> }) => {
    try { return await create(); } catch { return undefined; }
  },
}));
vi.mock('@/shared/components/ui/runtime/sonner', () => ({ toast: { error: vi.fn() } }));
vi.mock('@/shared/lib/errorHandling/runtimeError', () => ({ normalizeAndPresentAndRethrow: (error: unknown) => { throw error; } }));

const digest = `sha256:${'a'.repeat(64)}`;
const params: BatchImageGenerationTaskParams = {
  project_id: 'project-main', prompts: [{ id: 'prompt', fullPrompt: 'a lighthouse' }],
  imagesPerPrompt: 1, model_name: 'z-image', execution: 'cloud', resolution: '1024x1024',
};
const target = { ownerRef: 'occurrence:occ-0', lane: 'picture', anchor: null };
const scope = { projectId: 'project-main', timelineId: 'timeline-main', realmId: 'realm', actorId: 'actor' };
const document = fixture.cases.find((item) => item.name === 'trimmed-child')!.document as unknown as CanonicalDocument;
const basis = { canonicalDocument: document, head: { revisionId: document.parent_revision.revision_id, publicationId: 'publication' } };
const sessions: Awaited<ReturnType<typeof createTimelineCommandSession>>[] = [];
let posts: { body: string; key: string }[];
let composed: number;
let wrongTaskKey: boolean;
let beforePost: (() => Promise<void>) | undefined;
let fetchMock: ReturnType<typeof vi.fn>;

function admission(spec: Record<string, unknown>) {
  return { project: scope.projectId, capability_id: 'generation.generate_image', capability_digest: digest,
    schema_version: '1', input_object_ids: [], spec: { family: 'generation.generate_image', params: spec, output_policy: {} },
    storage_estimate: { scratch_bytes: 1, output_bytes: 1 },
    generation_intent: { version: 1, modality: 'image', opaque: { keep: null } },
    settlement_effect: { effect_type: 'generation.publish_v1', target_id: scope.projectId, payload: {
      version: 1, modality: 'image', generation_type: 'image', metadata: {}, partial_success_policy: 'reject',
      groups: [{ group_key: 'main', selectors: [{ selector: 'main-0', ordinal: 0, variant_key: 'original', output_port: 'generated_images' }] }],
    } },
  };
}
function reply(value: unknown) { return new Response(JSON.stringify(value), { status: 200, headers: { 'Content-Type': 'application/json' } }); }
async function environment(available = true) {
  let box!: ClaimedOutbox;
  let current = true;
  const real = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (_name, work) => work() });
  const storage = { ...real, create: (async (ownerScope, work) => real.create(ownerScope, (claimed, owner) => {
    box = claimed; return work(claimed, owner);
  })) as typeof real.create };
  const host = { client: new AstridLocalClient({ projectSlug: scope.projectId }), isCurrentIdentity: () => current };
  async function mount() {
    const session = await createTimelineCommandSession({ scope, initial: basis, outboxes: storage,
      ...(available ? { imagePlacementHost: host } : {}), changed: vi.fn(), preview: vi.fn(), project: vi.fn(),
      send: vi.fn(() => { throw new Error('No timeline commit expected'); }),
    });
    sessions.push(session);
    return session;
  }
  const session = await mount();
  return { session, mount, storage, box: () => box, invalidate: () => { current = false; } };
}
function editor(session: Awaited<ReturnType<typeof createTimelineCommandSession>>) {
  const view = render(<QueryClientProvider client={new QueryClient()}><MemoryRouter>
    <EditorImageGeneration placement={session.imageGeneration} />
  </MemoryRouter></QueryClientProvider>);
  fireEvent.click(screen.getByRole('button', { name: 'Generate image' }));
  return view;
}
function approve() {
  fireEvent.click(screen.getByRole('checkbox', { name: /Add the generated image/ }));
  fireEvent.change(screen.getByLabelText('Raw occurrence reference'), { target: { value: target.ownerRef } });
  fireEvent.change(screen.getByLabelText('Raw lane ID'), { target: { value: target.lane } });
}
beforeEach(() => {
  projectId = scope.projectId; posts = []; composed = 0; wrongTaskKey = false; beforePost = undefined;
  fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = new URL(String(input), 'http://fixture.test');
    if (url.pathname.endsWith('/generation/compose')) {
      composed++;
      return reply(admission(JSON.parse(String(init?.body)).params));
    }
    if (url.pathname.endsWith('/v1/capabilities')) return reply({ items: [{ capability_id: 'generation.generate_image', definition_digest: digest,
      status: 'ready', required_resource_keys: [], estimated_scratch_bytes: 1, estimated_output_bytes: 1 }], next_cursor: null });
    if (url.pathname.endsWith('/v1/tasks') && init?.method === 'POST') {
      await beforePost?.();
      const body = String(init.body), key = (init.headers as Record<string, string>)['Idempotency-Key'];
      posts.push({ body, key });
      const data = { task_id: 'task', run_id: 'run', project_id: scope.projectId, state: 'queued', version: 1,
        capability_id: 'generation.generate_image', capability_digest: digest, schema_version: '1', input_object_ids: [],
        spec: {}, idempotency_key: wrongTaskKey ? 'unrelated-key' : key, created_at: '2026-10-20', updated_at: '2026-10-20', attempt_id: null, runtime_epoch: 1 };
      return reply({ data, receipt: { receipt_id: 'receipt', command_kind: 'task.create', idempotency_key: key,
        request_hash: digest, project_id: scope.projectId, project_seq: [1, 1], event_ids: ['1'], result: {}, created_at: '2026-10-20' } });
    }
    throw new Error(`Unexpected fixture request ${url.pathname}`);
  });
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(async () => { cleanup(); for (const session of sessions.splice(0)) await session.dispose(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe('editor-owned image generation preparation (in-process host fixture)', () => {
  it('shows the real unavailable gate and retains a checked draft without composing or posting', async () => {
    const env = await environment(false); editor(env.session); approve();
    expect(screen.getByRole('status')).toHaveTextContent(IMAGE_PLACEMENT_UNAVAILABLE);
    await act(async () => { await generate(params); });
    expect(screen.getByRole('alert')).toHaveTextContent('host/session binding is not qualified');
    expect(screen.getByLabelText('Raw occurrence reference')).toHaveValue(target.ownerRef);
    expect(fetchMock).not.toHaveBeenCalled();
    expect((await env.storage.list(scope))[0].placementContinuations).toBeUndefined();
  });

  it('ordinary unchecked generation still uses the real producer and reserves no approval', async () => {
    const env = await environment(false); editor(env.session);
    await act(async () => { await generate(params); });
    expect(posts).toHaveLength(1); expect(composed).toBe(1);
    expect((await env.storage.list(scope))[0].placementContinuations).toBeUndefined();
  });

  it('reserves final normalized bytes, key, raw target, basis, output and IDs before the task POST', async () => {
    const env = await environment(); editor(env.session); approve();
    beforePost = async () => {
      const [saved] = (await env.storage.list(scope))[0].placementContinuations!;
      expect(saved.input).toMatchObject({ autoApprove: true, head: basis.head, ownerRef: target.ownerRef, lane: target.lane, anchor: null,
        fallback: { at: null, track: target.lane }, readClosure: { head: basis.head, savedCanonicalDocument: document },
        policy: { owner: target.ownerRef, preferredTrack: target.lane, autoApprove: true },
        output: { group_key: 'main', variant_key: 'original', output_port: 'generated_images', ordinal: 0 } });
      expect(saved.input.createdIds).toEqual([(saved.input.policy as { clipId: string }).clipId]);
    };
    await act(async () => { await generate(params); });
    expect(posts).toHaveLength(1);
    const [saved] = (await env.storage.list(scope))[0].placementContinuations!;
    expect(posts[0]).toEqual({ body: saved.input.request.body, key: saved.input.request.key });
    expect(JSON.parse(posts[0].body).generation_intent.opaque).toEqual({ keep: null });
  });

  it('refuses an admission response for another task key and retains the reserved intent', async () => {
    const env = await environment(); editor(env.session); approve(); wrongTaskKey = true;
    await act(async () => { await generate(params); });
    expect(posts).toHaveLength(1);
    expect(screen.getByRole('alert')).toHaveTextContent('Task response differs from the reserved admission');
    const original = (await env.storage.list(scope))[0].placementContinuations![0];
    expect(original.input.request.key).toBe(posts[0].key);
    expect(original.taskLocator).toBeUndefined();
    expect(original.conflict).toBeUndefined();
  });

  it('a rejected durable reservation gives zero task POST and retains the form', async () => {
    const env = await environment(); editor(env.session); approve();
    vi.spyOn(env.box(), 'reservePlacementAdmission').mockRejectedValueOnce(new Error('reservation transaction aborted'));
    await act(async () => { await generate(params); });
    expect(posts).toEqual([]);
    expect(screen.getByRole('alert')).toHaveTextContent('reservation transaction aborted');
    expect(screen.getByRole('checkbox')).toBeChecked();
    expect((await env.storage.list(scope))[0].placementContinuations).toBeUndefined();
  });

  it('a delayed reservation produces zero task POST until durability completes', async () => {
    const env = await environment(); editor(env.session); approve();
    const reserve = env.box().reservePlacementAdmission.bind(env.box());
    let release!: () => void;
    const gate = new Promise<void>((resolve) => { release = resolve; });
    const spy = vi.spyOn(env.box(), 'reservePlacementAdmission').mockImplementation(async (...args) => { await gate; return reserve(...args); });
    let flight!: Promise<string[]>;
    act(() => { flight = generate(params); });
    await waitFor(() => expect(spy).toHaveBeenCalledOnce());
    expect(posts).toEqual([]);
    await act(async () => { release(); await flight; });
    expect(posts).toHaveLength(1);
  });

  it('refuses absent targets and multiple images before task submission', async () => {
    const env = await environment(); editor(env.session);
    fireEvent.click(screen.getByRole('checkbox'));
    await act(async () => { await generate(params); });
    expect(screen.getByRole('alert')).toHaveTextContent('explicit raw occurrence and lane');
    await act(async () => { await generate({ ...params, imagesPerPrompt: 2 }); });
    expect(screen.getByRole('alert')).toHaveTextContent('one prompt and one image');
    expect(posts).toEqual([]); expect(composed).toBe(0);
  });

  it('two owner reopenings reuse the exact task, approval and IDs without recomposition', async () => {
    const env = await environment(); editor(env.session); approve();
    await act(async () => { await generate(params); });
    const original = (await env.storage.list(scope))[0];
    const saved = original.placementContinuations![0];
    cleanup(); await env.session.dispose();
    for (let repeat = 0; repeat < 2; repeat++) {
      const reopened = await env.mount();
      expect(reopened.getState().status).toBe('recovery');
      await reopened.recover(original.ownerId);
      const allocate = vi.spyOn(crypto, 'randomUUID');
      const prepared = await reopened.imageGeneration.prepare(target);
      expect(prepared.reservation!.key).toBe(saved.input.request.key);
      expect(allocate).not.toHaveBeenCalled();
      allocate.mockRestore();
      editor(reopened); approve();
      await act(async () => { await generate(params); });
      expect((await env.storage.list(scope))[0].placementContinuations).toEqual([saved]);
      cleanup(); await reopened.dispose();
    }
    expect(composed).toBe(1);
    expect(posts).toEqual(Array(3).fill({ body: saved.input.request.body, key: saved.input.request.key }));
  });

  it('invalidating the host after durable reservation prevents task POST and retains the exact intent', async () => {
    const env = await environment(); editor(env.session); approve();
    const reserve = env.box().reservePlacementAdmission.bind(env.box());
    vi.spyOn(env.box(), 'reservePlacementAdmission').mockImplementation(async (...args) => {
      const saved = await reserve(...args); env.invalidate(); return saved;
    });
    await act(async () => { await generate(params); });
    expect(posts).toEqual([]);
    const saved = (await env.storage.list(scope))[0].placementContinuations![0];
    expect(saved.input.autoApprove).toBe(true);
    expect(saved.input.request.key).toBeTruthy();
    expect(screen.getByRole('alert')).toHaveTextContent('host/session binding');
    expect(saved.conflict).toBeUndefined();
  });

  it('changing a saved target or prompt refuses without rewriting its approval', async () => {
    const env = await environment(); editor(env.session); approve();
    await act(async () => { await generate(params); });
    const original = (await env.storage.list(scope))[0];
    fireEvent.change(screen.getByLabelText('Raw lane ID'), { target: { value: 'different-lane' } });
    await act(async () => { await generate(params); });
    expect(screen.getByRole('alert')).toHaveTextContent('Saved placement approval differs');
    fireEvent.change(screen.getByLabelText('Raw lane ID'), { target: { value: target.lane } });
    await act(async () => { await generate({ ...params, prompts: [{ id: 'prompt', fullPrompt: 'changed' }] }); });
    expect(screen.getByRole('alert')).toHaveTextContent('Saved placement task differs');
    expect(posts).toHaveLength(1); expect(composed).toBe(1);
    expect((await env.storage.list(scope))[0]).toEqual(original);
  });

  it('dirty predecessors refuse checked generation with no admission or inferred approval', async () => {
    const env = await environment(); editor(env.session); approve();
    await env.box().append({ commands: ['earlier guarded edit'] }, { head: basis.head });
    await act(async () => { await generate(params); });
    expect(screen.getByRole('alert')).toHaveTextContent('Acknowledge earlier timeline work');
    expect(posts).toEqual([]); expect(composed).toBe(0);
    expect((await env.storage.list(scope))[0].placementContinuations).toBeUndefined();
  });

  it('scope or lifecycle change refuses the original intent without rewriting it', async () => {
    const env = await environment(); const view = editor(env.session); approve();
    await act(async () => { await generate(params); });
    const original = (await env.storage.list(scope))[0];
    projectId = 'other-project'; view.rerender(<QueryClientProvider client={new QueryClient()}><MemoryRouter>
      <EditorImageGeneration placement={env.session.imageGeneration} />
    </MemoryRouter></QueryClientProvider>);
    await act(async () => { await generate(params); });
    expect(screen.getByRole('alert')).toHaveTextContent('original editor project changed');
    env.invalidate();
    await expect(env.session.imageGeneration.prepare(target)).rejects.toThrow('host/session binding');
    expect(posts).toHaveLength(1);
    expect((await env.storage.list(scope))[0]).toEqual(original);
  });
});

