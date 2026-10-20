import type { PreparedShotComposition } from '../data/shotCompositionAdapter.ts';
import { serializeProjectedTimelineConfig } from '../lib/serialize.ts';
import type { TimelineHeadRevision } from '../data/DataProvider.ts';
import type { TimelineConfig } from '../types/index.ts';

// Keep recovery-only roots outside the strict display/compiled config domain.
const displayFields = {
  output: true, clips: true, tracks: true, pinnedShotGroups: true,
  theme: true, theme_overrides: true, generation_defaults: true, app: true,
} satisfies Record<keyof TimelineConfig, true>;

export function createRecoveryConfig() {
  let retained: { head: TimelineHeadRevision | undefined; roots: Record<string, unknown>; composition?: PreparedShotComposition } | undefined;
  return {
    remember(head: TimelineHeadRevision | undefined, config: unknown, composition?: PreparedShotComposition) {
      retained = {
        head: head ? { ...head } : undefined,
        composition,
        roots: structuredClone(Object.fromEntries(Object.entries(config as object)
          .filter(([key]) => !Object.prototype.hasOwnProperty.call(displayFields, key)))),
      };
    },
    snapshot(head: TimelineHeadRevision | undefined, config: TimelineConfig, derived = false, composition?: PreparedShotComposition) {
      const sameBase = retained && head?.projectId === retained.head?.projectId
        && head?.timelineId === retained.head?.timelineId
        && head?.headRevisionId === retained.head?.headRevisionId
        && head?.headPublicationId === retained.head?.headPublicationId;
      const rawComposition = composition ?? (sameBase ? retained!.composition : undefined);
      const authored = derived || rawComposition
        ? serializeProjectedTimelineConfig(config, rawComposition ?? null) : config;
      return structuredClone({ ...authored, ...(sameBase ? retained!.roots : {}) });
    },
  };
}
