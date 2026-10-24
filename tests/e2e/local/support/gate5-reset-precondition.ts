type JsonObject = Record<string, unknown>;

export interface Gate5ResetPreconditionInput {
  request: unknown;
  responseStatus: number | undefined;
  responseBody: unknown;
  expectedBase: { revisionId: string; publicationId: string };
  clipId: string;
  expectedPosition: number;
  settledOutboxes: readonly unknown[];
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
  if (input.responseStatus !== 200) throw new Error(`Gate5 precondition response status ${String(input.responseStatus)}`);

  const request = object(input.request, 'request');
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
  if (!/^(accepted|rebased|merged)$/.test(string(data.status, 'response status'))) throw new Error('Gate5 precondition was not accepted');
  const acceptedRevisionId = string(data.accepted_revision_id, 'accepted revision');
  const receipt = object(envelope.receipt, 'receipt');
  string(receipt.receipt_id, 'receipt id');
  if (!sameJson(receipt.result, data)) throw new Error('Gate5 precondition receipt does not match response data');

  const document = object(data.canonical_document, 'canonical document');
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

  for (const candidate of input.settledOutboxes) {
    const outbox = object(candidate, 'outbox');
    if (outbox.pending) throw new Error('Gate5 precondition owner is still pending');
    const intents = outbox.intents;
    if (!Array.isArray(intents) || intents.length !== 0) throw new Error('Gate5 precondition owner is not settled');
  }
  if (!input.settledOutboxes.length) throw new Error('Gate5 precondition owner is missing');
}
