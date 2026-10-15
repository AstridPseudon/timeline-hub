import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { ACP_ROUTES, buildAcpPath } from '../src/integrations/astrid/acpRouteContract.ts';

test('ACP path parameters and query values remain separate encoded values', () => {
  assert.equal(
    buildAcpPath('unassignedProjectSessions', { projectId: 'project /?#' }, { connection_id: 'connection /?&=' }),
    '/acp/projects/project%20%2F%3F%23/chat/unassigned?connection_id=connection%20%2F%3F%26%3D',
  );
  assert.equal(buildAcpPath('connect'), '/acp/connect');
  assert.throws(() => buildAcpPath('projectChat'), /Missing ACP route parameter: projectId/);
});

test('every direct ACP transport call takes its path and method from the shared contract', () => {
  const source = readFileSync(new URL('../src/integrations/astrid/acpRoutes.ts', import.meta.url), 'utf8');
  const calls = [...source.matchAll(/\.requestJson\(buildAcpPath\('([^']+)'/g)].map(match => match[1]);
  const methods = [...source.matchAll(/method: ACP_ROUTES\.([A-Za-z]+)\.method/g)].map(match => match[1]);
  assert.equal(calls.length, [...source.matchAll(/\.requestJson\(/g)].length);
  assert.deepEqual(calls, methods);
  assert.deepEqual([...calls].sort(), Object.keys(ACP_ROUTES).sort());
});
