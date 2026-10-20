import type { ManagedOutput, MediaSelection, Task } from '@/integrations/runtime/generated';
import { AstridRuntimeClient } from '@/integrations/runtime/client';
import { asRecord } from '@/shared/lib/typeCoercion';
import { getLegacyAutoPlacementPresentation } from './legacyAutoPlacementPresentation';

export function runtimeTaskRecoveryPresentation(task: Task, projectId: string) {
  if (task.project_id !== projectId) return null;
  const spec = asRecord(task.spec.spec) ?? task.spec;
  return getLegacyAutoPlacementPresentation({
    id: task.task_id,
    status: task.state === 'succeeded' ? 'Complete' : 'In Progress',
    params: asRecord(spec.params) ?? {},
    resultData: task.result,
    generationIntent: task.generation_intent ?? spec.generation_intent,
    hasAsset: true,
  });
}

export function isRuntimeRecoveryOutput(task: Task, output: ManagedOutput): boolean {
  return output.task_id === task.task_id && output.project_id === task.project_id
    && output.run_id === task.run_id
    && (!task.attempt_id || output.attempt_id === task.attempt_id)
    && ['available', 'promoted'].includes(output.state)
    && /^sha256:[0-9a-f]{64}$/.test(output.object_id)
    && /^(image|video)\//.test(output.media_type)
    && !['thumbnail', 'manifest', 'recoverable_snapshot'].includes(output.role);
}

/** Only the existing selection read may supply a generation/variant identity. */
export async function readRuntimeRecoverySelection(
  client: Pick<AstridRuntimeClient, 'getProjectMediaSelection'>,
  projectId: string,
  output: ManagedOutput,
): Promise<MediaSelection> {
  const selection = await client.getProjectMediaSelection(projectId, {
    association_id: output.association_id,
    object_id: output.object_id,
    version: output.version,
  });
  if (selection.object_id !== output.object_id || !selection.generation_id
    || !selection.variant_id || !selection.asset || !selection.catalog_digest) {
    throw new Error('Output selection is unavailable');
  }
  return selection;
}
