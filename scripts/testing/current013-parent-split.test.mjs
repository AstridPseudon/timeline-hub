// Launcher controls only; no browser, Runtime, build or vendor subprocess is run.
import assert from 'node:assert/strict';
import { readFileSync as hostReadFileSync } from 'node:fs';
import test from 'node:test';
import { pathToFileURL } from 'node:url';
import { createContext, SourceTextModule, SyntheticModule } from 'node:vm';

const launcher = new URL('./current013-parent-split.mjs', import.meta.url);
const source = hostReadFileSync(launcher, 'utf8');
const input = { app: '/snapshot', appTree: 'a'.repeat(40), agent: '/retained/agent', runtime: '/retained/runtime', runtimeProducer: '/retained/producer',
  agentPython: '/venv-agent/bin/python', runtimePython: '/venv-runtime/bin/python', agentSha: '8130a401bf44a518d5a40ae274d398b8c560be55', runtimeSha: '2c4ac180c2220bdad966bc01e95ad230e99ce26a' };

async function load({ enabled = true, status = 0, moved = false, preflightFailure = false, launchFailure = false, cacheId } = {}) {
  const calls = [];
  const process = { env: enabled ? { TIMELINE_CURRENT013_RUN: '1' } : {}, argv: [], exitCode: undefined, cwd: () => '/snapshot' };
  const context = createContext({ process, URL });
  const module = new SourceTextModule(source, { context, identifier: launcher.href, initializeImportMeta(meta) { meta.url = launcher.href; } });
  let checks = 0;
  await module.link((specifier) => {
    let exports;
    if (specifier === 'node:crypto') exports = { createHash: () => ({ update() { return this; }, digest: () => '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738' }) };
    else if (specifier === 'node:fs') exports = { readFileSync: () => Buffer.from(JSON.stringify({ artifacts: Object.fromEntries(Array.from({ length: 75 }, (_, i) => [`a${i}`, {}])) })), accessSync() {}, constants: { X_OK: 1 }, existsSync: () => true, realpathSync: (value) => value, statSync: () => ({ isFile: () => true, isDirectory: () => true }) };
    else if (specifier === 'node:child_process') exports = { execFileSync: (command, args = []) => {
      if (command === 'git' && args[2] === 'rev-parse') {
        const root = args[1]; const tree = args[3] === 'HEAD^{tree}';
        if (tree) return root.includes('agent') ? '236c3e57e0265c52b81ba8085de3193026176bff' : root.includes('runtime') ? '7ab412cc4bcbe517efcfa806e092336390312e18' : input.appTree;
        return root.includes('agent') ? input.agentSha : input.runtimeSha;
      }
      if (command === 'git' && args[2] === 'status') return '';
      if (command === 'tar') return Array.from({ length: 77 }, (_, i) => `package/file${i}`).join('\n');
      throw new Error(`unexpected command ${command}`);
    }, spawnSync: (...args) => { calls.push(args); if (launchFailure) throw new Error('child launch failed'); return { status }; } };
    else if (specifier === 'node:path') exports = { default: { isAbsolute: () => true, join: (...parts) => parts.join('/') } };
    else if (specifier === 'node:url') exports = { pathToFileURL };
    else throw new Error(`unexpected import ${specifier}`);
    return new SyntheticModule(Object.keys(exports), function () { for (const [key, value] of Object.entries(exports)) this.setExport(key, value); }, { context });
  });
  await module.evaluate();
  process.env.TIMELINE_CURRENT013_APP_TREE = preflightFailure ? 'b'.repeat(40) : input.appTree;
  process.env.TIMELINE_CURRENT013_AGENT_SHA = input.agentSha;
  process.env.TIMELINE_CURRENT013_RUNTIME_SHA = input.runtimeSha;
  process.env.ASTRID_CHECKOUT = input.agent; process.env.ASTRID_RUNTIME_CHECKOUT = input.runtime;
  process.env.TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT = input.runtimeProducer;
  process.env.ASTRID_PYTHON = input.agentPython; process.env.ASTRID_RUNTIME_PYTHON = input.runtimePython;
  process.env.PRIVATE13_NODE_MODULES = '/private/node_modules'; process.env.TIMELINE_CURRENT013_PRIVATE13_READY = '/private/READY'; process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE = '/browser/chrome';
  process.env.TIMELINE_CURRENT013_CACHE_ID = cacheId ?? module.namespace.parentSplitCacheIdentity(input);
  return { run: module.namespace.runCurrent013ParentSplit, process, calls, checks: () => checks, cacheIdentity: module.namespace.parentSplitCacheIdentity };
}

test('requires explicit enablement and binds cache identity to source and pair', async () => {
  const disabled = await load({ enabled: false });
  assert.throws(disabled.run, /manager-approved/);
  const stale = await load({ cacheId: 'old-cache' });
  assert.throws(stale.run, /CACHE_ID/);
  assert.notEqual(stale.cacheIdentity({ ...input, appTree: 'b'.repeat(40) }), stale.cacheIdentity(input));
});

test('source guard refusal never launches the browser lane', async () => {
  const probe = await load({ preflightFailure: true });
  assert.throws(probe.run, /App tree changed/);
  assert.equal(probe.calls.length, 0);
});

test('delegates only the named parent-split config and preserves child status', async () => {
  const probe = await load();
  probe.run();
  assert.equal(JSON.stringify(probe.calls[0][1]), JSON.stringify(['run', 'test:e2e:three-products', '--', '--config', 'playwright.parent-split.config.ts']));
  assert.equal(probe.process.exitCode, 0);
});

test('cache remains source-bound when the child fails', async () => {
  const probe = await load({ status: 7 });
  assert.equal(probe.cacheIdentity(input).includes('agent8130a401'), true);
  assert.equal(probe.process.exitCode, undefined);
});
