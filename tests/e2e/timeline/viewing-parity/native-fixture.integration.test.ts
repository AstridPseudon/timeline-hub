import assert from 'node:assert/strict';
import { execFileSync, spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, realpathSync, statfsSync } from 'node:fs';
import { cp, mkdir, mkdtemp, readdir, readFile, rename, rm, stat, symlink, unlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { basename, delimiter, join, relative } from 'node:path';
import { test } from 'node:test';
import { AstridLocalClient } from '../../../../src/integrations/astrid/client';
import type { Task } from '../../../../src/integrations/runtime/generated';
import { assertTaskAuthority } from './authority';

const FROZEN_SOURCES = {
  runtime: {
    root: '/home/user/work/wt/rt-pin-2c4ac180',
    commit: '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
    label: 'rt-pin/official013',
  },
  agent: {
    root: '/home/user/work/wt/agt-pin-973c082e',
    commit: '973c082e451844aeca399ac4d8a04f3039216cc0',
    label: 'agt-pin/reviewed973',
  },
} as const;

type FrozenSource = (typeof FROZEN_SOURCES)[keyof typeof FROZEN_SOURCES];

function git(root: string, ...args: string[]): string {
  return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8' }).trim();
}

async function sourceManifest(root: string): Promise<{ files: number; sha256: string }> {
  const entries: string[] = [];
  async function visit(directory: string): Promise<void> {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      if (entry.name === '__pycache__' || entry.name.endsWith('.pyc')) continue;
      const absolute = join(directory, entry.name);
      if (entry.isDirectory()) await visit(absolute);
      else {
        assert.equal(entry.isFile(), true, `frozen source contains non-file ${absolute}`);
        const digest = createHash('sha256').update(await readFile(absolute)).digest('hex');
        entries.push(`${relative(root, absolute)}\0${digest}`);
      }
    }
  }
  await visit(root);
  entries.sort();
  return { files: entries.length, sha256: createHash('sha256').update(entries.join('\n')).digest('hex') };
}

async function archiveFrozenSources(directory: string) {
  const archived = {} as Record<keyof typeof FROZEN_SOURCES, { root: string; tree: string; archiveSha256: string; manifest: { files: number; sha256: string } }>;
  for (const [name, source] of Object.entries(FROZEN_SOURCES) as Array<[keyof typeof FROZEN_SOURCES, FrozenSource]>) {
    assert.equal(git(source.root, 'rev-parse', source.commit), source.commit, `${name} frozen commit is unavailable`);
    const tree = git(source.root, 'rev-parse', `${source.commit}^{tree}`);
    const archive = execFileSync('git', ['-C', source.root, 'archive', '--format=tar', source.commit], { maxBuffer: 512 * 1024 * 1024 });
    const root = join(directory, name);
    execFileSync('mkdir', ['-p', root]);
    execFileSync('tar', ['-xf', '-', '-C', root], { input: archive });
    archived[name] = { root, tree, archiveSha256: createHash('sha256').update(archive).digest('hex'), manifest: await sourceManifest(root) };
  }
  return archived;
}

function pythonSourceProof(python: string, runtime: string, agent: string) {
  const output = execFileSync(python, ['-B', '-c', [
    'import astrid, json, runtime_protocol, sys',
    'print(json.dumps({"astrid": astrid.__file__, "runtime_protocol": runtime_protocol.__file__, "sys_path": sys.path}))',
  ].join(';')], {
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: [runtime, agent].join(delimiter) },
    encoding: 'utf8',
  });
  const proof = JSON.parse(output.trim()) as { astrid: string; runtime_protocol: string; sys_path: string[] };
  assert.equal(proof.astrid.startsWith(`${agent}/`), true, `Agent module escaped frozen archive: ${proof.astrid}`);
  assert.equal(proof.runtime_protocol.startsWith(`${runtime}/`), true,
    `Runtime module escaped frozen archive: ${proof.runtime_protocol}`);
  assert.deepEqual(proof.sys_path.filter(path => path === runtime || path === agent), [runtime, agent]);
  return proof;
}

const QUALIFIED_NODE_SHA256 = '43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490';
const QUALIFIED_CHROME_SHA256 = 'cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76';
const QUALIFIED_HOST_ENV = {
  ASTRID_REMOTION_PROJECT_DIR: '/tmp/vw-m3-public13-host-one-root-catalog-stage/remotion',
  ASTRID_NODE_EXECUTABLE: '/tmp/vw-m3-public13-host-one-root-catalog-stage/toolchain/node-v20.19.4-linux-x64/bin/node',
  ASTRID_REMOTION_BROWSER_EXECUTABLE: '/opt/google/chrome/chrome',
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH: '/home/user/work/venv-agent/lib/python3.11/site-packages',
} as const;
const BROWSER_LOCK = '/tmp/timeline-viewing-browser.lock';
const MIN_FREE_BYTES = 10 * 1024 * 1024 * 1024;
const ARTIFACT_ROOT = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-three-media-public13-mp4';

function assertFreeDiskFloor(path: string): void {
  const stats = statfsSync(path);
  assert.ok(stats.bavail * stats.bsize >= MIN_FREE_BYTES,
    `free disk below 10 GiB floor at ${path}: ${stats.bavail * stats.bsize} bytes`);
}

function acquireBrowserLock(): ReturnType<typeof spawn> {
  const locker = spawn('flock', ['-x', BROWSER_LOCK, 'sleep', '300'], { stdio: 'ignore' });
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const probe = spawnSync('flock', ['-n', BROWSER_LOCK, 'true'], { stdio: 'ignore' });
    if (probe.status !== 0) return locker;
    spawnSync('sleep', ['0.05'], { stdio: 'ignore' });
  }
  locker.kill('SIGTERM');
  assert.fail(`could not acquire ${BROWSER_LOCK}`);
}

function artifactPath(name: string): string {
  return join(ARTIFACT_ROOT, name);
}

function compositionArtifactProof(root: string): { sha256: string; members: number } {
  const artifact = join(root, 'remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz');
  const members = execFileSync('tar', ['-tzf', artifact], { encoding: 'utf8' }).trim().split('\n').filter(Boolean);
  return { sha256: createHash('sha256').update(readFileSync(artifact)).digest('hex'), members: members.length };
}

function assertProcessGroupGone(pid: number): void {
  try {
    process.kill(-pid, 0);
  } catch (error) {
    const code = (error as NodeJS.ErrnoException).code;
    if (code === 'ESRCH') return;
    throw error;
  }
  assert.fail(`owned pack-host process group ${pid} survived cleanup`);
}

function qualifiedToolchainProof(): { node: { path: string; sha256: string }; browser: { path: string; version: string; sha256: string } } {
  const node = requiredPath('ASTRID_NODE_EXECUTABLE');
  const browser = requiredPath('ASTRID_REMOTION_BROWSER_EXECUTABLE');
  const version = execFileSync(browser, ['--product-version'], { encoding: 'utf8' }).trim();
  assert.equal(version, '155.0.8059.84', `unexpected Chrome155 version: ${version}`);
  const browserSha256 = createHash('sha256').update(readFileSync(browser)).digest('hex');
  assert.equal(browserSha256, QUALIFIED_CHROME_SHA256, `Chrome155 executable changed: ${browser}`);
  return {
    node: { path: node, sha256: createHash('sha256').update(readFileSync(node)).digest('hex') },
    browser: { path: browser, version, sha256: browserSha256 },
  };
}

function requiredPath(name: string): string {
  const value = process.env[name] ?? QUALIFIED_HOST_ENV[name as keyof typeof QUALIFIED_HOST_ENV];
  assert.ok(value && value.startsWith('/'), `${name} must be an absolute path for the real host lane`);
  let resolved: string;
  try {
    resolved = realpathSync(value);
  } catch (error) {
    assert.fail(`${name} is not a real path: ${value} (${String(error)})`);
  }
  if (name === 'ASTRID_NODE_EXECUTABLE') {
    assert.equal(createHash('sha256').update(readFileSync(resolved)).digest('hex'), QUALIFIED_NODE_SHA256,
      `ASTRID_NODE_EXECUTABLE is not the qualified Node 20.19.4 binary: ${resolved}`);
  }
  return resolved;
}

async function prepareOwnedRemotionProject(directory: string, agent: string, python: string): Promise<string> {
  const qualified = requiredPath('ASTRID_REMOTION_PROJECT_DIR');
  const projectRoot = join(directory, 'project');
  const remotion = join(projectRoot, 'remotion');
  await cp(join(agent, 'remotion'), remotion, {
    recursive: true,
    filter: source => basename(source) !== 'node_modules',
  });
  await cp(join(agent, 'astrid'), join(projectRoot, 'astrid'), { recursive: true });

  // The project source must come from the frozen Agent archive. Only the
  // dependency graph is borrowed, and each package is linked into this owned
  // project as a leaf so build output and caches cannot touch the source graph.
  const sharedNodeModules = join(qualified, 'node_modules');
  const privateNodeModules = join(remotion, 'node_modules');
  assert.equal(realpathSync(sharedNodeModules), sharedNodeModules);
  await mkdir(privateNodeModules);
  const linkPackage = async (source: string, destination: string): Promise<void> => {
    assert.equal(await stat(source).then(() => true).catch(() => false), true, `dependency missing: ${source}`);
    assert.equal(await stat(destination).then(() => true).catch(() => false), false, `dependency collision: ${destination}`);
    await symlink(realpathSync(source), destination, 'dir');
  };
  for (const entry of await readdir(sharedNodeModules, { withFileTypes: true })) {
    if (entry.name === '.bin' || entry.name === '.cache' || entry.name === '@banodoco') continue;
    const source = join(sharedNodeModules, entry.name);
    const destination = join(privateNodeModules, entry.name);
    if (entry.name.startsWith('@') && entry.isDirectory()) {
      await mkdir(destination);
      for (const scoped of await readdir(source, { withFileTypes: true })) {
        if (scoped.name === '.bin' || scoped.name === '.cache') continue;
        await linkPackage(join(source, scoped.name), join(destination, scoped.name));
      }
    } else {
      await linkPackage(source, destination);
    }
  }
  await mkdir(join(privateNodeModules, '.bin'));
  for (const entry of await readdir(join(sharedNodeModules, '.bin'), { withFileTypes: true })) {
    await linkPackage(join(sharedNodeModules, '.bin', entry.name), join(privateNodeModules, '.bin', entry.name));
  }

  // Runtime's source-custody validator requires the Remotion CLI itself to
  // resolve inside the owned project. Its package bytes remain the qualified
  // read-only dependency; only this small entry package is materialized.
  const privateCli = join(privateNodeModules, '@remotion', 'cli');
  await rm(privateCli, { recursive: true, force: true });
  await cp(join(sharedNodeModules, '@remotion', 'cli'), privateCli, { recursive: true });

  const publicPackage = join(privateNodeModules, '@banodoco', 'timeline-composition');
  await mkdir(join(privateNodeModules, '@banodoco'));
  execFileSync('tar', ['-xzf', join(remotion, 'artifacts/banodoco-timeline-composition-0.0.13.tgz'),
    '-C', join(privateNodeModules, '@banodoco')]);
  await rename(join(privateNodeModules, '@banodoco', 'package'), publicPackage);
  execFileSync(python, ['-B', join(agent, 'scripts/gen_remotion_types.py'),
    join(remotion, 'src/types.generated.ts'), '--include-element-registries'], {
    cwd: agent,
    env: {
      ...process.env,
      ASTRID_REMOTION_PROJECT_DIR: remotion,
      ASTRID_NODE_EXECUTABLE: requiredPath('ASTRID_NODE_EXECUTABLE'),
      PYTHONPATH: agent,
      PYTHONDONTWRITEBYTECODE: '1',
    },
    encoding: 'utf8',
    maxBuffer: 2 * 1024 * 1024,
  });
  assert.equal(realpathSync(remotion), remotion);
  assert.equal(realpathSync(join(projectRoot, 'astrid')), join(projectRoot, 'astrid'));
  assert.equal(realpathSync(publicPackage), publicPackage);
  assert.equal(await stat(join(remotion, 'src/LiveSceneClip.tsx')).then(() => true).catch(() => false), true);
  assert.equal(await stat(join(projectRoot, 'astrid/packs/rendering/editor/live-scenes/SceneSurface.tsx'))
    .then(() => true).catch(() => false), true);
  return remotion;
}

function cleanHostEnvironment(runtime: string, agent: string): Record<string, string> {
  const blocked = new Set([
    'ASTRID_PACKS_PATH', 'NODE_OPTIONS', 'NODE_PATH', 'NODE_ICU_DATA', 'OPENSSL_CONF',
    'PYTHONEXECUTABLE', '__PYVENV_LAUNCHER__', 'PYTHONHOME', 'PYTHONPYCACHEPREFIX',
    'PYTHONPLATLIBDIR', 'PYTHONCASEOK', 'PYTHONSTARTUP', 'PYTHONSAFEPATH', 'PYTHONUTF8',
    'PYTHONCOERCECLOCALE', 'PYTHONPATH',
  ]);
  const inherited = Object.fromEntries(Object.entries(process.env).filter(([key]) =>
    !blocked.has(key) && !key.startsWith('GIT_') && !key.startsWith('DYLD_') && !key.startsWith('LD_')));
  return {
    ...inherited,
    PYTHONDONTWRITEBYTECODE: '1',
    PYTHONUNBUFFERED: '1',
    PYTHONPATH: [runtime, agent].join(delimiter),
    ASTRID_RUNTIME_CHECKOUT: runtime,
    ASTRID_CHECKOUT: agent,
    ASTRID_REMOTION_BROWSER_EXECUTABLE: requiredPath('ASTRID_REMOTION_BROWSER_EXECUTABLE'),
    ASTRID_TIMELINE_SCHEMA_PYTHONPATH: QUALIFIED_HOST_ENV.ASTRID_TIMELINE_SCHEMA_PYTHONPATH,
  };
}

function startProductionPackHost(
  python: string,
  runtime: string,
  agent: string,
  handoff: Record<string, unknown>,
): { hostPid: number; readyCapabilities: string[] } {
  const script = [
    'import json, sys',
    'from astrid.sdk.host_bootstrap import ensure_pack_host',
    'value = json.loads(sys.argv[1])',
    'result = ensure_pack_host(value, reconfigure_action="viewing admission setup")',
    'print(json.dumps({"host_pid": result.get("host_pid"), "host_status": result.get("host_status"), "ready_capabilities": result.get("host_ready_capabilities", [])}))',
  ].join('; ');
  const env = {
    ...cleanHostEnvironment(runtime, agent),
    ASTRID_PACK_HOST_PYTHON: python,
    ASTRID_REMOTION_PROJECT_DIR: requiredPath('ASTRID_REMOTION_PROJECT_DIR'),
    ASTRID_NODE_EXECUTABLE: requiredPath('ASTRID_NODE_EXECUTABLE'),
  };
  const output = execFileSync(python, ['-B', '-c', script, JSON.stringify(handoff)], {
    cwd: agent,
    env,
    encoding: 'utf8',
    maxBuffer: 2 * 1024 * 1024,
  });
  const result = JSON.parse(output.trim().split('\n').pop()!) as {
    host_pid?: number;
    host_status?: string;
    ready_capabilities?: unknown;
  };
  assert.equal(result.host_status, 'ready', `production pack host did not become ready: ${output}`);
  assert.ok(Number.isSafeInteger(result.host_pid) && result.host_pid > 0, `production pack host returned no PID: ${output}`);
  assert.ok(Array.isArray(result.ready_capabilities));
  return { hostPid: result.host_pid, readyCapabilities: result.ready_capabilities.filter((value): value is string => typeof value === 'string') };
}

function pauseOwnedPackHost(hostPid: number): void {
  assert.equal(process.platform, 'linux', 'owned pack-host pause requires Linux process-group inspection');
  const stat = readFileSync(`/proc/${hostPid}/stat`, 'utf8');
  const closingParen = stat.lastIndexOf(')');
  assert.ok(closingParen > 0, `invalid host process stat for ${hostPid}`);
  const fields = stat.slice(closingParen + 2).trim().split(/\s+/);
  assert.equal(Number(fields[2]), hostPid, `production host ${hostPid} is not its own process-group leader`);
  process.kill(hostPid, 0);
  // The production launcher starts the host in its own session, so the PID is
  // also the process-group leader. Only pause after ensure_pack_host reported
  // readiness; this keeps admission queued without starting a render call.
  process.kill(-hostPid, 'SIGSTOP');
}

async function stopProductionPackHost(
  harness: { tmp: string }, hostPid: number, python: string, agent: string, runtime: string,
): Promise<void> {
  try { process.kill(-hostPid, 'SIGCONT'); } catch { /* the host may have exited during failure cleanup */ }
  const runtimeAlias = join(harness.tmp, 'runtime');
  await symlink(join(harness.tmp, 'support'), runtimeAlias, 'dir');
  try {
    const script = [
      'import json, sys',
      'from astrid.sdk.upgrade import stop_pack_host',
      'print(json.dumps(stop_pack_host(sys.argv[1])))',
    ].join('; ');
    execFileSync(python, ['-B', '-c', script, harness.tmp], {
      cwd: agent,
      env: cleanHostEnvironment(runtime, agent),
      encoding: 'utf8',
      maxBuffer: 256 * 1024,
    });
  } finally {
    await unlink(runtimeAlias).catch(() => undefined);
  }
}

test('native retained frame fixture restores and admits one normal render task', async () => {
  const sourceTemp = await mkdtemp(join(tmpdir(), 'native-frame-frozen-pair-'));
  const previousEnv = { ...process.env };
  let harness: import('../../local/support/harness').DirectHarness | undefined;
  let productionHost: { hostPid: number; readyCapabilities: string[] } | undefined;
  let productionHostStopped = false;
  let productionHostCleanupError: unknown;
  let browserLock: ReturnType<typeof spawn> | undefined;
  let privateRenderRoot: string | undefined;
  try {
    assertFreeDiskFloor(tmpdir());
    browserLock = acquireBrowserLock();
    const archived = await archiveFrozenSources(sourceTemp);
    const runtimePython = process.env.ASTRID_RUNTIME_PYTHON ?? '/home/user/work/venv-runtime/bin/python';
    const agentPython = process.env.ASTRID_PYTHON ?? '/home/user/work/venv-agent/bin/python';
    assert.equal(await readFile(runtimePython).then(() => true).catch(() => false), true, `Runtime Python missing: ${runtimePython}`);
    assert.equal(await readFile(agentPython).then(() => true).catch(() => false), true, `Agent Python missing: ${agentPython}`);
    process.env.ASTRID_RUNTIME_CHECKOUT = archived.runtime.root;
    process.env.ASTRID_CHECKOUT = archived.agent.root;
    process.env.ASTRID_RUNTIME_PYTHON = runtimePython;
    process.env.ASTRID_PYTHON = agentPython;
    const moduleProof = pythonSourceProof(runtimePython, archived.runtime.root, archived.agent.root);
    const { DirectHarness } = await import('../../local/support/harness');
    const { assertCanonicalNativeMedia, assertPinnedFrameParityFixture, nativeFrameParitySetup,
      prepareFrameParityFixture, prepareNativeFrameParityRealm, readRuntimeJson, timelineBase } = await import('./fixture');
    const { ORIGINAL_640 } = await import('./canvas');
    const remotionPackage = JSON.parse(await readFile(join(archived.agent.root, 'remotion/package.json'), 'utf8')) as {
      dependencies?: Record<string, string>;
    };
    const before = {
      app: { source: 'App test source is the central snapshot; no App source archive is substituted' },
      runtime: { commit: FROZEN_SOURCES.runtime.commit, tree: archived.runtime.tree, archiveSha256: archived.runtime.archiveSha256, manifest: archived.runtime.manifest },
      agent: { commit: FROZEN_SOURCES.agent.commit, tree: archived.agent.tree, archiveSha256: archived.agent.archiveSha256, manifest: archived.agent.manifest },
      packageVersions: {
        remotion: remotionPackage.dependencies?.remotion,
        timelineComposition: remotionPackage.dependencies?.['@banodoco/timeline-composition'],
      },
      toolchain: qualifiedToolchainProof(),
      compositionArtifact: compositionArtifactProof(archived.agent.root),
      moduleProof,
    };
    assert.equal(before.compositionArtifact.members, 77);
    assert.equal(before.compositionArtifact.sha256, '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738');
    console.log(`[native-frame-source-proof] before ${JSON.stringify(before)}`);
    harness = new DirectHarness();
    await harness.start({ seed: false, beforeRuntimeStart: async current => {
      await prepareNativeFrameParityRealm(current, ORIGINAL_640);
    }});
    await harness.enableTimelineAuthoring(process.env.ASTRID_PYTHON!);
    const setup = nativeFrameParitySetup(harness);
    const empty = await readRuntimeJson<{ head_revision_id: string; head_publication_id: string }>(harness,
      `${timelineBase({ projectId: setup.projectId, timelineId: setup.timelineId })}`);
    assert.deepEqual({ project_id: empty.project_id, timeline_id: empty.timeline_id,
      head_revision_id: empty.head_revision_id, head_publication_id: empty.head_publication_id },
    { project_id: setup.projectId, timeline_id: setup.timelineId,
      head_revision_id: setup.head.revision_id, head_publication_id: setup.head.publication_id });

    const fixture = await prepareFrameParityFixture(harness, ORIGINAL_640, setup);
    assert.equal(fixture.media.length, 3);
    assert.deepEqual(fixture.media.map(pin => pin.name), ['image', 'video', 'audio']);
    assert.equal(fixture.sourceVideoMediaId, fixture.media.find(pin => pin.name === 'video')!.objectId);
    assert.deepEqual(fixture.parent.payload.config, setup.document.parent_revision.payload.config);
    assert.deepEqual(setup.document.dependency_manifest.media,
      fixture.media.map(pin => ({ media_id: pin.objectId, content_digest: pin.digest })).sort((a, b) => a.media_id.localeCompare(b.media_id)));
    assertCanonicalNativeMedia(fixture, ORIGINAL_640);
    assert.equal(harness.audit().filter(entry => entry.method === 'POST' && entry.path.endsWith('/composition-revisions')).length, 0);

    privateRenderRoot = await mkdtemp('/tmp/r-');
    const privateHome = join(privateRenderRoot, 'home');
    const privateTemp = join(privateRenderRoot, 'tmp');
    const privateConfig = join(privateRenderRoot, 'config');
    const privateCache = join(privateRenderRoot, 'cache');
    await mkdir(privateHome);
    await mkdir(privateTemp);
    await mkdir(privateConfig);
    await mkdir(privateCache);
    assert.equal(realpathSync(privateRenderRoot), privateRenderRoot);
    assert.equal(realpathSync(privateTemp), privateTemp);
    process.env.ASTRID_REMOTION_PROJECT_DIR = await prepareOwnedRemotionProject(privateRenderRoot, archived.agent.root, agentPython);
    Object.assign(process.env, {
      HOME: privateHome,
      TMPDIR: privateTemp,
      TMP: privateTemp,
      TEMP: privateTemp,
      XDG_CONFIG_HOME: privateConfig,
      XDG_CACHE_HOME: privateCache,
    });

    const discovery = harness.discovery();
    productionHost = startProductionPackHost(agentPython, archived.runtime.root, archived.agent.root, {
      ...discovery,
      source_checkout: archived.agent.root,
      runtime_instance_id: harness.runtimeInstanceId,
    });
    assert.ok(productionHost.readyCapabilities.includes('rendering.render'), `real host capabilities: ${JSON.stringify(productionHost)}`);
    const catalogItemsBeforePause: Array<Record<string, unknown>> = [];
    let catalogBeforePause: { items: Array<Record<string, unknown>> } = { items: catalogItemsBeforePause };
    let catalogCursor: string | undefined;
    for (let attempt = 0; attempt < 100; attempt += 1) {
      const catalogPage = await readRuntimeJson<{ items: Array<Record<string, unknown>>; next_cursor?: string | null }>(harness,
        `/v1/capabilities?limit=50${catalogCursor ? `&cursor=${encodeURIComponent(catalogCursor)}` : ''}`);
      catalogItemsBeforePause.push(...catalogPage.items);
      catalogBeforePause = { items: catalogItemsBeforePause };
      if (catalogItemsBeforePause.some(item => item.capability_id === 'rendering.render')) break;
      const nextCursor = catalogPage.next_cursor;
      if (typeof nextCursor !== 'string' || nextCursor.length === 0) break;
      catalogCursor = nextCursor;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    const renderCapabilityBeforePause = catalogBeforePause.items.find(item => item.capability_id === 'rendering.render');
    assert.ok(renderCapabilityBeforePause, `real host must register rendering.render in the Runtime catalog: ${JSON.stringify(catalogBeforePause)}`);
    assert.equal(renderCapabilityBeforePause.status, 'ready');
    assert.equal(catalogBeforePause.items.some(item => String(item.capability_id).toLowerCase().includes('stitch')), false);
    pauseOwnedPackHost(productionHost.hostPid);

    const objectsBefore = (await readRuntimeJson<{ items: unknown[] }>(harness,
      `/v1/projects/${fixture.projectId}/objects?limit=50`)).items;
    const forged = await harness.runtimeJson('POST', '/v1/tasks', {
      project: fixture.projectId,
      capability_id: 'rendering.render',
      capability_digest: `sha256:${'0'.repeat(64)}`,
      input_object_ids: [],
      spec: {
        authority_context: {
          mode: 'composed_capture', project_id: fixture.projectId, timeline_id: fixture.timelineId,
          revision_id: fixture.headRevisionId,
          capture_snapshot: { config: { clips: [{ id: 'forged', hold: 999 }] }, registry: {} },
        },
        inputs: { filmstrip_authority: '{}' },
      },
    });
    assert.notEqual(forged.status, 201);
    const objectsAfter = (await readRuntimeJson<{ items: unknown[] }>(harness,
      `/v1/projects/${fixture.projectId}/objects?limit=50`)).items;
    assert.deepEqual(objectsAfter, objectsBefore);
    assert.equal(harness.audit().filter(entry => entry.method === 'POST' && entry.path.endsWith('/composition-revisions')).length, 0);

    const { createServer } = await import('vite');
    const viteServer = await createServer({
      configFile: join(process.cwd(), 'config/testing/vitest.config.ts'),
      server: { middlewareMode: true },
      resolve: { alias: { react: 'react', 'react-dom': 'react-dom' } },
      plugins: [{
        name: 'normal-admission-react-hook-stub',
        enforce: 'pre',
        resolveId(id: string) {
          return id === 'react' ? '\0normal-admission-react' : undefined;
        },
        load(id: string) {
          return id === '\0normal-admission-react'
            ? 'export const useEffect = () => undefined; export default {};'
            : undefined;
        },
      }],
      logLevel: 'error',
    });
    try {
      const { buildRenderTimelinePayload, enqueueAstridRuntimeRenderTimeline } = await viteServer.ssrLoadModule(
        '/src/tools/video-editor/lib/renderRouter.ts',
      );
    const internal = fixture.internal.payload as {
      tracks: unknown[];
      clips: unknown[];
      registry: { assets: Record<string, Record<string, unknown>> };
    };
    const built = buildRenderTimelinePayload({
      request: {
        timelineId: fixture.timelineId,
        assetRegistry: internal.registry,
        resolvedConfig: {
          ...internal,
          registry: internal.registry.assets,
        } as never,
        renderRuntime: { projectId: fixture.projectId },
      },
      correlationId: 'normal-three-media-admission',
    });
    assert.equal(built.error, undefined);
    assert.ok(built.payload);
    assert.deepEqual(built.payload.input_object_ids, fixture.media.map(pin => pin.objectId));
    assert.deepEqual(
      (built.payload.timeline as { clips: unknown[] }).clips,
      internal.clips,
      'App payload must retain the unchanged three-media fixture',
    );

    const originalFetch = globalThis.fetch;
    const observed: Array<{ url: string; method: string; status: number; body: unknown }> = [];
    globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = new URL(input instanceof Request ? input.url : String(input), 'http://localhost');
      const headers = new Headers(init?.headers);
      if (url.pathname.startsWith('/api/astrid/')) {
        assert.equal(headers.has('Authorization'), false, 'normal App admission must use the door credential, not a browser bearer');
        headers.set('Origin', harness!.origin);
      }
      const response = await originalFetch(input, { ...init, headers });
      if (url.pathname.startsWith('/api/astrid/')) {
        observed.push({ url: url.toString(), method: init?.method ?? 'GET', status: response.status, body: await response.clone().json() });
      }
      return response;
    }) as typeof fetch;
    try {
      const admitted = await enqueueAstridRuntimeRenderTimeline(built.payload, {
        client: new AstridLocalClient({
          projectSlug: fixture.projectId,
          baseUrl: `http://127.0.0.1:${harness.doorPort}/api/astrid`,
        }),
        idempotencyKey: 'normal-three-media-admission',
      });
      assert.equal(admitted.status, 'queued', admitted.message);
      assert.ok(admitted.task_id);
      const cancelled = await harness.runtimeJson('POST', `/v1/tasks/${encodeURIComponent(admitted.task_id)}/cancel`, {}, {
        'Idempotency-Key': 'normal-three-media-admission-cancel',
      });
      assert.ok([200, 201].includes(cancelled.status), `queued admission cancellation: ${JSON.stringify(cancelled.body)}`);
      assert.equal((cancelled.body as { data?: { state?: string } }).data?.state, 'cancelled');

      const catalogPages = observed.filter(entry => entry.url.includes('/v1/capabilities'));
      assert.ok(catalogPages.length > 0);
      assert.equal(catalogPages.every(entry => entry.status === 200), true);
      const catalogItems = catalogPages.flatMap(entry =>
        (entry.body as { items: Array<Record<string, unknown>> }).items);
      const renderCapability = catalogItems.find(item => item.capability_id === 'rendering.render');
      assert.ok(renderCapability, 'normal Runtime catalog must register rendering.render');
      assert.equal(renderCapability.status, 'ready');
      assert.equal(typeof renderCapability.definition_digest, 'string');
      assert.equal(catalogItems.some(item => String(item.capability_id).toLowerCase().includes('stitch')), false);

      const admission = observed.find(entry => entry.method === 'POST' && entry.url.endsWith('/v1/tasks'));
      assert.ok(admission);
      assert.equal(admission.status, 201);
      const receiptEnvelope = admission.body as {
        data: { task_id: string; capability_id: string; capability_digest: string; input_object_ids: string[]; spec: Record<string, unknown> };
        receipt: { command_kind: string; idempotency_key: string; result: { task_id: string } };
      };
      assert.equal(receiptEnvelope.data.task_id, admitted.task_id);
      assert.equal(receiptEnvelope.data.capability_id, 'rendering.render');
      assert.equal(receiptEnvelope.data.capability_digest, renderCapability.definition_digest);
      assert.deepEqual(receiptEnvelope.data.input_object_ids.slice(0, fixture.media.length), fixture.media.map(pin => pin.objectId));
      assert.equal(receiptEnvelope.receipt.command_kind, 'task.create');
      assert.equal(receiptEnvelope.receipt.idempotency_key, 'normal-three-media-admission');
      assert.equal((receiptEnvelope.receipt.result as unknown as { task: { id: string } }).task.id, admitted.task_id);

      const accepted = await readRuntimeJson<{
        task_id: string;
        capability_id: string;
        input_object_ids: string[];
        spec: { spec: { params: Record<string, unknown>; inputs: Record<string, unknown>; timeline_snapshot_ref: Record<string, unknown> } };
      }>(harness, `/v1/tasks/${encodeURIComponent(admitted.task_id)}`);
      assert.equal(accepted.task_id, admitted.task_id);
      assert.equal(accepted.capability_id, 'rendering.render');
      assert.deepEqual(accepted.input_object_ids.slice(0, fixture.media.length), fixture.media.map(pin => pin.objectId));
      assert.equal(accepted.spec.spec.params.timeline_ref, fixture.timelineId);
      assert.equal(accepted.spec.spec.params.selector, 'rendering.remotion');
      assert.equal(accepted.spec.spec.inputs.timeline_ref, fixture.timelineId);
      const authority = accepted.spec.spec.inputs.timeline_authority as Record<string, unknown>;
      assert.equal(authority.authority, 'kernel');
      assert.equal(authority.project_id, fixture.projectId);
      assert.equal(authority.timeline_id, fixture.timelineId);
      assert.equal(authority.parent_revision_id, fixture.headRevisionId);
      assert.equal(authority.parent_content_digest, fixture.parent.content_digest);
      assert.match(String(authority.snapshot_digest), /^sha256:[0-9a-f]{64}$/);
      assert.equal(Array.isArray(authority.dependency_digests), true);
      assert.deepEqual(authority.managed_media_admissions, Object.fromEntries(
        fixture.media.map(pin => [pin.objectId, pin.digest]),
      ));
      assert.deepEqual(authority.input_object_ids, fixture.media.map(pin => pin.objectId));
      const snapshot = accepted.spec.spec.timeline_snapshot_ref as { digest: string; project_id: string; timeline_id: string };
      assert.match(snapshot.digest, /^sha256:[0-9a-f]{64}$/);
      assert.equal(snapshot.project_id, fixture.projectId);
      assert.equal(snapshot.timeline_id, fixture.timelineId);
      assert.equal(accepted.input_object_ids.includes(snapshot.digest), true);
      assert.equal(JSON.stringify(accepted).toLowerCase().includes('stitch'), false);
      assert.equal(JSON.stringify(accepted).includes('fake'), false);
    } finally {
      globalThis.fetch = originalFetch;
    }
    assert.deepEqual(harness.audit().filter(entry => entry.method === 'POST' && entry.path.endsWith('/tasks'))
      .map(entry => ({ path: entry.path, status: entry.status, origin: entry.origin })),
    [{ path: '/v1/tasks', status: 201, origin: harness.origin }]);
    assert.equal(harness.audit().some(entry => entry.path.toLowerCase().includes('stitch')), false);
    await assertPinnedFrameParityFixture(harness, fixture);

    // The preceding admission is deliberately paused/cancelled. Continue this
    // same owned host only after those assertions and prove one normal CPU run.
    process.kill(-productionHost.hostPid, 'SIGCONT');
    const actualObserved: Array<{ url: string; method: string; status: number; body: unknown }> = [];
    const actualOriginalFetch = globalThis.fetch;
    globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = new URL(input instanceof Request ? input.url : String(input), 'http://localhost');
      const headers = new Headers(init?.headers);
      if (url.pathname.startsWith('/api/astrid/')) {
        assert.equal(headers.has('Authorization'), false, 'normal export admission must use the door credential');
        headers.set('Origin', harness!.origin);
      }
      const response = await actualOriginalFetch(input, { ...init, headers });
      if (url.pathname.startsWith('/api/astrid/')) {
        actualObserved.push({ url: url.toString(), method: init?.method ?? 'GET', status: response.status,
          body: await response.clone().json() });
      }
      return response;
    }) as typeof fetch;
    let actualTaskId: string | undefined;
    try {
      const actual = await enqueueAstridRuntimeRenderTimeline(built.payload!, {
        client: new AstridLocalClient({
          projectSlug: fixture.projectId,
          baseUrl: `http://127.0.0.1:${harness.doorPort}/api/astrid`,
        }),
        idempotencyKey: 'normal-three-media-cpu-export',
      });
      assert.equal(actual.status, 'queued', actual.message);
      assert.ok(actual.task_id);
      actualTaskId = actual.task_id;
    } finally {
      globalThis.fetch = actualOriginalFetch;
    }
    const actualAdmission = actualObserved.find(entry => entry.method === 'POST' && entry.url.endsWith('/v1/tasks'));
    assert.ok(actualAdmission, 'normal CPU export must perform the Runtime task admission');
    assert.equal(actualAdmission.status, 201);
    const actualRequest = actualAdmission.body as {
      data: { task_id: string; capability_id: string; spec: { spec: { params: Record<string, unknown>; output_policy: Record<string, unknown> } } };
    };
    assert.equal(actualRequest.data.task_id, actualTaskId);
    assert.equal(actualRequest.data.capability_id, 'rendering.render');
    assert.equal(actualRequest.data.spec.spec.params.timeline_ref, fixture.timelineId);
    assert.equal(actualRequest.data.spec.spec.params.selector, 'rendering.remotion');
    assert.deepEqual(actualRequest.data.spec.spec.output_policy, {
      format: 'mp4', destination: 'download', filename: built.payload!.output_filename,
    });

    const actualTaskPath = `/v1/tasks/${encodeURIComponent(actualTaskId!)}`;
    const actualInitial = await readRuntimeJson<Record<string, unknown>>(harness, actualTaskPath);
    const actualInitialSpec = actualInitial.spec as { spec: { params: Record<string, unknown>; inputs: Record<string, unknown>; output_policy: Record<string, unknown> } };
    assert.equal(actualInitial.capability_id, 'rendering.render');
    assert.equal(actualInitialSpec.spec.params.selector, 'rendering.remotion');
    assert.equal(actualInitialSpec.spec.params.timeline_ref, fixture.timelineId);
    assert.deepEqual(actualInitialSpec.spec.output_policy, actualRequest.data.spec.spec.output_policy);
    const actualFrozen = assertTaskAuthority(actualInitial as unknown as Task, fixture,
      String(actualInitial.capability_digest));
    const actualAuthority = actualFrozen.authority;

    let actualTask = actualInitial;
    const deadline = Date.now() + 240_000;
    while (actualTask.state !== 'succeeded') {
      assert.notEqual(actualTask.state, 'failed', `normal CPU render failed: ${JSON.stringify(actualTask)}`);
      assert.notEqual(actualTask.state, 'cancelled', `normal CPU render cancelled: ${JSON.stringify(actualTask)}`);
      assert.ok(Date.now() < deadline, `normal CPU render did not finish: ${JSON.stringify(actualTask)}`);
      await new Promise(resolve => setTimeout(resolve, 500));
      actualTask = await readRuntimeJson<Record<string, unknown>>(harness, actualTaskPath);
    }
    const actualCompleted = await readRuntimeJson<Record<string, unknown>>(harness, actualTaskPath);
    assert.deepEqual(actualCompleted.spec, actualInitial.spec, 'normal task spec changed while rendering');
    const outputs = await readRuntimeJson<{ items: Array<Record<string, unknown>> }>(harness,
      `${actualTaskPath}/managed-outputs?limit=50`);
    const videoOutput = outputs.items.find(item => String(item.filename ?? '').endsWith('.mp4'));
    assert.ok(videoOutput, `normal task has no MP4 output: ${JSON.stringify(outputs)}`);
    assert.equal(videoOutput.task_id, actualTaskId);
    assert.equal(videoOutput.project_id, fixture.projectId);
    assert.equal(videoOutput.media_type, 'video/mp4');
    const videoObjectId = String(videoOutput.object_id);
    const videoResponse = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(videoObjectId)}`);
    assert.equal(videoResponse.status, 200);
    const videoBytes = new Uint8Array(await videoResponse.arrayBuffer());
    assert.ok(videoBytes.byteLength > 1_000);
    await mkdir(ARTIFACT_ROOT, { recursive: true });
    const exportPath = artifactPath(`task-${actualTaskId}.mp4`);
    await writeFile(exportPath, videoBytes);
    assert.equal((await stat(exportPath)).size, videoBytes.byteLength);

    const probe = spawnSync('ffprobe', [
      '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', exportPath,
    ], { encoding: 'utf8' });
    assert.equal(probe.status, 0, `ffprobe failed: ${probe.stderr}`);
    assert.equal(probe.stderr, '');
    const metadata = JSON.parse(probe.stdout) as { streams: Array<Record<string, unknown>>; format: Record<string, unknown> };
    const videoStream = metadata.streams.find(stream => stream.codec_type === 'video');
    const audioStream = metadata.streams.find(stream => stream.codec_type === 'audio');
    assert.ok(videoStream, 'normal output must contain a video stream');
    assert.ok(audioStream, 'normal output must contain an audio stream');
    assert.deepEqual({ codec_name: videoStream.codec_name, width: videoStream.width, height: videoStream.height,
      r_frame_rate: videoStream.r_frame_rate, nb_read_frames: videoStream.nb_read_frames },
    { codec_name: 'h264', width: 640, height: 360, r_frame_rate: '30/1', nb_read_frames: '165' });
    assert.equal(Number(videoStream.duration), 5.5);
    assert.deepEqual({ codec_name: audioStream.codec_name, sample_rate: audioStream.sample_rate,
      channels: audioStream.channels }, { codec_name: 'aac', sample_rate: '48000', channels: 2 });
    assert.ok(Number(audioStream.duration) >= 5.4 && Number(audioStream.duration) <= 5.6);
    assert.ok(Number(metadata.format.duration) >= 5.4 && Number(metadata.format.duration) <= 5.6);
    const decode = spawnSync('ffmpeg', ['-v', 'error', '-i', exportPath, '-f', 'null', '-'], { encoding: 'utf8' });
    assert.equal(decode.status, 0, `ffmpeg decode failed: ${decode.stderr}`);
    assert.equal(decode.stderr, '', 'normal MP4 must be playable without decoder errors');

    const provenanceOutput = outputs.items.find(item => String(item.filename ?? '').endsWith('.provenance.json'));
    assert.ok(provenanceOutput, 'normal task must publish renderer provenance');
    const provenanceResponse = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(String(provenanceOutput.object_id))}`);
    assert.equal(provenanceResponse.status, 200);
    const provenance = JSON.parse(await provenanceResponse.text()) as Record<string, unknown>;
    assert.equal(provenance.engine, 'rendering.remotion');
    assert.deepEqual(provenance.canonical_timeline, actualAuthority);
    const backend = (provenance.backend_fragments as Record<string, Record<string, unknown>>)['rendering.remotion'];
    assert.deepEqual(backend, {
      ...backend,
      renderer: 'remotion', composition_id: 'TimelineComposition',
      project_dir: requiredPath('ASTRID_REMOTION_PROJECT_DIR'),
    });
    await writeFile(artifactPath(`task-${actualTaskId}.ffprobe.json`), `${JSON.stringify(metadata, null, 2)}\n`);
    await writeFile(artifactPath(`task-${actualTaskId}.provenance.json`), `${JSON.stringify(provenance, null, 2)}\n`);
    await assertPinnedFrameParityFixture(harness, fixture);
    assert.equal(productionHostStopped, false, 'owned pack host must remain available until task evidence is read');
    } finally {
      await viteServer.close();
    }
    await stopProductionPackHost(harness, productionHost.hostPid, agentPython, archived.agent.root, archived.runtime.root);
    productionHostStopped = true;
    assertProcessGroupGone(productionHost.hostPid);
    await harness.stop();
    harness = undefined;
    const after = {
      runtime: await sourceManifest(archived.runtime.root),
      agent: await sourceManifest(archived.agent.root),
      toolchain: qualifiedToolchainProof(),
      compositionArtifact: compositionArtifactProof(archived.agent.root),
    };
    assert.deepEqual(after.runtime, before.runtime.manifest);
    assert.deepEqual(after.agent, before.agent.manifest);
    assert.deepEqual(after.toolchain, before.toolchain);
    assert.deepEqual(after.compositionArtifact, before.compositionArtifact);
    console.log(`[native-frame-source-proof] after ${JSON.stringify(after)}`);
  } finally {
    if (productionHost && !productionHostStopped && harness) {
      try {
        await stopProductionPackHost(harness, productionHost.hostPid,
          process.env.ASTRID_PYTHON ?? '/home/user/work/venv-agent/bin/python',
          process.env.ASTRID_CHECKOUT ?? FROZEN_SOURCES.agent.root,
          process.env.ASTRID_RUNTIME_CHECKOUT ?? FROZEN_SOURCES.runtime.root);
      } catch (error) {
        productionHostCleanupError = error;
      }
    }
    const harnessStopError = await harness?.stop().then(() => undefined, error => error);
    for (const name of Object.keys(process.env)) {
      if (!(name in previousEnv)) delete process.env[name];
    }
    Object.assign(process.env, previousEnv);
    if (privateRenderRoot) await rm(privateRenderRoot, { recursive: true, force: true });
    await rm(sourceTemp, { recursive: true, force: true });
    browserLock?.kill('SIGTERM');
    if (harnessStopError && !productionHostCleanupError) productionHostCleanupError = harnessStopError;
    if (productionHostCleanupError) throw productionHostCleanupError;
  }
});
