/** P1: the mounted App's local split -> trim chain through the durable v2 save session. */
import { expect, type Page, type Route } from '@playwright/test';
import { randomUUID } from 'node:crypto';
import type { CommitRequest } from '../../../src/integrations/runtime/timeline-commit-types.ts';
import { APP_ENTRY_ROUTE, commandOutboxes, expectConnected, firstTrackName, test as appTest } from './support/app.ts';
import { ASTRID_PYTHON, AstridCli } from './support/astrid.ts';
import { compositionPublication, harnessUnavailableReason, type DirectHarness } from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_WRITES = /\/timelines\/[^/]+\/composition-revisions$/;
const SOURCE_ID = 'p1-chain-source';
const SPLIT_AT = 2;

type ChainSeed = { projectSlug: string; timelineId: string; sourceId: string };
type CommitPost = { body: CommitRequest; raw: string; key: string; status?: number; response?: any };

const test = appTest.extend<object, { astrid: AstridCli }>({
  astrid: async ({ harness }, use) => {
    const client = await AstridCli.create(harness);
    await client.preflight();
    await use(client);
  },
});
test.beforeAll(() => {
  const reason = harnessUnavailableReason();
  if (reason) throw new Error(`P1 chain cannot run: ${reason}`);
});

function pin(result: any) {
  return { revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id };
}

function parentOf(result: any) {
  return result.data.canonical_document.parent_revision.payload;
}

function assertV2Request(post: CommitPost, harness: DirectHarness, seed: ChainSeed) {
  const body = post.body as any;
  expect(body).toMatchObject({
    api_version: 1,
    project_id: harness.seed.projectId,
    timeline_id: seed.timelineId,
    base_revision_id: expect.any(String),
    base_publication_id: expect.any(String),
    commands: expect.any(Array),
    label: expect.any(String),
    steps: expect.any(Array),
    merge: expect.stringMatching(/^(fields|atomic)$/),
    dry_run: false,
  });
  for (const step of body.steps) {
    expect(step).toMatchObject({ id: expect.any(String), label: expect.any(String), intent: expect.any(String),
      tags: expect.any(Array), command_ordinals: expect.any(Array), patch: expect.any(Array) });
    if ('reads' in step) expect(step.reads).toEqual(expect.any(Array));
  }
  if ('reads' in body) expect(body.reads).toEqual(expect.any(Array));
  expect(post.key).toBeTruthy();
}

function assertAcceptedData(result: any, post: CommitPost, status: 'accepted' | 'merged') {
  expect(result).toMatchObject({ data: { status, canonical_document: expect.any(Object), document_digest: expect.any(String),
    commands: expect.any(Array), id_map: expect.any(Object), provider_version: expect.any(String),
    compiler_version: expect.any(String), merge_mode: expect.stringMatching(/^(fields|atomic)$/), steps: expect.any(Array) },
    receipt: { receipt_id: expect.any(String), idempotency_key: post.key, request_hash: expect.any(String) } });
  expect(result.data).not.toHaveProperty('dependencies');
  expect(result.data.steps).toEqual(expect.any(Array));
  for (const step of result.data.steps) expect(step).toMatchObject({ id: expect.any(String), label: expect.any(String),
    intent: expect.any(String), tags: expect.any(Array), command_ordinals: expect.any(Array), patch: expect.any(Array), dependencies: expect.any(Array) });
  expect(result.receipt.result).toEqual(result.data);
}

async function seedOneClip(harness: DirectHarness): Promise<ChainSeed> {
  const timelineId = randomUUID();
  const publication = compositionPublication({ projectId: harness.seed.projectId, timelineId }, null, 'P1 chain', 30);
  const clip = {
    id: SOURCE_ID, at: 0, track: 'V1', clipType: 'media', asset: 'p1-video', from: 0, to: 8, speed: 1, hold: 8,
    app: { opaque: { keep: null, ordered: [false, 0, ''] }, astrid: { for: 8 }, 'org.example': { literal: SOURCE_ID, clear: null } },
  };
  const parent = publication.parent_composition as Record<string, any>;
  parent.config = { ...parent.config, clips: [clip], opaque: { root: null, order: [0, false] } };
  parent.clips = [clip];
  parent.registry = { assets: {
    'p1-video': { file: harness.seed.video.mediaType === 'video/webm' ? 'p1-video.webm' : 'p1-video.mp4',
      type: harness.seed.video.mediaType, duration: 8, media_id: harness.seed.video.objectId, content_sha256: harness.seed.video.digest },
  } };
  const published = await harness.runtimeJson('POST', `/v1/projects/${harness.seed.projectId}/timelines/${timelineId}/composition-revisions`, publication);
  expect(published.status, JSON.stringify(published.body)).toBe(200);
  const project = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}`);
  return { projectSlug: (project.body.data ?? project.body).slug, timelineId, sourceId: SOURCE_ID };
}

async function history(harness: DirectHarness, seed: ChainSeed) {
  const result = await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  expect(result.status, JSON.stringify(result.body)).toBe(200);
  return result.body;
}

function observe(page: Page) {
  const posts: CommitPost[] = [];
  const legacy: string[] = [];
  page.on('request', (request) => {
    if (request.method() !== 'POST') return;
    const path = new URL(request.url()).pathname;
    if (COMMITS.test(path)) posts.push({ body: JSON.parse(request.postData() ?? '{}'), raw: request.postData() ?? '', key: request.headers()['idempotency-key'] });
    if (LEGACY_WRITES.test(path)) legacy.push(path);
  });
  page.on('response', (response) => {
    if (!COMMITS.test(new URL(response.url()).pathname)) return;
    const post = [...posts].reverse().find((candidate) => candidate.key === response.request().headers()['idempotency-key']);
    if (!post) return;
    post.status = response.status();
    void response.json().then((body) => { post.response = body; }).catch(() => {});
  });
  return { posts, legacy };
}

async function openChain(page: Page, harness: DirectHarness, seed: ChainSeed) {
  const runtimeResponses: RuntimeDiagnosticResponse[] = [];
  const pageErrors: DiagnosticErrorSignal[] = [];
  const consoleErrors: DiagnosticErrorSignal[] = [];
  page.on('response', (response) => {
    const method = diagnosticMethod(response.request().method());
    const status = diagnosticStatus(response.status());
    let route: DiagnosticRoute | undefined;
    try { route = diagnosticRoute(new URL(response.url()).pathname); } catch { return; }
    if (method && status !== undefined && route) boundedPush(runtimeResponses, { method, route, status });
  });
  page.on('pageerror', (error) => boundedPush(pageErrors, classifyDiagnosticError(error.message)));
  page.on('console', (message) => {
    if (message.type() === 'error') boundedPush(consoleErrors, classifyDiagnosticError(message.text()));
  });
  try {
    await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}?localProject=${encodeURIComponent(seed.projectSlug)}&localTimeline=${encodeURIComponent(seed.timelineId)}`);
    await expectConnected(page);
    await expect(firstTrackName(page)).toBeVisible();
    await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).some((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  } catch (error) {
    await openChainDiagnostics(page, seed.timelineId, runtimeResponses, pageErrors, consoleErrors);
    throw error;
  }
}

async function setPlayhead(page: Page, seconds: number) {
  const ruler = page.getByTestId('timeline-ruler');
  const labels = ruler.locator('[data-testid="timeline-ruler-labels"] span');
  const marks = await labels.evaluateAll((nodes) => nodes.map((node) => ({ text: node.textContent?.trim() ?? '', box: node.getBoundingClientRect().toJSON() })));
  const parsed = marks.map((mark) => {
    const match = mark.text.match(/^(\d+):(\d\d)\.(\d\d)$/);
    return match ? { seconds: Number(match[1]) * 60 + Number(match[2]) + Number(match[3]) / 100, box: mark.box } : null;
  }).filter((mark): mark is { seconds: number; box: DOMRect } => mark !== null);
  const zero = parsed.find((mark) => mark.seconds === 0);
  const anchor = parsed.find((mark) => mark.seconds > 0);
  expect(zero, 'the real timeline ruler must expose a zero-time anchor').toBeTruthy();
  expect(anchor, 'the real timeline ruler must expose a second time anchor').toBeTruthy();
  const pixelsPerSecond = (anchor!.box.x - zero!.box.x) / anchor!.seconds;
  await page.mouse.click(zero!.box.x - 6 + seconds * pixelsPerSecond, (await ruler.boundingBox())!.y + 15);
}

async function splitSource(page: Page, seed: ChainSeed) {
  await page.locator(`.clip-action[data-clip-id="${seed.sourceId}"]`).click();
  await setPlayhead(page, SPLIT_AT);
  await page.keyboard.press('s');
}

async function trimSourceWindow(page: Page, clipId: string, value: string) {
  await page.locator(`.clip-action[data-clip-id="${clipId}"]`).click();
  await page.getByRole('tab', { name: 'Timing', exact: true }).click();
  // The current product renders FieldLabel and NumberInput in one normal DOM container;
  // keep the same Source In intent without requiring an accessibility patch in this proof.
  const field = page.getByText('Source In', { exact: true }).locator('..');
  await expect(field).toBeVisible();
  const input = field.locator('input:not([aria-hidden="true"])');
  await expect(input).toBeEditable();
  await input.fill(value);
  await input.press('Enter');
  await input.press('Tab');
}

async function forward(route: Route, response: any, body: any) {
  await route.fulfill({ status: response.status(), headers: response.headers(), body: JSON.stringify(body) });
}

const DIAGNOSTIC_LIMIT = 40;
const DIAGNOSTIC_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'] as const;
type DiagnosticMethod = typeof DIAGNOSTIC_METHODS[number];
type DiagnosticRoute =
  | '/api/runtime/v1/health' | '/api/runtime/v1/realm' | '/api/runtime/v1/handshake'
  | '/api/runtime/v1/projects' | '/api/runtime/v1/projects/:project'
  | '/api/runtime/v1/projects/:project/timelines'
  | '/api/runtime/v1/projects/:project/timelines/:timeline'
  | '/api/runtime/v1/projects/:project/timelines/:timeline/commits'
  | '/api/runtime/v1/projects/:project/timelines/:timeline/inspect'
  | '/api/runtime/v1/projects/:project/timelines/:timeline/commit'
  | '/api/astrid/v1/health' | '/api/astrid/v1/realm' | '/api/astrid/v1/handshake'
  | '/api/astrid/v1/projects' | '/api/astrid/v1/projects/:project'
  | '/api/astrid/v1/projects/:project/timelines'
  | '/api/astrid/v1/projects/:project/timelines/:timeline'
  | '/api/astrid/v1/projects/:project/timelines/:timeline/commits'
  | '/api/astrid/v1/projects/:project/timelines/:timeline/inspect'
  | '/api/astrid/v1/projects/:project/timelines/:timeline/commit'
  | '/runtime-config/v1/workspace.json' | '/runtime-config/v1/operation/:handle';
type DiagnosticErrorSignal =
  | 'failed_to_fetch' | 'network_error' | 'connection_refused' | 'runtime_unavailable'
  | 'operation_unavailable' | 'paired_connector_error' | 'no_proxy_on_hosted_origin' | 'unknown';
type DiagnosticConnectionState =
  | 'connected' | 'stopped' | 'restarted' | 'connecting' | 'phone' | 'permission'
  | 'pending' | 'blocked' | 'set_up' | 'update_needed' | 'unknown';

type DiagnosticRuntimeResponse = { method: DiagnosticMethod; route: DiagnosticRoute; status: number };

const DIAGNOSTIC_ERROR_LABELS: ReadonlyArray<[DiagnosticErrorSignal, string]> = [
  ['failed_to_fetch', 'failed to fetch'],
  ['network_error', 'network error'],
  ['connection_refused', 'connection refused'],
  ['runtime_unavailable', 'runtime unavailable'],
  ['operation_unavailable', 'operation_unavailable'],
  ['paired_connector_error', 'paired_connector_error'],
  ['no_proxy_on_hosted_origin', 'no_proxy_on_hosted_origin'],
];

const DIAGNOSTIC_CONNECTION_STATES: readonly DiagnosticConnectionState[] = [
  'connected', 'stopped', 'restarted', 'connecting', 'phone', 'permission', 'pending', 'blocked', 'set_up', 'update_needed', 'unknown',
];

const DIAGNOSTIC_ROUTE_TEMPLATES: ReadonlyArray<[RegExp, string]> = [
  [/^\/v1\/health$/, '/v1/health'],
  [/^\/v1\/realm$/, '/v1/realm'],
  [/^\/v1\/handshake$/, '/v1/handshake'],
  [/^\/v1\/projects$/, '/v1/projects'],
  [/^\/v1\/projects\/[^/]+$/, '/v1/projects/:project'],
  [/^\/v1\/projects\/[^/]+\/timelines$/, '/v1/projects/:project/timelines'],
  [/^\/v1\/projects\/[^/]+\/timelines\/[^/]+$/, '/v1/projects/:project/timelines/:timeline'],
  [/^\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commits$/, '/v1/projects/:project/timelines/:timeline/commits'],
  [/^\/v1\/projects\/[^/]+\/timelines\/[^/]+\/inspect$/, '/v1/projects/:project/timelines/:timeline/inspect'],
  [/^\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/, '/v1/projects/:project/timelines/:timeline/commit'],
];

function boundedPush<T>(items: T[], item: T) {
  if (items.length < DIAGNOSTIC_LIMIT) items.push(item);
}

function diagnosticMethod(value: string): DiagnosticMethod | undefined {
  return (DIAGNOSTIC_METHODS as readonly string[]).includes(value) ? value as DiagnosticMethod : undefined;
}

function diagnosticStatus(value: number): number | undefined {
  return Number.isInteger(value) && value >= 100 && value <= 599 ? value : undefined;
}

function diagnosticRoute(pathname: string): DiagnosticRoute | undefined {
  if (pathname === '/runtime-config/v1/workspace.json') return pathname;
  if (pathname.startsWith('/runtime-config/v1/operation/')) return '/runtime-config/v1/operation/:handle';
  const prefix = pathname.startsWith('/api/runtime/') ? '/api/runtime' : pathname.startsWith('/api/astrid/') ? '/api/astrid' : undefined;
  if (!prefix) return undefined;
  const suffix = pathname.slice(prefix.length);
  const template = DIAGNOSTIC_ROUTE_TEMPLATES.find(([pattern]) => pattern.test(suffix))?.[1];
  return template ? `${prefix}${template}` as DiagnosticRoute : undefined;
}

function classifyDiagnosticError(value: string): DiagnosticErrorSignal {
  const normalized = value.toLowerCase();
  return DIAGNOSTIC_ERROR_LABELS.find(([, phrase]) => normalized.includes(phrase))?.[0] ?? 'unknown';
}

function diagnosticConnectionState(value: string | null): DiagnosticConnectionState {
  return (DIAGNOSTIC_CONNECTION_STATES as readonly string[]).includes(value ?? '') ? value as DiagnosticConnectionState : 'unknown';
}

function summarizeOutboxes(records: any[]) {
  const observed = records.slice(0, DIAGNOSTIC_LIMIT);
  const intentLengths = observed.map((record) => Array.isArray(record.intents) ? record.intents.length : 0);
  const pendingIntentLengths = observed.map((record) => record.pending ? 1 : 0);
  const outcomeKinds = observed
    .map((record) => record.pending?.outcome?.kind)
    .filter((kind): kind is 'accepted' | 'rejected' | 'retry' => kind === 'accepted' || kind === 'rejected' || kind === 'retry');
  return {
    ownerCount: records.length,
    intentLengths,
    pendingIntentLengths,
    outcomeKinds,
    hasIdleOwner: records.some((record) => !record.pending && Array.isArray(record.intents) && record.intents.length === 0),
    hasPending: records.some((record) => !!record.pending),
    hasIntents: intentLengths.some((length) => length > 0),
    hasConflict: records.some((record) => record.intents?.some((intent: any) => intent.conflict !== undefined)),
  };
}

async function visibleDiagnostic(locator: { isVisible(): Promise<boolean> }) {
  try {
    return await locator.isVisible();
  } catch {
    return false;
  }
}

async function openChainDiagnostics(
  page: Page,
  timelineId: string,
  runtimeResponses: DiagnosticRuntimeResponse[],
  pageErrors: DiagnosticErrorSignal[],
  consoleErrors: DiagnosticErrorSignal[],
) {
  let outboxSummary: ReturnType<typeof summarizeOutboxes> | null = null;
  let outboxReadFailed = false;
  try {
    outboxSummary = summarizeOutboxes(await commandOutboxes(page, timelineId));
  } catch {
    outboxReadFailed = true;
  }
  const connection = page.getByTestId('runtime-connection-status');
  const runtimePanel = page.getByTestId('runtime-not-connected');
  const recovery = page.getByTestId('timeline-command-recovery');
  const timelineError = page.locator('[data-video-editor-timeline-error="true"]');
  const provider = page.getByTestId('video-editor-provider');
  const connectionState = await connection.getAttribute('data-state').catch(() => null);
  const panelState = await runtimePanel.getAttribute('data-state').catch(() => null);
  const selectedTimelineId = await provider.getAttribute('data-timeline-id').catch(() => null);
  const alertCount = await page.locator('[role="alert"]:visible').count().catch(() => 0);
  console.log(`[P1 openChain diagnostics] ${JSON.stringify({
    outboxReadFailed,
    outboxes: outboxSummary,
    ui: {
      selectedTimelineMatchesExpectedId: selectedTimelineId === timelineId,
      connectionState: diagnosticConnectionState(connectionState ?? panelState),
      runtimePanelVisible: await visibleDiagnostic(runtimePanel),
      recoveryVisible: await visibleDiagnostic(recovery),
      timelineErrorVisible: await visibleDiagnostic(timelineError),
      alertCount,
    },
    runtimeResponses,
    errorSignals: {
      page: { count: pageErrors.length, known: pageErrors.filter((signal) => signal !== 'unknown') },
      console: { count: consoleErrors.length, known: consoleErrors.filter((signal) => signal !== 'unknown') },
    },
  })}`);
}

// Source proof only: execution is NOT READY until A2 supplies its existing authoritative
// read/intent seam. The strict merged reply assertions below remain required; do not infer
// reads or reinterpret this boundary as a refusal.
test('P1 split -> trim new clip: accepted split, merged trim after Agent edit, lost ACK restart and exact retry', async ({ page, harness, astrid }) => {
  const seed = await seedOneClip(harness);
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const traffic = observe(page);
  let heldSplit: Route | undefined;
  let heldTrim: Route | undefined;
  await page.route(COMMITS, async (route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    const post = traffic.posts.find((candidate) => candidate.key === route.request().headers()['idempotency-key']);
    if (post && traffic.posts.indexOf(post) === 0) { heldSplit = route; return; }
    if (post && traffic.posts.indexOf(post) === 1) { heldTrim = route; return; }
    const response = await route.fetch({ maxRetries: 0 });
    await forward(route, response, await response.json());
  });
  await openChain(page, harness, seed);
  const before = await history(harness, seed);
  const original = (await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${before.head.revision_id}`)).body.payload;
  expect(original.clips).toHaveLength(1);
  const originalClip = structuredClone(original.clips[0]);
  await splitSource(page, seed);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
  await expect.poll(() => !!heldSplit, CEILING).toBe(true);
  const split = traffic.posts[0];
  assertV2Request(split, harness, seed);
  const splitCommand = split.body.commands[0] as any;
  expect(splitCommand).toMatchObject({ schema_version: 1, op: 'doc.patch', version: '1', select: null });
  const inserted = (splitCommand.args.changes as Array<any>).find((change) => change.op === 'list.insert' && change.path.join('.') === 'clips');
  expect(inserted).toMatchObject({ before: { state: 'absent' }, value: { id: expect.any(String), clipType: 'media', track: 'V1' },
    order_before: [SOURCE_ID], after_id: SOURCE_ID });
  expect(inserted.id).toMatch(/^p1-chain-source-/);
  expect(inserted.value.id).toBe(inserted.id);
  expect(splitCommand.created).toEqual([`parent/clip:${inserted.id}`]);
  const rightId = inserted.id;
  expect(split.body).toMatchObject({ api_version: 1, project_id: harness.seed.projectId, timeline_id: seed.timelineId,
    base_revision_id: before.head.revision_id, base_publication_id: before.head.publication_id,
    source: { via: 'app' }, merge: 'fields', dry_run: false, label: expect.any(String), commands: [splitCommand] });
  expect(split.body.steps[0]).toMatchObject({ command_ordinals: [0], patch: splitCommand.args.changes });

  // Release only after the dependent has been authored locally. The outbox must persist it
  // behind the held split instead of sending it with a guessed base or a new ID.
  await trimSourceWindow(page, rightId, '3');
  await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
  expect((await commandOutboxes(page, seed.timelineId)).some((owner) => owner.pending && owner.intents.length > 0)).toBe(true);
  const splitWire = await heldSplit!.fetch({ maxRetries: 0 });
  split.response = await splitWire.json(); split.status = splitWire.status();
  await forward(heldSplit!, splitWire, split.response);
  assertAcceptedData(split.response, split, 'accepted');
  expect(split.response.data.rebased_onto).toBeNull();
  const splitDocument = parentOf(split.response);
  expect(splitDocument.clips.map((clip: any) => clip.id)).toEqual([SOURCE_ID, rightId]);
  // This seed is a hold clip in the current App. Its UI split changes hold/at/ID only;
  // it does not manufacture a source-window split or strip the authored app state.
  expect(splitDocument.clips[0]).toEqual({ ...originalClip, hold: SPLIT_AT });
  expect(splitDocument.clips[1]).toEqual({ ...originalClip, id: rightId, at: SPLIT_AT, hold: originalClip.hold - SPLIT_AT });
  expect(splitDocument.config.opaque).toEqual({ root: null, order: [0, false] });
  expect(splitDocument.config.clips).toEqual(splitDocument.clips);
  expect(split.response.data.steps[0].patch).toEqual(expect.arrayContaining([expect.objectContaining({ op: 'list.insert', id: rightId,
    value: expect.objectContaining({ id: rightId }), before: { state: 'absent' }, order_before: [SOURCE_ID], after_id: SOURCE_ID })]));
  expect(splitDocument.registry).toEqual((await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${split.response.data.accepted_revision_id}`)).body.payload.registry);

  await expect.poll(() => traffic.posts.length, CEILING).toBe(2);
  const trim = traffic.posts[1];
  await expect.poll(() => !!heldTrim, CEILING).toBe(true);
  assertV2Request(trim, harness, seed);
  expect(trim.status).toBeUndefined();
  expect(trim.body.steps[0]).toMatchObject({ command_ordinals: [0], patch: (trim.body.commands[0] as any).args.changes });
  expect(trim.body.commands[0]).toMatchObject({ op: 'doc.patch', select: null });
  const trimChange = (trim.body.commands[0] as any).args.changes.find((change: any) => change.path.includes(`id:${rightId}`) && change.path.at(-1) === 'from');
  expect(trimChange).toMatchObject({ value: 3, before: { state: 'present', value: SPLIT_AT }, path: ['clips', `id:${rightId}`, 'from'] });
  expect(trim.body.base_revision_id).toBe(split.response.data.accepted_revision_id);
  expect(trim.body.base_publication_id).toBe(split.response.receipt.receipt_id);

  const agent = await astrid.commitCaptured(harness.seed.projectId, seed.timelineId, pin(split.response), { kind: 'label', trackId: 'V1', label: 'Agent edit after split' }, 'p1-agent-after-split');
  expect(agent.data.status).toBe('accepted');
  expect(agent.data.rebased_onto).toBeNull();
  const originalTrim = { raw: trim.raw, key: trim.key };
  const acceptedTrimResponse = await heldTrim!.fetch({ maxRetries: 0 });
  const acceptedTrim = await acceptedTrimResponse.json();
  expect(acceptedTrimResponse.status()).toBe(200);
  assertAcceptedData(acceptedTrim, trim, 'merged');
  expect(acceptedTrim.data.rebased_onto).toEqual(pin(agent));
  const mergedDocument = parentOf(acceptedTrim);
  expect(mergedDocument.clips.map((clip: any) => clip.id)).toEqual([SOURCE_ID, rightId]);
  expect(mergedDocument.clips[0]).toMatchObject({ id: SOURCE_ID, from: originalClip.from, to: originalClip.to, hold: SPLIT_AT });
  expect(mergedDocument.clips[1]).toMatchObject({ id: rightId, at: SPLIT_AT, from: 3, to: originalClip.to, hold: originalClip.to - 3 });
  expect(mergedDocument.config.clips).toEqual(mergedDocument.clips);
  expect(mergedDocument.clips[0].app).toEqual(originalClip.app);
  expect(mergedDocument.clips[1].app.opaque).toEqual(originalClip.app.opaque);
  expect(mergedDocument.clips[1].app['org.example']).toEqual(originalClip.app['org.example']);
  expect(mergedDocument.clips[1].app['org.example']).toHaveProperty('clear', null);
  expect(mergedDocument.clips[1].app).not.toHaveProperty('astrid');
  expect(mergedDocument.registry).toEqual(splitDocument.registry);
  expect(mergedDocument.occurrences).toEqual(splitDocument.occurrences);
  expect(acceptedTrim.data.canonical_document.shot_revisions).toEqual(split.response.data.canonical_document.shot_revisions);
  expect(acceptedTrim.data.canonical_document.internal_timeline_revisions).toEqual(split.response.data.canonical_document.internal_timeline_revisions);
  expect(mergedDocument.config.tracks).toEqual(expect.arrayContaining([expect.objectContaining({ id: 'V1', label: 'Agent edit after split' })]));
  await heldTrim!.abort('connectionreset');
  await page.unroute(COMMITS);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).some((owner) => owner.pending?.outcome?.kind === 'retry'), CEILING).toBe(true);
  const owner = (await commandOutboxes(page, seed.timelineId)).find((candidate) => candidate.pending?.request.key === originalTrim.key)!;
  expect(owner.pending?.request).toMatchObject({ body: originalTrim.raw, key: originalTrim.key });
  await page.reload();
  await expectConnected(page);
  await expect(firstTrackName(page)).toBeVisible();
  expect(traffic.posts).toHaveLength(2);
  const restarted = await harness.restartRuntime();
  expect(restarted.oldInstanceId).toBeTruthy();
  await expectConnected(page);
  const recovered = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: /^Recover saved edits/ }).and(page.locator(`[data-owner-id="${owner.ownerId}"]`)).click();
  const retryResponse = await recovered;
  expect(retryResponse.status()).toBe(200);
  expect(retryResponse.request().postData()).toBe(originalTrim.raw);
  expect(retryResponse.request().headers()['idempotency-key']).toBe(originalTrim.key);
  const retry = await retryResponse.json();
  expect(retry).toEqual(acceptedTrim);
  expect(retry.data.status).toBe('merged');
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  expect(traffic.legacy).toEqual([]);
  const final = (await history(harness, seed)).items;
  expect(final).toHaveLength(before.items.length + 3);
  expect(final.filter((item: any) => item.receipt?.idempotency_key === originalTrim.key)).toHaveLength(1);
});

test('P1 split -> trim new clip: a real Agent move refuses the stale trim and the App rolls back with a message', async ({ page, harness, astrid }) => {
  const seed = await seedOneClip(harness);
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const traffic = observe(page);
  await openChain(page, harness, seed);
  const before = await history(harness, seed);
  const original = (await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${before.head.revision_id}`)).body.payload;
  const originalClip = structuredClone(original.clips[0]);
  await splitSource(page, seed);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
  await expect.poll(() => traffic.posts[0].response, CEILING).not.toBeUndefined();
  const split = traffic.posts[0];
  assertV2Request(split, harness, seed);
  const splitDocument = parentOf(split.response);
  const inserted = (split.body.commands[0] as any).args.changes.find((change: any) => change.op === 'list.insert');
  expect(inserted.value.id).toBe(inserted.id);
  expect(inserted.order_before).toEqual([SOURCE_ID]);
  expect(inserted.after_id).toBe(SOURCE_ID);
  const rightId = inserted.id;
  const agent = await astrid.commitCaptured(harness.seed.projectId, seed.timelineId, pin(split.response), { kind: 'move', clipId: rightId, on: 3 }, 'p1-agent-conflict');
  expect(agent.data.status).toBe('accepted');
  expect(agent.data.rebased_onto).toBeNull();
  const agentParent = parentOf(agent);
  // Preserve the exact split baseline for fields the native move did not intend to change.
  expect(agentParent.clips[0]).toEqual(splitDocument.clips[0]);
  expect(agentParent.clips[1]).toMatchObject({ id: rightId, at: 3, from: originalClip.from, to: originalClip.to, hold: originalClip.to - SPLIT_AT });
  expect(agentParent.clips[1].app).toEqual({ ...splitDocument.clips[1].app,
    astrid: { fixed_start: true, for: originalClip.to - SPLIT_AT } });
  await trimSourceWindow(page, rightId, '3');
  await expect.poll(() => traffic.posts.length, CEILING).toBe(2);
  await expect.poll(() => traffic.posts[1].status, CEILING).not.toBeUndefined();
  expect(traffic.posts[1].status).toBe(409);
  expect(traffic.posts[1].response.details).toMatchObject({ status: 'conflict', reason: expect.any(String),
    current: pin(agent), conflicts: expect.any(Array) });
  expect(traffic.posts[1].response.details.conflicts.length).toBeGreaterThan(0);
  for (const conflict of traffic.posts[1].response.details.conflicts) {
    expect(conflict).toMatchObject({ kind: expect.any(String), ref: expect.any(String), path: expect.any(Array),
      base: expect.any(Object), theirs: expect.any(Object), ours: expect.any(Object), choices: expect.any(Array) });
    for (const token of conflict.path) expect(token).toEqual(expect.any(String));
    for (const state of [conflict.base, conflict.theirs, conflict.ours]) {
      if (state.state === 'present') expect(state).toHaveProperty('value');
      else expect(state).toEqual({ state: 'absent' });
    }
  }
  // C0c normalizes the atomic touched scope to the parent payload root,
  // rather than a native parent/clip alias or the clips/config.clips mirror.
  expect(traffic.posts[1].response.details.conflicts).toEqual(expect.arrayContaining([
    expect.objectContaining({ kind: 'atomic_scope_changed', ref: 'parent', path: [] }),
  ]));
  expect(traffic.posts[1].response.details.path).toEqual([]);
  await expect(page.getByTestId('timeline-command-recovery')).toContainText('Your changes are retained and need resolution before they can be saved.');
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).find((owner) => owner.pending)?.pending?.outcome?.kind, CEILING).toBe('rejected');
  const current = await history(harness, seed);
  expect(current.items).toHaveLength(before.items.length + 2);
  expect(current.head).toEqual(pin(agent));
  const currentRevision = (await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${current.head.revision_id}`)).body;
  const currentParent = currentRevision.payload;
  // The refused trim must leave the complete canonical parent/closure equal to the
  // actual accepted Agent baseline; do not reconstruct a guessed move result here.
  expect(currentRevision).toMatchObject({ revision_id: agent.data.canonical_document.parent_revision.revision_id,
    content_digest: agent.data.canonical_document.parent_revision.content_digest,
    payload: agentParent, dependency_manifest: agent.data.canonical_document.dependency_manifest });
  expect(agent.data.canonical_document.shot_revisions).toEqual([]);
  expect(agent.data.canonical_document.internal_timeline_revisions).toEqual([]);
  expect(currentParent.clips.map((clip: any) => clip.id)).toEqual([SOURCE_ID, rightId]);
  expect(currentParent.clips[0]).toEqual(agentParent.clips[0]);
  expect(currentParent.clips[1]).toEqual(agentParent.clips[1]);
  expect(currentParent.clips[0].app.opaque).toEqual(currentParent.clips[1].app.opaque);
  expect(currentParent.clips[0].app['org.example']).toEqual(currentParent.clips[1].app['org.example']);
  expect(currentParent.clips[0].app.astrid).toEqual(splitDocument.clips[0].app.astrid);
  expect(currentParent.clips[1].app.astrid).toEqual({ fixed_start: true, for: originalClip.to - SPLIT_AT });
  expect(currentParent.config.clips).toEqual(currentParent.clips);
  expect(traffic.legacy).toEqual([]);
});
