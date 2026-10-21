import { useEffect } from 'react';
import { useRuntimeGateOpen } from '@/integrations/runtime/runtimeGateOpen.tsx';
import { useIsMobile, useIsTablet, useViewportWidth, isTabletHardware } from '@/shared/hooks/mobile';
import { resolveTimelineDeviceClass } from '../../lib/mobile-interaction-model';
import { startEditorTourIfFirstRun } from './tourFlag';

/** The same desktop test the editor itself uses to choose its layout. */
export function useIsDesktopEditor(): boolean {
  const isMobile = useIsMobile();
  const isTablet = useIsTablet();
  const viewportWidth = useViewportWidth();
  return resolveTimelineDeviceClass({ isMobile, isTablet, viewportWidth, isTabletHardware: isTabletHardware() }) === 'desktop';
}

/**
 * Starts the tour the first time the real editor is mounted with a project selection, on desktop, once the connection
 * gate is open: the editor mounts beneath the connection card while it hands over, and the tour waits for it to leave.
 */
export function useEditorTourTrigger(hasSelection: boolean): void {
  const desktop = useIsDesktopEditor();
  const gateOpen = useRuntimeGateOpen();
  useEffect(() => {
    // The Runtime answers asynchronously: a change in eligibility meanwhile (or an unmount) cancels the start.
    let current = true;
    void startEditorTourIfFirstRun(hasSelection && desktop && gateOpen, () => current);
    return () => {
      current = false;
    };
  }, [hasSelection, desktop, gateOpen]);
}
