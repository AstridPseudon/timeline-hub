export type D141jVisibilityEvent = Readonly<{
  kind: 'accepted-canonical-read';
  acceptedReadId: string;
  projectId: string;
  parentDocumentId: string;
  acceptedReadHeadRevisionId: string;
  previousAcceptedReadHeadRevisionId: string | null;
  occurrenceIds: readonly string[];
}> | Readonly<{
  kind: 'active-occurrences-before-useShotGroups';
  acceptedReadId: string;
  projectId: string;
  parentDocumentId: string;
  acceptedReadHeadRevisionId: string;
  occurrenceIds: readonly string[];
}> | Readonly<{
  kind: 'useShotGroups-input-and-result';
  acceptedReadId: string;
  inputOccurrenceIds: readonly string[];
  resultOccurrenceIds: readonly string[];
  resultGroupKeys: readonly string[];
  resultGroupCount: number;
}> | Readonly<{
  kind: 'before-shot-group-overlay';
  acceptedReadId: string;
  canonicalOccurrenceIds: readonly string[];
  shotGroupOccurrenceIds: readonly string[];
  shotGroupKeys: readonly string[];
  shotGroupCount: number;
}>;

export type D141jVisibilityArtifact = Readonly<{
  schema: 'timeline.app.d141j.visibility.v1';
  expectedOccurrenceId: string;
  events: readonly D141jVisibilityEvent[];
}>;

export type D141jVisibilityCollector = Readonly<{
  record: (event: D141jVisibilityEvent) => void;
  nextAcceptedReadId: () => string;
  snapshot: () => D141jVisibilityArtifact;
}>;

let activeCollector: D141jVisibilityCollector | null = null;
const readCorrelationByOccurrences = new WeakMap<object, Readonly<{
  acceptedReadId: string;
  projectId: string;
  parentDocumentId: string;
  acceptedReadHeadRevisionId: string;
}>>();

export function createD141jVisibilityCollector(expectedOccurrenceId: string): D141jVisibilityCollector {
  const events: D141jVisibilityEvent[] = [];
  let acceptedReadCount = 0;
  return {
    record(event) {
      events.push(event);
    },
    nextAcceptedReadId() {
      acceptedReadCount += 1;
      return `accepted-read-${acceptedReadCount}`;
    },
    snapshot() {
      return {
        schema: 'timeline.app.d141j.visibility.v1',
        expectedOccurrenceId,
        events: events.map((event) => ({ ...event })),
      };
    },
  };
}

export function installD141jVisibilityCollector(collector: D141jVisibilityCollector): () => void {
  const previousCollector = activeCollector;
  activeCollector = collector;
  return () => {
    if (activeCollector === collector) activeCollector = previousCollector;
  };
}

export function observeD141jAcceptedCanonicalRead({
  projectId,
  parentDocumentId,
  acceptedReadHeadRevisionId,
  previousAcceptedReadHeadRevisionId,
  occurrenceIds,
  occurrences,
}: {
  projectId: string;
  parentDocumentId: string;
  acceptedReadHeadRevisionId: string;
  previousAcceptedReadHeadRevisionId: string | null;
  occurrenceIds: readonly string[];
  occurrences?: readonly { occurrenceId: string }[];
}): void {
  if (!activeCollector) return;
  const acceptedReadId = activeCollector.nextAcceptedReadId();
  if (occurrences) {
    readCorrelationByOccurrences.set(occurrences, {
      acceptedReadId,
      projectId,
      parentDocumentId,
      acceptedReadHeadRevisionId,
    });
  }
  activeCollector?.record({
    kind: 'accepted-canonical-read',
    acceptedReadId,
    projectId,
    parentDocumentId,
    acceptedReadHeadRevisionId,
    previousAcceptedReadHeadRevisionId,
    occurrenceIds: [...occurrenceIds],
  });
}

export function observeD141jActiveOccurrencesBeforeUseShotGroups(
  canonicalOccurrences: ReadonlyArray<{
    projectId: string;
    parentDocumentId: string;
    occurrenceId: string;
  }>,
): void {
  if (!activeCollector) return;
  const acceptedRead = [...canonicalOccurrences][0];
  if (!acceptedRead) return;
  const correlation = readCorrelationByOccurrences.get(canonicalOccurrences);
  if (!correlation) return;
  const occurrenceIds = canonicalOccurrences.map((occurrence) => occurrence.occurrenceId);
  activeCollector.record({
    kind: 'active-occurrences-before-useShotGroups',
    acceptedReadId: correlation?.acceptedReadId ?? '',
    projectId: correlation?.projectId ?? acceptedRead.projectId,
    parentDocumentId: correlation?.parentDocumentId ?? acceptedRead.parentDocumentId,
    acceptedReadHeadRevisionId: correlation?.acceptedReadHeadRevisionId ?? '',
    occurrenceIds,
  });
}

export function observeD141jUseShotGroupsInputAndResult(
  inputOccurrences: ReadonlyArray<{ occurrenceId: string }>,
  resultGroups: ReadonlyArray<{
    canonicalIdentity?: { occurrenceId: string };
    pendingOccurrenceId?: string;
    shotId: string;
    start: number;
    end?: number;
  }>,
): void {
  if (!activeCollector) return;
  const correlation = readCorrelationByOccurrences.get(inputOccurrences);
  if (!correlation) return;
  activeCollector.record({
    kind: 'useShotGroups-input-and-result',
    acceptedReadId: correlation?.acceptedReadId ?? '',
    inputOccurrenceIds: inputOccurrences.map((occurrence) => occurrence.occurrenceId),
    resultOccurrenceIds: resultGroups
      .map((group) => group.canonicalIdentity?.occurrenceId ?? group.pendingOccurrenceId ?? '')
      .filter((occurrenceId) => occurrenceId.length > 0),
    resultGroupKeys: resultGroups.map((group) => (
      group.canonicalIdentity?.occurrenceId ?? group.pendingOccurrenceId ?? group.shotId
    )),
    resultGroupCount: resultGroups.length,
  });
}

export function observeD141jBeforeShotGroupOverlay(
  canonicalOccurrences: ReadonlyArray<{ occurrenceId: string }>,
  shotGroups: ReadonlyArray<{
    canonicalIdentity?: { occurrenceId: string };
    pendingOccurrenceId?: string;
    shotId: string;
  }>,
): void {
  if (!activeCollector) return;
  const correlation = readCorrelationByOccurrences.get(canonicalOccurrences);
  if (!correlation) return;
  activeCollector.record({
    kind: 'before-shot-group-overlay',
    acceptedReadId: correlation?.acceptedReadId ?? '',
    canonicalOccurrenceIds: canonicalOccurrences.map((occurrence) => occurrence.occurrenceId),
    shotGroupOccurrenceIds: shotGroups
      .map((group) => group.canonicalIdentity?.occurrenceId ?? group.pendingOccurrenceId ?? '')
      .filter((occurrenceId) => occurrenceId.length > 0),
    shotGroupKeys: shotGroups.map((group) => (
      group.canonicalIdentity?.occurrenceId ?? group.pendingOccurrenceId ?? group.shotId
    )),
    shotGroupCount: shotGroups.length,
  });
}
