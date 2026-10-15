import type { TimelineDataItemRef } from '@/shared/state/selectionStore.ts';
import type { DataLaneView } from '@/tools/video-editor/data/typed/envelope.ts';

export interface TimelineItemSelectionSummaryProps {
  readonly clipCount: number;
  readonly dataItems: readonly TimelineDataItemRef[];
  readonly lanes: readonly DataLaneView[];
}

const TRANSCRIPT_KIND_ID = 'reigh.transcript';

function plural(count: number, singular: string, pluralForm = `${singular}s`): string {
  return `${count} ${count === 1 ? singular : pluralForm}`;
}

/** Read-only summary for mixed media and typed-data timeline selections. */
export function TimelineItemSelectionSummary({
  clipCount,
  dataItems,
  lanes,
}: TimelineItemSelectionSummaryProps) {
  const totalCount = clipCount + dataItems.length;
  if (totalCount === 0) return null;

  const lanesById = new Map(lanes.map((lane) => [lane.laneId, lane]));
  const allTranscript = dataItems.length > 0 && dataItems.every(
    (item) => lanesById.get(item.laneId)?.kindId === TRANSCRIPT_KIND_ID,
  );
  const title = clipCount === 0 && allTranscript
    ? `${plural(dataItems.length, 'transcript item')} selected`
    : `${totalCount} items selected`;

  const laneCounts = new Map<string, { label: string; count: number }>();
  for (const item of dataItems) {
    const lane = lanesById.get(item.laneId);
    const label = lane?.label || 'Data items';
    const existing = laneCounts.get(item.laneId);
    laneCounts.set(item.laneId, { label, count: (existing?.count ?? 0) + 1 });
  }

  const details: string[] = [];
  if (clipCount > 0) details.push(plural(clipCount, 'media clip'));
  if (dataItems.length > 0 && allTranscript && clipCount > 0) {
    details.push(plural(dataItems.length, 'transcript item'));
  } else {
    for (const { label, count } of laneCounts.values()) details.push(`${label} · ${count}`);
  }

  return (
    <section
      aria-label="Timeline selection summary"
      aria-live="polite"
      role="status"
      data-testid="timeline-item-selection-summary"
      className="rounded-md border border-border bg-card px-3 py-2 text-sm"
    >
      <p className="font-medium text-foreground">{title}</p>
      <p className="mt-1 text-xs text-muted-foreground">{details.join(' · ')}</p>
    </section>
  );
}
