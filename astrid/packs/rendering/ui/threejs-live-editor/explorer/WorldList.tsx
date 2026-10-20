import { clockText, button } from './ui';
import type { Row } from './rows';

/** The project's one world list: worlds in the video, library worlds, the sample, and Import. */
export function WorldList({ timeline, library, selectedKey, sampleLabel, offerSample, busy, onPick, onRemove, onAddSample, onImport }: {
  timeline: readonly Row[]; library: readonly Row[]; selectedKey: string | undefined;
  sampleLabel: string; offerSample: boolean; busy: boolean;
  onPick: (key: string) => void; onRemove: (row: Row) => void; onAddSample: () => void; onImport: () => void;
}) {
  const item = (row: Row, removable: boolean) => (
    <li key={row.key} className="world-explorer-row flex min-w-0 items-center gap-1 rounded-md hover:bg-muted">
      <button
        type="button"
        className="min-h-8 min-w-0 flex-1 truncate rounded-md px-2 py-1 text-left text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        aria-current={row.key === selectedKey ? 'true' : undefined}
        style={row.key === selectedKey ? { background: 'hsl(var(--primary) / 0.12)' } : undefined}
        onClick={() => onPick(row.key)}
      >
        {row.name} <span className="tabular-nums text-muted-foreground">{clockText(row.duration)}</span>
        {row.uses.length ? <span className="text-muted-foreground"> · {row.uses.length} use{row.uses.length === 1 ? '' : 's'}</span> : null}
      </button>
      {removable ? (
        <button
          type="button"
          aria-label={`Remove ${row.name} from library`}
          title={`Remove ${row.name} from library`}
          disabled={busy}
          className="world-explorer-remove flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-muted-foreground hover:bg-background hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
          onClick={() => onRemove(row)}
        >
          <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
        </button>
      ) : null}
    </li>
  );
  return (
    <div className="flex min-w-0 flex-col gap-1" role="group" aria-label="Worlds">
      {/* The remove action stays quiet until its row is hovered or has focus inside it. */}
      <style>{'.world-explorer-remove{opacity:0}.world-explorer-row:hover .world-explorer-remove,.world-explorer-row:focus-within .world-explorer-remove{opacity:1}'}</style>
      {timeline.length ? (
        <>
          <p className="px-2 text-[10px] uppercase tracking-wide text-muted-foreground">In this video</p>
          <ul aria-label="In this video" className="flex flex-col gap-0.5">{timeline.map((row) => item(row, false))}</ul>
        </>
      ) : null}
      {library.length ? (
        <>
          <p className="px-2 pt-1 text-[10px] uppercase tracking-wide text-muted-foreground">Library</p>
          <ul aria-label="Library" className="flex flex-col gap-0.5">{library.map((row) => item(row, true))}</ul>
        </>
      ) : null}
      <div className="flex flex-wrap items-center gap-1 pt-1">
        {offerSample ? (
          <button type="button" className={`${button} border border-border`} disabled={busy} onClick={onAddSample}>Add sample: {sampleLabel}</button>
        ) : null}
        <button type="button" className={`${button} border border-border`} disabled={busy} onClick={onImport}>Import world…</button>
      </div>
    </div>
  );
}
