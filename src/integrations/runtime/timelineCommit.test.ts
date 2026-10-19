import { describe, expect, it } from 'vitest';
import type { Transport } from './generated.ts';
import { classifyRuntimeCommitFailure, AstridRuntimeClient } from './client.ts';
import { ApiError } from './generated.ts';
import { RuntimeDataProvider } from './dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST } from './contract-metadata.ts';

const PROJECT_ID = 'project-commit';
const TIMELINE_ID = 'timeline-commit';

function json(value: unknown): Uint8Array {
  return new TextEncoder().encode(JSON.stringify(value));
}

function accepted(revisionId: string, publicationId: string, baseRevisionId: string, basePublicationId: string, idMap: Record<string, string> = {}) {
  const parentPayload = {
    config: { clips: [], opaque: { keep: null } },
    registry: { assets: {} },
    clips: [],
    occurrences: [],
    bundle: null,
    unknown: { nested: ['value'] },
  };
  return {
    data: {
      status: 'accepted',
      base_revision_id: baseRevisionId,
      base_publication_id: basePublicationId,
      previous_revision_id: baseRevisionId,
      previous_publication_id: basePublicationId,
      accepted_revision_id: revisionId,
      rebased_onto: null,
      canonical_document: {
        schema_version: 1,
        project_id: PROJECT_ID,
        timeline_id: TIMELINE_ID,
        parent_revision: { revision_id: revisionId, content_digest: 'sha256:parent', payload: parentPayload },
        shot_revisions: [],
        internal_timeline_revisions: [],
        dependency_manifest: { shots: [], internal_timelines: [], media: [], documents: [] },
      },
      document_digest: 'sha256:document',
      commands: [{ schema_version: 1, op: 'clip.move', version: '1', select: 'parent/clip:x', args: { on: 7 } }],
      id_map: idMap,
      provider_version: 'provider-1',
      compiler_version: 'compiler-1',
      publisher: 'actor-1',
    },
    receipt: {
      receipt_id: publicationId,
      command_kind: 'timeline.commit',
      idempotency_key: `key-${publicationId}`,
      request_hash: `hash-${publicationId}`,
      project_id: PROJECT_ID,
      project_seq: [1, 1],
      event_ids: [`event-${publicationId}`],
      result: {},
      created_at: '2026-10-19T00:00:00Z',
    },
  };
}

function transportFor(response: unknown, requests: Array<{ method: string; path: string; body?: unknown }>): Transport {
  return async (method, path, _headers, body) => {
    const parsed = body ? JSON.parse(new TextDecoder().decode(body)) : undefined;
    requests.push({ method, path, ...(parsed === undefined ? {} : { body: parsed }) });
    if (path === '/v1/health') return { status: 200, headers: {}, body: json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, runtime_epoch: 1, runtime_instance_id: 'instance-1' }) };
    if (path === '/v1/handshake') return { status: 200, headers: {}, body: json({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST, session_id: 'session-1', actor_id: 'actor-1', realm_id: 'realm-1', scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'], capabilities: ['execution_binding.targeted.v1'] }) };
    if (path === '/v1/realm') return { status: 200, headers: {}, body: json({ realm_id: 'realm-1', display_name: 'fixture', version: 1, created_at: '2026-10-19T00:00:00Z' }) };
    if (path.endsWith('/commit')) return { status: 200, headers: {}, body: json(response) };
    if (path.endsWith('/commits?limit=50')) return { status: 200, headers: {}, body: json({ items: [], next_cursor: null, head: { revision_id: 'r1', publication_id: 'p1' } }) };
    throw new Error(`unexpected Runtime request: ${method} ${path}`);
  };
}

function request(baseRevisionId = 'r0', basePublicationId = 'p0') {
  return {
    api_version: 1 as const,
    project_id: PROJECT_ID,
    timeline_id: TIMELINE_ID,
    base_revision_id: baseRevisionId,
    base_publication_id: basePublicationId,
    commands: [{ schema_version: 1 as const, op: 'clip.move', version: '1', select: 'parent/clip:x', args: { on: 7 } }],
  };
}

describe('Runtime timeline commit capability', () => {
  it('projects the exact accepted closure and retains publication identity without a latest read', async () => {
    const requests: Array<{ method: string; path: string; body?: unknown }> = [];
    const provider = new RuntimeDataProvider({
      projectId: PROJECT_ID,
      baseUrl: 'http://runtime.test',
      token: 'token',
      transport: transportFor(accepted('r1', 'p1', 'r0', 'p0'), requests),
    });
    const result = await provider.commitTimeline(request(), 'retry-1');
    expect(result.accepted).toEqual({ revisionId: 'r1', publicationId: 'p1' });
    expect(result.receipt.receipt_id).toBe('p1');
    expect(Object.keys(result)).toContain('receipt');
    expect(result.canonicalDocument.parent_revision.payload).toMatchObject({ bundle: null, unknown: { nested: ['value'] } });
    expect(result.graph).toMatchObject({
      accepted_identity: { revision_id: 'r1', publication_id: 'p1' },
      primary_timeline: { head: { revision_id: 'r1', publication_id: 'p1' } },
    });
    expect(requests.some(({ path }) => path.includes('/inspect') || path.includes('/composition-revisions/'))).toBe(false);
  });

  it('keeps same revision acknowledgements distinct by publication', async () => {
    const requests: Array<{ method: string; path: string; body?: unknown }> = [];
    const responses = [accepted('r1', 'p1', 'r0', 'p0'), accepted('r1', 'p2', 'r1', 'p1')];
    const transport = async (...args: Parameters<Transport>) => {
      if (args[1].endsWith('/commit')) return { status: 200, headers: {}, body: json(responses.shift()) };
      return transportFor(accepted('r1', 'p1', 'r0', 'p0'), requests)(...args);
    };
    const provider = new RuntimeDataProvider({ projectId: PROJECT_ID, baseUrl: 'http://runtime.test', token: 'token', transport });
    const first = await provider.commitTimeline(request(), 'retry-1');
    const second = await provider.commitTimeline(request('r1', 'p1'), 'retry-2');
    expect(first.accepted).toEqual({ revisionId: 'r1', publicationId: 'p1' });
    expect(second.accepted).toEqual({ revisionId: 'r1', publicationId: 'p2' });
  });

  it('builds an explicit timeline.inverse command through the same capability', async () => {
    const requests: Array<{ method: string; path: string; body?: unknown }> = [];
    const provider = new RuntimeDataProvider({ projectId: PROJECT_ID, baseUrl: 'http://runtime.test', token: 'token', transport: transportFor(accepted('r2', 'p2', 'r1', 'p1'), requests) });
    await provider.undoTimeline({ projectId: PROJECT_ID, timelineId: TIMELINE_ID, headRevisionId: 'r1', headPublicationId: 'p1' }, ['p-a', 'p-b'], 'undo-key');
    const commit = requests.find((entry) => entry.path.endsWith('/commit'));
    expect(commit?.body).toMatchObject({
      base_revision_id: 'r1',
      base_publication_id: 'p1',
      commands: [{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: ['p-a', 'p-b'] } }],
    });
  });

  it('rejects a nonidentity id_map and classifies typed failures', async () => {
    const provider = new RuntimeDataProvider({ projectId: PROJECT_ID, baseUrl: 'http://runtime.test', token: 'token', transport: transportFor(accepted('r1', 'p1', 'r0', 'p0', { 'parent/clip:x': 'parent/clip:y' }), []) });
    await expect(provider.commitTimeline(request(), 'retry-1')).rejects.toThrow('non-identity id_map');
    expect(classifyRuntimeCommitFailure(new ApiError(409, 'conflict', 'conflict', '', { status: 'conflict' }))).toBe('conflict');
    expect(classifyRuntimeCommitFailure(new ApiError(409, 'conflict', 'busy', '', { status: 'refused', reason: 'head_busy' }))).toBe('refused');
    expect(classifyRuntimeCommitFailure(new ApiError(422, 'invalid', 'bad'))).toBe('validation');
    expect(classifyRuntimeCommitFailure(new ApiError(503, 'not_ready', 'unknown'))).toBe('unknown');
  });

  it('keeps recoverable identity scoped to the authenticated actor and realm', async () => {
    const client = new AstridRuntimeClient({ baseUrl: 'http://runtime.test', token: 'token', transport: transportFor(accepted('r1', 'p1', 'r0', 'p0'), []) });
    await expect(client.getRecoverableIdentity()).resolves.toEqual({ actorId: 'actor-1', realmId: 'realm-1' });
  });
});
