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
