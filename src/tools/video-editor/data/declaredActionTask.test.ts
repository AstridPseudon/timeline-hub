import { describe, expect, it } from 'vitest';
import { buildDeclaredActionTaskRequest, prepareDeclaredActionTaskRequest } from './declaredActionTask';
import { runtimeCapabilitySchema, type RuntimeCapability } from './bridgeContract';

function capability(): RuntimeCapability {
  return {
    capability_id: 'chiptune.compose',
    definition_digest: `sha256:${'a'.repeat(64)}`,
    status: 'ready',
    required_resource_keys: ['cpu'],
    estimated_scratch_bytes: 7,
    estimated_output_bytes: 11,
    action_declaration: { kind: 'generator' },
  };
}

const params = {
  duration_s: 2, bpm: 132, key: 'A minor', seed: 424021,
  sections: [{ start_s: 0, end_s: 2, energy: 0.37, mood: 'wistful' }],
  hits: [0.5, { t: 1, kind: 'thud' }], mutes: [[1.5, 1.75]],
  duck: [{ start_s: 0.5, end_s: 1, gain_db: -6 }], vo_mask: [[1, 1.2]],
  duck_db: -10, master_db: -16, style: 'nes',
};

describe('declared action storage projection', () => {
  it.each([[0, 0], [7, 11]])('preserves producer estimates %i/%i and canonical params', (scratch, output) => {
    const row = { ...capability(), estimated_scratch_bytes: scratch, estimated_output_bytes: output };
    const before = JSON.stringify(params);
    const request = buildDeclaredActionTaskRequest('synthetic', 'chiptune.compose', row, params);
    expect(request.storage_estimate).toEqual({ scratch_bytes: scratch, output_bytes: output });
    expect(request.spec).toEqual({ family: 'chiptune.compose', params, output_policy: {} });
    expect(request.spec.params).toBe(params);
    expect(JSON.stringify(params)).toBe(before);
    expect(request.capability_digest).toBe(row.definition_digest);
    expect(request.input_object_ids).toEqual([]);
  });

  it.each(['estimated_scratch_bytes', 'estimated_output_bytes'] as const)('refuses unknown or invalid %s without coercion', (key) => {
    for (const value of [undefined, null, false, '0', -1, 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1]) {
      const row = { ...capability(), [key]: value } as RuntimeCapability;
      expect(() => buildDeclaredActionTaskRequest('synthetic', 'chiptune.compose', row, params))
        .toThrow(`no valid declared ${key}`);
    }
  });

  it('refuses the existing catalog unavailable representation even with numeric placeholders', () => {
    const row = runtimeCapabilitySchema.parse({
      ...capability(), status: 'unavailable', estimated_scratch_bytes: 0, estimated_output_bytes: 0,
      unavailable_reason: 'storage_estimate:reason=missing or invalid declared storage estimate: estimated_output_bytes',
    });
    expect(() => buildDeclaredActionTaskRequest('synthetic', 'chiptune.compose', row, params))
      .toThrow('missing or invalid declared storage estimate');
  });

  it('preserves project, action identity and Generator guards', () => {
    expect(() => buildDeclaredActionTaskRequest('', 'chiptune.compose', capability(), params)).toThrow('selected Runtime project');
    expect(() => buildDeclaredActionTaskRequest('synthetic', 'other', capability(), params)).toThrow('not the admitted action');
    expect(() => buildDeclaredActionTaskRequest('synthetic', 'chiptune.compose', { ...capability(), action_declaration: undefined }, params)).toThrow('no Generator declaration');
  });
});

it('requires a host adapter for request-estimated declarations and never uses zero', async () => {
  const { estimated_output_bytes: _output, estimated_scratch_bytes: _scratch, ...base } = capability();
  const row = { ...base, storage_estimate: { mode: 'request_estimated' as const,
    estimator: { id: 'example.plan', version: 1, implementation_digest: `sha256:${'b'.repeat(64)}` } } };
  await expect(prepareDeclaredActionTaskRequest('synthetic', 'chiptune.compose', row, params)).rejects.toThrow('unavailable');
  expect(() => buildDeclaredActionTaskRequest('synthetic', 'chiptune.compose', row, params)).toThrow('typed preparation');
});

it('refuses combined overflow in static v1 admission', () => {
  expect(() => buildDeclaredActionTaskRequest('synthetic', 'chiptune.compose', {
    ...capability(), estimated_output_bytes: Number.MAX_SAFE_INTEGER, estimated_scratch_bytes: 1,
  }, params)).toThrow();
});
