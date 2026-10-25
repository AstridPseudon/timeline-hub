import { createHash, randomUUID } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { startDirectHarness } from '/home/user/work/app/tests/e2e/local/support/harness.ts';

const stage = process.env.D111B_STAGE;
const logDir = process.env.D111B_LOG_DIR;
const runId = process.env.D111B_RUN_ID;
if (!stage || !logDir || !runId) throw new Error('D111b launcher inputs are required');

const digest = (value) => createHash('sha256').update(value).digest('hex');
const fail = (message, value) => { throw new Error(`${message}: ${JSON.stringify(value)}`); };
const stable = (value) => Array.isArray(value) ? value.map(stable) : value && typeof value === 'object'
  ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, stable(value[key])])) : value;

function state(value, key) {
  return Object.hasOwn(value, key) ? { state: 'present', value: value[key] } : { state: 'absent' };
}

function sourceClips(document) {
  const parent = document.parent_revision.payload;
  const config = parent.config ?? {};
  const topLevel = !Object.hasOwn(config, 'clips') && Array.isArray(parent.clips);
  return { config, path: topLevel ? ['clips'] : ['config', 'clips'], rows: topLevel ? parent.clips : config.clips };
}

function readsFor(document, selectedId) {
  const { config, path, rows } = sourceClips(document);
  const order = rows.map((row) => String(row.id));
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
  const parentResponse = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${revisionId}`);
  if (parentResponse.status !== 200) fail('parent read failed', parentResponse.status);
  const parent = parentResponse.body;
  const manifest = parent.dependency_manifest ?? {};
  const shots = await Promise.all((manifest.shots ?? []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/shots/${pin.shot_id}/revisions/${pin.revision_id}`);
    if (response.status !== 200) fail('shot read failed', response.status);
    return { ...pin, payload: response.body.payload };
  }));
  const internals = await Promise.all((manifest.internal_timelines ?? []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/revisions/${pin.revision_id}`);
    if (response.status !== 200) fail('internal read failed', response.status);
    return { ...pin, payload: response.body.payload };
  }));
  return { schema_version: 1, project_id: seed.projectId, timeline_id: seed.timelineId,
    parent_revision: { revision_id: parent.revision_id, content_digest: parent.content_digest, payload: parent.payload },
    shot_revisions: shots, internal_timeline_revisions: internals, dependency_manifest: manifest };
}

function requestFor(seed, head, document, ordinal) {
  const { config, path, rows } = sourceClips(document);
  const selected = rows.find((row) => String(row.id) === 'f2-app-clip');
  if (!selected) fail('seed selected clip missing');
  const id = `d111b-native-${ordinal}`;
  const track = typeof selected.track === 'string' && Array.isArray(config.tracks) && config.tracks.some((row) => row.id === selected.track)
    ? selected.track : config.tracks?.find((row) => row.kind === 'visual')?.id ?? config.tracks?.[0]?.id ?? 'elements';
  const duration = typeof selected.hold === 'number' && Number.isFinite(selected.hold)
    ? Math.max(0, selected.hold) : typeof selected.from === 'number' && typeof selected.to === 'number' && selected.to > selected.from
      ? selected.to - selected.from : undefined;
  if (typeof selected.at !== 'number' || typeof duration !== 'number') fail('selected timing missing', selected);
  const inserted = { id, at: selected.at, track, clipType: 'am-burst', hold: duration,
    elementRef: { id: 'am-burst', kind: 'effect', packId: 'astrid_motion', revision: 'sha256:f4b453923da74f104d41baf34ab9760bc7474d53d7ce034e11e0ec0197babf29' } };
  const reads = readsFor(document, String(selected.id));
  const order = rows.map((row) => String(row.id));
  const changes = [{ op: 'list.insert', ref: 'parent', path: ['clips'], id, before: { state: 'absent' }, value: inserted,
    order_before: order, after_id: order.at(-1) }];
  const command = { schema_version: 1, op: 'doc.patch', version: '1', select: null,
    created: [`parent/clip:${id}`], args: { changes } };
  const step = { id: `d111b-step-${ordinal}`, label: 'D111b native element', intent: 'timeline.apply_element',
    tags: ['D111b'], command_ordinals: [0], patch: changes, reads };
  return { api_version: 1, project_id: seed.projectId, timeline_id: seed.timelineId,
    base_revision_id: head.revision_id, base_publication_id: head.publication_id, commands: [command],
    label: `D111b native element ${ordinal}`, steps: [step], merge: 'atomic', reads, dry_run: false, source: { via: 'app' } };
}

async function history(harness, seed) {
  const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/commits?limit=100`);
  if (response.status !== 200) fail('history read failed', response.status);
  return response.body;
}

function canonicalDigest(value) {
  return `sha256:${digest(JSON.stringify(value, Object.keys(value).sort()))}`;
}

async function main() {
  const harness = await startDirectHarness({ deferTimelineInitialization: false });
  const result = { task: 'D111bnative', stage, run_id: runId, runtime: process.env.D111B_REAL_RUNTIME,
    phases: [], points: [], lifecycle_start: harness.lifecycleObservation };
  try {
    result.phases.push('startup-witness');
    harness.withdrawProductCredential();
    try {
      const tag = `d111b-refusal-${runId}`;
      const refused = await fetch(`${harness.runtimeUrl}/v1/projects/unknown`, { headers: { 'X-D111B-Refusal-Tag': tag } });
      result.tagged_refusal = { tag, status: refused.status, request_id: refused.headers.get('X-Request-ID') };
    } finally { harness.restoreProductCredential(); }
    if (result.tagged_refusal.status !== 401) fail('tagged refusal was not 401', result.tagged_refusal);
    result.phases.push('tagged-refusal-control');

    const three = await harness.seedThreeProducts(15, 'native-none');
    const seed = { ...harness.seed, ...three };
    result.seed = { project_id: seed.projectId, timeline_id: seed.timelineId, app_clip_id: seed.appClipId };
    result.phases.push('genuine-registered-provider-seed');
    let current = await history(harness, seed);
    let document = await canonicalAt(harness, seed, current.head.revision_id);
    result.initial = { history_items: current.items?.length ?? null,
      canonical_document_bytes: Buffer.byteLength(JSON.stringify(document)),
      parent_payload_bytes: Buffer.byteLength(JSON.stringify(document.parent_revision.payload)) };

    const pointOrdinals = [0, 1, 3, 7];
    for (let ordinal = 0; ordinal < 8; ordinal += 1) {
      const request = requestFor(seed, current.head, document, ordinal);
      const requestText = JSON.stringify(request);
      const key = `D111b-${stage}-native-${ordinal}`;
      const started = process.hrtime.bigint();
      const response = await harness.runtimeFetch(`/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/commit`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': key }, body: requestText,
        signal: AbortSignal.timeout(120000),
      });
      const body = await response.json().catch(() => null);
      const elapsedMs = Number(process.hrtime.bigint() - started) / 1e6;
      if (response.status !== 200 || !body?.receipt) fail('native commit refused', { ordinal, status: response.status, body });
      const receiptDocument = body.receipt.canonical_document ?? body.data?.canonical_document;
      if (!receiptDocument) fail('receipt omitted canonical document', ordinal);
      current = await history(harness, seed);
      const readback = await canonicalAt(harness, seed, current.head.revision_id);
      const receiptText = JSON.stringify(stable(receiptDocument));
      const readbackText = JSON.stringify(stable(readback));
      if (receiptText !== readbackText) fail('receipt/readback mismatch', { ordinal, receipt_sha256: digest(receiptText), readback_sha256: digest(readbackText) });
      const point = { ordinal, status: response.status, request_bytes: Buffer.byteLength(requestText), request_sha256: digest(requestText),
        response_bytes: Number(response.headers.get('Content-Length') ?? Buffer.byteLength(JSON.stringify(body))), elapsed_ms: elapsedMs,
        history_items: current.items?.length ?? null, canonical_document_bytes: Buffer.byteLength(readbackText),
        receipt_sha256: digest(receiptText), receipt_id: body.receipt.receipt_id ?? body.data?.receipt?.receipt_id ?? null,
        canonical_digest: body.receipt.document_digest ?? body.data?.document_digest ?? canonicalDigest(receiptDocument),
        existing_rows_preserved: sourceClips(readback).rows.some((row) => String(row.id) === 'f2-app-clip'),
        receipt_readback_byte_identical: receiptText === readbackText };
      result.points.push(point);
      if (pointOrdinals.includes(ordinal)) result.phases.push(`native-accepted-${ordinal}`);
      document = readback;
    }
    result.final = { history_items: current.items?.length ?? null, head_revision_id: current.head.revision_id,
      head_publication_id: current.head.publication_id, canonical_document_bytes: Buffer.byteLength(JSON.stringify(document)) };
    result.phases.push('receipts-canonical-history-verified');
  } catch (error) {
    result.error = { class: error?.constructor?.name || 'Error', message: String(error?.message || error) };
  } finally {
    const managed = harness.runtime;
    result.runtime_pid = managed?.child.pid;
    await harness.stop().catch((error) => { result.stop_error = String(error?.message || error); });
    if (managed) {
      writeFileSync(`${logDir}/runtime.stdout.log`, JSON.stringify({ sha256: digest(managed.stdout), bytes: Buffer.byteLength(managed.stdout), lines: managed.stdout.split('\n').filter(Boolean).length }) + '\n', { mode: 0o600 });
      writeFileSync(`${logDir}/runtime.stderr.log`, managed.stderr, { mode: 0o600 });
    }
    result.lifecycle_end = harness.lifecycleObservation;
  }
  result.runtime_stderr_sha256 = digest(readFileSync(`${logDir}/runtime.stderr.log`));
  result.runtime_stderr_bytes = readFileSync(`${logDir}/runtime.stderr.log`).byteLength;
  result.runtime_stderr_capture = 'direct';
  mkdirSync(logDir, { recursive: true, mode: 0o700 });
  writeFileSync(`${logDir}/result-${stage}.json`, `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 });
  console.log(JSON.stringify({ stage, completed: !result.error, points: result.points.length, stderr_sha256: result.runtime_stderr_sha256 }));
  if (result.error || result.points.length !== 8) process.exitCode = 1;
}

await main();
