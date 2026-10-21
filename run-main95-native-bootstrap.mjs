import { readFileSync, realpathSync } from 'node:fs';
import { execFileSync, spawnSync } from 'node:child_process';
import path from 'node:path';

const root = process.env.TIMELINE_APP_ROOT;
if (!root) throw new Error('TIMELINE_APP_ROOT is required');

const privateModules = realpathSync(process.env.TIMELINE_MAIN95_PRIVATE13_NODE_MODULES);
const app = (args, options = {}) => spawnSync(
  path.join(privateModules, '.bin/playwright'),
  args,
  { cwd: root, stdio: options.capture ? ['ignore', 'pipe', 'pipe'] : 'inherit', env: { ...process.env, NODE_PATH: undefined }, ...options },
);
const gitHead = (dir) => execFileSync('git', ['-C', dir, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
const gitTree = (dir) => execFileSync('git', ['-C', dir, 'rev-parse', 'HEAD^{tree}'], { encoding: 'utf8' }).trim();
const expectedAgent = '6efc81500a0e0688c2bb41e736503f0fc3e04abb';
const expectedRuntime = '95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c';
const expectedApp = 'ea5c9522f852735c9888f5b3a54b70f230351465';
const expectedAppTree = '0b193ba0d2f6dfa8d38ea51cd07c168191566e1d';

const provenance = JSON.parse(readFileSync(path.join(root, 'vendor/astrid-browser/provenance.json'), 'utf8'));
const lock = JSON.parse(readFileSync(path.join(root, 'runtime.lock.json'), 'utf8'));
if (provenance.astrid_commit !== expectedAgent || lock.source_commit !== expectedRuntime) {
  throw new Error(`Main95 tuple mismatch: Agent ${provenance.astrid_commit}, Runtime ${lock.source_commit}`);
}
if (gitTree(root) !== expectedAppTree) throw new Error('exact committed App tree is required');
if (gitTree(root) !== execFileSync('git', ['-C', root, 'rev-parse', `${expectedApp}^{tree}`], { encoding: 'utf8' }).trim()) {
  throw new Error('pinned App source commit/tree is unavailable');
}
if (!process.env.ASTRID_CHECKOUT || !process.env.ASTRID_RUNTIME_CHECKOUT) throw new Error('exact Agent/Runtime checkouts are required');
if (gitHead(process.env.ASTRID_CHECKOUT) !== expectedAgent || gitTree(process.env.ASTRID_CHECKOUT) !== process.env.TIMELINE_MAIN95_AGENT_TREE) {
  throw new Error('exact Agent checkout head/tree is required');
}
if (gitHead(process.env.ASTRID_RUNTIME_CHECKOUT) !== expectedRuntime || gitTree(process.env.ASTRID_RUNTIME_CHECKOUT) !== process.env.TIMELINE_MAIN95_RUNTIME_TREE) {
  throw new Error('exact Runtime checkout head/tree is required');
}

const cli = path.join(privateModules, '.bin/playwright');
const cliSource = realpathSync(cli);
const programSource = realpathSync(path.join(privateModules, 'playwright/lib/program.js'));
if (!cliSource.startsWith(`${privateModules}/`) || !programSource.startsWith(`${privateModules}/`) || cli === path.join(privateModules, '@playwright/test/cli.js')) {
  throw new Error(`Playwright CLI is not the private genuine bin: ${cliSource}`);
}
const version = spawnSync(cli, ['--version'], { cwd: root, encoding: 'utf8', env: { ...process.env, NODE_PATH: undefined } });
if (version.error || version.status !== 0 || version.stdout.trim() !== 'Version 1.60.0') {
  throw new Error(`unexpected private Playwright CLI version/source: ${version.error?.message ?? version.stdout + version.stderr}`);
}
console.log(`[main95-bootstrap] effective Playwright CLI ${cliSource}; ${version.stdout.trim()}`);

const config = 'playwright.main95-native-bootstrap.config.ts';
const list = app(['test', '--config', config, '--list'], { encoding: 'utf8', capture: true });
const discovery = `${list.stdout ?? ''}\n${list.stderr ?? ''}`;
process.stdout.write(discovery);
if (list.error) throw new Error(`Main95 bootstrap discovery could not start: ${list.error.message}`);
if (list.status !== 0) throw new Error(`Main95 bootstrap discovery failed (exit ${list.status ?? 'signal'})`);
if (!/Total:\s+1 test in 1 file/.test(discovery) || (discovery.match(/main95-native-bootstrap\.integration\.spec\.ts:/g) || []).length !== 1) {
  throw new Error(`expected exactly one Main95 bootstrap title discovery, got:\n${discovery}`);
}
console.log('[main95-bootstrap] discovered exactly one Main95 bootstrap test');

const run = app(['test', '--config', config]);
process.exit(run.status ?? 1);
