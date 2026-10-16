import type { BridgeTaskAdmissionRequest, RuntimeCapability } from './bridgeContract.ts';

export const CHIPTUNE_COMPOSE_ACTION_ID = 'chiptune.compose';

/**
 * Map the admitted Generator action onto App's existing HC-04 task request.
 * Runtime owns the capability digest, task identity, and output association;
 * this projection carries only the selected action and its validated inputs.
 */
export function buildDeclaredActionTaskRequest(
  project: string,
  actionId: string,
  capability: RuntimeCapability,
  values: Record<string, unknown>,
): BridgeTaskAdmissionRequest {
  if (!project.trim()) throw new Error('A selected Runtime project is required to run this action.');
  if (actionId !== CHIPTUNE_COMPOSE_ACTION_ID || capability.capability_id !== actionId) {
    throw new Error(`Runtime capability ${capability.capability_id} is not the admitted action ${actionId}.`);
  }
  if (capability.status !== 'ready') {
    throw new Error(`Runtime capability ${actionId} is not ready.${capability.unavailable_reason ? ` ${capability.unavailable_reason}` : ''}`);
  }
  if (capability.action_declaration?.kind !== 'generator') {
    throw new Error(`Runtime capability ${actionId} has no Generator declaration.`);
  }
  // These values are producer-owned declarations, including legitimate zero.
  // An absent/invalid estimate must never become a zero or unlimited request.
  for (const key of ['estimated_scratch_bytes', 'estimated_output_bytes'] as const) {
    const estimate = capability[key];
    if (!Number.isSafeInteger(estimate) || estimate < 0) {
      throw new Error(`Runtime capability ${actionId} has no valid declared ${key}.`);
    }
  }

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
