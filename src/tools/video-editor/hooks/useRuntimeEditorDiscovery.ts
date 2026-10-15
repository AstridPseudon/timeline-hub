import { useEffect, useMemo, useState } from "react";
import { assertNativeEditorConnection } from "@/integrations/astrid/nativeEditorConnection.ts";
import { useQuery } from "@tanstack/react-query";
import { z } from "zod";
import { ReighRuntimeClient } from "@/integrations/runtime/client.ts";
import type { Project } from "@/integrations/runtime/generated.ts";
const timelineSchema = z.looseObject({
  timeline_id: z.string().min(1),
  project_id: z.string().optional(),
  name: z.string().optional(),
  slug: z.string().optional(),
  is_default: z.boolean().optional(),
  is_shot: z.boolean().optional(),
  created_at: z.string().optional(),
  updated_at: z.string().optional(),
});
export type RuntimeEditorTimeline = z.infer<typeof timelineSchema>;
export function chooseRuntimeTimeline(
  project: Project,
  timelines: readonly RuntimeEditorTimeline[],
): RuntimeEditorTimeline | undefined {
  const available = timelines.filter((t) => !t.is_shot);
  const defaultId = project.metadata?.default_timeline_id;
  return (
    available.find((t) => t.timeline_id === defaultId) ??
    available.find((t) => t.is_default) ??
    available.find((t) => t.slug === "main") ??
    [...available].sort((a, b) => a.timeline_id.localeCompare(b.timeline_id))[0]
  );
}
/**
 * Discovery gates the selectors and the timeline auto-pick, not the editor
 * itself, so a failure must recover on its own. A bounded retry with
 * exponential backoff covers a transient blip; the slow poll below picks up a
 * Runtime that comes back later without the user pressing Retry.
 */
export const RUNTIME_DISCOVERY_RETRY_COUNT = 3;
export const RUNTIME_DISCOVERY_RETRY_DELAY_CAP_MS = 8_000;
export const RUNTIME_DISCOVERY_RECOVERY_POLL_MS = 15_000;
const runtimeDiscoveryRetryDelay = (attempt: number) =>
  Math.min(500 * 2 ** attempt, RUNTIME_DISCOVERY_RETRY_DELAY_CAP_MS);
const runtimeDiscoveryRecoveryPoll = (query: { state: { status: string } }) =>
  query.state.status === "error" ? RUNTIME_DISCOVERY_RECOVERY_POLL_MS : false;

/** Native discovery uses exactly the editor's authenticated Runtime connector. */
export function useRuntimeEditorDiscovery({
  enabled,
  projectId,
  open,
}: {
  enabled: boolean;
  projectId: string | null;
  open: boolean;
}) {
  const client = useMemo(() => new ReighRuntimeClient(), []);
  const [session] = useState(() => crypto.randomUUID());
  const projectsQuery = useQuery({
    queryKey: ["runtime-editor", session, "projects"],
    enabled,
    queryFn: async () => {
      await assertNativeEditorConnection();
      const rows = await client.listProjects();
      if (
        rows.some((p) => !p.project_id || !p.slug || typeof p.name !== "string")
      )
        throw new Error("Runtime returned malformed project metadata.");
      return rows.filter((p) => !p.archived);
    },
    retry: RUNTIME_DISCOVERY_RETRY_COUNT,
    retryDelay: runtimeDiscoveryRetryDelay,
    refetchInterval: runtimeDiscoveryRecoveryPoll,
    staleTime: 0,
  });
  const project =
    projectsQuery.data?.find((p) => p.project_id === projectId) ?? null;
  const timelinesQuery = useQuery({
    queryKey: ["runtime-editor", session, projectId, "timelines"],
    enabled: enabled && !!project,
    queryFn: async () => {
      const rows = z
        .array(timelineSchema)
        .parse(await client.listTimelines(projectId!));
      if (rows.some((t) => t.project_id && t.project_id !== projectId))
        throw new Error(
          "Runtime returned a timeline belonging to a different project.",
        );
      return rows;
    },
    retry: RUNTIME_DISCOVERY_RETRY_COUNT,
    retryDelay: runtimeDiscoveryRetryDelay,
    refetchInterval: runtimeDiscoveryRecoveryPoll,
    staleTime: 0,
  });
  const { refetch: refreshProjects } = projectsQuery,
    { refetch: refreshTimelines } = timelinesQuery;
  useEffect(() => {
    if (!enabled || !open) return;
    void refreshProjects();
    if (projectId && project) void refreshTimelines();
  }, [enabled, open, projectId, project, refreshProjects, refreshTimelines]);
  const reconnect = async () => {
    await client.reconnect();
    await refreshProjects();
    if (project) await refreshTimelines();
  };
  return { projectsQuery, timelinesQuery, project, client, reconnect };
}
