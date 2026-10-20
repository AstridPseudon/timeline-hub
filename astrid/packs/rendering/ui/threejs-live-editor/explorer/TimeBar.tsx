import { useRef, type PointerEvent, type ReactNode } from 'react';

export type BarMarker = { readonly key: string; readonly from: number; readonly to: number; readonly title: string };

/** A scrubbable time bar over [start, end]. Events are ticks (points) or bands (spans); children add more layers. */
export function TimeBar({ start, end, time, label, valueText, disabled, markers = [], onSeek, children }: {
  start: number; end: number; time: number; label: string; valueText: string; disabled?: boolean;
  markers?: readonly BarMarker[]; onSeek: (time: number) => void;
  children?: (pct: (time: number) => string) => ReactNode;
}) {
  const bar = useRef<HTMLDivElement>(null);
  const scrubbing = useRef(false);
  const span = Math.max(end - start, 0);
  const pct = (t: number) => `${span > 0 ? Math.min(Math.max((t - start) / span, 0), 1) * 100 : 0}%`;
  const timeAt = (clientX: number) => {
    const rect = bar.current?.getBoundingClientRect();
    const fraction = rect && rect.width > 0 ? Math.min(Math.max((clientX - rect.left) / rect.width, 0), 1) : 0;
    return start + fraction * span;
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
  return (
    <div
      ref={bar}
      role="slider"
      tabIndex={0}
      aria-label={label}
      aria-valuemin={start}
      aria-valuemax={end}
      aria-valuenow={Number(time.toFixed(2))}
      aria-valuetext={valueText}
      aria-disabled={disabled}
      className="relative h-7 touch-none select-none rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      onPointerDown={down}
      onPointerMove={move}
      onPointerUp={up}
      onPointerCancel={up}
    >
      <div className="absolute inset-x-0 top-1/2 h-1 -translate-y-1/2 rounded-full" style={{ background: 'hsl(var(--muted-foreground) / 0.25)' }} />
      {disabled ? null : (
        <>
          {children?.(pct)}
          {markers.map((marker) => (marker.to > marker.from ? (
            <div
              key={marker.key}
              data-event-marker="band"
              title={marker.title}
              className="absolute top-1/2 h-2 -translate-y-1/2 rounded-sm"
              style={{ left: pct(marker.from), width: `calc(${pct(marker.to)} - ${pct(marker.from)})`, minWidth: 3, background: 'hsl(var(--foreground) / 0.28)' }}
            />
          ) : (
            <span
              key={marker.key}
              data-event-marker="tick"
              title={marker.title}
              className="absolute top-1/2 h-3.5 w-px -translate-y-1/2"
              style={{ left: pct(marker.from), background: 'hsl(var(--foreground) / 0.7)' }}
            />
          )))}
          <div className="absolute inset-y-0 w-px" style={{ left: pct(time), background: 'hsl(var(--primary))' }} />
        </>
      )}
    </div>
  );
}
