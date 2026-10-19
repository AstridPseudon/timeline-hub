import { isInvalidTimelineRowTarget } from '@/tools/video-editor/lib/drop-position.ts';
import { captureClipMove, submitClipMove, type CapturedClipMove, type ClipMoveCapturePort } from '../commands/semanticGestures.ts';
import { userSelectTimelineClip } from '@/shared/state/selectionStore.ts';
import type { DropPosition } from '@/tools/video-editor/lib/drop-position.ts';
import type { ClipDragPlan } from '@/tools/video-editor/lib/clip-drag-planner.ts';
import type { TimelineInputModality } from '@/tools/video-editor/lib/mobile-interaction-model.ts';
import {
  CLIP_ACTION_SELECTOR,
  CLIP_ID_DATASET_KEY,
  ROW_ID_DATASET_KEY,
} from '@/tools/video-editor/lib/timeline-dom.ts';
import type { ClipOffset } from '@/tools/video-editor/lib/multi-drag-utils.ts';
import {
  findEnclosingPinnedGroup,
  resolveGroupTrackId,
} from '@/tools/video-editor/lib/pinned-group-projection.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { TrackKind } from '@/tools/video-editor/types/index.ts';
import type { TimelineAction } from '@/tools/video-editor/types/timeline-canvas.ts';

export interface ActionDragState {
  rowId: string;
  initialStart: number;
  initialEnd: number;
  latestStart: number;
  latestEnd: number;
}

export interface GroupDragEntry {
  groupKey: { shotId: string; trackId: string };
  originStart: number;
  originTrackId: string;
}

export interface DragSession {
  clipId: string;
  draggedClipIds: string[];
  groupDragEntry: GroupDragEntry | null;
}

export interface InternalDragSession extends DragSession {
  pointerId: number;
  sourceRowId: string;
  sourceKind: TrackKind;
  clipOffsets: ClipOffset[];
  ctrlKey: boolean;
  metaKey: boolean;
  wasSelectedOnPointerDown: boolean;
  startClientX: number;
  startClientY: number;
  pointerOffsetX: number;
  pointerOffsetY: number;
  pointerCoordinateYOffset: number;
  clipDuration: number;
  clipEl: HTMLElement;
  inputModality: TimelineInputModality;
  floatingGhostEl: HTMLElement | null;
  countBadgeEl: HTMLSpanElement | null;
  dragAllowed: boolean;
  hasMoved: boolean;
  claimedGestureOwner: boolean;
  transactionId: string;
  moveCapture?: CapturedClipMove;
  moveCaptureError?: string;
}

export interface DragIntent {
  readonly pointerId: number;
  readonly clipId: string;
  readonly sourceRowId: string;
  readonly sourceKind: TrackKind;
  readonly draggedClipIds: readonly string[];
  readonly clipOffsets: readonly ClipOffset[];
  readonly ctrlKey: boolean;
  readonly metaKey: boolean;
  readonly wasSelectedOnPointerDown: boolean;
  readonly startClientX: number;
  readonly startClientY: number;
  readonly pointerOffsetX: number;
  readonly pointerOffsetY: number;
  readonly pointerCoordinateYOffset: number;
  readonly clipDuration: number;
  readonly inputModality: TimelineInputModality;
  readonly dragAllowed: boolean;
  readonly transactionId: string;
  readonly groupDragEntry: GroupDragEntry | null;
}

export type DragMachineState =
  | { phase: 'idle' }
  | { phase: 'pending'; controller: AbortController; intent: DragIntent; session: InternalDragSession }
  | { phase: 'dragging'; controller: AbortController; intent: DragIntent; session: InternalDragSession };

interface BuildPendingDragSessionArgs {
  clipId: string;
  rowId: string;
  sourceKind: TrackKind;
  sourceAction: TimelineAction;
  current: TimelineData;
  clipTarget: HTMLElement;
  labelTarget: HTMLElement | null;
  event: PointerEvent;
  selectedClipIds: Set<string>;
  additiveSelection: boolean;
  dragAllowed: boolean;
  inputModality: TimelineInputModality;
  pixelsPerSecond: number;
  clipMove?: ClipMoveCapturePort;
}

interface BuildPendingDragSessionResult {
  actionDragState: ActionDragState;
  intent: DragIntent;
  session: InternalDragSession;
}

interface CommitDraggingSessionArgs {
  session: InternalDragSession;
  nextStart: number;
  dropPosition: DropPosition | null;
  crossTrackActive: boolean;
  lastPlan?: ClipDragPlan | null;
}

export function findClipElement(
  wrapper: HTMLDivElement,
  clipId: string,
  rowId: string,
): HTMLElement | null {
  const candidates = wrapper.querySelectorAll<HTMLElement>(CLIP_ACTION_SELECTOR);
  for (const candidate of candidates) {
    if (candidate.dataset[CLIP_ID_DATASET_KEY] === clipId && candidate.dataset[ROW_ID_DATASET_KEY] === rowId) {
      return candidate;
    }
  }
  return null;
}

export function updateFloatingGhostPosition(
  session: InternalDragSession,
  clientX: number,
  clientY: number,
): void {
  if (!session.floatingGhostEl) return;
  const adjustedClientY = clientY + session.pointerCoordinateYOffset;
  session.floatingGhostEl.style.left = `${clientX - session.pointerOffsetX}px`;
  session.floatingGhostEl.style.top = `${adjustedClientY - session.pointerOffsetY}px`;
}

export function createFloatingGhost(clipEl: HTMLElement): HTMLElement {
  const rect = clipEl.getBoundingClientRect();
  const el = clipEl.cloneNode(true) as HTMLElement;
  el.classList.add('cross-track-ghost');
  el.style.width = `${rect.width}px`;
  el.style.height = `${rect.height}px`;
  document.body.appendChild(el);
  return el;
}

export function ensureCountBadge(session: InternalDragSession): void {
  if (session.draggedClipIds.length <= 1 || session.countBadgeEl) {
    return;
  }

  const badge = document.createElement('span');
  badge.className = 'pointer-events-none absolute right-1 top-1 rounded-full bg-primary px-1.5 py-0.5 text-[10px] font-semibold leading-none text-primary-foreground shadow-sm';
  badge.textContent = `${session.draggedClipIds.length} clips`;
  session.clipEl.appendChild(badge);
  session.countBadgeEl = badge;
}

export function buildClipOffsets(
  current: TimelineData,
  draggedClipIds: readonly string[],
  anchorInitialStart: number,
): ClipOffset[] {
  return draggedClipIds.flatMap((draggedClipId) => {
    for (const row of current.rows) {
      const action = row.actions.find((candidate) => candidate.id === draggedClipId);
      if (action) {
        return [{
          clipId: draggedClipId,
          rowId: row.id,
          deltaTime: action.start - anchorInitialStart,
          initialStart: action.start,
          initialEnd: action.end,
        }];
      }
    }

    return [];
  });
}

export function buildPendingDragSession({
  clipId,
  rowId,
  sourceKind,
  sourceAction,
  current,
  clipTarget,
  labelTarget,
  event,
  selectedClipIds,
  additiveSelection,
  dragAllowed,
  inputModality,
  pixelsPerSecond,
  clipMove,
}: BuildPendingDragSessionArgs): BuildPendingDragSessionResult {
  const enclosingGroup = findEnclosingPinnedGroup(current.config, clipId);
  const clipRect = clipTarget.getBoundingClientRect();
  const pointerCoordinateYOffset = labelTarget
    ? clipRect.top - labelTarget.getBoundingClientRect().top
    : 0;
  const adjustedStartClientY = event.clientY + pointerCoordinateYOffset;

  let groupLiveStart = sourceAction.start;
  let groupLiveEnd = sourceAction.end;
  if (enclosingGroup) {
    const memberActions: { start: number; end: number }[] = [];
    for (const row of current.rows) {
      for (const action of row.actions) {
        if (enclosingGroup.group.clipIds.includes(action.id)) {
          memberActions.push({ start: action.start, end: action.end });
        }
      }
    }
    if (memberActions.length > 0) {
      groupLiveStart = Math.min(...memberActions.map((action) => action.start));
      groupLiveEnd = Math.max(...memberActions.map((action) => action.end));
    }
  }

  const initialStart = enclosingGroup ? groupLiveStart : sourceAction.start;
  const clipDuration = enclosingGroup
    ? (groupLiveEnd - groupLiveStart)
    : (sourceAction.end - sourceAction.start);
  const shouldDragSelectedSet = additiveSelection && selectedClipIds.has(clipId);
  const draggedClipIds = enclosingGroup
    ? shouldDragSelectedSet
      ? [
          ...enclosingGroup.group.clipIds,
          ...[...selectedClipIds].filter((selectedClipId) => !enclosingGroup.group.clipIds.includes(selectedClipId)),
        ]
      : [...enclosingGroup.group.clipIds]
    : shouldDragSelectedSet
      ? [clipId, ...[...selectedClipIds].filter((selectedClipId) => selectedClipId !== clipId)]
      : [clipId];
  const clipOffsets = buildClipOffsets(current, draggedClipIds, initialStart);
  const validDraggedClipIds = clipOffsets.map(({ clipId: draggedClipId }) => draggedClipId);
  const groupDragEntry = enclosingGroup
    ? {
        groupKey: enclosingGroup.groupKey,
        originStart: groupLiveStart,
        originTrackId: resolveGroupTrackId(enclosingGroup.group, current.rows),
      }
    : null;
  const transactionId = crypto.randomUUID();
  let moveCapture: CapturedClipMove | undefined;
  let moveCaptureError: string | undefined;
  try {
    if (groupDragEntry || validDraggedClipIds.length !== 1) {
      throw new Error('clip.move v1 does not support group or multi-clip moves.');
    }
    moveCapture = captureClipMove(clipMove, current, clipId);
  } catch (error) {
    moveCaptureError = error instanceof Error ? error.message : 'Clip move capture failed.';
  }

  const intent: DragIntent = {
    pointerId: event.pointerId,
    clipId,
    sourceRowId: rowId,
    sourceKind,
    draggedClipIds: validDraggedClipIds,
    clipOffsets,
    ctrlKey: event.ctrlKey,
    metaKey: event.metaKey,
    wasSelectedOnPointerDown: selectedClipIds.has(clipId),
    startClientX: event.clientX,
    startClientY: adjustedStartClientY,
    pointerOffsetX: groupDragEntry
      ? event.clientX - (clipRect.left - ((sourceAction.start - initialStart) * pixelsPerSecond))
      : event.clientX - clipRect.left,
    pointerOffsetY: adjustedStartClientY - clipRect.top,
    pointerCoordinateYOffset,
    clipDuration,
    inputModality,
    dragAllowed,
    transactionId,
    groupDragEntry,
  };

  return {
    actionDragState: {
      rowId,
      initialStart,
      initialEnd: initialStart + clipDuration,
      latestStart: initialStart,
      latestEnd: initialStart + clipDuration,
    },
    intent,
    session: {
      ...intent,
      moveCapture,
      moveCaptureError,
      draggedClipIds: [...intent.draggedClipIds],
      clipOffsets: [...clipOffsets],
      clipEl: clipTarget,
      floatingGhostEl: null,
      countBadgeEl: null,
      hasMoved: false,
      claimedGestureOwner: false,
    },
  };
}

export function commitDraggingSession({
  session,
  nextStart,
  dropPosition,
  crossTrackActive,
  lastPlan,
}: CommitDraggingSessionArgs): { deferDeactivate: boolean; refusal?: string } {
  const refuse = (refusal: string) => ({ deferDeactivate: false, refusal });
  const plan = lastPlan ?? dropPosition?.plan;
  if (isInvalidTimelineRowTarget(plan?.rejectReason) || dropPosition?.isReject
    || plan?.rejectReason || plan?.valid === false) {
    return refuse('The clip drop target is unavailable.');
  }
  if (session.groupDragEntry || session.draggedClipIds.length !== 1) {
    return refuse('clip.move v1 does not support group or multi-clip moves.');
  }
  if (dropPosition?.isNewTrack || plan?.needsNewTrack) {
    return refuse('clip.move v1 does not create tracks.');
  }
  // The published built-in capture has no sibling/hard-wall snap query yet.
  // Do not turn a consumed live query into unguarded absolute positioning.
  if (plan?.snapped && plan.snapEdgeType !== 'none' && plan.snapEdgeType !== 'timeline-start') {
    return refuse('clip.move v1 cannot capture this snap query.');
  }
  if (!session.moveCapture) return refuse(session.moveCaptureError ?? 'clip.move capture is unavailable.');
  const targetTrackId = plan?.targetTrackId ?? dropPosition?.trackId ?? session.sourceRowId;
  try {
    submitClipMove(session.moveCapture, plan?.resolvedStart ?? nextStart, {
      trackId: targetTrackId,
      transactionId: session.transactionId,
    });
    userSelectTimelineClip(session.clipId, { additive: false });
    return { deferDeactivate: crossTrackActive };
  } catch (error) {
    return refuse(error instanceof Error ? error.message : 'Clip move failed.');
  }
}
