// No service or App dependencies: exercise the exact generated product artifact.
import assert from 'node:assert/strict';
import test from 'node:test';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const source = process.env.TIMELINE_COMMIT_CLIENT
  ? pathToFileURL(process.env.TIMELINE_COMMIT_CLIENT).href
  : new URL('../src/generated.ts', import.meta.url).href;
const { WorkspaceClient } = await import(source);
const fixture = JSON.parse(readFileSync(new URL('../../../conformance/fixtures/timeline-commit-candidate.json', import.meta.url)));
const value = id => structuredClone(fixture.cases.find(c => c.id === id).value);

for (const [http, id] of [[200, 'CC-RESULT-PREVIEW'], [200, 'CC-RESULT-CONFLICT'], [400, 'CC-HTTP-400-REQUEST_ID_CONFLICT'], [503, 'CC-RESULT-UNAVAILABLE']]) {
  test(`CC-TS-${http}-${id}: exact retry, headers, opaque JSON, typed result`, async () => {
    const calls = [];
    const result = value(id);
    const transport = async (method, path, headers, body) => {
      calls.push({ method, path, headers, body: JSON.parse(new TextDecoder().decode(body)) });
      return { status: http, headers: {}, body: new TextEncoder().encode(JSON.stringify(result)) };
    };
    const client = new WorkspaceClient('http://unused', 'test-token', transport);
    const request = value('CC-REQ-DRY-RUN');
    request.project_id = 'p/with space';
    request.timeline_id = 't?#';
    request.change = { document: { 'opaque:future': [null, false, { preserve: true }] }, adapter: 'sheet' };
    const before = structuredClone(request);
    assert.deepEqual(await client.commitTimeline(request), result);
    assert.deepEqual(await client.commitTimeline(request), result);
    assert.deepEqual(calls[0], calls[1]);
    assert.deepEqual(request, before);
    assert.deepEqual(calls[0].body, request);
    assert.equal(calls[0].method, 'POST');
    assert.equal(calls[0].path, `/astrid/v1/projects/${encodeURIComponent(request.project_id)}/timelines/${encodeURIComponent(request.timeline_id)}/commit`);
    assert.equal(calls[0].headers['Idempotency-Key'], request.request_id);
    assert.equal(calls[0].headers['X-Astrid-Session'], request.session_id);
    assert.equal(calls[0].headers.Authorization, 'Bearer test-token');
    assert.equal('publisher' in calls[0].body, false);
  });
}
