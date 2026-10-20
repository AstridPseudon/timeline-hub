import { useCallback } from 'react';
import { captureClipScalarEdit } from '../commands/clipScalarGesture.ts';
import { useTimelineEditorData, useTimelineEditorOps } from './timelineStore.ts';

/** Authoring controls always capture through the host session, including when it is unavailable. */
export function useClipScalarControl(clipId: string | undefined) {
  const { dataRef } = useTimelineEditorData();
  const { clipScalar } = useTimelineEditorOps();
  return useCallback(() => {
    const current = dataRef.current;
    if (!current || !clipId) throw new Error('Select a loaded clip before editing clip fields.');
    // Resolve ownership against the capturing session's raw bundle and projection binding.
    return captureClipScalarEdit(clipScalar, current, clipId);
  }, [clipId, clipScalar, dataRef]);
}

export function useClipScalarControls(clipIds: string[]) {
  const { dataRef } = useTimelineEditorData();
  const { clipScalar } = useTimelineEditorOps();
  return useCallback(() => {
    const current = dataRef.current;
    if (!current || !clipIds.length) throw new Error('Select loaded clips before editing clip fields.');
    return clipIds.map((clipId) => captureClipScalarEdit(clipScalar, current, clipId));
  }, [clipIds, clipScalar, dataRef]);
}
