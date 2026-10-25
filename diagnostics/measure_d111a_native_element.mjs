import { createHash, randomUUID } from 'node:crypto';
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { startDirectHarness } from '/home/user/work/app/tests/e2e/local/support/harness.ts';

const runtime = process.env.D111_REAL_RUNTIME;
const profile = process.env.D111_PROFILE;
const logDir = process.env.D111_LOG_DIR;
const marker = process.env.D111A_REQUEST_MARKER;
if (!runtime || !profile || !logDir || !marker) throw new Error('D111A launcher inputs are required');

const fail = (message, extra = {}) => { throw new Error(`${message}: ${JSON.stringify(extra)}`); };
const object = (value, label) => {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(label);
  return value;
};
const state = (row, key) => Object.hasOwn(row, key) ? { state: 'present', value: row[key] } : { state: 'absent' };

function sourceClips(document) {
  const parent = object(document.parent_revision.payload, 'parent payload');
  const config = object(parent.config, 'parent config');
  const topLevel = !Object.hasOwn(config, 'clips') && Array.isArray(parent.clips);
  const rows = topLevel ? parent.clips : config.clips;
  if (!Array.isArray(rows)) fail('parent clips are not an array');
  return { parent, config, path: topLevel ? ['clips'] : ['config', 'clips'], rows };
}

function readsFor(document, selectedId) {
  const { config, path, rows } = sourceClips(document);
  const order = rows.map((row) => String(row.id));
  if (order.some((id) => !id)) fail('clip identity missing');
  const reads = [{ kind: 'collection', ref: 'parent', path, members: [...order].sort(), order }];
  for (const row of rows) {
    reads.push({ kind: 'field', ref: 'parent', path: [...path, `id:${String(row.id)}`, 'id'], state: state(row, 'id') });
    if (String(row.id) === selectedId) {
      for (const key of ['clipType', 'hold', 'from', 'to', 'speed', 'track', 'at']) {
        reads.push({ kind: 'field', ref: 'parent', path: [...path, `id:${String(row.id)}`, key], state: state(row, key) });
      }
    }
  }
  reads.push({ kind: 'field', ref: 'parent', path: ['config', 'tracks'], state: state(config, 'tracks') });
  return reads;
}

async function canonicalAt(harness, seed, revisionId) {
  const parentResponse = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${revisionId}`);
  if (parentResponse.status !== 200) fail('parent read failed', { status: parentResponse.status });
  const parent = parentResponse.body;
  const manifest = object(parent.dependency_manifest, 'dependency manifest');
  const shots = await Promise.all((manifest.shots ?? []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/shots/${String(pin.shot_id)}/revisions/${String(pin.revision_id)}`);
    if (response.status !== 200) fail('shot read failed', { status: response.status });
    return { ...pin, payload: response.body.payload };
  }));
  const internals = await Promise.all((manifest.internal_timelines ?? []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/revisions/${String(pin.revision_id)}`);
    if (response.status !== 200) fail('internal read failed', { status: response.status });
    return { ...pin, payload: response.body.payload };
  }));
  return { schema_version: 1, project_id: harness.seed.projectId, timeline_id: seed.timelineId,
    parent_revision: { revision_id: String(parent.revision_id), content_digest: String(parent.content_digest), payload: parent.payload },
    shot_revisions: shots, internal_timeline_revisions: internals, dependency_manifest: manifest };
}

function elementRequest(harness, seed, document, head) {
  const { config, rows } = sourceClips(document);
  const selectedId = seed.appClipId;
  const selected = rows.find((row) => String(row.id) === selectedId);
  if (!selected) fail('selected App clip missing', { selectedId });
  const track = typeof selected.track === 'string' && Array.isArray(config.tracks) && config.tracks.some((row) => row.id === selected.track)
    ? selected.track : config.tracks?.find((row) => row.kind === 'visual')?.id ?? config.tracks?.[0]?.id ?? 'elements';
  const duration = typeof selected.hold === 'number' && Number.isFinite(selected.hold)
    ? Math.max(0, selected.hold) : typeof selected.from === 'number' && typeof selected.to === 'number' && selected.to > selected.from
      ? selected.to - selected.from : selected.hold;
  if (typeof selected.at !== 'number' || typeof duration !== 'number') fail('selected clip timing missing');
  const baseId = `element-am-burst-${Math.round(selected.at * 1000)}`;
  let id = baseId;
  let suffix = 2;
  while (rows.some((row) => String(row.id) === id)) id = `${baseId}-${suffix++}`;
  const value = { id, at: selected.at, track, clipType: 'am-burst', hold: duration,
    elementRef: { id: 'am-burst', kind: 'effect', packId: 'astrid_motion', revision: 'sha256:f4b453923da74f104d41baf34ab9760bc7474d53d7ce034e11e0ec0197babf29' } };
  const order = rows.map((row) => String(row.id));
  const reads = readsFor(document, selectedId);
  const changes = [{ op: 'list.insert', ref: 'parent', path: ['clips'], id,
    before: { state: 'absent' }, value, order_before: order, after_id: order.at(-1) }];
  const command = { schema_version: 1, op: 'doc.patch', version: '1', select: null,
    created: [`parent/clip:${id}`], args: { changes } };
  const step = { id: randomUUID(), label: 'Edit timeline', intent: 'timeline.apply_element', tags: [],
    command_ordinals: [0], patch: changes, reads };
  return { key: randomUUID(), body: { api_version: 1, project_id: harness.seed.projectId, timeline_id: seed.timelineId,
    base_revision_id: head.revision_id, base_publication_id: head.publication_id, commands: [command], label: 'Edit timeline',
    steps: [step], merge: 'atomic', reads, dry_run: false, source: { via: 'app' } },
    safe: { selected_id: selectedId, inserted_id: id, source_path: ['clips'], read_count: reads.length, command_op: command.op, intent: step.intent } };
}

const harness = await startDirectHarness({ deferTimelineInitialization: true });
const result = { profile, runtime, source: { app_harness: 'e41f26ec201f9b5874142fb06061020eb6d4f0dc7748af521e4ddafd531765c3', runtime, agent: process.env.ASTRID_CHECKOUT }, phases: [] };
try {
  result.phases.push('startup-ready');
  harness.withdrawProductCredential();
  try {
    const response = await fetch(`${harness.runtimeUrl}/v1/projects/unknown`, {
      headers: { 'X-D111A-Refusal-Tag': 'startup-auth-refusal' },
    });
    result.positive_control = { kind: 'product-credential-withdrawal', tag: 'startup-auth-refusal', status: response.status };
  } finally { harness.restoreProductCredential(); }
  result.phases.push('tagged-refusal-control');
  const seed = await harness.seedThreeProducts(15, 'native-none');
  result.seed = { timeline_id: seed.timelineId, head_revision_id: seed.headRevisionId, app_clip_id: seed.appClipId };
  result.phases.push('native-seed');
  if (result.positive_control.status !== 401) fail('credential refusal control failed');
  const history = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  if (history.status !== 200) fail('history read failed', { status: history.status });
  const document = await canonicalAt(harness, seed, history.body.head.revision_id);
  const request = elementRequest(harness, seed, document, history.body.head);
  const requestText = JSON.stringify(request.body);
  const requestHash = createHash('sha256').update(requestText).digest('hex');
  result.element = request.safe;
  result.request = { route: `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commit`, request_sha256: requestHash,
    request_bytes: Buffer.byteLength(requestText), start_utc: new Date().toISOString() };
  writeFileSync(`${logDir}/request.json`, requestText, { mode: 0o600 });
  writeFileSync(marker, 'active\n', { mode: 0o600 });
  const start = process.hrtime.bigint();
  const response = await harness.runtimeFetch(result.request.route, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': request.key },
    body: requestText, signal: AbortSignal.timeout(120_000) });
  const body = await response.json().catch(() => null);
  const elapsedMs = Number(process.hrtime.bigint() - start) / 1e6;
  writeFileSync(marker, 'done\n', { mode: 0o600 });
  writeFileSync(`${logDir}/reply.json`, JSON.stringify(body), { mode: 0o600 });
  result.request.end_utc = new Date().toISOString();
  result.request.elapsed_ms = elapsedMs;
  result.request.pid = harness.runtime?.child.pid;
  result.request.outcome = response.status;
  result.reply = { status: response.status, body_keys: body && typeof body === 'object' ? Object.keys(body).sort() : [], receipt_present: Boolean(body?.receipt),
    accepted: body?.accepted === true, merged: body?.merged === true, refused: body?.status === 'refused' || response.status === 409,
    conflict: response.status === 409, invalid: response.status === 422 };
  result.phases.push('element-response');
} catch (error) {
  result.error = { class: error?.constructor?.name ?? 'unknown', message: String(error?.message ?? error) };
} finally {
  try { writeFileSync(marker, 'done\n', { mode: 0o600 }); } catch { /* evidence root may not exist after startup failure */ }
  const managed = harness.runtime;
  result.runtime_pid = managed?.child.pid;
  await harness.stop().catch((error) => { result.stop_error = String(error?.message ?? error); });
  mkdirSync(logDir, { recursive: true });
  if (managed) {
    writeFileSync(`${logDir}/runtime.stdout.log`, managed.stdout, { mode: 0o600 });
    writeFileSync(`${logDir}/runtime.stderr.log`, managed.stderr, { mode: 0o600 });
  }
}
result.lifecycle = harness.lifecycleObservation;
result.runtime_logs = { stdout: `${logDir}/runtime.stdout.log`, stderr: `${logDir}/runtime.stderr.log` };
try { result.runtime_stderr_sha256 = createHash('sha256').update(readFileSync(`${logDir}/runtime.stderr.log`)).digest('hex'); } catch { result.runtime_stderr_sha256 = null; }
const profiles = [];
for (const name of readdirSync(logDir).filter((item) => item.startsWith('profile-') && item.endsWith('.json'))) {
  const item = JSON.parse(readFileSync(`${logDir}/${name}`, 'utf8'));
  profiles.push({ file: name, pid: item.pid, process_identity: item.process_identity, sampling_interval_ms: item.sampling_interval_ms,
    lost_samples: item.lost_samples, observer_cpu_ms: item.observer_cpu_ms, sample_total: item.sample_total,
    top_inclusive_frames: item.top_inclusive_frames, function_counts: item.function_counts,
    function_inclusive_cpu_ns: item.function_inclusive_cpu_ns, requests: item.requests,
    inclusive_overlap: item.inclusive_overlap, sample_membership: item.sample_membership,
    handlers: item.handlers, read_metrics: item.read_metrics, metric_errors: item.metric_errors,
    sampler_errors: item.sampler_errors });
}
result.profiles = profiles;
result.lifecycle = {
  cold: 'startup, credential-refusal control, genuine provider seed, and preflight reads before the measured POST',
  warm: 'the measured element POST in the same provider/runtime process; no cache reset or forced history reset',
};
mkdirSync(logDir, { recursive: true });
writeFileSync(`${logDir}/result-${profile}.json`, `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 });
console.log(JSON.stringify({ completed: !result.error, status: result.reply?.status, pid: result.request?.pid, profiles: profiles.length }));
if (result.error || result.reply?.status !== 200 || !result.reply.receipt_present) process.exitCode = 1;
