import { describe, expect, it } from 'vitest';

import { getBridgeTaskClient } from '@/integrations/astrid/bridgeTaskReads.ts';
import { prepareDeclaredActionTaskRequest } from '@/tools/video-editor/data/declaredActionTask.ts';
import type { DeclaredActionCapability } from '@/tools/video-editor/data/bridgeContract.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from './contract-metadata.ts';
import { ReighRuntimeClient, RUNTIME_CLIENT_SCOPES } from './client.ts';
import type { StoragePreparation, Transport } from './generated.ts';
import { createRuntimeDeclaredActionPreparationAdapter } from './declaredActionPreparation.ts';
import { canonicalJsonStringify, sha256Hex } from '@/tools/video-editor/data/typed/timelineBundle.ts';

const PROJECT_ID = 'project/typed prep';
const CAPABILITY_ID = 'chiptune.compose';
const CAPABILITY_DIGEST = `sha256:${'a'.repeat(64)}`;
const ESTIMATOR = {
  id: 'chiptune.compose.storage',
  version: 1,
  implementation_digest: `sha256:${'b'.repeat(64)}`,
};

async function digest(value: unknown): Promise<string> {
  return `sha256:${await sha256Hex(canonicalJsonStringify(value))}`;
}

function json(value: unknown): Uint8Array {
  return new TextEncoder().encode(JSON.stringify(value));
}

function capability(): DeclaredActionCapability {
  return {
    capability_id: CAPABILITY_ID,
    definition_digest: CAPABILITY_DIGEST,
    status: 'ready',
    required_resource_keys: ['cpu'],
    storage_estimate: { mode: 'request_estimated', estimator: ESTIMATOR },
    action_declaration: { kind: 'generator', inputs: [], outputs: [] },
  };
}

describe('Runtime declared-action preparation adapter', () => {
  it('uses the authenticated prepare route and forwards its exact estimate into HC-04', async () => {
    const requests: Array<{ method: string; path: string; headers: Record<string, string>; body?: Record<string, unknown> }> = [];
    const transport: Transport = async (method, path, headers, body) => {
      const parsed = body === undefined
        ? undefined
        : JSON.parse(new TextDecoder().decode(body)) as Record<string, unknown>;
      requests.push({ method, path, headers, ...(parsed ? { body: parsed } : {}) });
      if (path === '/v1/health') {
        return { status: 200, headers: {}, body: json({
          status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
          runtime_epoch: 9, runtime_instance_id: 'runtime-test',
        }) };
      }
      if (path === '/v1/handshake') {
        const handshake = parsed as { requested_scopes: string[] };
        return { status: 200, headers: {}, body: json({
          protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
          session_id: 'session-test', actor_id: 'reigh-app', realm_id: 'realm-test',
          scopes: handshake.requested_scopes, capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY],
        }) };
      }
      if (path === '/v1/realm') {
        return { status: 200, headers: {}, body: json({
          realm_id: 'realm-test', display_name: 'test', version: 1, created_at: '2026-10-16T00:00:00Z',
        }) };
      }
      if (path === `/v1/projects/${encodeURIComponent(PROJECT_ID)}/capabilities/${CAPABILITY_ID}/prepare`) {
        const request = parsed as { capability_digest: string; schema_version: number; spec: Record<string, unknown>; input_object_ids: unknown[] };
        const binding = {
          capability_id: CAPABILITY_ID,
          capability_digest: request.capability_digest,
          schema_version: 1,
          spec: request.spec,
          input_facts: [],
          spec_digest: await digest(request.spec),
          source_digest: `sha256:${'c'.repeat(64)}`,
          estimator: ESTIMATOR,
          storage_estimate: { scratch_bytes: 777, output_bytes: 2049 },
        };
        const reply: StoragePreparation = {
          ...binding,
          preparation_digest: await digest(binding),
        };
        return { status: 200, headers: {}, body: json(reply) };
      }
      throw new Error(`Unexpected Runtime request: ${method} ${path}`);
    };

    const runtime = new ReighRuntimeClient({ transport });
    const adapter = createRuntimeDeclaredActionPreparationAdapter(runtime);
    const result = await prepareDeclaredActionTaskRequest(
      PROJECT_ID,
      CAPABILITY_ID,
      capability(),
      { duration_s: 2, sections: [{ start_s: 0, end_s: 2, energy: 0.5 }] },
      adapter,
    );

    expect(result.storage_estimate).toEqual({ scratch_bytes: 777, output_bytes: 2049 });
    expect(result.spec.params).toEqual({ duration_s: 2, sections: [{ start_s: 0, end_s: 2, energy: 0.5 }] });
    const prepare = requests.find((request) => request.path.endsWith('/prepare'));
    expect(prepare).toMatchObject({
      method: 'POST',
      path: `/v1/projects/${encodeURIComponent(PROJECT_ID)}/capabilities/${CAPABILITY_ID}/prepare`,
      headers: { 'Content-Type': 'application/json' },
      body: {
        capability_digest: CAPABILITY_DIGEST,
        schema_version: 1,
        input_object_ids: [],
      },
    });
    expect(prepare?.headers).not.toHaveProperty('Idempotency-Key');
    expect(prepare?.body?.spec).toEqual(result.spec);
    expect(requests.find((request) => request.path === '/v1/handshake')?.body?.requested_scopes)
      .toEqual(RUNTIME_CLIENT_SCOPES);
  });

  it('is wired into the existing bridge task client used by the Generator form', () => {
    expect(getBridgeTaskClient('typed-preparation-test').declaredActionPreparation).toBeDefined();
  });
});
