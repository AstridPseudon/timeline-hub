import { describe, expect, it } from 'vitest';
import type { Task as RuntimeTask } from '@/integrations/runtime/generated.ts';
import { runtimeTaskLabel, runtimeTaskModality, runtimeTaskProgress, runtimeTaskStateLabel } from './activityPresentation';

function task(overrides: Partial<RuntimeTask> & { progress?: unknown } = {}): RuntimeTask {
  return {
    task_id: 'task-1',
    run_id: 'run-1',
    project_id: 'project-1',
    state: 'running',
    version: 1,
    capability_id: 'generation.generate_video',
    capability_digest: 'sha256:capability',
    idempotency_key: 'admit:task-1',
    created_at: '2026-10-14T00:00:00Z',
    updated_at: '2026-10-14T00:00:01Z',
    runtime_epoch: 1,
    input_object_ids: [],
    spec: { spec: { family: 'generation.generate_video' } },
    ...overrides,
  };
}

describe('activityPresentation', () => {
  it('uses readable task and state labels', () => {
    expect(runtimeTaskLabel(task())).toBe('Video generation');
    expect(runtimeTaskLabel(task({ spec: { spec: { family: 'media.clip_extract' } } }))).toBe('Clip extraction');
    expect(runtimeTaskStateLabel('cancel_requested')).toBe('Stopping');
  });

  it('maps task families to a safe visual modality with a neutral fallback', () => {
    expect(runtimeTaskModality(task({ spec: { spec: { family: 'generation.generate_image' } } }))).toBe('image');
    expect(runtimeTaskModality(task({ spec: { spec: { family: 'generation.generate_video' } } }))).toBe('video');
    expect(runtimeTaskModality(task({ spec: { spec: { family: 'audio.transcribe' } } }))).toBe('audio');
    expect(runtimeTaskModality(task({ spec: { spec: { family: 'rendering.timeline_visualize' } } }))).toBe('render');
    expect(runtimeTaskModality(task({ spec: { spec: { family: 'vendor.unknown_action' } } }))).toBe('neutral');
  });

  it('only accepts bounded progress values supplied by Runtime', () => {
    expect(runtimeTaskProgress(task({ progress: { phase: 'Extracting', percent: 35.5, current: 2, total: 6 } })))
      .toEqual({ phase: 'Extracting', percent: 35.5, current: 2, total: 6 });
    expect(runtimeTaskProgress(task({ progress: { phase: '   ', percent: 50 } }))).toBeNull();
    expect(runtimeTaskProgress(task({ progress: { phase: 'Working', percent: 101 } }))).toBeNull();
    expect(runtimeTaskProgress(task({ progress: { phase: 'x'.repeat(65), percent: 50 } }))).toBeNull();
    expect(runtimeTaskProgress(task({ progress: { phase: 'Working', percent: 50, current: -1, total: 0 } })))
      .toEqual({ phase: 'Working', percent: 50 });
    expect(runtimeTaskProgress(task())).toBeNull();
  });
});
