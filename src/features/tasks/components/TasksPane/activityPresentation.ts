import { asRecord } from '@/shared/lib/typeCoercion';
import type { Task as RuntimeTask } from '@/integrations/runtime/generated.ts';

export interface RuntimeTaskProgress {
  phase: string;
  percent: number;
  current?: number;
  total?: number;
}

const TASK_LABELS: Record<string, string> = {
  'generation.generate_image': 'Image generation',
  'generation.generate_video': 'Video generation',
  'rendering.timeline_visualize': 'Timeline render',
  'rendering.render': 'Timeline render',
  'media.clip_extract': 'Clip extraction',
};

export function runtimeTaskLabel(task: RuntimeTask): string {
  const spec = asRecord(task.spec);
  const nested = asRecord(spec?.spec) ?? spec;
  const family = nested?.family;
  const key = typeof family === 'string' && family.trim() ? family.trim() : task.capability_id;
  if (TASK_LABELS[key]) return TASK_LABELS[key];
  return key
    .split(/[._-]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ') || 'Runtime task';
}

export function runtimeTaskProgress(task: RuntimeTask): RuntimeTaskProgress | null {
  const progress = asRecord((task as RuntimeTask & { progress?: unknown }).progress);
  if (!progress) return null;
  const phase = typeof progress.phase === 'string' ? progress.phase.trim() : '';
  const percent = progress.percent;
  if (!phase || phase.length > 64 || typeof percent !== 'number' || !Number.isFinite(percent) || percent < 0 || percent > 100) {
    return null;
  }
  const current = progress.current;
  const total = progress.total;
  const hasCurrent = typeof current === 'number' && Number.isFinite(current) && current >= 0;
  const hasTotal = typeof total === 'number' && Number.isFinite(total) && total > 0;
  return {
    phase,
    percent,
    ...(hasCurrent && hasTotal ? { current, total } : {}),
  };
}

export function runtimeTaskStateLabel(state: RuntimeTask['state']): string {
  const labels: Record<string, string> = {
    queued: 'Queued',
    ready: 'Ready',
    running: 'Running',
    cancel_requested: 'Stopping',
    retrying: 'Retrying',
    succeeded: 'Complete',
    failed: 'Failed',
    cancelled: 'Cancelled',
  };
  return labels[state] ?? 'Active';
}

