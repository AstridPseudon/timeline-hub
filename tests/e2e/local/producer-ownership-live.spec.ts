/** One bounded real-route proof for producer ownership and protected-clip preservation. */
import { expect } from '@playwright/test';
import {
  test as appTest,
} from './support/app.ts';
import {
  clipFromRevision,
  discardFirstAcceptedCommitAcknowledgement,
  observeProducerCommits,
  openProducerOwnershipTimeline,
  producerOwnershipRevision,
  protectedClipState,
  sceneCreateShots,
  sceneMoveShots,
  seedProducerOwnershipFixture,
  submittedTargets,
  transcriptRegenerate,
  type ProducerOwnershipSeed,
} from './support/producer-ownership.ts';

const WAIT = { timeout: 20_000 };

const test = appTest.extend<object, { producerSeed: ProducerOwnershipSeed }>({
  producerSeed: [async ({ harness }, use) => {
    await use(await seedProducerOwnershipFixture(harness));
  }, { scope: 'worker', timeout: 240_000 }],
});

async function assertProtectedUnchanged(
  harness: Parameters<typeof producerOwnershipRevision>[0],
  seed: ProducerOwnershipSeed,
  before: ReturnType<typeof protectedClipState>,
) {
  const after = await producerOwnershipRevision(harness, seed);
  const afterState = protectedClipState(after.body, seed);
  assertProtectedPresent(seed, afterState);
  expect(afterState, 'foreign and user clips retain every authored field and order').toEqual(before);
  return after;
}

function assertProtectedPresent(seed: ProducerOwnershipSeed, state: ReturnType<typeof protectedClipState>) {
  for (const protectedId of seed.protectedClipIds) {
    const entry = state.find((candidate) => candidate.clip?.id === protectedId);
    expect(entry?.order, `seeded protected clip ${protectedId} exists before deep comparison`).toBeGreaterThanOrEqual(0);
    expect(entry?.clip?.id, `seeded protected clip ${protectedId} has the expected identity`).toBe(protectedId);
  }
}

function assertNoProtectedTargets(seed: ProducerOwnershipSeed, requests: ReturnType<typeof observeProducerCommits>['requests']) {
  const targets = requests.flatMap((request) => submittedTargets(request.body));
  for (const protectedId of seed.protectedClipIds) {
    expect(targets, `no submitted operation targets protected clip ${protectedId}`).not.toEqual(
      expect.arrayContaining([expect.stringContaining(protectedId)]),
    );
  }
}

function assertFreshSceneTargets(seed: ProducerOwnershipSeed, requests: ReturnType<typeof observeProducerCommits>['requests']) {
  const targets = requests.flatMap((request) => submittedTargets(request.body));
  for (const freshId of seed.sceneFreshClipIds) {
    expect(targets.some((target) => target.includes(freshId)), `scene producer targets fresh owned clip ${freshId}`).toBe(true);
  }
  assertNoProtectedTargets(seed, requests);
}

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
  requests: ReturnType<typeof observeProducerCommits>['requests'],
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

async function waitForHeadChange(harness: Parameters<typeof producerOwnershipRevision>[0], seed: ProducerOwnershipSeed, previous: string) {
  await expect.poll(async () => (await producerOwnershipRevision(harness, seed)).head, WAIT).not.toBe(previous);
}

function markNoAcceptedOwnershipProof(reason: string) {
  test.info().annotations.push({
    type: 'no-accepted-ownership-proof',
    description: reason,
  });
}

test.describe('producer ownership on the mounted editor route', () => {
  test('accepts and reloads fresh ownership when supported, otherwise preserves the visible atomic refusal', async ({ page, harness, producerSeed }) => {
    const traffic = observeProducerCommits(page);
    try {
      await openProducerOwnershipTimeline(page, harness, producerSeed);
      const initial = await producerOwnershipRevision(harness, producerSeed);
      const protectedBefore = protectedClipState(initial.body, producerSeed);
      expect(initial.head, 'dedicated producer timeline is read by its exact seeded timeline ID').toBe(producerSeed.headRevisionId);
      assertProtectedPresent(producerSeed, protectedBefore);

      const transcriptAlerts = await page.getByRole('alert').allTextContents();
      await transcriptRegenerate(page);
      const transcriptOutcome = await waitForAction(page, traffic.requests, transcriptAlerts);
      assertNoProtectedTargets(producerSeed, traffic.requests);

      if (transcriptOutcome === 'refused') {
        markNoAcceptedOwnershipProof('Transcript producer was visibly refused; no accepted fresh ownership is claimed.');
        await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
        await page.reload();
        await openProducerOwnershipTimeline(page, harness, producerSeed);
        const retryTraffic = observeProducerCommits(page);
        try {
          const retryAlerts = await page.getByRole('alert').allTextContents();
          await transcriptRegenerate(page);
          expect(await waitForAction(page, retryTraffic.requests, retryAlerts)).toBe('refused');
          assertNoProtectedTargets(producerSeed, retryTraffic.requests);
        } finally {
          retryTraffic.dispose();
        }
        await assertProtectedUnchanged(harness, producerSeed, protectedBefore);

        const sceneTraffic = observeProducerCommits(page);
        try {
          const sceneAlerts = await page.getByRole('alert').allTextContents();
          await sceneCreateShots(page);
          expect(await waitForAction(page, sceneTraffic.requests, sceneAlerts)).toBe('refused');
          assertNoProtectedTargets(producerSeed, sceneTraffic.requests);
        } finally {
          sceneTraffic.dispose();
        }
        await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
        return;
      }

      await waitForHeadChange(harness, producerSeed, initial.head);
      const transcriptAccepted = await producerOwnershipRevision(harness, producerSeed);
      expect(clipFromRevision(transcriptAccepted.body, producerSeed.transcriptMissingClipId)).toMatchObject({
        app: { managedBy: 'haus.astrid.transcript-lane' },
      });
      await page.reload();
      await openProducerOwnershipTimeline(page, harness, producerSeed);
      expect(protectedClipState((await producerOwnershipRevision(harness, producerSeed)).body, producerSeed)).toEqual(protectedBefore);

      const retryTraffic = observeProducerCommits(page);
      const lostAcknowledgement = await discardFirstAcceptedCommitAcknowledgement(page, retryTraffic.requests);
      try {
        const beforeScene = await producerOwnershipRevision(harness, producerSeed);
        const sceneAlerts = await page.getByRole('alert').allTextContents();
        await sceneCreateShots(page);
        const sceneOutcome = await waitForAction(page, retryTraffic.requests, sceneAlerts);
        if (sceneOutcome === 'refused') {
          markNoAcceptedOwnershipProof('Scene producer was visibly refused; no complete accepted ownership proof is claimed.');
          await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
          return;
        }
        await lostAcknowledgement.accepted;
        const originalRetry = retryTraffic.requests[0];
        expect(originalRetry?.rawBody).toBeTruthy();
        expect(originalRetry?.key).toBeTruthy();
        await page.reload();
        await openProducerOwnershipTimeline(page, harness, producerSeed);
        await expect.poll(() => retryTraffic.requests.length, WAIT).toBeGreaterThan(1);
        expect(retryTraffic.requests[1]?.rawBody).toBe(originalRetry?.rawBody);
        expect(retryTraffic.requests[1]?.key).toBe(originalRetry?.key);
        await waitForHeadChange(harness, producerSeed, beforeScene.head);
      } finally {
        await lostAcknowledgement.dispose();
        retryTraffic.dispose();
      }
      const afterScene = await producerOwnershipRevision(harness, producerSeed);
      assertFreshSceneTargets(producerSeed, retryTraffic.requests);
      for (const clipId of producerSeed.sceneFreshClipIds) {
        expect(clipFromRevision(afterScene.body, clipId)).toMatchObject({ app: { managedBy: 'haus.astrid.scene-phase-markers' } });
      }
      expect(protectedClipState(afterScene.body, producerSeed)).toEqual(protectedBefore);

      const secondTranscriptHead = afterScene.head;
      const secondTranscriptTraffic = observeProducerCommits(page);
      try {
        const secondTranscriptAlerts = await page.getByRole('alert').allTextContents();
        await transcriptRegenerate(page);
        expect(await waitForAction(page, secondTranscriptTraffic.requests, secondTranscriptAlerts)).toBe('submitted');
        assertNoProtectedTargets(producerSeed, secondTranscriptTraffic.requests);
      } finally {
        secondTranscriptTraffic.dispose();
      }
      await waitForHeadChange(harness, producerSeed, secondTranscriptHead);
      expect(protectedClipState((await producerOwnershipRevision(harness, producerSeed)).body, producerSeed)).toEqual(protectedBefore);

      const sceneMoveTraffic = observeProducerCommits(page);
      try {
        const sceneMoveAlerts = await page.getByRole('alert').allTextContents();
        await sceneMoveShots(page);
        const sceneMoveOutcome = await waitForAction(page, sceneMoveTraffic.requests, sceneMoveAlerts);
        if (sceneMoveOutcome === 'refused') {
          markNoAcceptedOwnershipProof('Scene alignment was visibly refused; no accepted alignment ownership proof is claimed.');
          await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
          return;
        }
        assertFreshSceneTargets(producerSeed, sceneMoveTraffic.requests);
      } finally {
        sceneMoveTraffic.dispose();
      }
      await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
    } finally {
      traffic.dispose();
    }
  });
});
