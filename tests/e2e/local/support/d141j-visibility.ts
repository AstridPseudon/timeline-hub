import { writeFile } from 'node:fs/promises';
import type { Page } from '@playwright/test';
import type { D141jVisibilityArtifact } from '../../../../src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts';

export const D141J_VISIBILITY_ARTIFACT_FILE = 'd141j-visibility.json';
export const D141J_VISIBILITY_MODULE_SPECIFIER = '/src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts';

type TestOutcome = 'passed' | 'failed' | 'timedOut' | 'skipped' | 'interrupted' | 'unknown';
type CaptureStatus = 'captured' | 'unavailable';

export type D141jVisibilityRetainedArtifact = D141jVisibilityArtifact & {
  retention: {
    testOutcome: TestOutcome;
    beforePageClose: boolean;
    pageClosed: boolean;
    capture: CaptureStatus;
  };
};

type BrowserAction =
  | { action: 'install'; moduleSpecifier: string; expectedOccurrenceId: string }
  | { action: 'snapshot'; moduleSpecifier: string }
  | { action: 'uninstall'; moduleSpecifier: string };

type DiagnosticTestInfo = {
  outputPath(...pathSegments: string[]): string;
  attach(name: string, options: { path: string; contentType: string }): Promise<void>;
  status?: unknown;
};

type VisibilityPage = Pick<Page, 'evaluate'>;

const STATE_KEY = '__timelineD141jVisibilityCollector';

function browserCollectorOperation({ action, moduleSpecifier, expectedOccurrenceId }: BrowserAction): Promise<unknown> {
  const win = window as unknown as Window & Record<string, unknown>;
  const state = win[STATE_KEY] as {
    collector: { snapshot: () => D141jVisibilityArtifact };
    uninstall: () => void;
  } | undefined;

  if (action === 'install') {
    return import(moduleSpecifier).then((visibilityModule: typeof import('../../../../src/tools/video-editor/diagnostics/d141jVisibilityObservation.ts')) => {
      const collector = visibilityModule.createD141jVisibilityCollector(expectedOccurrenceId);
      const uninstall = visibilityModule.installD141jVisibilityCollector(collector);
      win[STATE_KEY] = { collector, uninstall };
      return true;
    });
  }
  if (action === 'snapshot') return Promise.resolve(state?.collector.snapshot() ?? null);
  if (!state) return Promise.resolve(false);
  state.uninstall();
  delete win[STATE_KEY];
  return Promise.resolve(true);
}

async function evaluateAction<T>(page: VisibilityPage, action: BrowserAction): Promise<T> {
  return page.evaluate(browserCollectorOperation, action) as Promise<T>;
}

function outcome(value: unknown, fallback: TestOutcome): TestOutcome {
  return value === 'passed' || value === 'failed' || value === 'timedOut' || value === 'skipped' || value === 'interrupted'
    ? value : fallback;
}

function artifact(
  snapshot: D141jVisibilityArtifact | null,
  expectedOccurrenceId: string,
  testOutcome: TestOutcome,
  beforePageClose: boolean,
): D141jVisibilityRetainedArtifact {
  return {
    schema: 'timeline.app.d141j.visibility.v1',
    expectedOccurrenceId: snapshot?.expectedOccurrenceId ?? expectedOccurrenceId,
    events: snapshot?.events ?? [],
    retention: {
      testOutcome,
      beforePageClose,
      pageClosed: !beforePageClose,
      capture: snapshot ? 'captured' : 'unavailable',
    },
  };
}

export async function retainD141jVisibilityArtifact(
  testInfo: DiagnosticTestInfo,
  retained: D141jVisibilityRetainedArtifact,
): Promise<boolean> {
  try {
    const output = testInfo.outputPath(D141J_VISIBILITY_ARTIFACT_FILE);
    await writeFile(output, `${JSON.stringify(retained)}\n`, { encoding: 'utf8', mode: 0o600 });
    await testInfo.attach(D141J_VISIBILITY_ARTIFACT_FILE, { path: output, contentType: 'application/json' });
    return true;
  } catch {
    return false;
  }
}

export type D141jVisibilitySession = {
  snapshot(): Promise<D141jVisibilityArtifact | null>;
  uninstall(): Promise<boolean>;
};

export async function installD141jVisibilityCollector(
  page: VisibilityPage,
  expectedOccurrenceId: string,
): Promise<D141jVisibilitySession> {
  await evaluateAction<boolean>(page, { action: 'install', moduleSpecifier: D141J_VISIBILITY_MODULE_SPECIFIER, expectedOccurrenceId });
  return {
    snapshot: () => evaluateAction<D141jVisibilityArtifact | null>(page, { action: 'snapshot', moduleSpecifier: D141J_VISIBILITY_MODULE_SPECIFIER }),
    uninstall: async () => evaluateAction<boolean>(page, { action: 'uninstall', moduleSpecifier: D141J_VISIBILITY_MODULE_SPECIFIER }),
  };
}

/**
 * Private mounted diagnostic opt-in. The caller owns the existing App page fixture;
 * this wrapper only adds one collector session and retains its snapshot before that
 * fixture closes the page. Empty events remain empty when the mounted route observes
 * no occurrence, and are not promoted to a semantic pass.
 */
export async function withMountedD141jVisibilityCollector<T>(
  page: VisibilityPage,
  testInfo: DiagnosticTestInfo,
  expectedOccurrenceId: string,
  run: (session: D141jVisibilitySession) => Promise<T>,
): Promise<T> {
  let session: D141jVisibilitySession | undefined;
  let operationOutcome: TestOutcome = 'failed';
  try {
    session = await installD141jVisibilityCollector(page, expectedOccurrenceId);
    const result = await run(session);
    operationOutcome = 'passed';
    return result;
  } finally {
    let snapshot: D141jVisibilityArtifact | null = null;
    if (session) {
      try { snapshot = await session.snapshot(); } catch { /* A closed page is retained as unavailable. */ }
    }
    await retainD141jVisibilityArtifact(testInfo, artifact(
      snapshot,
      expectedOccurrenceId,
      outcome(testInfo.status, operationOutcome),
      true,
    ));
    try { await session?.uninstall(); } catch { /* Diagnostic cleanup is disposable. */ }
  }
}
