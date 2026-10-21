/** One current-pin journey for existing-output producer ownership negatives. */
import { expect } from '@playwright/test';
import { test as appTest } from './support/app.ts';
import {
  clipFromRevision,
  currentPinRevision,
  discardFirstAcceptedCommitAcknowledgement,
  observeProducerCommits,
  openCurrentPinTimeline,
  protectedClipState,
  sceneMoveShots,
  seedCurrentPinProducerFixture,
  transcriptRegenerate,
  type CommitObservation,
  type CurrentPinProducerSeed,
} from './support/producer-ownership-current-pin.ts';

const WAIT = { timeout: 20_000 };

const test = appTest.extend<object, { producerSeed: CurrentPinProducerSeed }>({
  producerSeed: [async ({ harness }, use) => {
    await use(await seedCurrentPinProducerFixture(harness));
  }, { scope: 'worker', timeout: 240_000 }],
});

function newAlertText(current: readonly string[], previous: readonly string[]): string[] {
  const remaining = new Map<string, number>();
  for (const text of previous) remaining.set(text, (remaining.get(text) ?? 0) + 1);
  return current.filter((text) => {
    const count = remaining.get(text) ?? 0;
    if (count > 0) {
      remaining.set(text, count - 1);
      return false;
    }
    return true;
  });
}

async function waitForAction(
  page: Parameters<typeof transcriptRegenerate>[0],
  requests: CommitObservation[],
  previousAlerts: readonly string[],
) {
  const deadline = Date.now() + WAIT.timeout;
  for (;;) {
    if (requests.length > 0) return 'submitted' as const;
    const alerts = newAlertText(await page.getByRole('alert').allTextContents(), previousAlerts);
    if (alerts.some((text) => text.includes('Native patch refused'))) return 'refused' as const;
    if (Date.now() > deadline) throw new Error('producer action produced neither a commit nor an atomic refusal');
    await page.waitForTimeout(50);
  }
}

async function waitForHeadChange(harness: Parameters<typeof currentPinRevision>[0], seed: CurrentPinProducerSeed, previous: string) {
  await expect.poll(async () => (await currentPinRevision(harness, seed)).head, WAIT).not.toBe(previous);
}

function assertProtectedPresent(seed: CurrentPinProducerSeed, state: ReturnType<typeof protectedClipState>) {
  for (const protectedId of seed.protectedClipIds) {
    const entry = state.find((candidate) => candidate.clip?.id === protectedId);
    expect(entry?.order, `protected clip ${protectedId} exists`).toBeGreaterThanOrEqual(0);
    expect(entry?.clip?.id, `protected clip ${protectedId} retains its identity`).toBe(protectedId);
  }
}

async function assertProtectedUnchanged(
  harness: Parameters<typeof currentPinRevision>[0],
  seed: CurrentPinProducerSeed,
  before: ReturnType<typeof protectedClipState>,
) {
  const after = await currentPinRevision(harness, seed);
  const state = protectedClipState(after.body, seed);
  assertProtectedPresent(seed, state);
  expect(state, 'foreign and user rows retain every field and their order').toEqual(before);
  return after;
}

function commands(request: CommitObservation): Array<Record<string, any>> {
  return request.body.commands as Array<Record<string, any>>;
}

function markNoAcceptedProof(reason: string) {
  test.info().annotations.push({ type: 'no-accepted-ownership-proof', description: reason });
}

test.describe('producer ownership on the current mounted route', () => {
  test('removes only stale owned transcript output and moves only owned scene output', async ({ page, harness, producerSeed }) => {
    await openCurrentPinTimeline(page, harness, producerSeed);
    await expect(page.locator('[data-lane-kind="astrid.transcript"]')).toBeVisible();
    // The stale source item is valid but outside the carrier's [0, 4] window;
    // only the two protected in-window source items are visible to the lane.
    await expect(page.getByTestId('transcript-lane-chip')).toHaveCount(2);

    const initial = await currentPinRevision(harness, producerSeed);
    const protectedBefore = protectedClipState(initial.body, producerSeed);
    expect(initial.head, 'the route reads the exact dedicated timeline head').toBe(producerSeed.headRevisionId);
    assertProtectedPresent(producerSeed, protectedBefore);
    expect(clipFromRevision(initial.body, producerSeed.transcriptStaleClipId)).toMatchObject({
      app: { managedBy: 'haus.astrid.transcript-lane' },
    });
    expect(clipFromRevision(initial.body, producerSeed.sceneOwnedClipId)).toMatchObject({
      app: { managedBy: 'haus.astrid.scene-phase-markers' },
    });

    const transcriptTraffic = observeProducerCommits(page);
    const transcriptAlerts = await page.getByRole('alert').allTextContents();
    await transcriptRegenerate(page);
    const transcriptOutcome = await waitForAction(page, transcriptTraffic.requests, transcriptAlerts);
    if (transcriptOutcome === 'refused') {
      markNoAcceptedProof('Current transcript stale-remove route was visibly refused; no accepted transcript deletion is claimed.');
      expect(transcriptTraffic.requests).toEqual([]);
      expect((await currentPinRevision(harness, producerSeed)).head).toBe(initial.head);
      await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
      await page.reload();
      await openCurrentPinTimeline(page, harness, producerSeed);
      const retryTraffic = observeProducerCommits(page);
      try {
        const retryAlerts = await page.getByRole('alert').allTextContents();
        await transcriptRegenerate(page);
        expect(await waitForAction(page, retryTraffic.requests, retryAlerts)).toBe('refused');
        expect(retryTraffic.requests).toEqual([]);
      } finally {
        retryTraffic.dispose();
      }
      await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
    } else {
      const transcriptRequest = transcriptTraffic.requests[0]!;
      expect(commands(transcriptRequest)).toEqual([
        expect.objectContaining({
          op: 'clip.delete',
          select: `parent/clip:${producerSeed.transcriptStaleClipId}`,
          args: {},
        }),
      ]);
      await waitForHeadChange(harness, producerSeed, initial.head);
      const afterTranscript = await currentPinRevision(harness, producerSeed);
      expect(clipFromRevision(afterTranscript.body, producerSeed.transcriptStaleClipId)).toBeUndefined();
      expect(protectedClipState(afterTranscript.body, producerSeed)).toEqual(protectedBefore);
      await page.reload();
      await openCurrentPinTimeline(page, harness, producerSeed);
    }
    transcriptTraffic.dispose();

    const beforeScene = await currentPinRevision(harness, producerSeed);
    const sceneTraffic = observeProducerCommits(page);
    const lostAcknowledgement = await discardFirstAcceptedCommitAcknowledgement(page, sceneTraffic.requests);
    try {
      const sceneAlerts = await page.getByRole('alert').allTextContents();
      await sceneMoveShots(page);
      const sceneOutcome = await waitForAction(page, sceneTraffic.requests, sceneAlerts);
      if (sceneOutcome === 'refused') {
        markNoAcceptedProof('Current scene MOVE/HOLD route was visibly refused; no accepted alignment ownership is claimed.');
        await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
        return;
      }

      await lostAcknowledgement.accepted;
      const original = sceneTraffic.requests[0]!;
      expect(commands(original).map((command) => command.op)).toEqual(['clip.move', 'clip.set']);
      expect(commands(original)).toEqual(expect.arrayContaining([
        expect.objectContaining({ op: 'clip.move', select: `parent/clip:${producerSeed.sceneOwnedClipId}`, args: { at: 1 } }),
        expect.objectContaining({ op: 'clip.set', select: `parent/clip:${producerSeed.sceneOwnedClipId}`, args: { values: { hold: 5 }, clear: [] } }),
      ]));

      await page.reload();
      await openCurrentPinTimeline(page, harness, producerSeed);
      await expect.poll(() => sceneTraffic.requests.length, WAIT).toBeGreaterThan(1);
      expect(sceneTraffic.requests[1]?.rawBody).toBe(original.rawBody);
      expect(sceneTraffic.requests[1]?.key).toBe(original.key);
      await waitForHeadChange(harness, producerSeed, beforeScene.head);
    } finally {
      await lostAcknowledgement.dispose();
      sceneTraffic.dispose();
    }

    const afterScene = await currentPinRevision(harness, producerSeed);
    expect(clipFromRevision(afterScene.body, producerSeed.sceneOwnedClipId)).toMatchObject({ at: 1, hold: 5 });
    expect(protectedClipState(afterScene.body, producerSeed)).toEqual(protectedBefore);

    const undoTraffic = observeProducerCommits(page);
    try {
      await page.getByRole('button', { name: 'Undo', exact: true }).click();
      await expect.poll(() => undoTraffic.requests.length, WAIT).toBe(1);
      expect(commands(undoTraffic.requests[0]!)).toEqual([
        expect.objectContaining({ op: 'timeline.inverse' }),
      ]);
      await waitForHeadChange(harness, producerSeed, afterScene.head);
    } finally {
      undoTraffic.dispose();
    }
    const afterUndo = await currentPinRevision(harness, producerSeed);
    expect(clipFromRevision(afterUndo.body, producerSeed.sceneOwnedClipId)).toMatchObject({ at: 30, hold: 2 });
    expect(protectedClipState(afterUndo.body, producerSeed)).toEqual(protectedBefore);
  });
});
