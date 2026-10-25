import { useEffect, useState, type RefObject } from 'react';
import { Maximize2, Minimize2, Pause, Play, Repeat, SkipBack, Volume1, Volume2, VolumeX } from 'lucide-react';
import { Slider as SliderPrimitive } from '@base-ui/react/slider';
import type { PlayerRef } from '@remotion/player';
import { Button } from '@/shared/components/ui/button.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import { CENTISECOND_TIME_OPTIONS, formatTime } from '@/shared/lib/timeFormatting';
import {
  PREVIEW_PLAYBACK_RATES,
  setPreviewPlaybackPreferences,
  togglePreviewMuted,
  usePreviewPlaybackPreferences,
} from './previewPlaybackPreferences.ts';

/** The stage's round glass buttons: dark over any picture, in either theme. */
const STAGE_BUTTON_CLASS = 'pointer-events-auto shrink-0 rounded-full border-[color:var(--video-editor-stage-control-border)] bg-[var(--video-editor-stage-control-bg)] text-[color:var(--video-editor-stage-fg)] hover:bg-[var(--video-editor-stage-control-bg-hover)] hover:text-[color:var(--video-editor-stage-fg)]';
const STAGE_BUTTON_ON_CLASS = 'border-[color:var(--video-editor-accent-border)] bg-[var(--video-editor-accent-bg-strong)] text-[color:var(--video-editor-accent-text)] hover:bg-[var(--video-editor-accent-bg-hover)] hover:text-[color:var(--video-editor-accent-text)]';
const STAGE_TEXT_CLASS = 'font-mono text-xs tabular-nums tracking-[0.08em] text-[color:var(--video-editor-stage-fg-muted)]';

/** A mouse press must not leave focus on the button, so Space keeps meaning play. */
const keepFocus = (event: { preventDefault: () => void }) => event.preventDefault();

export interface PreviewTransportProps {
  playerRef: RefObject<PlayerRef>;
  fps: number;
  durationInFrames: number;
  isPlaying: boolean;
  canPlay: boolean;
  /** Shown in the middle of the bar when set (the full editor's output size). */
  resolution?: string | null;
  /** The narrow bar (condensed editor, phone): listening, transport and fullscreen only. */
  compact: boolean;
  /** Phone/tablet: touch-sized buttons, and mute in place of a volume slider (iOS fixes media volume). */
  touchChrome: boolean;
  /** Volume, speed, loop and fullscreen beside the transport. A staged shell that sizes the
   *  transport itself (the public homepage) keeps to jump and play. */
  playerControls: boolean;
  fullscreen: boolean;
  /** Fullscreen while playing and idle: the bar fades away. */
  idle: boolean;
  onTogglePlay: () => void;
  onJumpToStart: () => void;
  onSeekFrame: (frame: number) => void;
  onToggleFullscreen: () => void;
}

export function PreviewTransport({
  playerRef,
  fps,
  durationInFrames,
  isPlaying,
  canPlay,
  resolution,
  compact,
  touchChrome,
  playerControls,
  fullscreen,
  idle,
  onTogglePlay,
  onJumpToStart,
  onSeekFrame,
  onToggleFullscreen,
}: PreviewTransportProps) {
  const { loop, rate } = usePreviewPlaybackPreferences();
  const large = touchChrome || fullscreen;
  const buttonSize = large ? 'h-11 w-11' : 'h-8 w-8';
  const iconSize = large ? 'h-[18px] w-[18px]' : 'h-4 w-4';
  // Speed and loop are for watching; the narrow bar keeps to the essentials until fullscreen.
  const showWatchControls = fullscreen || !compact;

  return (
    <div
      className={cn(
        'astrid-preview-transport pointer-events-none absolute inset-x-0 bottom-0 z-10 px-3 transition-[opacity,visibility] duration-300',
        fullscreen ? 'pb-4 pt-12' : 'py-3',
        idle && 'invisible opacity-0',
      )}
      style={{
        // Fullscreen: a deeper fade, so the scrubber reads over a bright picture.
        backgroundImage: fullscreen
          ? 'linear-gradient(to top, var(--video-editor-stage-control-bg-strong), var(--video-editor-stage-control-bg) 55%, transparent)'
          : 'linear-gradient(to top, var(--video-editor-stage-gradient-start), transparent)',
        ...(fullscreen ? {
          paddingLeft: 'max(1rem, env(safe-area-inset-left))',
          paddingRight: 'max(1rem, env(safe-area-inset-right))',
          paddingBottom: 'max(1rem, env(safe-area-inset-bottom))',
        } : null),
      }}
      data-preview-transport
    >
      {fullscreen && (
        <PreviewScrubber playerRef={playerRef} fps={fps} durationInFrames={durationInFrames} touch={touchChrome} onSeekFrame={onSeekFrame} />
      )}
      {/* Play sits in the middle while there is room; on a narrow screen the sides keep their
          width and the middle gives way, so nothing overlaps. A phone held upright in fullscreen
          spreads the whole row evenly instead. */}
      <div
        className={cn(
          'grid grid-cols-[minmax(max-content,1fr)_auto_minmax(max-content,1fr)] items-center gap-2',
          fullscreen && 'max-sm:flex max-sm:justify-between',
        )}
      >
        <div className={cn('flex min-w-0 items-center gap-2 justify-self-start', fullscreen && 'max-sm:contents')}>
          {playerControls && <PreviewVolumeControl buttonSize={buttonSize} iconSize={iconSize} slider={!touchChrome} />}
        </div>
        <div className={cn('flex items-center gap-2', fullscreen && 'max-sm:contents')}>
          <Button
            type="button"
            variant="outline"
            size="icon"
            className={cn(STAGE_BUTTON_CLASS, buttonSize)}
            onMouseDown={keepFocus}
            onClick={onJumpToStart}
            title="Jump to beginning"
            aria-label="Jump to beginning"
          >
            <SkipBack className={iconSize} />
          </Button>
          <Button
            type="button"
            variant="outline"
            size="icon"
            className={cn(STAGE_BUTTON_CLASS, large ? 'h-12 w-12' : 'h-10 w-10')}
            disabled={!canPlay}
            onMouseDown={keepFocus}
            onClick={onTogglePlay}
            title={isPlaying ? 'Pause (Space)' : 'Play (Space)'}
            aria-label={isPlaying ? 'Pause' : 'Play'}
          >
            {isPlaying ? <Pause className={iconSize} /> : <Play className={cn(iconSize, 'fill-current')} />}
          </Button>
          {resolution && !compact && !fullscreen && (
            <div className="pointer-events-none rounded-full bg-background/70 px-2 py-1 text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
              {resolution}
            </div>
          )}
        </div>
        <div className={cn('flex min-w-0 items-center justify-end gap-2 justify-self-end', fullscreen && 'max-sm:contents')}>
          {playerControls && showWatchControls && (
            <>
              <PreviewSpeedSelect rate={rate} large={large} />
              <Button
                type="button"
                variant="outline"
                size="icon"
                className={cn(STAGE_BUTTON_CLASS, buttonSize, loop && STAGE_BUTTON_ON_CLASS)}
                onMouseDown={keepFocus}
                onClick={() => setPreviewPlaybackPreferences({ loop: !loop })}
                aria-pressed={loop}
                title={loop ? 'Loop on' : 'Loop off'}
                aria-label="Loop playback"
              >
                <Repeat className={iconSize} />
              </Button>
            </>
          )}
          {playerControls && (
            <Button
              type="button"
              variant="outline"
              size="icon"
              className={cn(STAGE_BUTTON_CLASS, buttonSize)}
              onMouseDown={keepFocus}
              onClick={onToggleFullscreen}
              title={fullscreen ? 'Exit full screen (Esc)' : 'Full screen (F)'}
              aria-label={fullscreen ? 'Exit full screen' : 'Full screen'}
            >
              {fullscreen ? <Minimize2 className={iconSize} /> : <Maximize2 className={iconSize} />}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

function StageSlider({
  value,
  max,
  step,
  label,
  valueText,
  onChange,
  className,
  thumbClassName,
}: {
  value: number;
  max: number;
  step: number;
  label: string;
  valueText: string;
  onChange: (value: number) => void;
  className?: string;
  thumbClassName?: string;
}) {
  return (
    <SliderPrimitive.Root
      value={value}
      min={0}
      max={max}
      step={step}
      thumbAlignment="edge"
      onValueChange={(next) => onChange(Array.isArray(next) ? (next[0] ?? 0) : (next as number))}
      className={cn('group/stage-slider pointer-events-auto relative flex touch-none select-none items-center', className)}
    >
      <SliderPrimitive.Control className="flex h-full w-full cursor-pointer items-center">
        <SliderPrimitive.Track className="relative h-1 w-full rounded-full bg-[var(--video-editor-stage-ghost-border)] transition-[height] duration-150 group-hover/stage-slider:h-1.5 group-data-[dragging]/stage-slider:h-1.5">
          <SliderPrimitive.Indicator className="absolute h-full rounded-full bg-[var(--video-editor-stage-fg)]" />
          <SliderPrimitive.Thumb
            getAriaLabel={() => label}
            getAriaValueText={() => valueText}
            className={cn(
              'h-3 w-3 rounded-full bg-[var(--video-editor-stage-fg)] shadow-[0_0_0_4px_rgb(0_0_0/0.18)] outline-none transition-opacity duration-150 focus-visible:ring-2 focus-visible:ring-[var(--video-editor-accent-border-strong)]',
              thumbClassName,
            )}
          />
        </SliderPrimitive.Track>
      </SliderPrimitive.Control>
    </SliderPrimitive.Root>
  );
}

function PreviewVolumeControl({ buttonSize, iconSize, slider }: { buttonSize: string; iconSize: string; slider: boolean }) {
  const { volume, muted } = usePreviewPlaybackPreferences();
  const level = muted ? 0 : volume;
  const Icon = level === 0 ? VolumeX : level < 0.5 ? Volume1 : Volume2;
  const percent = Math.round(level * 100);
  return (
    // Hovering or focusing the group opens the level, as video players do; touch keeps to mute.
    <div className="group/volume pointer-events-auto flex min-w-0 items-center">
      <Button
        type="button"
        variant="outline"
        size="icon"
        className={cn(STAGE_BUTTON_CLASS, buttonSize)}
        onMouseDown={keepFocus}
        onClick={togglePreviewMuted}
        aria-pressed={level === 0}
        title={level === 0 ? 'Unmute' : 'Mute'}
        aria-label="Mute preview"
      >
        <Icon className={iconSize} />
      </Button>
      {slider && (
        <div className="w-0 overflow-hidden opacity-0 transition-[width,opacity] duration-200 ease-out group-hover/volume:w-[5.5rem] group-hover/volume:opacity-100 group-focus-within/volume:w-[5.5rem] group-focus-within/volume:opacity-100">
          <StageSlider
            className="ml-2.5 mr-1 h-6 w-[4.75rem]"
            value={level}
            max={1}
            step={0.01}
            label="Preview volume"
            valueText={`${percent}%`}
            onChange={(next) => setPreviewPlaybackPreferences({ volume: next, muted: next === 0 })}
          />
        </div>
      )}
    </div>
  );
}

function formatRate(rate: number): string {
  return `${rate}×`;
}

function PreviewSpeedSelect({ rate, large }: { rate: number; large: boolean }) {
  return (
    // A native list: it opens over a fullscreen element and on phones, where a portal popover cannot.
    <label
      className={cn(
        STAGE_BUTTON_CLASS,
        'relative inline-flex items-center justify-center border px-2.5 text-[11px] font-medium tabular-nums transition-colors focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2 focus-within:ring-offset-background',
        large ? 'h-11 min-w-11' : 'h-8 min-w-8',
        rate !== 1 && STAGE_BUTTON_ON_CLASS,
      )}
      title="Playback speed"
    >
      <span aria-hidden>{formatRate(rate)}</span>
      <select
        aria-label="Playback speed"
        value={String(rate)}
        onChange={(event) => setPreviewPlaybackPreferences({ rate: Number(event.target.value) })}
        className="absolute inset-0 cursor-pointer appearance-none rounded-full opacity-0"
      >
        {PREVIEW_PLAYBACK_RATES.map((option) => (
          <option key={option} value={String(option)}>{option === 1 ? 'Normal' : formatRate(option)}</option>
        ))}
      </select>
    </label>
  );
}

/** Fullscreen hides the timeline, so the picture carries its own position and scrubber. */
function PreviewScrubber({
  playerRef,
  fps,
  durationInFrames,
  touch,
  onSeekFrame,
}: {
  playerRef: RefObject<PlayerRef>;
  fps: number;
  durationInFrames: number;
  /** Touch has no hover, so the handle stays in view. */
  touch: boolean;
  onSeekFrame: (frame: number) => void;
}) {
  const [frame, setFrame] = useState(() => playerRef.current?.getCurrentFrame() ?? 0);
  useEffect(() => {
    const player = playerRef.current;
    if (!player) return undefined;
    const onFrame = (event: { detail: { frame: number } }) => setFrame(event.detail.frame);
    setFrame(player.getCurrentFrame());
    player.addEventListener('frameupdate', onFrame);
    return () => player.removeEventListener('frameupdate', onFrame);
  }, [playerRef]);
  const lastFrame = Math.max(0, durationInFrames - 1);
  const shown = Math.min(frame, lastFrame);
  const time = (value: number) => formatTime(value / fps, CENTISECOND_TIME_OPTIONS);
  return (
    <div className="mb-3 flex items-center gap-3">
      <span className={cn(STAGE_TEXT_CLASS, 'shrink-0')}>{time(shown)}</span>
      <StageSlider
        className="h-5 min-w-0 flex-1"
        thumbClassName={touch ? undefined : 'opacity-0 group-hover/stage-slider:opacity-100 group-focus-within/stage-slider:opacity-100 group-data-[dragging]/stage-slider:opacity-100'}
        value={shown}
        max={Math.max(1, lastFrame)}
        step={1}
        label="Playback position"
        valueText={`${time(shown)} of ${time(durationInFrames)}`}
        onChange={(next) => {
          setFrame(next);
          onSeekFrame(Math.round(next));
        }}
      />
      <span className={cn(STAGE_TEXT_CLASS, 'shrink-0 text-[color:var(--video-editor-stage-fg-subtle)]')}>{time(durationInFrames)}</span>
    </div>
  );
}

