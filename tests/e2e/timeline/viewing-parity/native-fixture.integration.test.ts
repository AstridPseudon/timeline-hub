import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, realpathSync } from 'node:fs';
import { mkdtemp, readdir, readFile, rm, symlink, unlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { delimiter, join, relative } from 'node:path';
import { test } from 'node:test';
import { AstridLocalClient } from '../../../../src/integrations/astrid/client';

const FROZEN_SOURCES = {
  runtime: {
    root: '/home/user/work/wt/rt-pin-2c4ac180',
    commit: '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
    label: 'rt-pin/official013',
  },
  agent: {
    root: '/home/user/work/wt/agt-pin-04f59c0c',
    commit: '04f59c0c106c6a6e5bad95f4c56037d77229e8f7',
    label: 'agt-pin/public013',
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

function requiredPath(name: string): string {
  const value = process.env[name];
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
    ...process.env,
    PYTHONDONTWRITEBYTECODE: '1',
    PYTHONUNBUFFERED: '1',
    PYTHONPATH: [runtime, agent, process.env.PYTHONPATH].filter(Boolean).join(delimiter),
    ASTRID_RUNTIME_CHECKOUT: runtime,
    ASTRID_CHECKOUT: agent,
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
      env: {
        ...process.env,
        PYTHONDONTWRITEBYTECODE: '1',
        ASTRID_RUNTIME_CHECKOUT: runtime,
        ASTRID_CHECKOUT: agent,
        PYTHONPATH: [runtime, agent, process.env.PYTHONPATH].filter(Boolean).join(delimiter),
      },
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
  try {
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
      moduleProof,
    };
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

    const discovery = harness.discovery();
    productionHost = startProductionPackHost(agentPython, archived.runtime.root, archived.agent.root, {
      ...discovery,
      source_checkout: archived.agent.root,
      runtime_instance_id: harness.runtimeInstanceId,
    });
    assert.ok(productionHost.readyCapabilities.includes('rendering.render'), `real host capabilities: ${JSON.stringify(productionHost)}`);
    const catalogBeforePause = await readRuntimeJson<{ items: Array<Record<string, unknown>> }>(harness,
      '/v1/capabilities?limit=50');
    const renderCapabilityBeforePause = catalogBeforePause.items.find(item => item.capability_id === 'rendering.render');
    assert.ok(renderCapabilityBeforePause, 'real host must register rendering.render in the Runtime catalog');
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

      const catalog = observed.find(entry => entry.url.includes('/v1/capabilities'));
      assert.ok(catalog);
      assert.equal(catalog.status, 200);
      const catalogItems = (catalog.body as { items: Array<Record<string, unknown>> }).items;
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
      assert.deepEqual(receiptEnvelope.data.input_object_ids, fixture.media.map(pin => pin.objectId));
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
    } finally {
      await viteServer.close();
    }
    await stopProductionPackHost(harness, productionHost.hostPid, agentPython, archived.agent.root, archived.runtime.root);
    productionHostStopped = true;
    await harness.stop();
    harness = undefined;
    const after = {
      runtime: await sourceManifest(archived.runtime.root),
      agent: await sourceManifest(archived.agent.root),
    };
    assert.deepEqual(after.runtime, before.runtime.manifest);
    assert.deepEqual(after.agent, before.agent.manifest);
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
    await harness?.stop();
    for (const name of Object.keys(process.env)) {
      if (!(name in previousEnv)) delete process.env[name];
    }
    Object.assign(process.env, previousEnv);
    await rm(sourceTemp, { recursive: true, force: true });
    if (productionHostCleanupError) throw productionHostCleanupError;
  }
});
