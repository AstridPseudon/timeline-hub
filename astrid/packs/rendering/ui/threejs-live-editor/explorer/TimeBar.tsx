import { useEffect, useRef, useState, type KeyboardEvent, type PointerEvent } from 'react';
import { moveRangeHandle, sliderKeyTime, type BarRange } from './model';

/** An event on the bar: a point when `to === from`, else a span. `time` is the label's clock text. */
export type BarMarker = { readonly key: string; readonly from: number; readonly to: number; readonly title: string; readonly time?: string };
/** A stretch of the world already used by a clip. */
export type BarUse = { readonly key: string; readonly from: number; readonly to: number; readonly title: string };

const FALLBACK_WIDTH = 320;
const KNOB = 12;
/** A point marker's hit area, centred on its tick. */
const POINT_HIT = 16;
/** Quiet colours only: foreground, muted and primary. */
const TRACK = 'hsl(var(--muted-foreground) / 0.28)';
const MARK = 'hsl(var(--foreground) / 0.72)';
const USE = 'hsl(var(--muted-foreground) / 0.6)';
const PRIMARY = 'hsl(var(--primary))';

const ring = 'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring';

/**
 * One time bar for both modes: a neutral track with a playhead knob, event marks drawn on the track (ticks for points,
 * tinted bands for spans, each a button that jumps; the name shows as a small tooltip on hover or focus, so there is no
 * label lane), and a thin lane of existing uses. With `range`, the
 * in/out range is a segment with two draggable handles. The track is a slider: ←/→ (Shift ×5) and Home/End.
 */
export function TimeBar({ start, end, time, label, valueText, disabled, markers = [], uses = [], range, onSeek, onJump, onRange }: {
  start: number; end: number; time: number; label: string; valueText: string; disabled?: boolean;
  markers?: readonly BarMarker[]; uses?: readonly BarUse[];
  range?: BarRange; onSeek: (time: number) => void; onJump?: (time: number) => void; onRange?: (range: BarRange) => void;
}) {
  const rail = useRef<HTMLDivElement>(null);
  const scrubbing = useRef(false);
  const dragging = useRef<'from' | 'to' | null>(null);
  const [width, setWidth] = useState(FALLBACK_WIDTH);
  const span = Math.max(end - start, 0);
  const step = Math.min(Math.max(span / 50, 0.1), 1);
  const fraction = (t: number) => (span > 0 ? Math.min(Math.max((t - start) / span, 0), 1) : 0);
  const pct = (t: number) => `${fraction(t) * 100}%`;

  useEffect(() => {
    const element = rail.current;
    if (!element) return;
    const measure = () => { if (element.clientWidth > 0) setWidth(element.clientWidth); };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  const timeAt = (clientX: number) => {
    const rect = rail.current?.getBoundingClientRect();
    const f = rect && rect.width > 0 ? Math.min(Math.max((clientX - rect.left) / rect.width, 0), 1) : 0;
    return start + f * span;
  };

  const down = (event: PointerEvent<HTMLDivElement>) => {
    if (disabled) return;
    event.currentTarget.setPointerCapture?.(event.pointerId);
    scrubbing.current = true;
    onSeek(timeAt(event.clientX));
  };
  const move = (event: PointerEvent<HTMLDivElement>) => { if (scrubbing.current) onSeek(timeAt(event.clientX)); };
  const up = (event: PointerEvent<HTMLDivElement>) => {
    scrubbing.current = false;
    event.currentTarget.releasePointerCapture?.(event.pointerId);
  };
  const keyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (disabled || event.ctrlKey || event.metaKey || event.altKey) return;
    const next = sliderKeyTime(event, { time, start, end, step });
    if (next === undefined) return;
    event.preventDefault();
    event.stopPropagation();
    onSeek(next);
  };

  const applyHandle = (which: 'from' | 'to', t: number) => {
    if (!range || !onRange) return;
    onRange(moveRangeHandle(range, which, t, { start, end }));
  };
  const handleDown = (which: 'from' | 'to') => (event: PointerEvent<HTMLDivElement>) => {
    if (disabled) return;
    event.stopPropagation();
    event.currentTarget.setPointerCapture?.(event.pointerId);
    dragging.current = which;
  };
  const handleMove = (which: 'from' | 'to') => (event: PointerEvent<HTMLDivElement>) => {
    if (dragging.current === which) applyHandle(which, timeAt(event.clientX));
  };
  const handleUp = (event: PointerEvent<HTMLDivElement>) => {
    dragging.current = null;
    event.currentTarget.releasePointerCapture?.(event.pointerId);
  };
  const handleKey = (which: 'from' | 'to') => (event: KeyboardEvent<HTMLDivElement>) => {
    if (!range || event.ctrlKey || event.metaKey || event.altKey) return;
    const current = which === 'from' ? range.from : range.to;
    const next = sliderKeyTime(event, { time: current, start, end, step: 0.1 });
    if (next === undefined) return;
    event.preventDefault();
    event.stopPropagation();
    applyHandle(which, next);
  };

  const marks = [...markers].sort((a, b) => a.from - b.from).map((marker) => ({
    marker, x: fraction(marker.from) * width, w: Math.max((fraction(marker.to) - fraction(marker.from)) * width, 0),
  }));

  const lane = 'absolute inset-y-0 left-2 right-2';

  return (
    <div className="relative mx-1.5 h-[18px] select-none" ref={rail} data-time-bar>
      <div
        role="slider"
        tabIndex={0}
        aria-label={label}
        aria-valuemin={start}
        aria-valuemax={end}
        aria-valuenow={Number(time.toFixed(2))}
        aria-valuetext={valueText}
        aria-disabled={disabled}
        className={`absolute -inset-x-2 inset-y-0 touch-none rounded-sm ${disabled ? '' : 'cursor-pointer'} ${ring}`}
        onPointerDown={down}
        onPointerMove={move}
        onPointerUp={up}
        onPointerCancel={up}
        onKeyDown={keyDown}
      >
        <div className={lane}>
          <div className="absolute inset-x-0 top-[7px] h-1 rounded-full" style={{ background: TRACK }} />
          {disabled ? null : (
            <>
              {range ? (
                <div
                  data-range-segment
                  className="absolute top-[6px] h-1.5 rounded-full"
                  style={{ left: pct(range.from), width: `calc(${pct(range.to)} - ${pct(range.from)})`, background: 'hsl(var(--primary) / 0.5)' }}
                />
              ) : null}
              {uses.map((use) => (
                <div
                  key={use.key}
                  data-use
                  title={use.title}
                  className="absolute top-[15px] h-0.5 rounded-full"
                  style={{ left: pct(use.from), width: `calc(${pct(use.to)} - ${pct(use.from)})`, background: USE }}
                />
              ))}
            </>
          )}
        </div>
      </div>

      {!disabled ? (
        <div className="pointer-events-none absolute -inset-x-2 inset-y-0">
          <div className={lane}>
            {marks.map(({ marker, x, w }) => {
              const isSpan = marker.to > marker.from;
              const name = marker.time ? `${marker.title}, ${marker.time}` : marker.title;
              const edge = fraction(marker.from) < 0.2 ? 'left' : fraction(marker.from) > 0.8 ? 'right' : 'middle';
              return (
                <button
                  key={marker.key}
                  type="button"
                  data-event-marker={isSpan ? 'band' : 'tick'}
                  aria-label={name}
                  className={`group pointer-events-auto absolute top-0 h-[18px] rounded-sm ${ring}`}
                  style={{ left: isSpan ? x : x - POINT_HIT / 2, width: isSpan ? Math.max(w, 10) : POINT_HIT }}
                  onPointerDown={(event) => event.stopPropagation()}
                  onClick={() => (onJump ?? onSeek)(marker.from)}
                >
                  {isSpan ? (
                    <span aria-hidden="true" className="absolute inset-x-0 top-[5px] h-2 rounded-[2px] border" style={{ borderColor: MARK, background: 'hsl(var(--foreground) / 0.16)' }} />
                  ) : (
                    <span aria-hidden="true" className="absolute left-[7.25px] top-[2px] h-3.5 w-[1.5px] rounded-full" style={{ background: MARK }} />
                  )}
                  {/* The name is a small tooltip above the mark, on hover or focus; the bar reserves no space for it. */}
                  <span
                    role="tooltip"
                    data-label="hover"
                    className={`pointer-events-none absolute bottom-full z-20 mb-1 hidden whitespace-nowrap rounded px-1.5 py-0.5 text-[10px] leading-3 group-hover:block group-focus-visible:block ${edge === 'left' ? 'left-0' : edge === 'right' ? 'right-0' : 'left-1/2 -translate-x-1/2'}`}
                    style={{ background: 'rgba(5, 6, 15, 0.88)', color: 'rgba(255, 255, 255, 0.92)' }}
                  >
                    {marker.title}
                  </span>
                </button>
              );
            })}
          </div>
          <div className={lane}>
            <div
              data-playhead
              aria-hidden="true"
              className="pointer-events-none absolute rounded-full"
              style={{
                left: pct(time), top: 9 - KNOB / 2, width: KNOB, height: KNOB, marginLeft: -KNOB / 2,
                background: PRIMARY, boxShadow: '0 0 0 2px hsl(var(--background))',
              }}
            />
            {/* Drawn after the knob, so the range brackets stay on top and grabbable when the playhead sits on them. */}
            {range ? (['from', 'to'] as const).map((which) => {
              const value = which === 'from' ? range.from : range.to;
              return (
                <div
                  key={which}
                  role="slider"
                  tabIndex={0}
                  data-range-handle={which}
                  aria-label={which === 'from' ? 'Range start' : 'Range end'}
                  aria-valuemin={start}
                  aria-valuemax={end}
                  aria-valuenow={Number(value.toFixed(2))}
                  className={`pointer-events-auto absolute touch-none cursor-ew-resize rounded-[3px] ${ring}`}
                  style={{
                    left: pct(value), top: 0, width: 8, height: 18,
                    marginLeft: which === 'from' ? -7 : -1,
                    background: 'hsl(var(--background))', border: `2px solid ${PRIMARY}`,
                    borderRadius: which === 'from' ? '4px 1px 1px 4px' : '1px 4px 4px 1px',
                  }}
                  onPointerDown={handleDown(which)}
                  onPointerMove={handleMove(which)}
                  onPointerUp={handleUp}
                  onPointerCancel={handleUp}
                  onKeyDown={handleKey(which)}
                />
              );
            }) : null}
          </div>
        </div>
      ) : null}
    </div>
  );
}
