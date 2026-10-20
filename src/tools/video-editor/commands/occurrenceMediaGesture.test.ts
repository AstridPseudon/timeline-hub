import { describe, expect, it, vi } from 'vitest';
import type { EditCommand, MediaSelection } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { captureOccurrenceMediaEdit, submitOccurrenceMediaEdit } from './occurrenceMediaGesture.ts';

const media: MediaSelection = {
  asset: 'asset-new',
  generation_id: 'generation-new',
  variant_id: 'variant-new',
  object_id: `sha256:${'a'.repeat(64)}`,
  catalog_digest: `sha256:${'b'.repeat(64)}`,
};

const request = {
  kind: 'add' as const,
  ownerRef: 'occurrence:occurrence-1' as const,
  trackRef: 'occurrence:occurrence-1/track:video' as const,
  media,
  row: { id: 'child-new', clipType: 'image', track: 'video', at: 0, hold: 1 },
};

const command: EditCommand = {
  schema_version: 1,
  op: 'occurrence.add-media',
  version: '1',
  select: request.ownerRef,
  args: { media, row: request.row },
  intent: { ownership: 'occurrence' },
};

const preview = { version: 1, source: 'occurrence.media', operations: [] } as TimelinePatch;

describe('occurrence media gesture boundary', () => {
  it('submits only the exact command returned for the captured request', async () => {
    const submit = vi.fn();
    const port = {
      capture: vi.fn(() => ({ request })),
      finish: vi.fn(async () => ({ command, preview })),
      submit,
    };

    const captured = captureOccurrenceMediaEdit(port, {} as TimelineData, request);
    await submitOccurrenceMediaEdit(captured);

    expect(submit).toHaveBeenCalledWith({ command, preview });
  });

  it('refuses a command whose args no longer match the captured immutable request', async () => {
    const submit = vi.fn();
    const port = {
      capture: vi.fn(() => ({ request })),
      finish: vi.fn(async () => ({
        command: { ...command, args: { media, row: { ...request.row, at: 2 } } },
        preview,
      })),
      submit,
    };

    await expect(submitOccurrenceMediaEdit(captureOccurrenceMediaEdit(port, {} as TimelineData, request)))
      .rejects.toThrow('Unsupported occurrence media capture result');
    expect(submit).not.toHaveBeenCalled();
  });
});
