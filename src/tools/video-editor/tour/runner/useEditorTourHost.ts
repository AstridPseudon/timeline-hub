import { useEffect } from 'react';
import { registerEditorTourOverlay } from '../timeline/editorTourSlot.tsx';
import { EditorTourRunner } from './EditorTourRunner';
import { useEditorTourTrigger } from './useEditorTourTrigger';

/**
 * The editor page's one hook for the tour: registers the running overlay in the page's tour slot and
 * runs the first-run trigger. `hasSelection` is the USER's project selection being mounted, not
 * whatever is mounted now, since the page mounts the demo editor while the tour runs.
 */
export function useEditorTourHost(hasSelection: boolean): void {
  useEffect(() => {
    registerEditorTourOverlay(EditorTourRunner);
    return () => registerEditorTourOverlay(null);
  }, []);
  useEditorTourTrigger(hasSelection);
}
