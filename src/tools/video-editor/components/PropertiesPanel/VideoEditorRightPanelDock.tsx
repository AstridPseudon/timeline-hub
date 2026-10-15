import { useId, useState } from 'react';
import { ChevronDown, PanelsTopLeft, Settings2 } from 'lucide-react';
import { PropertiesPanel } from './PropertiesPanel';
import { VideoEditorAssetPanelSurface } from './VideoEditorAssetPanelSurface';
import { useTimelineEditorData, useTimelineEditorOps } from '@/tools/video-editor/hooks/timelineStore';
import { getPanelKey } from '@/tools/video-editor/runtime/ExtensionPanelHost';
import { useVideoEditorAssetPanels } from '@/tools/video-editor/runtime/useVideoEditorRenderContext';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext';
import { defaultPreferences } from '@/tools/video-editor/hooks/useEditorPreferences';
import { shellRegionAttrs } from '@/tools/video-editor/lib/timeline-dom';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuLabel, DropdownMenuRadioGroup, DropdownMenuRadioItem } from '@/shared/components/ui/dropdown-menu';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog';
import { ExtensionManager } from '@/tools/video-editor/components/ExtensionManager';

export const HOST_PROPERTIES_PANEL_KEY = 'host:properties';
export interface VideoEditorRightPanelDockProps {
  readonly leftPanelPresent: boolean;
  readonly responsive?: boolean;
  readonly rightInset?: number;
  readonly enabled?: boolean;
  /** Place Compact in the editor's reserved upper-right grid cell on desktop. */
  readonly compactDock?: boolean;
  /** Use the editor shell's shared Extension Manager dialog. */
  readonly onOpenExtensionManager?: () => void;
  readonly extensionManagerOpen?: boolean;
}
const control = 'flex h-8 min-h-10 sm:min-h-8 min-w-0 items-center gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs text-muted-foreground hover:bg-accent hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring';

/** Visibility changes never replace the retained panel subtree or its React key. */
export function VideoEditorRightPanelDock({
  leftPanelPresent,
  responsive = false,
  rightInset = 12,
  enabled = true,
  compactDock = false,
  onOpenExtensionManager,
  extensionManagerOpen,
}: VideoEditorRightPanelDockProps) {
  const panels = useVideoEditorAssetPanels();
  const runtime = useOptionalVideoEditorRuntime();
  const data = useTimelineEditorData();
  const ops = useTimelineEditorOps();
  const preferences = data.preferences ?? defaultPreferences;
  const inspectorTargetKind = data.inspectorTarget?.kind;
  const hasInspectableSelection = (data.selectedClipIds?.size ?? 0) > 0
    || Boolean(data.selectedTrackId)
    || inspectorTargetKind === 'dataItem'
    || inspectorTargetKind === 'dataLane'
    || inspectorTargetKind === 'shader'
    || inspectorTargetKind === 'shotOccurrence';
  const [settings, setSettings] = useState<Record<string, boolean>>({});
  const [localManagerOpen, setLocalManagerOpen] = useState(false);
  const [manageTooltipOpen, setManageTooltipOpen] = useState(false);
  const manageTooltipId = useId();
  const selected = preferences.selectedRightPanelId;
  const tab = selected ? selected === HOST_PROPERTIES_PANEL_KEY ? 'inspector' : 'extensions' : preferences.rightPanelTab ?? 'inspector';
  const remembered = panels.find((panel) => getPanelKey(panel) === preferences.lastExtensionPanelId) ?? panels[0];
  const tool = panels.find((panel) => getPanelKey(panel) === selected) ?? remembered;
  const toolKey = tool ? getPanelKey(tool) : null;
  const currentKey = tab === 'inspector' ? HOST_PROPERTIES_PANEL_KEY : toolKey ?? HOST_PROPERTIES_PANEL_KEY;
  // Inspector and Extensions share one display mode. The host slot is the
  // canonical value; per-extension slots are read only for legacy migration.
  const layout = preferences.rightPanelLayoutSlotsByPanelId[HOST_PROPERTIES_PANEL_KEY]
    ?? preferences.rightPanelLayoutSlotsByPanelId[currentKey]
    ?? 'dock';
  const open = selected !== null && (tab === 'inspector' || panels.some((panel) => getPanelKey(panel) === selected));
  const dock = open && layout === 'dock';
  const compactInGrid = open && layout === 'compact' && compactDock && !responsive;
  const inGrid = compactInGrid || (dock && !responsive);
  const showTab = (next: 'inspector' | 'extensions', displayMode: 'compact' | 'dock' = layout) => {
    // Capture the visible mode before changing the selected panel. This
    // promotes legacy per-panel state to the shared placement slot.
    ops.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, displayMode);
    ops.setSelectedRightPanelId(next === 'inspector' ? HOST_PROPERTIES_PANEL_KEY : toolKey);
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
  const [displayMenuOpen, setDisplayMenuOpen] = useState(false);
  const managerOpen = onOpenExtensionManager ? extensionManagerOpen === true : localManagerOpen;
  const openManager = () => {
    setManageTooltipOpen(false);
    if (onOpenExtensionManager) onOpenExtensionManager();
    else setLocalManagerOpen(true);
  };
  return <section hidden={!enabled} aria-hidden={!enabled} role="region" aria-label="Video editor right panel"
    data-testid="video-editor-right-panel-dock" data-layout={layout} data-open={String(open)} data-responsive={String(responsive)}
    {...shellRegionAttrs('rightPanel')}
    data-placement={compactInGrid ? 'upper-right-grid' : dock ? 'full-height-grid' : 'overlay'}
    className={`${compactInGrid ? '' : dock && !responsive ? 'row-span-full' : 'absolute z-40'} ${enabled ? 'flex' : 'hidden'} min-h-0 min-w-0 flex-col overflow-hidden rounded-xl border border-border bg-card/95 ${inGrid ? '' : 'shadow-xl'}`}
    style={compactInGrid
      ? { gridColumn: leftPanelPresent ? 3 : 2, gridRow: '1', width: '100%', height: '100%', maxHeight: '100%' }
      : dock
        ? responsive ? { top: 12, right: rightInset, bottom: 12, left: 12 } : { gridColumn: leftPanelPresent ? 3 : 2, gridRow: '1 / -1', width: '100%' }
        : { top: 12, right: rightInset, width: `calc(100vw - ${12 + rightInset}px)`, maxWidth: 420, maxHeight: 'min(70dvh, 620px)', height: open ? 'min(70dvh, 620px)' : undefined }}>
    <div className="flex shrink-0 items-center gap-1 border-b border-border/70 px-2 py-1.5">
      <div role="tablist" aria-label="Right panel surface" className="flex min-w-0 flex-1 gap-1">
        {(['inspector', 'extensions'] as const).map((value) => {
          const showInspectorHint = value === 'inspector' && tab === 'extensions' && hasInspectableSelection;
          return <button key={value} type="button" role="tab" tabIndex={tab === value ? 0 : -1} aria-selected={tab === value} aria-label={showInspectorHint ? 'Inspector — selection available' : value === 'inspector' ? 'Inspector' : 'Extensions'} onKeyDown={(event) => {
          if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) { event.preventDefault(); const next = event.key === 'Home' ? 'inspector' : event.key === 'End' ? 'extensions' : value === 'inspector' ? 'extensions' : 'inspector'; showTab(next); event.currentTarget.parentElement?.querySelector<HTMLButtonElement>(`[data-surface-tab="${next}"]`)?.focus(); }
        }} data-surface-tab={value} onClick={() => showTab(value)} className={`min-h-10 sm:min-h-8 rounded-md px-2.5 text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${tab === value ? 'bg-muted text-foreground' : 'text-muted-foreground hover:text-foreground'}`}>
            {value === 'inspector' ? 'Inspector' : 'Extensions'}
            {showInspectorHint && <span data-testid="inspector-selection-hint" aria-hidden="true" className="ml-1.5 inline-block h-1.5 w-1.5 rounded-full bg-primary align-middle" />}
          </button>;
        })}
      </div>
      <DropdownMenu open={displayMenuOpen} onOpenChange={setDisplayMenuOpen}>
        <DropdownMenuTrigger className={`${control} w-10 shrink-0 justify-center px-0 sm:w-8`} aria-label="Panel display" title="Panel display"><PanelsTopLeft className="h-4 w-4" /></DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuLabel>Panel display</DropdownMenuLabel>
          <DropdownMenuRadioGroup value={open ? layout : 'closed'} onValueChange={(value) => {
            setDisplayMenuOpen(false);
            if (value === 'closed') ops.setSelectedRightPanelId(null);
            else { ops.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, value as 'compact' | 'dock'); if (!open) showTab(tab, value as 'compact' | 'dock'); }
          }}>
            <DropdownMenuRadioItem value="compact">Compact</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="dock">Full-height</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="closed">Closed</DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
    {open && tab === 'extensions' && <div className="flex shrink-0 items-center gap-1.5 border-b border-border/60 p-2">
      <>
        <DropdownMenu><DropdownMenuTrigger className={`${control} flex-1 justify-between`} aria-label="Active extension"><span className="min-w-0 truncate">Active · {tool?.label ?? 'Choose tool'}</span><ChevronDown className="h-3 w-3 shrink-0" /></DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="max-w-[calc(100vw-24px)] min-w-48"><DropdownMenuRadioGroup value={toolKey ?? ''} onValueChange={(key) => { ops.setRightPanelLayoutSlot(HOST_PROPERTIES_PANEL_KEY, layout); ops.setSelectedRightPanelId(key); }}>{panels.map((panel) => <DropdownMenuRadioItem key={getPanelKey(panel)} value={getPanelKey(panel)}>{panel.label || panel.id}</DropdownMenuRadioItem>)}</DropdownMenuRadioGroup></DropdownMenuContent>
        </DropdownMenu>
        <div className="relative flex-1" onPointerEnter={() => setManageTooltipOpen(true)} onPointerLeave={() => setManageTooltipOpen(false)} onFocusCapture={() => setManageTooltipOpen(true)} onBlurCapture={() => setManageTooltipOpen(false)} onPointerDownCapture={() => setManageTooltipOpen(false)} onClickCapture={() => setManageTooltipOpen(false)} onKeyDownCapture={(event) => { if (event.key === 'Escape') setManageTooltipOpen(false); }}>
          <button type="button" className={`${control} w-full justify-center`} aria-label="Manage extensions" aria-haspopup="dialog" aria-expanded={managerOpen} aria-describedby={manageTooltipOpen ? manageTooltipId : undefined} onClick={openManager}>
              <Settings2 className="h-4 w-4 shrink-0" /><span>Manage</span>
          </button>
          {manageTooltipOpen && <div id={manageTooltipId} role="tooltip" className="absolute right-0 top-full z-50 mt-2 max-h-64 max-w-64 overflow-auto rounded-md border border-border bg-popover px-3 py-2 text-xs text-popover-foreground shadow-md">
              <span className="font-medium">Enabled extensions</span>
              {enabledExtensionLabels.length
                ? <ul className="mt-1 list-inside list-disc">{enabledExtensionLabels.map(({ key, label }) => <li key={key}>{label}</li>)}</ul>
                : <p className="mt-1">No extensions are currently enabled.</p>}
            </div>}
        </div>
      </>
    </div>}
    <div className="min-h-0 flex-1 overflow-hidden" hidden={!open}>
      {enabled && <>
        <div className="h-full min-h-0 overflow-auto p-3" hidden={tab !== 'inspector'}><PropertiesPanel /></div>
        <div className="h-full min-h-0 overflow-hidden" hidden={tab !== 'extensions'}><VideoEditorAssetPanelSurface includeBuiltIn={false} activePanelKey={open && tab === 'extensions' ? toolKey : null} settingsByPanelKey={settingsByPanelKey} /></div>
      </>}
    </div>
    {!onOpenExtensionManager && <Dialog open={localManagerOpen} onOpenChange={setLocalManagerOpen}><DialogContent className="max-h-[85dvh] overflow-auto"><DialogHeader><DialogTitle>Extensions</DialogTitle></DialogHeader><ExtensionManager /></DialogContent></Dialog>}
  </section>;

}
