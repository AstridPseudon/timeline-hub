/** A test-only Runtime timeline scope. */
export type TimelineScope = Readonly<{
  projectId: string;
  timelineId: string;
}>;

/** Build a Runtime timeline path from the scope chosen by the test. */
export function timelineBase(scope: TimelineScope): string {
  return `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}`;
}
