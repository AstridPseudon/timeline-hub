import { editTranscriptText, type TranscriptTextEdit, type TranscriptTextEditResult } from '@/tools/video-editor/data/typed/editTranscript.ts';
import type { CommitDataOptions } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import type { TimelineData } from './timeline-data.ts';
import type { TimelineEditability } from './timeline-editability.ts';
import { buildDataFromCurrentRegistry } from './timeline-save-utils.ts';

export type CommitTranscriptTextEditResult = TranscriptTextEditResult
  | { ok: false; code: 'timeline_unavailable' | 'timeline_read_only'; message: string };

/** Host-only adapter: one source correction enters the existing save/history/CAS path. */
export function commitTranscriptTextEdit(
  context: {
    dataRef: { current: TimelineData | null };
    commitData: (next: TimelineData, options?: CommitDataOptions) => void;
    editability?: TimelineEditability;
  },
  edit: TranscriptTextEdit,
): CommitTranscriptTextEditResult {
  const current = context.dataRef.current;
  if (!current) return { ok: false, code: 'timeline_unavailable', message: 'Wait for the timeline to finish loading before correcting text.' };
  const permission = context.editability?.checkTimeline?.();
  if (permission && !permission.allowed) {
    return { ok: false, code: 'timeline_read_only', message: 'This timeline is currently read-only. Finish the active edit or reopen it with editing access.' };
  }
  const result = editTranscriptText(current.sourceItemsBySchemaRef, edit);
  if (!result.ok || !result.changed) return result;
  const next = buildDataFromCurrentRegistry(current.config, current, {
    sourceItemsBySchemaRef: result.sourceItemsBySchemaRef,
  });
  context.commitData(next, { semantic: true });
  return result;
}
