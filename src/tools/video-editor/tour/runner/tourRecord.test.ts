import { beforeEach, describe, expect, it, vi } from 'vitest';
import { EDITOR_TOUR_VERSION } from '@/shared/lib/editorTourVersion';
import {
  buildEditorTourRecord,
  EDITOR_TOUR_STATE_KEY,
  readRuntimeTourStatus,
  recordEditorTour,
  shouldAutoStartEditorTour,
} from './tourRecord';

const client = vi.hoisted(() => ({
  getUserAppState: vi.fn(),
  updateUserAppState: vi.fn(),
}));

vi.mock('@/integrations/runtime/client', () => ({
  AstridRuntimeClient: class {
    getUserAppState = client.getUserAppState;
    updateUserAppState = client.updateUserAppState;
  },
}));

const conflict = Object.assign(new Error('app-state version conflict'), { status: 409 });
const absent = { version: 0, content: null };
const record = buildEditorTourRecord('completed', 3, 'feedback', new Date('2026-10-21T10:00:00Z'));

beforeEach(() => {
  client.getUserAppState.mockReset().mockResolvedValue(absent);
  client.updateUserAppState.mockReset().mockResolvedValue({});
});

describe('shouldAutoStartEditorTour', () => {
  it.each([
    [false, 'unseen', true],
    [false, 'unavailable', true],
    [false, 'seen', false],
    [true, 'unseen', false],
    [true, 'unavailable', false],
    [true, 'seen', false],
  ] as const)('local seen %s, Runtime %s: %s', (localSeen, runtime, expected) => {
    expect(shouldAutoStartEditorTour({ localSeen, runtime })).toBe(expected);
  });
});

describe('buildEditorTourRecord', () => {
  it('carries the tour version, outcome, act/beat and an ISO time', () => {
    expect(record).toEqual({ version: EDITOR_TOUR_VERSION, outcome: 'completed', step: 'act3/feedback', at: '2026-10-21T10:00:00.000Z' });
  });
});

describe('readRuntimeTourStatus', () => {
  it('is unseen when the Runtime has no record', async () => {
    await expect(readRuntimeTourStatus()).resolves.toBe('unseen');
    expect(client.getUserAppState).toHaveBeenCalledWith(EDITOR_TOUR_STATE_KEY);
  });

  it.each(['started', 'completed', 'skipped'] as const)('is seen once a "%s" record exists for this tour version', async (outcome) => {
    client.getUserAppState.mockResolvedValue({ version: 2, content: { version: EDITOR_TOUR_VERSION, outcome, step: 'act1/welcome', at: 't' } });
    await expect(readRuntimeTourStatus()).resolves.toBe('seen');
  });

  it.each(['act3/finale', 'act3/feedback'])('is seen for a completed record ending at %s: old records still parse', async (step) => {
    client.getUserAppState.mockResolvedValue({ version: 2, content: { version: EDITOR_TOUR_VERSION, outcome: 'completed', step, at: 't' } });
    await expect(readRuntimeTourStatus()).resolves.toBe('seen');
  });

  it('is unseen when the record is for an older tour version, so a reworked tour shows again', async () => {
    client.getUserAppState.mockResolvedValue({ version: 2, content: { version: EDITOR_TOUR_VERSION - 1, outcome: 'completed', step: 'x', at: 't' } });
    await expect(readRuntimeTourStatus()).resolves.toBe('unseen');
  });

  it('is unseen for a malformed record', async () => {
    client.getUserAppState.mockResolvedValue({ version: 1, content: { outcome: 'completed' } });
    await expect(readRuntimeTourStatus()).resolves.toBe('unseen');
  });

  it('is unavailable when the route is missing (older Runtime) or the read fails', async () => {
    client.getUserAppState.mockRejectedValueOnce(Object.assign(new Error('not found'), { status: 404 }));
    await expect(readRuntimeTourStatus()).resolves.toBe('unavailable');
    client.getUserAppState.mockRejectedValueOnce(new TypeError('Failed to fetch'));
    await expect(readRuntimeTourStatus()).resolves.toBe('unavailable');
  });
});

describe('recordEditorTour', () => {
  it('creates the record at version 0', async () => {
    await recordEditorTour(record);
    expect(client.updateUserAppState).toHaveBeenCalledWith(EDITOR_TOUR_STATE_KEY, record, 0);
  });

  it('updates against the current version', async () => {
    client.getUserAppState.mockResolvedValue({ version: 4, content: {} });
    await recordEditorTour(record);
    expect(client.updateUserAppState).toHaveBeenCalledWith(EDITOR_TOUR_STATE_KEY, record, 4);
  });

  it('reads again and retries once after a version conflict', async () => {
    client.getUserAppState.mockResolvedValueOnce({ version: 1, content: {} }).mockResolvedValueOnce({ version: 2, content: {} });
    client.updateUserAppState.mockRejectedValueOnce(conflict);
    await recordEditorTour(record);
    expect(client.updateUserAppState).toHaveBeenNthCalledWith(2, EDITOR_TOUR_STATE_KEY, record, 2);
  });

  it('swallows every failure: a missing route, a conflict that persists and an unreachable Runtime', async () => {
    client.getUserAppState.mockRejectedValueOnce(Object.assign(new Error('not found'), { status: 404 }));
    await expect(recordEditorTour(record)).resolves.toBeUndefined();
    client.updateUserAppState.mockRejectedValue(conflict);
    await expect(recordEditorTour(record)).resolves.toBeUndefined();
    client.getUserAppState.mockRejectedValue(new TypeError('Failed to fetch'));
    await expect(recordEditorTour(record)).resolves.toBeUndefined();
  });

  it('writes in order, so "started" lands before the outcome', async () => {
    const order: string[] = [];
    client.updateUserAppState.mockImplementation(async (_key: string, content: { outcome: string }) => {
      await new Promise((resolve) => setTimeout(resolve, content.outcome === 'started' ? 20 : 0));
      order.push(content.outcome);
    });
    void recordEditorTour(buildEditorTourRecord('started', 1, 'welcome'));
    await recordEditorTour(buildEditorTourRecord('skipped', 1, 'welcome'));
    expect(order).toEqual(['started', 'skipped']);
  });
});
