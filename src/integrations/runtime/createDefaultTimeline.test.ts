import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { AstridRuntimeClient, RUNTIME_CLIENT_SCOPES, RUNTIME_CLIENT_VERSION } from './client.ts';
import { ApiError, type CanonicalDocument, type CommitRequest, type Transport } from './generated.ts';
import { RUNTIME_SCHEMA_DIGEST } from './contract-metadata.ts';
import fixture from '@/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json';
import { fixtureDigest } from './__tests__/timelineCommitFixture.ts';
import { createCanonicalTimeline, ensureProjectHasTimeline } from './createDefaultTimeline.ts';

function runtimeClient(timelines: Record<string, unknown>[]) {
  return {
    getProject: vi.fn(async () => ({ project_id: 'project-id', version: 1, metadata: { unrelated: true } })),
    updateProject: vi.fn(async (_id, _key, _version, _name, metadata) => ({ project_id: 'project-id', version: 2, metadata })),
    listTimelines: vi.fn(async () => timelines),
    publishParentComposition: vi.fn(async () => ({ revision_id: 'parent-head' })),
  } as unknown as AstridRuntimeClient;
}

type NativeTransportOptions = {
  projectId: string;
  timelineId: string;
  existing?: boolean;
  lose?: 'create' | 'init';
  createKey?: string;
  initName?: string;
};

const headerMap = (headers: Record<string, string>) => Object.fromEntries(
  Object.entries(headers).map(([name, value]) => [name.toLowerCase(), value]),
);

function requireNativeRequest(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(`native transport contract violation: ${message}`);
}

function nativeTransport(options: NativeTransportOptions) {
  const parentPayload = { ...structuredClone(fixture.bundle.parent), occurrences: [] };
  const initializedPayload = { ...structuredClone(fixture.after_bundle.parent), occurrences: [] };
  const h0 = { revision_id: 'parent-0', publication_id: 'bootstrap-p0' };
  const h1 = { revision_id: 'initialized', publication_id: 'init-p1' };
  let created = options.existing === true;
  let initialized = false;
  let createAttempts = 0;
  let initAttempts = 0;
  let createRequest: { timeline_id: string; name?: string } | undefined;
  let initRequest: CommitRequest | undefined;
  let initReceipt: Record<string, unknown> | undefined;
  const calls: Array<{ method: string; path: string; headers: Record<string, string>; body?: unknown }> = [];
  const bytes = (value: unknown) => new TextEncoder().encode(JSON.stringify(value));
  const ok = (value: unknown) => ({ status: 200, headers: { 'content-type': 'application/json' }, body: bytes(value) });
  const document = (revision: string, payload: Record<string, unknown>): CanonicalDocument => ({
    schema_version: 1,
    project_id: options.projectId,
    timeline_id: options.timelineId,
    parent_revision: { revision_id: revision, content_digest: fixtureDigest(payload), payload },
    shot_revisions: [],
    internal_timeline_revisions: [],
    dependency_manifest: { shots: [], internal_timelines: [], media: [], documents: [] },
  });
  const h0Document = () => document(h0.revision_id, parentPayload);
  const h1Document = () => document(h1.revision_id, initializedPayload);
  const expectedCommands = (name = options.initName ?? 'Main') => {
    const commands = structuredClone(fixture.commands);
    commands[0].args.name = name;
    commands[0].args.slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'timeline';
    return commands;
  };
  const projectPath = `/v1/projects/${encodeURIComponent(options.projectId)}`;
  const timelinePath = () => `${projectPath}/timelines/${encodeURIComponent(options.timelineId)}`;
  const expectedHeaders = (headers: Record<string, string>, expected: Record<string, unknown>) => {
    expect(headerMap(headers)).toEqual(expected);
  };
  const h0Receipt = {
    receipt_id: h0.publication_id,
    command_kind: 'parent_composition.publish',
    idempotency_key: `bootstrap:${options.timelineId}`,
    request_hash: 'bootstrap-hash',
    project_id: options.projectId,
    project_seq: [1, 1] as [number, number],
    event_ids: ['bootstrap-event'],
    result: {
      project_id: options.projectId, timeline_id: options.timelineId, revision_id: h0.revision_id,
      content_digest: fixtureDigest(parentPayload), old_head: null, new_head: h0.revision_id, payload: parentPayload,
    },
    created_at: '2026-10-20T00:00:00Z',
  };
  const commitResponse = (request: CommitRequest) => {
    const data = {
      status: 'accepted' as const,
      base_revision_id: request.base_revision_id,
      base_publication_id: request.base_publication_id,
      previous_revision_id: h0.revision_id,
      previous_publication_id: h0.publication_id,
      accepted_revision_id: h1.revision_id,
      rebased_onto: null,
      canonical_document: h1Document(),
      document_digest: fixtureDigest(h1Document()),
      commands: request.commands,
      id_map: {},
      provider_version: 'provider-1',
      compiler_version: 'compiler-1',
      publisher: 'actor-1',
    };
    return { data, receipt: {
      receipt_id: h1.publication_id,
      command_kind: 'timeline.commit',
      idempotency_key: 'init-key',
      request_hash: 'init-hash',
      project_id: options.projectId,
      project_seq: [2, 2] as [number, number],
      event_ids: ['init-event'],
      result: data,
      created_at: '2026-10-20T00:00:00Z',
    } };
  };
  const history = () => {
    const current = initialized ? h1 : h0;
    const currentDocument = initialized ? h1Document() : h0Document();
    const currentReceipt = initialized ? initReceipt : h0Receipt;
    return {
      head: current,
      next_cursor: null,
      items: [{
        publication_id: current.publication_id,
        revision_id: current.revision_id,
        previous: initialized ? h0 : null,
        receipt: currentReceipt,
        intent: initialized ? 'recorded' : 'bootstrap',
        records: initialized ? {
          schema_version: 1,
          commands: initRequest!.commands.map((command) => ({ command })),
          undo_of: [], restored_from: null,
        } : null,
        provider_version: initialized ? 'provider-1' : null,
        compiler_version: initialized ? 'compiler-1' : null,
        publisher: initialized ? 'actor-1' : null,
      },
      ...(initialized ? [{
        publication_id: h0.publication_id, revision_id: h0.revision_id, previous: null,
        receipt: h0Receipt, intent: 'bootstrap', records: null,
        provider_version: null, compiler_version: null, publisher: null,
      }] : []),
      ],
      currentDocument,
    };
  };
  const transport: Transport = async (method, path, headers, body) => {
    const text = body ? new TextDecoder().decode(body as Uint8Array) : undefined;
    const parsed = text ? JSON.parse(text) as Record<string, unknown> : undefined;
    calls.push({ method, path, headers, body: parsed });
    if (method === 'GET' && path === '/v1/health') {
      expectedHeaders(headers, { accept: 'application/json' });
      requireNativeRequest(parsed === undefined, 'health must not carry a body');
      return ok({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_instance_id: 'runtime-instance-fixture' });
    }
    if (method === 'POST' && path === '/v1/handshake') {
      expectedHeaders(headers, { accept: 'application/json', 'content-type': 'application/json' });
      expect(parsed).toEqual({
        protocol: 'workspace.v1',
        client_name: 'astrid-browser',
        client_version: RUNTIME_CLIENT_VERSION,
        requested_scopes: RUNTIME_CLIENT_SCOPES,
      });
      return ok({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 'session-fixture', actor_id: 'astrid-product-connector', realm_id: 'realm-fixture', scopes: RUNTIME_CLIENT_SCOPES, capabilities: ['execution_binding.targeted.v1'] });
    }
    if (method === 'GET' && path === '/v1/realm') {
      expectedHeaders(headers, { accept: 'application/json' });
      requireNativeRequest(parsed === undefined, 'realm must not carry a body');
      return ok({ realm_id: 'realm-fixture', display_name: 'Fixture', version: 1, created_at: '2026-10-14T00:00:00Z' });
    }
    if (method === 'GET' && path === `${timelinePath()}/commits?limit=50`) {
      expectedHeaders(headers, { accept: 'application/json' });
      requireNativeRequest(parsed === undefined, 'history must not carry a body');
      const current = history();
      return ok({ head: current.head, next_cursor: current.next_cursor, items: current.items });
    }
    if (method === 'GET' && (path === `${timelinePath()}/composition-revisions/${h0.revision_id}`
      || path === `${timelinePath()}/composition-revisions/${h1.revision_id}`)) {
      expectedHeaders(headers, { accept: 'application/json' });
      requireNativeRequest(parsed === undefined, 'composition revision must not carry a body');
      const revision = path.split('/').at(-1);
      const current = revision === h1.revision_id ? h1Document() : h0Document();
      return ok({ project_id: current.project_id, timeline_id: current.timeline_id, ...current.parent_revision, dependency_manifest: current.dependency_manifest });
    }
    if (method === 'POST' && path === `${projectPath}/timelines`) {
      expectedHeaders(headers, { accept: 'application/json', 'content-type': 'application/json', 'idempotency-key': expect.any(String) });
      requireNativeRequest(parsed?.timeline_id && typeof parsed.timeline_id === 'string',
        'create must identify a timeline');
      requireNativeRequest(Object.keys(parsed).every((key) => key === 'timeline_id' || key === 'name'),
        'create has unexpected fields');
      requireNativeRequest(parsed.name === undefined || typeof parsed.name === 'string',
        'create name must be a string when present');
      expect(headers['Idempotency-Key'] ?? headers['idempotency-key']).toBe(options.createKey ?? expect.any(String));
      expect(parsed).toEqual({
        timeline_id: parsed.timeline_id,
        ...(options.existing ? {} : { name: options.initName ?? 'Main' }),
      });
      createAttempts += 1;
      createRequest = parsed as typeof createRequest;
      options.timelineId = createRequest.timeline_id;
      h0Receipt.result.timeline_id = options.timelineId;
      created = true;
      const key = headers['Idempotency-Key'] ?? headers['idempotency-key'];
      if (options.lose === 'create' && createAttempts === 1) throw new Error('simulated lost response after create');
      const data = { project_id: options.projectId, timeline_id: options.timelineId, archived: false, head_revision_id: h0.revision_id, head_publication_id: h0.publication_id };
      return ok({ data, receipt: { receipt_id: 'create-receipt', command_kind: 'timeline.create', idempotency_key: key, request_hash: 'create-hash', project_id: options.projectId, project_seq: [1, 1], event_ids: ['create-event'], result: data, created_at: '2026-10-20T00:00:00Z' } });
    }
    if (method === 'POST' && path === `${timelinePath()}/commit`) {
      expectedHeaders(headers, { accept: 'application/json', 'content-type': 'application/json', 'idempotency-key': expect.any(String) });
      const expectedRequest = {
        api_version: 1,
        project_id: options.projectId,
        timeline_id: options.timelineId,
        base_revision_id: h0.revision_id,
        base_publication_id: h0.publication_id,
        commands: expectedCommands(),
        source: { via: 'app' },
      };
      expect(parsed).toEqual(expectedRequest);
      requireNativeRequest(parsed.dry_run === undefined, 'bootstrap commit must not be a preview');
      const key = headers['Idempotency-Key'] ?? headers['idempotency-key'];
      requireNativeRequest(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,255}$/.test(key ?? ''),
        'commit must carry a valid idempotency key');
      if (initRequest) expect(parsed).toEqual(initRequest);
      initAttempts += 1;
      initRequest = parsed as unknown as CommitRequest;
      initialized = true;
      const response = commitResponse(initRequest);
      response.receipt.idempotency_key = headers['Idempotency-Key'] ?? headers['idempotency-key'] ?? '';
      initReceipt = response.receipt;
      if (options.lose === 'init' && initAttempts === 1) throw new Error('simulated lost response after init');
      return ok(response);
    }
    if (method === 'POST' && (path === `${timelinePath()}/composition-revisions`
      || path === `${projectPath}/timeline-documents`)) {
      throw new Error(`legacy bootstrap route rejected: ${method} ${path}`);
    }
    throw new Error(`unexpected ${method} ${path}`);
  };
  return { transport, calls, state: () => ({ createAttempts, initAttempts, created, initialized, createRequest, initRequest }) };
}

function nativeClient(projectId: string, timelines: Record<string, unknown>[], options: NativeTransportOptions) {
  const native = nativeTransport(options);
  const client = new AstridRuntimeClient({
    baseUrl: `http://runtime-${projectId}.test`,
    expectedIdentity: { actorId: 'astrid-product-connector', realmId: 'realm-fixture', runtimeInstanceId: 'runtime-instance-fixture' },
    transport: native.transport,
  });
  client.getProject = vi.fn(async () => ({ project_id: projectId, version: 1, metadata: { unrelated: true } })) as never;
  client.listTimelines = vi.fn(async () => timelines) as never;
  client.updateProject = vi.fn(async (_id, _key, _version, _name, metadata) => ({ project_id: projectId, version: 2, metadata })) as never;
  client.publishParentComposition = vi.fn(async () => ({ revision_id: 'legacy-parent-head' })) as never;
  return { client, native };
}

function installNativeHarness(transport: Transport) {
  vi.stubGlobal('indexedDB', createFakeIndexedDB());
  vi.stubGlobal('navigator', { locks: { request: async (_name: string, _options: unknown, work: (lock: object) => Promise<unknown>) => work({}) } });
  vi.stubGlobal('fetch', async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = new URL(String(input), 'http://runtime.test');
    const headers = Object.fromEntries(new Headers(init?.headers).entries());
    const body = init?.body === undefined ? undefined : new Uint8Array(await new Response(init.body).arrayBuffer());
    const response = await transport(init?.method ?? 'GET', `${url.pathname}${url.search}`, headers, body);
    return new Response(response.body, { status: response.status, headers: response.headers });
  });
}

describe('ensureProjectHasTimeline', () => {
  it('never reapplies defaults over an already headed timeline with opaque authored edits', async () => {
    const authored = JSON.parse('{"opaque":[null,false,[]],"nullable":null,"ordered":[3,1,2],"__proto__":{"literal":true},"constructor":0,"prototype":false}');
    const timelines = [{ timeline_id: 'main-id', head_revision_id: 'edited-head', config: authored }];
    const client = runtimeClient(timelines);
    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('main-id');
    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('main-id');
    expect(client.publishParentComposition).not.toHaveBeenCalled();
    expect(timelines[0].config).toEqual(authored);
  });

  it('reuses an existing canonical timeline head instead of creating a duplicate', async () => {
    const client = runtimeClient([
      { timeline_id: 'older', head_revision_id: 'head-older', slug: 'reference' },
      { timeline_id: 'main-id', head_revision_id: 'head-main', slug: 'main', is_default: true },
    ]);

    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('main-id');
    expect(client.publishParentComposition).not.toHaveBeenCalled();
  });

  it('creates and initializes a canonical empty timeline through the native Runtime transport', async () => {
    const projectId = 'project-native-create';
    const timelineId = 'timeline-native-create';
    const { client, native } = nativeClient(projectId, [], {
      projectId, timelineId, createKey: `astrid-first-timeline-${projectId}`, initName: 'Main',
    });
    installNativeHarness(native.transport);

    const createdId = await ensureProjectHasTimeline(projectId, client);
    expect(createdId).toBe(native.state().createRequest?.timeline_id);

    const state = native.state();
    expect(state.createAttempts).toBe(1);
    expect(state.initAttempts).toBe(1);
    expect(state.createRequest).toEqual({ timeline_id: expect.any(String), name: 'Main' });
    expect(state.initRequest?.commands).toEqual(fixture.commands);
    expect(native.calls.some(({ path }) => path.includes('/composition-revisions') && !path.includes('/commits'))).toBe(true);
    expect(native.calls.filter(({ path }) => path.endsWith('/commit'))).toHaveLength(1);
  });

  it('repairs an existing headless shell without creating a second timeline', async () => {
    const projectId = 'project-native-repair';
    const timelineId = 'headless-shell';
    const { client, native } = nativeClient(projectId, [{ timeline_id: timelineId, head_revision_id: null }], {
      projectId, timelineId, existing: true, createKey: `astrid-first-timeline-${projectId}`, initName: 'Main',
    });
    installNativeHarness(native.transport);

    await expect(ensureProjectHasTimeline(projectId, client)).resolves.toBe(timelineId);

    const state = native.state();
    expect(state.createAttempts).toBe(1);
    expect(state.initAttempts).toBe(1);
    expect(state.createRequest).toEqual({ timeline_id: timelineId });
    expect(state.initRequest?.base_revision_id).toBe('parent-0');
    expect(state.initRequest?.base_publication_id).toBe('bootstrap-p0');
    expect(client.publishParentComposition).not.toHaveBeenCalled();
  });

  it('honors a reassigned Main pointer over a timeline named main without changing either composition', async () => {
    const client = runtimeClient([
      { timeline_id: 'original', slug: 'main', head_revision_id: 'h1' },
      { timeline_id: 'chosen', slug: 'other', head_revision_id: 'h2' },
    ]);
    vi.mocked(client.getProject).mockResolvedValue({ version: 1, metadata: { default_timeline_id: 'chosen' } } as never);
    expect(await ensureProjectHasTimeline('project-id', client)).toBe('chosen');
    expect(client.publishParentComposition).not.toHaveBeenCalled();
    expect(client.updateProject).not.toHaveBeenCalled();
  });

  it('returns the canonical ID when the project primary metadata contains a timeline alias', async () => {
    const client = runtimeClient([
      { timeline_id: 'timeline-canonical', timeline_ulid: 'timeline-alias', head_revision_id: 'head' },
    ]);
    vi.mocked(client.getProject).mockResolvedValue({
      version: 1,
      metadata: { default_timeline_id: 'timeline-alias' },
    } as never);

    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('timeline-canonical');
    expect(client.updateProject).not.toHaveBeenCalled();
  });

  it('prefers an exact canonical ID over another timeline alias collision', async () => {
    const client = runtimeClient([
      { timeline_id: 'alias-match', timeline_ulid: 'shared-ref', head_revision_id: 'alias-head' },
      { timeline_id: 'shared-ref', timeline_ulid: 'other-alias', head_revision_id: 'canonical-head' },
    ]);
    vi.mocked(client.getProject).mockResolvedValue({
      version: 1,
      metadata: { default_timeline_id: 'shared-ref' },
    } as never);

    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('shared-ref');
    expect(client.updateProject).not.toHaveBeenCalled();
  });

  it('refetches timelines and preserves a concurrent primary assignment by canonical ID', async () => {
    const client = runtimeClient([
      { timeline_id: 'original', head_revision_id: 'old-head' },
    ]);
    vi.mocked(client.getProject)
      .mockResolvedValueOnce({ version: 1, metadata: {} } as never)
      .mockResolvedValueOnce({ version: 2, metadata: { default_timeline_id: 'new-alias' } } as never);
    vi.mocked(client.listTimelines)
      .mockResolvedValueOnce([{ timeline_id: 'original', head_revision_id: 'old-head' }] as never)
      .mockResolvedValueOnce([{
        timeline_id: 'concurrent-canonical',
        timeline_ulid: 'new-alias',
        head_revision_id: 'new-head',
      }] as never);

    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('concurrent-canonical');
    expect(client.updateProject).not.toHaveBeenCalled();
    expect(client.listTimelines).toHaveBeenCalledTimes(2);
  });

  it('throws a retryable error instead of returning an unresolved concurrent alias', async () => {
    const client = runtimeClient([{ timeline_id: 'original', head_revision_id: 'old-head' }]);
    vi.mocked(client.getProject)
      .mockResolvedValueOnce({ version: 1, metadata: {} } as never)
      .mockResolvedValueOnce({ version: 2, metadata: { default_timeline_id: 'unresolved-alias' } } as never)
      .mockResolvedValueOnce({ version: 2, metadata: { default_timeline_id: 'unresolved-alias' } } as never);
    vi.mocked(client.listTimelines)
      .mockResolvedValueOnce([{ timeline_id: 'original', head_revision_id: 'old-head' }] as never)
      .mockResolvedValueOnce([{ timeline_id: 'original', head_revision_id: 'old-head' }] as never);

    await expect(ensureProjectHasTimeline('project-id', client)).rejects.toThrow(
      'could not be resolved to a canonical timeline ID; retry',
    );
    expect(client.updateProject).not.toHaveBeenCalled();
  });

  it('merges a newly created Main pointer with concurrent chat metadata after a CAS conflict', async () => {
    const projectId = 'project-native-cas';
    const timelineId = 'timeline-native-cas';
    const { client, native } = nativeClient(projectId, [], {
      projectId, timelineId, createKey: `astrid-first-timeline-${projectId}`, initName: 'Main',
    });
    installNativeHarness(native.transport);
    vi.mocked(client.getProject).mockResolvedValueOnce({ version: 1, metadata: {} } as never)
      .mockResolvedValueOnce({ version: 1, metadata: {} } as never)
      .mockResolvedValue({ version: 2, metadata: { chat: { keep: true } } } as never);
    vi.mocked(client.updateProject).mockRejectedValueOnce(new ApiError(409, 'version_conflict', 'changed'));
    const id = await ensureProjectHasTimeline(projectId, client);
    expect(client.updateProject).toHaveBeenLastCalledWith(projectId, expect.any(String), 2, undefined,
      { chat: { keep: true }, default_timeline_id: id });
    expect(native.state().initAttempts).toBe(1);
    expect(client.publishParentComposition).not.toHaveBeenCalled();
  });

  it('creates an additional canonical timeline with its own idempotency key', async () => {
    const projectId = 'project-native-additional';
    const timelineId = 'project-timeline-2';
    const { client, native } = nativeClient(projectId, [], {
      projectId, timelineId, createKey: `astrid-timeline-create-${projectId}-${timelineId}`, initName: 'Timeline 2',
    });
    installNativeHarness(native.transport);

    await expect(createCanonicalTimeline(projectId, {
      name: 'Timeline 2',
      timelineId,
    }, client)).resolves.toBe(timelineId);
    expect(native.state().createRequest).toEqual({ timeline_id: timelineId, name: 'Timeline 2' });
    const createCall = native.calls.find(({ method, path }) => method === 'POST' && path.endsWith('/timelines'));
    expect(createCall?.headers['Idempotency-Key'] ?? createCall?.headers['idempotency-key']).toBe(
      `astrid-timeline-create-${projectId}-${timelineId}`,
    );
    expect(client.publishParentComposition).not.toHaveBeenCalled();
  });

  it('replays the exact native initialization request after a lost response', async () => {
    const projectId = 'project-native-retry';
    const timelineId = 'timeline-native-retry';
    const idempotencyKey = 'timeline-native-retry-key';
    const { client, native } = nativeClient(projectId, [], {
      projectId, timelineId, lose: 'init', createKey: idempotencyKey, initName: 'Retry',
    });
    installNativeHarness(native.transport);

    await expect(createCanonicalTimeline(projectId, { name: 'Retry', timelineId, idempotencyKey }, client))
      .rejects.toThrow('simulated lost response after init');
    await expect(createCanonicalTimeline(projectId, { name: 'Retry', timelineId, idempotencyKey }, client))
      .resolves.toBe(timelineId);

    const creates = native.calls.filter(({ method, path }) => method === 'POST' && path.endsWith('/timelines'));
    const commits = native.calls.filter(({ method, path }) => method === 'POST' && path.endsWith('/commit'));
    expect(creates).toHaveLength(1);
    expect(commits).toHaveLength(2);
    expect(creates[0]?.body).toEqual({ timeline_id: timelineId, name: 'Retry' });
    expect(commits[0]).toEqual(commits[1]);
    expect(commits[0]?.path).toBe(`/v1/projects/${projectId}/timelines/${timelineId}/commit`);
    expect(headerMap(commits[0]?.headers ?? {})).toEqual({
      accept: 'application/json',
      'content-type': 'application/json',
      'idempotency-key': expect.any(String),
    });
    expect(commits[0]?.body).toEqual(expect.objectContaining({
      api_version: 1,
      project_id: projectId,
      timeline_id: timelineId,
      base_revision_id: 'parent-0',
      base_publication_id: 'bootstrap-p0',
      commands: expect.arrayContaining([
        expect.objectContaining({ op: 'timeline.init', args: expect.objectContaining({ name: 'Retry', slug: 'retry' }) }),
      ]),
      source: { via: 'app' },
    }));
    expect(commits[0]?.headers['Idempotency-Key'] ?? commits[0]?.headers['idempotency-key']).toBe(
      commits[1]?.headers['Idempotency-Key'] ?? commits[1]?.headers['idempotency-key'],
    );
    expect(creates[0]?.headers['Idempotency-Key']).toBe(idempotencyKey);
    expect(native.state().initAttempts).toBe(2);
    expect(native.calls.some(({ method, path }) => method === 'POST' && path.endsWith('/composition-revisions'))).toBe(false);
    expect(native.calls.some(({ path }) => path.includes('/timeline-documents'))).toBe(false);
    expect(native.calls.filter(({ method, path }) => method === 'POST' && path === '/v1/handshake')).not.toHaveLength(0);
    expect(client.publishParentComposition).not.toHaveBeenCalled();
  });
});
