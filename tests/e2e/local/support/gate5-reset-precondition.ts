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
  clipId: string;
  expectedPosition: number;
  settledOutboxes: readonly unknown[];
  authoritativeHead: unknown;
  authoritativeRevision: unknown;
}

function object(value: unknown, label: string): JsonObject {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`Gate5 precondition ${label} is missing`);
  return value as JsonObject;
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
  const commands = request.commands;
  if (!Array.isArray(commands) || commands.length !== 1) throw new Error('Gate5 precondition command is missing');
  const command = object(commands[0], 'command');
  if (command.op !== 'clip.move') throw new Error('Gate5 precondition is not a clip move');
  if (command.select !== `parent/clip:${input.clipId}`) throw new Error('Gate5 precondition clip mismatch');
  const args = object(command.args, 'command arguments');
  if (args.on !== input.expectedPosition) throw new Error('Gate5 precondition requested position mismatch');

  const envelope = object(input.responseBody, 'response');
  const data = object(envelope.data, 'response data');
  if (string(data.status, 'response status') !== 'accepted') throw new Error('Gate5 precondition was not accepted');
  if (data.base_revision_id !== request.base_revision_id || data.base_publication_id !== request.base_publication_id) {
    throw new Error('Gate5 precondition response base mismatch');
  }
  if (data.previous_revision_id !== input.expectedBase.revisionId || data.previous_publication_id !== input.expectedBase.publicationId) {
    throw new Error('Gate5 precondition response previous head mismatch');
  }
  const acceptedRevisionId = string(data.accepted_revision_id, 'accepted revision');
  if (!sameJson(data.commands, request.commands)) throw new Error('Gate5 precondition response command mismatch');
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
  const clips = payload.clips;
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
  const authoritativeClips = authoritativePayload.clips;
  if (!Array.isArray(authoritativeClips)) throw new Error('Gate5 precondition authoritative clips are missing');
  const authoritativeClip = authoritativeClips.find((candidate) => candidate && typeof candidate === 'object' && !Array.isArray(candidate)
    && (candidate as JsonObject).id === input.clipId);
  if (!authoritativeClip) throw new Error('Gate5 precondition authoritative clip is missing');
  if (number((authoritativeClip as JsonObject).at, 'authoritative position') !== input.expectedPosition) {
    throw new Error('Gate5 precondition authoritative position mismatch');
  }

  for (const candidate of input.settledOutboxes) {
    const outbox = object(candidate, 'outbox');
    if (outbox.pending) throw new Error('Gate5 precondition owner is still pending');
    const intents = outbox.intents;
    if (!Array.isArray(intents) || intents.length !== 0) throw new Error('Gate5 precondition owner is not settled');
  }
  if (!input.settledOutboxes.length) throw new Error('Gate5 precondition owner is missing');
}
