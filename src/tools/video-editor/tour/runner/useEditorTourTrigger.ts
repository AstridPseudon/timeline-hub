import { useIsMobile, useIsTablet, useViewportWidth, isTabletHardware } from '@/shared/hooks/mobile';
import { resolveTimelineDeviceClass } from '../../lib/mobile-interaction-model';

/** The same desktop test the editor itself uses to choose its layout. */
export function useIsDesktopEditor(): boolean {
  const isMobile = useIsMobile();
  const isTablet = useIsTablet();
  const viewportWidth = useViewportWidth();
  return resolveTimelineDeviceClass({ isMobile, isTablet, viewportWidth, isTabletHardware: isTabletHardware() }) === 'desktop';
}
