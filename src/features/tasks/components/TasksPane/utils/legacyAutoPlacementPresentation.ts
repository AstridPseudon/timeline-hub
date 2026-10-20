import type { TaskStatus } from '@/types/tasks';

export const LEGACY_AUTO_PLACEMENT_LABEL = 'Not placed: place manually';
export const LEGACY_UNCONFIRMED_PLACEMENT_LABEL = 'Placement unconfirmed: place manually';

interface LegacyAutoPlacementTaskInput {
  id: string;
  status: TaskStatus;
  params: Record<string, unknown>;
  /** Existing Runtime result or legacy complete_task result_data, when readable. */
  resultData?: unknown;
  generationIntent?: unknown;
  hasAsset: boolean;
}

export interface LegacyAutoPlacementPresentation {
  taskId: string;
  label: typeof LEGACY_AUTO_PLACEMENT_LABEL | typeof LEGACY_UNCONFIRMED_PLACEMENT_LABEL;
  /** The completed output remains available to the existing gallery/lightbox. */
  assetRetained: true;
  action: 'place-manually';
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

export function hasLegacyPlacementIntent(params: Record<string, unknown>): boolean {
  return isRecord(params.placement_intent) || isRecord(params.timeline_placement);
}

function hasRetiredCompletionMarker(resultData: unknown): boolean {
  const result = isRecord(resultData) ? resultData : null;
  const followUp = result?.completion_follow_up;
  if (!isRecord(followUp) || followUp.status !== 'degraded' || !Array.isArray(followUp.issues)) {
    return false;
  }

  return followUp.issues.some((issue) => {
    if (!isRecord(issue)) return false;
    return issue.step === 'timeline_placement'
      && issue.code === 'automatic_timeline_placement_retired';
  });
}

/**
 * Project one task/output pair into the bounded legacy recovery affordance.
 * A failed or still-running task is never presented as a successful retained
 * output, and no timeline owner, variant, approval, or destination is inferred.
 */
export function getLegacyAutoPlacementPresentation(
  task: LegacyAutoPlacementTaskInput,
): LegacyAutoPlacementPresentation | null {
  if (task.status !== 'Complete' || !task.hasAsset) {
    return null;
  }

  if (task.generationIntent != null || task.params.generation_intent != null) {
    return null;
  }

  // Request parameters survive successful historical placement and can also be
  // retained by modern requests. Intent alone says nothing about the outcome.
  const retired = hasRetiredCompletionMarker(task.resultData);
  if (!retired && !hasLegacyPlacementIntent(task.params)) {
    return null;
  }

  return {
    taskId: task.id,
    label: retired ? LEGACY_AUTO_PLACEMENT_LABEL : LEGACY_UNCONFIRMED_PLACEMENT_LABEL,
    assetRetained: true,
    action: 'place-manually',
  };
}
