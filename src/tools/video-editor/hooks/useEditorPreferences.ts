import { useCallback } from 'react';
import { useEditorSettings } from '@/tools/video-editor/settings/useEditorSettings.ts';

export type ClipTab = 'effects' | 'timing' | 'position' | 'audio' | 'text';
export type RightPanelLayoutSlot = 'compact' | 'dock';

export interface EditorPreferences {
  scaleWidth: number;
  activeClipTab: ClipTab;
  /** The selected host panel; null closes its surface without discarding its state. */
  selectedRightPanelId: string | null;
  /** User-selected placement, scoped to qualified panel contribution IDs. */
  rightPanelLayoutSlotsByPanelId: Record<string, RightPanelLayoutSlot>;
  /** Data-kind lanes are optional and start hidden. */
  showDataLanes: boolean;
  assetPanel: {
    showAll: boolean;
    showHidden: boolean;
    hidden: string[];
  };
}

export const defaultPreferences: EditorPreferences = {
  scaleWidth: 160,
  activeClipTab: 'effects',
  selectedRightPanelId: 'host:properties',
  rightPanelLayoutSlotsByPanelId: {},
  showDataLanes: false,
  assetPanel: {
    showAll: false,
    showHidden: false,
    hidden: [],
  },
};

function normalizePreferences(value: EditorPreferences): EditorPreferences {
  // Older per-timeline records predate the panel fields. Fill only missing
  // fields so a saved user selection (including null/closed) survives reload.
  return {
    ...defaultPreferences,
    ...value,
    selectedRightPanelId: value.selectedRightPanelId === undefined
      ? defaultPreferences.selectedRightPanelId
      : value.selectedRightPanelId,
    rightPanelLayoutSlotsByPanelId: {
      ...defaultPreferences.rightPanelLayoutSlotsByPanelId,
      ...(value.rightPanelLayoutSlotsByPanelId ?? {}),
    },
    showDataLanes: value.showDataLanes ?? defaultPreferences.showDataLanes,
    assetPanel: {
      ...defaultPreferences.assetPanel,
      ...value.assetPanel,
      hidden: [...(value.assetPanel?.hidden ?? defaultPreferences.assetPanel.hidden)],
    },
  };
}

export function useEditorPreferences(timelineId: string) {
  const [preferences, setPreferences] = useEditorSettings<EditorPreferences>(
    `video-editor:preferences:${timelineId}`,
    defaultPreferences,
  );

  const normalizedPreferences = normalizePreferences(preferences);

  const scale = 5;
  const scaleWidth = normalizedPreferences.scaleWidth;

  const setScaleWidth = useCallback((updater: number | ((value: number) => number)) => {
    setPreferences((current) => ({
      ...normalizePreferences(current),
      scaleWidth: typeof updater === 'function' ? (updater as (value: number) => number)(current.scaleWidth) : updater,
    }));
  }, [setPreferences]);

  const setActiveClipTab = useCallback((tab: ClipTab) => {
    setPreferences((current) => ({
      ...normalizePreferences(current),
      activeClipTab: tab,
    }));
  }, [setPreferences]);

  const setAssetPanelState = useCallback((patch: Partial<EditorPreferences['assetPanel']>) => {
    setPreferences((current) => ({
      ...normalizePreferences(current),
      assetPanel: {
        ...normalizePreferences(current).assetPanel,
        ...patch,
      },
    }));
  }, [setPreferences]);

  const setSelectedRightPanelId = useCallback((selectedRightPanelId: string | null) => {
    setPreferences((current) => ({ ...normalizePreferences(current), selectedRightPanelId }));
  }, [setPreferences]);

  const setRightPanelLayoutSlot = useCallback((panelId: string, slot: RightPanelLayoutSlot) => {
    setPreferences((current) => {
      const normalized = normalizePreferences(current);
      return {
        ...normalized,
        rightPanelLayoutSlotsByPanelId: {
          ...normalized.rightPanelLayoutSlotsByPanelId,
          [panelId]: slot,
        },
      };
    });
  }, [setPreferences]);

  const setShowDataLanes = useCallback((showDataLanes: boolean) => {
    setPreferences((current) => ({ ...normalizePreferences(current), showDataLanes }));
  }, [setPreferences]);

  return {
    preferences: normalizedPreferences,
    scaleWidth,
    scale,
    setScaleWidth,
    setActiveClipTab,
    setAssetPanelState,
    setSelectedRightPanelId,
    setRightPanelLayoutSlot,
    setShowDataLanes,
  };
}
