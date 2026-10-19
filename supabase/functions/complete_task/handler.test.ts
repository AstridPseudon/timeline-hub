import { beforeEach, describe, expect, it, vi } from 'vitest';
import { completeTaskHandler } from './handler.ts';
import { CompletionError } from './errors.ts';

const mocks = vi.hoisted(() => ({
  bootstrapEdgeHandler: vi.fn(),
  enforceRateLimit: vi.fn(),
  parseCompleteTaskRequest: vi.fn(),
  validateStoragePathSecurity: vi.fn(),
  handleStorageOperations: vi.fn(),
  getStoragePublicUrl: vi.fn(),
  cleanupFile: vi.fn(),
  setThumbnailInParams: vi.fn((params: Record<string, unknown>) => params),
  createGenerationFromTask: vi.fn(),
  checkOrchestratorCompletion: vi.fn(),
  validateAndCleanupShotId: vi.fn(),
  triggerCostCalculationIfNotSubTask: vi.fn(),
  completeTaskErrorResponse: vi.fn((message: string, status: number, errorCode?: string, options?: { recoverable?: boolean }) =>
    new Response(JSON.stringify({ message, errorCode, recoverable: options?.recoverable }), {
      status,
      headers: { 'Content-Type': 'application/json' },
    }),
  ),
  fetchTaskContext: vi.fn(),
  markTaskFailed: vi.fn(),
  persistCompletionFollowUpIssues: vi.fn(),
  resolveTaskStorageActor: vi.fn(),
  toErrorMessage: vi.fn((error: unknown) => (error instanceof Error ? error.message : String(error))),
}));

vi.mock('../_shared/http.ts', () => ({
  jsonResponse: (body: unknown, status = 200) =>
    new Response(JSON.stringify(body), {
      status,
      headers: { 'Content-Type': 'application/json' },
    }),
}));

vi.mock('../_shared/rateLimit.ts', () => ({
  enforceRateLimit: (...args: unknown[]) => mocks.enforceRateLimit(...args),
  RATE_LIMITS: {
    userAction: { maxRequests: 100, windowSeconds: 60 },
  },
}));

vi.mock('../_shared/edgeHandler.ts', () => ({
  bootstrapEdgeHandler: (...args: unknown[]) => mocks.bootstrapEdgeHandler(...args),
  NO_SESSION_RUNTIME_OPTIONS: {},
}));

vi.mock('../_shared/errorMessage.ts', () => ({
  toErrorMessage: (...args: unknown[]) => mocks.toErrorMessage(...args),
}));

vi.mock('../_shared/taskActorPolicy.ts', () => ({
  resolveTaskStorageActor: (...args: unknown[]) => mocks.resolveTaskStorageActor(...args),
}));

vi.mock('./request.ts', () => ({
  parseCompleteTaskRequest: (...args: unknown[]) => mocks.parseCompleteTaskRequest(...args),
  validateStoragePathSecurity: (...args: unknown[]) => mocks.validateStoragePathSecurity(...args),
}));

vi.mock('./storage.ts', () => ({
  handleStorageOperations: (...args: unknown[]) => mocks.handleStorageOperations(...args),
  getStoragePublicUrl: (...args: unknown[]) => mocks.getStoragePublicUrl(...args),
  cleanupFile: (...args: unknown[]) => mocks.cleanupFile(...args),
}));

vi.mock('./params.ts', () => ({
  setThumbnailInParams: (...args: unknown[]) => mocks.setThumbnailInParams(...args),
}));

vi.mock('./generation.ts', () => ({
  createGenerationFromTask: (...args: unknown[]) => mocks.createGenerationFromTask(...args),
}));

vi.mock('./orchestrator.ts', () => ({
  checkOrchestratorCompletion: (...args: unknown[]) => mocks.checkOrchestratorCompletion(...args),
}));

vi.mock('./shotValidation.ts', () => ({
  validateAndCleanupShotId: (...args: unknown[]) => mocks.validateAndCleanupShotId(...args),
}));

vi.mock('./billing.ts', () => ({
  triggerCostCalculationIfNotSubTask: (...args: unknown[]) => mocks.triggerCostCalculationIfNotSubTask(...args),
}));

vi.mock('./completionHelpers.ts', () => ({
  completeTaskErrorResponse: (...args: unknown[]) => mocks.completeTaskErrorResponse(...args),
  fetchTaskContext: (...args: unknown[]) => mocks.fetchTaskContext(...args),
  markTaskFailed: (...args: unknown[]) => mocks.markTaskFailed(...args),
  persistCompletionFollowUpIssues: (...args: unknown[]) => mocks.persistCompletionFollowUpIssues(...args),
}));

function createLogger() {
  return {
    setDefaultTaskId: vi.fn(),
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn(),
    critical: vi.fn(),
    debug: vi.fn(),
    flush: vi.fn().mockResolvedValue(undefined),
  };
}

function createSupabaseAdmin() {
  const finalEq = vi.fn().mockResolvedValue({ error: null });
  const firstEq = vi.fn().mockReturnValue({ eq: finalEq });
  const update = vi.fn().mockReturnValue({ eq: firstEq });
  const rpc = vi.fn(() => { throw new Error('Unexpected canonical RPC'); });
  const from = vi.fn((table: string) => {
    if (table !== 'tasks') throw new Error(`Unexpected canonical table: ${table}`);
    return { update };
  });
  return { from, update, firstEq, finalEq, rpc };
}

describe('completeTaskHandler', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.stubGlobal('Deno', {
      env: {
        get: (key: string) => {
          if (key === 'SUPABASE_SERVICE_ROLE_KEY') return 'service-role-key';
          if (key === 'SUPABASE_URL') return 'https://example.supabase.co';
          return undefined;
        },
      },
    });

    mocks.enforceRateLimit.mockResolvedValue(null);
    mocks.parseCompleteTaskRequest.mockResolvedValue({
      success: true,
      data: {
        taskId: 'task-1',
        mode: 'upload',
        filename: 'out.png',
        requiresOrchestratorCheck: false,
        storagePath: null,
        storagePathTaskId: null,
      },
    });
    mocks.resolveTaskStorageActor.mockResolvedValue({
      ok: true,
      value: {
        isServiceRole: true,
        taskOwnerVerified: true,
        callerId: 'service-role',
        taskUserId: 'user-1',
      },
    });
    mocks.fetchTaskContext.mockResolvedValue({
      id: 'task-1',
      task_type: 'image_generation',
      project_id: 'project-1',
      params: {},
      result_data: {},
      tool_type: 'wan',
      category: 'image',
      content_type: 'image',
      variant_type: null,
    });
    mocks.handleStorageOperations.mockResolvedValue({
      publicUrl: 'https://cdn.example.com/tasks/task-1/out.png',
      objectPath: 'tasks/user-1/task-1/out.png',
      thumbnailUrl: null,
    });
    mocks.validateAndCleanupShotId.mockResolvedValue({
      needsUpdate: false,
      updatedParams: {},
    });
    mocks.createGenerationFromTask.mockResolvedValue({
      status: 'created',
      generation: { id: 'gen-1' },
      completionAsset: null,
    });
    mocks.checkOrchestratorCompletion.mockResolvedValue(undefined);
    mocks.triggerCostCalculationIfNotSubTask.mockResolvedValue({ ok: true });
    mocks.persistCompletionFollowUpIssues.mockResolvedValue({ ok: true });
  });

  it('returns bootstrap response when bootstrap fails', async () => {
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: false,
      response: new Response('blocked', { status: 401 }),
    });

    const response = await completeTaskHandler(
      new Request('https://edge.test/complete-task', { method: 'POST' }),
    );

    expect(response.status).toBe(401);
    await expect(response.text()).resolves.toBe('blocked');
  });

  it('returns parse failure response from request parser', async () => {
    const logger = createLogger();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: {
        supabaseAdmin: createSupabaseAdmin(),
        logger,
        auth: { userId: 'user-1', isServiceRole: false },
      },
    });

    mocks.parseCompleteTaskRequest.mockResolvedValue({
      success: false,
      response: new Response('invalid', { status: 400 }),
    });

    const response = await completeTaskHandler(
      new Request('https://edge.test/complete-task', { method: 'POST' }),
    );

    expect(response.status).toBe(400);
    await expect(response.text()).resolves.toBe('invalid');
  });

  it('completes task and returns success payload', async () => {
    const logger = createLogger();
    const supabaseAdmin = createSupabaseAdmin();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: {
        supabaseAdmin,
        logger,
        auth: { userId: null, isServiceRole: true },
      },
    });

    const response = await completeTaskHandler(
      new Request('https://edge.test/complete-task', { method: 'POST' }),
    );

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({
      success: true,
      public_url: 'https://cdn.example.com/tasks/task-1/out.png',
      thumbnail_url: null,
      follow_up: { status: 'ok', issues: [] },
      message: 'Task completed and file uploaded successfully',
    });

    expect(logger.setDefaultTaskId).toHaveBeenCalledWith('task-1');
    expect(mocks.resolveTaskStorageActor).toHaveBeenCalled();
    expect(mocks.fetchTaskContext).toHaveBeenCalled();
    expect(mocks.createGenerationFromTask).toHaveBeenCalled();
    expect(mocks.triggerCostCalculationIfNotSubTask).toHaveBeenCalledWith(
      supabaseAdmin, 'https://example.supabase.co', 'service-role-key', 'task-1',
    );
    expect(supabaseAdmin.from).toHaveBeenCalledWith('tasks');
    expect(logger.flush).toHaveBeenCalled();
  });

  it('preserves structured CompletionError details when generation creation fails', async () => {
    const logger = createLogger();
    const supabaseAdmin = createSupabaseAdmin();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: {
        supabaseAdmin,
        logger,
        auth: { userId: null, isServiceRole: true },
      },
    });
    mocks.createGenerationFromTask.mockRejectedValue(
      new CompletionError({
        code: 'generation_route_no_result',
        message: 'No generation route produced a result',
        context: 'createGenerationFromTask',
        recoverable: false,
        metadata: { task_id: 'task-1' },
      }),
    );

    const response = await completeTaskHandler(
      new Request('https://edge.test/complete-task', { method: 'POST' }),
    );

    expect(response.status).toBe(500);
    await expect(response.json()).resolves.toEqual({
      message: 'No generation route produced a result',
      errorCode: 'generation_route_no_result',
      recoverable: false,
    });
    expect(logger.error).toHaveBeenCalledWith('Generation creation failed', expect.objectContaining({
      error_code: 'generation_route_no_result',
      recoverable: false,
      error_context: 'createGenerationFromTask',
      error_metadata: { task_id: 'task-1' },
    }));
    expect(mocks.markTaskFailed).toHaveBeenCalledWith(
      supabaseAdmin,
      'task-1',
      'Generation creation failed [generation_route_no_result]: No generation route produced a result',
    );
    expect(mocks.completeTaskErrorResponse).toHaveBeenCalledWith(
      'No generation route produced a result',
      500,
      'generation_route_no_result',
      { recoverable: false },
    );
  });

  it('wraps plain generation failures with the generic internal server response', async () => {
    const logger = createLogger();
    const supabaseAdmin = createSupabaseAdmin();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: {
        supabaseAdmin,
        logger,
        auth: { userId: null, isServiceRole: true },
      },
    });
    mocks.createGenerationFromTask.mockRejectedValue(new Error('boom'));

    const response = await completeTaskHandler(
      new Request('https://edge.test/complete-task', { method: 'POST' }),
    );

    expect(response.status).toBe(500);
    await expect(response.json()).resolves.toEqual({
      message: 'Internal server error',
      errorCode: 'internal_server_error',
      recoverable: undefined,
    });
    expect(logger.error).toHaveBeenCalledWith('Generation creation failed', expect.objectContaining({
      error: 'boom',
      error_code: 'generation_completion_failed',
      recoverable: true,
    }));
    expect(mocks.markTaskFailed).toHaveBeenCalledWith(
      supabaseAdmin,
      'task-1',
      'Generation creation failed: boom',
    );
  });

  it('rejects missing actor authentication before parsing or preparing media', async () => {
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: { supabaseAdmin: createSupabaseAdmin(), logger: createLogger(), auth: null },
    });

    const response = await completeTaskHandler(new Request('https://edge.test/complete-task'));

    expect(response.status).toBe(401);
    expect(mocks.parseCompleteTaskRequest).not.toHaveBeenCalled();
    expect(mocks.handleStorageOperations).not.toHaveBeenCalled();
    expect(mocks.createGenerationFromTask).not.toHaveBeenCalled();
  });

  it.each([401, 403])('preserves actor policy rejection (%i) without completion effects', async (statusCode) => {
    const supabaseAdmin = createSupabaseAdmin();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: { supabaseAdmin, logger: createLogger(), auth: { userId: 'other-user', isServiceRole: false } },
    });
    mocks.resolveTaskStorageActor.mockResolvedValue({ ok: false, statusCode, error: 'Forbidden' });

    const response = await completeTaskHandler(new Request('https://edge.test/complete-task'));

    expect(response.status).toBe(statusCode);
    expect(mocks.handleStorageOperations).not.toHaveBeenCalled();
    expect(mocks.createGenerationFromTask).not.toHaveBeenCalled();
    expect(supabaseAdmin.update).not.toHaveBeenCalled();
    expect(mocks.triggerCostCalculationIfNotSubTask).not.toHaveBeenCalled();
  });

  it('completes for a verified task owner without service-role billing', async () => {
    const supabaseAdmin = createSupabaseAdmin();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: { supabaseAdmin, logger: createLogger(), auth: { userId: 'user-1', isServiceRole: false } },
    });
    mocks.resolveTaskStorageActor.mockResolvedValue({
      ok: true,
      value: { isServiceRole: false, taskOwnerVerified: true, callerId: 'user-1', taskUserId: 'user-1' },
    });

    const response = await completeTaskHandler(new Request('https://edge.test/complete-task'));

    expect(response.status).toBe(200);
    expect(mocks.enforceRateLimit).toHaveBeenCalled();
    expect(mocks.createGenerationFromTask).toHaveBeenCalledWith(
      supabaseAdmin, 'task-1', expect.anything(), expect.any(String), null, expect.anything(),
      { isServiceRole: false, taskOwnerVerified: true, actorId: 'user-1' },
    );
    expect(mocks.triggerCostCalculationIfNotSubTask).not.toHaveBeenCalled();
  });

  it('keeps completion successful and persists recoverable billing warnings', async () => {
    const supabaseAdmin = createSupabaseAdmin();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: { supabaseAdmin, logger: createLogger(), auth: { userId: null, isServiceRole: true } },
    });
    mocks.triggerCostCalculationIfNotSubTask.mockResolvedValue({
      ok: false, errorCode: 'billing_retry', message: 'Retry billing',
    });

    const response = await completeTaskHandler(new Request('https://edge.test/complete-task'));

    expect(response.status).toBe(200);
    expect(await response.json()).toMatchObject({
      success: true,
      follow_up: { status: 'degraded', issues: [{ step: 'cost_calculation', code: 'billing_retry', message: 'Retry billing' }] },
    });
    expect(mocks.persistCompletionFollowUpIssues).toHaveBeenCalledWith(
      supabaseAdmin, 'task-1', {}, [{ step: 'cost_calculation', code: 'billing_retry', message: 'Retry billing' }],
    );
    expect(mocks.markTaskFailed).not.toHaveBeenCalled();
  });

  it('fails completion and cleans prepared output when the task update fails', async () => {
    const supabaseAdmin = createSupabaseAdmin();
    mocks.bootstrapEdgeHandler.mockResolvedValue({
      ok: true,
      value: { supabaseAdmin, logger: createLogger(), auth: { userId: null, isServiceRole: true } },
    });
    supabaseAdmin.finalEq.mockResolvedValue({ error: new Error('task update failed') });

    const response = await completeTaskHandler(new Request('https://edge.test/complete-task'));

    expect(response.status).toBe(500);
    expect(mocks.markTaskFailed).toHaveBeenCalledWith(
      supabaseAdmin, 'task-1', 'Task completion DB update failed: task update failed',
    );
    expect(mocks.cleanupFile).toHaveBeenCalledWith(supabaseAdmin, 'tasks/user-1/task-1/out.png');
    expect(mocks.triggerCostCalculationIfNotSubTask).not.toHaveBeenCalled();
  });
});
