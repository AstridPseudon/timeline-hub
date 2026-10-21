import type { CSSProperties } from 'react';
import { EDITOR_TOUR_MEDIA, type EditorTourMediaSlot } from '../tourMedia';
import { TourMedia, type TourMediaKind } from './TourMedia';
import { cn } from '@/shared/components/ui/contracts/cn.ts';

const NODES: ReadonlyArray<{ kind: TourMediaKind; slot: EditorTourMediaSlot }> = [
  { kind: 'frame', slot: EDITOR_TOUR_MEDIA.frames[0] },
  { kind: 'still', slot: EDITOR_TOUR_MEDIA.stills[0] },
  { kind: 'video', slot: EDITOR_TOUR_MEDIA.video },
];

const delay = (ms: number) => ({ '--tour-delay': `${ms}ms` }) as CSSProperties;

/**
 * Three.js frame → realistic frames → video. Steps up to `filled` show their media; the newest one arrives with the
 * card (its connector draws in, then the thumbnail fades up); later steps wait as empty frames.
 */
export function TourStrip({ filled, labels, size = 'compact', playing = false }: {
  filled: 1 | 2 | 3;
  labels: readonly [string, string, string];
  size?: 'compact' | 'large';
  /** The video step loops (large strip only). */
  playing?: boolean;
}) {
  const large = size === 'large';
  return (
    <ol className="flex items-start" aria-label={labels.join(', then ')}>
      {NODES.map((node, index) => {
        const reached = index < filled;
        const newest = !large && index === filled - 1;
        return (
          <li key={node.kind} className={cn('flex items-start', index > 0 && 'flex-1')}>
            {index > 0 && (
              <span aria-hidden="true" className={cn('relative mx-2 h-px flex-1 bg-border', large ? 'mt-[27px]' : 'mt-4')}>
                {reached && <span className={cn('absolute inset-0 origin-left bg-primary/60', newest && 'editor-tour-grow')} style={delay(700)} />}
              </span>
            )}
            <span className={cn('flex flex-col items-center gap-1.5', large ? 'w-24' : 'w-14')}>
              <span
                className={cn(
                  'relative block overflow-hidden rounded-[5px]',
                  large ? 'h-[54px] w-24' : 'h-8 w-14',
                  reached ? 'bg-muted shadow-sm ring-1 ring-border' : 'border border-dashed border-border',
                  newest && 'ring-primary/70',
                )}
              >
                {reached && (
                  <span className={cn('absolute inset-0', newest && 'editor-tour-fade')} style={delay(1000)}>
                    <TourMedia slot={node.slot} kind={node.kind} poster={EDITOR_TOUR_MEDIA.stills[0].url} playing={large && playing && node.kind === 'video'} />
                  </span>
                )}
              </span>
              <span className={cn('whitespace-nowrap leading-none', large ? 'text-xs text-foreground' : 'text-[11px]', reached ? (large ? '' : 'text-foreground') : 'text-muted-foreground')}>
                {labels[index]}
              </span>
            </span>
          </li>
        );
      })}
    </ol>
  );
}
