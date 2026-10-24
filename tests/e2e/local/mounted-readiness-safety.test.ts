import assert from 'node:assert/strict';
import { test } from 'node:test';
import type { BrowserContext, Page } from '@playwright/test';
import { mkdtempSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { createFakeIndexedDB } from '../../../vendor/fake-indexeddb/index.js';
import { createCommitOutbox } from '../../../src/tools/video-editor/commands/commitOutbox.ts';
import { bootstrapMountedBaseline } from './support/app.ts';
import type { DirectHarness } from './support/harness.ts';
import { clearMountedBootstrapFailure, hasFreshSettledOwner, isFreshlyConnected, MountedBootstrapError, readExistingReadonly, readMountedBootstrapFailure, recordMountedBootstrapFailure, retainMountedBootstrapDiagnostics } from './mounted-readiness-safety.ts';

test('missing database is unavailable, not a verified empty baseline', async () => {
  let reads = 0;
  const result = await readExistingReadonly(async () => false, async () => {
    reads += 1;
    return [];
  });
  assert.deepEqual(result, { status: 'unknown', reason: 'unavailable' });
  assert.equal(reads, 0);
});

test('database read rejection remains unknown', async () => {
  const result = await readExistingReadonly(async () => true, async () => { throw new Error('read rejected'); });
  assert.deepEqual(result, { status: 'unknown', reason: 'read-rejected' });
});

test('an available empty database is a verified empty baseline', async () => {
  const result = await readExistingReadonly(async () => true, async () => []);
  assert.deepEqual(result, { status: 'verified', value: [] });
});

test('only a new settled owner qualifies after the verified baseline', () => {
  const previous = new Set(['old-owner']);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'old-owner', intents: [] }], previous), false);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'new-owner', pending: { state: 'pending' }, intents: [] }], previous), false);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'new-owner', intents: ['gesture'] }], previous), false);
  assert.equal(hasFreshSettledOwner([{ ownerId: 'new-owner', intents: [] }], previous), true);
});

test('a closed page read cannot become a verified baseline', async () => {
  const result = await readExistingReadonly(async () => { throw new Error('page closed'); }, async () => []);
  assert.deepEqual(result, { status: 'unknown', reason: 'unavailable' });
});

test('a disconnected selection read cannot retain the initial connected claim', () => {
  assert.equal(isFreshlyConnected({ attached: true, state: 'connected' }), true);
  assert.equal(isFreshlyConnected({ attached: true, state: 'disconnected' }), false);
  assert.equal(isFreshlyConnected({ attached: 'UNKNOWN', state: 'connected' }), false);
});

test('mounted bootstrap failures expose only a finite safe projection', () => {
  clearMountedBootstrapFailure();
  const cause = new Error('private cause remains on the error');
  recordMountedBootstrapFailure(new MountedBootstrapError({ stage: 'selection', code: 'mounted-bootstrap', class: 'mounted-bootstrap' }, cause));
  assert.deepEqual(readMountedBootstrapFailure(), { stage: 'selection', code: 'mounted-bootstrap', class: 'mounted-bootstrap' });
  clearMountedBootstrapFailure();
  assert.equal(readMountedBootstrapFailure(), undefined);
});

test('mounted bootstrap retention uses the real serialized producer snapshot and preserves unknowns', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'mounted-bootstrap-lifecycle-'));
  const artifactPath = join(directory, 'mounted-bootstrap-lifecycle.json');
  const testInfo = {
    outputPath(name: string) { assert.equal(name, 'mounted-bootstrap-lifecycle.json'); return artifactPath; },
    async attach(name: string) { assert.equal(name, 'mounted-bootstrap-lifecycle.json'); },
  };
  const page = {
    async evaluate<T>(fn: () => T): Promise<T> {
      void fn;
      return {
        status: 'observed', buffer: 'mounted-bootstrap', accepted: 1, rejected: 0, overflow: 0, listenerErrors: 0,
        records: [{ version: 1, phase: 'basis-read', basisStatus: 'loading', projectId: 'project', timelineId: 'timeline',
          identityPresent: 'UNKNOWN', sessionPresent: false, errorCode: 'UNKNOWN', errorClass: 'UNKNOWN' }],
      } as T;
    },
  };
  await retainMountedBootstrapDiagnostics(testInfo, page, 'failed');
  const artifact = JSON.parse(readFileSync(artifactPath, 'utf8')) as { status: string; lifecycle: { beforePageClose: boolean }; diagnostics: { records: Array<Record<string, unknown>> } };
  assert.equal(artifact.status, 'captured');
  assert.equal(artifact.lifecycle.beforePageClose, true);
  assert.equal(artifact.diagnostics.records[0].phase, 'basis-read');
  assert.equal(artifact.diagnostics.records[0].identityPresent, 'UNKNOWN');
});

test('mounted bootstrap retention keeps an early UNKNOWN artifact when the page closes or the writer fails', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'mounted-bootstrap-unknown-'));
  const artifactPath = join(directory, 'mounted-bootstrap-lifecycle.json');
  const closedPage = { async evaluate(): Promise<never> { throw new Error('page closed'); } };
  await retainMountedBootstrapDiagnostics({ outputPath: () => artifactPath, attach: async () => {} }, closedPage, 'failed');
  const artifact = JSON.parse(readFileSync(artifactPath, 'utf8')) as { status: string; diagnostics: unknown };
  assert.equal(artifact.status, 'UNKNOWN');
  assert.equal(artifact.diagnostics, 'UNKNOWN');
  await assert.doesNotReject(() => retainMountedBootstrapDiagnostics({
    outputPath: () => { throw new Error('output unavailable'); },
    attach: async () => {},
  }, closedPage, 'failed'));
});

// The vendored fake uses event listeners and a database Map. Adapt only its
// browser API surface; all owner creation and reads use the production storage.
function browserEvents<T extends { addEventListener(name: string, listener: () => void): void }>(target: T, names: string[]): T {
  for (const name of names) Object.defineProperty(target, `on${name}`, {
    set(listener: () => void) { target.addEventListener(name, listener); },
  });
  return target;
}

function bootstrapControl(beforeProbe: (probe: number, storage: ReturnType<typeof createCommitOutbox>) => Promise<void>) {
  const factory = createFakeIndexedDB();
  const storage = createCommitOutbox({ indexedDB: factory, exclusiveLock: async (_name, work) => work() });
  let probes = 0;
  let opens = 0;
  let closed = false;
  const browserFactory = {
    async databases() {
      await beforeProbe(++probes, storage);
      return [...factory.databases.keys()].map((name) => ({ name }));
    },
    open(name: string) {
      opens += 1;
      const request = factory.open(name);
      request.addEventListener('success', () => {
        const db = request.result;
        const transaction = db.transaction.bind(db);
        db.transaction = (store: string, mode: string) => {
          assert.equal(mode, 'readonly');
          return browserEvents(transaction(store, mode), ['complete', 'abort']);
        };
      });
      return browserEvents(request, ['success', 'error']);
    },
  };
  const locator = { _apiName: 'Locator', _expect: async () => ({ matches: true }), first() { return this; } };
  const page = {
    on() {}, async goto() {}, locator: () => locator, getByRole: () => locator,
    async evaluate<T, A>(fn: (arg: A) => T, arg: A) {
      const prior = globalThis.indexedDB;
      Object.defineProperty(globalThis, 'indexedDB', { configurable: true, value: browserFactory });
      try { return await fn(arg); }
      finally { Object.defineProperty(globalThis, 'indexedDB', { configurable: true, value: prior }); }
    },
    async close() { closed = true; },
  };
  return {
    run: () => bootstrapMountedBaseline({ newPage: async () => page as unknown as Page } as BrowserContext,
      { origin: 'https://bootstrap.test', seed: { projectId: 'project', timelineId: 'timeline', projectName: 'Project' } } as DirectHarness),
    state: () => ({ probes, opens, closed, databases: factory.databases.size }),
  };
}

test('real bootstrap stays mounted through absent, empty, other-project and dirty DB states until the production scoped claim', async () => {
  const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project', timelineId: 'timeline' };
  const control = bootstrapControl(async (probe, storage) => {
    assert.equal(control.state().closed, false);
    if (probe === 2) await storage.list(scope);
    if (probe === 4) await storage.create({ ...scope, projectId: 'other-project' }, async () => {});
    if (probe === 6) await storage.create(scope, async (box) => {
      await box.append({ edit: true }, { head: { revisionId: 'revision', publicationId: 'publication' } });
    });
    if (probe === 8) await storage.create(scope, async () => {});
  });
  const owners = await control.run();
  assert.equal(owners.filter((owner) => owner.scope.projectId === 'project' && owner.intents.length === 0).length, 1);
  assert.deepEqual(control.state(), { probes: 9, opens: 4, closed: true, databases: 1 });
});

test('real bootstrap never creates a missing database or accepts an empty fallback and closes on timeout', async () => {
  const control = bootstrapControl(async () => {});
  await assert.rejects(control.run(), MountedBootstrapError);
  assert.equal(control.state().opens, 0);
  assert.equal(control.state().databases, 0);
  assert.equal(control.state().closed, true);
  assert.deepEqual(readMountedBootstrapFailure(), { stage: 'outbox-read', code: 'mounted-bootstrap', class: 'mounted-bootstrap' });
});

test('real bootstrap preserves a rejected existence probe as a bounded outbox-read failure', async () => {
  const control = bootstrapControl(async () => { throw new Error('private database failure'); });
  await assert.rejects(control.run(), MountedBootstrapError);
  assert.equal(control.state().closed, true);
  assert.deepEqual(readMountedBootstrapFailure(), { stage: 'outbox-read', code: 'mounted-bootstrap', class: 'mounted-bootstrap' });
  assert.doesNotMatch(JSON.stringify(readMountedBootstrapFailure()), /private/);
});
