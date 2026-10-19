import { useState, useCallback } from 'react';
import { useSettingsEventIntent } from '@/app/hooks/useSettingsModalIntents';

export function useSettingsModal() {
  const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
  const [settingsInitialTab, setSettingsInitialTab] = useState<string | undefined>(undefined);

  const handleOpenSettings = useCallback((initialTab?: string) => {
    setSettingsInitialTab(initialTab);
    setIsSettingsModalOpen(true);
  }, []);

  useSettingsEventIntent(useCallback(({ settingsTab }) => {
    handleOpenSettings(settingsTab);
  }, [handleOpenSettings]));

  return {
    isSettingsModalOpen,
    setIsSettingsModalOpen,
    settingsInitialTab,
    handleOpenSettings,
  };
}
