import { useEffect } from 'react';
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

/** Starts the tour the first time the real editor is mounted with a project selection, on desktop. */
export function useEditorTourTrigger(hasSelection: boolean): void {
  const desktop = useIsDesktopEditor();
  useEffect(() => {
    startEditorTourIfFirstRun(hasSelection && desktop);
  }, [hasSelection, desktop]);
}
