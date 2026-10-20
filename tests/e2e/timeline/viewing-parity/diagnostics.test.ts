import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { test } from 'node:test';
import type { Page } from '@playwright/test';
import { ACP_RESOURCE_ERROR, classifyPageDiagnostics, collectPageDiagnostics, type PageDiagnostic } from './diagnostics';

const origin = 'http://127.0.0.1:17340';
const project = 'current-project';
const url = `${origin}/api/astrid/acp/projects/${project}/chat`;
const response = (overrides = {}): Extract<PageDiagnostic, { kind: 'response' }> => ({ kind: 'response',
  url, method: 'GET', status: 503, body: '{ "error": "acp_unavailable" }', ...overrides });
const consoleError = (overrides = {}): Extract<PageDiagnostic, { kind: 'console' }> => ({ kind: 'console',
  message: ACP_RESOURCE_ERROR, location: { url, lineNumber: 0, columnNumber: 0 }, ...overrides });
const classify = (raw: PageDiagnostic[]) => classifyPageDiagnostics(raw, origin, project);

for (const path of ['/api/astrid/acp/models', '/api/astrid/acp/agents', `/api/astrid/acp/projects/${project}/chat`]) {
  test(`classifies only correlated optional ACP unavailability: ${path}`, () => {
    const target = `${origin}${path}`;
    const raw = [consoleError({ location: { url: target, lineNumber: 0, columnNumber: 0 } }), response({ url: target })];
    assert.deepEqual(classify(raw), { raw, optionalAcp: raw, failures: [] });
  });
}

for (const [name, overrides] of Object.entries({
  'wrong body': { body: '{"error":"unauthorized"}' },
  'extra body field': { body: '{"error":"acp_unavailable","detail":"failure"}' },
  'array body': { body: '[{"error":"acp_unavailable"}]' },
  'invalid JSON': { body: 'acp_unavailable' },
  'unreadable body': { body: undefined, bodyError: 'closed' },
  'wrong status': { status: 500 },
  'auth status': { status: 403 },
  'wrong method': { method: 'POST' },
  'HEAD method': { method: 'HEAD' },
})) {
  test(`retains ${name} and its console error as failures`, () => {
    const raw = [response(overrides), consoleError()];
    assert.deepEqual(classify(raw), { raw, optionalAcp: [], failures: raw });
  });
}

for (const [name, target] of Object.entries({
  'wrong origin': url.replace('127.0.0.1', 'localhost'),
  'wrong port': url.replace('17340', '17341'),
  'wrong project': url.replace(project, 'other-project'),
  'query string': `${url}?project=${project}`,
  'catalog': `${origin}/api/astrid/v1/capabilities`,
  'media': `${origin}/api/astrid/v1/objects/media.mp4`,
  'admission': `${origin}/api/astrid/v1/tasks`,
  'auth': `${origin}/api/astrid/auth`,
  'unrelated ACP': `${origin}/api/astrid/acp/status`,
})) {
  test(`retains matching ${name} response and console error as failures`, () => {
    const raw = [response({ url: target }), consoleError({ location: { url: target, lineNumber: 0, columnNumber: 0 } })];
    assert.deepEqual(classify(raw), { raw, optionalAcp: [], failures: raw });
  });
}

test('requires an exact resource-load message and matching resource location', () => {
  for (const error of [consoleError({ message: `app: ${ACP_RESOURCE_ERROR}` }),
    consoleError({ location: { url: `${origin}/page.js`, lineNumber: 0, columnNumber: 0 } }),
    consoleError({ location: { url, lineNumber: 1, columnNumber: 0 } })]) {
    const raw = [response(), error];
    assert.deepEqual(classify(raw).failures, raw);
  }
  assert.deepEqual(classify([consoleError()]).failures, [consoleError()]);
  assert.deepEqual(classify([response()]).failures, [response()]);
});

test('retains all page, media, transport and other console errors beside optional chat diagnostics', () => {
  const optional = [response(), consoleError()];
  const failures: PageDiagnostic[] = [
    { kind: 'pageerror', message: ACP_RESOURCE_ERROR },
    { kind: 'requestfailed', url: `${origin}/video.mp4`, method: 'GET', message: 'net::ERR_FAILED' },
    consoleError({ message: 'media decode failed' }),
    response({ url: `${origin}/video.mp4` }),
  ];
  const raw = [...optional, ...failures];
  assert.deepEqual(classify(raw), { raw, optionalAcp: optional, failures });
});

test('does not let one valid response hide repeated or ambiguous errors on the same URL', () => {
  const raw = [response(), consoleError(), consoleError()];
  assert.deepEqual(classify(raw).failures, [raw[2]]);
  for (const extra of [response({ status: 500 }), response({ method: 'POST' }),
    { kind: 'requestfailed', url, method: 'GET', message: 'net::ERR_FAILED' } as const]) {
    const ambiguous = [response(), consoleError(), extra];
    assert.deepEqual(classify(ambiguous).failures, ambiguous);
  }
});

test('collector retains raw errors, waits for the response body and removes listeners', async () => {
  const page = new EventEmitter();
  const logs = collectPageDiagnostics(page as unknown as Page, origin, project);
  let resolveBody!: (body: string) => void;
  page.emit('response', { url: () => url, status: () => 503, request: () => ({ method: () => 'GET' }),
    text: () => new Promise<string>(resolve => { resolveBody = resolve; }) });
  page.emit('console', { type: () => 'error', text: () => ACP_RESOURCE_ERROR,
    location: () => ({ url, lineNumber: 0, columnNumber: 0 }) });
  page.emit('pageerror', new Error('page crashed'));
  page.emit('requestfailed', { url: () => `${origin}/media.mp4`, method: () => 'GET',
    failure: () => ({ errorText: 'decode request failed' }) });
  const result = logs.result();
  resolveBody('{"error":"acp_unavailable"}');
  const diagnostics = await result;
  assert.equal(diagnostics.raw.length, 4);
  assert.equal(diagnostics.optionalAcp.length, 2);
  assert.deepEqual(diagnostics.failures.map(item => item.kind), ['pageerror', 'requestfailed']);
  logs.stop();
  assert.deepEqual(page.eventNames(), []);
});

test('collector fails closed when an optional response body cannot be read', async () => {
  const page = new EventEmitter();
  const logs = collectPageDiagnostics(page as unknown as Page, origin, project);
  try {
    page.emit('response', { url: () => url, status: () => 503, request: () => ({ method: () => 'GET' }),
      text: async () => { throw new Error('closed'); } });
    page.emit('console', { type: () => 'error', text: () => ACP_RESOURCE_ERROR,
      location: () => ({ url, lineNumber: 0, columnNumber: 0 }) });
    const diagnostics = await logs.result();
    assert.equal(diagnostics.failures.length, 2);
    assert.match(JSON.stringify(diagnostics.raw), /closed/);
  } finally { logs.stop(); }
});
