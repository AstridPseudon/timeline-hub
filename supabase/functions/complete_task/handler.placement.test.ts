import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { completeTaskHandler } from './handler.ts';

const mocks = vi.hoisted(() => ({
  bootstrap: vi.fn(),
  parseRequest: vi.fn(),
  resolveActor: vi.fn(),
  storage: vi.fn(),
  cleanupFile: vi.fn(),
  billing: vi.fn(),
  orchestrator: vi.fn(),
  fetch: vi.fn(),
}));

vi.mock('../_shared/edgeHandler.ts', () => ({
  bootstrapEdgeHandler: mocks.bootstrap,
  NO_SESSION_RUNTIME_OPTIONS: {},
}));
vi.mock('../_shared/taskActorPolicy.ts', () => ({ resolveTaskStorageActor: mocks.resolveActor }));
vi.mock('../_shared/rateLimit.ts', () => ({
  enforceRateLimit: vi.fn().mockResolvedValue(null),
  RATE_LIMITS: { userAction: {} },
}));
vi.mock('./request.ts', () => ({
  parseCompleteTaskRequest: mocks.parseRequest,
  validateStoragePathSecurity: vi.fn(),
}));
vi.mock('./storage.ts', () => ({
  handleStorageOperations: mocks.storage,
  cleanupFile: mocks.cleanupFile,
  getStoragePublicUrl: vi.fn(),
}));
vi.mock('./billing.ts', () => ({ triggerCostCalculationIfNotSubTask: mocks.billing }));
vi.mock('./orchestrator.ts', () => ({ checkOrchestratorCompletion: mocks.orchestrator }));

const shotId = '11111111-1111-4111-8111-111111111111';
const publicUrl = 'https://cdn.example.com/out.png';
const thumbnailUrl = 'https://cdn.example.com/thumb.png';
const timelinePlacement = {
  timeline_id: 'timeline-1',
  source_clip_id: 'clip-1',
  target_track: 'V1',
  insertion_time: 12.5,
  intent: 'after_source',
};
const placementIntent = {
  timeline_id: 'timeline-1',
  anchor_clip_id: 'clip-1',
  relation: 'after',
  preferred_track_id: 'V1',
  fallback_track_id: 'V1',
  fallback_at: 12.5,
};

function setup(params: Record<string, unknown>) {
  const task = {
    id: 'task-1',
    project_id: 'project-1',
    task_type: 'single_image',
    params: { shot_id: shotId, add_in_position: true, ...params },
    result_data: { retained: true },
    materialized_inputs: [{ generation_id: 'input-1', kind: 'remote', target: 'inputs/source.png' }],
    task_types: { tool_type: 'wan', content_type: 'image', category: 'image', variant_type: null },
  };
  let generation: { id: string } | null = null;
  const updates: Record<string, unknown>[] = [];
  const variants: Record<string, unknown>[] = [];
  const taskQuery = {
    select: vi.fn().mockReturnThis(),
    eq: vi.fn().mockReturnThis(),
    single: vi.fn().mockResolvedValue({ data: task, error: null }),
    update: vi.fn((values: Record<string, unknown>) => {
      updates.push(values);
      return taskQuery;
    }),
    then: (resolve: (result: { error: null }) => unknown) => Promise.resolve({ error: null }).then(resolve),
  };
  const generationInsert = vi.fn((record: Record<string, unknown>) => {
    generation = { id: record.id as string };
    return { select: () => ({ single: async () => ({ data: generation, error: null }) }) };
  });
  const rpc = vi.fn((name: string) => {
    if (name !== 'add_generation_to_shot') throw new Error(`Forbidden canonical RPC: ${name}`);
    return Promise.resolve({ error: null });
  });
  const from = vi.fn((table: string) => {
    if (table === 'tasks') return taskQuery;
    if (table === 'generations') {
      return {
        data: generation ? [generation] : [],
        error: null,
        contains: vi.fn().mockReturnThis(),
        order: vi.fn().mockReturnThis(),
        limit: vi.fn().mockReturnThis(),
        select: vi.fn().mockReturnThis(),
        insert: generationInsert,
      };
    }
    if (table === 'generation_variants') {
      return {
        insert: (record: Record<string, unknown>) => {
          variants.push(record);
          return { select: () => ({ single: async () => ({ data: { id: 'variant-1' }, error: null }) }) };
        },
      };
    }
    if (table === 'shots') {
      return {
        select: () => ({ eq: () => ({ single: async () => ({ data: { id: shotId }, error: null }) }) }),
      };
    }
    throw new Error(`Forbidden canonical table/config update: ${table}`);
  });
  const supabaseAdmin = { from, rpc };
  mocks.bootstrap.mockResolvedValue({
    ok: true,
    value: {
      supabaseAdmin,
      auth: { isServiceRole: true, userId: null },
      logger: {
        info: vi.fn(), warn: vi.fn(), error: vi.fn(), critical: vi.fn(), debug: vi.fn(),
        flush: vi.fn(), setDefaultTaskId: vi.fn(),
      },
    },
  });
  return { task, updates, variants, from, rpc, taskQuery, generationInsert, supabaseAdmin };
}

function complete() {
  return completeTaskHandler(new Request('https://edge.test/complete-task', { method: 'POST' }));
}

describe('complete_task retained relational placement', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.stubGlobal('Deno', { env: { get: () => undefined } });
    // Any append/Runtime publication must fail even if a follow-up catches the error.
    mocks.fetch.mockImplementation(() => { throw new Error('Forbidden canonical append/Runtime request'); });
    vi.stubGlobal('fetch', mocks.fetch);
    mocks.parseRequest.mockResolvedValue({
      success: true,
      data: { taskId: 'task-1', filename: 'out.png', mode: 'upload', storagePath: null, requiresOrchestratorCheck: false },
    });
    mocks.resolveActor.mockResolvedValue({
      ok: true,
      value: { isServiceRole: true, taskOwnerVerified: true, callerId: null, taskUserId: 'user-1' },
    });
    mocks.storage.mockResolvedValue({ publicUrl, thumbnailUrl, objectPath: 'output/out.png' });
    mocks.billing.mockResolvedValue({ ok: true });
    mocks.orchestrator.mockResolvedValue(undefined);
  });

  afterEach(() => {
    expect(mocks.fetch).not.toHaveBeenCalled();
    vi.unstubAllGlobals();
  });

  it.each([
    { timeline_placement: timelinePlacement },
    { placement_intent: placementIntent },
    { timeline_placement: timelinePlacement, placement_intent: placementIntent },
  ])('completes media, billing and shot linking without publishing for %j', async (params) => {
    const db = setup(params);
    const response = await complete();
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body).toMatchObject({
      success: true,
      public_url: publicUrl,
      thumbnail_url: thumbnailUrl,
      follow_up: {
        status: 'degraded',
        issues: [{
          step: 'timeline_placement',
          code: 'automatic_timeline_placement_retired',
          message: 'Task output was saved; automatic timeline placement is no longer supported.',
        }],
      },
    });
    expect(body).not.toHaveProperty('clip_id');
    expect(body).not.toHaveProperty('config_version');
    expect(mocks.storage).toHaveBeenCalledWith(db.supabaseAdmin, expect.anything(), 'user-1', true);
    expect(db.generationInsert).toHaveBeenCalledOnce();
    const generationId = db.generationInsert.mock.calls[0][0].id;
    expect(db.variants).toEqual([expect.objectContaining({
      generation_id: generationId, location: publicUrl, thumbnail_url: thumbnailUrl,
      params: expect.objectContaining({ ...params, source_task_id: 'task-1', created_from: 'generation_original' }),
    })]);
    expect(db.rpc.mock.calls).toEqual([['add_generation_to_shot', {
      p_shot_id: shotId, p_generation_id: generationId, p_with_position: true,
    }]]);
    expect(db.from).not.toHaveBeenCalledWith('timelines');
    expect(db.updates).toContainEqual(expect.objectContaining({ status: 'Complete', output_location: publicUrl }));
    expect(db.taskQuery.eq).toHaveBeenCalledWith('status', 'In Progress');
    expect(db.updates).toContainEqual(expect.objectContaining({
      result_data: { retained: true, completion_follow_up: expect.objectContaining({ issues: body.follow_up.issues }) },
    }));
    expect(mocks.cleanupFile).toHaveBeenCalledWith(db.supabaseAdmin, 'inputs/source.png');
    expect(mocks.orchestrator).toHaveBeenCalledOnce();
    expect(mocks.billing).toHaveBeenCalledOnce();
  });

  it('retains the existing regeneration route on retry without a second generation or canonical write', async () => {
    const db = setup({ placement_intent: placementIntent });
    expect((await complete()).status).toBe(200);
    expect((await complete()).status).toBe(200);

    expect(db.generationInsert).toHaveBeenCalledOnce();
    expect(db.variants).toHaveLength(2);
    expect(db.variants[1]).toMatchObject({ variant_type: 'regenerated', location: publicUrl });
    expect(db.rpc).toHaveBeenCalledTimes(2);
    expect(db.rpc.mock.calls.every(([name]) => name === 'add_generation_to_shot')).toBe(true);
    expect(db.from).not.toHaveBeenCalledWith('timelines');
  });
});
