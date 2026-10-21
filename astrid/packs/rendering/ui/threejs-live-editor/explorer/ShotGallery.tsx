import { useEffect, useId, useMemo, useRef, useState, type DragEvent } from 'react';
import type { PanelClipDragProps } from '@astrid/editor-sdk';
import { useShotStill } from '../useShotStill';
import { clockText } from './ui';

/** A 3 x 3 grid per page. */
export const SHOTS_PER_PAGE = 9;

export type GalleryShot = { readonly name: string; readonly start: number; readonly end: number };

/** Case-insensitive name match; blank query keeps everything. Keeps each shot's index in the full list. */
export function filterShots<T extends { readonly name: string }>(shots: readonly T[], query: string): { shot: T; index: number }[] {
  const needle = query.trim().toLowerCase();
  const all = shots.map((shot, index) => ({ shot, index }));
  return needle ? all.filter(({ shot }) => shot.name.toLowerCase().includes(needle)) : all;
}

export const pageCount = (matches: number, perPage = SHOTS_PER_PAGE) => Math.max(1, Math.ceil(matches / perPage));

const GRIP = (
  <svg aria-hidden="true" width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><circle cx="9" cy="6" r="1.8" /><circle cx="15" cy="6" r="1.8" /><circle cx="9" cy="12" r="1.8" /><circle cx="15" cy="12" r="1.8" /><circle cx="9" cy="18" r="1.8" /><circle cx="15" cy="18" r="1.8" /></svg>
);
const PLUS = (
  <svg aria-hidden="true" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round"><path d="M12 5v14M5 12h14" /></svg>
);
const OVERLAY = { background: 'rgba(5, 6, 15, 0.7)', color: 'rgba(255, 255, 255, 0.9)' } as const;

function Still({ revision, start, name }: { revision: string; start: number; name: string }) {
  const still = useShotStill(revision, start);
  if (still.status === 'ready') {
    return <img src={still.url} alt="" draggable={false} className="h-full w-full object-cover" width={320} height={180} />;
  }
  return (
    <div
      className={`grid h-full w-full place-items-center text-[10px] text-muted-foreground ${still.status === 'error' ? '' : 'animate-pulse'}`}
      style={{ background: 'hsl(var(--muted) / 0.6)' }}
      role="img"
      aria-label={still.status === 'error' ? `No preview for ${name}` : `Loading preview of ${name}`}
    >
      {still.status === 'error' ? 'No preview' : null}
    </div>
  );
}

function ShotCard({ shot, index, current, revision, fullscreen, addDisabled, addTitle, dragProps, onSelect, onAdd }: {
  shot: GalleryShot; index: number; current: boolean; revision: string; fullscreen: boolean;
  addDisabled: boolean; addTitle?: string;
  dragProps: PanelClipDragProps | null;
  onSelect: (index: number) => void; onAdd: (index: number) => void;
}) {
  const card = useRef<HTMLLIElement>(null);
  const range = `${clockText(shot.start)} – ${clockText(shot.end)}`;
  return (
    <li ref={card} className="group relative flex min-w-0 flex-col gap-1" data-shot-card data-current={current ? 'true' : undefined}>
      <button
        type="button"
        aria-current={current ? 'true' : undefined}
        aria-label={`${shot.name}, ${range}`}
        title={`Play ${shot.name}`}
        className="flex min-w-0 flex-col gap-1 rounded-md p-1 text-left hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        style={current ? { background: 'hsl(var(--primary) / 0.12)', boxShadow: 'inset 0 0 0 1.5px hsl(var(--primary) / 0.7)' } : undefined}
        onClick={() => onSelect(index)}
      >
        <span className="block aspect-video w-full overflow-hidden rounded" style={{ background: '#05060f' }}>
          <Still revision={revision} start={shot.start} name={shot.name} />
        </span>
        <span className="truncate text-xs font-medium leading-tight">{shot.name}</span>
        <span className="truncate text-[10px] tabular-nums leading-tight text-muted-foreground">{range}</span>
      </button>
      {fullscreen ? (
        <button
          type="button"
          aria-label={`Add ${shot.name} to video`}
          title={addTitle ?? `Add ${shot.name} to the video at the playhead`}
          disabled={addDisabled}
          className="absolute right-2 top-2 flex h-6 items-center gap-1 rounded-full px-2 text-[10px] opacity-90 hover:opacity-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-40"
          style={OVERLAY}
          onClick={() => onAdd(index)}
        >
          {PLUS}Add
        </button>
      ) : dragProps ? (
        <span
          {...dragProps}
          aria-hidden="true"
          data-testid="shot-drag-handle"
          title={`Drag ${shot.name} onto the timeline`}
          className="absolute left-2 top-2 flex h-6 w-6 cursor-grab items-center justify-center rounded-full active:cursor-grabbing"
          style={OVERLAY}
          onDragStart={(event: DragEvent<HTMLSpanElement>) => {
            dragProps.onDragStart(event);
            try { if (card.current) event.dataTransfer.setDragImage(card.current, 16, 16); } catch { /* the default ghost is fine */ }
          }}
        >
          {GRIP}
        </span>
      ) : null}
    </li>
  );
}

/**
 * The Shots view: one searchable, paged gallery (3 x 3 per page) of a world's shots, each with its
 * start-frame still. Docked, a card's grip drags the shot onto the timeline; in full screen the
 * timeline is covered, so a card offers "Add to video" instead.
 */
export function ShotGallery({ shots, currentIndex, revision, fullscreen, addDisabled, addTitle, dragPropsFor, onSelect, onAdd }: {
  shots: readonly GalleryShot[];
  currentIndex: number;
  revision: string;
  fullscreen: boolean;
  addDisabled: boolean;
  addTitle?: string;
  dragPropsFor: (index: number) => PanelClipDragProps | null;
  onSelect: (index: number) => void;
  onAdd: (index: number) => void;
}) {
  const [query, setQuery] = useState('');
  const [requestedPage, setRequestedPage] = useState(0);
  const searchId = useId();
  const matches = useMemo(() => filterShots(shots, query), [shots, query]);
  const pages = pageCount(matches.length);
  const page = Math.min(requestedPage, pages - 1);
  const visible = matches.slice(page * SHOTS_PER_PAGE, (page + 1) * SHOTS_PER_PAGE);
  const searching = query.trim() !== '';
  // A different world starts again from the first page with no filter.
  const lastRevision = useRef(revision);
  useEffect(() => {
    if (lastRevision.current === revision) return;
    lastRevision.current = revision;
    setQuery('');
    setRequestedPage(0);
  }, [revision]);

  const countText = shots.length === 0 ? 'No shots yet'
    : searching ? `${matches.length} of ${shots.length} ${shots.length === 1 ? 'shot' : 'shots'}`
      : `${shots.length} ${shots.length === 1 ? 'shot' : 'shots'}`;

  return (
    <section aria-label="Shots" className="flex min-w-0 flex-col gap-2" data-testid="shot-gallery">
      {/* The search row stays at the top of the scroller while the cards scroll under it; the pager keeps one width on every page. */}
      <div className="sticky top-0 z-10 -mt-1 flex items-center gap-2 bg-background pb-1 pt-1">
        <label htmlFor={searchId} className="sr-only">Search shots</label>
        <input
          id={searchId}
          type="search"
          value={query}
          placeholder="Search shots"
          autoComplete="off"
          className="min-h-10 min-w-0 flex-1 rounded-md border border-border/70 bg-transparent px-2 text-xs placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring sm:min-h-8"
          onChange={(event) => { setQuery(event.target.value); setRequestedPage(0); }}
          onKeyDown={(event) => { if (event.key === 'Escape' && query) { event.stopPropagation(); setQuery(''); setRequestedPage(0); } }}
        />
        <span aria-live="polite" className="shrink-0 text-[11px] tabular-nums text-muted-foreground">{countText}</span>
        {pages > 1 ? (
          <nav aria-label="Shots pages" className="flex shrink-0 items-center">
            <button type="button" aria-label="Previous page" className="flex h-8 w-7 items-center justify-center rounded-md text-sm hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-40" disabled={page === 0} onClick={() => setRequestedPage(page - 1)}>‹</button>
            <span className="text-center text-[11px] tabular-nums text-muted-foreground" style={{ minWidth: `${String(pages).length * 2 + 3}ch` }} aria-live="polite" aria-label={`Page ${page + 1} of ${pages}`}>{page + 1} / {pages}</span>
            <button type="button" aria-label="Next page" className="flex h-8 w-7 items-center justify-center rounded-md text-sm hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-40" disabled={page >= pages - 1} onClick={() => setRequestedPage(page + 1)}>›</button>
          </nav>
        ) : null}
      </div>

      {matches.length === 0 ? (
        <div className="flex flex-col items-center gap-2 rounded-md border border-dashed border-border/70 px-3 py-6 text-center text-xs text-muted-foreground">
          {searching ? (
            <>
              <p>No shots match &ldquo;{query.trim()}&rdquo;</p>
              <button type="button" className="rounded-md border border-border/70 px-2 py-1 hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" onClick={() => { setQuery(''); setRequestedPage(0); }}>Clear search</button>
            </>
          ) : (
            <p>This world has no shots yet. It will show its whole length as one shot.</p>
          )}
        </div>
      ) : (
        <ul aria-label="Shots" className="m-0 grid list-none grid-cols-3 gap-x-1 gap-y-2 p-0">
          {visible.map(({ shot, index }) => (
            <ShotCard
              key={`${index}:${shot.start}:${shot.name}`}
              shot={shot}
              index={index}
              current={index === currentIndex}
              revision={revision}
              fullscreen={fullscreen}
              addDisabled={addDisabled}
              addTitle={addTitle}
              dragProps={fullscreen ? null : dragPropsFor(index)}
              onSelect={onSelect}
              onAdd={onAdd}
            />
          ))}
        </ul>
      )}

    </section>
  );
}
