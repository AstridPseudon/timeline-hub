import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { ensureProjectHasTimeline } from '@/integrations/runtime/createDefaultTimeline.ts';
import type { Project } from '@/integrations/runtime/generated.ts';
import { chooseRuntimeTimeline, type RuntimeEditorTimeline } from '@/tools/video-editor/hooks/useRuntimeEditorDiscovery.ts';

export interface StarterProjectSelection {
  projectId: string;
  timelineId: string | null;
}

export const STARTER_PROJECT_INTENT_METADATA = 'astrid_onboarding_intent';

function existingProject(projects: Project[], preferredId?: string | null): Project | undefined {
  return projects.find(project => project.project_id === preferredId || project.slug === preferredId)
    ?? [...projects].sort((left, right) => {
      const leftTime = Date.parse(left.created_at) || 0;
      const rightTime = Date.parse(right.created_at) || 0;
      return rightTime - leftTime || left.slug.localeCompare(right.slug);
    })[0];
}

async function readTimelines(client: AstridRuntimeClient, projectId: string): Promise<RuntimeEditorTimeline[]> {
  const rows = await client.listTimelines(projectId);
  if (rows.some(row => typeof row.timeline_id !== 'string' || !row.timeline_id
    || (row.project_id !== undefined && row.project_id !== projectId))) {
    throw new Error('Runtime returned invalid timelines. Retry to refresh the workspace.');
  }
  return rows.filter(row => row.archived !== true).map(row => ({
    ...row,
    timeline_id: row.timeline_id as string,
    is_shot: row.is_shot === true || (typeof row.slug === 'string' && row.slug.startsWith('shot-')),
  }));
}

/** Only called after connecting. The Runtime remains the authority, including after an unknown
 * create response: discover the same intent's project before attempting another mutation. */
export async function prepareStarterProject({
  intentId,
  preferredProjectId,
  client = new AstridRuntimeClient(),
}: {
  intentId: string;
  preferredProjectId?: string | null;
  client?: AstridRuntimeClient;
}): Promise<StarterProjectSelection> {
  if (!/^[a-zA-Z0-9-]{1,80}$/.test(intentId)) throw new Error('Invalid project setup request.');
  // Never convert discovery failure into an empty workspace.
  const discovered = await client.listProjects();
  if (discovered.some(project => !project.project_id || !project.slug || typeof project.name !== 'string')) {
    throw new Error('Runtime returned invalid projects. Retry to refresh the workspace.');
  }
  const projects = discovered.filter(project => !project.archived);
  let project = projects.find(item => item.metadata?.[STARTER_PROJECT_INTENT_METADATA] === intentId);
  if (!project && projects.length) {
    const selected = existingProject(projects, preferredProjectId)!;
    const timelines = await readTimelines(client, selected.project_id);
    // Existing work is read-only here, including an existing project with no timeline yet.
    return { projectId: selected.project_id, timelineId: chooseRuntimeTimeline(selected, timelines)?.timeline_id ?? null };
  }
  if (!project) {
    if (discovered.some(item => item.metadata?.[STARTER_PROJECT_INTENT_METADATA] === intentId)) {
      throw new Error('This starter project was archived. Open an existing project from the editor.');
    }
    project = await client.createProject('My first project', `astrid-onboarding-project-${intentId}`,
      `my-first-project-${intentId.slice(0, 8)}`, {
        aspect_ratio: '16:9',
        [STARTER_PROJECT_INTENT_METADATA]: intentId,
      });
  }
  const timelineId = await ensureProjectHasTimeline(project.project_id, client);
  const timelines = await readTimelines(client, project.project_id);
  if (!timelines.some(timeline => timeline.timeline_id === timelineId && timeline.head_revision_id)) {
    throw new Error('Your project was created, but its timeline is not ready yet. Retry to finish setup.');
  }
  return { projectId: project.project_id, timelineId };
}
