import type { TimelineHeadRevision } from '../data/DataProvider.ts';
import type { TimelineConfig } from '../types/index.ts';

// Keep recovery-only roots outside the strict display/compiled config domain.
const displayFields = {
  output: true, clips: true, tracks: true, pinnedShotGroups: true,
  theme: true, theme_overrides: true, generation_defaults: true, app: true,
} satisfies Record<keyof TimelineConfig, true>;

export function createRecoveryConfig() {
  let retained: { head: TimelineHeadRevision | undefined; roots: Record<string, unknown> } | undefined;
  return {
    remember(head: TimelineHeadRevision | undefined, config: unknown) {
      retained = {
        head: head ? { ...head } : undefined,
        roots: structuredClone(Object.fromEntries(Object.entries(config as object)
          .filter(([key]) => !Object.prototype.hasOwnProperty.call(displayFields, key)))),
      };
    },
    snapshot(head: TimelineHeadRevision | undefined, config: TimelineConfig) {
      const sameBase = retained && head?.projectId === retained.head?.projectId
        && head?.timelineId === retained.head?.timelineId
        && head?.headRevisionId === retained.head?.headRevisionId
        && head?.headPublicationId === retained.head?.headPublicationId;
      return structuredClone({ ...config, ...(sameBase ? retained!.roots : {}) });
    },
  };
}
