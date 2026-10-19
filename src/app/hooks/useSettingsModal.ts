import { useState, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import {
  useSettingsEventIntent,
  useSettingsRouteIntent,
} from '@/app/hooks/useSettingsModalIntents';

export function useSettingsModal() {
  const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
  const [settingsInitialTab, setSettingsInitialTab] = useState<string | undefined>(undefined);
  const location = useLocation();

  const handleOpenSettings = useCallback((initialTab?: string) => {
    setSettingsInitialTab(initialTab);
    setIsSettingsModalOpen(true);
  }, []);

  useSettingsRouteIntent(location.state, useCallback(({ settingsTab }) => {
    handleOpenSettings(settingsTab);
  }, [handleOpenSettings]));

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
