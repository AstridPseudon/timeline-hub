import {
  bridgeTaskAdmissionRequestSchema, bridgeTaskStorageEstimateSchema,
  type BridgeTaskAdmissionRequest, type DeclaredActionCapability,
} from './bridgeContract.ts';
import {
  declaredActionPreparationRequestSchema, preparedDeclaredActionSchema,
  type DeclaredActionPreparationAdapter,
} from '@/integrations/astrid/declaredActionPreparation.ts';

export const CHIPTUNE_COMPOSE_ACTION_ID = 'chiptune.compose';

/**
 * Map the admitted Generator action onto App's existing HC-04 task request.
 * Runtime owns the capability digest, task identity, and output association;
 * this projection carries only the selected action and its validated inputs.
 */
export function buildDeclaredActionTaskRequest(
  project: string,
  actionId: string,
  capability: DeclaredActionCapability,
  values: Record<string, unknown>,
): BridgeTaskAdmissionRequest {
  if (!project.trim()) throw new Error('A selected Runtime project is required to run this action.');
  if (capability.capability_id !== actionId) {
    throw new Error(`Runtime capability ${capability.capability_id} is not the admitted action ${actionId}.`);
  }
  if (capability.status !== 'ready') {
    throw new Error(`Runtime capability ${actionId} is not ready.${capability.unavailable_reason ? ` ${capability.unavailable_reason}` : ''}`);
  }
  if (capability.action_declaration?.kind !== 'generator') {
    throw new Error(`Runtime capability ${actionId} has no Generator declaration.`);
  }
  if ('storage_estimate' in capability) {
    if (capability.storage_estimate.mode !== 'static') {
      throw new Error(`Runtime capability ${actionId} requires available typed preparation.`);
    }
    return bridgeTaskAdmissionRequestSchema.parse({
      ...declaredActionInput(project, actionId, capability, values),
      storage_estimate: {
        scratch_bytes: capability.storage_estimate.scratch_bytes,
        output_bytes: capability.storage_estimate.output_bytes,
      },
    });
  }
  // Preserve static v1, including legitimate zero, without coercion.
  for (const key of ['estimated_scratch_bytes', 'estimated_output_bytes'] as const) {
    if (!Number.isSafeInteger(capability[key]) || capability[key] < 0) {
      throw new Error(`Runtime capability ${actionId} has no valid declared ${key}.`);
    }
  }
  bridgeTaskStorageEstimateSchema.parse({
    scratch_bytes: capability.estimated_scratch_bytes, output_bytes: capability.estimated_output_bytes,
  });

  return {
    project,
    capability_id: capability.capability_id,
    capability_digest: capability.definition_digest,
    schema_version: '1',
    input_object_ids: [],
    spec: {
      family: capability.capability_id,
      params: values,
      output_policy: {},
    },
    storage_estimate: {
      scratch_bytes: capability.estimated_scratch_bytes,
      output_bytes: capability.estimated_output_bytes,
    },
  };
}

function declaredActionInput(
  project: string, actionId: string, capability: DeclaredActionCapability, values: Record<string, unknown>,
) {
  return declaredActionPreparationRequestSchema.parse({
    project, capability_id: actionId, capability_digest: capability.definition_digest,
    schema_version: '1', input_object_ids: [],
    spec: { family: actionId, params: values, output_policy: {} },
  });
}

/** Shared generic-form path. No provider/task is invoked until preparation validates. */
export async function prepareDeclaredActionTaskRequest(
  project: string, actionId: string, capability: DeclaredActionCapability,
  values: Record<string, unknown>, adapter?: DeclaredActionPreparationAdapter,
): Promise<BridgeTaskAdmissionRequest> {
  if (!('storage_estimate' in capability) || capability.storage_estimate.mode !== 'request_estimated') {
    return buildDeclaredActionTaskRequest(project, actionId, capability, values);
  }
  if (!project.trim() || capability.capability_id !== actionId || capability.status !== 'ready'
    || capability.action_declaration?.kind !== 'generator') {
    throw new Error(`Runtime capability ${actionId} is unavailable for typed preparation.`);
  }
  if (!adapter) throw new Error('Typed action preparation is unavailable in the authenticated host integration.');
  const expectedEstimator = structuredClone(capability.storage_estimate.estimator);
  const expected = structuredClone(declaredActionInput(project, actionId, capability, values));
  // The adapter cannot mutate the comparison snapshot or the returned request later.
  const prepared = preparedDeclaredActionSchema.parse(structuredClone(await adapter.prepare(structuredClone(expected))));
  const matches = async (left: unknown, right: unknown) =>
    await adapter.digest(left) === await adapter.digest(right);
  if (expected.input_object_ids.length !== 0 || prepared.capability_id !== expected.capability_id
    || prepared.capability_digest !== expected.capability_digest
    || !await matches(prepared.spec, expected.spec) || !await matches(prepared.estimator, expectedEstimator)) {
    throw new Error('Typed action preparation request or estimator identity mismatch.');
  }
  if (await adapter.digest(prepared.spec) !== prepared.spec_digest) {
    throw new Error('Typed action preparation spec digest mismatch.');
  }
  const { preparation_digest, ...binding } = prepared;
  if (await adapter.digest(binding) !== preparation_digest) {
    throw new Error('Typed action preparation binding or storage pair mismatch.');
  }
  return { ...expected, storage_estimate: prepared.storage_estimate };
}
