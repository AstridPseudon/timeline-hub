/**
 * The Astrid side of the three-product journey (card F2-C): the real `astrid` CLI and `astrid.core.dev.cross_client`, run
 * as subprocesses against the same Runtime the hosted page talks to.
 *
 * Every call gets an environment built from nothing (no ambient Astrid state, no ambient Runtime, no proxy), a state
 * root inside the harness's tmp (removed by `harness.stop()`), Astrid then Runtime checkouts in `PYTHONPATH`, and the four
 * `ASTRID_TIMELINE_EVAL_*` variables. The endpoint is read from the Runtime's discovery file before each call, so a restarted
 * Runtime on a new port is followed with no special case. The explicit context makes `astrid` skip the launcher and the pack
 * host (astrid/sdk/client.py `open_from_launcher`), which is also why this runs on Linux. The product token never enters it.
 */
import { execFileSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, realpathSync } from 'node:fs';
import { loadavg } from 'node:os';
import path from 'node:path';
import { ASTRID_ACTOR, REPO_ROOT, RUNTIME_CHECKOUT, spawnGroup, stopGroup, type DirectHarness } from './harness.ts';
import type { CommitAcceptedMutation, HeadPin } from '../../../../src/integrations/runtime/timeline-commit-types.ts';

/** The Astrid tree to test. The editable install in a venv may point elsewhere, so `PYTHONPATH` puts this one first and the identity probe asserts it. */
export const ASTRID_CHECKOUT = path.resolve(process.env.ASTRID_CHECKOUT
  ?? [path.join(REPO_ROOT, '..', 'astrid-agent'), path.join(REPO_ROOT, '../..', 'agent')]
    .find((dir) => existsSync(path.join(dir, 'astrid', '__init__.py')))
  ?? path.join(REPO_ROOT, '..', 'astrid-agent'));
export const ASTRID_PYTHON = process.env.ASTRID_PYTHON
  ?? [path.join(ASTRID_CHECKOUT, '.venv/bin/python'), path.join(ASTRID_CHECKOUT, '../venv-agent/bin/python')].find(existsSync)
  ?? path.join(ASTRID_CHECKOUT, '.venv/bin/python');
/** A hang ceiling for one Astrid call (R-10): durations are recorded, never judged. */
export const ASTRID_CALL_CEILING_MS = 120_000;

/** What `python -m astrid.core.dev.cross_client identity` prints (astrid/core/dev/cross_client.py). */
export interface AstridIdentity {
  astrid_file: string;
  astrid_head: string | null;
  realm_id: string;
  actor_id: string;
  runtime_instance_id: string;
  schema_digest: string;
}

/** What `cross_client host` prints; `task_id`, `state` and `outputs` are present with `--run-once`. */
export interface AstridHostResult {
  capability_id: string;
  executor_id: string;
  task_id?: string | null;
  state?: string;
  outputs?: Array<{ name: string; object_id: string; media_type: string; size: number }>;
}

export interface ManagedMarkerSeed {
  taskId: string;
  objectId: string;
  selection: { generation_id: string; variant_id: string; catalog_digest: string };
}

/** One Astrid call, as recorded for the run summary. */
export interface AstridCall {
  argv: string[];
  durationMs: number;
  exitCode: number | null;
  loadAverageStart: number;
  loadAverageEnd: number;
}

export interface AstridRun { stdout: string; stderr: string; exitCode: number | null; durationMs: number }

/** The `--json` envelope the CLI prints (`{"ok": true, "data": ...}`). */
export interface AstridEnvelope<T = any> { ok: boolean; data?: T; error?: unknown; [key: string]: unknown }

/** Why Astrid cannot run here, or null when it can. Names the checkout, the Python or the module that is missing. */
export function astridUnavailableReason(): string | null {
  if (!existsSync(path.join(ASTRID_CHECKOUT, 'astrid', '__init__.py'))) return `Astrid checkout not found at ${ASTRID_CHECKOUT} (set ASTRID_CHECKOUT)`;
  if (!existsSync(ASTRID_PYTHON)) return `Astrid Python not found at ${ASTRID_PYTHON} (set ASTRID_PYTHON, or make ${ASTRID_CHECKOUT}/.venv)`;
  if (!existsSync(path.join(ASTRID_CHECKOUT, 'astrid', 'core', 'dev', 'cross_client.py'))) return `the Astrid checkout at ${ASTRID_CHECKOUT} has no astrid/core/dev/cross_client.py (card F2-B is not in it)`;
  return null;
}

/** The schema digests the two vendored clients were generated with, read from their generated metadata. */
export function vendoredDigests(): { app: string; astrid: string } {
  const read = (file: string, pattern: RegExp) => {
    if (!existsSync(file)) throw new Error(`cannot read the vendored contract metadata at ${file}`);
    const found = pattern.exec(readFileSync(file, 'utf8'));
    if (!found) throw new Error(`no SCHEMA_DIGEST in ${file}`);
    return found[1];
  };
  return {
    app: read(path.join(REPO_ROOT, 'src', 'integrations', 'runtime', 'generated-contract-metadata.ts'), /SCHEMA_DIGEST = "(sha256:[0-9a-f]+)"/),
    astrid: read(path.join(ASTRID_CHECKOUT, 'astrid_runtime_client', 'contract_metadata.py'), /SCHEMA_DIGEST = '(sha256:[0-9a-f]+)'/),
  };
}

function gitHead(dir: string): string | null {
  try { return execFileSync('git', ['-C', dir, 'rev-parse', 'HEAD'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 10_000 }).trim() || null; } catch { return null; }
}

function vendorLock(file: string): { source_commit: string | null; producer_version: string | null } {
  try {
    const lock = JSON.parse(readFileSync(file, 'utf8'));
    return { source_commit: lock.source_commit ?? null, producer_version: lock.producer_version ?? null };
  } catch { return { source_commit: null, producer_version: null }; }
}

/** The revisions this run tested, for `three-products-summary.json`. Pass the identity the probe printed so `astrid.__file__` is recorded. */
export function revisionSet(identity?: AstridIdentity) {
  const digests = vendoredDigests();
  return {
    appHead: gitHead(REPO_ROOT),
    astridHead: gitHead(ASTRID_CHECKOUT),
    astridFile: identity?.astrid_file ?? null,
    runtimeHead: gitHead(RUNTIME_CHECKOUT),
    vendorLocks: {
      app: vendorLock(path.join(REPO_ROOT, 'runtime.lock.json')),
      astrid: vendorLock(path.join(ASTRID_CHECKOUT, 'runtime.lock.json')),
    },
    schemaDigest: { app: digests.app, astrid: digests.astrid, runtime: identity?.schema_digest ?? null },
  };
}

export class AstridCli {
  readonly calls: AstridCall[] = [];
  private readonly home: string;
  private readonly state: string;
  private readonly data: string;
  private readonly credentialFile: string;
  private readonly token: string;
  /** The marker PNG's colour: fixed per run, and the same on every `host` call (a different colour is a different capability digest, so a task admitted against one is never claimed by the other). */
  readonly markerColor = randomBytes(3).toString('hex');

  private constructor(private readonly harness: DirectHarness, token: string) {
    // A real path: Astrid's credential reader refuses a symlink anywhere in it (the tmp root may be one).
    const root = realpathSync(harness.tmp);
    this.home = path.join(root, 'astrid-home');
    this.state = path.join(root, 'astrid-state');
    this.data = path.join(root, 'astrid-data');
    this.credentialFile = path.join(root, 'astrid-credential.json');
    this.token = token;
  }

  /** Mints the Astrid actor's credential through the Runtime's own route and makes its state roots inside the harness tmp. */
  static async create(harness: DirectHarness): Promise<AstridCli> {
    const reason = astridUnavailableReason();
    if (reason) throw new Error(reason);
    const token = await harness.provisionCredential(ASTRID_ACTOR, 'astrid-credential.json');
    const cli = new AstridCli(harness, token);
    for (const dir of [cli.home, cli.state]) mkdirSync(dir, { recursive: true, mode: 0o700 });
    return cli;
  }

  /** The Astrid actor's bearer token, for the page-wide "no token reached the page" sniff. It is never passed to a process (only its file is). */
  get secret(): string { return this.token; }

  /** Built from nothing: the discovery file is read now, so the endpoint is the Runtime's current one. */
  private env(): NodeJS.ProcessEnv {
    const discovery = this.harness.discovery();
    return {
      PATH: process.env.PATH ?? '/usr/local/bin:/usr/bin:/bin',
      HOME: this.home,
      XDG_STATE_HOME: this.state,
      ASTRID_RUNTIME_DATA_ROOT: this.data,
      PYTHONPATH: [ASTRID_CHECKOUT, RUNTIME_CHECKOUT].join(path.delimiter),
      PYTHONDONTWRITEBYTECODE: '1',
      PYTHONUNBUFFERED: '1',
      ASTRID_TIMELINE_EVAL_ENDPOINT: discovery.endpoint,
      ASTRID_TIMELINE_EVAL_CREDENTIAL: this.credentialFile,
      // The realm the harness made, not the one discovery names: Astrid refuses any other realm, so a mix-up fails loudly.
      ASTRID_TIMELINE_EVAL_REALM_ID: this.harness.realmId,
      ASTRID_TIMELINE_EVAL_ACTOR_ID: ASTRID_ACTOR,
    };
  }

  private redact(text: string): string { return text.split(this.token).join('[astrid-token]'); }

  /** Runs `python <argv>` and records the call. A non-zero exit throws with the output tails unless `ok` is false. */
  async python(argv: string[], options: { ok?: boolean; timeoutMs?: number } = {}): Promise<AstridRun> {
    const env = this.env();
    const started = Date.now();
    const loadAverageStart = loadavg()[0];
    const managed = spawnGroup(ASTRID_PYTHON, argv, { cwd: this.home, env, exactEnv: true });
    let hung = false;
    const timer = setTimeout(() => { hung = true; void stopGroup(managed, 2000); }, options.timeoutMs ?? ASTRID_CALL_CEILING_MS);
    const exitCode = await managed.exited;
    clearTimeout(timer);
    await stopGroup(managed, 2000); // reap a straggler child of the group, which also lets its pipes close
    await managed.closed; // every byte of stdout and stderr has been read
    const durationMs = Date.now() - started;
    this.calls.push({ argv, durationMs, exitCode, loadAverageStart, loadAverageEnd: loadavg()[0] });
    const run: AstridRun = { stdout: this.redact(managed.stdout), stderr: this.redact(managed.stderr), exitCode, durationMs };
    if (hung) throw new Error(`astrid call hung past ${options.timeoutMs ?? ASTRID_CALL_CEILING_MS} ms: ${argv.join(' ')}\n${run.stderr.slice(-1200)}`);
    if ((exitCode === 0) !== (options.ok ?? true)) {
      throw new Error(`astrid call ${options.ok === false ? 'unexpectedly succeeded' : `exited ${exitCode}`}: ${argv.join(' ')}\n${run.stdout.slice(-1200)}\n${run.stderr.slice(-1200)}`);
    }
    return run;
  }

  /** `python -m astrid <args>`. */
  astrid(args: string[], options?: { ok?: boolean; timeoutMs?: number }): Promise<AstridRun> {
    return this.python(['-m', 'astrid', ...args], options);
  }

  private markerIntent() {
    return {
      version: 1, modality: 'image', partial_success_policy: 'reject',
      groups: [{ group_key: 'main', selectors: [{ selector: 'marker', ordinal: 0, variant_key: 'original', required: true }] }],
    };
  }

  private markerEffect(projectId: string) {
    return {
      effect_type: 'generation.publish_v1', target_id: projectId,
      payload: {
        version: 1, modality: 'image', generation_type: 'f2.marker', metadata: {}, partial_success_policy: 'reject',
        groups: [{ group_key: 'main', selectors: [{ selector: 'marker', ordinal: 0, variant_key: 'original', output_port: 'marker', required: true }] }],
      },
    };
  }

  /** Admit a real marker task using the installed test capability's normal public task API. */
  async createMarkerTask(project: string, projectId: string, key: string): Promise<AstridEnvelope<{ task_id: string }>> {
    return this.json(['tasks', 'create', '--project', project, '--capability', 'f2.marker', '--spec', '{}',
      '--generation-intent', JSON.stringify(this.markerIntent()), '--settlement-effect', JSON.stringify(this.markerEffect(projectId)),
      '--idempotency-key', key, '--json']);
  }

  /** Read one exact managed output through the generated Runtime SDK, then bind the requested authored alias. */
  async readManagedMedia(taskId: string, output: string, asset: string): Promise<ManagedMarkerSeed> {
    const program = `
import json, os, sys
from pathlib import Path
from astrid.sdk.workspace_client import resolve_runtime_connection
from astrid_runtime_client import WorkspaceClient
task_id, output_name, asset, project_id = json.loads(sys.argv[1])
endpoint, token = resolve_runtime_connection(os.environ['ASTRID_TIMELINE_EVAL_ENDPOINT'], Path(os.environ['ASTRID_TIMELINE_EVAL_CREDENTIAL']))
client = WorkspaceClient(endpoint, token)
rows, cursor = client.list_managed_outputs(task_id)
assert cursor is None, 'managed output page exceeded bounded fixture read'
row = next((item for item in rows if item.output_port == output_name and item.ordinal == 0), None)
assert row is not None, (task_id, output_name)
captured = client.get_project_media_selection(project_id, {
    'association_id': row.association_id, 'object_id': row.object_id, 'version': row.version})
selection = client.get_project_media_selection(project_id, {
    'asset': asset, 'generation_id': captured['generation_id'], 'variant_id': captured['variant_id']})
verified = client.get_project_verified_media(project_id, selection)
assert verified['selection'] == selection
print(json.dumps({'task_id': task_id, 'object_id': row.object_id, 'selection': selection, 'verified': verified}))
`;
    const run = await this.python(['-c', program, JSON.stringify([taskId, output, asset, this.harness.seed.projectId])]);
    const result = JSON.parse(run.stdout.trim().split('\n').pop()!);
    return { taskId, objectId: result.object_id, selection: result.selection };
  }

  /** Admit and execute one real f2.marker task, retaining its managed immutable selection for fixture seeding. */
  async seedManagedMarker(project: string, projectId: string, key: string, asset: string): Promise<ManagedMarkerSeed> {
    await this.host({ register: true });
    const created = await this.createMarkerTask(project, projectId, key);
    if (!created.ok || !created.data?.task_id) throw new Error(`managed marker admission failed: ${JSON.stringify(created)}`);
    const ran = await this.host({ runOnce: true });
    if (ran.task_id !== created.data.task_id || ran.state !== 'succeeded') throw new Error(`managed marker execution failed: ${JSON.stringify(ran)}`);
    return this.readManagedMedia(created.data.task_id, 'marker', asset);
  }

  /** Read the original pinned basis in Python, then capture and commit with this client's own credential. */
  async commitCaptured(projectId: string, timelineId: string, base: HeadPin, operation:
    { kind: 'track'; id: string } | { kind: 'move'; clipId: string; on: number }
    | { kind: 'label'; trackId: string; label: string }
    | { kind: 'batch'; edits: Array<
      { kind: 'hold'; select: string; delta: number }
      | { kind: 'clear-asset'; select: string }
    > }
    | { kind: 'task-media-swap'; select: string; taskId: string; output: string; oldTaskId: string; oldOutput: string; asset: string }, key: string): Promise<CommitAcceptedMutation> {
    const program = `
import json, sys
from astrid.sdk.client import AstridClient
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_swap_media
from astrid.sdk.timeline.capture import capture_move, capture_track_create
from astrid.sdk.timeline._track_commands import capture_track_set
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.workspace_client import resolve_runtime_connection
from astrid_runtime_client import WorkspaceClient
import os
from pathlib import Path
project, timeline, base, operation, key = json.loads(sys.argv[1])
with AstridClient.open_from_launcher(start_pack_host=False, client_name='three-products-command') as client:
    def read(operation, *args, expected):
        result = client.timelines._typed(operation, *args)
        assert result.ok, result.as_dict()
        row = result.data
        assert all(row.get(field) == value for field, value in expected.items()), (operation, expected)
        return row

    cursor = None
    while True:
        history = client.timelines._typed('list_timeline_commits', project, timeline, cursor=cursor, limit=50)
        assert history.ok, history.as_dict()
        if any(row['revision_id'] == base['revision_id'] and row['publication_id'] == base['publication_id']
               for row in history.data['items']):
            break
        cursor = history.data['next_cursor']
        assert cursor, ('original base pair is missing from scoped history', base)

    parent = read('get_project_parent_composition_revision', project, timeline, base['revision_id'],
                  expected=dict(project_id=project, timeline_id=timeline, revision_id=base['revision_id']))
    manifest = parent['dependency_manifest']
    shots, internals = [], []
    for pin in manifest['shots']:
        row = read('get_project_shot_revision', project, pin['shot_id'], pin['revision_id'],
                   expected=dict(project_id=project, **pin))
        shots.append({**pin, 'payload': row['payload']})
    for pin in manifest['internal_timelines']:
        row = read('get_project_timeline_revision', project, pin['timeline_id'], pin['revision_id'],
                   expected=dict(project_id=project, **pin))
        internals.append({**pin, 'payload': row['payload']})
    # Keep Python's raw JSON numbers and all original document/media pins for digest and closure validation.
    document = dict(schema_version=1, project_id=project, timeline_id=timeline,
                    parent_revision={field: parent[field] for field in ('revision_id', 'content_digest', 'payload')},
                    shot_revisions=shots, internal_timeline_revisions=internals, dependency_manifest=manifest)
    bundle = bundle_from_document(document)
    state = State(bundle)
    if operation['kind'] == 'track':
        command = capture_track_create(bundle, 'parent', {'id': operation['id'], 'kind': 'audio', 'label': operation['id']})
    elif operation['kind'] == 'label':
        command = capture_track_set(bundle, 'parent/track:' + operation['trackId'], values={'label': operation['label']})
    elif operation['kind'] == 'batch':
        commands = []
        for edit in operation['edits']:
            if edit['kind'] == 'hold':
                row = state.entity(edit['select'])
                command = capture_clip_set(bundle, edit['select'], values={'hold': row['hold'] + edit['delta']})
            elif edit['kind'] == 'clear-asset':
                command = capture_clip_set(bundle, edit['select'], clear=['asset'])
            else:
                raise ValueError('unsupported native batch edit kind: ' + edit['kind'])
            commands.append(command)
        body_commands = commands
    elif operation['kind'] == 'task-media-swap':
        endpoint, token = resolve_runtime_connection(client.endpoint, Path(os.environ['ASTRID_TIMELINE_EVAL_CREDENTIAL']))
        runtime = WorkspaceClient(endpoint, token)
        def media(task_id, output, asset):
            rows, cursor = runtime.list_managed_outputs(task_id)
            assert cursor is None, 'managed output page exceeded bounded capture read'
            row = next((item for item in rows if item.output_port == output and item.ordinal == 0), None)
            assert row is not None, (task_id, output)
            captured = runtime.get_project_media_selection(project, {'association_id': row.association_id, 'object_id': row.object_id, 'version': row.version})
            pin = runtime.get_project_media_selection(project, {'asset': asset, 'generation_id': captured['generation_id'], 'variant_id': captured['variant_id']})
            verified = runtime.get_project_verified_media(project, pin)
            assert verified['selection'] == pin
            return pin, verified
        old_media, old_verified = media(operation['oldTaskId'], operation['oldOutput'], 'f2-placeholder')
        new_media, new_verified = media(operation['taskId'], operation['output'], operation['asset'])
        assert old_media['object_id'] != new_media['object_id'], 'swap fixture must use distinct immutable outputs'
        command = capture_occurrence_swap_media(bundle, operation['select'], old_media, new_media, verified_media=[old_verified, new_verified])
        body_commands = [command]
    else:
        command = capture_move(bundle, 'parent/clip:' + operation['clipId'], operation['on'])
        body_commands = [command]
    if operation['kind'] != 'batch' and operation['kind'] != 'task-media-swap':
        body_commands = [command]
    body = dict(api_version=1, project_id=project, timeline_id=timeline,
                base_revision_id=base['revision_id'], base_publication_id=base['publication_id'],
                commands=body_commands, source={'via': 'python'})
    result = client.timelines.commit(project, timeline, body, idempotency_key=key)
    assert result.ok, result.as_dict()
    print(json.dumps(result.as_dict()))
`;
    const run = await this.python(['-c', program, JSON.stringify([projectId, timelineId, base, operation, key])]);
    const result = JSON.parse(run.stdout.trim().split('\n').pop()!);
    if (!result.ok || !result.receipt) throw new Error(`Agent command was not accepted: ${JSON.stringify(result)}`);
    return { data: result.data, receipt: result.receipt } as CommitAcceptedMutation;
  }

  /** `python -m astrid <args>` where the last stdout line is the `--json` envelope; the caller passes `--json`. */
  async json<T = any>(args: string[], options?: { timeoutMs?: number }): Promise<AstridEnvelope<T>> {
    const run = await this.astrid(args, options);
    return parseEnvelope(args, run);
  }

  /** The connected identity, as the handshake and health of this Astrid answer it. */
  async identity(): Promise<AstridIdentity> {
    const run = await this.python(['-m', 'astrid.core.dev.cross_client', 'identity']);
    return JSON.parse(run.stdout.trim().split('\n').pop()!);
  }

  /**
   * `cross_client host`: registers the `f2.marker` executor and, with `runOnce`, claims and runs at most one task. The worker
   * credential is the Runtime's own, named by discovery, and the executor takes the worker's actor id: the Runtime binds a worker
   * credential to the executor it operates (runtime_protocol/service.py `_assert_executor_identity`).
   */
  async host(options: { runOnce?: boolean; register?: boolean }): Promise<AstridHostResult> {
    const discovery = this.harness.discovery();
    const args = ['-m', 'astrid.core.dev.cross_client', 'host',
      '--pack-root', path.join(this.data, 'f2-packs'),
      '--worker-credential', discovery.worker_credential_file,
      '--executor-id', discovery.worker_actor,
      '--color', this.markerColor,
      ...(options.register ? ['--register'] : []),
      ...(options.runOnce ? ['--run-once'] : [])];
    const run = await this.python(args);
    return JSON.parse(run.stdout.trim().split('\n').pop()!);
  }

  /**
   * The checks that must hold before any case: Astrid is the checkout we meant (`astrid.__file__`), it is connected to the
   * harness's realm and Runtime instance, and the App, Astrid and the Runtime agree on the schema digest. Each failure names its cause.
   */
  async preflight(): Promise<AstridIdentity> {
    const digest = contractDigest();
    const health = await fetch(`${this.harness.runtimeUrl}/v1/health`).then((response) => response.json()) as { schema_digest?: string };
    if (health.schema_digest !== digest) {
      throw new Error(`contract mismatch: the Runtime serves schema ${health.schema_digest} but the App and Astrid vendor ${digest}; re-vendor the clients from this Runtime (card C1)`);
    }
    const identity = await this.identity();
    const checkout = realpathSync(ASTRID_CHECKOUT);
    if (!identity.astrid_file.startsWith(checkout + path.sep)) {
      throw new Error(`the wrong Astrid ran: ${identity.astrid_file} is not under ${checkout}; its venv's editable install points elsewhere, so PYTHONPATH must come first`);
    }
    const disagreements = realmDisagreements('Astrid', identity, this.harness, digest);
    if (disagreements.length) throw new Error(disagreements.join('; '));
    return identity;
  }
}

/** The one contract digest the App and Astrid both vendor; throws, naming the older client to re-vendor, when they differ. */
export function contractDigest(): string {
  const digests = vendoredDigests();
  if (digests.app !== digests.astrid) {
    throw new Error(`contract mismatch: the App vendors schema ${digests.app} but Astrid vendors ${digests.astrid}; re-vendor the older one (card C1)`);
  }
  return digests.app;
}

/**
 * Where what a product saw (its realm, the Runtime instance it reached, the schema digest it reports) differs from the harness's
 * realm and instance and from the contract digest. Empty when it agrees; each entry names the product and the cause. The single
 * comparison behind both the preflight and the journey's per-case "same realm" check.
 */
export function realmDisagreements(
  who: string,
  seen: { realm_id?: string; runtime_instance_id?: string; schema_digest?: string },
  harness: Pick<DirectHarness, 'realmId' | 'runtimeInstanceId'>,
  digest: string,
): string[] {
  const problems: string[] = [];
  if (seen.realm_id !== harness.realmId) problems.push(`${who} is connected to realm ${seen.realm_id}, not the harness's ${harness.realmId}`);
  if (seen.runtime_instance_id !== harness.runtimeInstanceId) problems.push(`${who} reached Runtime instance ${seen.runtime_instance_id}, not the harness's ${harness.runtimeInstanceId}`);
  if (seen.schema_digest !== digest) problems.push(`${who} reports schema ${seen.schema_digest}, not ${digest}; re-vendor (C1)`);
  return problems;
}

function parseEnvelope<T>(args: string[], run: AstridRun): AstridEnvelope<T> {
  const text = run.stdout.trim();
  try { return JSON.parse(text); } catch { /* the envelope may follow progress lines */ }
  const line = text.split('\n').reverse().find((candidate) => candidate.trim().startsWith('{'));
  if (!line) throw new Error(`astrid ${args.join(' ')} printed no JSON envelope:\n${run.stdout.slice(-1200)}`);
  return JSON.parse(line);
}
