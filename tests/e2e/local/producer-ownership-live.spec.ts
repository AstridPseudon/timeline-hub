/** One bounded real-route proof for producer ownership and protected-clip preservation. */
import { expect } from '@playwright/test';
import {
  holdCommandRequests,
  test as appTest,
} from './support/app.ts';
import {
  clipFromRevision,
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
  expect(protectedClipState(after.body, seed), 'foreign and user clips retain every authored field and order').toEqual(before);
  return after;
}

function assertNoProtectedTargets(seed: ProducerOwnershipSeed, requests: ReturnType<typeof observeProducerCommits>['requests']) {
  const targets = requests.flatMap((request) => submittedTargets(request.body));
  for (const protectedId of seed.protectedClipIds) {
    expect(targets, `no submitted operation targets protected clip ${protectedId}`).not.toEqual(
      expect.arrayContaining([expect.stringContaining(protectedId)]),
    );
  }
}

async function waitForAction(page: Parameters<typeof transcriptRegenerate>[0], requests: ReturnType<typeof observeProducerCommits>['requests']) {
  const deadline = Date.now() + WAIT.timeout;
  for (;;) {
    if (requests.length > 0) return 'submitted' as const;
    const alerts = await page.getByRole('alert').allTextContents();
    if (alerts.some((text) => text.includes('Native patch refused'))) return 'refused' as const;
    if (Date.now() > deadline) throw new Error('producer action produced neither a commit nor an atomic refusal');
    await page.waitForTimeout(50);
  }
}

async function waitForHeadChange(harness: Parameters<typeof producerOwnershipRevision>[0], seed: ProducerOwnershipSeed, previous: string) {
  await expect.poll(async () => (await producerOwnershipRevision(harness, seed)).head, WAIT).not.toBe(previous);
}

test.describe('producer ownership on the mounted editor route', () => {
  test('accepts and reloads fresh ownership when supported, otherwise preserves the visible atomic refusal', async ({ page, harness, producerSeed }) => {
    const traffic = observeProducerCommits(page);
    try {
      await openProducerOwnershipTimeline(page, harness, producerSeed);
      const initial = await producerOwnershipRevision(harness, producerSeed);
      const protectedBefore = protectedClipState(initial.body, producerSeed);

      await transcriptRegenerate(page);
      const transcriptOutcome = await waitForAction(page, traffic.requests);
      assertNoProtectedTargets(producerSeed, traffic.requests);

      if (transcriptOutcome === 'refused') {
        await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
        await page.reload();
        await openProducerOwnershipTimeline(page, harness, producerSeed);
        const retryTraffic = observeProducerCommits(page);
        try {
          await transcriptRegenerate(page);
          expect(await waitForAction(page, retryTraffic.requests)).toBe('refused');
          assertNoProtectedTargets(producerSeed, retryTraffic.requests);
        } finally {
          retryTraffic.dispose();
        }
        await assertProtectedUnchanged(harness, producerSeed, protectedBefore);

        const sceneTraffic = observeProducerCommits(page);
        try {
          await sceneCreateShots(page);
          expect(await waitForAction(page, sceneTraffic.requests)).toBe('refused');
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

      const held = await holdCommandRequests(page);
      const retryTraffic = observeProducerCommits(page);
      try {
        const beforeScene = await producerOwnershipRevision(harness, producerSeed);
        await sceneCreateShots(page);
        const sceneOutcome = await waitForAction(page, retryTraffic.requests);
        if (sceneOutcome === 'refused') {
          await held.release(false);
          await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
          return;
        }
        const firstRetryBody = held.requests[0]?.postData();
        expect(firstRetryBody).toBeTruthy();
        await held.release(false);
        await page.reload();
        await openProducerOwnershipTimeline(page, harness, producerSeed);
        await expect.poll(() => retryTraffic.requests.length, WAIT).toBeGreaterThan(1);
        expect(retryTraffic.requests[1]?.rawBody).toBe(firstRetryBody);
        await waitForHeadChange(harness, producerSeed, beforeScene.head);
      } finally {
        retryTraffic.dispose();
      }
      const afterScene = await producerOwnershipRevision(harness, producerSeed);
      for (const clipId of producerSeed.sceneFreshClipIds) {
        expect(clipFromRevision(afterScene.body, clipId)).toMatchObject({ app: { managedBy: 'haus.astrid.scene-phase-markers' } });
      }
      expect(protectedClipState(afterScene.body, producerSeed)).toEqual(protectedBefore);

      const secondTranscriptHead = afterScene.head;
      const secondTranscriptTraffic = observeProducerCommits(page);
      try {
        await transcriptRegenerate(page);
        expect(await waitForAction(page, secondTranscriptTraffic.requests)).toBe('submitted');
        assertNoProtectedTargets(producerSeed, secondTranscriptTraffic.requests);
      } finally {
        secondTranscriptTraffic.dispose();
      }
      await waitForHeadChange(harness, producerSeed, secondTranscriptHead);
      expect(protectedClipState((await producerOwnershipRevision(harness, producerSeed)).body, producerSeed)).toEqual(protectedBefore);

      const sceneMoveTraffic = observeProducerCommits(page);
      try {
        await sceneMoveShots(page);
        const sceneMoveOutcome = await waitForAction(page, sceneMoveTraffic.requests);
        assertNoProtectedTargets(producerSeed, sceneMoveTraffic.requests);
        if (sceneMoveOutcome === 'refused') {
          await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
          return;
        }
      } finally {
        sceneMoveTraffic.dispose();
      }
      await assertProtectedUnchanged(harness, producerSeed, protectedBefore);
    } finally {
      traffic.dispose();
    }
  });
});
