/**
 * Source-stage coverage for the unsafe legacy headless-shell bootstrap.
 *
 * The current direct harness cannot create this fixture through a supported
 * Runtime API: timeline-document creation is retired and public timeline reads
 * intentionally omit the legacy config/registry.  The central qualification
 * run supplies a test-only native fixture adapter through
 * ASTRID_APP_HEADLESS_FIXTURE_MODULE.  The adapter seeds and reads the exact
 * legacy bytes; it is not a browser route, product endpoint, or compatibility
 * writer.  Keeping the seam here makes the missing owner capability explicit.
 */
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { expect, type Page } from '@playwright/test';
import {
  APP_ENTRY_ROUTE,
  test as appTest,
} from './support/app.ts';
import {
  PRODUCT_ACTOR,
  REPO_ROOT,
  RUNTIME_CHECKOUT,
  type DirectHarness,
} from './support/harness.ts';

const COMPOSITION_PUBLICATION = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/composition-revisions$/;
const COMMIT = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const PROJECT_PATCH = /\/v1\/projects\/[^/]+$/;
const FIRST_TIMELINE_BUTTON = { name: 'Create first timeline', exact: true };

type JsonObject = Record<string, unknown>;

interface LegacySnapshot {
  config: JsonObject;
  registry: JsonObject;
  clips: unknown[];
}

interface HeadlessFixture {
  projectId: string;
  projectSlug: string;
  timelineId: string;
  timelineName: string;
  /** The native fixture authority's exact authored bytes before the page opens. */
  original: LegacySnapshot;
  editedClipId: string;
  opaqueRootKeys: string[];
}

interface FixtureSetupArgs {
  runtimeUrl: string;
  productToken: string;
  appHead: string;
  runtimeHead: string;
  schemaDigest: string;
}

interface FixtureReadArgs extends FixtureSetupArgs {
  projectId: string;
  timelineId: string;
}

interface HeadlessFixtureAdapter {
  prepareNonemptyHeadless(args: FixtureSetupArgs): Promise<HeadlessFixture>;
  prepareEmptyHeadless(args: FixtureSetupArgs): Promise<HeadlessFixture>;
  readLegacy(args: FixtureReadArgs): Promise<LegacySnapshot>;
}

interface RuntimeErrorBody {
  error: {
    code: string;
    message: string;
    details: JsonObject;
  };
}

interface SourcePins {
  appHead: string;
  runtimeHead: string;
  schemaDigest: string;
}

function requiredEnv(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) {
    throw new Error(
      `headless bootstrap safety requires ${name}; do not qualify against an unpinned App/Runtime pair`,
    );
  }
  return value;
}

function sourcePins(): SourcePins {
  return {
    appHead: requiredEnv('ASTRID_APP_EXPECTED_HEAD'),
    runtimeHead: requiredEnv('ASTRID_RUNTIME_EXPECTED_HEAD'),
    schemaDigest: requiredEnv('ASTRID_RUNTIME_EXPECTED_SCHEMA_DIGEST'),
  };
}

function checkoutHead(checkout: string): string {
  return execFileSync('git', ['-C', checkout, 'rev-parse', 'HEAD'], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

async function loadFixtureAdapter(): Promise<HeadlessFixtureAdapter> {
  const modulePath = process.env.ASTRID_APP_HEADLESS_FIXTURE_MODULE?.trim();
  if (!modulePath) {
    throw new Error(
      'headless bootstrap safety is blocked: set ASTRID_APP_HEADLESS_FIXTURE_MODULE to the owner-supplied native historical fixture adapter; the shared harness cannot represent a nonempty headless shell',
    );
  }
  const loaded = (await import(pathToFileURL(modulePath).href)) as {
    default?: Partial<HeadlessFixtureAdapter>;
  } & Partial<HeadlessFixtureAdapter>;
  const adapter = loaded.default ?? loaded;
  for (const method of ['prepareNonemptyHeadless', 'prepareEmptyHeadless', 'readLegacy'] as const) {
    if (typeof adapter[method] !== 'function') {
      throw new Error(`headless fixture adapter must export ${method}()`);
    }
  }
  return adapter as HeadlessFixtureAdapter;
}

function setupArgs(harness: DirectHarness, pins: SourcePins): FixtureSetupArgs {
  return {
    runtimeUrl: harness.runtimeUrl,
    productToken: harness.productToken,
    appHead: pins.appHead,
    runtimeHead: pins.runtimeHead,
    schemaDigest: pins.schemaDigest,
  };
}

function projectUrl(harness: DirectHarness, projectSlug: string): string {
  return `${harness.origin}${APP_ENTRY_ROUTE}?localProject=${encodeURIComponent(projectSlug)}`;
}

async function openProject(page: Page, harness: DirectHarness, projectSlug: string): Promise<void> {
  await page.goto(projectUrl(harness, projectSlug));
}

async function publicTimeline(harness: DirectHarness, fixture: Pick<HeadlessFixture, 'projectId' | 'timelineId'>) {
  return harness.runtimeJson('GET', `/v1/projects/${fixture.projectId}/timelines/${fixture.timelineId}`);
}

async function projectState(harness: DirectHarness, fixture: Pick<HeadlessFixture, 'projectId'>) {
  return harness.runtimeJson('GET', `/v1/projects/${fixture.projectId}`);
}

async function compositionHistory(harness: DirectHarness, fixture: Pick<HeadlessFixture, 'projectId' | 'timelineId'>) {
  return harness.runtimeJson(
    'GET',
    `/v1/projects/${fixture.projectId}/timelines/${fixture.timelineId}/composition-revisions?limit=50`,
  );
}

async function timelineHistory(harness: DirectHarness, fixture: Pick<HeadlessFixture, 'timelineId'>) {
  return harness.runtimeJson('GET', `/v1/timelines/${fixture.timelineId}/history?limit=100`);
}

function fixtureArgs(harness: DirectHarness, pins: SourcePins): FixtureSetupArgs {
  return setupArgs(harness, pins);
}

function assertLegacyFixtureShape(fixture: HeadlessFixture, snapshot: LegacySnapshot): void {
  expect(snapshot.clips, 'the fixture contains authored clip arrays').toEqual(fixture.original.clips);
  expect(snapshot.clips.some((clip) => (
    clip && typeof clip === 'object' && (clip as JsonObject).id === fixture.editedClipId
  )), 'the fixture contains a real edited clip').toBe(true);
  for (const key of fixture.opaqueRootKeys) {
    expect(Object.prototype.hasOwnProperty.call(snapshot.config, key), `config keeps own opaque root ${key}`).toBe(true);
  }
  expect(Object.prototype.hasOwnProperty.call(snapshot.config, '__proto__'), 'config keeps an own __proto__ root').toBe(true);
  expect(snapshot.config.nullRoot, 'config keeps the explicit null root').toBeNull();
  expect(snapshot.config.prototype, 'config keeps the prototype root').toEqual(fixture.original.config.prototype);
}

function acceptedWrite(entry: ReturnType<DirectHarness['audit']>[number]): boolean {
  return entry.status >= 200 && entry.status < 300 && (
    COMPOSITION_PUBLICATION.test(entry.path)
    || COMMIT.test(entry.path)
    || PROJECT_PATCH.test(entry.path) && entry.method === 'PATCH'
  );
}

async function expectVisibleRefusal(
  page: Page,
  action: () => Promise<void>,
): Promise<{ status: number; error: RuntimeErrorBody['error'] }> {
  const responsePromise = page.waitForResponse((response) => (
    response.request().method() === 'POST' && COMPOSITION_PUBLICATION.test(new URL(response.url()).pathname)
  ));
  await action();
  const response = await responsePromise;
  const body = (await response.json()) as Partial<RuntimeErrorBody>;
  expect(response.status(), 'the unsafe bootstrap publication is refused').toBeGreaterThanOrEqual(400);
  expect(body.error).toEqual({
    code: expect.any(String),
    message: expect.any(String),
    details: expect.any(Object),
  });
  const error = body.error!;
  const detail = `${response.status()} ${error.code}: ${error.message.replace(/[\r\n]+/g, ' ').slice(0, 120)}`;
  await expect(page.getByRole('alert').filter({ hasText: 'Timeline setup failed' })).toContainText(
    `Timeline setup failed (${detail})`,
  );
  return { status: response.status(), error };
}

async function assertUnchanged(
  harness: DirectHarness,
  adapter: HeadlessFixtureAdapter,
  args: FixtureReadArgs,
  fixture: HeadlessFixture,
  before: { project: unknown; publicTimeline: unknown; composition: unknown; timeline: unknown; legacy: LegacySnapshot },
): Promise<void> {
  const afterProject = await projectState(harness, fixture);
  const afterPublic = await publicTimeline(harness, fixture);
  const afterComposition = await compositionHistory(harness, fixture);
  const afterTimeline = await timelineHistory(harness, fixture);
  const afterLegacy = await adapter.readLegacy(args);
  expect(afterProject.body).toEqual(before.project);
  expect(afterPublic.body).toEqual(before.publicTimeline);
  expect(afterComposition.body).toEqual(before.composition);
  expect(afterTimeline.body).toEqual(before.timeline);
  expect(afterLegacy).toEqual(before.legacy);
  expect(afterLegacy.clips).toEqual(fixture.original.clips);
  expect(afterLegacy.config).toEqual(fixture.original.config);
  expect(afterLegacy.registry).toEqual(fixture.original.registry);
}

const test = appTest.extend<{
  pins: SourcePins;
  fixtureAdapter: HeadlessFixtureAdapter;
}>({
  pins: [async ({ harness }, use) => {
    const pins = sourcePins();
    expect(checkoutHead(REPO_ROOT)).toBe(pins.appHead);
    expect(checkoutHead(RUNTIME_CHECKOUT)).toBe(pins.runtimeHead);
    const health = await harness.runtimeJson('GET', '/v1/health');
    expect(health.body).toMatchObject({ schema_digest: pins.schemaDigest, protocol: 'workspace.v1' });
    const handshake = await harness.runtimeJson('GET', '/v1/handshake');
    expect(handshake.body).toMatchObject({
      actor_id: PRODUCT_ACTOR,
      realm_id: harness.realmId,
      schema_digest: pins.schemaDigest,
      protocol: 'workspace.v1',
    });
    await use(pins);
  }, { scope: 'worker' }],
  // Playwright needs the empty destructuring pattern to make this a worker fixture.
  // eslint-disable-next-line no-empty-pattern
  fixtureAdapter: [async ({}, use) => use(await loadFixtureAdapter()), { scope: 'worker' }],
});

test.describe('headless bootstrap safety', () => {
  test('refuses a nonempty historical headless Main with a visible Runtime error and no write', async ({ harness, page, pins, fixtureAdapter }) => {
    const fixture = await fixtureAdapter.prepareNonemptyHeadless(fixtureArgs(harness, pins));
    const readArgs = { ...fixtureArgs(harness, pins), projectId: fixture.projectId, timelineId: fixture.timelineId };
    const originalLegacy = await fixtureAdapter.readLegacy(readArgs);
    assertLegacyFixtureShape(fixture, originalLegacy);
    const before = {
      project: (await projectState(harness, fixture)).body,
      publicTimeline: (await publicTimeline(harness, fixture)).body,
      composition: (await compositionHistory(harness, fixture)).body,
      timeline: (await timelineHistory(harness, fixture)).body,
      legacy: originalLegacy,
    };
    expect((before.publicTimeline as JsonObject).head_revision_id).toBeNull();
    expect((before.publicTimeline as JsonObject).head_publication_id).toBeNull();
    expect(before.composition).toMatchObject({ items: [] });
    expect(before.publicTimeline).not.toHaveProperty('config');
    expect(before.publicTimeline).not.toHaveProperty('registry');
    const auditAtStart = harness.audit().length;

    await openProject(page, harness, fixture.projectSlug);
    const firstRefusal = await expectVisibleRefusal(page, async () => {
      await page.getByRole('button', FIRST_TIMELINE_BUTTON).click();
    });
    const firstWrites = harness.audit().slice(auditAtStart);
    expect(firstWrites.filter(acceptedWrite), 'no publication, commit, or metadata write is accepted').toEqual([]);
    await assertUnchanged(harness, fixtureAdapter, readArgs, fixture, before);

    const retry = await expectVisibleRefusal(page, async () => {
      await page.getByRole('button', FIRST_TIMELINE_BUTTON).click();
    });
    expect(retry).toEqual(firstRefusal);
    await assertUnchanged(harness, fixtureAdapter, readArgs, fixture, before);

    const reloadRefusal = page.waitForResponse((response) => (
      response.request().method() === 'POST' && COMPOSITION_PUBLICATION.test(new URL(response.url()).pathname)
    ));
    await page.reload();
    const reloadResponse = await reloadRefusal;
    expect(reloadResponse.status()).toBeGreaterThanOrEqual(400);
    const reloadBody = (await reloadResponse.json()) as Partial<RuntimeErrorBody>;
    expect(reloadBody.error).toEqual(firstRefusal.error);
    const reloadDetail = `${reloadResponse.status()} ${reloadBody.error!.code}: ${reloadBody.error!.message.replace(/[\r\n]+/g, ' ').slice(0, 120)}`;
    await expect(page.getByRole('alert').filter({ hasText: 'Timeline setup failed' })).toContainText(
      `Timeline setup failed (${reloadDetail})`,
    );
    await assertUnchanged(harness, fixtureAdapter, readArgs, fixture, before);
    expect(harness.audit().slice(auditAtStart).filter(acceptedWrite), 'no refusal attempt accepted a write').toEqual([]);
    expect((await publicTimeline(harness, fixture)).body).toEqual(before.publicTimeline);
  });

  test('retains genuine empty headless repair as a positive requirement', async ({ harness, page, pins, fixtureAdapter }) => {
    const fixture = await fixtureAdapter.prepareEmptyHeadless(fixtureArgs(harness, pins));
    const readArgs = { ...fixtureArgs(harness, pins), projectId: fixture.projectId, timelineId: fixture.timelineId };
    const before = await publicTimeline(harness, fixture);
    const emptyLegacy = await fixtureAdapter.readLegacy(readArgs);
    expect(emptyLegacy).toEqual(fixture.original);
    expect(emptyLegacy.config).toEqual({});
    expect(emptyLegacy.registry).toEqual({});
    expect(emptyLegacy.clips).toEqual([]);
    expect(before.body).toMatchObject({ head_revision_id: null, head_publication_id: null });
    const acceptedPublication = page.waitForResponse((response) => (
      response.request().method() === 'POST' && COMPOSITION_PUBLICATION.test(new URL(response.url()).pathname)
    ));
    await openProject(page, harness, fixture.projectSlug);
    const response = await acceptedPublication;
    expect(response.status()).toBeGreaterThanOrEqual(200);
    expect(response.status()).toBeLessThan(300);
    const after = await publicTimeline(harness, fixture);
    expect(after.body).toMatchObject({ timeline_id: fixture.timelineId });
    expect((after.body as JsonObject).head_revision_id).toEqual(expect.any(String));
    expect(await fixtureAdapter.readLegacy(readArgs)).toEqual(fixture.original);
  });

  test('retains fresh project creation as a positive requirement', async ({ harness, page }) => {
    const project = await harness.runtimeJson('POST', '/v1/projects', { name: 'Fresh bootstrap positive' });
    expect(project.status).toBe(201);
    const projectData = project.body.data as JsonObject;
    const projectId = projectData.project_id as string;
    const projectSlug = projectData.slug as string;
    await openProject(page, harness, projectSlug);
    const timelines = await harness.runtimeJson('GET', `/v1/projects/${projectId}/timelines`);
    expect(timelines.body.items).toHaveLength(1);
    expect((timelines.body.items[0] as JsonObject).head_revision_id).toEqual(expect.any(String));
  });
});
