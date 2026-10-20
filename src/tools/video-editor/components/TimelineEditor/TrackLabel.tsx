import { useCallback, useContext, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import type { DraggableAttributes } from '@dnd-kit/core';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { SyntheticListenerMap } from '@dnd-kit/core/dist/hooks/utilities';
import { Check, GripVertical, Settings, Trash2, Video, Volume2, VolumeX } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/shared/components/ui/dialog.tsx';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select.tsx';
import { Slider } from '@/shared/components/ui/slider.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import { usePortalMousedownGuard } from '@/shared/hooks/usePortalMousedownGuard.ts';
import {
  ExtensionContextMenuItems,
  hasEligibleExtensionContextMenuItems,
} from '@/tools/video-editor/components/TimelineEditor/ExtensionContextMenuItems.tsx';
import { MOBILE_SHEET_CLASS } from '@/tools/video-editor/lib/mobile-sheet.ts';
import { VideoEditorRuntimeContext } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { trackRole } from '@/tools/video-editor/data/timelineOutputProjection.ts';
import { isTrackMuted } from '@/tools/video-editor/lib/editor-utils.ts';
import { trackLabelAttrs } from '@/tools/video-editor/lib/timeline-dom.ts';
import type { TimelineDeviceClass } from '@/tools/video-editor/lib/mobile-interaction-model.ts';
import type { TrackBlendMode, TrackDefinition, TrackFit } from '@/tools/video-editor/types/index.ts';
import type { TargetContextPayload } from '@astrid/editor-sdk';

interface TrackLabelProps {
  id: string;
  track: TrackDefinition;
  isSelected: boolean;
  hasClips: boolean;
  deviceClass?: TimelineDeviceClass;
  onSelect: (trackId: string) => void;
  onChange: (trackId: string, patch: Partial<TrackDefinition>) => void;
  onRemove: (trackId: string) => void;
}

interface TrackLabelContentProps {
  track: TrackDefinition;
  /** Read-only context shown in the label without changing the persisted name. */
  displayLabel?: string;
  isSelected: boolean;
  hasClips: boolean;
  deviceClass?: TimelineDeviceClass;
  onSelect: (trackId: string) => void;
  onChange: (trackId: string, patch: Partial<TrackDefinition>) => void;
  onRemove: (trackId: string) => void;
  readOnly?: boolean;
  rowDragging?: boolean;
  /** Adds a track; offered in the touch track sheet (desktop has + Video / + Audio in the footer). */
  onAddTrack?: (kind: 'visual' | 'audio') => void;
  dragListeners?: SyntheticListenerMap;
  dragAttributes?: DraggableAttributes;
}

export const FIT_OPTIONS: { value: TrackFit; label: string }[] = [
  { value: 'cover', label: 'Cover' },
  { value: 'contain', label: 'Contain' },
  { value: 'manual', label: 'Manual' },
];

export const BLEND_OPTIONS: { value: TrackBlendMode; label: string }[] = [
  { value: 'normal', label: 'Normal' },
  { value: 'multiply', label: 'Multiply' },
  { value: 'screen', label: 'Screen' },
  { value: 'overlay', label: 'Overlay' },
  { value: 'darken', label: 'Darken' },
  { value: 'lighten', label: 'Lighten' },
  { value: 'soft-light', label: 'Soft Light' },
  { value: 'hard-light', label: 'Hard Light' },
];

export function FieldLabel({ children }: { children: React.ReactNode }) {
  return <div className="text-[11px] font-medium text-muted-foreground">{children}</div>;
}

interface TrackContextMenuState {
  x: number;
  y: number;
  target: TargetContextPayload;
}

function validateTrackContextMenuTarget(
  target: TargetContextPayload,
  currentTrackId: string,
): string | null {
  if (target.target !== 'track') return null;
  if (target.trackId !== currentTrackId) {
    return `Track "${target.trackId}" is no longer available.`;
  }
  return null;
}

function TrackExtensionContextMenu({
  menu,
  menuRef,
  trackId,
  closeMenu,
}: {
  menu: TrackContextMenuState;
  menuRef: React.RefObject<HTMLDivElement>;
  trackId: string;
  closeMenu: () => void;
}) {
  const [adjusted, setAdjusted] = useState<{ x: number; y: number } | null>(null);
  const runtime = useContext(VideoEditorRuntimeContext);
  const commandRegistry = runtime?.commandRegistry;
  const extensions = runtime?.extensionRuntime?.extensions ?? [];
  const items = commandRegistry
    ? commandRegistry.getSnapshot().contextMenuItems.filter((item) => item.target === menu.target.target)
    : [];

  useLayoutEffect(() => {
    const node = menuRef.current;
    if (!node) {
      setAdjusted(null);
      return;
    }

    const recompute = () => {
      const rect = node.getBoundingClientRect();
      const pad = 8;
      setAdjusted({
        x: Math.max(pad, Math.min(menu.x, window.innerWidth - rect.width - pad)),
        y: Math.max(pad, Math.min(menu.y, window.innerHeight - rect.height - pad)),
      });
    };

    recompute();

    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(recompute);
    observer.observe(node);
    return () => observer.disconnect();
  }, [menu.x, menu.y, menuRef]);

  usePortalMousedownGuard(menuRef);

  const pos = adjusted ?? menu;

  return createPortal(
    <div
      ref={menuRef}
      className="fixed z-50 min-w-[10rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95"
      style={{ left: pos.x, top: pos.y, visibility: adjusted ? 'visible' : 'hidden' }}
    >
      <ExtensionContextMenuItems
        items={items}
        target={menu.target}
        extensions={extensions}
        commandRegistry={commandRegistry}
        closeMenu={closeMenu}
        validateTarget={(target) => validateTrackContextMenuTarget(target, trackId)}
      />
    </div>,
    document.body,
  );
}

function TrackSettingsFields({
  track,
  onChange,
}: {
  track: TrackDefinition;
  onChange: (trackId: string, patch: Partial<TrackDefinition>) => void;
}) {
  return (
    <div className="space-y-4 pt-2">
      <div className="space-y-1.5">
        <FieldLabel>Use</FieldLabel>
        <Select
          value={trackRole(track)}
          onValueChange={(value) => {
            if (value === 'output' || value === 'source') onChange(track.id, { role: value });
          }}
        >
          <SelectTrigger className="h-9 text-xs" aria-label="Track role"><SelectValue>{trackRole(track) === 'source' ? 'Source' : 'Output'}</SelectValue></SelectTrigger>
          <SelectContent>
            <SelectItem value="output">Output</SelectItem>
            <SelectItem value="source">Source</SelectItem>
          </SelectContent>
        </Select>
        <p className="text-xs text-muted-foreground">
          {trackRole(track) === 'source' ? 'Reference material. Excluded from final output.' : 'Included in final output.'}
          {' '}Applies to all items on this track.
        </p>
      </div>
      {track.kind === 'visual' && (
        <>
          <div className="space-y-1.5">
            <FieldLabel>Fit</FieldLabel>
            <Select
              value={track.fit ?? 'contain'}
              onValueChange={(value) => onChange(track.id, { fit: value as TrackFit })}
            >
              <SelectTrigger className="h-8 text-xs"><SelectValue /></SelectTrigger>
              <SelectContent>
                {FIT_OPTIONS.map((opt) => (
                  <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1.5">
            <FieldLabel>Scale ({((track.scale ?? 1) * 100).toFixed(0)}%)</FieldLabel>
            <Slider
              value={[track.scale ?? 1]}
              min={0.1}
              max={2}
              step={0.05}
              onValueChange={(v) => onChange(track.id, { scale: v })}
            />
          </div>
          <div className="space-y-1.5">
            <FieldLabel>Opacity ({((track.opacity ?? 1) * 100).toFixed(0)}%)</FieldLabel>
            <Slider
              value={[track.opacity ?? 1]}
              min={0}
              max={1}
              step={0.05}
              onValueChange={(v) => onChange(track.id, { opacity: v })}
            />
          </div>
          <div className="space-y-1.5">
            <FieldLabel>Blend Mode</FieldLabel>
            <Select
              value={track.blendMode ?? 'normal'}
              onValueChange={(value) => onChange(track.id, { blendMode: value as TrackBlendMode })}
            >
              <SelectTrigger className="h-8 text-xs"><SelectValue /></SelectTrigger>
              <SelectContent>
                {BLEND_OPTIONS.map((opt) => (
                  <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </>
      )}
      {track.kind === 'audio' && (
        <div className="space-y-2">
          <div className="space-y-1.5">
            <FieldLabel>Default Volume ({((track.volume ?? 1) * 100).toFixed(0)}%)</FieldLabel>
            <Slider
              value={[track.volume ?? 1]}
              min={0}
              max={1}
              step={0.05}
              onValueChange={(v) => onChange(track.id, { volume: v })}
            />
          </div>
          <Button
            type="button"
            variant="secondary"
            size="sm"
            className="gap-1.5"
            onClick={() => onChange(track.id, { muted: !isTrackMuted(track) })}
          >
            {isTrackMuted(track) ? <Volume2 className="h-3.5 w-3.5" /> : <VolumeX className="h-3.5 w-3.5" />}
            {isTrackMuted(track) ? 'Unmute Track' : 'Mute Track'}
          </Button>
        </div>
      )}
    </div>
  );
}

interface TrackSettingsDialogProps {
  track: TrackDefinition;
  triggerClassName: string;
  iconClassName: string;
  onChange: (trackId: string, patch: Partial<TrackDefinition>) => void;
}

function TrackSettingsDialog({
  track,
  triggerClassName,
  iconClassName,
  onChange,
}: TrackSettingsDialogProps) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className={cn(triggerClassName, 'text-muted-foreground')}
          title="Track settings"
          aria-label="Track settings"
          onClick={(event) => event.stopPropagation()}
        >
          <Settings className={iconClassName} />
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-sm" onClick={(e) => e.stopPropagation()}>
        <DialogHeader>
          <DialogTitle>{track.label} — Track settings</DialogTitle>
          <DialogDescription>
            Choose how this track is used, and defaults for new items.
          </DialogDescription>
        </DialogHeader>
        <TrackSettingsFields track={track} onChange={onChange} />
      </DialogContent>
    </Dialog>
  );
}

/**
 * The touch track sheet: tapping a track's name opens the same actions the
 * desktop track row offers (rename, settings, add track, delete with its
 * confirm), in the clip sheet's bottom-sheet look.
 */
function TrackSheet({
  open,
  onOpenChange,
  track,
  hasClips,
  confirmingDelete,
  onChange,
  onRemoveClick,
  onAddTrack,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  track: TrackDefinition;
  hasClips: boolean;
  confirmingDelete: boolean;
  onChange: (trackId: string, patch: Partial<TrackDefinition>) => void;
  onRemoveClick: (event: React.MouseEvent) => void;
  onAddTrack?: (kind: 'visual' | 'audio') => void;
}) {
  const sheetButton = 'h-11 flex-1 justify-center gap-1.5';
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        data-testid="timeline-track-sheet"
        className={MOBILE_SHEET_CLASS}
        onClick={(event) => event.stopPropagation()}
      >
        <DialogHeader className="sr-only">
          <DialogTitle>{track.label} — Track</DialogTitle>
          <DialogDescription>Track name, settings and actions.</DialogDescription>
        </DialogHeader>
        <div aria-hidden="true" className="mx-auto mt-2 h-1 w-10 shrink-0 rounded-full bg-border" />
        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-3 [&_[role=combobox]]:h-11">
          <div className="space-y-1.5">
            <FieldLabel>Name</FieldLabel>
            <input
              className="h-11 w-full rounded-md border border-border bg-background px-3 text-base outline-none focus-visible:ring-2 focus-visible:ring-ring"
              value={track.label}
              aria-label="Track name"
              onChange={(event) => onChange(track.id, { label: event.target.value })}
            />
          </div>
          <TrackSettingsFields track={track} onChange={onChange} />
          {onAddTrack && (
            <div className="flex gap-2">
              <Button type="button" variant="secondary" className={sheetButton} onClick={() => onAddTrack('visual')}>
                Add video track
              </Button>
              <Button type="button" variant="secondary" className={sheetButton} onClick={() => onAddTrack('audio')}>
                Add audio track
              </Button>
            </div>
          )}
          <Button
            type="button"
            variant="outline"
            className={cn('h-11 w-full justify-center gap-1.5', confirmingDelete && 'border-destructive text-destructive')}
            onClick={(event) => {
              onRemoveClick(event);
              if (!hasClips || confirmingDelete) onOpenChange(false);
            }}
          >
            {confirmingDelete ? <Check className="h-4 w-4" /> : <Trash2 className="h-4 w-4" />}
            {confirmingDelete ? 'Tap again to confirm deletion' : 'Delete track'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

export function TrackLabelContent({
  track,
  displayLabel,
  isSelected,
  hasClips,
  deviceClass = 'desktop',
  onSelect,
  onChange,
  onRemove,
  readOnly = false,
  rowDragging = false,
  onAddTrack,
  dragListeners,
  dragAttributes,
}: TrackLabelContentProps) {
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [trackSheetOpen, setTrackSheetOpen] = useState(false);
  const [contextMenu, setContextMenu] = useState<TrackContextMenuState | null>(null);
  const confirmTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const runtime = useContext(VideoEditorRuntimeContext);
  const commandRegistry = runtime?.commandRegistry;
  const extensions = runtime?.extensionRuntime?.extensions ?? [];

  const closeMenu = useCallback(() => setContextMenu(null), []);

  useEffect(() => {
    if (!confirmingDelete) return;
    confirmTimerRef.current = setTimeout(() => setConfirmingDelete(false), 2000);
    return () => { if (confirmTimerRef.current) clearTimeout(confirmTimerRef.current); };
  }, [confirmingDelete]);

  const handleRemoveClick = useCallback((event: React.MouseEvent) => {
    event.stopPropagation();
    if (!hasClips) {
      onRemove(track.id);
      return;
    }
    if (confirmingDelete) {
      setConfirmingDelete(false);
      onRemove(track.id);
    } else {
      setConfirmingDelete(true);
    }
  }, [confirmingDelete, hasClips, onRemove, track.id]);

  useEffect(() => {
    if (!contextMenu) return;
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        closeMenu();
      }
    };
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') closeMenu();
    };
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [contextMenu, closeMenu]);

  const handleContextMenu = useCallback((event: React.MouseEvent) => {
    const target: TargetContextPayload = { target: 'track', trackId: track.id };
    if (!hasEligibleExtensionContextMenuItems(commandRegistry, extensions, target)) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();
    onSelect(track.id);
    setContextMenu({
      x: event.clientX,
      y: event.clientY,
      target,
    });
  }, [commandRegistry, extensions, onSelect, readOnly, track.id]);

  // Desktop reveals the track actions on hover. Touch has no hover: tapping the
  // name opens the track sheet instead (reordering stays a desktop drag).
  const showTrackActions = !readOnly && deviceClass === 'desktop';
  const opensTrackSheet = !readOnly && deviceClass !== 'desktop';
  const isSource = trackRole(track) === 'source';

  return (
    <>
      <div
        className={cn(
          'group relative flex h-9 items-center gap-1 border-b border-border text-xs text-foreground',
          deviceClass === 'desktop' ? 'px-2' : 'px-1.5',
          isSelected ? 'bg-accent/70' : 'bg-card/60 hover:bg-accent/50',
          isSource && 'border-l-2 border-l-amber-500/60',
        )}
        {...trackLabelAttrs(track.id)}
        data-track-dragging={rowDragging ? 'true' : undefined}
        onClick={() => {
          onSelect(track.id);
          if (opensTrackSheet) setTrackSheetOpen(true);
        }}
        onContextMenu={readOnly ? undefined : handleContextMenu}
      >
        <span className="pointer-events-none relative z-10 shrink-0 text-muted-foreground">
          {isSource ? (
            <span className="rounded bg-muted px-1 py-0.5 text-[9px] font-medium text-foreground" title="Source — excluded from final output" aria-label="Source — excluded from final output">Source</span>
          ) : track.kind === 'visual' ? <Video className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
        </span>

        {/* Full label shown at rest; on desktop it fades out for the hover overlay */}
        <span
          className={cn('min-w-0 flex-1 truncate', showTrackActions && (rowDragging ? 'opacity-0' : 'transition-opacity group-hover:opacity-0'))}
          title={displayLabel ?? track.label}
        >
          {displayLabel ?? track.label}
        </span>

        {showTrackActions ? (
          /* Keep the existing activator mounted during a drag. The name stays
             visible without hover, and unrelated actions release its space. */
          <div className={cn('absolute inset-0 flex items-center gap-1 px-2', rowDragging ? 'opacity-100' : 'opacity-0 transition-opacity group-hover:opacity-100')}>
            <span className={cn('shrink-0', isSource ? 'w-10' : 'w-[18px]')} />
            <input
              className="min-w-0 flex-1 bg-transparent text-xs outline-none"
              value={rowDragging ? displayLabel ?? track.label : track.label}
              aria-label="Track name"
              readOnly={rowDragging}
              onChange={(event) => onChange(track.id, { label: event.target.value })}
              onClick={(event) => event.stopPropagation()}
            />
            <div className="flex shrink-0 items-center">
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-6 w-6 cursor-grab touch-none text-muted-foreground active:cursor-grabbing"
                title="Reorder track"
                aria-label="Reorder track"
                onClick={(event) => event.stopPropagation()}
                {...dragAttributes}
                {...dragListeners}
              >
                <GripVertical className="h-3.5 w-3.5" />
              </Button>
              <TrackSettingsDialog
                track={track}
                triggerClassName={cn('h-6 w-6', rowDragging && 'hidden')}
                iconClassName="h-3.5 w-3.5"
                onChange={onChange}
              />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className={cn('h-6 w-6', rowDragging && 'hidden', confirmingDelete ? 'text-destructive hover:text-destructive' : 'text-muted-foreground')}
                title={confirmingDelete ? 'Click again to confirm deletion' : 'Remove track'}
                onClick={handleRemoveClick}
              >
                {confirmingDelete ? <Check className="h-3.5 w-3.5" /> : <Trash2 className="h-3.5 w-3.5" />}
              </Button>
            </div>
          </div>
        ) : null}
      </div>
      {opensTrackSheet && (
        <TrackSheet
          open={trackSheetOpen}
          onOpenChange={setTrackSheetOpen}
          track={track}
          hasClips={hasClips}
          confirmingDelete={confirmingDelete}
          onChange={onChange}
          onRemoveClick={handleRemoveClick}
          onAddTrack={onAddTrack}
        />
      )}
      {contextMenu && (
        <TrackExtensionContextMenu
          menu={contextMenu}
          menuRef={menuRef}
          trackId={track.id}
          closeMenu={closeMenu}
        />
      )}
    </>
  );
}

export function TrackLabel({
  id,
  track,
  isSelected,
  hasClips,
  deviceClass,
  onSelect,
  onChange,
  onRemove,
}: TrackLabelProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div ref={setNodeRef} style={style}>
      <TrackLabelContent
        track={track}
        isSelected={isSelected}
        hasClips={hasClips}
        deviceClass={deviceClass}
        onSelect={onSelect}
        onChange={onChange}
        onRemove={onRemove}
        rowDragging={isDragging}
        dragListeners={listeners}
        dragAttributes={attributes}
      />
    </div>
  );
}
