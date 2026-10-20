import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import type { TimelineSnapshot } from '@astrid/editor-sdk';
import { readMarkers, SCENE_PHASE_EXTENSION_ID } from '@/tools/video-editor/dev/scene-phase-markers/extension';
import {
  THREE_PRODUCTS_SCENE_MARKER_EXTENSION_ID,
  THREE_PRODUCTS_SCENE_MARKERS,
} from '../../tests/e2e/local/support/harness.ts';

const journey = vi.hoisted(() => ({
  cases: new Map<string, (fixtures: unknown) => Promise<void>>(),
  opened: new Error('editor opened'),
  openApp: vi.fn(),
}));

vi.mock('../../tests/e2e/local/support/app.ts', async (importOriginal) => {
  const original = await importOriginal<typeof import('../../tests/e2e/local/support/app.ts')>();
  const register = (name: string, run: (fixtures: unknown) => Promise<void>) => {
    journey.cases.set(name, run);
  };
  const test = Object.assign(register, {
    extend: () => register,
    describe: { configure: vi.fn() },
    beforeAll: vi.fn(), beforeEach: vi.fn(), afterEach: vi.fn(), afterAll: vi.fn(),
  });
  return { ...original, test, openApp: journey.openApp };
});

// Register the actual journey without starting its worker-scoped browser/Runtime
// fixtures. Stop at navigation so setup ordering is tested without live sockets.
import '../../tests/e2e/local/three-products.spec.ts';

let supportDir: string;
beforeEach(() => {
  journey.openApp.mockReset().mockRejectedValue(journey.opened);
  supportDir = mkdtempSync(path.join(tmpdir(), 'three-products-authoring-'));
  mkdirSync(path.join(supportDir, 'credentials'));
  writeFileSync(path.join(supportDir, 'credentials/owner.token'), 'unit-owner-token');
  writeFileSync(path.join(supportDir, 'worker.token'), 'unit-worker-token');
});
afterEach(() => rmSync(supportDir, { recursive: true, force: true }));

const selectedCases = [
  'M2 real gate 5',
  'M1 real dependency conflict',
];

function fixtureHarness(enableTimelineAuthoring: ReturnType<typeof vi.fn>) {
  return { origin: 'https://app.test', enableTimelineAuthoring, supportDir,
    discovery: () => ({ worker_credential_file: path.join(supportDir, 'worker.token') }) };
}

it.each(selectedCases)('enables authoring before opening %s in a fresh worker', async (prefix) => {
  const run = [...journey.cases].find(([name]) => name.startsWith(prefix))![1];
  const enableTimelineAuthoring = vi.fn(async () => {});
  const page = { on: vi.fn(), url: () => 'about:blank' };
  const harness = fixtureHarness(enableTimelineAuthoring);
  await expect(run({ page, harness, astrid: {}, seed3: {} })).rejects.toBe(journey.opened);
  expect(enableTimelineAuthoring).toHaveBeenCalledTimes(1);
  expect(journey.openApp).toHaveBeenCalledWith(page, harness);
  expect(enableTimelineAuthoring.mock.invocationCallOrder[0])
    .toBeLessThan(journey.openApp.mock.invocationCallOrder[0]);
});

it('does not open the editor when authoring startup refuses the cohort', async () => {
  const run = [...journey.cases].find(([name]) => name.startsWith('M2 real gate 5'))![1];
  const refused = new Error('authoring provider interface/contract mismatch');
  const enableTimelineAuthoring = vi.fn().mockRejectedValue(refused);
  const page = { on: vi.fn(), url: () => 'about:blank' };
  await expect(run({ page, harness: fixtureHarness(enableTimelineAuthoring),
    astrid: {}, seed3: {} })).rejects.toBe(refused);
  expect(journey.openApp).not.toHaveBeenCalled();
});

it('keeps the ordinary seed markers in the panel reader shape', () => {
  expect(THREE_PRODUCTS_SCENE_MARKER_EXTENSION_ID).toBe(SCENE_PHASE_EXTENSION_ID);
  const snapshot = {
    app: { [THREE_PRODUCTS_SCENE_MARKER_EXTENSION_ID]: { sceneMarkers: [...THREE_PRODUCTS_SCENE_MARKERS] } },
  } as unknown as TimelineSnapshot;
  expect(readMarkers(snapshot, SCENE_PHASE_EXTENSION_ID)).toEqual([
    { id: 'ordinary-marker-a', time: 1 },
    { id: 'ordinary-marker-b', time: 6 },
  ]);
});
