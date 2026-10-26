import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, unlinkSync } from 'node:fs';
import { test } from 'node:test';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  D141J_VISIBILITY_MODULE_SPECIFIER,
  installD141jVisibilityCollector,
  withMountedD141jVisibilityCollector,
  type D141jVisibilitySession,
} from './d141j-visibility.ts';
import { mountedD141jVisibilityPageFixture } from './app.ts';
import * as visibilityModule from '../../../../src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts';

type Action = { action: 'install' | 'snapshot' | 'uninstall'; moduleSpecifier: string; expectedOccurrenceId?: string };

function browserDouble() {
  let collector: visibilityModule.D141jVisibilityCollector | undefined;
  let uninstall: (() => void) | undefined;
  const evaluations: Action[] = [];
  const page = {
    async evaluate(operation: unknown, action: Action) {
      evaluations.push(action);
      assert.equal(action.moduleSpecifier, D141J_VISIBILITY_MODULE_SPECIFIER);
      if (action.action === 'install') {
        assert.match(String(operation), /import\(moduleSpecifier\)/);
        assert.ok(action.expectedOccurrenceId);
        collector = visibilityModule.createD141jVisibilityCollector(action.expectedOccurrenceId);
        uninstall = visibilityModule.installD141jVisibilityCollector(collector);
        return true;
      }
      if (action.action === 'snapshot') return collector?.snapshot() ?? null;
      uninstall?.();
      collector = undefined;
      uninstall = undefined;
      return true;
    },
    record(event: visibilityModule.D141jVisibilityEvent) { collector?.record(event); },
    evaluations,
  };
  return page;
}

function testInfo(status: string, output: string, onAttach?: () => void) {
  const attachments: string[] = [];
  return {
    status,
    outputPath: () => output,
    async attach(name: string, options: { path: string; contentType: string }) {
      assert.equal(options.path, output);
      assert.equal(options.contentType, 'application/json');
      attachments.push(name);
      onAttach?.();
    },
    attachments,
  };
}

function mountedFixtureDouble() {
  const events: string[] = [];
  const mock = browserDouble();
  const evaluate = mock.evaluate.bind(mock);
  const page = Object.assign(mock, {
    async evaluate(operation: unknown, action: Action) {
      events.push(`evaluate:${action.action}`);
      return evaluate(operation, action);
    },
    async close() { events.push('page-close'); },
  });
  const context = {
    async newPage() { events.push('page-create'); return page; },
  };
  const fixture = async (
    _args: { context: typeof context }, use: (value: typeof page) => Promise<void>,
  ) => {
    events.push('fixture-enter');
    try { await use(page); } finally { await page.close(); }
  };
  return { context, events, fixture, page };
}

const accepted = {
  kind: 'accepted-canonical-read' as const,
  acceptedReadId: 'accepted-read-1',
  projectId: 'project-1',
  parentDocumentId: 'parent-1',
  acceptedReadHeadRevisionId: 'revision-1',
  previousAcceptedReadHeadRevisionId: null,
  occurrenceIds: ['occurrence-1'],
};

test('mounted installer uses the devserver module import and extracts the real collector snapshot', async () => {
  const mock = browserDouble();
  const session = await installD141jVisibilityCollector(mock as never, 'occurrence-1');
  mock.record(accepted);
  const snapshot = await session.snapshot();
  assert.equal(mock.evaluations[0]?.action, 'install');
  assert.equal(snapshot?.schema, 'timeline.app.d141j.visibility.v1');
  assert.deepEqual(snapshot?.events, [accepted]);
  assert.equal(await session.uninstall(), true);
  assert.equal(await session.snapshot(), null);
});

test('retention writes and attaches an honest empty artifact when the mounted route has no events', async () => {
  const mock = browserDouble();
  const output = join(mkdtempSync(join(tmpdir(), 'd141j-visibility-')), 'd141j-visibility.json');
  const info = testInfo('passed', output);
  try {
    await withMountedD141jVisibilityCollector(mock as never, info, 'missing-occurrence', async () => undefined);
    const retained = JSON.parse(readFileSync(output, 'utf8'));
    assert.deepEqual(Object.keys(retained).sort(), ['events', 'expectedOccurrenceId', 'retention', 'schema']);
    assert.equal(retained.expectedOccurrenceId, 'missing-occurrence');
    assert.deepEqual(retained.events, []);
    assert.deepEqual(retained.retention, { testOutcome: 'passed', beforePageClose: true, pageClosed: false, capture: 'captured' });
    assert.deepEqual(info.attachments, ['d141j-visibility.json']);
  } finally {
    if (existsSync(output)) unlinkSync(output);
  }
});

test('failure still retains before cleanup and always uninstalls the collector', async () => {
  const mock = browserDouble();
  const output = join(mkdtempSync(join(tmpdir(), 'd141j-visibility-')), 'd141j-visibility.json');
  const info = testInfo('failed', output);
  try {
    await assert.rejects(
      withMountedD141jVisibilityCollector(mock as never, info, 'occurrence-1', async (session: D141jVisibilitySession) => {
        mock.record(accepted);
        assert.deepEqual((await session.snapshot())?.events, [accepted]);
        throw new Error('ordinary test failure');
      }),
      /ordinary test failure/,
    );
    const retained = JSON.parse(readFileSync(output, 'utf8'));
    assert.equal(retained.retention.testOutcome, 'failed');
    assert.equal(retained.retention.beforePageClose, true);
    assert.equal(retained.retention.pageClosed, false);
    assert.deepEqual(info.attachments, ['d141j-visibility.json']);
    assert.equal(await mock.evaluate(() => null, { action: 'snapshot', moduleSpecifier: D141J_VISIBILITY_MODULE_SPECIFIER }), null);
  } finally {
    if (existsSync(output)) unlinkSync(output);
  }
});

test('the shared mounted page fixture is inert by default and wires opt-in capture around the real page lifetime', async () => {
  const previous = process.env.TIMELINE_D141J_VISIBILITY_CAPTURE;
  const restore = () => {
    if (previous === undefined) delete process.env.TIMELINE_D141J_VISIBILITY_CAPTURE;
    else process.env.TIMELINE_D141J_VISIBILITY_CAPTURE = previous;
  };
  try {
    delete process.env.TIMELINE_D141J_VISIBILITY_CAPTURE;
    const disabled = mountedFixtureDouble();
    await mountedD141jVisibilityPageFixture(
      { context: disabled.context as never }, async () => { disabled.events.push('test-body'); },
      testInfo('passed', join(mkdtempSync(join(tmpdir(), 'd141j-visibility-')), 'disabled.json')) as never,
      disabled.fixture as never,
    );
    assert.deepEqual(disabled.events, ['fixture-enter', 'test-body', 'page-close']);
    assert.deepEqual(disabled.page.evaluations, []);

    process.env.TIMELINE_D141J_VISIBILITY_CAPTURE = JSON.stringify({ expectedOccurrenceId: 'occurrence-1' });
    const enabled = mountedFixtureDouble();
    const output = join(mkdtempSync(join(tmpdir(), 'd141j-visibility-')), 'd141j-visibility.json');
    const info = testInfo('passed', output, () => enabled.events.push('attach'));
    await mountedD141jVisibilityPageFixture(
      { context: enabled.context as never }, async () => { enabled.events.push('test-body'); },
      info as never,
      enabled.fixture as never,
    );
    assert.deepEqual(enabled.events, ['fixture-enter', 'evaluate:install', 'test-body', 'evaluate:snapshot', 'attach', 'evaluate:uninstall', 'page-close']);
    assert.deepEqual(enabled.page.evaluations.map(({ action }) => action), ['install', 'snapshot', 'uninstall']);
    assert.deepEqual(info.attachments, ['d141j-visibility.json']);
    assert.equal(JSON.parse(readFileSync(output, 'utf8')).retention.beforePageClose, true);
    unlinkSync(output);
  } finally {
    restore();
  }
});

test('malformed mounted capture config fails closed without changing ordinary fixture behavior', async () => {
  const previous = process.env.TIMELINE_D141J_VISIBILITY_CAPTURE;
  try {
    process.env.TIMELINE_D141J_VISIBILITY_CAPTURE = '{not-json';
    const mounted = mountedFixtureDouble();
    await mountedD141jVisibilityPageFixture(
      { context: mounted.context as never }, async () => { mounted.events.push('test-body'); },
      testInfo('passed', join(mkdtempSync(join(tmpdir(), 'd141j-visibility-')), 'malformed.json')) as never,
      mounted.fixture as never,
    );
    assert.deepEqual(mounted.events, ['fixture-enter', 'test-body', 'page-close']);
    assert.deepEqual(mounted.page.evaluations, []);
  } finally {
    if (previous === undefined) delete process.env.TIMELINE_D141J_VISIBILITY_CAPTURE;
    else process.env.TIMELINE_D141J_VISIBILITY_CAPTURE = previous;
  }
});

test('shared mounted wiring retains a failing test before the fixture closes its page', async () => {
  const previous = process.env.TIMELINE_D141J_VISIBILITY_CAPTURE;
  process.env.TIMELINE_D141J_VISIBILITY_CAPTURE = JSON.stringify({ expectedOccurrenceId: 'occurrence-1' });
  const mounted = mountedFixtureDouble();
  const output = join(mkdtempSync(join(tmpdir(), 'd141j-visibility-')), 'd141j-visibility.json');
  const info = testInfo('failed', output, () => mounted.events.push('attach'));
  try {
    await assert.rejects(
      mountedD141jVisibilityPageFixture(
        { context: mounted.context as never },
        async () => { mounted.events.push('test-body'); throw new Error('ordinary test failure'); },
        info as never,
        mounted.fixture as never,
      ),
      /ordinary test failure/,
    );
    assert.deepEqual(mounted.events, ['fixture-enter', 'evaluate:install', 'test-body', 'evaluate:snapshot', 'attach', 'evaluate:uninstall', 'page-close']);
    assert.deepEqual(mounted.page.evaluations.map(({ action }) => action), ['install', 'snapshot', 'uninstall']);
    assert.equal(JSON.parse(readFileSync(output, 'utf8')).retention.testOutcome, 'failed');
    assert.equal(JSON.parse(readFileSync(output, 'utf8')).retention.beforePageClose, true);
    assert.deepEqual(info.attachments, ['d141j-visibility.json']);
  } finally {
    unlinkSync(output);
    if (previous === undefined) delete process.env.TIMELINE_D141J_VISIBILITY_CAPTURE;
    else process.env.TIMELINE_D141J_VISIBILITY_CAPTURE = previous;
  }
});
