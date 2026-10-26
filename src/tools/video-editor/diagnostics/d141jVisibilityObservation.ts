export type D141jVisibilityEvent = Readonly<{
  kind: 'accepted-canonical-read';
  projectId: string;
  parentDocumentId: string;
  acceptedReadHeadRevisionId: string;
  previousAcceptedReadHeadRevisionId: string | null;
  occurrenceIds: readonly string[];
}> | Readonly<{
  kind: 'active-occurrences-before-useShotGroups';
  projectId: string;
  parentDocumentId: string;
  acceptedReadHeadRevisionId: string;
  occurrenceIds: readonly string[];
}> | Readonly<{
  kind: 'useShotGroups-input-and-result';
  inputOccurrenceIds: readonly string[];
  resultOccurrenceIds: readonly string[];
  resultGroupKeys: readonly string[];
  resultGroupCount: number;
}> | Readonly<{
  kind: 'before-shot-group-overlay';
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
  snapshot: () => D141jVisibilityArtifact;
}>;

let activeCollector: D141jVisibilityCollector | null = null;

export function createD141jVisibilityCollector(expectedOccurrenceId: string): D141jVisibilityCollector {
  const events: D141jVisibilityEvent[] = [];
  return {
    record(event) {
      events.push(event);
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
}: {
  projectId: string;
  parentDocumentId: string;
  acceptedReadHeadRevisionId: string;
  previousAcceptedReadHeadRevisionId: string | null;
  occurrenceIds: readonly string[];
}): void {
  if (!activeCollector) return;
  activeCollector?.record({
    kind: 'accepted-canonical-read',
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
  const occurrenceIds = canonicalOccurrences.map((occurrence) => occurrence.occurrenceId);
  activeCollector.record({
    kind: 'active-occurrences-before-useShotGroups',
    projectId: acceptedRead.projectId,
    parentDocumentId: acceptedRead.parentDocumentId,
    acceptedReadHeadRevisionId: getAcceptedReadHeadRevisionId(),
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
  activeCollector.record({
    kind: 'useShotGroups-input-and-result',
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
  activeCollector.record({
    kind: 'before-shot-group-overlay',
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

function getAcceptedReadHeadRevisionId(): string {
  // The collector records the accepted head on its first event. This keeps the
  // hook seam read-only without threading diagnostic state through product APIs.
  const snapshot = activeCollector?.snapshot();
  const acceptedRead = snapshot?.events.find((event) => event.kind === 'accepted-canonical-read');
  return acceptedRead?.kind === 'accepted-canonical-read'
    ? acceptedRead.acceptedReadHeadRevisionId
    : '';
}
