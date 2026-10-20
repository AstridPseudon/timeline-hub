import type { CSSProperties } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { AppHeader } from '@/shared/components/AppHeader.tsx';
import { useHeaderState } from '@/shared/contexts/ToolPageHeaderContext';
import { useHomeNavigation } from '@/shared/hooks/useHomeNavigation';
import { isHomeToolPathActive } from '@/shared/lib/tooling/homeNavigation';
import { useViewportResponsive } from '@/shared/hooks/responsive/useViewportResponsive';
import { cn } from '@/shared/components/ui/contracts/cn';
import { useVideoEditorRouteState } from '@/app/hooks/useVideoEditorRouteState';
import { usePanesStore } from '@/shared/state/panesStore';
import { usePaneControlsHosted } from '@/shared/state/paneControlsHost';
import { TOOL_ROUTES } from '@/shared/lib/tooling/toolRoutes';

interface LayoutMainContentProps {
  isMobileSplitView: boolean;
}

export function LayoutMainContent(props: LayoutMainContentProps) {
  const { isMobileSplitView } = props;
  const { pathname } = useLocation();
  const { isEditorRoute, isVideoEditorShellActive } = useVideoEditorRouteState();
  const isFullEditorSurface = isVideoEditorShellActive;
  const { navigateHome, targetPath } = useHomeNavigation();
  const isEditorPaneLocked = usePanesStore((state) => state.isEditorPaneLocked);
  const effectiveEditorPaneHeight = usePanesStore((state) => state.effectiveEditorPaneHeight);
  const isTasksPaneLocked = usePanesStore((state) => state.isTasksPaneLocked);
  const tasksPaneWidth = usePanesStore((state) => state.tasksPaneWidth);
  const isShotsPaneLocked = usePanesStore((state) => state.isShotsPaneLocked);
  const shotsPaneWidth = usePanesStore((state) => state.shotsPaneWidth);
  const isGenerationsPaneLocked = usePanesStore((state) => state.isGenerationsPaneLocked);
  const isGenerationsPaneOpen = usePanesStore((state) => state.isGenerationsPaneOpen);
  const effectiveGenerationsPaneHeight = usePanesStore((state) => state.effectiveGenerationsPaneHeight);
  // A page that hosts the pane entry points gets the gallery as a sheet over it, not a pane that pushes it up.
  const paneControlsHosted = usePaneControlsHosted();
  const { header, globalHeaderContent } = useHeaderState();
  const { isSm, isMd, isLg, isXl, is2Xl, contentWidth, contentHeight } = useViewportResponsive();

  const containerPadding = isLg ? 'px-6' : isSm ? 'px-4' : 'px-2';
  const containerSpacing = 'py-1';
  const isImageGenerationPage = pathname === TOOL_ROUTES.IMAGE_GENERATION;

  const contentStyle = {
    marginRight: isTasksPaneLocked ? `${tasksPaneWidth}px` : '0px',
    marginLeft: isShotsPaneLocked ? `${shotsPaneWidth}px` : '0px',
    paddingTop: isEditorPaneLocked && isVideoEditorShellActive ? `${effectiveEditorPaneHeight}px` : '0px',
    paddingBottom: isMobileSplitView || isImageGenerationPage || paneControlsHosted
      ? '0px'
      : ((isGenerationsPaneLocked || isGenerationsPaneOpen) ? `${effectiveGenerationsPaneHeight}px` : '0px'),
    '--content-width': `${contentWidth}px`,
    '--content-height': `${contentHeight}px`,
    '--content-sm': isSm ? '1' : '0',
    '--content-md': isMd ? '1' : '0',
    '--content-lg': isLg ? '1' : '0',
    '--content-xl': isXl ? '1' : '0',
    '--content-2xl': is2Xl ? '1' : '0',
    willChange: 'margin, padding',
  } as CSSProperties;

  return (
    <>
      <AppHeader
        navigationMode={isHomeToolPathActive(pathname, targetPath) ? 'tools' : 'home'}
        onNavigate={isEditorRoute ? undefined : navigateHome}
        navigationControls={globalHeaderContent}
        showProjectControls={!isEditorRoute}
      />

      <div
        className={cn(
          'relative z-10 content-container',
          isFullEditorSurface
            ? 'min-h-0 flex-1 overflow-hidden transition-[margin,padding] duration-300 ease-smooth'
            : 'transition-[margin,padding] duration-300 ease-smooth',
        )}
        data-video-editor-route={isEditorRoute ? 'true' : 'false'}
        data-video-editor-shell-active={isFullEditorSurface ? 'true' : 'false'}
        style={contentStyle}
      >
        <main
          className={cn(
            isFullEditorSurface
              ? 'h-full w-full overflow-hidden'
              : cn('container mx-auto', containerPadding, containerSpacing),
          )}
        >
          {!isFullEditorSurface && header}
          <Outlet />
        </main>
      </div>
    </>
  );
}
