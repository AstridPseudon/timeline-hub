import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, readdir, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { delimiter, join, relative } from 'node:path';
import { test } from 'node:test';

const FROZEN_SOURCES = {
  runtime: {
    root: '/home/user/banodoco/banodoco-workspace-runtime',
    commit: '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
    label: 'official013/S2',
  },
  agent: {
    root: '/home/user/peteromallet/astrid-agent',
    commit: 'd8749a9ce12a699672faf3ad96b4e4cbea9245c2',
    label: 'official013/S2',
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

test('native retained frame fixture restores through /v1 with no legacy seed or forged task write', async () => {
  const sourceTemp = await mkdtemp(join(tmpdir(), 'native-frame-frozen-pair-'));
  const previousEnv = { ...process.env };
  let harness: import('../../local/support/harness').DirectHarness | undefined;
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
    const { nativeFrameParitySetup, prepareFrameParityFixture, prepareNativeFrameParityRealm, readRuntimeJson, timelineBase } = await import('./fixture');
    const { ORIGINAL_640 } = await import('./canvas');
    const before = {
      app: { source: 'App test source is the central snapshot; no App source archive is substituted' },
      runtime: { commit: FROZEN_SOURCES.runtime.commit, tree: archived.runtime.tree, archiveSha256: archived.runtime.archiveSha256, manifest: archived.runtime.manifest },
      agent: { commit: FROZEN_SOURCES.agent.commit, tree: archived.agent.tree, archiveSha256: archived.agent.archiveSha256, manifest: archived.agent.manifest },
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
    assert.equal(fixture.sourceVideoMediaId, fixture.media[1].objectId);
    assert.deepEqual(fixture.parent.payload.config, setup.document.parent_revision.payload.config);
    assert.equal(harness.audit().filter(entry => entry.method === 'POST' && entry.path.endsWith('/composition-revisions')).length, 0);

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
    await harness?.stop();
    for (const name of Object.keys(process.env)) {
      if (!(name in previousEnv)) delete process.env[name];
    }
    Object.assign(process.env, previousEnv);
    await rm(sourceTemp, { recursive: true, force: true });
  }
});
