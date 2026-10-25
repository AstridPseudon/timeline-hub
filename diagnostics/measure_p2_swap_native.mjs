import { createHash, randomUUID } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { makePng, startDirectHarness } from '/home/user/work/app/tests/e2e/local/support/harness.ts';

const runtime = process.env.P2_SWAP_RUNTIME;
const agent = process.env.P2_SWAP_AGENT;
const evidence = process.env.P2_SWAP_EVIDENCE;
if (!runtime || !agent || !evidence) throw new Error('P2 SWAP launcher inputs are required');
const py = process.env.ASTRID_PYTHON || '/home/user/work/venv-agent/bin/python';
const digest = (value) => createHash('sha256').update(value).digest('hex');
const jsonDigest = (value) => digest(JSON.stringify(value));
const fail = (message, value) => { throw new Error(`${message}: ${JSON.stringify(value)}`); };

function safeBody(body) {
  const value = body?.data && typeof body.data === 'object' ? body.data : body;
  const details = value?.details && typeof value.details === 'object' ? value.details : {};
  return {
    keys: body && typeof body === 'object' ? Object.keys(body).sort() : [],
    data_keys: value && typeof value === 'object' ? Object.keys(value).sort() : [],
    detail_keys: Object.keys(details).sort(),
    reason: details.reason ?? value?.reason ?? body?.reason ?? null,
    code: value?.code ?? body?.code ?? null,
    path: value?.path ?? body?.path ?? null,
    hint: typeof (value?.hint ?? body?.hint) === 'string' ? (value?.hint ?? body?.hint).slice(0, 160) : null,
  };
}

async function canonicalAt(harness, seed, revisionId) {
  const parentResponse = await harness.runtimeFetch(`/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${revisionId}`);
  if (parentResponse.status !== 200) fail('parent read failed', parentResponse.status);
  const rawParent = await parentResponse.text();
  const parent = JSON.parse(rawParent);
  const manifest = parent.dependency_manifest || {};
  const shots = await Promise.all((manifest.shots || []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/shots/${pin.shot_id}/revisions/${pin.revision_id}`);
    if (response.status !== 200) fail('shot read failed', response.status);
    if (response.body.content_digest !== pin.content_digest) fail('shot content digest mismatch', { revision_id: pin.revision_id });
    return { ...pin, payload: response.body.payload };
  }));
  const internals = await Promise.all((manifest.internal_timelines || []).map(async (pin) => {
    const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/revisions/${pin.revision_id}`);
    if (response.status !== 200) fail('internal read failed', response.status);
    if (response.body.content_digest !== pin.content_digest) fail('internal content digest mismatch', { revision_id: pin.revision_id });
    return { ...pin, payload: response.body.payload };
  }));
  return { schema_version: 1, project_id: seed.projectId, timeline_id: seed.timelineId,
    parent_revision: { revision_id: parent.revision_id, content_digest: parent.content_digest, payload: parent.payload },
    shot_revisions: shots, internal_timeline_revisions: internals, dependency_manifest: manifest,
    raw_parent_body: rawParent };
}

async function history(harness, seed) {
  const response = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  if (response.status !== 200) fail('history read failed', response.status);
  return response.body;
}

async function selectedPin(harness, seed, selected) {
  const verifiedQuery = new URLSearchParams({ asset: selected.asset, generation_id: selected.generation_id,
    variant_id: selected.variant_id, object_id: selected.object_id, catalog_digest: selected.catalog_digest });
  const verifiedResponse = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/media-selection/verified?${verifiedQuery}`);
  if (verifiedResponse.status !== 200) fail('verified media failed', verifiedResponse.status);
  return { selected, verified: verifiedResponse.body.data || verifiedResponse.body };
}

async function importBytes(harness, seed, bytes, filename) {
  const imported = await harness.runtimeFetch(`/v1/projects/${seed.projectId}/media-imports`, {
    method: 'POST', headers: { 'Content-Type': 'image/png', 'Idempotency-Key': randomUUID(), 'X-Original-Name': filename },
    body: new Uint8Array(bytes),
  });
  if (imported.status !== 201) fail('media import failed', imported.status);
  const importedBody = await imported.json();
  const data = importedBody.data || importedBody;
  const selectedResponse = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/media-selection?asset=${encodeURIComponent(data.variant_id)}&generation_id=${encodeURIComponent(data.generation_id)}&variant_id=${encodeURIComponent(data.variant_id)}`);
  if (selectedResponse.status !== 200) fail('media selection failed', selectedResponse.status);
  return { ...await selectedPin(harness, seed, selectedResponse.body.data || selectedResponse.body),
    entry: { media_id: data.entry?.object_id || data.object_id, type: 'image', generationId: data.generation_id, variantId: data.variant_id } };
}

async function importFreshPin(harness, seed, source, filename) {
  const object = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(source.objectId)}`);
  if (object.status !== 200) fail('fresh source read failed', object.status);
  return importBytes(harness, seed, new Uint8Array(await object.arrayBuffer()), filename);
}

function agentCommand(document, operation, media, verified, values, stage = operation) {
  const { raw_parent_body, ...canonicalDocument } = document;
  const input = JSON.stringify({ document: canonicalDocument, raw_parent_body, operation, media, verified, ...values });
  const source = [
    'import json,sys',
    'from astrid.sdk.timeline.commit import _digest, bundle_from_document',
    'from astrid.sdk.timeline.native_occurrence_fork import capture_occurrence_fork',
    'from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_swap_media',
    'd=json.load(sys.stdin)',
    'd.get("raw_parent_body") and d["document"]["parent_revision"].update(payload=json.loads(d["raw_parent_body"])["payload"])',
    'images=[("parent",d["document"]["parent_revision"]),*( ("shot:"+str(x.get("revision_id")),x) for x in d["document"]["shot_revisions"]),*(("internal:"+str(x.get("revision_id")),x) for x in d["document"]["internal_timeline_revisions"])]',
    'bad=[{"image":name,"revision_id":row.get("revision_id"),"declared":row.get("content_digest"),"actual":_digest(row.get("payload"))} for name,row in images if row.get("content_digest")!=_digest(row.get("payload"))]',
    'bad and sys.exit("immutable payload digest mismatch:"+json.dumps(bad,separators=(",",":")))',
    'b=bundle_from_document(d["document"])',
    'c=(capture_occurrence_fork(b,d["owner"],d["shot_id"]) if d["operation"]=="fork" else capture_occurrence_swap_media(b,d["select"],d["old_media"],d["media"],verified_media=[d["verified"],d["old_verified"]]))',
    'print(json.dumps(c,separators=(",",":")))',
  ].join(';');
  try {
    return JSON.parse(execFileSync(py, ['-c', source], { input, cwd: agent, encoding: 'utf8', env: {
      ...process.env, PYTHONPATH: agent, ASTRID_CHECKOUT: agent, PYTHONDONTWRITEBYTECODE: '1',
    }, timeout: 60_000 }).trim());
  } catch (error) {
    throw new Error(`${stage} Agent production caller failed: ${error?.message || error}`);
  }
}

function requestFor(seed, head, commands, label, source, merge = 'fields', patch = [], reads = null) {
  const request = { api_version: 1, project_id: seed.projectId, timeline_id: seed.timelineId,
    base_revision_id: head.revision_id, base_publication_id: head.publication_id, commands, label,
    steps: [{ id: `${label.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${randomUUID()}`,
      label, intent: label, tags: [], command_ordinals: commands.map((_, index) => index), patch }],
    merge, dry_run: false, source };
  if (reads !== null) request.reads = reads;
  return request;
}

async function post(harness, seed, request, label) {
  const text = JSON.stringify(request);
  const start = performance.now();
  const response = await harness.runtimeFetch(`/v1/projects/${seed.projectId}/timelines/${seed.timelineId}/commit`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': `p2-swap-native-${label}-${randomUUID()}` },
    body: text, signal: AbortSignal.timeout(120_000),
  });
  const body = await response.json().catch(() => null);
  return { status: response.status, elapsed_ms: Math.round(performance.now() - start),
    request_sha256: jsonDigest(request), request_bytes: Buffer.byteLength(text), response: safeBody(body),
    receipt_present: Boolean(body?.receipt), body: body && typeof body === 'object' ? body : null };
}

function stripPost(post) {
  const result = { ...post };
  delete result.body;
  return result;
}

async function runD112Positive() {
  const harness = await startDirectHarness({ deferTimelineInitialization: false });
  const result = { sequence: ['native seed', 'occurrence.add-media', 'occurrence.swap-media', 'timeline.inverse'] };
  try {
    const seed = { ...harness.seed, ...await harness.seedThreeProducts(15, 'native-none') };
    let current = await history(harness, seed);
    let document = await canonicalAt(harness, seed, current.head.revision_id);
    const image = await importFreshPin(harness, seed, harness.seed.image, 'd112-native-add.png');
    const replacement = await importFreshPin(harness, seed, harness.seed.image, 'd112-native-swap.png');
    const internal = document.internal_timeline_revisions[0].payload;
    const target = internal.clips.find((row) => row.id === 'f2-agent-clip');
    const owner = 'occurrence:f2-occurrence';
    const addRow = { id: `d112-native-add-${randomUUID()}`, clipType: 'image', track: 'V2', asset: image.selected.asset, at: 9, hold: 3 };
    const add = (() => {
      const { raw_parent_body: rawParentBody, ...canonicalDocument } = document;
      const input = JSON.stringify({ document: canonicalDocument, raw_parent_body: rawParentBody, media: image.selected, verified: image.verified, row: addRow });
      const source = ['import json,sys', 'from astrid.sdk.timeline.commit import bundle_from_document', 'from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_add_media', 'd=json.load(sys.stdin)', 'd.get("raw_parent_body") and d["document"]["parent_revision"].update(payload=json.loads(d["raw_parent_body"])["payload"])', 'b=bundle_from_document(d["document"])', 'c=capture_occurrence_add_media(b,"occurrence:f2-occurrence",d["row"],d["media"],verified_media=[d["verified"]])', 'print(json.dumps(c,separators=(",",":")))'].join(';');
      return JSON.parse(execFileSync(py, ['-c', source], { input, cwd: agent, encoding: 'utf8', env: { ...process.env, PYTHONPATH: agent, ASTRID_CHECKOUT: agent, PYTHONDONTWRITEBYTECODE: '1' } }).trim());
    })();
    const addPost = await post(harness, seed, requestFor(seed, current.head, [add], 'D112native ADD', { via: 'python' }, 'atomic'), 'd112-add');
    if (addPost.status !== 200) fail('D112 ADD refused', stripPost(addPost));
    current = await history(harness, seed); document = await canonicalAt(harness, seed, current.head.revision_id);
    const added = document.internal_timeline_revisions[0].payload.clips.find((item) => item.id === addRow.id);
    const swap = agentCommand(document, 'swap', replacement.selected, replacement.verified, { select: `${owner}/clip:${added.id}`, old_media: image.selected, old_verified: image.verified }, 'D112 positive swap');
    const swapPost = await post(harness, seed, requestFor(seed, current.head, [swap], 'D112native SWAP', { via: 'python' }, 'atomic'), 'd112-swap');
    if (swapPost.status !== 200) fail('D112 SWAP refused', stripPost(swapPost));
    current = await history(harness, seed);
    const undo = { schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [swapPost.body.receipt.receipt_id] } };
    const undoPost = await post(harness, seed, requestFor(seed, current.head, [undo], 'D112native nativeUndo', { via: 'python' }, 'atomic'), 'd112-undo');
    if (undoPost.status !== 200) fail('D112 Undo refused', stripPost(undoPost));
    result.initial_history_items = current.items?.length ?? null;
    result.add = stripPost(addPost); result.swap = stripPost(swapPost); result.undo = stripPost(undoPost);
    return result;
  } finally { await harness.stop().catch(() => {}); }
}

async function runAppReplay() {
  const harness = await startDirectHarness({ deferTimelineInitialization: false });
  const result = { sequence: ['native seed', 'old-media reimport', 'shared placement', 'authored old-media patch', 'occurrence.fork', 'occurrence.swap-media'] };
  let managed;
  try {
    const seed = { ...harness.seed, ...await harness.seedThreeProducts(15, 'native-none') };
    let current = await history(harness, seed);
    let document = await canonicalAt(harness, seed, current.head.revision_id);
    const sourceOccurrence = document.parent_revision.payload.occurrences.find((row) => row.occurrence_id === 'f2-occurrence');
    const sourceShot = document.shot_revisions.find((row) => row.revision_id === sourceOccurrence.shot_revision_id);
    const internal = document.internal_timeline_revisions.find((row) => row.revision_id === sourceShot.internal_timeline_revision_id);
    const target = internal.payload.clips.find((row) => row.id === 'f2-agent-clip');
    const oldMedia = await importFreshPin(harness, seed, harness.seed.image, 'p2-popup-old.png');
    const sharedOccurrenceId = 'f2-occurrence-copy';
    const placement = { schema_version: 1, op: 'occurrence.place-shared', version: '1', select: 'occurrence:f2-occurrence', args: { occurrence_id: sharedOccurrenceId, on: 12 }, intent: { ownership: 'occurrence' }, created: [`occurrence:${sharedOccurrenceId}`] };
    const placed = await post(harness, seed, requestFor(seed, current.head, [placement], 'P2 popup shared placement', { via: 'python' }, 'atomic'), 'app-place');
    if (placed.status !== 200) fail('App setup placement refused', stripPost(placed));
    current = await history(harness, seed); document = await canonicalAt(harness, seed, current.head.revision_id);
    const latestInternal = document.internal_timeline_revisions.find((row) => row.revision_id === internal.revision_id);
    const opaque = { keep: [null, false, 0, { source: 'fixture' }] };
    const changes = [
      { op: 'set', ref: 'parent', path: ['p2_popup_opaque'], before: { state: 'absent' }, value: opaque },
      { op: 'set', ref: `internal-revision:${latestInternal.revision_id}`, path: ['clips', 'id:f2-agent-clip', 'asset'], before: { state: 'present', value: target.asset }, value: oldMedia.selected.asset },
      { op: 'set', ref: `internal-revision:${latestInternal.revision_id}`, path: ['registry', 'assets', oldMedia.selected.asset], before: { state: 'absent' }, value: oldMedia.entry },
    ];
    const authored = { schema_version: 1, op: 'doc.patch', version: '1', select: null, created: [`occurrence:f2-occurrence/asset:${oldMedia.selected.asset}`, `occurrence:${sharedOccurrenceId}/asset:${oldMedia.selected.asset}`], args: { changes } };
    const setup = await post(harness, seed, requestFor(seed, current.head, [authored], 'P2 popup authored media', { via: 'python' }, 'atomic', changes), 'app-authored');
    if (setup.status !== 200) fail('App setup authored patch refused', stripPost(setup));
    current = await history(harness, seed); document = await canonicalAt(harness, seed, current.head.revision_id);
    const replacement = await importBytes(harness, seed, makePng(65, 49), 'p2-popup-new.png');
    const forkId = `shot-fork-${randomUUID()}`;
    const fork = agentCommand(document, 'fork', null, null, { owner: `occurrence:${sharedOccurrenceId}`, shot_id: forkId }, 'App replay fork');
    const swap = agentCommand(document, 'swap', replacement.selected, replacement.verified, { select: `occurrence:${sharedOccurrenceId}/clip:f2-agent-clip`, old_media: oldMedia.selected, old_verified: oldMedia.verified }, 'App replay swap');
    const swapRequest = requestFor(seed, current.head, [fork, swap], 'Edit timeline', { via: 'app' }, 'fields', [], []);
    const swapPost = await post(harness, seed, swapRequest, 'app-swap');
    const swapResult = stripPost(swapPost);
    result.placement = stripPost(placed); result.authored = stripPost(setup); result.fork = { generated: true, op: fork.op, select: fork.select, shot_id: fork.args.shot_id };
    result.swap = { ...swapResult, reason: swapResult.response.reason };
    result.request = { status: swapPost.status, request_sha256: swapPost.request_sha256, request_bytes: swapPost.request_bytes, command_ops: swapRequest.commands.map((command) => command.op), source: swapRequest.source, merge: swapRequest.merge, reads: swapRequest.reads };
    result.input_manifest = { initial_history_items: current.items?.length ?? null, head_revision_id: current.head.revision_id, head_publication_id: current.head.publication_id, shared_occurrence_id: sharedOccurrenceId, source_occurrence_id: 'f2-occurrence', target_clip_id: 'f2-agent-clip', old_media_object_id: oldMedia.selected.object_id, new_media_object_id: replacement.selected.object_id };
    return result;
  } finally {
    managed = harness.runtime;
    await harness.stop().catch(() => {});
    const stderr = managed?.stderr || '';
    result.stderr_bytes = Buffer.byteLength(stderr);
    result.stderr_sha256 = digest(stderr);
    const lines = stderr.split('\n').filter(Boolean).map((line) => { try { return JSON.parse(line); } catch { return null; } }).filter(Boolean);
    result.stderr_diagnostics = lines.filter((line) => line.event === 'timeline_commit_error').map((line) => ({ reason: line.reason, request_id: line.request_id, exception_class_chain_length: Array.isArray(line.exception_class_chain) ? line.exception_class_chain.length : 0 }));
    result.swap = result.swap || { status: null, reason: null };
    result.swap.diagnostic_reason = result.stderr_diagnostics.at(-1)?.reason || null;
  }
}

async function main() {
  mkdirSync(evidence, { recursive: true, mode: 0o700 });
  const sourceIdentity = JSON.parse(process.env.P2_SWAP_SOURCE_IDENTITY);
  const result = { task: 'rt-P2-SWAP-replay-return-1055', preflight: 'PASS', source_identity: sourceIdentity };
  try {
    result.d112_positive = await runD112Positive();
    result.app_replay = await runAppReplay();
    result.comparison = { difference: `D112 positive uses direct add -> swap -> nativeUndo on the registered seeded occurrence and accepts both media commands. The recorded App sequence first creates the shared occurrence, authors the old media into the child, then sends fork + swap as one ordinary App request; fork accepts, while the fresh native reconstruction returns ${result.app_replay.swap.reason} before a receipt. The retained App packet reported history_unavailable; this fresh fixture therefore does not claim the same lower predicate. No classifier/safety denial is involved.`, actual_app_source: '96d4754b4eef0591a208d6b51b60c30fc44b6915', recorded_runtime: 'd23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e', recorded_app_reason: 'history_unavailable', observed_replay_reason: result.app_replay.swap.reason };
  } catch (error) {
    result.error = { class: error?.constructor?.name || 'Error', message: String(error?.message || error).slice(0, 1000) };
  }
  writeFileSync(`${evidence}/result-p2-swap-native.json`, `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 });
  console.log(JSON.stringify({ task: result.task, preflight: result.preflight, d112_swap: result.d112_positive?.swap?.status, app_fork: result.app_replay?.fork?.status, app_swap: result.app_replay?.swap?.status, app_reason: result.app_replay?.swap?.reason, error: result.error?.message || null }));
  if (result.error) process.exitCode = 1;
}
await main();
