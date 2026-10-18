import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { DirectHarness, spawnGroup, stopGroup } from './harness.ts';
import { loadQuickDescriptor, parseQuickDescriptor } from './quick-descriptor.ts';

const valid = {
  version: 1,
  dataRoot: '/tmp/quick/data', sourceManifest: '/tmp/quick/source.json', discoveryFile: '/tmp/quick/support/discovery.json',
  productCredentialFile: '/tmp/quick/product.json', astridCredentialFile: '/tmp/quick/astrid.json',
  projectId: 'project-id', projectSlug: 'project-slug', timelineId: 'timeline-id', headRevisionId: 'head-id',
  realmId: 'realm-id', runtimeInstanceId: 'runtime-instance-id',
  revisions: { astrid: 'a'.repeat(40), runtime: 'b'.repeat(40), app: 'c'.repeat(40) },
  resultFile: '/tmp/quick/result.json',
};

describe('QUICK descriptor and attachment support', () => {
  it('accepts version 1 absolute paths and all three pinned revisions', () => {
    assert.deepEqual(parseQuickDescriptor(JSON.stringify(valid)), valid);
  });

  it('rejects invalid JSON, non-objects, and unsupported versions', () => {
    assert.throws(() => parseQuickDescriptor('{'), /valid JSON/);
    assert.throws(() => parseQuickDescriptor('[]'), /JSON object/);
    assert.throws(() => parseQuickDescriptor(JSON.stringify({ ...valid, version: 2 })), /version must be 1/);
  });

  it('rejects missing fields, relative paths, and malformed Git SHAs', () => {
    assert.throws(() => parseQuickDescriptor(JSON.stringify({ ...valid, projectId: '' })), /projectId/);
    assert.throws(() => parseQuickDescriptor(JSON.stringify({ ...valid, sourceManifest: 'source.json' })), /sourceManifest.*absolute/);
    assert.throws(() => parseQuickDescriptor(JSON.stringify({ ...valid, revisions: { ...valid.revisions, app: 'main' } })), /revisions.app/);
  });

  it('loads a private regular descriptor file and rejects symlinks or broad permissions', () => {
    const dir = mkdtempSync(path.join(tmpdir(), 'quick-descriptor-test-'));
    const file = path.join(dir, 'descriptor.json');
    const link = path.join(dir, 'descriptor-link.json');
    try {
      writeFileSync(file, JSON.stringify(valid), { mode: 0o600 });
      chmodSync(file, 0o600);
      assert.deepEqual(loadQuickDescriptor(file), valid);
      chmodSync(file, 0o644);
      assert.throws(() => loadQuickDescriptor(file), /group or others/);
      symlinkSync(file, link);
      assert.throws(() => loadQuickDescriptor(link), /regular file, not a symlink/);
    } finally { rmSync(dir, { recursive: true, force: true }); }
  });

  it('preserves the explicit adopted Astrid data root in an exact child environment', async () => {
    const child = spawnGroup(process.execPath, ['-e', 'process.stdout.write(process.env.ASTRID_RUNTIME_DATA_ROOT ?? "missing")'], {
      cwd: process.cwd(), exactEnv: true, env: { PATH: process.env.PATH, ASTRID_RUNTIME_DATA_ROOT: '/adopted/runtime-root' },
    });
    await child.exited;
    await stopGroup(child);
    await child.closed;
    assert.equal(child.stdout, '/adopted/runtime-root');
  });

  it('attaches without creating, stopping, or removing F1-owned Runtime state', async () => {
    const dir = mkdtempSync(path.join(tmpdir(), 'quick-attachment-test-'));
    const dataRoot = path.join(dir, 'f1-data');
    const support = path.join(dataRoot, 'runtime');
    const credentials = path.join(dataRoot, 'credentials');
    mkdirSync(support, { recursive: true });
    mkdirSync(credentials, { recursive: true });
    const sentinel = path.join(dataRoot, 'f1-owned.txt');
    writeFileSync(sentinel, 'F1 owns this');
    const realmId = 'f1-realm';
    const runtimeInstanceId = 'f1-runtime-instance';
    const runtime = createServer((request, response) => {
      response.setHeader('Content-Type', 'application/json');
      if (request.url === '/v1/health') return response.end(JSON.stringify({ realm_id: realmId, runtime_instance_id: runtimeInstanceId }));
      if (request.url === '/v1/projects/project-id') return response.end(JSON.stringify({ data: { name: 'Quick Project', slug: 'project-slug' } }));
      response.statusCode = 404;
      response.end('{}');
    });
    await new Promise<void>((resolve) => runtime.listen(0, '127.0.0.1', resolve));
    const endpoint = `http://127.0.0.1:${(runtime.address() as { port: number }).port}`;
    const discoveryFile = path.join(support, 'discovery.json');
    const productCredentialFile = path.join(credentials, 'product.json');
    const astridCredentialFile = path.join(credentials, 'astrid.json');
    writeFileSync(discoveryFile, JSON.stringify({ endpoint, active_realm: realmId, runtime_instance_id: runtimeInstanceId, worker_credential_file: path.join(credentials, 'worker.json'), worker_actor: 'worker' }));
    writeFileSync(productCredentialFile, JSON.stringify({ token: 'product-token', actor_id: 'product' }));
    writeFileSync(astridCredentialFile, JSON.stringify({ token: 'astrid-token', actor_id: 'astrid-f2' }));
    const descriptorFile = path.join(dir, 'descriptor.json');
    writeFileSync(descriptorFile, JSON.stringify({ ...valid, dataRoot, sourceManifest: path.join(support, 'source.json'), discoveryFile, productCredentialFile, astridCredentialFile, realmId, runtimeInstanceId }), { mode: 0o600 });
    chmodSync(descriptorFile, 0o600);
    const previousDescriptor = process.env.ASTRID_QUICK_DESCRIPTOR;
    process.env.ASTRID_QUICK_DESCRIPTOR = descriptorFile;
    const harness = new DirectHarness();
    const forbidden = () => { throw new Error('attachment must not create or start another Runtime'); };
    Object.assign(harness, { createRealm: forbidden, startRuntime: forbidden, seedRuntime: forbidden });
    Object.assign(harness, { startGateway: async () => {
      harness.gatewayBase = 'http://127.0.0.1:17340/api/runtime';
      return { base: harness.gatewayBase, realm_id: realmId, acp: false };
    } });
    try {
      await harness.start();
      assert.equal(harness.attachment?.realmId, realmId);
      assert.equal(harness.quickSeed?.projectName, 'Quick Project');
      await harness.stopRuntime();
      await harness.stop();
      assert.equal(existsSync(sentinel), true);
      assert.equal(readFileSync(sentinel, 'utf8'), 'F1 owns this');
      const health = await fetch(`${endpoint}/v1/health`);
      assert.equal(health.status, 200);
    } finally {
      await harness.stop().catch(() => {});
      if (previousDescriptor === undefined) delete process.env.ASTRID_QUICK_DESCRIPTOR;
      else process.env.ASTRID_QUICK_DESCRIPTOR = previousDescriptor;
      await new Promise<void>((resolve, reject) => runtime.close((error) => error ? reject(error) : resolve()));
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
