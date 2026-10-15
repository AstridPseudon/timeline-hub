import { useId, useMemo, useState } from 'react';
import { PropertiesPanel } from '@/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx';
import { VideoEditorAssetPanelSurface } from '@/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx';
import { useTimelineEditorData, useTimelineEditorOps } from '@/tools/video-editor/hooks/timelineStore.ts';
import { getPanelKey } from '@/tools/video-editor/runtime/ExtensionPanelHost';
import { useVideoEditorAssetPanels } from '@/tools/video-editor/runtime/useVideoEditorRenderContext.ts';
import {
  defaultPreferences,
  type RightPanelLayoutSlot,
} from '@/tools/video-editor/hooks/useEditorPreferences.ts';
import { shellRegionAttrs } from '@/tools/video-editor/lib/timeline-dom.ts';

export const HOST_PROPERTIES_PANEL_KEY = 'host:properties';

export interface VideoEditorRightPanelDockProps {
  readonly leftPanelPresent: boolean;
  /** Narrow shell layouts show a persistent control strip and an on-demand surface. */
  readonly responsive?: boolean;
  readonly rightInset?: number;
  readonly enabled?: boolean;
}

/**
 * Host-owned selector and presentation for the existing inspector plus
 * extension panels. Its one persistent subtree moves between the compact
 * overlay and the full-height grid dock, so changing layout or selection does
 * not remount extension panels (ExtensionPanelHost hides inactive instances).
 */
export function VideoEditorRightPanelDock({
  leftPanelPresent,
  responsive = false,
  rightInset = 12,
  enabled = true,
}: VideoEditorRightPanelDockProps) {
  const panels = useVideoEditorAssetPanels();
  const selectId = useId();
  const [responsivePanelExpanded, setResponsivePanelExpanded] = useState(false);
  const data = useTimelineEditorData();
  const ops = useTimelineEditorOps();
  const preferences = data.preferences ?? defaultPreferences;
  const selectedPanelId = preferences.selectedRightPanelId;
  const availablePanelIds = useMemo(() => new Set(panels.map(getPanelKey)), [panels]);
  const selectedExtensionPanelId = selectedPanelId && availablePanelIds.has(selectedPanelId)
    ? selectedPanelId
    : null;
  const hasSelectedPanel = selectedPanelId === HOST_PROPERTIES_PANEL_KEY || selectedExtensionPanelId !== null;
  const savedSlots = Object.values(preferences.rightPanelLayoutSlotsByPanelId);
  const fallbackLayout: RightPanelLayoutSlot = preferences.rightPanelLayoutSlotsByPanelId[HOST_PROPERTIES_PANEL_KEY]
    ?? savedSlots[savedSlots.length - 1]
    ?? 'dock';
  const layout = selectedPanelId
    ? preferences.rightPanelLayoutSlotsByPanelId[selectedPanelId] ?? fallbackLayout
    : fallbackLayout;
  const panelSurfaceVisible = hasSelectedPanel && (!responsive || responsivePanelExpanded);
  const responsiveFullDock = responsive && panelSurfaceVisible && layout === 'dock';
  const fullDock = !responsive && panelSurfaceVisible && layout === 'dock';

  const selectPanel = (panelId: string | null) => {
    if (panelId && preferences.rightPanelLayoutSlotsByPanelId[panelId] === undefined) {
      ops.setRightPanelLayoutSlot(panelId, layout);
    }
    ops.setSelectedRightPanelId(panelId);
    if (responsive) setResponsivePanelExpanded(Boolean(panelId));
  };

  const selectLayout = (slot: RightPanelLayoutSlot) => {
    ops.setRightPanelLayoutSlot(selectedPanelId ?? HOST_PROPERTIES_PANEL_KEY, slot);
  };

  const compactWidth = `calc(100vw - ${12 + rightInset}px)`;
  const rootClass = responsive
    ? responsiveFullDock
      ? 'absolute z-40 flex min-h-0 min-w-0 flex-col overflow-hidden rounded-xl border border-border bg-card/95 shadow-xl'
      : `absolute z-40 flex min-w-0 flex-col overflow-hidden rounded-xl border border-border bg-card/95 shadow-xl ${panelSurfaceVisible ? 'right-3 top-3 max-h-[min(70vh,620px)]' : 'right-3 bottom-3'}`
    : fullDock
      ? 'row-span-full flex min-h-0 min-w-0 flex-col overflow-hidden rounded-xl border border-border bg-card/95'
      : 'absolute right-3 top-3 z-40 flex max-h-[min(70vh,620px)] min-w-0 flex-col overflow-hidden rounded-xl border border-border bg-card/95 shadow-xl';
  const rootStyle = responsiveFullDock
    ? {
      top: 12,
      right: rightInset,
      bottom: 12,
      left: 12,
      width: 'auto',
      maxWidth: 'none',
      maxHeight: 'none',
    }
    : responsive
      ? {
        top: panelSurfaceVisible ? 12 : undefined,
        right: rightInset,
        bottom: panelSurfaceVisible ? undefined : 12,
        width: compactWidth,
        maxWidth: 420,
        maxHeight: panelSurfaceVisible ? 'min(70vh, 620px)' : undefined,
      }
      : fullDock
        ? {
      gridColumn: leftPanelPresent ? 3 : 2,
      gridRow: '1 / -1',
      width: '100%',
        }
        : {
          right: 12,
          top: 12,
          width: compactWidth,
          maxWidth: 420,
          maxHeight: 'min(70vh, 620px)',
        };

  return (
    <section
      className={rootClass}
      style={rootStyle}
      data-testid="video-editor-right-panel-dock"
      data-layout={layout}
      data-open={panelSurfaceVisible ? 'true' : 'false'}
      data-responsive={responsive ? 'true' : 'false'}
      hidden={!enabled}
      aria-hidden={!enabled}
      role="region"
      aria-label="Video editor right panel"
      {...shellRegionAttrs('rightPanel')}
    >
      <div className="flex shrink-0 flex-wrap items-center gap-1.5 border-b border-border bg-background/90 p-2">
        <label className="sr-only" htmlFor={selectId}>Right panel</label>
        <select
          id={selectId}
          aria-label="Right panel"
          className="h-9 min-w-0 flex-1 rounded-md border border-input bg-background px-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          value={hasSelectedPanel ? selectedPanelId ?? '' : ''}
          onChange={(event) => selectPanel(event.currentTarget.value || null)}
        >
          <option value="">Closed</option>
          <option value={HOST_PROPERTIES_PANEL_KEY}>Properties</option>
          {panels.map((panel) => {
            const key = getPanelKey(panel);
            return <option key={key} value={key}>{panel.label || panel.id}</option>;
          })}
        </select>

        <button
          type="button"
          className="min-h-9 rounded-md px-2 text-xs font-medium hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-pressed={layout === 'compact'}
          onClick={() => selectLayout('compact')}
        >
          Compact
        </button>
        <button
          type="button"
          className="min-h-9 rounded-md px-2 text-xs font-medium hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-pressed={layout === 'dock'}
          onClick={() => selectLayout('dock')}
        >
          Full-height dock
        </button>
        {responsive && (
          <button
            type="button"
            className="min-h-9 rounded-md px-2 text-xs font-medium hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            aria-expanded={panelSurfaceVisible}
            disabled={!hasSelectedPanel}
            onClick={() => setResponsivePanelExpanded(!responsivePanelExpanded)}
          >
            {panelSurfaceVisible ? 'Close panel' : 'Open panel'}
          </button>
        )}
        <button
          type="button"
          className="min-h-9 rounded-md px-2 text-xs font-medium hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-pressed={preferences.showDataLanes}
          onClick={() => ops.setShowDataLanes(!preferences.showDataLanes)}
        >
          {preferences.showDataLanes ? 'Hide timeline lanes' : 'Show timeline lanes'}
        </button>
      </div>

      <div className="min-h-0 flex-1 overflow-auto" hidden={!panelSurfaceVisible}>
        {enabled && (
          <>
            <div className="h-full min-h-0 overflow-auto p-3" hidden={selectedPanelId !== HOST_PROPERTIES_PANEL_KEY}>
              <PropertiesPanel />
            </div>
            <div className="h-full min-h-0 overflow-auto p-3" hidden={!selectedExtensionPanelId}>
              <VideoEditorAssetPanelSurface
                includeBuiltIn={false}
                activePanelKey={panelSurfaceVisible ? selectedExtensionPanelId : null}
              />
            </div>
          </>
        )}
      </div>
    </section>
  );
}
