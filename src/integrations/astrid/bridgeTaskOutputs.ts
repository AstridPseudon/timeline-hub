import { AstridLocalClient } from './client.ts';
import { AstridRuntimeClient } from '@/integrations/runtime/client';
import { bridgeMediaUrl } from '@/shared/lib/media/bridgeMediaUrl';
import type { Task } from '@/types/tasks';

export interface BridgeTaskOutputRecord extends Record<string, unknown> {
  id: string;
  location: string;
  thumbnail_url: string;
  type: string;
  created_at: string;
  project_id: string;
  task_id: string;
  params: Record<string, unknown>;
  _variant_id: string;
  _variant_is_primary: boolean;
}

/**
 * Resolve existing managed outputs, retaining the older result.outputs read
 * for migration. The output row supplies the task/media association.
 */
export async function readBridgeTaskOutputs(task: Task): Promise<BridgeTaskOutputRecord[]> {
  const client = new AstridRuntimeClient();
  const managed: BridgeTaskOutputRecord[] = [];
  let hasManagedRows = false;
  let cursor: string | undefined;
  const seenCursors = new Set<string>();
  while (true) {
    const page = await client.listManagedOutputs(task.id, cursor, 50);
    hasManagedRows ||= page.items.length > 0;
    for (const output of page.items) {
      if (output.task_id !== task.id || output.project_id !== task.projectId
        || output.state !== 'available' || !output.object_id.startsWith('sha256:')) continue;
      const location = bridgeMediaUrl(task.projectId, output.object_id);
      managed.push({
        id: output.association_id,
        location,
        thumbnail_url: location,
        type: output.media_type.startsWith('image/') ? 'image'
          : output.media_type.startsWith('video/') ? 'video' : output.media_type,
        created_at: task.updatedAt ?? task.createdAt,
        project_id: task.projectId,
        task_id: task.id,
        params: {},
        _variant_id: output.object_id,
        _variant_is_primary: output.ordinal === 0,
      });
    }
    if (page.next_cursor === null) break;
    if (seenCursors.has(page.next_cursor)) {
      throw new Error('Workspace Runtime managed-output pagination repeated a cursor');
    }
    seenCursors.add(page.next_cursor);
    cursor = page.next_cursor;
  }
  if (hasManagedRows) return managed;

  // Preserve the older result.outputs migration read when no managed row exists.
  const detail = await new AstridLocalClient({ projectSlug: task.projectId }).tasks.get(task.id);
  return (detail.outputs ?? []).map((output) => {
    const params = typeof output.params_json === 'string'
      ? parseParams(output.params_json)
      : (output.params_json ?? {});
    const location = bridgeMediaUrl(task.projectId, output.media_id);
    return {
      id: `${task.id}:${output.ordinal}`,
      location,
      thumbnail_url: location,
      type: output.role.includes('video') ? 'video' : output.role.includes('image') ? 'image' : output.role,
      created_at: task.updatedAt ?? task.createdAt,
      project_id: task.projectId,
      task_id: task.id,
      params,
      _variant_id: output.media_id,
      _variant_is_primary: output.is_primary ?? output.ordinal === 0,
    };
  });
}

function parseParams(value: string): Record<string, unknown> {
  try {
    const parsed: unknown = JSON.parse(value);
    return typeof parsed === 'object' && parsed !== null && !Array.isArray(parsed)
      ? parsed as Record<string, unknown>
      : {};
  } catch {
    return {};
  }
}
