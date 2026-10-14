import { describe, expect, it, vi } from 'vitest';
import { ReighRuntimeClient, RUNTIME_CLIENT_SCOPES } from './client.ts';
import type { Transport } from './generated.ts';
import {
  RUNTIME_SCHEMA_DIGEST,
  RUNTIME_TARGETED_EXECUTION_CAPABILITY,
} from './contract-metadata.ts';
import { createCanonicalTimeline, ensureProjectHasTimeline } from './createDefaultTimeline.ts';

function runtimeClient(timelines: Record<string, unknown>[]) {
  return {
    listTimelines: vi.fn(async () => timelines),
    publishParentComposition: vi.fn(async () => ({ revision_id: 'parent-head' })),
  } as unknown as ReighRuntimeClient;
}

describe('ensureProjectHasTimeline', () => {
  it('reuses an existing canonical timeline head instead of creating a duplicate', async () => {
    const client = runtimeClient([
      { timeline_id: 'older', head_revision_id: 'head-older', slug: 'reference' },
      { timeline_id: 'main-id', head_revision_id: 'head-main', slug: 'main', is_default: true },
    ]);

    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('main-id');
    expect(client.publishParentComposition).not.toHaveBeenCalled();
  });

  it('publishes a canonical empty composition atomically for a new project timeline', async () => {
    const client = runtimeClient([]);

    const created = await ensureProjectHasTimeline('project-id', client);

    expect(created).toBeTruthy();
    expect(client.listTimelines).toHaveBeenCalledWith('project-id');
    expect(client.publishParentComposition).toHaveBeenCalledWith(
      'project-id',
      created,
      expect.objectContaining({
        project_id: 'project-id',
        timeline_id: created,
        expected_head: null,
        parent_revision_id: expect.any(String),
        parent_composition: expect.objectContaining({
          slug: 'main',
          name: 'Main',
          config: expect.objectContaining({ clips: [], tracks: expect.any(Array) }),
          registry: { assets: {} },
          clips: [],
          occurrences: [],
        }),
        shot_revisions: [],
        internal_timeline_revisions: [],
      }),
      'reigh-first-timeline-project-id',
    );
  });

  it('repairs an existing headless shell without creating a second timeline', async () => {
    const client = runtimeClient([{ timeline_id: 'headless-shell', head_revision_id: null }]);

    await expect(ensureProjectHasTimeline('project-id', client)).resolves.toBe('headless-shell');
    expect(client.publishParentComposition).toHaveBeenCalledWith(
      'project-id',
      'headless-shell',
      expect.objectContaining({ expected_head: null }),
      expect.any(String),
    );
  });

  it('creates an additional canonical timeline with its own idempotency key', async () => {
    const client = runtimeClient([]);

    await expect(createCanonicalTimeline('project-id', {
      name: 'Timeline 2',
      timelineId: 'project-timeline-2',
    }, client)).resolves.toBe('project-timeline-2');
    expect(client.publishParentComposition).toHaveBeenCalledWith(
      'project-id',
      'project-timeline-2',
      expect.objectContaining({
        expected_head: null,
        parent_composition: expect.objectContaining({ slug: 'timeline-2', name: 'Timeline 2' }),
      }),
      'reigh-timeline-create-project-id-project-timeline-2',
    );
  });

  it('uses the current atomic Runtime route and replays a stable first-timeline publication', async () => {
    const requests: Array<{
      method: string;
      path: string;
      headers: Record<string, string>;
      body?: Record<string, unknown>;
    }> = [];
    let publishCount = 0;
    const json = (value: unknown) => new TextEncoder().encode(JSON.stringify(value));
    const transport: Transport = async (method, path, headers, body) => {
      const parsedBody = body
        ? JSON.parse(new TextDecoder().decode(body as Uint8Array)) as Record<string, unknown>
        : undefined;
      requests.push({ method, path, headers, ...(parsedBody ? { body: parsedBody } : {}) });

      if (method === 'GET' && path === '/v1/health') {
        return {
          status: 200,
          headers: {},
          body: json({
            status: 'ok',
            protocol: 'workspace.v1',
            schema_digest: RUNTIME_SCHEMA_DIGEST,
            runtime_epoch: 1,
            runtime_instance_id: 'runtime-instance-fixture',
          }),
        };
      }
      if (method === 'POST' && path === '/v1/handshake') {
        return {
          status: 200,
          headers: {},
          body: json({
            protocol: 'workspace.v1',
            schema_digest: RUNTIME_SCHEMA_DIGEST,
            session_id: 'session-fixture',
            actor_id: 'reigh-product-connector',
            realm_id: 'realm-fixture',
            scopes: RUNTIME_CLIENT_SCOPES,
            capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY],
          }),
        };
      }
      if (method === 'GET' && path === '/v1/realm') {
        return {
          status: 200,
          headers: {},
          body: json({ realm_id: 'realm-fixture', display_name: 'Fixture', version: 1, created_at: '2026-10-14T00:00:00Z' }),
        };
      }
      if (method === 'GET' && path === '/v1/projects/project-id/timelines?limit=200') {
        return { status: 200, headers: {}, body: json({ items: [], next_cursor: null }) };
      }
      if (method === 'POST' && path.startsWith('/v1/projects/project-id/timelines/') && path.endsWith('/composition-revisions')) {
        publishCount += 1;
        if (publishCount === 1) throw new Error('simulated lost response after commit');
        const timelineId = path.split('/').at(-2);
        return {
          status: 201,
          headers: {},
          body: json({
            data: { project_id: 'project-id', timeline_id: timelineId, revision_id: parsedBody?.parent_revision_id },
            receipt: { receipt_id: 'composition.publish:reigh-first-timeline-project-id' },
          }),
        };
      }
      throw new Error(`unexpected ${method} ${path}`);
    };
    const client = new ReighRuntimeClient({
      baseUrl: 'http://runtime.test',
      expectedIdentity: {
        actorId: 'reigh-product-connector',
        realmId: 'realm-fixture',
        runtimeInstanceId: 'runtime-instance-fixture',
      },
      transport,
    });

    await expect(ensureProjectHasTimeline('project-id', client)).rejects.toThrow('simulated lost response');
    const timelineId = await ensureProjectHasTimeline('project-id', client);

    const publications = requests.filter(({ method, path }) => (
      method === 'POST' && path.endsWith('/composition-revisions')
    ));
    expect(publications).toHaveLength(2);
    expect(publications[0]).toEqual(publications[1]);
    expect(publications[0]).toMatchObject({
      method: 'POST',
      path: `/v1/projects/project-id/timelines/${timelineId}/composition-revisions`,
      headers: {
        'Content-Type': 'application/json',
        'Idempotency-Key': 'reigh-first-timeline-project-id',
      },
      body: {
        project_id: 'project-id',
        timeline_id: timelineId,
        expected_head: null,
        parent_revision_id: expect.stringMatching(/^[0-9a-f-]{36}$/),
        parent_composition: {
          slug: 'main',
          name: 'Main',
          registry: { assets: {} },
          clips: [],
          occurrences: [],
          config: expect.objectContaining({ clips: [], tracks: expect.any(Array) }),
        },
        shot_revisions: [],
        internal_timeline_revisions: [],
      },
    });
    expect(publications[0]?.headers['Idempotency-Key']).toMatch(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,255}$/);
    expect(publications[0]?.path).not.toContain('timeline-documents');
  });
});
