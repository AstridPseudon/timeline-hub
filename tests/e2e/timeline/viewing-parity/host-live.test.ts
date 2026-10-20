import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { lstat, readFile, writeFile } from 'node:fs/promises';
import { isAbsolute, join } from 'node:path';
import { test } from 'node:test';
import { DirectHarness } from '../../local/support/harness';
import { startRealPackHost, type PackHostSession } from './bootstrap';
import { readRuntimeJson } from './fixture';
import { assertSourceVersionsUnchanged, readyRenderCapability, sourceVersions } from './harness';

function committedSource(root: string, expected: string | undefined): { revision: string; tree: string } {
  assert.match(expected ?? '', /^[0-9a-f]{40}$/, 'manager must select a full committed source revision');
  const git = (...args: string[]) => execFileSync('git', args, { cwd: root, encoding: 'utf8' }).trim();
  const revision = git('rev-parse', 'HEAD');
  assert.equal(revision, expected, 'source differs from manager-selected revision');
  assert.equal(git('status', '--porcelain', '--untracked-files=normal'), '', 'selected source must be clean');
  return { revision, tree: git('rev-parse', 'HEAD^{tree}') };
}

async function assertNoHost(support: string, pid?: number): Promise<void> {
  for (const name of ['generic-host.json', 'generic-host.ready.json']) {
    await assert.rejects(lstat(join(support, name)), { code: 'ENOENT' });
  }
  if (pid !== undefined) {
    // Signal zero only observes existence. Cleanup belongs entirely to the helper.
    assert.throws(() => process.kill(pid, 0), { code: 'ESRCH' }, 'owned host leader survived');
    assert.throws(() => process.kill(-pid, 0), { code: 'ESRCH' }, 'owned host group survived');
  }
}

// Central named suite only, after the manager grants the final Agent source.
test('actual App pack-host wrapper joins the live Runtime catalog and cleans its owned host',
  { timeout: 420_000 }, async () => {
    assert.equal(process.platform, 'linux');
    assert.equal(process.version, 'v20.19.4');
    const proofPath = process.env.VIEWING_HOST_PROOF_PATH;
    assert.ok(proofPath && isAbsolute(proofPath), 'parent must select an absolute proof output');
    const before = await sourceVersions();
    const selected = {
      agent: committedSource(before.roots.agent, process.env.VIEWING_HOST_AGENT_REVISION),
      runtime: committedSource(before.roots.runtime, process.env.VIEWING_HOST_RUNTIME_REVISION),
      composition: committedSource(before.roots.composition, process.env.VIEWING_HOST_COMPOSITION_REVISION),
    };
    assert.ok((await lstat(join(before.roots.agent, 'tests/packs/rendering/real_pack_host.py'))).isFile());
    const parentEnvironment = Object.fromEntries([
      'HOME', 'LANG', 'PATH', 'ASTRID_CHECKOUT', 'ASTRID_PYTHON', 'ASTRID_PACK_HOST_PYTHON',
      'ASTRID_RUNTIME_CHECKOUT', 'ASTRID_RUNTIME_PYTHON', 'ASTRID_NODE_EXECUTABLE',
      'ASTRID_REMOTION_PROJECT_DIR', 'ASTRID_REMOTION_BROWSER_EXECUTABLE',
      'ASTRID_TIMELINE_SCHEMA_PYTHONPATH', 'TIMELINE_COMPOSITION_CHECKOUT',
    ].map(name => [name, process.env[name]]));
    const proof = { sources: before, selected, parentEnvironment, lifecycle: ['graph-preflight'] };
    await writeFile(proofPath, JSON.stringify(proof, null, 2) + '\n');

    // No browser, build, render task or parity media fixture is needed here.
    const harness = new DirectHarness();
    let host: PackHostSession | undefined;
    try {
      await harness.start();
      await assertNoHost(harness.supportDir);
      const discovery = harness.discovery();
      assert.equal(discovery.runtime_instance_id, harness.runtimeInstanceId);
      assert.equal(discovery.endpoint, harness.runtimeUrl);
      const invocation = {
        executable: process.env.ASTRID_PYTHON, cwd: before.roots.agent,
        args: ['-m', 'tests.packs.rendering.real_pack_host',
          '--realm-dir', harness.realmDir, '--support-dir', harness.supportDir,
          '--discovery-file', join(harness.supportDir, 'discovery.json'),
          '--source-checkout', before.roots.agent, '--runtime-instance-id', harness.runtimeInstanceId],
        runtimeEnvironment: harness.runtimeEnv(),
      };
      let registration: Record<string, unknown> | undefined;
      host = await startRealPackHost(harness, async () => {
        await readyRenderCapability(harness);
        registration = JSON.parse(await readFile(join(harness.supportDir, 'generic-host.json'), 'utf8'));
        assert.equal(registration!.source_checkout, before.roots.agent);
        assert.equal(registration!.runtime_instance_id, harness.runtimeInstanceId);
        assert.equal(registration!.executor_id, 'astrid-pack-host');
        assert.ok(Number.isSafeInteger(registration!.pid) && Number(registration!.pid) > 0);
      });
      const capability = await readyRenderCapability(harness);
      proof.lifecycle.push('live-catalog-rendering.render-ready');
      const pid = Number(registration!.pid);
      await host.stop(); // Requires matching stopped acknowledgement AND helper exit 0.
      proof.lifecycle.push('stop-stopped-exit0');
      await assertNoHost(harness.supportDir, pid);
      assert.ok(harness.runtimeRunning);
      const health = await readRuntimeJson<{ runtime_instance_id: string }>(harness, '/v1/health');
      assert.equal(health.runtime_instance_id, harness.runtimeInstanceId);
      proof.lifecycle.push('host-and-registration-absent-runtime-healthy');
      const after = await sourceVersions();
      assertSourceVersionsUnchanged(before, after);
      assert.deepEqual({
        agent: committedSource(after.roots.agent, process.env.VIEWING_HOST_AGENT_REVISION),
        runtime: committedSource(after.roots.runtime, process.env.VIEWING_HOST_RUNTIME_REVISION),
        composition: committedSource(after.roots.composition, process.env.VIEWING_HOST_COMPOSITION_REVISION),
      }, selected);
      await writeFile(proofPath, JSON.stringify({ ...proof, invocation, capability,
        runtimeInstanceId: harness.runtimeInstanceId, host: {
          pid, sourceDigest: registration!.source_checkout_digest,
          closureDigest: registration!.source_closure_digest,
          inventoryIdentity: registration!.source_inventory_identity,
          bootManifestHash: registration!.boot_manifest_hash,
        },
      }, null, 2) + '\n');
    } finally {
      try { await host?.stop(); } finally { await harness.stop(); }
    }
  });
