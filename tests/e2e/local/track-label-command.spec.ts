/**
 * M2 real parent-track label journey.
 *
 * This is deliberately separate from three-products.spec.ts: the M1 mixed-editing case remains the
 * historical refusal proof, while this case is the positive command-path replacement for track labels.
 */
import { expect, type Page, type Request } from '@playwright/test';
import {
  harnessUnavailableReason,
  type DirectHarness,
  type ThreeProductsSeed,
} from './support/harness.ts';
import {
  currentHead,
  dragTimelineClip,
  expectConnected,
  firstTrackName,
  openApp,
  openSeededTimeline,
  revisionBody,
  test as appTest,
} from './support/app.ts';
import {
  ASTRID_PYTHON,
  AstridCli,
  astridUnavailableReason,
} from './support/astrid.ts';
import type {
  CanonicalDocument,
  CommitAcceptedMutation,
  HeadPin,
  HistoryPage,
} from '../../../src/integrations/runtime/timeline-commit-types.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_SAVES = /\/timelines\/[^/]+\/composition-revisions$/;
const NEW_LABEL = 'Picture é 🎬';

type CommitPost = {
  request: Request;
  body: Record<string, any>;
};

const test = appTest.extend<object, { seed3: ThreeProductsSeed; astrid: AstridCli }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
  astrid: [async ({ harness }, use) => { await use(await AstridCli.create(harness)); }, { scope: 'worker', timeout: 240_000 }],
});

test.describe.configure({ mode: 'serial' });

test.beforeAll(() => {
  const reason = harnessUnavailableReason() ?? astridUnavailableReason();
  if (reason) throw new Error(`the M2 track-label journey cannot run: ${reason}`);
});

function pinOf(result: CommitAcceptedMutation): HeadPin {
  return { revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id };
}

function trackIn(document: CanonicalDocument): Record<string, any> {
  const tracks = (document.parent_revision.payload.config as { tracks?: Array<Record<string, any>> }).tracks ?? [];
  const track = tracks.find((candidate) => candidate.id === 'V1');
  expect(track, 'the seeded parent track V1 remains addressable').toBeTruthy();
  return track!;
}

function expectOpaqueClosure(document: CanonicalDocument, seed: ThreeProductsSeed) {
  expect((document.parent_revision.payload.config as Record<string, any>).x_f2_opaque)
    .toEqual(seed.opaque.config);
  const child = document.internal_timeline_revisions
    .flatMap((revision) => ((revision.payload as Record<string, any>).clips as Array<Record<string, any>> | undefined) ?? [])
    .find((clip) => clip.id === seed.agentClipId);
  expect(child?.app?.f2Opaque, 'the Agent-owned opaque child state survives the App command').toEqual(seed.opaque.clip);
}

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const response = await harness.runtimeJson<HistoryPage>('GET',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  return response.body;
}

function attachTraffic(page: Page) {
  const commits: CommitPost[] = [];
  const legacy: string[] = [];
  page.on('request', (request) => {
    if (request.method() !== 'POST') return;
    const pathname = new URL(request.url()).pathname;
    if (COMMITS.test(pathname)) commits.push({ request, body: request.postDataJSON() as Record<string, any> });
    if (LEGACY_SAVES.test(pathname)) legacy.push(pathname);
  });
  return { commits, legacy };
}

async function waitForCommitCount(commits: CommitPost[], count: number) {
  await expect.poll(() => commits.length, {
    ...CEILING,
    message: 'the real App gesture must produce the expected Runtime /v1 command commit',
  }).toBe(count);
}

test('M2 real move then ordinary Unicode track rename reloads and guarded UI undo preserves an Agent edit', async ({ page, harness, astrid, seed3 }) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  await astrid.preflight();

  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);

  const originalHead = await currentHead(harness);
  const originalBody = await revisionBody(harness, originalHead);
  const originalPayload = originalBody.payload as Record<string, any>;
  const originalTrack = (originalPayload.config.tracks as Array<Record<string, any>>).find((track) => track.id === 'V1');
  expect(originalTrack, 'the seed has a parent V1 track').toBeTruthy();
  expect(Object.prototype.hasOwnProperty.call(originalTrack, 'label'), 'the original label is present, not a display fallback').toBe(true);
  expect(originalTrack!.label).toBe('V1');
  await expect(firstTrackName(page)).toHaveValue('V1');

  const traffic = attachTraffic(page);

  // Real pointer gesture first: the label command must be based on the accepted moved head.
  const moveResponse = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await dragTimelineClip(page, seed3.appClipId, seed3.transitionClipId, 0, 5, 15);
  const movedResponse = await moveResponse;
  expect(movedResponse.status(), await movedResponse.text()).toBe(200);
  await waitForCommitCount(traffic.commits, 1);
  const moved = await movedResponse.json() as CommitAcceptedMutation;
  expect(moved.data.commands).toHaveLength(1);
  expect(moved.data.commands[0]).toMatchObject({ op: 'clip.move', select: `parent/clip:${seed3.appClipId}`, args: { on: 5 } });
  expectOpaqueClosure(moved.data.canonical_document, seed3);

  // Consume the actual textbox through focus, typing and blur. No Enter shortcut or direct port is used.
  const label = firstTrackName(page);
  const renameResponse = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await label.click();
  await label.press('Control+A');
  await label.type(NEW_LABEL);
  await label.blur();
  const renamed = await renameResponse;
  expect(renamed.status(), await renamed.text()).toBe(200);
  await waitForCommitCount(traffic.commits, 2);
  const renameRequest = traffic.commits[1];
  expect(renameRequest.body).not.toHaveProperty('parent_composition');
  expect(renameRequest.body.commands).toHaveLength(1);
  expect(renameRequest.body.commands[0]).toMatchObject({
    schema_version: 1,
    op: 'track.set',
    version: '1',
    select: 'parent/track:V1',
  });
  expect(renameRequest.body.commands[0].args).toEqual({ values: { label: NEW_LABEL }, clear: [] });
  const renamedResult = await renamed.json() as CommitAcceptedMutation;
  expect(renamedResult.data.status).toMatch(/^(accepted|rebased)$/);
  expect(trackIn(renamedResult.data.canonical_document).label).toBe(NEW_LABEL);
  expectOpaqueClosure(renamedResult.data.canonical_document, seed3);
  await expect(label).toHaveValue(NEW_LABEL);

  const renamePublication = pinOf(renamedResult);
  const renameHistory = await history(harness, seed3);
  expect(renameHistory.items.find((entry) => entry.publication_id === renamePublication.publication_id)?.records?.commands[0].command)
    .toMatchObject({ op: 'track.set', select: 'parent/track:V1', args: { values: { label: NEW_LABEL }, clear: [] } });

  // A separate real Agent authoring edit changes a disjoint parent track before reload and undo.
  const independent = await astrid.commitCaptured(
    harness.seed.projectId,
    seed3.timelineId,
    renamePublication,
    { kind: 'track', id: 'f2-independent-C' },
    'm2-track-label-independent',
  );
  expect(independent.data.canonical_document.parent_revision.payload.config).toMatchObject({
    tracks: expect.arrayContaining([expect.objectContaining({ id: 'f2-independent-C' })]),
  });
  expectOpaqueClosure(independent.data.canonical_document, seed3);

  // Reload must load the accepted Unicode label and the committed history, not a draft or display fallback.
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await expect(firstTrackName(page)).toHaveValue(NEW_LABEL);
  const reloadedHistory = await history(harness, seed3);
  expect(reloadedHistory.items.some((entry) => entry.publication_id === renamePublication.publication_id)).toBe(true);

  const undoResponse = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  const undoneResponse = await undoResponse;
  expect(undoneResponse.status(), await undoneResponse.text()).toBe(200);
  await waitForCommitCount(traffic.commits, 3);
  const undoRequest = traffic.commits[2];
  expect(undoRequest.body.commands).toEqual([{
    schema_version: 1,
    op: 'timeline.inverse',
    version: '1',
    select: null,
    args: { publications: [renamePublication.publication_id] },
  }]);
  const undone = await undoneResponse.json() as CommitAcceptedMutation;
  expect(trackIn(undone.data.canonical_document)).toHaveProperty('label', 'V1');
  expect(undone.data.canonical_document.parent_revision.payload.config).toMatchObject({
    tracks: expect.arrayContaining([
      expect.objectContaining({ id: 'f2-independent-C' }),
      expect.objectContaining({ id: 'V1' }),
    ]),
  });
  expectOpaqueClosure(undone.data.canonical_document, seed3);
  await expect(firstTrackName(page)).toHaveValue('V1');

  const finalHistory = await history(harness, seed3);
  const undoEntry = finalHistory.items.find((entry) => entry.publication_id === undone.receipt.receipt_id);
  expect(undoEntry?.records?.undo_of).toEqual([renamePublication.publication_id]);
  expect(finalHistory.head.revision_id).toBe(undone.data.accepted_revision_id);
  expect(traffic.commits.map((post) => post.body.commands[0].op)).toEqual(['clip.move', 'track.set', 'timeline.inverse']);
  expect(traffic.commits.every((post) => !Object.prototype.hasOwnProperty.call(post.body, 'parent_composition'))).toBe(true);
  expect(traffic.legacy, 'M2 label editing must not emit legacy whole-config saves').toEqual([]);
});
