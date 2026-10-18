/**
 * Three products on one realm (testing plan F2, thin slice on the Plan A direct path):
 *
 *   npm run test:e2e:three-products    # hosted App build -> loopback gateway -> real Runtime, plus the real Astrid CLI
 *
 * The App (hosted build, Chromium) and the agent (the Astrid CLI as a subprocess) are two clients of one Runtime. Nothing in a
 * case is a stand-in: the page talks to the real gateway, Astrid to the same Runtime over its own credential, and the Runtime
 * is the real daemon on a throwaway realm. Needs an Astrid checkout (ASTRID_CHECKOUT, default ../astrid-agent) with its Python
 * (ASTRID_PYTHON, default <checkout>/.venv/bin/python); a missing prerequisite fails the run with its name, it never skips.
 *
 * Cases
 *   1  agent -> open App   an Astrid task and the agent's publication show up in the open App with no reload
 *   2  concurrent edit     the App's acknowledgement is lost while the agent publishes and the App edits again
 *   3  Runtime restart     the draft survives, saves after the relaunch, and the agent follows the new endpoint
 * Every case first proves the three products share one realm, one Runtime instance and one contract, and ends with the
 * page-wide check that no credential ever reached the page.
 *
 * Not covered here (recorded, each released by a named test; plan "Owned debt"):
 *   step 3  render R adversarially (publish R+1 before it runs)   needs rendering without a provisioned Remotion and Linux custody
 *   step 4  playback parity of that render                         same
 *   step 6  Codex image -> sprite                                  full tier only, needs the network
 *
 * Speed: durations, Astrid call times and the load average are written to three-products-summary.json (beside the Playwright
 * output) and never judged (R-10). Waits are hang ceilings, not budgets. The ordering of events is made by awaited CLI calls and
 * route holds, never by sleeping.
 */
import { expect, type Locator, type Page, type Request } from '@playwright/test';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { cpus, loadavg } from 'node:os';
import path from 'node:path';
import { harnessUnavailableReason, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';
import { currentHead, editFirstTrackName, expectConnected, firstTrackName, holdTimelineSaves, openApp, openSeededTimeline, revisionBody, test as appTest, UI } from './support/app.ts';
import { AstridCli, astridUnavailableReason, contractDigest, realmDisagreements, revisionSet, type AstridCall, type AstridIdentity } from './support/astrid.ts';

/** A hang ceiling for one wait (R-10): many times the usual time, never a budget. */
const CEILING = { timeout: 90_000 };
const SAVES = /\/timelines\/[^/]+\/composition-revisions$/;
const CONFLICT_TITLE = 'This timeline changed somewhere else';

const test = appTest.extend<object, { seed3: ThreeProductsSeed; astrid: AstridCli; quickAstrid: AstridCli }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
  astrid: [async ({ harness, seed3 }, use) => {
    const astrid = await AstridCli.create(harness);
    journey.activeAstrid = astrid;
    journey.identity = await astrid.preflight();
    // The seed must be something Astrid accepts as it is (a real finding otherwise): check a fresh working copy of it, then drop it.
    await astrid.astrid(['timelines', 'checkout', seed3.timelineId, '--project', seed3.projectSlug, '--fresh', '--json']);
    await astrid.astrid(['timelines', 'check', seed3.timelineId, '--project', seed3.projectSlug, '--no-sweep']);
    await astrid.astrid(['timelines', 'discard', seed3.timelineId, '--project', seed3.projectSlug]);
    journey.preflightCalls = [...astrid.calls];
    await use(astrid);
  }, { scope: 'worker', timeout: 240_000 }],
  quickAstrid: [async ({ harness }, use) => {
    if (!harness.attachment) throw new Error('quick Astrid fixture requires ASTRID_QUICK_DESCRIPTOR');
    const astrid = await AstridCli.create(harness);
    journey.activeAstrid = astrid;
    journey.identity = await astrid.preflight();
    journey.preflightCalls = [...astrid.calls];
    await use(astrid);
  }, { scope: 'worker', timeout: 0 }],
});

test.describe.configure({ mode: 'serial' });
test.beforeAll(() => {
  const reason = harnessUnavailableReason() ?? astridUnavailableReason();
  if (reason) throw new Error(`the three-products journey cannot run: ${reason}`);
});

// ---------------------------------------------------------------------------------------------
// The run summary (revision set, durations, load: reported, never judged)

interface CaseRecord {
  name: string;
  status: string;
  durationMs: number;
  loadAverageStart: number;
  loadAverageEnd: number;
  astridCalls: AstridCall[];
  facts: Record<string, unknown>;
}

const journey = {
  startedAt: new Date().toISOString(),
  loadAverageStart: loadavg(),
  identity: undefined as AstridIdentity | undefined,
  preflightCalls: [] as AstridCall[],
  cases: [] as CaseRecord[],
  activeAstrid: undefined as AstridCli | undefined,
  /** What the running case has learned that the summary should carry (named facts, never verdicts on speed). */
  facts: {} as Record<string, unknown>,
  caseStart: { at: 0, load: 0, calls: 0 },
};

test.beforeEach(() => {
  journey.facts = {};
  journey.caseStart = { at: Date.now(), load: loadavg()[0], calls: journey.activeAstrid?.calls.length ?? 0 };
});

// Playwright reads fixture dependencies from the destructuring pattern, so the empty pattern is required.
// eslint-disable-next-line no-empty-pattern
test.afterEach(async ({}, testInfo) => {
  const astrid = journey.activeAstrid;
  journey.cases.push({
    name: testInfo.title,
    status: testInfo.status ?? 'unknown',
    durationMs: testInfo.duration,
    loadAverageStart: journey.caseStart.load,
    loadAverageEnd: loadavg()[0],
    astridCalls: astrid?.calls.slice(journey.caseStart.calls) ?? [],
    facts: journey.facts,
  });
});

// Playwright reads fixture dependencies from the destructuring pattern, so the empty pattern is required.
// eslint-disable-next-line no-empty-pattern
test.afterAll(async ({}, testInfo) => {
  const outputDir = testInfo.project.outputDir;
  mkdirSync(outputDir, { recursive: true });
  writeFileSync(path.join(outputDir, 'three-products-summary.json'), JSON.stringify({
    startedAt: journey.startedAt,
    note: 'reported, never judged (testing plan R-10)',
    revisions: revisionSet(journey.identity),
    machine: { cpus: cpus().length, loadAverageStart: journey.loadAverageStart, loadAverageEnd: loadavg() },
    preflight: { astridCalls: journey.preflightCalls },
    cases: journey.cases,
  }, null, 2));
});

// ---------------------------------------------------------------------------------------------
// Helpers: what the Runtime holds, what the page was told, what the agent sees

/** JSON with sorted keys, so "equal" means the same data whatever the key order. */
function canonical(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical((value as Record<string, unknown>)[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

const timelineBase = (harness: DirectHarness, seed: Pick<ThreeProductsSeed, 'timelineId'>) => `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}`;

/** Every composition revision of the seeded timeline, newest first. */
async function allRevisions(harness: DirectHarness, seed: Pick<ThreeProductsSeed, 'timelineId'>): Promise<Array<{ revision_id: string; is_current_head: boolean }>> {
  const items: Array<{ revision_id: string; is_current_head: boolean }> = [];
  let cursor: string | null = null;
  do {
    const page: { status: number; body: any } = await harness.runtimeJson('GET', `${timelineBase(harness, seed)}/composition-revisions?limit=50${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ''}`);
    expect(page.status, JSON.stringify(page.body)).toBe(200);
    items.push(...page.body.items);
    cursor = page.body.next_cursor ?? null;
  } while (cursor);
  return items;
}

/** The parent composition of a revision and the agent's shot content beneath it, read straight from the Runtime. */
async function revisionState(harness: DirectHarness, seed: ThreeProductsSeed, revisionId: string) {
  const parent = (await revisionBody(harness, revisionId)).payload;
  const occurrence = (parent.occurrences as Array<Record<string, any>>).find((candidate) => candidate.occurrence_id === seed.occurrenceId);
  expect(occurrence, `revision ${revisionId} keeps the agent's shot placement`).toBeTruthy();
  const shot = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/shots/${seed.shotId}/revisions/${occurrence!.shot_revision_id}`);
  expect(shot.status, JSON.stringify(shot.body)).toBe(200);
  const inner = await harness.runtimeJson('GET', `${timelineBase(harness, seed)}/revisions/${(shot.body as any).internal_timeline_revision_id}`);
  expect(inner.status, JSON.stringify(inner.body)).toBe(200);
  const payload = (inner.body as any).payload;
  return {
    revisionId,
    parent,
    trackLabel: (parent.config.tracks as Array<Record<string, any>>).find((track) => track.id === 'V1')?.label as string | undefined,
    parentClips: Object.fromEntries((parent.clips as Array<Record<string, any>>).map((clip) => [clip.id, clip])) as Record<string, Record<string, any>>,
    shotClips: Object.fromEntries((payload.clips as Array<Record<string, any>>).map((clip) => [clip.id, clip])) as Record<string, Record<string, any>>,
    shotRegistry: payload.registry.assets as Record<string, Record<string, any>>,
    internalRevisionId: (shot.body as any).internal_timeline_revision_id as string,
  };
}

/** The opaque data neither client models is the seed's, unchanged, in the seed and in every later revision (the App's saves and the agent's alike). */
async function expectOpaqueDataKept(harness: DirectHarness, seed: ThreeProductsSeed) {
  const revisions = await allRevisions(harness, seed);
  const seedAt = revisions.findIndex((revision) => revision.revision_id === seed.headRevisionId);
  expect(seedAt, 'the seed revision is in the history').toBeGreaterThanOrEqual(0);
  for (const revision of revisions.slice(0, seedAt + 1)) {
    const state = await revisionState(harness, seed, revision.revision_id);
    expect(canonical(state.parent.config.x_f2_opaque), `config.x_f2_opaque in ${revision.revision_id}`).toBe(canonical(seed.opaque.config));
    expect(canonical(state.shotClips[seed.agentClipId].app?.f2Opaque), `${seed.agentClipId}.app.f2Opaque in ${revision.revision_id}`).toBe(canonical(seed.opaque.clip));
  }
  return revisions.length;
}

/** The agent's verbs, as the CLI ships them. */
function agentOf(astrid: AstridCli, seed: Pick<ThreeProductsSeed, 'timelineId' | 'projectSlug'>) {
  const common = [seed.timelineId, '--project', seed.projectSlug];
  return {
    checkout: () => astrid.astrid(['timelines', 'checkout', ...common, '--fresh', '--json']),
    edit: (...flags: string[]) => astrid.astrid(['timelines', 'edit', ...common, ...flags]),
    publish: async (message: string, idempotencyKey: string) => {
      const envelope = await astrid.json<{ new_head: string; old_head: string; idempotency_key: string; published?: boolean }>(['timelines', 'publish', ...common, '-m', message, '--idempotency-key', idempotencyKey, '--json']);
      expect(envelope.ok, JSON.stringify(envelope)).toBe(true);
      return envelope.data!;
    },
    status: async () => (await astrid.json<{ current_head: string }>(['timelines', 'status', ...common, '--json'])).data!,
    show: async () => (await astrid.json<{ head_revision_id: string; rows: Array<{ layers: Array<{ clip_id: string; asset: string | null }> }> }>(['timelines', 'show', ...common, '--published', '--json'])).data!,
  };
}

/** A credential never reaches the page: not in a request, a gateway answer, the DOM, or the page's storage. */
class TokenSniff {
  private readonly pending: Array<Promise<void>> = [];
  private readonly leaks: string[] = [];

  constructor(private readonly tokens: Record<string, string>) {}

  private scan(where: string, text: string | null | undefined) {
    if (!text) return;
    for (const [name, token] of Object.entries(this.tokens)) if (text.includes(token)) this.leaks.push(`${name} token in ${where}`);
  }

  attach(page: Page) {
    page.on('request', (request: Request) => {
      this.pending.push((async () => {
        const headers = await request.allHeaders().catch(() => request.headers());
        this.scan(`the URL of ${request.method()} ${request.url().split('?')[0]}`, request.url());
        this.scan(`the headers of ${request.method()} ${request.url().split('?')[0]}`, JSON.stringify(headers));
        this.scan(`the body of ${request.method()} ${request.url().split('?')[0]}`, request.postData());
      })());
    });
    page.on('response', (response) => {
      const type = response.headers()['content-type'] ?? '';
      if (!/json|text/.test(type) || !response.url().includes(`:${new URL(response.url()).port}/api/`)) return;
      this.pending.push(response.text().then((text) => this.scan(`the answer to ${response.request().method()} ${response.url().split('?')[0]}`, text)).catch(() => {}));
    });
  }

  async expectClean(page: Page) {
    await Promise.all(this.pending);
    const inPage = await page.evaluate(() => JSON.stringify({
      dom: document.documentElement.outerHTML,
      local: Object.fromEntries(Object.entries(window.localStorage)),
      session: Object.fromEntries(Object.entries(window.sessionStorage)),
      cookie: document.cookie,
    }));
    this.scan('the page (DOM, storage, cookies)', inPage);
    expect(this.leaks, 'no credential reached the page').toEqual([]);
  }
}

/** The credentials in play: the App's, Astrid's, and the Runtime's owner and worker credentials (none belongs in a page). */
function secretsOf(harness: DirectHarness, astrid: AstridCli): Record<string, string> {
  const fromFile = (file: string) => {
    const text = readFileSync(file, 'utf8').trim();
    try { const parsed = JSON.parse(text); return typeof parsed.token === 'string' ? parsed.token : text; } catch { return text; }
  };
  return {
    product: harness.productToken,
    astrid: astrid.secret,
    owner: fromFile(path.join(harness.supportDir, 'credentials', 'owner.token')),
    worker: fromFile(harness.discovery().worker_credential_file),
  };
}

/**
 * The three products are talking to the same Runtime: the realm and instance the harness made, the page's health and realm
 * (fetched from inside the page, through the gateway) and Astrid's handshake all agree, and so do the contract digests of the App,
 * of Astrid and of the Runtime. Returns what each saw, for the summary.
 */
async function expectSameRealm(page: Page, harness: DirectHarness, astrid: AstridCli) {
  const fromPage = await page.evaluate(async (base) => {
    const [health, realm] = await Promise.all([fetch(`${base}/v1/health`), fetch(`${base}/v1/realm`)]);
    return { health: await health.json(), realm: await realm.json() };
  }, harness.gatewayBase);
  const fromAstrid = await astrid.identity();
  const digest = contractDigest();
  expect([
    ...realmDisagreements('the page', { realm_id: fromPage.realm.realm_id, runtime_instance_id: fromPage.health.runtime_instance_id, schema_digest: fromPage.health.schema_digest }, harness, digest),
    ...realmDisagreements('Astrid', fromAstrid, harness, digest),
  ], 'the page, Astrid and the Runtime share one realm, instance and contract').toEqual([]);
  return { realmId: fromPage.realm.realm_id as string, runtimeInstanceId: fromPage.health.runtime_instance_id as string, schemaDigest: fromPage.health.schema_digest as string, astridFile: fromAstrid.astrid_file };
}

/** The transition control of the clip panel, found by its label (the panel's selects carry no accessible name). */
const transitionSelect = (page: Page): Locator => page.getByText('Transition', { exact: true }).locator('xpath=following::*[@role="combobox"][1]');

async function selectClip(page: Page, clipId: string) {
  await page.locator(`[data-clip-id="${clipId}"]`).first().click();
}

async function setTransitionToNone(page: Page, clipId: string) {
  await selectClip(page, clipId);
  await transitionSelect(page).click();
  await page.getByRole('option', { name: 'None', exact: true }).click();
  await expect(transitionSelect(page)).toContainText('None');
}

/** Opens the App's action pane, where the runtime activity dock lives (it slides away until opened). */
async function openActionPane(page: Page) {
  await page.getByRole('button', { name: /^Open Action pane/ }).click();
  await expect(page.locator('[data-runtime-activity-dock]')).toBeVisible();
}

/** What the page was told by the Runtime: the answers it received, keyed by what they are. */
function watchPageReads(page: Page, harness: DirectHarness) {
  const reads = { eventFeed: [] as Array<{ aggregate_type: string; aggregate_id: string; event_type: string }>, urls: [] as string[], internalRevisions: [] as Array<{ id: string; payload: any }>, compositionRevisions: [] as Array<{ id: string; payload: any }> };
  page.on('response', (response) => {
    const url = response.url();
    if (!url.startsWith(harness.gatewayBase) || response.request().method() !== 'GET' || response.status() !== 200) return;
    const route = url.slice(harness.gatewayBase.length);
    reads.urls.push(route);
    if (route.startsWith('/v1/events')) {
      void response.json().then((body) => { for (const item of body.items ?? []) reads.eventFeed.push({ aggregate_type: item.aggregate_type, aggregate_id: item.aggregate_id, event_type: item.event_type }); }).catch(() => {});
    } else if (/\/composition-revisions\/[^/?]+$/.test(route)) {
      void response.json().then((body) => { reads.compositionRevisions.push({ id: body.revision_id, payload: body.payload }); }).catch(() => {});
    } else if (/\/timelines\/[^/]+\/revisions\/[^/?]+$/.test(route)) {
      void response.json().then((body) => { reads.internalRevisions.push({ id: body.revision_id, payload: body.payload }); }).catch(() => {});
    }
  });
  return reads;
}

const noReloadFlag = (page: Page) => page.evaluate(() => (window as unknown as { __noReload?: boolean }).__noReload);

async function plantNoReloadFlag(page: Page) {
  await page.evaluate(() => { (window as unknown as { __noReload: boolean }).__noReload = true; });
}

// ---------------------------------------------------------------------------------------------
// 1. agent -> open App

test('agent -> open App: an Astrid task and its publication appear in the open App without a reload', async ({ page, harness, astrid, seed3 }) => {
  const agent = agentOf(astrid, seed3);
  const sniff = new TokenSniff(secretsOf(harness, astrid));
  sniff.attach(page);
  const reads = watchPageReads(page, harness);

  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await plantNoReloadFlag(page);
  await openActionPane(page);
  journey.facts.sameRealm = await expectSameRealm(page, harness, astrid);

  // The agent registers an executor and admits a task. The page learns of it from the Runtime's event feed, not from a reload.
  await astrid.host({ register: true });
  const created = await astrid.json<{ task_id: string }>(['tasks', 'create', '--project', seed3.projectSlug, '--capability', 'f2.marker', '--spec', '{}', '--json']);
  expect(created.ok, JSON.stringify(created)).toBe(true);
  const taskId = created.data!.task_id;
  const row = page.locator(`[data-activity-task-id="${taskId}"]`);
  await expect(row).toHaveAttribute('aria-label', /^F2 Marker, (Queued|Ready)$/, CEILING);
  await expect.poll(() => reads.eventFeed, { message: 'the page was told by the event feed', ...CEILING }).toContainEqual(expect.objectContaining({ aggregate_type: 'task', aggregate_id: taskId }));

  // The executor runs it: the task leaves the active rows and is listed as complete.
  const ran = await astrid.host({ runOnce: true });
  expect(ran).toMatchObject({ task_id: taskId, state: 'succeeded' });
  const output = ran.outputs?.find((candidate) => candidate.name === 'marker');
  expect(output, 'the task produced its marker image').toBeTruthy();
  await expect(row).toHaveCount(0, CEILING);
  await page.getByRole('button', { name: 'Peek at tasks' }).click();
  await expect(page.locator('[data-task-peek-surface="tasks"]').filter({ hasText: 'F2 Marker' }).getByText('Complete', { exact: true })).toBeVisible(CEILING);
  const settled = await astrid.json<{ state: string }>(['tasks', 'show', taskId, '--project', seed3.projectSlug, '--json']);
  expect(settled.data!.state, 'the Runtime agrees the task succeeded').toBe('succeeded');

  // The agent publishes the timeline with the task's output; the open page adopts that revision by itself.
  const before = await currentHead(harness);
  await agent.checkout();
  await agent.edit('--clip', seed3.agentClipId, '--swap-asset', `${seed3.markerAssetKey}=task:${taskId}/marker#0`);
  const published = await agent.publish('agent: marker', 'f2-case1');
  expect(published.old_head, 'the agent built on the head the App has').toBe(before);
  expect(published.new_head).not.toBe(before);
  expect(await currentHead(harness), 'the Runtime head is the agent\'s revision').toBe(published.new_head);

  await expect.poll(() => reads.urls.some((url) => url.includes(`/composition-revisions/${published.new_head}`)), CEILING).toBe(true);
  await expect.poll(() => reads.internalRevisions.some((revision) => revision.payload?.registry?.assets?.[seed3.markerAssetKey]), CEILING).toBe(true);
  const adopted = reads.internalRevisions.find((revision) => revision.payload?.registry?.assets?.[seed3.markerAssetKey])!;
  expect(adopted.payload.registry.assets[seed3.markerAssetKey].media_id, 'the page received the revision that carries the task\'s output').toBe(output!.object_id);
  expect(await noReloadFlag(page), 'the page was never reloaded').toBe(true);

  // The Runtime holds the same data: the revision is the task's work, and the agent's edit kept what neither client models.
  const state = await revisionState(harness, seed3, published.new_head);
  expect(state.shotRegistry[seed3.markerAssetKey].media_id).toBe(output!.object_id);
  expect(state.shotClips[seed3.agentClipId].asset).toBe(seed3.markerAssetKey);
  expect((await agent.show()).head_revision_id, 'the agent reads the head it published').toBe(published.new_head);
  // The App's next save is built on the agent's head, and the Runtime accepts it (the parent-head check of the retired handoff case).
  const appSaved = page.waitForResponse((response) => response.request().method() === 'POST' && SAVES.test(new URL(response.url()).pathname), CEILING);
  await editFirstTrackName(page, 'F2 App after agent');
  const appSave = await appSaved;
  expect(appSave.status(), 'the Runtime accepts the App\'s save on the agent\'s head').toBe(200);
  expect(appSave.request().postDataJSON().expected_head, 'the App built its save on the agent\'s head').toBe(published.new_head);
  await expect.poll(() => currentHead(harness), CEILING).not.toBe(published.new_head);
  const appRevision = await currentHead(harness);
  expect(await noReloadFlag(page), 'the page was still not reloaded after its own save').toBe(true);

  // The agent reads the App's save made on top of its own publication.
  expect((await agent.status()).current_head, 'the agent reads the App\'s revision').toBe(appRevision);

  const revisionCount = await expectOpaqueDataKept(harness, seed3);

  journey.facts = { ...journey.facts, taskId, outputObjectId: output!.object_id, agentRevision: published.new_head, appRevision, revisionCount };
  await sniff.expectClean(page);
});

// ---------------------------------------------------------------------------------------------
// 2. concurrent edit

/**
 * One outcome today, and the App picks it: a named conflict that keeps the draft.
 *
 * The App's save A commits at the Runtime but its acknowledgement is lost (the held response is aborted as a connection reset).
 * While it is unacknowledged the agent publishes B on top of A, and the App edits again (C).
 * Then the App's own transport retry replays A with the same idempotency key, and the Runtime returns the stored receipt
 * (new_head = A). From there one of two things happens, depending on whether a head poll that queued up during the hold ran
 * before the 500 ms retry; this test records which and asserts neither:
 *   (a) the provider's cached head has already moved to B, so it refuses the confirmed receipt ("The save was confirmed, but
 *       the timeline has since changed", dataProvider.ts:869-879); or
 *   (b) the receipt is accepted and the queued edit C is posted on head A, where the Runtime answers 409 stale_head
 *       (useTimelinePersistence.ts:700-721, service.py:3129-3134).
 * Both raise TimelineVersionConflictError, which opens "This timeline changed somewhere else" and freezes autosave
 * (useTimelinePersistence.ts:402-406, 806-833; useTimelineRealtime.ts:23-27). The merge is not reachable: B4 removed the path that
 * rebased onto the head and re-posted, and nothing in the App rebases a local draft onto another writer's head
 * (dataProvider.ts:766-773, 869-879). If a later App change merges here, that is a deliberate update to this test (R-7).
 */
test('concurrent edit: the App\'s acknowledgement is lost, the agent publishes, the App edits again; the App names the conflict and keeps its draft', async ({ page, harness, astrid, seed3 }) => {
  const agent = agentOf(astrid, seed3);
  const sniff = new TokenSniff(secretsOf(harness, astrid));
  sniff.attach(page);
  const watched = watchPageReads(page, harness);

  // Every save the page sends, with the key and head it names and what became of it.
  interface Post { key: string; expectedHead: string | null; status: number | null; outcome: 'held' | 'sent' | 'lost' }
  const posts: Post[] = [];
  const postOf = new Map<Request, Post>();
  page.on('request', (request) => {
    if (request.method() !== 'POST' || !SAVES.test(new URL(request.url()).pathname)) return;
    const post: Post = { key: request.headers()['idempotency-key'], expectedHead: JSON.parse(request.postData() ?? '{}').expected_head ?? null, status: null, outcome: 'sent' };
    postOf.set(request, post);
    posts.push(post);
  });
  page.on('response', (response) => { const post = postOf.get(response.request()); if (post) post.status = response.status(); });
  page.on('requestfailed', (request) => { const post = postOf.get(request); if (post) post.outcome = 'lost'; });

  // Hold the acknowledgement, not the request: the Runtime commits the save, the page never hears back.
  let holding = true;
  const held: Array<{ route: Parameters<Parameters<Page['route']>[1]>[0]; post: Post }> = [];
  await page.route(SAVES, async (route) => {
    const request = route.request();
    if (!holding || request.method() !== 'POST') return route.fallback();
    const post = postOf.get(request)!;
    const response = await route.fetch();
    post.status = response.status();
    post.outcome = 'held';
    held.push({ route, post });
  });

  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  journey.facts.sameRealm = await expectSameRealm(page, harness, astrid);
  const baseHead = await currentHead(harness);
  const revisionsBefore = (await allRevisions(harness, seed3)).length;

  // A: the App renames the track. The Runtime commits it; the acknowledgement is held.
  await editFirstTrackName(page, 'F2 App A');
  await expect.poll(() => held.length, CEILING).toBe(1);
  expect(held[0].post.status, 'the Runtime committed A').toBe(200);
  expect(held[0].post.expectedHead).toBe(baseHead);
  const keyA = held[0].post.key;
  await expect.poll(() => currentHead(harness), CEILING).not.toBe(baseHead);
  const headA = await currentHead(harness);
  expect(headA, 'the App\'s save is stored under its idempotency key').toBe(keyA);

  // B: the agent builds on A and publishes (it extends one clip and clears another one's asset).
  await agent.checkout();
  const stateA = await revisionState(harness, seed3, headA);
  await agent.edit('--clip', seed3.agentClipId, '--extend', '1');
  await agent.edit('--clip', seed3.agentClearClipId, '--clear-asset');
  const published = await agent.publish('agent: extend and clear', 'f2-case2');
  expect(published.old_head, 'the agent built on the App\'s save').toBe(headA);
  const headB = published.new_head;
  expect(await currentHead(harness)).toBe(headB);

  // C: the App edits again while A is unacknowledged (it clears a transition).
  await setTransitionToNone(page, seed3.transitionClipId);

  // The acknowledgement is lost: the page sees a connection reset, and its own retry follows.
  holding = false;
  await held[0].route.abort('connectionreset');

  const conflict = page.getByRole('alertdialog', { name: CONFLICT_TITLE });
  await expect(conflict).toBeVisible(CEILING);
  await expect(conflict.getByText('Keep your changes, or switch to the latest version.')).toBeVisible();
  await expect(conflict.getByRole('button', { name: 'Keep my changes' })).toBeVisible();
  await expect(conflict.getByRole('button', { name: 'Use latest version' })).toBeVisible();
  await page.unroute(SAVES);

  // Which of the two ways to the conflict ran (recorded, not asserted).
  const afterRelease = posts.slice(1);
  const queuedEditPosted = afterRelease.find((post) => post.expectedHead === headA && post.key !== keyA);
  const branch = queuedEditPosted ? 'b: the receipt was accepted, the queued edit was posted on A and the Runtime answered 409 stale_head' : 'a: the provider refused the confirmed receipt after its cached head moved to B';
  test.info().annotations.push({ type: 'case-2-branch', description: branch });
  journey.facts = { ...journey.facts, verdict: 'named_conflict', branch, posts: posts.map(({ expectedHead, status, outcome }, index) => ({ n: index + 1, expectedHead: expectedHead === null ? null : expectedHead === baseHead ? 'base head' : expectedHead === headA ? 'A' : expectedHead, status, outcome, sameKeyAsA: posts[index].key === keyA })) };

  // The draft is kept: the dialog is modal, so the editor behind it is hidden from the accessibility tree but still holds A and C.
  await expect(page.getByRole('textbox', { name: 'Track name', includeHidden: true }).first()).toHaveValue('F2 App A');
  await expect(transitionSelect(page)).toContainText('None');

  // The Runtime head is B and holds A and B, and not C.
  expect(await currentHead(harness), 'nothing was published after B').toBe(headB);
  const stateB = await revisionState(harness, seed3, headB);
  expect(stateB.trackLabel, 'B holds the App\'s save A').toBe('F2 App A');
  expect(stateB.shotClips[seed3.agentClipId].hold, 'B holds the agent\'s extension').toBe(stateA.shotClips[seed3.agentClipId].hold + 1);
  expect(stateB.shotClips[seed3.agentClearClipId].asset, 'B holds the agent\'s clear').toBeUndefined();
  expect(stateA.shotClips[seed3.agentClearClipId].asset, 'A still had that asset').toBeTruthy();
  expect(stateB.parentClips[seed3.transitionClipId].transition, 'C was never published').toEqual(stateA.parentClips[seed3.transitionClipId].transition);
  expect(stateB.parentClips[seed3.transitionClipId].transition).toBeTruthy();

  // One publication per retried save: A was replayed under its own key and made exactly one revision; the agent's publication made one.
  const revisions = (await allRevisions(harness, seed3)).map((revision) => revision.revision_id);
  expect(revisions.length, 'two new revisions: A and B').toBe(revisionsBefore + 2);
  expect(new Set(revisions).size, 'no revision is stored twice').toBe(revisions.length);
  expect(revisions.filter((id) => id === keyA), 'A\'s key names exactly one revision').toHaveLength(1);
  expect(posts.filter((post) => post.key === keyA).length, 'A was replayed with the same key').toBeGreaterThanOrEqual(2);
  expect(posts.filter((post) => post.expectedHead === baseHead).every((post) => post.key === keyA), 'every send on the base head is A\'s').toBe(true);

  // Opaque data and clears, in every revision.
  await expectOpaqueDataKept(harness, seed3);

  // Both clients agree after a reload: the App reads head B and shows A; the agent reads B.
  const readsBeforeReload = watched.urls.length;
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await expect(firstTrackName(page)).toHaveValue(stateB.trackLabel!);
  await expect.poll(() => watched.urls.slice(readsBeforeReload).some((url) => url.includes(`/composition-revisions/${headB}`)), CEILING).toBe(true);
  await selectClip(page, seed3.transitionClipId);
  await expect(transitionSelect(page)).toContainText('crossfade');
  expect((await agent.status()).current_head).toBe(headB);
  const shown = await agent.show();
  expect(shown.head_revision_id).toBe(headB);
  const layers = shown.rows.flatMap((row) => row.layers);
  expect(layers.find((layer) => layer.clip_id === seed3.agentClearClipId)?.asset, 'the agent sees the clear').toBeNull();
  journey.facts.headB = headB;
  await sniff.expectClean(page);
});

// ---------------------------------------------------------------------------------------------
// 3. Runtime restart with both attached

test('Runtime restart with the App open: the draft survives, saves after the relaunch, and the agent follows', async ({ page, harness, astrid, seed3 }) => {
  const agent = agentOf(astrid, seed3);
  const sniff = new TokenSniff(secretsOf(harness, astrid));
  sniff.attach(page);

  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const before = await expectSameRealm(page, harness, astrid);
  const headBefore = await currentHead(harness);

  // A draft that was never sent: the save is held, so the edit is a draft by construction.
  const releaseSaves = await holdTimelineSaves(page);
  await editFirstTrackName(page, 'F2 kept across restart');
  await plantNoReloadFlag(page);

  // The Runtime restarts on a new port; the page says so and does not reload itself.
  await harness.restartRuntime();
  await expect(page.getByRole('heading', { name: 'Astrid restarted' })).toBeVisible(CEILING);
  expect(await noReloadFlag(page), 'the page does not reload by itself').toBe(true);

  // The agent follows discovery to the new endpoint: same realm and contract, a new instance, and the draft is not in the Runtime.
  const after = await astrid.identity();
  expect(after.realm_id).toBe(before.realmId);
  expect(after.runtime_instance_id, 'the agent reached the relaunched Runtime').toBe(harness.runtimeInstanceId);
  expect(after.runtime_instance_id).not.toBe(before.runtimeInstanceId);
  expect(after.schema_digest).toBe(before.schemaDigest);
  expect((await agent.status()).current_head, 'the draft is not saved').toBe(headBefore);
  expect(await currentHead(harness)).toBe(headBefore);

  // The page reconnects after Reload, offers the draft back, and saves it once the hold is released.
  await page.getByRole('button', { name: UI.reload }).click();
  await expectConnected(page);
  await expect(page.getByRole('heading', { name: 'Astrid restarted' })).toHaveCount(0);
  await openSeededTimeline(page, harness);
  journey.facts.sameRealmAfterRestart = await expectSameRealm(page, harness, astrid);
  const recovered = page.getByRole('alert').filter({ hasText: 'You have unsaved changes' });
  await expect(recovered).toBeVisible(CEILING);
  await releaseSaves();
  const recoveredSave = page.waitForRequest((request) => request.method() === 'POST' && SAVES.test(new URL(request.url()).pathname), CEILING);
  await recovered.getByRole('button', { name: 'Save them' }).click();
  const keyAfter = (await recoveredSave).headers()['idempotency-key'];
  await expect.poll(() => currentHead(harness), CEILING).not.toBe(headBefore);
  await expect(firstTrackName(page)).toHaveValue('F2 kept across restart');

  // The agent reads what the App saved after the relaunch.
  const headAfter = await currentHead(harness);
  expect((await agent.status()).current_head).toBe(headAfter);
  expect((await agent.show()).head_revision_id).toBe(headAfter);
  const state = await revisionState(harness, seed3, headAfter);
  expect(state.trackLabel, 'the saved revision is the draft').toBe('F2 kept across restart');
  expect(headAfter, 'the post-restart save is stored under its idempotency key').toBe(keyAfter);
  await expectOpaqueDataKept(harness, seed3);

  journey.facts = { ...journey.facts, instanceBefore: before.runtimeInstanceId, instanceAfter: after.runtime_instance_id, headBefore, headAfter };
  await sniff.expectClean(page);
});

// ---------------------------------------------------------------------------------------------
// QUICK: F1 owns the realm and Runtime; this case attaches the App and real Astrid CLI to that one timeline.

test('quick: Astrid edit then App edit are visible and readable on the adopted timeline', async ({ page, harness, quickAstrid }) => {
  const descriptor = harness.attachment;
  const seed = harness.quickSeed;
  expect(descriptor, 'the quick descriptor selected the attached harness').toBeTruthy();
  expect(seed, 'the adopted project and timeline are available').toBeTruthy();
  const quickSeed = { timelineId: seed!.timelineId, projectSlug: seed!.projectSlug };
  const agent = agentOf(quickAstrid, quickSeed);
  const sniff = new TokenSniff(secretsOf(harness, quickAstrid));
  sniff.attach(page);
  const reads = watchPageReads(page, harness);

  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const sameRealm = await expectSameRealm(page, harness, quickAstrid);
  expect(sameRealm.realmId).toBe(descriptor!.realmId);
  expect(sameRealm.runtimeInstanceId).toBe(descriptor!.runtimeInstanceId);
  expect(sameRealm.astridFile).toContain('astrid');

  const baseRevisionId = descriptor!.headRevisionId;
  const base = await revisionBody(harness, baseRevisionId);
  const clips = (base.payload.clips ?? []) as Array<Record<string, any>>;
  expect(clips.length, 'the fixture has an editable media clip').toBeGreaterThan(0);
  const clip = clips[0];
  const mediaId = base.payload.registry.assets[clip.asset].media_id as string;
  const mediaUrl = `${harness.gatewayBase}/v1/objects/${encodeURIComponent(mediaId)}`;
  const preview = page.getByTestId('video-editor-preview-surface');
  const decodedFrame = preview.locator('[data-preview-media-src]');
  // ReadinessVideo forwards this marker to the painted media element and reports its decoded source separately.
  const renderedClip = preview.locator('[data-astrid-retry-token]');
  await expect(decodedFrame, 'the preview contains the fixture media source').toHaveCount(1);
  await expect(decodedFrame).toHaveAttribute('data-preview-media-src', mediaUrl);
  await expect(decodedFrame, 'Chromium decoded the fixture media').toHaveAttribute('data-preview-decoded-frame', 'true');
  await expect(renderedClip, 'one fixture media surface is rendered').toHaveCount(1);
  await expect(renderedClip, 'the editor visibly renders the fixture media').toBeVisible();
  await expect(renderedClip).toHaveCSS('opacity', '1');

  await agent.checkout();
  await agent.edit('--clip', String(clip.id), '--set', 'opacity=0.5');
  const astridPublished = await agent.publish('Quick Astrid edit', `quick-astrid-${descriptor!.timelineId}`);
  expect(astridPublished.old_head).toBe(baseRevisionId);
  const astridRevisionId = astridPublished.new_head;
  await expect.poll(async () => (await currentHead(harness)), { message: 'the App observes Astrid’s published revision' }).toBe(astridRevisionId);
  await expect.poll(() => reads.compositionRevisions.some((item) => item.id === astridRevisionId && item.payload?.clips?.some((candidate: any) => candidate.id === clip.id && candidate.opacity === 0.5)), { message: 'the editor reads Astrid’s edited clip content' }).toBe(true);
  await expect(renderedClip, 'Astrid’s opacity edit is visible in the rendered editor').toHaveCSS('opacity', '0.5');

  const appLabel = 'QUICK App edit';
  const appSaved = page.waitForResponse((response) => response.request().method() === 'POST' && SAVES.test(new URL(response.url()).pathname), CEILING);
  await editFirstTrackName(page, appLabel);
  const saveResponse = await appSaved;
  expect(saveResponse.ok(), `App save returned ${saveResponse.status()}`).toBe(true);
  expect(saveResponse.request().postDataJSON().expected_head, 'the App built on Astrid’s revision').toBe(astridRevisionId);
  const saveEnvelope = await saveResponse.json();
  const savedRevisionId = saveEnvelope.data?.new_head as string;
  expect(savedRevisionId, 'the App response identifies its saved revision').toBeTruthy();
  expect(saveEnvelope.data?.old_head, 'the App save receipt names Astrid’s revision as its parent').toBe(astridRevisionId);
  expect(savedRevisionId).not.toBe(astridRevisionId);
  expect(await currentHead(harness)).toBe(savedRevisionId);

  const status = await agent.status();
  const show = await agent.show();
  expect(status.current_head, 'Astrid reads the App-saved revision').toBe(savedRevisionId);
  expect(show.head_revision_id).toBe(savedRevisionId);
  const lineage = (await allRevisions(harness, quickSeed)).map((revision) => revision.revision_id);
  expect(lineage.indexOf(savedRevisionId), 'the App revision is the newest ancestor').toBeGreaterThanOrEqual(0);
  expect(lineage.indexOf(savedRevisionId)).toBeLessThan(lineage.indexOf(astridRevisionId));
  expect(lineage.indexOf(astridRevisionId)).toBeLessThan(lineage.indexOf(baseRevisionId));
  const astridRead = await quickAstrid.readTimelineBundle(seed!.timelineId, seed!.projectSlug, savedRevisionId);
  expect(astridRead.revisionId, 'Astrid opened the App-saved immutable revision').toBe(savedRevisionId);
  const composition = astridRead.bundle.parent as Record<string, any>;
  const labels = (composition.config.tracks as Array<Record<string, any>>).map((track) => track.label);
  expect(labels, 'Astrid reads the App-edited track label as content').toContain(appLabel);

  const revisions = revisionSet(journey.identity);
  const observedRevisions = { app: revisions.appHead, astrid: revisions.astridHead, runtime: revisions.runtimeHead };
  expect(observedRevisions).toEqual(descriptor!.revisions);
  const result = {
    realmId: sameRealm.realmId,
    runtimeInstanceId: sameRealm.runtimeInstanceId,
    baseRevisionId,
    astridRevisionId,
    savedRevisionId,
    astridParentRevisionId: astridPublished.old_head,
    appParentRevisionId: saveEnvelope.data.old_head as string,
    astridLabel: 'Quick Astrid edit',
    appLabel,
    revisions: observedRevisions,
  };
  mkdirSync(path.dirname(descriptor!.resultFile), { recursive: true });
  writeFileSync(descriptor!.resultFile, JSON.stringify(result, null, 2));
  journey.facts = { ...journey.facts, ...result };
  await sniff.expectClean(page);
});
