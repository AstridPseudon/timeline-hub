import { expect, test } from '@playwright/test';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { chromium } from 'playwright';
import { acceptedCommit } from '../../../src/integrations/runtime/__tests__/timelineCommitFixture.ts';

const OUTBOX_MODULE = '/src/tools/video-editor/commands/commitOutbox.ts';
const BLANK_ROUTE = '/__timeline-command-outbox__';
const scope = { realmId: 'browser-realm', actorId: 'browser-actor', projectId: 'browser-project', timelineId: 'browser-timeline' };
const h0 = { revisionId: 'R0', publicationId: 'P0' };
const ha = { revisionId: 'RA', publicationId: 'PA' };
const hb = { revisionId: 'RB', publicationId: 'PB' };
const nativeInitialDocument = acceptedCommit(
  { revision_id: h0.revisionId, publication_id: h0.publicationId },
  { revision_id: h0.revisionId, publication_id: h0.publicationId },
  { projectId: scope.projectId, timelineId: scope.timelineId },
).data.canonical_document;
const path = '/v1/projects/browser-project/timelines/browser-timeline/commit';

type BrowserRequest = { method: string; path: string; body: string; key: string };
type BrowserRecord = {
  ownerId: string;
  pending?: { request: BrowserRequest };
  intents: Array<{ id: string; payload: unknown; readyBase?: unknown }>;
};
type BrowserBox = {
  append(payload: unknown, basis: unknown): Promise<string>;
  dispatch(
    build: (intent: { payload: unknown }, base: { revisionId: string; publicationId: string }) => unknown,
    transmit: (request: BrowserRequest) => Promise<unknown>,
  ): Promise<BrowserRecord>;
  read(): Promise<BrowserRecord>;
};

function resolveChromium(): string {
  const executable = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ?? '/opt/pw-browsers/chromium';
  return executable;
}

async function openBlank(context: Awaited<ReturnType<typeof chromium.launchPersistentContext>>) {
  const page = await context.newPage();
  await page.route(`**${BLANK_ROUTE}`, (route) => route.fulfill({
    status: 200,
    contentType: 'text/html',
    body: '<!doctype html><title>outbox test</title>',
  }));
  const baseURL = process.env.BASE_URL ?? process.env.PLAYWRIGHT_BASE_URL;
  if (!baseURL) throw new Error('Playwright did not publish BASE_URL for the outbox browser test');
  await page.goto(`${baseURL}${BLANK_ROUTE}`, { waitUntil: 'domcontentloaded' });
  return page;
}

test('persists and excludes native browser command outbox claims across restart', async () => {
  test.setTimeout(120_000);
  const profile = await mkdtemp(join(tmpdir(), 'astrid-command-outbox-'));
  const launch = {
    executablePath: resolveChromium(),
    args: ['--no-sandbox'],
  };

  let context: Awaited<ReturnType<typeof chromium.launchPersistentContext>> | undefined;
  try {
    context = await chromium.launchPersistentContext(profile, launch);
    const firstPage = await openBlank(context);
    const setup = await firstPage.evaluate(async ({ modulePath, outboxScope, initialHead, requestPath }) => {
      const { createCommitOutbox } = await import(modulePath);
      const service = createCommitOutbox();
      const payloadA = {
        commands: [{
          schema_version: 1, op: 'clip.move', version: '1', select: 'parent/clip:opaque-A', args: { on: 5 },
          expect: [{ state: { present: true, value: { opaque: 'original-A' } } }, { state: { present: false } }],
          created: [{ id: 'allocated-A' }],
        }],
      };
      const payloadB = {
        commands: [{
          schema_version: 1, op: 'clip.move', version: '1', select: 'parent/clip:opaque-B', args: { on: 7 },
          expect: [{ state: { present: true, value: { opaque: 'original-B' } } }, { state: { present: false } }],
          created: [{ id: 'allocated-B' }],
        }],
      };
      const build = (intent: { payload: unknown }, base: { revisionId: string; publicationId: string }) => ({
        method: 'POST',
        path: requestPath,
        body: { base_revision_id: base.revisionId, base_publication_id: base.publicationId, proposal: intent.payload },
      });
      let ownerId = '';
      let requestA: unknown;
      let intentB = '';
      let reservationWasDurable = false;
      await service.create(outboxScope, async (rawBox: unknown, id: string) => {
        const box = rawBox as BrowserBox;
        ownerId = id;
        const intentA = await box.append(payloadA, { head: initialHead });
        await box.dispatch(build, async (request) => {
          requestA = request;
          const beforeTransmit = await service.list(outboxScope);
          reservationWasDurable = beforeTransmit.some((record: BrowserRecord) => record.ownerId === ownerId
            && record.pending?.request.key === request.key);
          intentB = await box.append(payloadB, { after: intentA });
          throw new Error('ack lost after A was transmitted');
        });
      });
      const records = await service.list(outboxScope);
      const owner = records.find((record: BrowserRecord) => record.ownerId === ownerId);
      return { ownerId, requestA, intentB, payloadA, payloadB, records, owner, reservationWasDurable };
    }, { modulePath: OUTBOX_MODULE, outboxScope: scope, initialHead: h0, requestPath: path });

    expect(setup.reservationWasDurable).toBe(true);
    expect(setup.ownerId).toMatch(/^[0-9a-f-]{36}$/);
    expect(setup.owner?.pending?.request).toEqual(setup.requestA);
    expect(setup.owner?.intents).toEqual(expect.arrayContaining([
      expect.objectContaining({ id: setup.intentB, payload: setup.payloadB }),
    ]));
    await firstPage.evaluate((ownerId) => sessionStorage.setItem('copied-owner-id', ownerId), setup.ownerId);

    const activeClaim = firstPage.evaluate(async ({ modulePath, outboxScope, ownerId }) => {
      const { createCommitOutbox } = await import(modulePath);
      const service = createCommitOutbox();
      await service.recover(outboxScope, ownerId, async () => {
        (window as unknown as { outboxClaimActive: boolean }).outboxClaimActive = true;
        await new Promise<void>((resolve) => {
          (window as unknown as { releaseOutboxClaim: () => void }).releaseOutboxClaim = resolve;
        });
      });
    }, { modulePath: OUTBOX_MODULE, outboxScope: scope, ownerId: setup.ownerId });
    await firstPage.waitForFunction(() => (window as unknown as { outboxClaimActive?: boolean }).outboxClaimActive === true);

    const secondPage = await openBlank(context);
    const concurrent = await secondPage.evaluate(async ({ modulePath, outboxScope, ownerId, initialHead }) => {
      const { createCommitOutbox } = await import(modulePath);
      const service = createCommitOutbox();
      let recoveryError = '';
      try {
        await service.recover(outboxScope, ownerId, async () => undefined);
      } catch (error) {
        recoveryError = error instanceof Error ? error.message : String(error);
      }
      const independent = await service.create(outboxScope, async (rawBox: unknown, independentOwnerId: string) => {
        const box = rawBox as BrowserBox;
        const intentId = await box.append({ independent: true }, { head: initialHead });
        return { independentOwnerId, intentId, record: await box.read() };
      });
      return { recoveryError, sessionOwner: sessionStorage.getItem('copied-owner-id'), independent };
    }, { modulePath: OUTBOX_MODULE, outboxScope: scope, ownerId: setup.ownerId, initialHead: h0 });
    expect(concurrent.recoveryError).toContain('already claimed');
    expect(concurrent.sessionOwner).toBeNull();
    expect(concurrent.independent.independentOwnerId).not.toBe(setup.ownerId);
    expect(concurrent.independent.record.intents).toHaveLength(1);
    await firstPage.evaluate(() => (window as unknown as { releaseOutboxClaim: () => void }).releaseOutboxClaim());
    await activeClaim;
    await context.close();
    context = undefined;

    context = await chromium.launchPersistentContext(profile, launch);
    const restartedPage = await openBlank(context);
    const recovered = await restartedPage.evaluate(async ({ modulePath, outboxScope, ownerId, acceptedHead, finalHead, requestPath }) => {
      const { createCommitOutbox } = await import(modulePath);
      const service = createCommitOutbox();
      const before = (await service.list(outboxScope)).find((record: BrowserRecord) => record.ownerId === ownerId);
      let requestA: unknown;
      let requestB: unknown;
      const afterA = await service.recover(outboxScope, ownerId, async (rawBox: unknown) => {
        const box = rawBox as BrowserBox;
        const after = await box.dispatch(() => {
          throw new Error('the persisted A request must be retried exactly');
        }, async (request: unknown) => {
          requestA = request;
          return { kind: 'accepted', head: acceptedHead, value: { accepted: 'A' } };
        });
        const withB = await box.dispatch((intent, base) => ({
          method: 'POST',
          path: requestPath,
          body: { base_revision_id: base.revisionId, base_publication_id: base.publicationId, proposal: intent.payload },
        }), async (request: unknown) => {
          requestB = request;
          return { kind: 'accepted', head: finalHead, value: { accepted: 'B' } };
        });
        return { after, withB, final: await box.read() };
      });
      return {
        before,
        afterA: afterA.after,
        final: afterA.final,
        requestA,
        requestB,
        sessionOwner: sessionStorage.getItem('copied-owner-id'),
        acceptedHead,
      };
    }, { modulePath: OUTBOX_MODULE, outboxScope: scope, ownerId: setup.ownerId, acceptedHead: ha, finalHead: hb, requestPath: path });

    expect(recovered.sessionOwner).toBeNull();
    expect(recovered.before?.pending?.request).toEqual(setup.requestA);
    expect(recovered.requestA).toEqual(setup.requestA);
    expect(recovered.requestA).toMatchObject({ method: 'POST', path });
    expect(JSON.parse((recovered.requestA as { body: string }).body)).toEqual({
      base_revision_id: h0.revisionId,
      base_publication_id: h0.publicationId,
      proposal: setup.payloadA,
    });
    expect(recovered.afterA.intents).toEqual(expect.arrayContaining([
      expect.objectContaining({ id: setup.intentB, payload: setup.payloadB, readyBase: ha }),
    ]));
    expect(recovered.requestB).toMatchObject({ method: 'POST', path });
    expect((recovered.requestB as { key: string }).key).not.toBe((recovered.requestA as { key: string }).key);
    expect(JSON.parse((recovered.requestB as { body: string }).body)).toEqual({
      base_revision_id: ha.revisionId,
      base_publication_id: ha.publicationId,
      proposal: setup.payloadB,
    });
    expect(recovered.final.intents).toEqual([]);
  } finally {
    if (context) await context.close();
    await rm(profile, { recursive: true, force: true });
  }
});

test('drains a native captured move on same-turn dispose before explicit recovery', async () => {
  const profile = await mkdtemp(join(tmpdir(), 'astrid-command-session-close-'));
  const launch = {
    executablePath: resolveChromium(),
    args: ['--no-sandbox'],
  };

  let context: Awaited<ReturnType<typeof chromium.launchPersistentContext>> | undefined;
  try {
    context = await chromium.launchPersistentContext(profile, launch);
    const firstPage = await openBlank(context);
    const setup = await firstPage.evaluate(async ({ modulePaths, outboxScope, initial, initialHead }) => {
      const { createCommitOutbox } = await import(modulePaths.outbox);
      const { createTimelineCommandSession } = await import(modulePaths.session);
      const { buildTimelineData } = await import(modulePaths.timelineData);
      const { captureClipMove, submitClipMove } = await import(modulePaths.gestures);
      const parent = initial.parent_revision.payload as { config: Record<string, unknown>; clips: unknown[]; registry: unknown };
      const current = await buildTimelineData(
        { ...parent.config, clips: parent.clips } as never, parent.registry as never, undefined, 1,
        undefined, { projectId: outboxScope.projectId, timelineId: outboxScope.timelineId,
          headRevisionId: initialHead.revisionId, headPublicationId: initialHead.publicationId },
      );
      const requests: Array<{ request: unknown; key: string }> = [];
      const session = await createTimelineCommandSession({
        scope: outboxScope,
        initial: { head: initialHead, canonicalDocument: initial },
        send: async (request: unknown, key: string) => {
          requests.push({ request, key });
          throw new Error('same-turn dispose must not start a network request');
        },
        preview: () => {},
        project: async () => {},
        changed: () => {},
      });
      const ownerId = session.getState().ownerId;
      if (!ownerId) throw new Error('native session did not claim an owner');
      const captured = captureClipMove(session.port, current, 'x');
      const expectedCommand = session.port.finish(captured.basis, 5).command;
      submitClipMove(captured, 5);
      await session.dispose();

      let claimReleased = false;
      await createCommitOutbox().recover(outboxScope, ownerId, async () => { claimReleased = true; });
      const records = await createCommitOutbox().list(outboxScope);
      return { claimReleased, expectedCommand, ownerId, records, requests };
    }, {
      modulePaths: {
        gestures: '/src/tools/video-editor/commands/semanticGestures.ts',
        outbox: OUTBOX_MODULE,
        session: '/src/tools/video-editor/commands/commitSession.ts',
        timelineData: '/src/tools/video-editor/lib/timeline-data.ts',
      },
      outboxScope: scope,
      initial: nativeInitialDocument,
      initialHead: h0,
    });

    expect(setup.claimReleased).toBe(true);
    expect(setup.requests).toEqual([]);
    expect(setup.ownerId).toMatch(/^[0-9a-f-]{36}$/);
    const saved = setup.records.find((record: BrowserRecord) => record.ownerId === setup.ownerId);
    expect(saved?.intents).toHaveLength(1);
    expect(saved?.intents[0]?.basis).toEqual({ head: h0 });
    expect(saved?.intents[0]?.payload).toMatchObject({ commands: [setup.expectedCommand] });
    const savedIntent = saved?.intents[0];
    expect(savedIntent).toBeDefined();

    await context.close();
    context = undefined;
    context = await chromium.launchPersistentContext(profile, launch);
    const restartedPage = await openBlank(context);
    const recovered = await restartedPage.evaluate(async ({ modulePaths, outboxScope, initial, initialHead, ownerId }) => {
      const { createCommitOutbox } = await import(modulePaths.outbox);
      const { createTimelineCommandSession } = await import(modulePaths.session);
      const outboxes = createCommitOutbox();
      const requests: Array<{ request: unknown; key: string }> = [];
      const session = await createTimelineCommandSession({
        scope: outboxScope,
        initial: { head: initialHead, canonicalDocument: initial },
        outboxes,
        send: async (request: unknown, key: string) => {
          requests.push({ request, key });
          throw new Error('transport intentionally unavailable during native recovery');
        },
        preview: () => {},
        project: async () => {},
        changed: () => {},
      });
      const before = (await outboxes.list(outboxScope)).find((record: BrowserRecord) => record.ownerId === ownerId);
      const recoverableOwners = session.getState().recoverableOwners;
      await session.recover(ownerId);
      const after = (await outboxes.list(outboxScope)).find((record: BrowserRecord) => record.ownerId === ownerId);
      await session.dispose();
      return { after, before, recoverableOwners, requests };
    }, {
      modulePaths: {
        outbox: OUTBOX_MODULE,
        session: '/src/tools/video-editor/commands/commitSession.ts',
      },
      outboxScope: scope,
      initial: nativeInitialDocument,
      initialHead: h0,
      ownerId: setup.ownerId,
    });

    expect(recovered.before?.intents[0]).toEqual(savedIntent);
    expect(recovered.recoverableOwners).toEqual([setup.ownerId]);
    expect(recovered.requests).toHaveLength(1);
    expect(recovered.after?.pending?.request.key).toBe(recovered.requests[0].key);
    expect(recovered.after?.intents[0]?.payload).toMatchObject({ commands: [setup.expectedCommand] });
    expect(JSON.parse(recovered.after?.pending?.request.body ?? '')).toEqual({
      api_version: 1,
      project_id: scope.projectId,
      timeline_id: scope.timelineId,
      base_revision_id: h0.revisionId,
      base_publication_id: h0.publicationId,
      commands: [setup.expectedCommand],
      source: { via: 'app' },
    });
    expect(recovered.requests[0].request).toEqual(JSON.parse(recovered.after?.pending?.request.body ?? ''));
  } finally {
    if (context) await context.close();
    await rm(profile, { recursive: true, force: true });
  }
});
