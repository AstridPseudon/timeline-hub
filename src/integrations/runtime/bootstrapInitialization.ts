import type { WorkspaceClient } from './generated.ts';
import { ApiError } from './generated.ts';
import { classifyRuntimeCommitFailure } from './client.ts';
import type { CommitRequest, JSON } from './timeline-commit-types.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '@/tools/video-editor/data/DataProvider.ts';
import { DEFAULT_OUTPUT, DEFAULT_VIDEO_TRACKS } from '@/tools/video-editor/lib/defaults.ts';
import { authoringBundleFromDocument } from '@/tools/video-editor/commands/authoringBundle.ts';
import { captureBootstrap } from '@/tools/video-editor/commands/bootstrapCapture.ts';
import { copy, equal, object } from '@/tools/video-editor/commands/clipMovePrimitives.ts';
import type { ClaimedOutbox, OutboxHead, OutboxOutcome, OutboxRecord } from '@/tools/video-editor/commands/commitOutbox.ts';

type Defaults = { name: string; slug: string; output: JSON; tracks: JSON };
type InitPayload = { kind: 'timeline-init'; commands: CommitRequest['commands'] };
type Ports = {
  createTimeline: WorkspaceClient['createTimeline'];
  loadLatest(timelineId: string): Promise<TimelineCommandBasis>;
  commitTimeline(request: CommitRequest, key: string): Promise<TimelineCommitResult>;
};
const json = (value: unknown): JSON => JSON.parse(JSON.stringify(value)) as JSON;
const sameHead = (a: OutboxHead, b: OutboxHead) => a.revisionId === b.revisionId && a.publicationId === b.publicationId;
const requireValue = (condition: unknown, message: string): void => { if (!condition) throw new Error(message); };

/** Source-only seam: caller holds the existing owner claim, including explicit crash recovery. */
export async function reserveBootstrapInitialization(box: ClaimedOutbox, name: string, key: string, createName: string | null = name) {
  requireValue(typeof name === 'string' && name === name.trim() && name.length > 0 && name.length <= 120,
    'Initialization requires a supported nonempty name');
  requireValue(createName === null || (typeof createName === 'string' && createName === createName.trim()
    && createName.length > 0 && createName.length <= 120), 'Create requires a supported name or an omitted name');
  const { scope } = await box.read();
  const defaults: Defaults = { name, slug: name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'timeline',
    output: copy(DEFAULT_OUTPUT), tracks: json(DEFAULT_VIDEO_TRACKS) };
  await box.reserveCreate(json(defaults), { method: 'POST', path: `/v1/projects/${encodeURIComponent(scope.projectId)}/timelines`,
    body: JSON.stringify({ timeline_id: scope.timelineId, ...(createName === null ? {} : { name: createName }) }), key });
}

function ready(record: OutboxRecord) {
  if (record.pending || record.intents.length) {
    const failure = record.pending?.outcome;
    throw new Error(failure && failure.kind !== 'accepted'
      ? String((failure.error as { message?: string })?.message ?? 'Initialization is not acknowledged; retain and retry the original request')
      : 'Initialization is not acknowledged; retain and retry the original request');
  }
}

/** No production caller until the paired registry/Runtime release and central browser proof. */
export async function resumeBootstrapInitialization(box: ClaimedOutbox, ports: Ports): Promise<TimelineCommandBasis> {
  let record = await box.read();
  const { scope } = record;
  const failure = (error: unknown): OutboxOutcome => {
    const kind = error instanceof ApiError && error.status >= 500 ? 'unknown' : classifyRuntimeCommitFailure(error);
    return { kind: kind === 'unknown' || kind === 'storage' ? 'retry' : 'rejected',
      error: { message: error instanceof Error ? error.message : String(error) } };
  };
  if (record.intents[0] && 'create' in record.intents[0].basis) {
    record = await box.dispatch(() => { throw new Error('Creation must already be reserved'); }, async (request) => {
      try {
        const body = JSON.parse(request.body) as { timeline_id: string; name?: string };
        requireValue(request.body === JSON.stringify({ timeline_id: scope.timelineId,
          ...(body.name === undefined ? {} : { name: body.name }) }), 'Create request differs from the generated request; draft retained');
        const result = await ports.createTimeline(scope.projectId, body.timeline_id, request.key, body.name);
        const receiptResult = result.receipt.result;
        requireValue(result.project_id === scope.projectId && result.timeline_id === scope.timelineId
          && result.archived === false && typeof result.head_revision_id === 'string' && !!result.head_revision_id
          && typeof result.head_publication_id === 'string' && !!result.head_publication_id
          && result.receipt.command_kind === 'timeline.create' && result.receipt.idempotency_key === request.key
          && result.receipt.project_id === scope.projectId && !!result.receipt.receipt_id
          && object(receiptResult) && receiptResult.project_id === scope.projectId && receiptResult.timeline_id === scope.timelineId
          && receiptResult.head_revision_id === result.head_revision_id && receiptResult.head_publication_id === result.head_publication_id,
        'Create did not return a tracked timeline and matching receipt; draft retained');
        return { kind: 'accepted', head: { revisionId: result.head_revision_id as string, publicationId: result.head_publication_id as string },
          // Generated create's receipt is non-enumerable. Persist it explicitly.
          value: json({ data: { ...result }, receipt: result.receipt }) };
      } catch (error) { return failure(error); }
    });
    ready(record);
  }
  if (!record.intents.length && record.accepted?.creation) {
    const created = record.accepted;
    const basis = await ports.loadLatest(scope.timelineId);
    const history = basis.history;
    const entry = history?.items[0];
    const document = basis.canonicalDocument;
    const receiptResult = entry?.receipt.result;
    requireValue(sameHead(basis.head, created.head) && history?.head.revision_id === created.head.revisionId
      && history.head.publication_id === created.head.publicationId && history.next_cursor === null && history.items.length === 1
      && entry?.intent === 'bootstrap' && entry.previous === null && entry.revision_id === created.head.revisionId
      && entry.publication_id === created.head.publicationId && entry.receipt.receipt_id === created.head.publicationId
      && entry.receipt.command_kind === 'parent_composition.publish' && entry.receipt.project_id === scope.projectId
      && object(receiptResult) && receiptResult.project_id === scope.projectId && receiptResult.timeline_id === scope.timelineId
      && receiptResult.revision_id === created.head.revisionId && receiptResult.content_digest === document.parent_revision.content_digest
      && receiptResult.old_head === null && receiptResult.new_head === created.head.revisionId
      && equal(receiptResult.payload, document.parent_revision.payload)
      && document.project_id === scope.projectId && document.timeline_id === scope.timelineId
      && document.parent_revision.revision_id === created.head.revisionId
      && equal(document.dependency_manifest, { shots: [], internal_timelines: [], media: [], documents: [] })
      && equal(document.shot_revisions, []) && equal(document.internal_timeline_revisions, []),
    'Initialization requires the original sole bootstrap publication; draft retained');
    const captured = captureBootstrap(await authoringBundleFromDocument(document), created.creation!.payload as Defaults);
    await box.append(json({ kind: 'timeline-init', commands: captured.commands }), { after: created.intentId });
    record = await box.read();
  }
  if (record.intents.length) {
    requireValue((record.intents[0].payload as InitPayload).kind === 'timeline-init' && record.intents.length === 1,
      'Outbox does not contain this initialization');
    record = await box.dispatch((intent, head) => ({ method: 'POST',
      path: `/v1/projects/${encodeURIComponent(scope.projectId)}/timelines/${encodeURIComponent(scope.timelineId)}/commit`,
      body: json({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
        base_revision_id: head.revisionId, base_publication_id: head.publicationId,
        commands: (intent.payload as InitPayload).commands, source: { via: 'app' } } satisfies CommitRequest),
    }), async (request) => {
      try {
        const body = JSON.parse(request.body) as CommitRequest;
        const result = await ports.commitTimeline(body, request.key);
        const response = result.response;
        requireValue(response.receipt.command_kind === 'timeline.commit' && response.receipt.idempotency_key === request.key
          && response.receipt.project_id === scope.projectId && response.receipt.receipt_id === result.accepted.publicationId
          && response.data.base_revision_id === body.base_revision_id && response.data.base_publication_id === body.base_publication_id
          && equal(response.data.commands, body.commands), 'Initialization commit receipt does not match its original request');
        return { kind: 'accepted', head: result.accepted, value: json({ kind: 'timeline-initialized', result }) };
      } catch (error) { return failure(error); }
    });
  }
  ready(record);
  requireValue((record.accepted?.value as { kind?: string })?.kind === 'timeline-initialized', 'No acknowledged initialization in this owner');
  // A late ACK is historical. Display today's verified basis, never reinstall defaults.
  return ports.loadLatest(scope.timelineId);
}
