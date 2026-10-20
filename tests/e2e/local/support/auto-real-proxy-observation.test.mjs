import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { compileFunction } from 'node:vm';
import ts from 'typescript';

const source = readFileSync(new URL('../auto-real-proxy.spec.ts', import.meta.url), 'utf8');
const constants = source.match(/^const (?:NATIVE_RUNTIME_COMMIT|TASK_API_POST|LEGACY_POST) = [^;]+;/gm);
assert.equal(constants?.length, 3, 'traffic classifier constants must remain source-visible');
const helper = source.match(/^function classifyRuntimePost\([^]*?^}/m)?.[0];
assert.ok(helper, 'traffic classifier helper must remain source-visible');
const classifyRuntimePost = compileFunction(
  `${constants.join('\n')}\n${ts.transpileModule(helper, {}).outputText}\nreturn classifyRuntimePost;`,
  [],
)();

const inverseHelpers = source.match(/^function normalRuntimeCommitPath\([^]*?^}\n\nfunction isExpectedInverseRequest\([^]*?^}/m)?.[0];
assert.ok(inverseHelpers, 'inverse request matcher must remain source-visible');
const isExpectedInverseRequest = compileFunction(
  `${ts.transpileModule(inverseHelpers, {}).outputText}\nreturn isExpectedInverseRequest;`,
  [],
)();

const headHelper = source.match(/^function requireAuthoritativeHead\([^]*?^}/m)?.[0];
assert.ok(headHelper, 'authoritative head helper must remain source-visible');
const requireAuthoritativeHead = compileFunction(
  `${ts.transpileModule(headHelper, {}).outputText}\nreturn requireAuthoritativeHead;`,
  [],
)();

function request(url, method, body) {
  return { method: () => method, url: () => url, postDataJSON: () => body };
}

const projectId = 'project-control';
const timelineId = 'timeline-control';
const publicationId = 'publication-control';
const commitPath = `/api/runtime/v1/projects/${projectId}/timelines/${timelineId}/commit`;
const inverseBody = {
  api_version: 1,
  project_id: projectId,
  timeline_id: timelineId,
  base_revision_id: 'revision-control',
  base_publication_id: 'publication-base-control',
  commands: [{
    schema_version: 1,
    op: 'timeline.inverse',
    version: '1',
    select: null,
    args: { publications: [publicationId] },
  }],
  source: { via: 'app' },
};

test('pure: exact native inverse matcher keeps its positive and 11 negative controls', () => {
  assert.equal(isExpectedInverseRequest(request(`https://app.test${commitPath}`, 'POST', inverseBody), projectId, timelineId, publicationId), true);
  const negatives = [
    ['wrong method', request(`https://app.test${commitPath}`, 'GET', inverseBody)],
    ['wrong path scope', request(`https://app.test/api/runtime/v1/projects/other/timelines/${timelineId}/commit`, 'POST', inverseBody)],
    ['wrong body project', request(`https://app.test${commitPath}`, 'POST', { ...inverseBody, project_id: 'other' })],
    ['wrong body timeline', request(`https://app.test${commitPath}`, 'POST', { ...inverseBody, timeline_id: 'other' })],
    ['operation-route lookalike', request(`https://app.test/runtime-config/v1/operation/runtime/v1/projects/${projectId}/timelines/${timelineId}/commit`, 'POST', inverseBody)],
    ['query lookalike', request(`https://app.test${commitPath}?lookalike=1`, 'POST', inverseBody)],
    ['empty base pin', request(`https://app.test${commitPath}`, 'POST', { ...inverseBody, base_revision_id: '' })],
    ['wrong publication', request(`https://app.test${commitPath}`, 'POST', { ...inverseBody, commands: [{ ...inverseBody.commands[0], args: { publications: ['other'] } }] })],
    ['two inverse commands', request(`https://app.test${commitPath}`, 'POST', { ...inverseBody, commands: [inverseBody.commands[0], inverseBody.commands[0]] })],
    ['extra body field', request(`https://app.test${commitPath}`, 'POST', { ...inverseBody, extra: true })],
    ['legacy publish route', request(`https://app.test/api/runtime/v1/projects/p/timelines/t/composition-revisions/publish`, 'POST', inverseBody)],
  ];
  for (const [label, candidate] of negatives) assert.equal(isExpectedInverseRequest(candidate, projectId, timelineId, publicationId), false, label);
});

test('pure: traffic controls classify native, task, and every retired publisher path explicitly', () => {
  const nativeCommit = `/api/runtime/v1/projects/p/timelines/t/commit`;
  assert.equal(classifyRuntimePost('POST', nativeCommit), 'native-commit', 'valid native inverse commit is not legacy traffic');

  const taskApi = [
    '/api/runtime/v1/tasks',
    '/api/runtime/v1/tasks/task-1/cancel',
    '/api/runtime/v1/tasks/task-1/retry',
    '/api/runtime/v1/managed-outputs/output-1/export',
  ];
  for (const path of taskApi) assert.equal(classifyRuntimePost('POST', path), 'task-api', `legitimate task API: ${path}`);

  const retiredPublishers = [
    '/api/runtime/v1/projects/p/timelines/t/composition-revisions',
    '/api/runtime/v1/projects/p/timelines/t/composition-revisions/publish',
    '/api/runtime/v1/projects/p/timelines/t/composition-revisions/canonical',
    '/api/runtime/v1/proxiedv1/projects/p/timelines/t/composition-revisions',
    '/api/runtime/legacy/projects/p/timelines/t/composition-revisions',
  ];
  for (const path of retiredPublishers) assert.equal(classifyRuntimePost('POST', path), 'legacy-writer', `retired publisher: ${path}`);

  for (const [method, path, expected] of [
    ['GET', nativeCommit, 'other'],
    ['POST', `${nativeCommit}/extra`, 'legacy-writer'],
    ['POST', '/api/runtime/v1/projects/p/timelines/t/committ', 'legacy-writer'],
    ['POST', '/api/astrid/v1/projects/p/timelines/t/composition-revisions', 'other'],
  ]) assert.equal(classifyRuntimePost(method, path), expected, `${method} ${path}`);
});

test('pure: authoritative head uses the Runtime pair when an older revision is reused', () => {
  assert.deepEqual(requireAuthoritativeHead({
    items: [
      { revision_id: 'newer-irrelevant-revision', is_current_head: false },
      { revision_id: 'reused-older-head', is_current_head: true },
    ],
    head: { revision_id: 'reused-older-head', publication_id: 'reused-head-publication' },
  }), { revision_id: 'reused-older-head', publication_id: 'reused-head-publication' });
});

test('pure: authoritative head refuses a missing or incomplete Runtime pair', () => {
  for (const body of [{}, { head: null }, { head: { revision_id: 'revision-only' } }, { head: { publication_id: 'publication-only' } }]) {
    assert.throws(() => requireAuthoritativeHead(body), /authoritative head pair/);
  }
});
