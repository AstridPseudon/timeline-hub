import React, { useEffect } from 'react';
import { useLocation, Navigate } from 'react-router-dom';
import { TasksPane } from '@/features/tasks/components/TasksPane/TasksPane';
import { GenerationsPane } from '@/features/gallery/components/GenerationsPane/GenerationsPane';
import { EditorPane } from '@/features/editor/components/EditorPaneTab';
import { ToolsPane } from '@/shared/components/ToolsPane/ToolsPane';
import { AstridLoading } from '@/shared/components/AstridLoading';
import { SettingsModal } from '@/shared/components/SettingsModal/SettingsModal';
import { OnboardingModal } from '@/shared/components/modals/OnboardingModal';
import { ChunkLoadErrorBoundary } from '@/shared/runtime/ChunkLoadErrorBoundary';
import { dispatchAppEvent } from '@/shared/lib/typedEvents';

// Lazy load ProductTour since it only shows during onboarding
const LazyProductTour = React.lazy(() =>
  import('@/shared/components/ProductTour').then(module => ({
    default: module.ProductTour
  }))
);
import { useIsMobile, useIsTablet } from '@/shared/hooks/mobile';
import { cn } from '@/shared/components/ui/contracts/cn';
import { useVideoEditorRouteState } from '@/app/hooks/useVideoEditorRouteState';
import { SocialIcons } from './components/SocialIcons';

import { useAuth } from '@/shared/contexts/AuthContext';
import { APP_ENTRY_PATH, prefersAppEntry } from './entryClassification.ts';
import { useSplitViewScroll } from './hooks/useSplitViewScroll';
import { useGlobalPaneShortcuts } from './hooks/useGlobalPaneShortcuts';
import { useSettingsModal } from './hooks/useSettingsModal';
import { useOnboardingFlow } from './hooks/useOnboardingFlow';
import { useResetCurrentShotOnRouteChange } from './hooks/useResetCurrentShotOnRouteChange';
import { useTextCase } from '@/shared/hooks/useTextCase';
import { LayoutMainContent } from './components/LayoutMainContent';
import { usePanesStore } from '@/shared/state/panesStore';
import { AppSkyBackground } from '@/shared/components/TimeOfDay/TimeOfDayControl';

// Scroll to top component
function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
    // Also dispatch event for custom scroll containers
    dispatchAppEvent('app:scrollToTop', { behavior: 'auto' });
  }, [pathname]);

  return null;
}

/** Provider-level Runtime and document gates already hold this shell until identity is resolved. */
export const Layout: React.FC = () => <LayoutShell />;

const LayoutShell: React.FC = () => {
  const { isVideoEditorShellActive } = useVideoEditorRouteState();
  const isTasksPaneLocked = usePanesStore((state) => state.isTasksPaneLocked);
  const tasksPaneWidth = usePanesStore((state) => state.tasksPaneWidth);
  const isShotsPaneLocked = usePanesStore((state) => state.isShotsPaneLocked);
  const shotsPaneWidth = usePanesStore((state) => state.shotsPaneWidth);
  const isGenerationsPaneLocked = usePanesStore((state) => state.isGenerationsPaneLocked);
  const generationsPaneHeight = usePanesStore((state) => state.generationsPaneHeight);

  // Mobile detection for split-view scroll handling
  const isMobile = useIsMobile();
  const isTablet = useIsTablet();
  const isSmallMobile = isMobile && !isTablet;

  // On small mobile with locked generations pane, create split-view scroll behavior
  const isMobileSplitView = isSmallMobile && isGenerationsPaneLocked && !isVideoEditorShellActive;

  // Extracted hooks
  const { splitViewWrapperRef } = useSplitViewScroll(isMobileSplitView);
  const { isAuthenticated, isLoading } = useAuth();
  const { preserveUserText, setPreserveUserText } = useTextCase();
  const { isSettingsModalOpen, setIsSettingsModalOpen, settingsInitialTab } = useSettingsModal();
  const { showOnboardingModal, onboardingMode, handleOnboardingClose } = useOnboardingFlow();
  useResetCurrentShotOnRouteChange();
  useGlobalPaneShortcuts();

  // Show loading spinner while determining auth state
  // (isLoading is always false here because AuthGate gates on it, but kept for safety)
  if (isLoading) {
    return (
      <AstridLoading />
    );
  }

  // Redirect unauthenticated users to home page (same-origin builds only: on the hosted
  // build `RuntimeConnectionGate` above has already held the shell until the Runtime
  // answered, and a connected gate is an authenticated session, so this never fires there).
  // /home is always the public landing page.
  //
  // Someone who installed Astrid or chose to use it in the browser never lands back on the
  // landing page: they go to the local editor, which this gate lets through.
  if (!isAuthenticated) {
    if (prefersAppEntry()) return <Navigate to={APP_ENTRY_PATH} replace />;
    return <Navigate to="/home" replace state={{ fromProtected: true }} />;
  }

  // Footer style matches main content margins for side panes
  const footerStyle = {
    marginRight: isTasksPaneLocked ? `${tasksPaneWidth}px` : '0px',
    marginLeft: isShotsPaneLocked ? `${shotsPaneWidth}px` : '0px',
    willChange: 'margin',
  } as React.CSSProperties;

  // Style for the scroll wrapper when in mobile split view
  // This wraps both header and content so they scroll together
  const splitViewWrapperStyle: React.CSSProperties = isMobileSplitView ? {
    height: `calc(100dvh - ${generationsPaneHeight}px)`,
    overflowY: 'auto',
    overscrollBehavior: 'contain',
    WebkitOverflowScrolling: 'touch',
  } : {};

  const mainContent = (
    <LayoutMainContent isMobileSplitView={isMobileSplitView} />
  );

  return (
    <div className={cn('relative flex min-h-screen flex-col', isVideoEditorShellActive && 'h-dvh min-h-0 overflow-hidden')}>
      <ScrollToTop />
      <AppSkyBackground />

      {/* When in mobile split view, wrap header + content in a scroll container */}
      {isMobileSplitView ? (
        <div ref={splitViewWrapperRef} style={splitViewWrapperStyle}>
          {mainContent}
        </div>
      ) : (
        mainContent
      )}

      {/* The local Astrid App hides the legacy tool-navigation sidebar. The
          task/status and editor panes remain available to the user. */}
      <>
        <EditorPane />
        <TasksPane />
        <ToolsPane />
        <GenerationsPane />
      </>

      {/* Social Icons Footer */}
      {!isVideoEditorShellActive && (
        <div
          className="relative transition-[margin] duration-300 ease-smooth"
          style={footerStyle}
        >
          <SocialIcons />
        </div>
      )}

      {/* App-shell modals. Local mode renders them too; their content
          degrades to empty/disabled states without account data. */}
      <SettingsModal
        isOpen={isSettingsModalOpen}
        onOpenChange={setIsSettingsModalOpen}
        initialTab={settingsInitialTab}
        preserveUserText={preserveUserText}
        setPreserveUserText={setPreserveUserText}
      />

      {/* Onboarding Modal */}
      <OnboardingModal
        isOpen={showOnboardingModal}
        mode={onboardingMode}
        onClose={handleOnboardingClose}
      />

      {/* Product Tour - lazy loaded since only needed during onboarding */}
      <ChunkLoadErrorBoundary>
        <React.Suspense fallback={null}>
          <LazyProductTour />
        </React.Suspense>
      </ChunkLoadErrorBoundary>
    </div>
  );
};
