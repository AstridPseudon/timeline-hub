// Proposal excerpt only; this file is not imported or activated by App.
// The applyable paired source is in ap2-m2-bootstrap-private-runtime-adapter-proposal.patch.

type NativeBootstrapOptions = {
  name: string;
  createName: string | null;
  createKey: string;
  outboxes?: ReturnType<typeof createCommitOutbox>;
};

/** @internal Keep the native bootstrap consumer behind RuntimeDataProvider. */
async function initializeNativeBootstrapTimeline(
  timelineId: string,
  options: NativeBootstrapOptions,
): Promise<TimelineCommandBasis> {
  const identity = await this.client.getRecoverableIdentity();
  return initializeBootstrapTimeline(
    { ...identity, projectId: this.projectId, timelineId },
    {
      ...options,
      ports: {
        createTimeline: (project, timeline, key, name) => this.client.createTimeline(project, timeline, key, name),
        listTimelineCommits: (project, timeline, cursor, limit) => this.client.listTimelineCommits(project, timeline, cursor, limit),
        getProjectParentCompositionRevision: (project, timeline, revision) =>
          this.client.getProjectParentCompositionRevision(project, timeline, revision),
        loadLatest: (id) => this.loadTimelineCommandBasis(id),
        commitTimeline: (request, key) => this.commitTimeline(request, key),
      },
    },
  );
}
