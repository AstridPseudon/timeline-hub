import { useCallback, useEffect, useMemo, useState } from 'react';
import { useUserUIState } from '@/shared/hooks/useUserUIState';
import { useIsMobile, useIsTablet } from '@/shared/hooks/mobile';
import { usePaneControlsHosted } from '@/shared/state/paneControlsHost';

type PaneLockKey = 'shots' | 'tasks' | 'gens' | 'editor';

interface PaneLocksState {
  shots: boolean;
  tasks: boolean;
  gens: boolean;
  editor: boolean;
}

const UNLOCKED_PANES: PaneLocksState = {
  shots: false,
  tasks: false,
  gens: false,
  editor: false,
};

export function usePaneLockPolicyState() {
  const isMobile = useIsMobile();
  const isTablet = useIsTablet();
  // Phones, and pages that host the pane entry points themselves (paneControlsHost.ts),
  // never lock panes. A lock saved elsewhere is kept, not applied, and returns on leaving.
  const paneControlsHosted = usePaneControlsHosted();
  const transientPanes = (isMobile && !isTablet) || paneControlsHosted;

  const { value: paneLocks, update: savePaneLocks, isLoading } = useUserUIState('paneLocks', UNLOCKED_PANES);
  const [locks, setLocks] = useState(paneLocks);

  const [isGenerationsPaneOpenState, setIsGenerationsPaneOpenState] = useState(false);
  const [isEditorPaneOpenState, setIsEditorPaneOpenState] = useState(false);
  const [isTasksPaneOpenState, setIsTasksPaneOpenState] = useState(false);

  useEffect(() => {
    if (transientPanes) {
      setLocks(UNLOCKED_PANES);
      // A Tasks pane held open by a saved lock closes with it.
      setIsTasksPaneOpenState(false);
      return;
    }

    if (!isLoading) {
      let newLocks = paneLocks;
      if (isTablet) {
        const activeLocks = Object.entries(paneLocks).filter(([_, locked]) => locked);
        if (activeLocks.length > 1) {
          const firstLocked = activeLocks[0][0] as PaneLockKey;
          newLocks = {
            shots: firstLocked === 'shots',
            tasks: firstLocked === 'tasks',
            gens: firstLocked === 'gens',
            editor: firstLocked === 'editor',
          };
        }
      }
      setLocks(newLocks);
      setIsTasksPaneOpenState(newLocks.tasks);
    }
  }, [isLoading, paneLocks, transientPanes, isTablet]);

  const createPaneLockSetter = useCallback(
    (lockKey: PaneLockKey) => (isLocked: boolean) => {
      if (typeof isLocked !== 'boolean') {
        return;
      }
      setLocks((prev) => {
        if (prev[lockKey] === isLocked) return prev;
        const exclusiveLock = (isMobile || isTablet) && isLocked;
        return exclusiveLock
          ? { ...UNLOCKED_PANES, [lockKey]: isLocked }
          : { ...prev, [lockKey]: isLocked };
      });

      if (!transientPanes) {
        const exclusiveLock = (isMobile || isTablet) && isLocked;
        savePaneLocks(
          exclusiveLock
            ? { ...UNLOCKED_PANES, [lockKey]: isLocked }
            : { [lockKey]: isLocked },
        );
      }

      if (lockKey === 'tasks') {
        setIsTasksPaneOpenState(isLocked);
      } else if ((isMobile || isTablet) && isLocked) {
        setIsTasksPaneOpenState(false);
      }
    },
    [isMobile, isTablet, transientPanes, savePaneLocks],
  );

  const setIsGenerationsPaneLocked = useMemo(() => createPaneLockSetter('gens'), [createPaneLockSetter]);
  const setIsEditorPaneLocked = useMemo(() => createPaneLockSetter('editor'), [createPaneLockSetter]);
  const setIsShotsPaneLocked = useMemo(() => createPaneLockSetter('shots'), [createPaneLockSetter]);
  const setIsTasksPaneLocked = useMemo(() => createPaneLockSetter('tasks'), [createPaneLockSetter]);

  const setIsGenerationsPaneOpen = useCallback((isOpen: boolean) => {
    setIsGenerationsPaneOpenState(isOpen);
  }, []);

  const setIsEditorPaneOpen = useCallback((isOpen: boolean) => {
    setIsEditorPaneOpenState(isOpen);
  }, []);

  const setIsTasksPaneOpen = useCallback((isOpen: boolean) => {
    if (!transientPanes) {
      setIsTasksPaneOpenState(isOpen);
    }
  }, [transientPanes]);

  const resetAllPaneLocks = useCallback(() => {
    setLocks(UNLOCKED_PANES);
    setIsTasksPaneOpenState(false);
    savePaneLocks(UNLOCKED_PANES);
  }, [savePaneLocks]);

  return {
    locks,
    isGenerationsPaneOpenState,
    isEditorPaneOpenState,
    isTasksPaneOpenState,
    setIsGenerationsPaneLocked,
    setIsEditorPaneLocked,
    setIsShotsPaneLocked,
    setIsTasksPaneLocked,
    setIsGenerationsPaneOpen,
    setIsEditorPaneOpen,
    setIsTasksPaneOpen,
    resetAllPaneLocks,
  };
}
