import { expect, type Response } from '@playwright/test';
import { APP_ENTRY_ROUTE, dragTimelineClip, expectConnected, firstTrackName, openSeededTimeline, revisionBody, test as appTest } from './support/app.ts';
import { AstridCli } from './support/astrid.ts';
import { harnessUnavailableReason, startDirectHarness, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';
import { mountedDiagnosticInitScript } from './p1-diagnostic-safety.ts';
import type { CommitAcceptedMutation, HeadPin, HistoryPage } from '../../../src/integrations/runtime/timeline-commit-types.ts';

const CEILING = { timeout: 90_000 };
const REMOTE_VISIBLE_TIMEOUT = 10_000;
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const REMOTE_LABEL = 'Agent live D79 edit';

const test = appTest.extend<object, { seed3: ThreeProductsSeed; astrid: AstridCli }>({
  // Match the proven D66/P1 normal stack: P3 owns initialization of the
  // common pristine Runtime shell, and the three-product seed is the first
  // authored fixture on the Astrid profile.
  // eslint-disable-next-line no-empty-pattern
  harness: [async ({}, use) => {
    const harness = await startDirectHarness({ deferTimelineInitialization: true });
    try { await use(harness); } finally { await harness.stop(); }
  }, { scope: 'worker', timeout: 240_000 }],
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
  astrid: [async ({ harness }, use) => { await use(await AstridCli.create(harness)); }, { scope: 'worker', timeout: 240_000 }],
});

test.beforeAll(() => {
  const reason = harnessUnavailableReason();
  if (reason) throw new Error(`D79 live-edit smoke cannot run: ${reason}`);
});

test.describe.configure({ mode: 'serial' });

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const response = await harness.runtimeJson<HistoryPage>('GET',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  return response.body;
}

function pinOf(result: CommitAcceptedMutation): HeadPin {
  return { revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id };
}

function remotePayloadSeen(response: Response): Promise<boolean> {
  if (response.request().method() !== 'GET') return Promise.resolve(false);
  return response.text().then((text) => text.includes(REMOTE_LABEL)).catch(() => false);
}

test('D79 live-edit smoke: Agent edit arrives during a held drag and remote undo stays safe', async ({ page, harness, astrid, seed3 }) => {
  await astrid.preflight();
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}`);
  await expectConnected(page);
  await openSeededTimeline(page, harness);

  const before = (await history(harness, seed3)).head;
  const original = await revisionBody(harness, before.revision_id);
  const originalTrack = (original.payload.config.tracks as Array<Record<string, any>>).find((track) => track.id === 'V1');
  expect(originalTrack?.label).toBe('V1');
  await expect(firstTrackName(page)).toHaveValue('V1');

  let remoteSnapshotSeenDuringHold = false;
  page.on('response', (response) => {
    void remotePayloadSeen(response).then((seen) => {
      if (seen) remoteSnapshotSeenDuringHold = true;
    });
  });

  let heldClipX: number | undefined;
  const clip = page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`).first();
  const initialClipBox = await clip.boundingBox();
  expect(initialClipBox).toBeTruthy();

  let agentTurnFinishedAt = 0;
  const localCommit = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await dragTimelineClip(page, seed3.appClipId, seed3.transitionClipId, 0, 5, 15, async () => {
    heldClipX = (await clip.boundingBox())?.x;
    const remote = await astrid.commitCaptured(harness.seed.projectId, seed3.timelineId, before,
      { kind: 'label', trackId: 'V1', label: REMOTE_LABEL }, 'd79-agent-live-edit');
    expect(remote.data.status).toBe('accepted');
    agentTurnFinishedAt = Date.now();

    // This wait runs before dragTimelineClip releases the real pointer. The
    // response is therefore a genuine usePollSync arrival during the hold.
    await expect.poll(() => remoteSnapshotSeenDuringHold, {
      timeout: REMOTE_VISIBLE_TIMEOUT,
      message: 'the open editor must poll the Agent revision while the drag is held',
    }).toBe(true);
    await expect(firstTrackName(page)).toHaveValue('V1');
  });

  expect(heldClipX).toBeGreaterThan(initialClipBox!.x + 10);
  const localResponse = await localCommit;
  expect(localResponse.status(), await localResponse.text()).toBe(200);
  const local = await localResponse.json() as CommitAcceptedMutation;
  expect(local.data.status).toMatch(/^(accepted|rebased)$/);
  expect((local.data.canonical_document.parent_revision.payload.config as any).clips)
    .toEqual(expect.arrayContaining([expect.objectContaining({ id: seed3.appClipId, at: 5 })]));

  // The remote payload was observed during the hold; after release it must be
  // adopted by the real poll path within the owner-requested ten seconds.
  await expect.poll(() => firstTrackName(page).inputValue(), {
    timeout: REMOTE_VISIBLE_TIMEOUT,
    message: 'the open timeline must show the Agent edit within ten seconds of the CLI turn',
  }).toBe(REMOTE_LABEL);
  expect(Date.now() - agentTurnFinishedAt).toBeLessThanOrEqual(REMOTE_VISIBLE_TIMEOUT);

  const undo = page.getByRole('button', { name: 'Undo', exact: true });
  await expect(undo).toBeEnabled();
  const commitsBeforeUndo = (await history(harness, seed3)).items.length;
  const undoResponse = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await undo.click();
  const undoneResponse = await undoResponse;
  expect(undoneResponse.status(), await undoneResponse.text()).toBe(200);
  const undone = await undoneResponse.json() as CommitAcceptedMutation;
  expect(undone.data.canonical_document.parent_revision.payload.config.clips)
    .toEqual(expect.arrayContaining([expect.objectContaining({ id: seed3.appClipId, at: 0 })]));

  // Undo may remove the local drag, but the remoteCommit boundary must prevent
  // the pre-remote V1 snapshot from coming back.
  await expect(firstTrackName(page)).toHaveValue(REMOTE_LABEL);
  const finalHistory = await history(harness, seed3);
  expect(finalHistory.items.length).toBeGreaterThan(commitsBeforeUndo);
  expect(finalHistory.items.find((entry) => entry.publication_id === pinOf(undone).publication_id)?.records?.undo_of)
    .toEqual([local.receipt.receipt_id]);
});

test('D79 live-edit smoke: disjoint App and Agent clip moves merge and remain visible', async ({ page, harness, astrid, seed3 }) => {
  await astrid.preflight();
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}`);
  await expectConnected(page);
  await openSeededTimeline(page, harness);

  const before = (await history(harness, seed3)).head;
  const original = await revisionBody(harness, before.revision_id);
  const clips = original.payload.config.clips as Array<Record<string, any>>;
  const appClip = clips.find((clip) => clip.id === seed3.appClipId);
  const transitionClip = clips.find((clip) => clip.id === seed3.transitionClipId);
  expect(appClip?.at).toEqual(expect.any(Number));
  expect(transitionClip?.at).toEqual(expect.any(Number));
  const appFrom = Number(appClip!.at);
  const transitionFrom = Number(transitionClip!.at);
  const transitionTo = transitionFrom - 5;
  const initialAppBox = await page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`).first().boundingBox();
  const initialTransitionBox = await page.locator(`.clip-action[data-clip-id="${seed3.transitionClipId}"]`).first().boundingBox();
  expect(initialAppBox).toBeTruthy();
  expect(initialTransitionBox).toBeTruthy();

  const localCommit = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await dragTimelineClip(page, seed3.transitionClipId, seed3.appClipId, transitionFrom, transitionTo, appFrom);
  const localResponse = await localCommit;
  expect(localResponse.status(), await localResponse.text()).toBe(200);
  const local = await localResponse.json() as CommitAcceptedMutation;
  expect(local.data.status).toMatch(/^(accepted|rebased)$/);
  const localPin = pinOf(local);
  expect(local.data.canonical_document.parent_revision.payload.config.clips)
    .toEqual(expect.arrayContaining([expect.objectContaining({ id: seed3.transitionClipId, at: transitionTo })]));

  // The Agent evaluation started from R0. Runtime must field-merge its app-clip
  // write onto the App's accepted transition-clip write at R1.
  const agent = await astrid.commitCaptured(harness.seed.projectId, seed3.timelineId, before,
    { kind: 'move', clipId: seed3.appClipId, on: appFrom + 5 }, 'd79-disjoint-agent-clip');
  expect(agent.data.status).toBe('merged');
  expect(agent.data.rebased_onto).toEqual(localPin);
  const mergedClips = (agent.data.canonical_document.parent_revision.payload.config as any).clips;
  expect(mergedClips).toEqual(expect.arrayContaining([
    expect.objectContaining({ id: seed3.appClipId, at: appFrom + 5 }),
    expect.objectContaining({ id: seed3.transitionClipId, at: transitionTo }),
  ]));

  await expect.poll(async () => {
    const appBox = await page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`).first().boundingBox();
    const transitionBox = await page.locator(`.clip-action[data-clip-id="${seed3.transitionClipId}"]`).first().boundingBox();
    return Boolean(appBox && transitionBox
      && appBox.x > initialAppBox!.x + 10
      && transitionBox.x < initialTransitionBox!.x - 10);
  }, { ...CEILING, timeout: REMOTE_VISIBLE_TIMEOUT, message: 'the open editor must retain both disjoint clip moves' }).toBe(true);
});

test.fail('D79 live-edit smoke: same-field Agent conflict preserves the App draft without overwrite', async ({ page, harness, astrid, seed3 }) => {
  // The frozen Agent checkout has no genuine timeline.open()/commit(fn)
  // evaluation seam. The bounded assertions below prove the available
  // stale-commit/no-write and mounted draft-retention paths; the final gap is
  // deliberately expected to fail until the real evaluation API exists.
  await page.addInitScript({ content: mountedDiagnosticInitScript({ buffer: 'D79-e', maxRecords: 32 }) });
  await astrid.preflight();
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}`);
  await expectConnected(page);
  await openSeededTimeline(page, harness);

  const before = (await history(harness, seed3)).head;
  const userCommit = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await firstTrackName(page).fill('D79 user R1');
  await firstTrackName(page).press('Enter');
  await firstTrackName(page).blur();
  const userResponse = await userCommit;
  expect(userResponse.status(), await userResponse.text()).toBe(200);
  const user = await userResponse.json() as CommitAcceptedMutation;
  expect((user.data.canonical_document.parent_revision.payload.config as any).tracks)
    .toEqual(expect.arrayContaining([expect.objectContaining({ id: 'V1', label: 'D79 user R1' })]));

  // This is the actual Agent CLI command evaluated against R0 after the App
  // has committed R1. It must be a 409 value conflict with no Runtime write.
  const agentConflict = await astrid.commitCapturedResult(harness.seed.projectId, seed3.timelineId, before,
    { kind: 'label', trackId: 'V1', label: 'D79 Agent same-field' }, 'd79-same-field-agent-conflict');
  expect(agentConflict.ok).toBe(false);
  expect(agentConflict.error).toMatchObject({ code: expect.any(String), details: { status: 'conflict', reason: 'value_conflict' } });
  expect((await history(harness, seed3)).head).toEqual(pinOf(user));

  // Now exercise the real mounted App stale-base path: hold its R2 request,
  // let a second Agent commit win R2, then release the App request into 409.
  let release!: () => void;
  let held!: boolean;
  const gate = new Promise<void>((resolve) => { release = resolve; });
  const intercept = async (route: import('@playwright/test').Route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    held = true;
    await gate;
    const response = await route.fetch({ maxRetries: 0 });
    await route.fulfill({ response });
  };
  await page.route(COMMITS, intercept);
  const staleResponsePromise = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await firstTrackName(page).fill('D79 retained draft');
  await firstTrackName(page).press('Enter');
  await firstTrackName(page).blur();
  await expect.poll(() => held, CEILING).toBe(true);
  const staleBase = (await history(harness, seed3)).head;
  const remote = await astrid.commitCaptured(harness.seed.projectId, seed3.timelineId, staleBase,
    { kind: 'label', trackId: 'V1', label: 'D79 Agent winner' }, 'd79-same-field-app-stale-base');
  expect(remote.data.status).toMatch(/^(accepted|rebased)$/);
  release();
  const staleResponse = await staleResponsePromise;
  expect(staleResponse.status(), await staleResponse.text()).toBe(409);
  expect((await staleResponse.json()).details).toMatchObject({ status: 'conflict', reason: 'value_conflict' });
  await expect(page.getByTestId('timeline-command-recovery')).toContainText('Your changes are retained and need resolution');
  await expect(firstTrackName(page)).toHaveValue('D79 retained draft');
  expect((await history(harness, seed3)).head).toEqual(pinOf(remote));
  await page.unroute(COMMITS, intercept);

  const diagnostics = await page.evaluate(() => (window as unknown as {
    __timelineSaveDiagnosticsSnapshot?: () => { records?: Array<Record<string, unknown>> };
  }).__timelineSaveDiagnosticsSnapshot?.() ?? null);
  expect(diagnostics?.records).toEqual(expect.any(Array));

  throw new Error('D79 gap: current Astrid CLI exposes no genuine timeline.open()/commit(fn) evaluation, bounded re-read, or rerun API; numeric Agent HTTP 409 and TimelineVersionConflictError draft-retained proof remain unavailable.');
});
