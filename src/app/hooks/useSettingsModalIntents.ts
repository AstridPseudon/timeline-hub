import { useCallback, useEffect } from 'react';
import { useAppEventListener } from '@/shared/lib/typedEvents';

interface SettingsLocationState {
  openSettings?: boolean;
  settingsTab?: string;
}

interface SettingsModalIntent {
  settingsTab?: string;
}

function parseSettingsLocationState(state: unknown): SettingsLocationState | null {
  if (!state || typeof state !== 'object') return null;
  const record = state as Record<string, unknown>;

  return {
    openSettings: record.openSettings === true,
    settingsTab: typeof record.settingsTab === 'string' ? record.settingsTab : undefined,
  };
}

function clearSettingsLocationIntent(): void {
  window.history.replaceState({}, document.title);
}

export function useSettingsRouteIntent(
  routeState: unknown,
  onIntent: (intent: SettingsModalIntent) => void,
): void {
  useEffect(() => {
    const parsed = parseSettingsLocationState(routeState);
    if (!parsed?.openSettings) return;

    onIntent({ settingsTab: parsed.settingsTab });
    clearSettingsLocationIntent();
  }, [routeState, onIntent]);
}

export function useSettingsEventIntent(
  onIntent: (intent: SettingsModalIntent) => void,
): void {
  const handleOpenSettingsEvent = useCallback(({ tab }: { tab?: string }) => {
    onIntent({ settingsTab: tab });
  }, [onIntent]);

  useAppEventListener('openSettings', handleOpenSettingsEvent);
}
