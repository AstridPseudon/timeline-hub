import { expect, type Page, type Request, type Response } from '@playwright/test';
import { THREE_PRODUCTS_REFERENCE_AT, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';
import { openEmbeddedCanonicalShot, test as appTest } from './support/app.ts';
import { ASTRID_PYTHON } from './support/astrid.ts';
import type { CanonicalDocument, CommitRequest, CommitAcceptedMutation } from '../../../src/integrations/runtime/timeline-commit-types.ts';

const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const CEILING = { timeout: 90_000 };

type JsonObject = Record<string, unknown>;

interface CommitPost {
  request: Request;
  response: Response;
  body: CommitRequest;
  json: CommitAcceptedMutation;
}

function object(value: unknown, label: string): JsonObject {
  expect(value, label).toBeTruthy();
  expect(typeof value, label).toBe('object');
  expect(Array.isArray(value), label).toBe(false);
  return value as JsonObject;
}

function childClips(document: CanonicalDocument, occurrenceId: string): JsonObject[] {
  const parent = object(document.parent_revision.payload, 'parent payload');
  const occurrences = parent.occurrences as JsonObject[];
  const occurrence = occurrences.find((candidate) => candidate.occurrence_id === occurrenceId);
  expect(occurrence, `occurrence ${occurrenceId}`).toBeTruthy();
  const shot = document.shot_revisions.find((candidate) => candidate.revision_id === occurrence!.shot_revision_id);
  expect(shot, `shot revision for ${occurrenceId}`).toBeTruthy();
  const internal = document.internal_timeline_revisions.find(
    (candidate) => candidate.revision_id === shot!.internal_timeline_revision_id,
  );
  expect(internal, `internal timeline for ${occurrenceId}`).toBeTruthy();
  const payload = object(internal!.payload, 'shot timeline payload');
  expect(Array.isArray(payload.clips), 'shot timeline clips').toBe(true);
  return payload.clips as JsonObject[];
}

function parentContainsClip(document: CanonicalDocument, clipId: string): boolean {
  const parent = object(document.parent_revision.payload, 'parent payload');
  const config = object(parent.config, 'parent config');
  const parentClips = Array.isArray(parent.clips) ? parent.clips : [];
  const configClips = Array.isArray(config.clips) ? config.clips : [];
  return [...parentClips, ...configClips].some((clip) => object(clip, 'parent clip').id === clipId);
}

async function openTimeline(page: Page, harness: DirectHarness, seed: ThreeProductsSeed): Promise<void> {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  await page.goto(`${harness.origin}/tools/video-editor`);
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByRole('combobox', { name: 'Select project' })).toContainText(harness.seed.projectName);
  await expect(page.getByRole('textbox', { name: 'Track name' }).first()).toBeVisible();
  expect(seed.timelineId).toBe(harness.seed.timelineId);
}

async function commitFromGesture(page: Page, gesture: () => Promise<void>): Promise<CommitPost> {
  const responsePromise = page.waitForResponse(
    (response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname),
    CEILING,
  );
  await gesture();
  const response = await responsePromise;
  const request = response.request();
  return {
    request,
    response,
    body: request.postDataJSON() as CommitRequest,
    json: await response.json() as CommitAcceptedMutation,
  };
}

async function dragGalleryImageIntoShot(page: Page): Promise<void> {
  await page.evaluate(() => {
    const source = [...document.querySelectorAll<HTMLElement>('[data-testid="generations-pane"] [data-gallery-item-id]')]
      .find((tile) => tile.querySelector('img'));
    const target = document.querySelector<HTMLElement>('[role="dialog"] .timeline-wrapper');
    if (!source) throw new Error('The locked bottom gallery has no draggable image tile.');
    if (!target) throw new Error('The open shot editor has no timeline drop target.');
    const targetBox = target.getBoundingClientRect();
    const clientX = targetBox.left + Math.max(1, targetBox.width / 2);
    const clientY = targetBox.top + Math.max(1, targetBox.height / 2);
    const dataTransfer = new DataTransfer();
    const event = (type: 'dragstart' | 'dragover' | 'drop' | 'dragend') => new DragEvent(type, {
      bubbles: true,
      cancelable: true,
      clientX,
      clientY,
      dataTransfer,
    });
    source.dispatchEvent(event('dragstart'));
    target.dispatchEvent(event('dragover'));
    target.dispatchEvent(event('drop'));
    source.dispatchEvent(event('dragend'));
  });
}

async function reloadAndOpenShot(page: Page, seed: ThreeProductsSeed, revisionId: string) {
  await page.reload();
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByRole('textbox', { name: 'Track name' }).first()).toBeVisible();
  await expect(page.getByTestId('preview-revision-label').filter({ hasText: `Committed ${revisionId}` }).first())
    .toBeVisible(CEILING);
  return openEmbeddedCanonicalShot(page, seed.occurrenceId, 'F2 agent shot');
}

appTest('C2 gallery drag into shot saves exactly one shot-local clip, reloads, and undoes', async ({ page, harness }) => {
  const seed = await harness.seedThreeProducts(THREE_PRODUCTS_REFERENCE_AT, 'native-none');
  await openTimeline(page, harness, seed);

  // Use the existing lockable bottom gallery. This is intentionally opened before
  // the shot editor so the journey proves that the gallery stays usable behind it.
  await page.getByRole('button', { name: 'Open Gallery', exact: true }).click();
  await expect(page.getByTestId('generations-pane')).toBeVisible();
  await page.getByRole('button', { name: 'Lock pane', exact: true }).click();
  const galleryImage = page.locator('[data-testid="generations-pane"] [data-gallery-item-id]:has(img)').first();
  await expect(galleryImage).toBeVisible(CEILING);

  const beforeHead = await harness.runtimeJson<{ head_revision_id: string }>(
    'GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}`,
  );
  const before = await harness.runtimeJson<CanonicalDocument>(
    'GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${beforeHead.body.head_revision_id}`,
  );
  const beforeChild = childClips(before.body, seed.occurrenceId);

  const dialog = await openEmbeddedCanonicalShot(page, seed.occurrenceId, 'F2 agent shot');
  await expect(page.locator('[data-dialog-backdrop]')).toHaveCount(0);
  await expect(galleryImage).toBeVisible();
  await expect(dialog.locator('.timeline-wrapper').first()).toBeVisible();

  const post = await commitFromGesture(page, () => dragGalleryImageIntoShot(page));
  const command = object(post.body.commands[0], 'gallery drop command');
  expect(command.op).toBe('occurrence.add-media');
  expect(command.select).toBe(`occurrence:${seed.occurrenceId}`);
  const row = object(object(command.args, 'gallery drop args').row, 'new shot clip');
  expect(row.id).toEqual(expect.any(String));

  const after = post.json.data.canonical_document;
  const afterChild = childClips(after, seed.occurrenceId);
  expect(afterChild.filter((clip) => !beforeChild.some((known) => known.id === clip.id)))
    .toEqual([expect.objectContaining({ id: row.id })]);
  expect(afterChild).toHaveLength(beforeChild.length + 1);
  expect(parentContainsClip(after, row.id as string)).toBe(false);

  const projectedClipId = `${seed.occurrenceId}:${row.id as string}`;
  await dialog.getByRole('button', { name: 'Close', exact: true }).click();
  await expect(page.locator(`.clip-action[data-clip-id="${projectedClipId}"]`)).toHaveCount(0);

  const reloadedDialog = await reloadAndOpenShot(page, seed, after.parent_revision.revision_id);
  await expect(reloadedDialog.locator(`.clip-action[data-clip-id="${projectedClipId}"]`)).toHaveCount(1);
  await reloadedDialog.getByRole('button', { name: 'Close', exact: true }).click();

  const undo = await commitFromGesture(page, async () => {
    await page.getByRole('button', { name: 'Undo', exact: true }).click();
  });
  expect(undo.body.commands[0]).toMatchObject({ op: 'timeline.inverse' });
  const undone = undo.json.data.canonical_document;
  expect(undone.parent_revision.payload).toEqual(before.body.parent_revision.payload);
  expect(undone.shot_revisions).toEqual(before.body.shot_revisions);
  expect(undone.internal_timeline_revisions).toEqual(before.body.internal_timeline_revisions);

  const undoneDialog = await reloadAndOpenShot(page, seed, undone.parent_revision.revision_id);
  await expect(undoneDialog.locator(`.clip-action[data-clip-id="${projectedClipId}"]`)).toHaveCount(0);
});
