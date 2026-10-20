// Launcher controls only; no browser, Runtime, build or vendor subprocess is run.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { pathToFileURL } from 'node:url';
import { createContext, SourceTextModule, SyntheticModule } from 'node:vm';
import { CURRENT013_COMPOSITION, CURRENT013_RUNTIME } from './current013-integration.mjs';

const launcher = new URL('./current013-parent-split.mjs', import.meta.url);
const source = readFileSync(launcher, 'utf8');
const input = { app: '/snapshot', appTree: 'a'.repeat(40), agent: '/retained/agent', runtime: '/retained/runtime',
  agentPython: '/venv-agent/bin/python', runtimePython: '/venv-runtime/bin/python',
  agentSha: 'd8749a9ce12a699672faf3ad96b4e4cbea9245c2', runtimeSha: CURRENT013_RUNTIME.commit };

async function load({ enabled = true, status = 0, moved = false, preflightFailure = false, launchFailure = false,
  agentSha = input.agentSha, cacheId } = {}) {
  const calls = [];
  const process = { env: enabled ? { TIMELINE_CURRENT013_RUN: '1' } : {}, argv: [], exitCode: undefined };
  const context = createContext({ process, URL });
  const module = new SourceTextModule(source, { context, identifier: launcher.href,
    initializeImportMeta(meta) { meta.url = launcher.href; } });
  let checks = 0;
  const selected = { ...input, agentSha };
  await module.link((specifier) => {
    let exports;
    if (specifier === 'node:crypto') exports = { createHash };
    else if (specifier === 'node:fs') exports = { readFileSync };
    else if (specifier === 'node:child_process') exports = { spawnSync: (...args) => {
      calls.push(args);
      if (launchFailure) throw new Error('child launch failed');
      return { status };
    } };
    else if (specifier === 'node:url') exports = { pathToFileURL };
    else {
      assert.equal(specifier, './current013-integration.mjs');
      exports = { CURRENT013_COMPOSITION, readCurrent013Inputs: () => selected, checkCurrent013Sources: (received) => {
        assert.equal(received, selected);
        checks++;
        if (preflightFailure) throw new Error('source guard refused');
        return { tree: moved && checks > 1 ? 'changed' : 'original' };
      } };
    }
    return new SyntheticModule(Object.keys(exports), function () {
      for (const [key, value] of Object.entries(exports)) this.setExport(key, value);
    }, { context });
  });
  await module.evaluate();
  process.env.TIMELINE_CURRENT013_CACHE_ID = cacheId ?? module.namespace.parentSplitCacheIdentity(selected);
  return { run: module.namespace.runCurrent013ParentSplit, process, calls, checks: () => checks,
    cacheIdentity: module.namespace.parentSplitCacheIdentity };
}

test('requires explicit enablement and the literal approved Agent before delegation', async () => {
  for (const options of [{ enabled: false }, { agentSha: 'b'.repeat(40) }]) {
    const probe = await load(options);
    assert.throws(probe.run, /manager-approved|requires Agent/);
    assert.equal(probe.checks(), 0);
    assert.equal(probe.calls.length, 0);
  }
});

test('cache identity binds the App tree, pair, client/public archive and launcher/helper bytes', async () => {
  const probe = await load({ cacheId: 'old-current013-m1-result' });
  assert.throws(probe.run, /CACHE_ID must identify/);
  const expected = probe.cacheIdentity(input);
  const hash = (url) => createHash('sha256').update(readFileSync(url)).digest('hex');
  assert.equal(expected, `parent-split-tree${input.appTree}-agent${input.agentSha}-runtime${input.runtimeSha}-client13-public12-${CURRENT013_COMPOSITION.sha256.slice(7)}-runner${hash(launcher)}-helper${hash(new URL('./current013-integration.mjs', import.meta.url))}`);
  assert.notEqual(probe.cacheIdentity({ ...input, appTree: 'c'.repeat(40) }), expected);
});

test('source guard refusal never launches the browser lane', async () => {
  const probe = await load({ preflightFailure: true });
  assert.throws(probe.run, /source guard refused/);
  assert.equal(probe.calls.length, 0);
});

test('delegates only parent-split config with validated inputs and checks both source boundaries', async () => {
  const probe = await load();
  probe.run();
  assert.equal(probe.checks(), 2);
  assert.equal(probe.calls.length, 1);
  const [command, args, options] = probe.calls[0];
  assert.equal(command, 'npm');
  assert.equal(JSON.stringify(args), JSON.stringify(['run', 'test:e2e:three-products', '--', '--config', 'playwright.clip-split.config.ts']));
  assert.equal(options.cwd, input.app);
  assert.equal(options.shell, false);
  assert.equal(options.env.TIMELINE_BUNDLE_AGENT_HEAD, input.agentSha);
  assert.equal(options.env.TIMELINE_BUNDLE_RUNTIME_HEAD, input.runtimeSha);
  for (const [name, value] of Object.entries({ ASTRID_CHECKOUT: input.agent, ASTRID_RUNTIME_CHECKOUT: input.runtime,
    ASTRID_PYTHON: input.agentPython, ASTRID_RUNTIME_PYTHON: input.runtimePython })) assert.equal(options.env[name], value);
  assert.equal(probe.process.exitCode, 0);
});

test('preserves child failure and postflight on launch errors or source movement', async () => {
  for (const status of [7, null]) {
    const probe = await load({ status });
    probe.run();
    assert.equal(probe.process.exitCode, status ?? 1);
    assert.equal(probe.checks(), 2);
  }
  for (const options of [{ moved: true }, { launchFailure: true }]) {
    const probe = await load(options);
    assert.throws(probe.run, options.moved ? /sources changed/ : /child launch failed/);
    assert.equal(probe.checks(), 2);
  }
});
