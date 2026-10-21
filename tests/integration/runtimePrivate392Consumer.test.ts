import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { afterEach, describe, expect, it } from 'vitest';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import type { CommitRequest, Transport } from '@/integrations/runtime/generated.ts';
import { buildTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { compileTimelinePatch } from '@/tools/video-editor/lib/timeline-patch.ts';
import { createCommitOutbox, type OutboxScope } from '@/tools/video-editor/commands/commitOutbox.ts';
import { createTimelineCommandSession, type TimelineCommandSession } from '@/tools/video-editor/commands/commitSession.ts';
import { authoringBundleFromDocument } from '@/tools/video-editor/commands/authoringBundle.ts';
import { captureProjectDataMember } from '@/tools/video-editor/commands/projectDataMember.ts';
import { buildVisualSeamProjectDataPatch, VISUAL_SEAM_PROJECT_DATA_TARGET } from '@/tools/video-editor/commands/visualSeamProjectDataMember.ts';
import type { TimelineConfig } from '@/tools/video-editor/types/index.ts';
import { ASTRID_CHECKOUT, ASTRID_PYTHON } from '../e2e/local/support/astrid.ts';
import {
  DirectHarness,
  PRODUCT_ACTOR,
  RUNTIME_CHECKOUT,
  compositionPublication,
  harnessUnavailableReason,
} from '../e2e/local/support/harness.ts';

const RUNTIME_COMMIT = 'f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414';
const AGENT_PIN = '1303ce6be32e7bd96ed5c6b35afcb15819e81b50';
const AGENT_SOURCE = 'e010e6a3868e963471244491bb6672c3e4a5135e';
const AGENT_SCHEMA = 'sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d';
const RUNTIME_ARTIFACTS = 'sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d';
const RUNTIME_SCHEMA = 'sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042';
const target = 'com.example.private392';
const settingsKey = '__dsl__:dsl://com.example.private392/main.json';

type WireEntry = {
  method: string;
  path: string;
  headers: Record<string, string>;
  body?: CommitRequest;
  status: number;
  response: unknown;
};

function gitHead(checkout: string): string {
  return execFileSync('git', ['-C', checkout, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
}

function gitRef(checkout: string, ref: string): string {
  return execFileSync('git', ['-C', checkout, 'rev-parse', ref], { encoding: 'utf8' }).trim();
}

function sha256(data: Uint8Array): string {
  return `sha256:${createHash('sha256').update(data).digest('hex')}`;
}

function exactIdentityPrerequisite(): string | null {
  const base = harnessUnavailableReason();
  if (base) return base;
  if (!existsSync(path.join(ASTRID_CHECKOUT, 'astrid', 'core', 'timeline', 'schema', 'edit-command.schema.json'))) {
    return `Agent schema source is missing under ${ASTRID_CHECKOUT}`;
  }
  return null;
}

function assertExactIdentity(): void {
  expect(gitHead(RUNTIME_CHECKOUT), 'Runtime checkout').toBe(RUNTIME_COMMIT);
  expect(gitHead(ASTRID_CHECKOUT), 'Agent normal private pin').toBe(AGENT_PIN);
  expect(gitRef(ASTRID_CHECKOUT, `${AGENT_PIN}^`), 'Agent e010 source parent').toBe(AGENT_SOURCE);
  expect(sha256(readFileSync(path.join(ASTRID_CHECKOUT, 'astrid', 'core', 'timeline', 'schema', 'edit-command.schema.json'))),
    'Agent e010/schema392 source').toBe(AGENT_SCHEMA);
  const appLock = JSON.parse(readFileSync(path.resolve('runtime.lock.json'), 'utf8')) as {
    producer_version?: string;
    source_commit?: string;
  };
  expect(appLock.source_commit, 'App Runtime source pin').toBe(RUNTIME_COMMIT);
  expect(appLock.producer_version, 'App Runtime artifact manifest').toBe(RUNTIME_ARTIFACTS);
  expect(RUNTIME_SCHEMA_DIGEST, 'App Runtime schema').toBe(RUNTIME_SCHEMA);
}

function bytes(body?: Uint8Array | Blob): Promise<Buffer | undefined> {
  if (!body) return Promise.resolve(undefined);
  if (body instanceof Blob) return body.arrayBuffer().then((value) => Buffer.from(value));
  return Promise.resolve(Buffer.from(body));
}

function doorTransport(harness: DirectHarness, wire: WireEntry[], loseFirstCommit = false): Transport {
  let lose = loseFirstCommit;
  return async (method, requestPath, headers, body) => {
    const requestBytes = await bytes(body);
    const response = await harness.doorRequest(requestPath, {
      method,
      headers,
      body: requestBytes,
    });
    const entry: WireEntry = {
      method,
      path: requestPath,
      headers: { ...headers },
      body: requestBytes ? JSON.parse(requestBytes.toString('utf8')) as CommitRequest : undefined,
      status: response.status,
      response: response.json(),
    };
    wire.push(entry);
    if (lose && requestPath.endsWith('/commit') && response.status < 500) {
      lose = false;
      throw new Error('lost acknowledgement after Runtime accepted the request');
    }
    return { status: response.status, headers: {}, body: new Uint8Array(response.body) };
  };
}

function runtimeTransport(harness: DirectHarness, token: string, wire: WireEntry[]): Transport {
  return async (method, requestPath, headers, body) => {
    const requestBytes = await bytes(body);
    const response = await fetch(`${harness.runtimeUrl}${requestPath}`, {
      method,
      headers: { ...headers, Authorization: `Bearer ${token}` },
      body: requestBytes,
    });
    const responseBytes = new Uint8Array(await response.arrayBuffer());
    const text = new TextDecoder().decode(responseBytes);
    wire.push({
      method,
      path: requestPath,
      headers: { ...headers },
      body: requestBytes ? JSON.parse(requestBytes.toString('utf8')) as CommitRequest : undefined,
      status: response.status,
      response: text ? JSON.parse(text) : null,
    });
    return { status: response.status, headers: {}, body: responseBytes };
  };
}

type SessionDriver = {
  provider: RuntimeDataProvider;
  session: TimelineCommandSession;
  current: () => TimelineData;
};

async function makeSession(options: {
  provider: RuntimeDataProvider;
  basis: Awaited<ReturnType<RuntimeDataProvider['loadTimelineCommandBasis']>>;
  scope: OutboxScope;
  outboxes: ReturnType<typeof createCommitOutbox>;
}): Promise<SessionDriver> {
  const { basis, provider, scope, outboxes } = options;
  const timelineId = scope.timelineId;
  const build = (next: typeof basis): Promise<TimelineData> => {
    const parent = next.canonicalDocument.parent_revision.payload;
    return buildTimelineData(parent.config as never, parent.registry as never, undefined, 1, undefined, {
      projectId: scope.projectId,
      timelineId,
      headRevisionId: next.head.revisionId,
      headPublicationId: next.head.publicationId,
    });
  };
  let current = await build(basis);
  const preview = (patch: TimelinePatch) => {
    const compiled = compileTimelinePatch(patch, current);
    if (!compiled.valid || !compiled.nextData) throw new Error('private392 preview compilation failed');
    current = compiled.nextData;
  };
  const session = await createTimelineCommandSession({
    initial: basis,
    scope,
    outboxes,
    loadLatest: () => provider.loadTimelineCommandBasis(timelineId),
    send: (request, key) => provider.commitTimeline(request, key),
    preview,
    project: async (next, previews) => {
      current = await build(next);
      previews.forEach(preview);
    },
    changed: () => {},
  });
  return { provider, session, current: () => current };
}

function patch(...operations: TimelinePatch['operations']): TimelinePatch {
  return { version: 1, operations };
}

async function waitFor<T>(read: () => T, predicate: (value: T) => boolean, label: string): Promise<T> {
  const deadline = Date.now() + 20_000;
  let value = read();
  while (!predicate(value) && Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, 10));
    value = read();
  }
  if (!predicate(value)) throw new Error(`Timed out waiting for ${label}`);
  return value;
}

describe('private392 App consumer through the real Runtime Door', () => {
  let harness: DirectHarness | undefined;

  afterEach(async () => {
    await harness?.stop();
    harness = undefined;
  });

  it('sends App-captured project data through Runtime f8da with durable retry, rebase, and undo', async () => {
    const prerequisite = exactIdentityPrerequisite();
    if (prerequisite) throw new Error(`private392 live prerequisite unavailable: ${prerequisite}`);
    assertExactIdentity();

    harness = await new DirectHarness().start({ seed: false });
    const project = await harness.runtimeJson('POST', '/v1/projects', { name: 'private392 consumer' });
    expect(project.status).toBe(201);
    const projectId = project.body.data.project_id as string;
    const timelineId = crypto.randomUUID();
    const seeded = await harness.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`,
      compositionPublication({ projectId, timelineId }, null, 'private392', 30));
    expect(seeded.status).toBe(200);
    await harness.enableTimelineAuthoring(ASTRID_PYTHON);

    const health = await fetch(`${harness.runtimeUrl}/v1/health`, { headers: { Authorization: `Bearer ${harness.productToken}` } });
    const healthBody = await health.json() as { protocol?: string; schema_digest?: string; runtime_instance_id?: string };
    expect(healthBody).toMatchObject({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA, runtime_instance_id: harness.runtimeInstanceId });

    const primaryWire: WireEntry[] = [];
    const primaryProvider = new RuntimeDataProvider({
      projectId,
      baseUrl: harness.doorBase,
      transport: doorTransport(harness, primaryWire, true),
    });
    const primaryScope: OutboxScope = { projectId, timelineId, realmId: harness.realmId, actorId: PRODUCT_ACTOR };
    const primaryOutboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (_key, work) => work() });
    const initial = await primaryProvider.loadTimelineCommandBasis(timelineId);
    expect(initial.canonicalDocument.parent_revision.payload.config.app).toBeUndefined();
    const first = await makeSession({ provider: primaryProvider, basis: initial, scope: primaryScope, outboxes: primaryOutboxes });

    const firstPatch = patch(
      { op: 'project-data.write', target, payload: { key: settingsKey, value: {
        keep: true, opaque: { nullish: null, disabled: false, ordered: [null, false, 'opaque'] },
      }, mode: 'merge' }, order: 1 },
      { op: 'project-data.write', target, payload: { key: settingsKey, value: { nested: { first: true } }, mode: 'merge' }, order: 2 },
      { op: 'project-data.write', target, payload: { key: 'replacement', value: { fresh: true }, mode: 'replace' }, order: 3 },
    );
    const captured = first.session.genericPatchPort.capture({ patch: firstPatch, current: first.current() });
    const prepared = first.session.genericPatchPort.finish(captured);
    expect(prepared.commands.map((command) => command.op)).toEqual(['project-data.write', 'project-data.write', 'project-data.write']);
    expect(prepared.commands[0].args).toMatchObject({ target, key: settingsKey, mode: 'replace' });
    expect(prepared.commands[0].expect).toMatchObject({
      'parent::config.app': { state: 'absent' },
      [`parent::config.app[${JSON.stringify(target)}]`]: { state: 'absent' },
    });
    first.session.genericPatchPort.submit(prepared);
    await waitFor(() => primaryWire.filter((entry) => entry.path.endsWith('/commit')).length, (count) => count === 1, 'first Runtime commit');
    const lostRequest = primaryWire.find((entry) => entry.path.endsWith('/commit'))!;
    await first.session.dispose();

    const owners = await primaryOutboxes.list(primaryScope);
    expect(owners).toHaveLength(1);
    expect(owners[0].pending?.outcome?.kind).toBe('retry');
    const reloadedProvider = new RuntimeDataProvider({
      projectId,
      baseUrl: harness.doorBase,
      transport: doorTransport(harness, primaryWire),
    });
    const reloaded = await makeSession({
      provider: reloadedProvider,
      basis: await reloadedProvider.loadTimelineCommandBasis(timelineId),
      scope: primaryScope,
      outboxes: primaryOutboxes,
    });
    await reloaded.session.recover(owners[0].ownerId);
    await reloaded.session.flush();
    const commitRequests = primaryWire.filter((entry) => entry.path.endsWith('/commit'));
    expect(commitRequests).toHaveLength(2);
    expect(commitRequests[1].body).toEqual(commitRequests[0].body);
    expect(commitRequests[1].headers['Idempotency-Key']).toBe(lostRequest.headers['Idempotency-Key']);
    expect((commitRequests[1].response as { data?: { status?: string } }).data?.status).toBe('accepted');
    const afterFirst = await reloadedProvider.loadTimelineCommandBasis(timelineId);
    const appAfterFirst = afterFirst.canonicalDocument.parent_revision.payload.config.app as Record<string, unknown>;
    expect(appAfterFirst[target]).toEqual({
      [settingsKey]: { keep: true, opaque: { nullish: null, disabled: false, ordered: [null, false, 'opaque'] }, nested: { first: true } },
      replacement: { fresh: true },
    });

    const disjointWire: WireEntry[] = [];
    const remoteToken = await harness.provisionCredential('private392-remote', 'private392-remote.json');
    const remoteProvider = new RuntimeDataProvider({
      projectId,
      baseUrl: harness.runtimeUrl,
      token: remoteToken,
      transport: runtimeTransport(harness, remoteToken, disjointWire),
    });
    const remoteScope: OutboxScope = { projectId, timelineId, realmId: harness.realmId, actorId: 'private392-remote' };
    const remoteOutboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (_key, work) => work() });
    const remote = await makeSession({
      provider: remoteProvider,
      basis: await remoteProvider.loadTimelineCommandBasis(timelineId),
      scope: remoteScope,
      outboxes: remoteOutboxes,
    });
    const disjoint = reloaded.session.genericPatchPort.capture({ patch: patch({
      op: 'project-data.write', target, payload: { key: settingsKey, value: { nested: { second: true } }, mode: 'merge' },
    }), current: reloaded.current() });
    const disjointPrepared = reloaded.session.genericPatchPort.finish(disjoint);
    const remoteWrite = remote.session.genericPatchPort.capture({ patch: patch({
      op: 'project-data.write', target, payload: { key: 'remote', value: { preserved: [null, false, 'opaque'] }, mode: 'replace' },
    }), current: remote.current() });
    remote.session.genericPatchPort.submit(remote.session.genericPatchPort.finish(remoteWrite));
    await remote.session.flush();
    reloaded.session.genericPatchPort.submit(disjointPrepared);
    await reloaded.session.flush();
    const rebased = primaryWire.filter((entry) => entry.path.endsWith('/commit')).at(-1);
    expect(rebased?.body?.base_revision_id).toBe(afterFirst.head.revisionId);
    expect((rebased?.response as { data?: { status?: string } }).data?.status).toBe('rebased');
    const afterRebase = await reloadedProvider.loadTimelineCommandBasis(timelineId);
    const appAfterRebase = afterRebase.canonicalDocument.parent_revision.payload.config.app as Record<string, unknown>;
    expect(appAfterRebase[target]).toMatchObject({
      remote: { preserved: [null, false, 'opaque'] },
      [settingsKey]: { nested: { second: true } },
    });

    await reloaded.session.undo();
    const afterUndo = await reloadedProvider.loadTimelineCommandBasis(timelineId);
    const appAfterUndo = afterUndo.canonicalDocument.parent_revision.payload.config.app as Record<string, unknown>;
    expect(appAfterUndo[target]).toEqual({
      [settingsKey]: { keep: true, opaque: { nullish: null, disabled: false, ordered: [null, false, 'opaque'] }, nested: { first: true } },
      replacement: { fresh: true },
      remote: { preserved: [null, false, 'opaque'] },
    });

    const stale = reloaded.session.genericPatchPort.capture({ patch: patch({
      op: 'project-data.write', target, payload: { key: settingsKey, value: { stale: true }, mode: 'replace' },
    }), current: reloaded.current() });
    const stalePrepared = reloaded.session.genericPatchPort.finish(stale);
    await remote.session.dispose();
    const latestRemoteProvider = new RuntimeDataProvider({
      projectId,
      baseUrl: harness.runtimeUrl,
      token: remoteToken,
      transport: runtimeTransport(harness, remoteToken, disjointWire),
    });
    const latestRemote = await makeSession({
      provider: latestRemoteProvider,
      basis: await latestRemoteProvider.loadTimelineCommandBasis(timelineId),
      scope: remoteScope,
      outboxes: remoteOutboxes,
    });
    const remoteStale = latestRemote.session.genericPatchPort.capture({ patch: patch({
      op: 'project-data.write', target, payload: { key: settingsKey, value: { changed: 'elsewhere' }, mode: 'replace' },
    }), current: latestRemote.current() });
    latestRemote.session.genericPatchPort.submit(latestRemote.session.genericPatchPort.finish(remoteStale));
    await latestRemote.session.flush();
    const historyBeforeStale = (await latestRemoteProvider.loadTimelineCommandBasis(timelineId)).head;
    reloaded.session.genericPatchPort.submit(stalePrepared);
    await waitFor(() => reloaded.session.getState().status, (status) => status === 'conflict', 'stale Runtime refusal');
    expect((await latestRemoteProvider.loadTimelineCommandBasis(timelineId)).head).toEqual(historyBeforeStale);
    await reloaded.session.useLatest();

    const allPrimaryPosts = primaryWire.filter((entry) => entry.method === 'POST');
    expect(allPrimaryPosts.filter((entry) => entry.path !== '/v1/handshake' && !entry.path.endsWith('/commit'))).toEqual([]);
    expect(disjointWire.filter((entry) => entry.method === 'POST' && entry.path !== '/v1/handshake' && !entry.path.endsWith('/commit'))).toEqual([]);
    expect(primaryWire.filter((entry) => entry.path.endsWith('/commit')).some((entry) => entry.status === 409)).toBe(true);
    await latestRemote.session.dispose();
    await reloaded.session.dispose();
  });

  it('accepts the dormant visual seam member through the same private392 Door and guarded native undo', async () => {
    const prerequisite = exactIdentityPrerequisite();
    if (prerequisite) throw new Error(`private392 live prerequisite unavailable: ${prerequisite}`);
    assertExactIdentity();

    harness = await new DirectHarness().start({ seed: false });
    const project = await harness.runtimeJson('POST', '/v1/projects', { name: 'private392 visual seam' });
    expect(project.status).toBe(201);
    const projectId = project.body.data.project_id as string;
    const timelineId = crypto.randomUUID();
    const storedReport = { version: 1, blocked: true, opaque: { source: 'legacy' } };
    const originalContract = {
      report: storedReport,
      mode: 'enforced',
      opaqueSibling: { retained: [null, false, 'opaque'] },
      intents: { '90': 'synchronized' },
    };
    const publication = compositionPublication({ projectId, timelineId }, null, 'private392 visual seam', 30);
    Object.assign(publication.parent_composition.config, {
      app: { visualSeamContract: originalContract },
    });
    const seeded = await harness.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, publication);
    expect(seeded.status).toBe(200);
    await harness.enableTimelineAuthoring(ASTRID_PYTHON);

    const wire: WireEntry[] = [];
    const provider = new RuntimeDataProvider({
      projectId,
      baseUrl: harness.doorBase,
      transport: doorTransport(harness, wire),
    });
    const initial = await provider.loadTimelineCommandBasis(timelineId);
    const currentConfig = initial.canonicalDocument.parent_revision.payload.config as unknown as TimelineConfig;
    const initialContract = currentConfig.app!.visualSeamContract as Record<string, unknown>;
    const initialContractOrder = Object.keys(initialContract);
    const acknowledgedConfig = structuredClone(currentConfig);
    const acknowledgedApp = acknowledgedConfig.app as Record<string, unknown>;
    const acknowledgedContract = acknowledgedApp.visualSeamContract as Record<string, unknown>;
    const nextIntents = { '90': 'synchronized', '120': 'hard-cut' };
    acknowledgedContract.intents = nextIntents;
    acknowledgedContract.report = { version: 2, blocked: false, derived: true };

    const seamPatch = buildVisualSeamProjectDataPatch(currentConfig, acknowledgedConfig);
    expect(seamPatch).toEqual({
      version: 1,
      source: 'visual-seam',
      operations: [{
        op: 'project-data.write',
        target: VISUAL_SEAM_PROJECT_DATA_TARGET,
        payload: { key: 'intents', value: nextIntents, mode: 'replace' },
        order: 0,
      }],
    });
    const captured = captureProjectDataMember(await authoringBundleFromDocument(initial.canonicalDocument), seamPatch!);
    expect(captured.commands).toHaveLength(1);
    expect(captured.commands[0].args).toEqual({
      target: VISUAL_SEAM_PROJECT_DATA_TARGET,
      key: 'intents',
      value: nextIntents,
      mode: 'replace',
    });
    expect(captured.commands[0].expect).toEqual({
      'parent::config.app.visualSeamContract.intents': { state: 'present', value: { '90': 'synchronized' } },
    });

    const accepted = await provider.commitTimeline({
      api_version: 1,
      project_id: projectId,
      timeline_id: timelineId,
      base_revision_id: initial.head.revisionId,
      base_publication_id: initial.head.publicationId,
      commands: captured.commands as CommitRequest['commands'],
      source: { via: 'app', detail: 'private392 dormant visual seam' },
    }, `private392-seam-${crypto.randomUUID()}`);
    expect(accepted.response.data.status).toBe('accepted');

    const saved = await provider.loadTimelineCommandBasis(timelineId);
    const savedContract = (saved.canonicalDocument.parent_revision.payload.config as unknown as TimelineConfig)
      .app!.visualSeamContract as Record<string, unknown>;
    expect(savedContract).toEqual({
      report: storedReport,
      mode: 'enforced',
      opaqueSibling: { retained: [null, false, 'opaque'] },
      intents: nextIntents,
    });
    expect(Object.keys(savedContract)).toEqual(initialContractOrder);
    expect(savedContract).not.toHaveProperty('absentSibling');

    const undone = await provider.undoTimeline({
      projectId,
      timelineId,
      headRevisionId: saved.head.revisionId,
      headPublicationId: saved.head.publicationId,
    }, [accepted.accepted.publicationId], `private392-seam-undo-${crypto.randomUUID()}`);
    expect(undone.response.data.status).toBe('accepted');
    const restored = await provider.loadTimelineCommandBasis(timelineId);
    const restoredContract = (restored.canonicalDocument.parent_revision.payload.config as unknown as TimelineConfig)
      .app!.visualSeamContract as Record<string, unknown>;
    expect(restoredContract).toEqual(originalContract);
    expect(Object.keys(restoredContract)).toEqual(initialContractOrder);
    expect(wire.filter((entry) => entry.path.endsWith('/commit'))).toHaveLength(2);
  });
});
