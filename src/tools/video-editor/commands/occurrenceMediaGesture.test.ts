import { describe, expect, it, vi } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { captureOccurrenceMediaEdit, submitOccurrenceMediaEdit, type OccurrenceMediaCapturePort,
  type OccurrenceMediaRequest } from './occurrenceMediaGesture.ts';
import type { JsonObject } from './types.ts';
import fixture from './fixtures/recipe_m2_occurrence_media.json';

const request: OccurrenceMediaRequest = { kind: 'add', ownerRef: 'occurrence:occ-a', trackRef: 'occurrence:occ-a/track:picture',
  row: fixture.add.commands[0].args.row, media: fixture.add.commands[0].args.media };
const command = (): EditCommand => structuredClone(fixture.add.commands[0]);

function port() {
  const preview = { version: 1, source: 'unit-only', operations: [] };
  return { capture: vi.fn(({ request }: Parameters<OccurrenceMediaCapturePort['capture']>[0]) => ({ request: structuredClone(request) })),
    finish: vi.fn(async (_basis: JsonObject) => ({ command: command(), preview })), submit: vi.fn((_input: Parameters<OccurrenceMediaCapturePort['submit']>[0]) => {}) } satisfies OccurrenceMediaCapturePort;
}

describe('occurrence media gesture boundary (detached unit fixtures)', () => {
  it('keeps caller-reserved identities in an immutable capture and submits only the native result', async () => {
    const native = port(), input = structuredClone(request), current = {} as TimelineData;
    const captured = captureOccurrenceMediaEdit(native, current, input);
    input.media.asset = 'later-popup-choice';
    input.row.id = 'later-reservation';
    await submitOccurrenceMediaEdit(captured);
    expect(native.capture).toHaveBeenCalledWith({ request: input, current });
    expect(captured.basis.request).toEqual(request);
    expect(Object.isFrozen(captured.basis.request)).toBe(true);
    expect(native.finish).toHaveBeenCalledWith(captured.basis);
    expect(native.submit.mock.calls[0][0].command).toEqual(fixture.add.commands[0]);
  });

  it.each(['op', 'select', 'args', 'intent'] as const)('rejects a changed native %s before submission', async (field) => {
    const native = port(), captured = captureOccurrenceMediaEdit(native, {} as TimelineData, request);
    const changed = { ...command(), [field]: field === 'args' ? { row: request.row, media: { ...request.media, asset: 'changed' } }
      : field === 'intent' ? { ownership: 'shared' } : 'unsupported' };
    native.finish.mockResolvedValue({ command: changed as EditCommand, preview: { version: 1, source: 'unit-only', operations: [] } });
    await expect(submitOccurrenceMediaEdit(captured)).rejects.toThrow('Unsupported occurrence media capture');
    expect(native.submit).not.toHaveBeenCalled();
    expect(captured.basis.request).toEqual(request);
  });

  it('leaves the original captured intention available after a read refusal', async () => {
    const native = port(), captured = captureOccurrenceMediaEdit(native, {} as TimelineData, request);
    native.finish.mockRejectedValueOnce(new Error('old media lifecycle changed'));
    await expect(submitOccurrenceMediaEdit(captured)).rejects.toThrow('old media lifecycle changed');
    expect(native.submit).not.toHaveBeenCalled();
    await submitOccurrenceMediaEdit(captured);
    expect(native.finish.mock.calls[0][0]).toBe(native.finish.mock.calls[1][0]);
    expect(native.submit).toHaveBeenCalledTimes(1);
  });
});
