import type { TaskStatus } from '@/types/tasks';

export const LEGACY_AUTO_PLACEMENT_LABEL = 'Not placed: place manually';

interface LegacyAutoPlacementTaskInput {
  id: string;
  status: TaskStatus;
  params: Record<string, unknown>;
  /**
   * The legacy complete_task result_data projection, when a caller has it.
   * Current task-list mappers do not carry this marker to TaskItem. Until a
   * supported read supplies it, the not-placed label must remain inactive.
   */
  resultData?: unknown;
  hasAsset: boolean;
}

export interface LegacyAutoPlacementPresentation {
  taskId: string;
  label: typeof LEGACY_AUTO_PLACEMENT_LABEL;
  /** The completed output remains available to the existing gallery/lightbox. */
  assetRetained: true;
  action: 'place-manually';
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
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

  // Request parameters survive successful historical placement and can also be
  // retained by modern requests. Intent alone says nothing about the outcome.
  if (!hasRetiredCompletionMarker(task.resultData)) {
    return null;
  }

  return {
    taskId: task.id,
    label: LEGACY_AUTO_PLACEMENT_LABEL,
    assetRetained: true,
    action: 'place-manually',
  };
}
