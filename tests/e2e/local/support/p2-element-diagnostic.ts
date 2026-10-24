import { writeFile } from 'node:fs/promises';
import type { Page, Request, Response } from '@playwright/test';
import { withDiagnosticDeadline } from '../p1-diagnostic-safety.ts';

export const P2_ELEMENT_DIAGNOSTIC_FILE = 'p2-element-apply-diagnostic.json';
const MAX_EVENTS = 24;
const MAX_BYTES = 24 * 1024;
const MAX_PENDING_REQUESTS = 8;
const RETENTION_TIMEOUT_MS = 500;
const UI_READ_TIMEOUT_MS = 150;

type Correlation = `apply-${number}`;
export type ElementApplyDiagnosticStage = 'apply-click' | 'request-start' | 'response' | 'request-failed' | 'page-close' | 'retained';
export type ElementApplyTerminal = 'unknown' | 'pending' | 'aborted' | 'failed' | 'accepted';
type RequestObservation = 'not-observed' | 'scoped-commit';
type FailureKind = 'none' | 'aborted' | 'failed' | 'unknown';
type ResponseKind = 'none' | 'success' | 'failure' | 'other';
type UiStage = 'apply' | 'request-pending' | 'response-received' | 'failure' | 'aborted' | 'retained' | 'unknown';
type UiConnection = 'connected' | 'disconnected' | 'unknown';
type UiDialog = 'present' | 'absent' | 'unknown';
type UiStatus = 'applied' | 'pending' | 'failed' | 'unknown';

export type ElementApplyUiState = {
  stage: UiStage;
  connection: UiConnection;
  dialog: UiDialog;
  status: UiStatus;
};

export type ElementApplyDiagnosticEvent = {
  version: 1;
  sequence: number;
  elapsedMs: number;
  stage: ElementApplyDiagnosticStage;
  correlation: Correlation | 'none';
  request: RequestObservation;
  idempotencyKey: 'present' | 'absent' | 'unknown';
  responseStatus: number | 'UNKNOWN';
  response: ResponseKind;
  failure: FailureKind;
  terminal: ElementApplyTerminal;
  ui: ElementApplyUiState;
};

export type ElementApplyDiagnosticSnapshot = {
  version: 1;
  kind: 'p2-element-apply-lifecycle';
  events: ElementApplyDiagnosticEvent[];
  terminal: ElementApplyTerminal;
  pageClosed: boolean;
};

export type ElementApplyDiagnosticArtifact = {
  version: 1;
  kind: 'p2-element-apply-lifecycle';
  status: 'observed' | 'UNKNOWN';
  lifecycle: {
    testOutcome: 'passed' | 'failed' | 'timedOut' | 'skipped' | 'interrupted' | 'unknown';
    beforePageClose: boolean;
    pageClosed: boolean;
  };
  diagnostic: ElementApplyDiagnosticSnapshot | 'UNKNOWN';
  losses: { write: boolean; events: boolean; ui: boolean };
};

type DiagnosticTestInfo = {
  outputPath(...pathSegments: string[]): string;
  attach(name: string, options: { path: string; contentType: string }): Promise<void>;
};

const UNKNOWN_UI: ElementApplyUiState = Object.freeze({ stage: 'unknown', connection: 'unknown', dialog: 'unknown', status: 'unknown' });

function boundedElapsed(startedAt: number): number {
  const value = Date.now() - startedAt;
  return Number.isSafeInteger(value) && value >= 0 && value <= 600_000 ? value : 600_000;
}

function statusCode(value: unknown): number | 'UNKNOWN' {
  return typeof value === 'number' && Number.isInteger(value) && value >= 100 && value <= 599 ? value : 'UNKNOWN';
}

function requestFailureKind(request: Request): FailureKind {
  try {
    const text = request.failure()?.errorText?.toLowerCase() ?? '';
    if (text.includes('abort') || text.includes('cancel') || text.includes('timeout')) return 'aborted';
    if (text) return 'failed';
  } catch { /* A failed request may no longer expose failure metadata. */ }
  return 'unknown';
}

function isCommitRequest(request: Request): boolean {
  try {
    return request.method() === 'POST' && /^\/(?:api\/runtime\/)?v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/.test(new URL(request.url()).pathname);
  } catch {
    return false;
  }
}

function requestBody(request: Request): Record<string, unknown> | undefined {
  try {
    const value = request.postDataJSON();
    return value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, unknown> : undefined;
  } catch {
    return undefined;
  }
}

/** The catalog Apply request's authenticated provenance and patch shape, not a UI alias, selects the target. */
function isElementApplyRequest(request: Request): boolean {
  const body = requestBody(request);
  if (!isCommitRequest(request) || keyPresence(request) !== 'present' || !body || body.api_version !== 1 || body.label !== 'Edit timeline'
    || body.merge !== 'atomic' || body.dry_run !== false || typeof body.project_id !== 'string'
    || typeof body.timeline_id !== 'string' || typeof body.base_revision_id !== 'string'
    || typeof body.base_publication_id !== 'string') return false;
  const source = body.source;
  if (!source || typeof source !== 'object' || Array.isArray(source) || (source as Record<string, unknown>).via !== 'app') return false;
  const commands = body.commands;
  const steps = body.steps;
  if (!Array.isArray(commands) || commands.length !== 1 || !Array.isArray(steps) || steps.length !== 1) return false;
  const command = commands[0];
  const step = steps[0];
  if (!command || typeof command !== 'object' || Array.isArray(command) || !step || typeof step !== 'object' || Array.isArray(step)) return false;
  const commandRecord = command as Record<string, unknown>;
  const stepRecord = step as Record<string, unknown>;
  const args = commandRecord.args;
  const changes = args && typeof args === 'object' && !Array.isArray(args) ? (args as Record<string, unknown>).changes : undefined;
  const firstChange = Array.isArray(changes) && changes.length === 1 ? changes[0] : undefined;
  const change = firstChange && typeof firstChange === 'object' && !Array.isArray(firstChange) ? firstChange as Record<string, unknown> : undefined;
  const path = change?.path;
  return commandRecord.schema_version === 1 && commandRecord.op === 'doc.patch' && commandRecord.version === '1'
    && commandRecord.select === null && Array.isArray(commandRecord.created)
    && stepRecord.intent === 'timeline.apply_element' && Array.isArray(stepRecord.command_ordinals)
    && stepRecord.command_ordinals.length === 1 && stepRecord.command_ordinals[0] === 0
    && Array.isArray(changes) && Array.isArray(stepRecord.patch) && Array.isArray(stepRecord.reads)
    && stepRecord.patch.length === changes.length
    && change?.op === 'list.insert' && change.ref === 'parent' && Array.isArray(path)
    && path.length > 0 && path.every((part) => typeof part === 'string') && path.at(-1) === 'clips';
}

function keyPresence(request: Request): 'present' | 'absent' | 'unknown' {
  try {
    return request.headers()['idempotency-key'] ? 'present' : 'absent';
  } catch {
    return 'unknown';
  }
}

function responseOutcome(status: number | 'UNKNOWN'): { response: ResponseKind; terminal: ElementApplyTerminal } {
  if (status === 'UNKNOWN') return { response: 'other', terminal: 'unknown' };
  if (status >= 200 && status <= 299) return { response: 'success', terminal: 'accepted' };
  if (status >= 400 && status <= 599) return { response: 'failure', terminal: 'failed' };
  return { response: 'other', terminal: 'unknown' };
}

function stateFor(stage: ElementApplyDiagnosticStage, terminal: ElementApplyTerminal): ElementApplyUiState {
  const uiStage: UiStage = stage === 'apply-click' ? 'apply'
    : stage === 'request-start' ? 'request-pending'
      : stage === 'response' ? 'response-received'
        : stage === 'request-failed' || terminal === 'failed' ? 'failure'
          : stage === 'page-close' || terminal === 'aborted' ? 'aborted'
            : stage === 'retained' ? 'retained' : 'unknown';
  return { ...UNKNOWN_UI, stage: uiStage };
}

function safeUiState(value: unknown): ElementApplyUiState {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return UNKNOWN_UI;
  const source = value as Record<string, unknown>;
  const stage = ['apply', 'request-pending', 'response-received', 'failure', 'aborted', 'retained', 'unknown'].includes(source.stage as string)
    ? source.stage as UiStage : 'unknown';
  const connection = ['connected', 'disconnected', 'unknown'].includes(source.connection as string)
    ? source.connection as UiConnection : 'unknown';
  const dialog = ['present', 'absent', 'unknown'].includes(source.dialog as string)
    ? source.dialog as UiDialog : 'unknown';
  const status = ['applied', 'pending', 'failed', 'unknown'].includes(source.status as string)
    ? source.status as UiStatus : 'unknown';
  return { stage, connection, dialog, status };
}

export function elementApplyUiScript(): string {
  return `(() => {
    const installKey = '__timelineP2ElementApplyBoundaryInstalled';
    if (window[installKey]) return;
    window[installKey] = true;
    document.addEventListener('click', (event) => {
      try {
        const target = event.target;
        if (!(target instanceof Element)) return;
        const button = target.closest('button');
        if (!button || (button.textContent || '').replace(/\\s+/g, ' ').trim() !== 'Apply') return;
        const notify = window.__timelineP2ElementApplyBoundary;
        if (typeof notify === 'function') void notify({ kind: 'apply-click' });
      } catch { /* Boundary observation is disposable. */ }
    }, true);
  })();`;
}

export function readElementApplyUiState(): ElementApplyUiState {
  try {
    const connectionNode = document.querySelector('[data-testid="runtime-connection-status"]');
    const connectionValue = connectionNode?.getAttribute('data-state');
    const connection: UiConnection = connectionValue === 'connected' ? 'connected' : connectionValue === 'disconnected' ? 'disconnected' : 'unknown';
    const dialog = document.querySelector('[role="dialog"]');
    const statusText = dialog?.querySelector('[role="status"]')?.textContent?.slice(0, 100).toLowerCase() ?? '';
    const status: UiStatus = statusText.includes('applied') ? 'applied'
      : statusText.includes('applying') || statusText.includes('pending') ? 'pending'
        : statusText.includes('failed') || statusText.includes('error') ? 'failed' : 'unknown';
    return { stage: 'retained', connection, dialog: dialog ? 'present' : 'absent', status };
  } catch {
    return UNKNOWN_UI;
  }
}

export class ElementApplyDiagnosticCollector {
  private readonly startedAt = Date.now();
  private readonly events: ElementApplyDiagnosticEvent[] = [];
  private readonly pendingRequests: Array<{ request: Request; response?: Response; failure?: FailureKind }> = [];
  private active?: { correlation: Correlation; request?: Request; terminal: ElementApplyTerminal };
  private applyOrdinal = 0;
  private closed = false;

  recordApplyClick(): void {
    this.applyOrdinal += 1;
    const correlation = `apply-${this.applyOrdinal}` as Correlation;
    this.active = { correlation, terminal: 'unknown' };
    this.record({ stage: 'apply-click', correlation, request: 'not-observed', idempotencyKey: 'unknown', responseStatus: 'UNKNOWN', response: 'none', failure: 'none', terminal: 'unknown' });
    const candidate = this.pendingRequests.pop();
    if (candidate) this.bindRequest(candidate);
  }

  recordRequest(request: Request): void {
    if (!isElementApplyRequest(request)) return;
    const candidate = this.pendingRequests.find((entry) => entry.request === request) ?? this.rememberRequest(request);
    if (this.active && !this.active.request && candidate) this.bindRequest(candidate);
  }

  recordResponse(response: Response): void {
    const request = response.request();
    if (!isElementApplyRequest(request)) return;
    if (!this.active?.request || request !== this.active.request) {
      const candidate = this.pendingRequests.find((entry) => entry.request === request);
      if (candidate) candidate.response = response;
      return;
    }
    if (this.active.terminal !== 'pending') return;
    const status = statusCode(response.status());
    const outcome = responseOutcome(status);
    this.active.terminal = outcome.terminal;
    this.record({ stage: 'response', correlation: this.active.correlation, request: 'scoped-commit', idempotencyKey: keyPresence(this.active.request), responseStatus: status, response: outcome.response, failure: outcome.terminal === 'failed' ? 'failed' : 'none', terminal: outcome.terminal });
  }

  recordRequestFailed(request: Request): void {
    if (!isElementApplyRequest(request)) return;
    if (!this.active?.request || request !== this.active.request) {
      const candidate = this.pendingRequests.find((entry) => entry.request === request);
      if (candidate) candidate.failure = requestFailureKind(request);
      return;
    }
    if (this.active.terminal !== 'pending') return;
    const failure = requestFailureKind(request);
    const terminal: ElementApplyTerminal = failure === 'aborted' ? 'aborted' : failure === 'failed' ? 'failed' : 'unknown';
    this.active.terminal = terminal;
    this.record({ stage: 'request-failed', correlation: this.active.correlation, request: 'scoped-commit', idempotencyKey: keyPresence(request), responseStatus: 'UNKNOWN', response: 'none', failure, terminal });
  }

  recordPageClose(): void {
    this.closed = true;
    if (!this.active) return;
    const terminal = this.active.terminal === 'pending' ? 'aborted' : this.active.terminal;
    this.active.terminal = terminal;
    this.record({ stage: 'page-close', correlation: this.active.correlation, request: this.active.request ? 'scoped-commit' : 'not-observed', idempotencyKey: this.active.request ? keyPresence(this.active.request) : 'unknown', responseStatus: 'UNKNOWN', response: 'none', failure: terminal === 'aborted' ? 'aborted' : 'none', terminal });
  }

  get hasApplyBoundary(): boolean { return this.events.length > 0; }

  snapshot(ui: ElementApplyUiState = UNKNOWN_UI): ElementApplyDiagnosticSnapshot {
    const events = this.events.slice(0, MAX_EVENTS).map((event) => ({ ...event, ui: event.stage === 'retained' ? ui : event.ui }));
    return { version: 1, kind: 'p2-element-apply-lifecycle', events, terminal: this.active?.terminal ?? 'unknown', pageClosed: this.closed };
  }

  recordRetained(): void {
    if (!this.active) return;
    this.record({ stage: 'retained', correlation: this.active.correlation, request: this.active.request ? 'scoped-commit' : 'not-observed', idempotencyKey: this.active.request ? keyPresence(this.active.request) : 'unknown', responseStatus: 'UNKNOWN', response: 'none', failure: 'none', terminal: this.active.terminal });
  }

  private record(input: Omit<ElementApplyDiagnosticEvent, 'version' | 'sequence' | 'elapsedMs' | 'ui'>): void {
    if (this.events.length >= MAX_EVENTS) return;
    this.events.push({ version: 1, sequence: this.events.length + 1, elapsedMs: boundedElapsed(this.startedAt), ...input, ui: stateFor(input.stage, input.terminal) });
  }

  private rememberRequest(request: Request): { request: Request; response?: Response; failure?: FailureKind } {
    if (this.pendingRequests.length >= MAX_PENDING_REQUESTS) this.pendingRequests.shift();
    const candidate = { request };
    this.pendingRequests.push(candidate);
    return candidate;
  }

  private bindRequest(candidate: { request: Request; response?: Response; failure?: FailureKind }): void {
    if (!this.active || this.active.request) return;
    const pendingIndex = this.pendingRequests.indexOf(candidate);
    if (pendingIndex >= 0) this.pendingRequests.splice(pendingIndex, 1);
    this.active.request = candidate.request;
    this.active.terminal = 'pending';
    this.record({ stage: 'request-start', correlation: this.active.correlation, request: 'scoped-commit', idempotencyKey: keyPresence(candidate.request), responseStatus: 'UNKNOWN', response: 'none', failure: 'none', terminal: 'pending' });
    if (candidate.failure) this.recordRequestFailed(candidate.request);
    else if (candidate.response) this.recordResponse(candidate.response);
  }
}

export function serializeElementApplyDiagnostic(artifact: ElementApplyDiagnosticArtifact): string {
  let text: string;
  try { text = `${JSON.stringify(artifact)}\n`; } catch { text = ''; }
  if (Buffer.byteLength(text, 'utf8') <= MAX_BYTES) return text;
  return `${JSON.stringify({ version: 1, kind: 'p2-element-apply-lifecycle', status: 'UNKNOWN', lifecycle: artifact.lifecycle, diagnostic: 'UNKNOWN', losses: { write: artifact.losses.write, events: true, ui: artifact.losses.ui } })}\n`;
}

function testOutcome(value: unknown): ElementApplyDiagnosticArtifact['lifecycle']['testOutcome'] {
  return ['passed', 'failed', 'timedOut', 'skipped', 'interrupted'].includes(value as string) ? value as ElementApplyDiagnosticArtifact['lifecycle']['testOutcome'] : 'unknown';
}

export async function retainElementApplyDiagnostic(
  testInfo: DiagnosticTestInfo,
  page: Pick<Page, 'evaluate'> | undefined,
  collector: ElementApplyDiagnosticCollector,
  outcome: unknown,
): Promise<boolean> {
  if (!collector.hasApplyBoundary) return false;
  const deadline = Date.now() + RETENTION_TIMEOUT_MS;
  collector.recordRetained();
  const initial: ElementApplyDiagnosticArtifact = {
    version: 1, kind: 'p2-element-apply-lifecycle', status: 'observed',
    lifecycle: { testOutcome: testOutcome(outcome), beforePageClose: !collector.snapshot().pageClosed, pageClosed: false },
    diagnostic: collector.snapshot(), losses: { write: false, events: false, ui: true },
  };
  let wrote = false;
  try {
    const output = testInfo.outputPath(P2_ELEMENT_DIAGNOSTIC_FILE);
    wrote = await withDiagnosticDeadline(async () => { await writeFile(output, serializeElementApplyDiagnostic(initial), { encoding: 'utf8', mode: 0o600 }); return true; }, false, RETENTION_TIMEOUT_MS);
    if (!wrote) return false;
    let ui = UNKNOWN_UI;
    if (page && Date.now() < deadline) {
      ui = safeUiState(await withDiagnosticDeadline(() => page.evaluate(readElementApplyUiState), UNKNOWN_UI, Math.min(UI_READ_TIMEOUT_MS, deadline - Date.now())));
    }
    const final: ElementApplyDiagnosticArtifact = {
      ...initial,
      diagnostic: collector.snapshot(ui),
      lifecycle: { ...initial.lifecycle, pageClosed: collector.snapshot().pageClosed },
      losses: { write: false, events: false, ui: ui === UNKNOWN_UI },
    };
    return await withDiagnosticDeadline(async () => { await writeFile(output, serializeElementApplyDiagnostic(final), { encoding: 'utf8', mode: 0o600 }); await testInfo.attach(P2_ELEMENT_DIAGNOSTIC_FILE, { path: output, contentType: 'application/json' }); return true; }, false, Math.max(0, deadline - Date.now()));
  } catch {
    return false;
  }
}

export async function installElementApplyDiagnostic(page: Page, collector: ElementApplyDiagnosticCollector): Promise<void> {
  page.on('request', (request) => collector.recordRequest(request));
  page.on('response', (response) => collector.recordResponse(response));
  page.on('requestfailed', (request) => collector.recordRequestFailed(request));
  page.on('close', () => collector.recordPageClose());
  const expose = page.exposeFunction('__timelineP2ElementApplyBoundary', () => collector.recordApplyClick()).catch(() => {});
  const init = page.addInitScript({ content: elementApplyUiScript() }).catch(() => {});
  await Promise.all([expose, init]);
}
