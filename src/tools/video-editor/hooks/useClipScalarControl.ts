import { useCallback } from 'react';
import { captureClipScalarEdit, type ClipScalarOwner } from '../commands/clipScalarGesture.ts';
import { useTimelineEditorData, useTimelineEditorOps } from './timelineStore.ts';

/** Authoring controls always capture through the host session, including when it is unavailable. */
export function useClipScalarControl(clipId: string | undefined) {
  const { dataRef } = useTimelineEditorData();
  const { clipScalar } = useTimelineEditorOps();
  return useCallback(() => {
    const current = dataRef.current;
    if (!current || !clipId) throw new Error('Select a loaded clip before editing clip fields.');
    const clip = current.resolvedConfig.clips.find((candidate) => candidate.id === clipId);
    const canonical = clip?.app?.canonical as { ownerRef?: unknown } | undefined;
    const owner = canonical?.ownerRef ?? 'parent';
    if (owner !== 'parent' && (typeof owner !== 'string' || !/^occurrence:[^/]+$/.test(owner))) {
      throw new Error('Clip fields require an explicit canonical owner.');
    }
    // The session validates this projection binding against the original raw bundle.
    return captureClipScalarEdit(clipScalar, current, clipId, owner as ClipScalarOwner);
  }, [clipId, clipScalar, dataRef]);
}
