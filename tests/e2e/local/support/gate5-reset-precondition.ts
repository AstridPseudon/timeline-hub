type JsonObject = Record<string, unknown>;

export interface Gate5ResetPreconditionInput {
  request: unknown;
  requestIdentity: unknown;
  responseRequest: unknown;
  requestIdempotencyKey: unknown;
  responseStatus: number | undefined;
  responseBody: unknown;
  expectedBase: { revisionId: string; publicationId: string };
  expectedScope: { projectId: string; timelineId: string };
  expectedOwnerId: string;
  preGestureDocument: unknown;
  clipId: string;
  expectedTrackId: string;
  expectedPreviousPosition: number;
  expectedPosition: number;
  settledOutboxes: readonly unknown[];
  authoritativeHead: unknown;
  authoritativeRevision: unknown;
}

function object(value: unknown, label: string): JsonObject {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`Gate5 precondition ${label} is missing`);
  return value as JsonObject;
}

function isRecord(value: unknown): value is JsonObject {
  return !!value && typeof value === 'object' && !Array.isArray(value);
}

function string(value: unknown, label: string): string {
  if (typeof value !== 'string' || !value) throw new Error(`Gate5 precondition ${label} is missing`);
  return value;
}

function number(value: unknown, label: string): number {
  if (typeof value !== 'number' || !Number.isFinite(value)) throw new Error(`Gate5 precondition ${label} is missing`);
  return value;
}

function sameJson(left: unknown, right: unknown): boolean {
  return JSON.stringify(left) === JSON.stringify(right);
}

/**
 * Reconstruct the move planner's ordered reads from the immutable pre-gesture
 * parent. The submitted request is deliberately not an input to this oracle.
 */
export function expectedGate5MoveReads(input: {
  preGestureDocument: unknown;
  clipId: string;
  expectedTrackId: string;
}): unknown[] {
  const document = object(input.preGestureDocument, 'pre-gesture document');
  const parentRevision = object(document.parent_revision, 'pre-gesture parent revision');
  const payload = object(parentRevision.payload, 'pre-gesture parent payload');
  const config = object(payload.config, 'pre-gesture config');
  const topLevelClips = !Object.prototype.hasOwnProperty.call(config, 'clips') && Array.isArray(payload.clips);
  const clipPath = topLevelClips ? ['clips'] : ['config', 'clips'];
  const clips = topLevelClips ? payload.clips : config.clips;
  if (!Array.isArray(clips)) throw new Error('Gate5 precondition pre-gesture clips are missing');
  const selected = clips.filter((candidate): candidate is JsonObject => isRecord(candidate) && candidate.id === input.clipId);
  if (selected.length !== 1) throw new Error('Gate5 precondition pre-gesture clip is ambiguous');
  const selectedClip = selected[0];
  const reads: unknown[] = [];
  const read = (value: JsonObject, key: string, path: string[]) => reads.push({
    kind: 'field', ref: 'parent', path: [...path, key],
    state: Object.prototype.hasOwnProperty.call(value, key)
      ? { state: 'present', value: structuredClone(value[key]) } : { state: 'absent' },
  });
  const readPath = (value: JsonObject, keys: string[], path: string[]) => {
    const [key, ...rest] = keys;
    if (rest.length && isRecord(value[key])) return readPath(value[key], rest, [...path, key]);
    read(value, key, path);
  };
  const timingReads = (item: JsonObject) => {
    for (const key of ['id', 'track', 'at', 'clipType', 'hold', 'from', 'to', 'speed', 'asset']) {
      read(item, key, [...clipPath, `id:${String(item.id)}`]);
    }
  };
  const registry = object(payload.registry, 'pre-gesture registry');
  const assetRead = (item: JsonObject) => {
    if (typeof item.asset !== 'string') return;
    readPath(registry, ['assets', item.asset], ['config', 'registry']);
  };

  timingReads(selectedClip);
  readPath(config, ['output', 'fps'], ['config']);
  if (!isRecord(config.output) || config.output.fps == null) {
    read(config, 'theme', ['config']);
    readPath(config, ['theme_overrides', 'visual', 'canvas', 'fps'], ['config']);
  }
  assetRead(selectedClip);
  const tracks = config.tracks;
  if (!Array.isArray(tracks)) throw new Error('Gate5 precondition pre-gesture tracks are missing');
  const track = tracks.filter((candidate): candidate is JsonObject => isRecord(candidate) && candidate.id === input.expectedTrackId);
  if (track.length !== 1) throw new Error('Gate5 precondition pre-gesture track is ambiguous');
  if (selectedClip.track !== input.expectedTrackId) throw new Error('Gate5 precondition pre-gesture track mismatch');
  read(track[0], 'kind', ['config', 'tracks', `id:${input.expectedTrackId}`]);
  read(config, 'pinnedShotGroups', ['config']);
  const order = clips.map((candidate) => isRecord(candidate) ? candidate.id : undefined);
  if (order.some((id) => typeof id !== 'string')) throw new Error('Gate5 precondition pre-gesture clip identity is missing');
  reads.push({ kind: 'collection', ref: 'parent', path: clipPath, members: [...order].sort(), order });
  for (const candidate of clips) {
    if (!isRecord(candidate)) throw new Error('Gate5 precondition pre-gesture clip is malformed');
    const item = candidate;
    if (item.id === input.clipId) continue;
    read(item, 'track', [...clipPath, `id:${String(item.id)}`]);
    if (item.track === input.expectedTrackId) {
      timingReads(item);
      assetRead(item);
    }
  }
  return reads;
}

/**
 * Validate the real mounted 0→5 commit before Gate5 issues its original 5→0 reset.
 * This is deliberately transport- and product-agnostic so the offline control can exercise every fail-closed edge.
 */
export function assertGate5ResetPrecondition(input: Gate5ResetPreconditionInput): void {
  if (input.responseRequest !== input.requestIdentity) throw new Error('Gate5 precondition response is not for the setup request');
  if (input.responseStatus !== 200) throw new Error(`Gate5 precondition response status ${String(input.responseStatus)}`);

  const request = object(input.request, 'request');
  if (request.api_version !== 1) throw new Error('Gate5 precondition request version mismatch');
  if (request.project_id !== input.expectedScope.projectId) throw new Error('Gate5 precondition project scope mismatch');
  if (request.timeline_id !== input.expectedScope.timelineId) throw new Error('Gate5 precondition timeline scope mismatch');
  if (request.base_revision_id !== input.expectedBase.revisionId) throw new Error('Gate5 precondition base revision mismatch');
  if (request.base_publication_id !== input.expectedBase.publicationId) throw new Error('Gate5 precondition base publication mismatch');
  if (request.label !== 'Edit timeline') throw new Error('Gate5 precondition label mismatch');
  if (request.merge !== 'fields') throw new Error('Gate5 precondition merge mismatch');
  if (request.dry_run !== false) throw new Error('Gate5 precondition dry-run mismatch');
  if (!sameJson(request.source, { via: 'app' })) throw new Error('Gate5 precondition source mismatch');
  const expectedReads = expectedGate5MoveReads({
    preGestureDocument: input.preGestureDocument, clipId: input.clipId, expectedTrackId: input.expectedTrackId,
  });
  if (!sameJson(request.reads, expectedReads)) throw new Error('Gate5 precondition move read dependencies mismatch');
  const commands = request.commands;
  if (!Array.isArray(commands) || commands.length !== 1) throw new Error('Gate5 precondition command is missing');
  const command = object(commands[0], 'command');
  if (command.schema_version !== 1 || command.op !== 'doc.patch' || command.version !== '1' || command.select !== null) {
    throw new Error('Gate5 precondition is not the mounted document patch');
  }
  if (!Array.isArray(command.created) || command.created.length !== 0) throw new Error('Gate5 precondition created claims mismatch');
  const args = object(command.args, 'command arguments');
  const changes = args.changes;
  if (!Array.isArray(changes) || changes.length !== 1) throw new Error('Gate5 precondition patch is missing');
  const change = object(changes[0], 'change');
  if (change.op !== 'set' || change.ref !== 'parent'
    || !sameJson(change.path, ['clips', `id:${input.clipId}`, 'at'])) throw new Error('Gate5 precondition clip mismatch');
  if (!sameJson(change.before, { state: 'present', value: input.expectedPreviousPosition })) {
    throw new Error('Gate5 precondition previous position mismatch');
  }
  if (change.value !== input.expectedPosition) throw new Error('Gate5 precondition requested position mismatch');
  const steps = request.steps;
  if (!Array.isArray(steps) || steps.length !== 1) throw new Error('Gate5 precondition step is missing');
  const step = object(steps[0], 'step');
  if (typeof step.id !== 'string' || !step.id || step.label !== 'Edit timeline'
    || step.intent !== `Move ${input.clipId} on ${input.expectedTrackId}` || !sameJson(step.tags, [])
    || !sameJson(step.command_ordinals, [0]) || !sameJson(step.patch, changes)
    || !sameJson(step.reads, request.reads)) throw new Error('Gate5 precondition step claims mismatch');

  const envelope = object(input.responseBody, 'response');
  const data = object(envelope.data, 'response data');
  if (string(data.status, 'response status') !== 'accepted') throw new Error('Gate5 precondition was not accepted');
  if (data.base_revision_id !== request.base_revision_id || data.base_publication_id !== request.base_publication_id) {
    throw new Error('Gate5 precondition response base mismatch');
  }
  if (data.previous_revision_id !== input.expectedBase.revisionId || data.previous_publication_id !== input.expectedBase.publicationId) {
    throw new Error('Gate5 precondition response previous head mismatch');
  }
  if (data.rebased_onto !== null) throw new Error('Gate5 precondition response rebase mismatch');
  const acceptedRevisionId = string(data.accepted_revision_id, 'accepted revision');
  const responseCommands = data.commands;
  if (!Array.isArray(responseCommands) || responseCommands.length !== 1) throw new Error('Gate5 precondition response command mismatch');
  const responseCommand = object(responseCommands[0], 'response command');
  for (const key of ['schema_version', 'op', 'version', 'select', 'args', 'created']) {
    if (!sameJson(responseCommand[key], command[key])) throw new Error('Gate5 precondition response command mismatch');
  }
  for (const key of ['intent', 'resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created']) {
    if (!Object.prototype.hasOwnProperty.call(responseCommand, key)) throw new Error(`Gate5 precondition response ${key} claim is missing`);
  }
  if (typeof data.document_digest !== 'string' || !data.document_digest
    || !object(data.id_map, 'id map') || typeof data.provider_version !== 'string' || typeof data.compiler_version !== 'string'
    || string(data.publisher, 'publisher') === '' || data.merge_mode !== 'fields'
    || data.label !== request.label || !sameJson(data.source, request.source)) {
    throw new Error('Gate5 precondition response metadata mismatch');
  }
  const responseSteps = data.steps;
  if (!Array.isArray(responseSteps) || responseSteps.length !== 1) throw new Error('Gate5 precondition response steps missing');
  const responseStep = object(responseSteps[0], 'response step');
  for (const key of ['id', 'label', 'intent', 'tags', 'command_ordinals', 'patch', 'dependencies']) {
    if (!Object.prototype.hasOwnProperty.call(responseStep, key)) throw new Error(`Gate5 precondition response ${key} is missing`);
  }
  const receipt = object(envelope.receipt, 'receipt');
  string(receipt.receipt_id, 'receipt id');
  if (string(input.requestIdempotencyKey, 'request idempotency key') !== receipt.idempotency_key) {
    throw new Error('Gate5 precondition receipt idempotency mismatch');
  }
  if (receipt.command_kind !== 'timeline.commit') throw new Error('Gate5 precondition receipt command mismatch');
  if (receipt.project_id !== input.expectedScope.projectId) throw new Error('Gate5 precondition receipt project mismatch');
  if (!sameJson(receipt.result, data)) throw new Error('Gate5 precondition receipt does not match response data');

  const document = object(data.canonical_document, 'canonical document');
  if (document.project_id !== input.expectedScope.projectId || document.timeline_id !== input.expectedScope.timelineId) {
    throw new Error('Gate5 precondition canonical scope mismatch');
  }
  const parentRevision = object(document.parent_revision, 'parent revision');
  if (parentRevision.revision_id !== acceptedRevisionId) throw new Error('Gate5 precondition canonical revision mismatch');
  const payload = object(parentRevision.payload, 'parent payload');
  const clips = payload.clips ?? object(payload.config, 'canonical config').clips;
  if (!Array.isArray(clips)) throw new Error('Gate5 precondition canonical clips are missing');
  const clip = clips.find((candidate) => candidate && typeof candidate === 'object' && !Array.isArray(candidate)
    && (candidate as JsonObject).id === input.clipId);
  if (!clip) throw new Error('Gate5 precondition canonical clip is missing');
  if (number((clip as JsonObject).at, 'canonical position') !== input.expectedPosition) {
    throw new Error('Gate5 precondition canonical position mismatch');
  }

  const authoritativeHead = object(input.authoritativeHead, 'authoritative head');
  if (authoritativeHead.revision_id !== acceptedRevisionId || authoritativeHead.publication_id !== receipt.receipt_id) {
    throw new Error('Gate5 precondition authoritative head mismatch');
  }
  const authoritativeRevision = object(input.authoritativeRevision, 'authoritative revision');
  if (authoritativeRevision.project_id !== input.expectedScope.projectId
    || authoritativeRevision.timeline_id !== input.expectedScope.timelineId
    || authoritativeRevision.revision_id !== acceptedRevisionId) {
    throw new Error('Gate5 precondition authoritative revision scope mismatch');
  }
  const authoritativePayload = object(authoritativeRevision.payload, 'authoritative payload');
  const authoritativeClips = authoritativePayload.clips ?? object(authoritativePayload.config, 'authoritative config').clips;
  if (!Array.isArray(authoritativeClips)) throw new Error('Gate5 precondition authoritative clips are missing');
  const authoritativeClip = authoritativeClips.find((candidate) => candidate && typeof candidate === 'object' && !Array.isArray(candidate)
    && (candidate as JsonObject).id === input.clipId);
  if (!authoritativeClip) throw new Error('Gate5 precondition authoritative clip is missing');
  if (number((authoritativeClip as JsonObject).at, 'authoritative position') !== input.expectedPosition) {
    throw new Error('Gate5 precondition authoritative position mismatch');
  }

  if (input.settledOutboxes.length !== 1) throw new Error('Gate5 precondition owner is missing or ambiguous');
  const outbox = object(input.settledOutboxes[0], 'outbox');
  const scope = object(outbox.scope, 'outbox scope');
  if (scope.projectId !== input.expectedScope.projectId || scope.timelineId !== input.expectedScope.timelineId) {
    throw new Error('Gate5 precondition owner scope mismatch');
  }
  if (outbox.ownerId !== input.expectedOwnerId) throw new Error('Gate5 precondition owner identity mismatch');
  if (outbox.pending) throw new Error('Gate5 precondition owner is still pending');
  const intents = outbox.intents;
  if (!Array.isArray(intents) || intents.length !== 0) throw new Error('Gate5 precondition owner is not settled');
  const accepted = object(outbox.accepted, 'accepted owner result');
  const acceptedHead = object(accepted.head, 'accepted owner head');
  if (acceptedHead.revisionId !== acceptedRevisionId || acceptedHead.publicationId !== receipt.receipt_id) {
    throw new Error('Gate5 precondition owner head mismatch');
  }
  const acceptedValue = object(accepted.value, 'accepted owner value');
  const acceptedIdentity = object(acceptedValue.accepted, 'accepted owner identity');
  if (acceptedIdentity.revisionId !== acceptedRevisionId || acceptedIdentity.publicationId !== receipt.receipt_id) {
    throw new Error('Gate5 precondition owner accepted identity mismatch');
  }
  const acceptedReceipt = object(acceptedValue.receipt, 'accepted owner receipt');
  if (!sameJson(acceptedValue.response, input.responseBody)
    || !sameJson(acceptedValue.canonicalDocument, document)
    || !sameJson(acceptedReceipt, receipt)
    || acceptedReceipt.idempotency_key !== input.requestIdempotencyKey) {
    throw new Error('Gate5 precondition owner receipt or canonical result mismatch');
  }
}
