import { useId, useState, type ReactNode } from 'react';
import { ChevronDown, Settings2 } from 'lucide-react';
import { PropertiesPanel } from './PropertiesPanel';
import { VideoEditorAssetPanelSurface } from './VideoEditorAssetPanelSurface';
import { useTimelineEditorData, useTimelineEditorOps } from '@/tools/video-editor/hooks/timelineStore';
import { getPanelKey } from '@/tools/video-editor/runtime/ExtensionPanelHost';
import { useVideoEditorAssetPanels } from '@/tools/video-editor/runtime/useVideoEditorRenderContext';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext';
import { defaultPreferences } from '@/tools/video-editor/hooks/useEditorPreferences';
import { shellRegionAttrs } from '@/tools/video-editor/lib/timeline-dom';
import { VIDEO_EDITOR_THEME_VARS } from '@/tools/video-editor/lib/themeTokens.ts';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuRadioGroup, DropdownMenuRadioItem } from '@/shared/components/ui/dropdown-menu';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog';
import { ExtensionManager } from '@/tools/video-editor/components/ExtensionManager';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import { COARSE_TOUCH_TARGET } from '@/shared/components/ui/contracts/touchTarget.ts';

import { HOST_EXTENSIONS_PANEL_KEY, HOST_PROPERTIES_PANEL_KEY, VideoEditorPanelDisplayControl } from './VideoEditorPanelDisplayControl';
export { HOST_EXTENSIONS_PANEL_KEY, HOST_PROPERTIES_PANEL_KEY } from './VideoEditorPanelDisplayControl';
export type VideoEditorRightPanelTab = 'video' | 'inspector' | 'extensions';
export interface VideoEditorRightPanelDockProps {
  readonly leftPanelPresent: boolean;
  readonly responsive?: boolean;
  readonly rightInset?: number;
  readonly enabled?: boolean;
  /** Place Compact in the editor's reserved upper-right grid cell on desktop. */
  readonly compactDock?: boolean;
  /** Actual desktop grid geometry; never a guessed preview height. */
  readonly measuredHeight?: number;
  /** Use the editor shell's shared Extension Manager dialog. */
  readonly onOpenExtensionManager?: () => void;
  readonly extensionManagerOpen?: boolean;
  /** Embed the shared tab surface in the touch picture area. */
  readonly touch?: boolean;
  /** The condensed shell's transient Video surface; host panel preferences stay intact. */
  readonly video?: {
    content: ReactNode;
    activeTab: VideoEditorRightPanelTab;
    onTabChange: (tab: VideoEditorRightPanelTab) => void;
  };
}
const controlLook = 'flex min-w-0 items-center gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs text-muted-foreground hover:bg-accent hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring';
const control = `${controlLook} h-8 min-h-10 sm:min-h-8`;
// Touch: the header's 36px controls with a 44px touch ring.
const touchControl = cn(controlLook, COARSE_TOUCH_TARGET, 'h-9 text-sm');
// The film-shaped box under the touch tab row (`--film-aspect` comes from the touch shell);
// in short landscape it fills the column instead.
const TOUCH_CONTENT = 'relative flex w-full flex-col overflow-hidden aspect-[var(--film-aspect)] max-h-[42dvh] min-h-[140px] [@media(orientation:landscape)_and_(max-height:500px)]:aspect-auto [@media(orientation:landscape)_and_(max-height:500px)]:max-h-none [@media(orientation:landscape)_and_(max-height:500px)]:min-h-0 [@media(orientation:landscape)_and_(max-height:500px)]:flex-1';

/** Visibility changes never replace the retained panel subtree or its React key. */
export function VideoEditorRightPanelDock({
  leftPanelPresent,
  responsive = false,
  rightInset = 12,
  enabled = true,
  compactDock = false,
  measuredHeight,
  onOpenExtensionManager,
  extensionManagerOpen,
  touch = false,
  video,
}: VideoEditorRightPanelDockProps) {
  const panels = useVideoEditorAssetPanels();
  const runtime = useOptionalVideoEditorRuntime();
  const data = useTimelineEditorData();
  const ops = useTimelineEditorOps();
  const preferences = data.preferences ?? defaultPreferences;
  const inspectorTargetKind = data.inspectorTarget?.kind;
  const hasInspectableSelection = (data.selectedClipIds?.size ?? 0) > 0
    // On touch the selected track is ambient (where new media lands) and tapping its
    // name opens Inspector itself, so only a picked item earns the hint.
    || (!touch && Boolean(data.selectedTrackId))
    || inspectorTargetKind === 'dataItem'
    || inspectorTargetKind === 'selection'
    || inspectorTargetKind === 'dataLane'
    || inspectorTargetKind === 'shader'
    || inspectorTargetKind === 'shotOccurrence';
  // Extension panels mount once the timeline has arrived, so they never show an empty
  // state ("add media first") for data that is still loading. Latched: later reloads
  // keep the retained subtree.
  const [contentReady, setContentReady] = useState(Boolean(data.data));
  if (!contentReady && data.data) setContentReady(true);
  const [settings, setSettings] = useState<Record<string, boolean>>({});
  const [localManagerOpen, setLocalManagerOpen] = useState(false);
  const [manageTooltipOpen, setManageTooltipOpen] = useState(false);
  const manageTooltipId = useId();
  const selected = preferences.selectedRightPanelId;
  const tab = video?.activeTab ?? (selected ? selected === HOST_PROPERTIES_PANEL_KEY ? 'inspector' : 'extensions' : preferences.rightPanelTab ?? 'inspector');
  const remembered = panels.find((panel) => getPanelKey(panel) === preferences.lastExtensionPanelId) ?? panels[0];
  const tool = panels.find((panel) => getPanelKey(panel) === selected) ?? remembered;
  const toolKey = tool ? getPanelKey(tool) : null;
  const currentKey = tab === 'inspector' ? HOST_PROPERTIES_PANEL_KEY : toolKey ?? HOST_PROPERTIES_PANEL_KEY;
  // Inspector and Extensions share one display mode. The host slot is the
  // canonical value; per-extension slots are read only for legacy migration.
  const layout = preferences.rightPanelLayoutSlotsByPanelId[HOST_PROPERTIES_PANEL_KEY]
    ?? preferences.rightPanelLayoutSlotsByPanelId[currentKey]
    ?? 'dock';
  // Only "Closed" (null) closes the dock: disabling the selected extension falls back to `tool`.
  const open = Boolean(video) || selected !== null;
  const dock = Boolean(video) || layout === 'dock';
  const compactInGrid = !video && open && layout === 'compact' && compactDock && !responsive;
  const inGrid = !responsive;
  const retainClosedSurface = enabled;
  const hidden = !enabled || (!open && !retainClosedSurface);
  // The outer grid track clips while it changes width. Keep the retained
  // reading surface at its final width so reflow cannot move its scroll anchor.
  const contentWidth = inGrid && !video
    ? 'max(0px, calc(min(420px, 32vw, calc(100vw - 24px)) - 2px))'
    : undefined;
  const tabs: readonly VideoEditorRightPanelTab[] = video ? ['video', 'inspector', 'extensions'] : ['inspector', 'extensions'];
  const showTab = (next: VideoEditorRightPanelTab, displayMode: 'compact' | 'dock' = layout) => {
    video?.onTabChange(next);
    if (next === 'video') return;
    // Capture the visible mode before changing the selected panel. This
    // promotes legacy per-panel state to the shared placement slot.
    ops.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, displayMode);
    // Extensions never closes the dock: with no panel to select it parks on the host key.
    ops.setSelectedRightPanelId(next === 'inspector' ? HOST_PROPERTIES_PANEL_KEY : toolKey ?? HOST_EXTENSIONS_PANEL_KEY);
  };
  const inventory = runtime?.extensionRuntime?.packageStateInventory ?? [];
  const enabledExtensionLabelsById = new Map(inventory
    .filter((entry) => entry.packageState === 'loaded')
    .map((entry) => [entry.extensionId, { key: entry.extensionId, label: entry.packageMetadata?.label ?? entry.extensionId }]));
  // Direct/dev-local extensions do not enter packageStateInventory. The full
  // Extension Manager derives their active state from this same runtime list.
  for (const extension of runtime?.extensionRuntime?.extensions ?? []) {
    const id = extension.manifest.id;
    if (typeof id !== 'string' || !id) continue;
    const inventoryEntry = inventory.find((entry) => entry.extensionId === id);
    enabledExtensionLabelsById.set(id, {
      key: id,
      label: inventoryEntry?.packageMetadata?.label ?? extension.manifest.label ?? id,
    });
  }
  const enabledExtensionLabels = [...enabledExtensionLabelsById.values()];
  const settingsByPanelKey = Object.fromEntries(panels.map((panel) => {
    const key = getPanelKey(panel);
    return [key, { open: settings[key] ?? false, onOpenChange: (value: boolean) => setSettings((current) => ({ ...current, [key]: value })) }];
  }));
  const managerOpen = onOpenExtensionManager ? extensionManagerOpen === true : localManagerOpen;
  const openManager = () => {
    setManageTooltipOpen(false);
    if (onOpenExtensionManager) onOpenExtensionManager();
    else setLocalManagerOpen(true);
  };
  const extensionsHeader = tab === 'extensions' && <div className={`flex shrink-0 items-center border-b border-border/60 p-2 ${touch ? 'gap-2' : 'gap-1.5'}`} style={{ minWidth: contentWidth, visibility: open ? undefined : 'hidden' }}>
    <DropdownMenu><DropdownMenuTrigger className={`${touch ? touchControl : control} flex-1 justify-between`} aria-label="Displayed extension"><span className="min-w-0 truncate">Display: {tool?.label ?? (panels.length ? 'Choose tool' : 'None')}</span><ChevronDown className="h-3 w-3 shrink-0" /></DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="max-w-[calc(100vw-24px)] min-w-48"><DropdownMenuRadioGroup value={toolKey ?? ''} onValueChange={(key) => { ops.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, layout); ops.setSelectedRightPanelId(key); }}>{panels.map((panel) => <DropdownMenuRadioItem key={getPanelKey(panel)} value={getPanelKey(panel)}>{panel.label || panel.id}</DropdownMenuRadioItem>)}</DropdownMenuRadioGroup></DropdownMenuContent>
    </DropdownMenu>
    <div className={touch ? 'relative shrink-0' : 'relative flex-1'} onPointerEnter={() => setManageTooltipOpen(true)} onPointerLeave={() => setManageTooltipOpen(false)} onFocusCapture={() => setManageTooltipOpen(true)} onBlurCapture={() => setManageTooltipOpen(false)} onPointerDownCapture={() => setManageTooltipOpen(false)} onClickCapture={() => setManageTooltipOpen(false)} onKeyDownCapture={(event) => { if (event.key === 'Escape') setManageTooltipOpen(false); }}>
      <button type="button" className={touch ? cn(touchControl, 'w-9 justify-center px-0') : `${control} w-full justify-center`} aria-label="Manage extensions" aria-haspopup="dialog" aria-expanded={managerOpen} aria-describedby={manageTooltipOpen ? manageTooltipId : undefined} onClick={openManager}>
        {/* Touch: an icon, so the active panel's name keeps the row. */}
        <Settings2 className="h-4 w-4 shrink-0" />{!touch && <span>Manage</span>}
      </button>
      {manageTooltipOpen && <div id={manageTooltipId} role="tooltip" className="absolute right-0 top-full z-50 mt-2 max-h-64 max-w-64 overflow-auto rounded-md border border-border bg-popover px-3 py-2 text-xs text-popover-foreground shadow-md">
        <span className="font-medium">Enabled extensions</span>
        {enabledExtensionLabels.length
          ? <ul className="mt-1 list-inside list-disc">{enabledExtensionLabels.map(({ key, label }) => <li key={key}>{label}</li>)}</ul>
          : <p className="mt-1">No extensions are currently enabled.</p>}
      </div>}
    </div>
  </div>;
  const body = <div className="min-h-0 flex-1 overflow-hidden" style={{ minWidth: contentWidth, visibility: open ? undefined : 'hidden' }}>
    {enabled && <>
      {video && <div className="flex h-full min-h-0 flex-col" hidden={tab !== 'video'} style={{ display: tab === 'video' ? undefined : 'none' }}>{video.content}</div>}
      <div className={`h-full min-h-0 overflow-auto ${touch ? 'px-3' : 'p-3'}`} hidden={tab !== 'inspector'}><PropertiesPanel visible={open && tab === 'inspector'} /></div>
      <div className="h-full min-h-0 overflow-hidden" hidden={tab !== 'extensions'}>{panels.length === 0 && tab === 'extensions' && <p data-testid="extensions-empty-state" className="p-4 text-center text-sm text-muted-foreground">No extensions are active for this project yet.</p>}{contentReady && <VideoEditorAssetPanelSurface includeBuiltIn={false} activePanelKey={open && tab === 'extensions' ? toolKey : null} settingsByPanelKey={settingsByPanelKey} />}</div>
    </>}
  </div>;
  // Touch: the Extensions picker sits inside the film-shaped box, so switching tabs never
  // changes the card's height.
  return <section hidden={hidden} aria-hidden={!enabled || !open} role="region" aria-label="Video editor right panel"
    data-testid="video-editor-right-panel-dock" data-layout={video ? 'dock' : layout} data-open={String(open)} data-responsive={String(responsive)}
    {...shellRegionAttrs('rightPanel')}
    data-placement={touch ? 'picture' : compactInGrid ? 'upper-right-grid' : dock ? 'full-height-grid' : 'overlay'}
    className={`video-editor-right-panel-motion ${touch ? 'relative h-full w-full' : inGrid ? 'row-span-full' : 'absolute z-40'} ${hidden ? 'hidden' : 'flex'} min-h-0 min-w-0 flex-col overflow-hidden rounded-xl border border-border bg-card/95 ${inGrid || touch ? '' : 'shadow-xl'}`}
    style={touch ? undefined : inGrid
      ? { gridColumn: leftPanelPresent ? 3 : 2, gridRow: '1 / -1', alignSelf: 'start', width: 'calc(100% - 12px)', marginInlineStart: 12, height: measuredHeight && measuredHeight > 0 ? measuredHeight : '100%', maxHeight: '100%', pointerEvents: open ? undefined : 'none', borderWidth: open ? undefined : 0 }
      : dock
        ? { top: 12, right: rightInset, width: open ? `calc(100% - ${12 + rightInset}px)` : 0, height: 'calc(100% - 24px)', pointerEvents: open ? undefined : 'none', borderWidth: open ? undefined : 0 }
        : { top: 12, right: rightInset, width: open ? `calc(100vw - ${12 + rightInset}px)` : 0, maxWidth: 420, maxHeight: 'min(70dvh, 620px)', height: 'min(70dvh, 620px)', pointerEvents: open ? undefined : 'none', borderWidth: open ? undefined : 0 }}>
    <div className={`flex shrink-0 items-center gap-1 border-b border-border/70 ${touch ? 'h-11 px-1' : 'px-2 py-1.5'}`} style={{ minWidth: contentWidth, visibility: open ? undefined : 'hidden' }}>
      <div role="tablist" aria-label="Right panel surface" className="flex min-w-0 flex-1 gap-1" style={VIDEO_EDITOR_THEME_VARS}>
        {tabs.map((value) => {
          const showInspectorHint = value === 'inspector' && tab !== 'inspector' && hasInspectableSelection;
          return <button key={value} type="button" role="tab" tabIndex={tab === value ? 0 : -1} aria-selected={tab === value} aria-label={showInspectorHint ? 'Inspector — selection available' : value === 'video' ? 'Video' : value === 'inspector' ? 'Inspector' : 'Extensions'} onKeyDown={(event) => {
          if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
            event.preventDefault();
            const next = event.key === 'Home' ? tabs[0] : event.key === 'End' ? tabs[tabs.length - 1]
              : tabs[(tabs.indexOf(value) + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length];
            showTab(next);
            event.currentTarget.parentElement?.querySelector<HTMLButtonElement>(`[data-surface-tab="${next}"]`)?.focus();
          }
        }} data-surface-tab={value} onClick={() => showTab(value)} className={`${touch ? `${COARSE_TOUCH_TARGET} h-9 min-w-0 flex-1 px-1 text-sm` : 'min-h-10 px-2.5 text-xs sm:min-h-8'} rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${tab === value ? 'bg-muted text-foreground' : 'text-muted-foreground hover:text-foreground'}`}>
            {value === 'video' ? 'Video' : value === 'inspector' ? 'Inspector' : 'Extensions'}
            {showInspectorHint && <span data-testid="inspector-selection-hint" aria-hidden="true" className="ml-1.5 inline-block h-1.5 w-1.5 rounded-full bg-[var(--video-editor-accent-border-strong)] align-middle" />}
          </button>;
        })}
      </div>
      {!video && <VideoEditorPanelDisplayControl visible={open} />}
    </div>
    {touch ? <div className={TOUCH_CONTENT}>{extensionsHeader}{body}</div> : <>{extensionsHeader}{body}</>}
    {!onOpenExtensionManager && <Dialog open={localManagerOpen} onOpenChange={setLocalManagerOpen}><DialogContent className="max-h-[85dvh] overflow-auto"><DialogHeader><DialogTitle>Extensions</DialogTitle></DialogHeader><ExtensionManager /></DialogContent></Dialog>}
  </section>;
}
