import assert from 'node:assert/strict';
import test from 'node:test';
import { WorkspaceClient } from '../src/generated.ts';

test('generated selection read encodes selectors once and returns exact server tuple', async () => {
  const calls = [];
  const result = { asset: '音/&+?% ', generation_id: 'g/ +', variant_id: 'v?#', object_id: 'sha256:' + 'a'.repeat(64), catalog_digest: 'sha256:' + 'b'.repeat(64) };
  const transport = async (method, path, headers, body) => {
    calls.push({ method, path, headers, body });
    return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(result)) };
  };
  const client = new WorkspaceClient('http://unused', 'reader', transport);
  assert.deepEqual(await client.getProjectMediaSelection('p/ +', result.asset, result.generation_id, result.variant_id), result);
  assert.equal(calls[0].method, 'GET');
  assert.equal(calls[0].body, undefined);
  assert.equal(calls[0].headers.Authorization, 'Bearer reader');
  const url = new URL(calls[0].path, 'http://unused');
  assert.equal(url.pathname, '/v1/projects/p%2F%20%2B/media-selection');
  assert.deepEqual([...url.searchParams], [['asset', result.asset], ['generation_id', result.generation_id], ['variant_id', result.variant_id]]);
});

test('captured output selector helper preserves exact tuple across retries', async () => {
  const calls = [];
  const result = { asset: 'variant/音', generation_id: 'generation', variant_id: 'variant/音', object_id: 'sha256:' + 'a'.repeat(64), catalog_digest: 'sha256:' + 'b'.repeat(64) };
  const client = new WorkspaceClient('http://unused', 'reader', async (method, path, headers, body) => {
    calls.push({ method, path, headers, body });
    return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(result)) };
  });
  const selectors = { association_id: 'output/音 +&', object_id: result.object_id, version: 3 };
  assert.deepEqual(await client.getProjectMediaSelectionForOutput('p/ +', selectors), result);
  assert.deepEqual(await client.getProjectMediaSelectionForOutput('p/ +', selectors), result);
  assert.deepEqual(calls[0], calls[1]);
  assert.equal(calls[0].method, 'GET');
  assert.equal(calls[0].body, undefined);
  const url = new URL(calls[0].path, 'http://unused');
  assert.equal(url.pathname, '/v1/projects/p%2F%20%2B/media-selection');
  assert.deepEqual([...url.searchParams], [['association_id', selectors.association_id], ['object_id', selectors.object_id], ['version', '3']]);
  for (const version of [0, -1, 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1]) {
    await assert.rejects(() => client.getProjectMediaSelectionForOutput('p', { ...selectors, version }));
  }
  assert.equal(calls.length, 2);
});
