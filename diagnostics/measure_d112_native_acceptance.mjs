import { createHash, randomUUID } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { startDirectHarness } from '/home/user/work/app/tests/e2e/local/support/harness.ts';

const runtime = process.env.D112_REAL_RUNTIME;
const agent = process.env.ASTRID_CHECKOUT;
const logDir = process.env.D112_LOG_DIR;
const stage = process.env.D112_STAGE;
if (!runtime || !agent || !logDir || !stage) throw new Error('D112 launcher inputs are required');
const py = process.env.ASTRID_PYTHON || '/home/user/work/venv-agent/bin/python';
const digest = (value) => createHash('sha256').update(value).digest('hex');
const fail = (message, value) => { throw new Error(`${message}: ${JSON.stringify(value)}`); };

async function canonicalAt(harness, seed, revisionId) {
  const parentResponse = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${revisionId}`);
  if (parentResponse.status !== 200) fail('parent read failed', parentResponse.status);
  const parent = parentResponse.body;
  const manifest = parent.dependency_manifest || {};
  const shots = await Promise.all((manifest.shots || []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/shots/${pin.shot_id}/revisions/${pin.revision_id}`);
    if (response.status !== 200) fail('shot read failed', response.status);
    return { ...pin, payload: response.body.payload };
  }));
  const internals = await Promise.all((manifest.internal_timelines || []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/revisions/${pin.revision_id}`);
    if (response.status !== 200) fail('internal read failed', response.status);
    return { ...pin, payload: response.body.payload };
  }));
  return { schema_version: 1, project_id: seed.projectId, timeline_id: seed.timelineId,
    parent_revision: { revision_id: parent.revision_id, content_digest: parent.content_digest, payload: parent.payload },
    shot_revisions: shots, internal_timeline_revisions: internals, dependency_manifest: manifest };
}

async function pinFor(harness, seed, document, alias) {
  const parent = document.parent_revision.payload;
  const registries = [parent.registry, parent.config?.registry,
    ...(document.internal_timeline_revisions || []).map((revision) => revision.payload?.registry)];
  const entry = registries.find((registry) => registry?.assets?.[alias])?.assets?.[alias];
  if (!entry?.generationId || !entry?.variantId) fail('missing genuine registry pin', alias);
  const query = new URLSearchParams({ asset: entry.variantId, generation_id: entry.generationId, variant_id: entry.variantId });
  const selectedResponse = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/media-selection?${query}`);
  if (selectedResponse.status !== 200) fail('media selection failed', selectedResponse.status);
  const selected = selectedResponse.body.data || selectedResponse.body;
  const verifiedQuery = new URLSearchParams({ asset: selected.asset, generation_id: selected.generation_id,
    variant_id: selected.variant_id, object_id: selected.object_id, catalog_digest: selected.catalog_digest });
  const verifiedResponse = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/media-selection/verified?${verifiedQuery}`);
  if (verifiedResponse.status !== 200) fail('verified media failed', verifiedResponse.status);
  return { selected, verified: verifiedResponse.body.data || verifiedResponse.body };
}

async function importFreshPin(harness, seed, source, filename) {
  const object = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(source.objectId)}`);
  if (object.status !== 200) fail('fresh source read failed', object.status);
  const imported = await harness.runtimeFetch(`/v1/projects/${seed.projectId}/media-imports`, {
    method: 'POST',
    headers: { 'Content-Type': source.mediaType, 'Idempotency-Key': randomUUID(), 'X-Original-Name': filename },
    body: new Uint8Array(await object.arrayBuffer()),
  });
  if (imported.status !== 201) fail('fresh media import failed', imported.status);
  const importedData = await imported.json();
  const data = importedData.data || importedData;
  const selectedResponse = await harness.runtimeJson('GET',
    `/v1/projects/${seed.projectId}/media-selection?asset=${encodeURIComponent(data.variant_id)}&generation_id=${encodeURIComponent(data.generation_id)}&variant_id=${encodeURIComponent(data.variant_id)}`);
  if (selectedResponse.status !== 200) fail('fresh media selection failed', selectedResponse.status);
  const selected = selectedResponse.body.data || selectedResponse.body;
  const verifiedResponse = await harness.runtimeJson('GET',
    `/v1/projects/${seed.projectId}/media-selection/verified?asset=${encodeURIComponent(selected.asset)}&generation_id=${encodeURIComponent(selected.generation_id)}&variant_id=${encodeURIComponent(selected.variant_id)}&object_id=${encodeURIComponent(selected.object_id)}&catalog_digest=${encodeURIComponent(selected.catalog_digest)}`);
  if (verifiedResponse.status !== 200) fail('fresh media verification failed', verifiedResponse.status);
  return { selected, verified: verifiedResponse.body.data || verifiedResponse.body };
}

function agentCommand(document, operation, media, verified, row) {
  const input = JSON.stringify({ document, operation, media, verified, row });
  const source = [
    'import json,sys',
    'from astrid.sdk.timeline.commit import bundle_from_document',
    'from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_add_media,capture_occurrence_swap_media',
    'd=json.load(sys.stdin)',
    "b=bundle_from_document(d['document'])",
    "c=(capture_occurrence_add_media(b,'occurrence:f2-occurrence',d['row'],d['media'],verified_media=[d['verified']]) if d['operation']=='add' else capture_occurrence_swap_media(b,'occurrence:f2-occurrence/clip:'+d['row']['id'],d['row']['old_media'],d['media'],verified_media=[d['verified'],d['row']['old_verified']]))",
    'print(json.dumps(c,separators=(\",\",\":\")))',
  ].join(';');
  return JSON.parse(execFileSync(py, ['-c', source], { input, cwd: agent, encoding: 'utf8', env: {
    ...process.env, PYTHONPATH: agent, ASTRID_CHECKOUT: agent, PYTHONDONTWRITEBYTECODE: '1',
  } }).trim());
}

function requestFor(seed, head, command, label) {
  return { api_version: 1, project_id: seed.projectId, timeline_id: seed.timelineId,
    base_revision_id: head.revision_id, base_publication_id: head.publication_id,
    commands: [command], label, steps: [{ id: `${label}-step`, label, intent: label,
      tags: ['D112native'], command_ordinals: [0], patch: [], reads: [] }],
    merge: 'atomic', reads: [], dry_run: false };
}

async function post(harness, seed, request, key) {
  const text = JSON.stringify(request);
  const response = await harness.runtimeFetch(`/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/commit`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': key },
    body: text, signal: AbortSignal.timeout(120000),
  });
  const body = await response.json().catch(() => null);
  return { status: response.status, body, bytes: Buffer.byteLength(text), request_sha256: digest(text) };
}

async function history(harness, seed) {
  const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  if (response.status !== 200) fail('history read failed', response.status);
  return response.body;
}

async function main() {
  const harness = await startDirectHarness({ deferTimelineInitialization: false });
  const result = { task: 'D112native', stage, runtime, agent, phases: [] };
  try {
    result.lifecycle_start = harness.lifecycleObservation;
    result.phases.push('startup-witness');
    harness.withdrawProductCredential();
    try {
      const refused = await fetch(`${harness.runtimeUrl}/v1/projects/unknown`);
      result.tagged_refusal = { tag: 'D112native-startup-refusal', status: refused.status };
    } finally { harness.restoreProductCredential(); }
    if (result.tagged_refusal.status !== 401) fail('tagged refusal was not 401', result.tagged_refusal);
    result.phases.push('tagged-refusal-control');
    const seed = { ...harness.seed, ...await harness.seedThreeProducts(15, 'native-none') };
    result.seed = { project_id: seed.projectId, timeline_id: seed.timelineId, head_revision_id: seed.headRevisionId };
    result.phases.push('genuine-registered-provider-seed');
    let current = await history(harness, seed);
    let document = await canonicalAt(harness, seed, current.head.revision_id);
    const image = await importFreshPin(harness, seed, harness.seed.image, 'd112-native-add.png');
    const replacement = await importFreshPin(harness, seed, harness.seed.image, 'd112-native-swap.png');
    result.source = { initial_history_items: current.items?.length ?? null,
      selection_fields: Object.keys(image.selected).sort(), verified_fields: Object.keys(image.verified).sort(),
      initial_head_revision_id: current.head.revision_id };
    const addRow = { id: `d112-native-add-${randomUUID()}`, clipType: 'image', track: 'V2', asset: image.selected.asset,
      at: 9, hold: 3 };
    const add = agentCommand(document, 'add', image.selected, image.verified, addRow);
    result.add_command = { op: add.op, select: add.select, created: add.created,
      arg_keys: Object.keys(add.args).sort() };
    const addKey = `D112native-${stage}-add-${randomUUID()}`;
    const addReply = await post(harness, seed, requestFor(seed, current.head, add, 'D112native ADD'), addKey);
    result.add_reply = { status: addReply.status, body_keys: Object.keys(addReply.body || {}).sort(),
      receipt_present: Boolean(addReply.body?.receipt), code: addReply.body?.code,
      message_class: typeof addReply.body?.message === 'string' ? addReply.body.message.slice(0, 120) : null,
      detail_keys: Object.keys(addReply.body?.details || {}).sort(), bytes: addReply.bytes, request_sha256: addReply.request_sha256 };
    if (addReply.status !== 200 || !addReply.body?.receipt) fail('native ADD refused', result.add_reply);
    result.phases.push('native-add-accepted');
    current = await history(harness, seed);
    document = await canonicalAt(harness, seed, current.head.revision_id);
    const added = document.internal_timeline_revisions[0].payload.clips.find((item) => item.id === addRow.id);
    if (!added) fail('native ADD did not materialize', addRow.id);
    const swap = agentCommand(document, 'swap', replacement.selected, replacement.verified,
      { id: added.id, old_media: image.selected, old_verified: image.verified });
    result.swap_command = { op: swap.op, select: swap.select, arg_keys: Object.keys(swap.args).sort() };
    const swapKey = `D112native-${stage}-swap-${randomUUID()}`;
    const swapReply = await post(harness, seed, requestFor(seed, current.head, swap, 'D112native SWAP'), swapKey);
    result.swap_reply = { status: swapReply.status, body_keys: Object.keys(swapReply.body || {}).sort(),
      receipt_present: Boolean(swapReply.body?.receipt), code: swapReply.body?.code,
      message_class: typeof swapReply.body?.message === 'string' ? swapReply.body.message.slice(0, 120) : null,
      detail_keys: Object.keys(swapReply.body?.details || {}).sort(), bytes: swapReply.bytes, request_sha256: swapReply.request_sha256 };
    if (swapReply.status !== 200 || !swapReply.body?.receipt) fail('native SWAP refused', result.swap_reply);
    result.phases.push('native-swap-accepted');
    current = await history(harness, seed);
    const undo = { schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
      args: { publications: [swapReply.body.receipt.receipt_id] } };
    const undoKey = `D112native-${stage}-undo-${randomUUID()}`;
    const undoReply = await post(harness, seed, requestFor(seed, current.head, undo, 'D112native nativeUndo'), undoKey);
    result.undo_reply = { status: undoReply.status, body_keys: Object.keys(undoReply.body || {}).sort(),
      receipt_present: Boolean(undoReply.body?.receipt), code: undoReply.body?.code,
      message_class: typeof undoReply.body?.message === 'string' ? undoReply.body.message.slice(0, 120) : null,
      detail_keys: Object.keys(undoReply.body?.details || {}).sort(), bytes: undoReply.bytes, request_sha256: undoReply.request_sha256 };
    if (undoReply.status !== 200 || !undoReply.body?.receipt) fail('nativeUndo refused', result.undo_reply);
    result.phases.push('native-undo-accepted');
    current = await history(harness, seed);
    result.final_controls = { history_items: current.items?.length ?? null, head_revision_id: current.head.revision_id,
      head_publication_id: current.head.publication_id, canonical_history_status: 200 };
  } catch (error) {
    result.error = { class: error?.constructor?.name || 'Error', message: String(error?.message || error) };
  } finally {
    const managed = harness.runtime;
    result.runtime_pid = managed?.child.pid;
    await harness.stop().catch((error) => { result.stop_error = String(error?.message || error); });
    mkdirSync(logDir, { recursive: true, mode: 0o700 });
    if (managed) {
      const stdout = managed.stdout || '';
      writeFileSync(`${logDir}/runtime.stdout.log`, `${JSON.stringify({
        sha256: digest(stdout), bytes: Buffer.byteLength(stdout), lines: stdout.split('\n').filter(Boolean).length,
      })}\n`, { mode: 0o600 });
      writeFileSync(`${logDir}/runtime.stderr.log`, managed.stderr, { mode: 0o600 });
    }
    result.lifecycle_end = harness.lifecycleObservation;
  }
  const stderr = readFileSync(`${logDir}/runtime.stderr.log`);
  result.runtime_stderr_sha256 = digest(stderr);
  result.runtime_stderr_bytes = stderr.length;
  writeFileSync(`${logDir}/result-${stage}.json`, `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 });
  console.log(JSON.stringify({ stage, completed: !result.error, add: result.add_reply?.status,
    swap: result.swap_reply?.status, undo: result.undo_reply?.status, stderr_sha256: result.runtime_stderr_sha256 }));
  if (result.error || result.add_reply?.status !== 200 || result.swap_reply?.status !== 200 || result.undo_reply?.status !== 200) process.exitCode = 1;
}
await main();
