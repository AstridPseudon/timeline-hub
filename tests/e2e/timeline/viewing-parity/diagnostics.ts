import type { ConsoleMessage, Page, Request, Response } from '@playwright/test';

export const ACP_RESOURCE_ERROR = 'Failed to load resource: the server responded with a status of 503 (Service Unavailable)';

export type PageDiagnostic =
  | { kind: 'pageerror'; message: string; stack?: string }
  | { kind: 'console'; message: string; location: { url: string; lineNumber: number; columnNumber: number } }
  | { kind: 'response'; url: string; method: string; status: number; body?: string; bodyError?: string }
  | { kind: 'requestfailed'; url: string; method: string; message: string };

function optionalAcpUrl(url: string, origin: string, projectId: string): boolean {
  return ['/api/astrid/acp/models', '/api/astrid/acp/agents',
    `/api/astrid/acp/projects/${encodeURIComponent(projectId)}/chat`]
    .some(path => url === `${new URL(origin).origin}${path}`);
}

function unavailableBody(body: string | undefined): boolean {
  try {
    const value = JSON.parse(body ?? '') as unknown;
    return typeof value === 'object' && value !== null && !Array.isArray(value)
      && Object.keys(value).length === 1 && 'error' in value && value.error === 'acp_unavailable';
  } catch { return false; }
}

/** Only paired optional-chat responses and Chromium resource errors are diagnostic. */
export function classifyPageDiagnostics(raw: readonly PageDiagnostic[], origin: string, projectId: string) {
  const optional = new Set<PageDiagnostic>();
  const responses = raw.filter(item => item.kind === 'response');
  for (const item of raw) {
    if (item.kind !== 'console' || item.message !== ACP_RESOURCE_ERROR
      || item.location.lineNumber !== 0 || item.location.columnNumber !== 0
      || !optionalAcpUrl(item.location.url, origin, projectId)) continue;
    const matching = responses.filter(response => response.url === item.location.url);
    // Ambiguous failures on the same URL cannot qualify a resource console message.
    if (!matching.length || matching.some(response => response.method !== 'GET'
      || response.status !== 503 || !unavailableBody(response.body))
      || raw.some(error => error.kind === 'requestfailed' && error.url === item.location.url)) continue;
    const response = matching.find(candidate => !optional.has(candidate));
    if (response) { optional.add(response); optional.add(item); }
  }
  return { raw: [...raw], optionalAcp: raw.filter(item => optional.has(item)),
    failures: raw.filter(item => !optional.has(item)) };
}

/** Observe real traffic without intercepting requests or changing product readiness. */
export function collectPageDiagnostics(page: Page, origin: string, projectId: string) {
  const raw: PageDiagnostic[] = [];
  const pending = new Set<Promise<void>>();
  const onPageError = (error: Error) => raw.push({ kind: 'pageerror', message: error.message, stack: error.stack });
  const onConsole = (message: ConsoleMessage) => {
    if (message.type() === 'error') raw.push({ kind: 'console', message: message.text(), location: message.location() });
  };
  const onRequestFailed = (request: Request) => raw.push({ kind: 'requestfailed', url: request.url(),
    method: request.method(), message: request.failure()?.errorText ?? 'unknown request failure' });
  const onResponse = (response: Response) => {
    if (response.status() < 400) return;
    const item: Extract<PageDiagnostic, { kind: 'response' }> = { kind: 'response', url: response.url(),
      method: response.request().method(), status: response.status() };
    raw.push(item);
    if (item.method !== 'GET' || item.status !== 503 || !optionalAcpUrl(item.url, origin, projectId)) return;
    const reading = response.text().then(body => { item.body = body; }, error => { item.bodyError = String(error); });
    pending.add(reading);
    void reading.then(() => pending.delete(reading));
  };
  page.on('pageerror', onPageError);
  page.on('console', onConsole);
  page.on('requestfailed', onRequestFailed);
  page.on('response', onResponse);
  return {
    async result() {
      await Promise.all([...pending]);
      return classifyPageDiagnostics(raw, origin, projectId);
    },
    stop() {
      page.off('pageerror', onPageError);
      page.off('console', onConsole);
      page.off('requestfailed', onRequestFailed);
      page.off('response', onResponse);
    },
  };
}
