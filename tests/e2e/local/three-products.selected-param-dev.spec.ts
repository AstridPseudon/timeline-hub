import { expect, type Page, type Request, type Route } from '@playwright/test';
import { commandOutboxes, openSeededTimeline, test as appTest } from './support/app.ts';
import type { DirectHarness, SelectedParamDevSeed } from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const STARTUP = { timeout: 20_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;

const test = appTest.extend<object, { selected: SelectedParamDevSeed }>({
  selected: [async ({ harness }, use) => { await use(await harness.seedSelectedParamDev()); }, { scope: 'worker', timeout: 240_000 }],
});

test.describe.configure({ mode: 'serial' });

interface CommitTraffic {
  request: Request;
  body: any;
  response?: { status: () => number };
}

function selectedCommand(traffic: CommitTraffic[], amount: number) {
  return traffic.find((post) => post.body?.commands?.[0]?.op === 'clip.set-params'
    && post.body.commands[0].args.values.amount === amount);
}

// Same-origin DEV omits the hosted RuntimeConnectionGate status pill. The App's existing
// mount is still observable: main.tsx renders into #root only after startup, and bootLayer.ts
// treats a non-empty #root as the first real page frame. Keep this separate from fixture data.
function expectAppMounted(page: Page) {
  return expect(page.locator('#root > *').first()).toBeAttached(STARTUP);
}

async function expectSelectedTimeline(page: Page, selected: SelectedParamDevSeed) {
  await expect(page.getByRole('combobox', { name: 'Select timeline' })).toBeVisible(CEILING);
  await expect.poll(() => new URL(page.url()).searchParams.get('project'), CEILING).toBe(selected.projectId);
  await expect.poll(() => new URL(page.url()).searchParams.get('timeline'), CEILING).toBe(selected.timelineId);
}

test('local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo', async ({ page, harness, selected }) => {
  await harness.startSelectedParamDevServer();
  const traffic: CommitTraffic[] = [];
  const legacyPosts: string[] = [];
  const commitPattern = COMMITS;
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    if (request.method() !== 'POST') return;
    if (commitPattern.test(pathname)) {
      traffic.push({ request, body: request.postDataJSON() });
    } else if (/composition-revisions|\/timeline\/save|supabase/.test(pathname)) {
      legacyPosts.push(pathname);
    }
  });
  page.on('response', (response) => {
    const post = traffic.find((candidate) => candidate.request === response.request());
    if (post) post.response = { status: () => response.status() };
  });

  await page.goto(`${harness.devOrigin}/tools/video-editor`);
  await expectAppMounted(page);
  await openSeededTimeline(page, harness);
  await expectSelectedTimeline(page, selected);
  const clip = page.locator(`.clip-action[data-clip-id="${selected.clipId}"]`).first();
  await expect(clip).toBeVisible(CEILING);
  await clip.click();
  await expect(page.getByTestId('astrid-element-params')).toBeVisible(CEILING);
  const amount = page.getByLabel('Amount');

  // The first edit is a real UI edit against the original P1, before P2 exists.
  await amount.fill('8');
  await expect.poll(() => selectedCommand(traffic, 8)?.response?.status() ?? 0, CEILING).toBe(200);
  const first = selectedCommand(traffic, 8)!;
  expect(first.body.commands[0].args.schema_source).toEqual(selected.p1DocumentPin);
  expect(first.body.commands[0].select).toBe(`parent/clip:${selected.clipId}`);

  // Admit P2 through the real Agent/Runtime project-pack path, then remove the authored source.
  // The page must continue to resolve the original P1 from its retained snapshot/object.
  const { p2 } = await harness.advanceSelectedParamAndRemoveSource(selected);
  expect(p2.revision).not.toBe(selected.p1.revision);
  await page.reload();
  await expectAppMounted(page);
  await openSeededTimeline(page, harness);
  await expectSelectedTimeline(page, selected);
  await expect(clip).toBeVisible(CEILING);
  await clip.click();
  await expect(page.getByTestId('astrid-element-params')).toBeVisible(CEILING);
  await expect(page.getByLabel('Amount')).toHaveValue('8');

  // The later P1 edit is refused by the retained P1 schema, not silently adopted by P2.
  await page.getByLabel('Amount').fill('16');
  await expect.poll(() => selectedCommand(traffic, 16)?.response?.status() ?? 0, CEILING).toBeGreaterThan(299);
  expect(selectedCommand(traffic, 16)!.body.commands[0].args.schema_source).toEqual(selected.p1DocumentPin);
  expect(selectedCommand(traffic, 16)!.body.commands[0].args.values.amount).toBe(16);

  // Lose only the acknowledgement after Runtime acceptance. Durable recovery must retain the exact request/key.
  const lost: { route: Route; body: string; key: string }[] = [];
  const loseAck = async (route: Route) => {
    if (route.request().method() !== 'POST' || lost.length > 0) return route.fallback();
    const response = await route.fetch({ maxRetries: 0 });
    lost.push({ route, body: route.request().postData()!, key: route.request().headers()['idempotency-key'] });
    void response;
  };
  await page.route(commitPattern, loseAck);
  await page.getByLabel('Amount').fill('9');
  await expect.poll(() => lost.length, CEILING).toBe(1);
  const lostBody = JSON.parse(lost[0].body);
  expect(lostBody.commands[0].args.schema_source).toEqual(selected.p1DocumentPin);
  await lost[0].route.abort('connectionreset').catch(() => {});
  await page.unroute(commitPattern, loseAck);
  await expect.poll(async () => (await commandOutboxes(page, selected.timelineId)).some((owner) => owner.pending?.outcome?.kind === 'retry'), CEILING).toBe(true);

  await page.reload();
  await expectAppMounted(page);
  await openSeededTimeline(page, harness);
  await expectSelectedTimeline(page, selected);
  await expect(clip).toBeVisible(CEILING);
  await clip.click();
  await expect(page.getByTestId('astrid-element-params')).toBeVisible(CEILING);
  await expect(page.getByLabel('Amount')).toHaveValue('8');
  const recovered = page.getByRole('button', { name: /^Recover saved edits/ }).first();
  await expect(recovered).toBeEnabled(CEILING);
  const retry = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await recovered.click();
  const retryResponse = await retry;
  expect(retryResponse.status()).toBe(200);
  expect(retryResponse.request().postData()).toBe(lost[0].body);
  expect(retryResponse.request().headers()['idempotency-key']).toBe(lost[0].key);
  await expect.poll(async () => (await commandOutboxes(page, selected.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);

  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  await expect.poll(() => traffic.some((post) => post.body?.commands?.[0]?.op === 'timeline.inverse'), CEILING).toBe(true);
  expect(legacyPosts).toEqual([]);
  expect(traffic.filter((post) => post.body?.commands?.[0]?.op === 'clip.set-params').every((post) => post.body.commands[0].args.schema_source.document_id === selected.p1DocumentPin.document_id)).toBe(true);
});
