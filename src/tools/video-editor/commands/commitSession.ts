import { captureOccurrenceAddMedia } from './occurrenceMediaCapture.ts';
import { equal, freezeJson } from './clipMovePrimitives.ts';
import type { CommitRequest, EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { ApiError } from '@/integrations/runtime/generated.ts';
import { classifyRuntimeCommitFailure } from '@/integrations/runtime/client.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { captureClipMove, finishClipMove, type AuthoredBundle } from './clipMoveCapture.ts';
import type { ClipMoveCapturePort, ClipMoveProposal } from './semanticGestures.ts';
import { createCommitOutbox, type ClaimedOutbox, type OutboxBasis, type OutboxHead, type OutboxRecord, type OutboxScope } from './commitOutbox.ts';

type Payload = { commands: EditCommand[]; before: AuthoredBundle; after: AuthoredBundle; preview: TimelinePatch | null; displayBasis?: TimelineCommandBasis };
export type CommandSessionState = {
  status: 'loading' | 'saved' | 'dirty' | 'saving' | 'retry' | 'conflict' | 'error' | 'recovery';
  error: string | null;
  ownerId: string | null;
  recoverableOwners: string[];
  canUndo: boolean;
};
type Options = {
  scope: OutboxScope;
  initial: TimelineCommandBasis;
  outboxes?: ReturnType<typeof createCommitOutbox>;
  send(request: CommitRequest, key: string): Promise<TimelineCommitResult>;
  preview(patch: TimelinePatch): void;
  project(basis: TimelineCommandBasis, previews: TimelinePatch[]): Promise<void>;
  changed(state: CommandSessionState): void;
};
const sameHead = (a: OutboxHead, b: OutboxHead) => a.revisionId === b.revisionId && a.publicationId === b.publicationId;
const message = (error: unknown) => error instanceof Error ? error.message : String(error);
const json = (value: unknown): JSON => JSON.parse(JSON.stringify(value)) as JSON;

/** One browser-lock lifetime, one durable prefix, original guarded suffixes. */
export async function createTimelineCommandSession(options: Options) {
  const storage = options.outboxes ?? createCommitOutbox();
  let bundle = await authoringBundleFromDocument(options.initial.canonicalDocument) as AuthoredBundle;
  let known = options.initial;
  let acceptedBasis = options.initial;
  let displayHead = options.initial.head;
  let projecting = false;
  let projectionPending: TimelineCommandBasis | undefined;
  let box: ClaimedOutbox | undefined;
  let record: OutboxRecord | undefined;
  let stopped = false;
  let closing: Promise<void> | undefined;
  let release: (() => void) | undefined;
  let lifetime: Promise<unknown> | undefined;
  let chain = Promise.resolve();
  let sending: Promise<void> | undefined;
  let lastIntent: string | undefined;
  let localGeneration = 0;
  let appendedGeneration = 0;
  let persistenceFailed = false;
  let persistenceError: string | undefined;
  const latestOwn = options.initial.history?.next_cursor == null ? options.initial.history?.items.slice().reverse().find((entry) => entry.publisher === options.scope.actorId
    && entry.intent === 'recorded' && entry.records) : undefined;
  const undos: string[] = latestOwn ? [latestOwn.publication_id] : [];
  const prepared = new Map<string, { payload: Payload; generation: number; basis: OutboxBasis }>();
  let state: CommandSessionState = { status: 'loading', error: null, ownerId: null, recoverableOwners: [], canUndo: false };
  function publish(status: CommandSessionState['status'], error: string | null = null) {
    if (stopped) return;
    state = { ...state, status, error, canUndo: !persistenceFailed
      && ((status === 'saved' && !!undos.length) || (status === 'dirty' && !!record?.intents.length && !record.pending)) };
    options.changed(state);
  }
  function publishRefusal() {
    const failure = record?.pending?.outcome?.kind === 'rejected'
      ? record.pending.outcome.error : record?.intents[0]?.conflict;
    if (failure === undefined) return false;
    const error = failure as { kind?: string; message?: string } | null;
    publish(error?.kind === 'conflict' ? 'conflict' : 'error', error?.message ?? 'Timeline command was refused');
    return true;
  }
  function assertReady() {
    if (stopped || !box || projecting || projectionPending || persistenceFailed || record?.intents[0]?.conflict !== undefined) {
      throw new Error(state.error ?? 'Timeline command session is unavailable');
    }
  }
  async function project(basis: TimelineCommandBasis, previews: TimelinePatch[]) {
    if (stopped) return;
    projecting = true;
    projectionPending = basis;
    try {
      await options.project(basis, previews);
      displayHead = basis.head;
      if (projectionPending === basis) projectionPending = undefined;
    } finally { projecting = false; }
  }
  async function pump() {
    if (sending) return sending;
    sending = (async () => {
      await chain;
      if (stopped || persistenceFailed || !box) return;
      record = await box.read();
      if (!record.intents.length && projectionPending) {
        const target = projectionPending;
        bundle = await authoringBundleFromDocument(target.canonicalDocument) as AuthoredBundle;
        await project(target, []);
        known = target;
        acceptedBasis = target;
      }
      if (publishRefusal()) return;
      while (!stopped && record.intents.length && record.intents[0].conflict === undefined) {
        publish('saving');
        const priorAccepted = record.accepted?.intentId;
        record = await box.dispatch((intent, head) => ({
          method: 'POST',
          path: `/v1/projects/${encodeURIComponent(options.scope.projectId)}/timelines/${encodeURIComponent(options.scope.timelineId)}/commit`,
          body: json({ api_version: 1, project_id: options.scope.projectId, timeline_id: options.scope.timelineId,
            base_revision_id: head.revisionId, base_publication_id: head.publicationId,
            commands: (intent.payload as unknown as Payload).commands, source: { via: 'app' } } satisfies CommitRequest),
        }), async (request) => {
          try {
            if (stopped) throw new Error('Timeline command session is closed');
            const result = await options.send(JSON.parse(request.body) as CommitRequest, request.key);
            return { kind: 'accepted', head: result.accepted, value: json(result) };
          } catch (error) {
            const kind = error instanceof ApiError && error.status >= 500 ? 'unknown' : classifyRuntimeCommitFailure(error);
            return { kind: kind === 'unknown' || kind === 'storage' ? 'retry' : 'rejected',
              error: { kind, message: message(error) } };
          }
        });
        if (stopped) return;
        if (record.accepted && record.accepted.intentId !== priorAccepted) {
          const result = record.accepted.value as unknown as TimelineCommitResult;
          acceptedBasis = { head: result.accepted, canonicalDocument: result.canonicalDocument, graph: result.graph };
          const previous = result.response.data;
          const followsKnown = sameHead(known.head, result.accepted) || sameHead(known.head, {
            revisionId: previous.previous_revision_id, publicationId: previous.previous_publication_id,
          }) || sameHead(known.head, { revisionId: previous.base_revision_id, publicationId: previous.base_publication_id });
          if (followsKnown) known = acceptedBasis;
          const commands = result.response.data.commands;
          if (commands.some((command) => command.op === 'timeline.inverse')) undos.pop();
          else if (undos[undos.length - 1] !== result.accepted.publicationId) undos.push(result.accepted.publicationId);
          // A's ACK cannot erase B, including B whose durable append is still queued.
          if (!record.intents.length && appendedGeneration === localGeneration) {
            const nextBundle = await authoringBundleFromDocument(known.canonicalDocument) as AuthoredBundle;
            if (!stopped && !record.intents.length && appendedGeneration === localGeneration) {
              const generation = localGeneration;
              acceptedBasis = known;
              bundle = nextBundle;
              await project(known, []);
              if (generation === localGeneration) lastIntent = undefined;
            }
          }
        }
        if (publishRefusal()) return;
        if (record.pending) {
          const outcome = record.pending.outcome;
          publish('retry',
            outcome && outcome.kind !== 'accepted' ? String((outcome.error as { message?: string } | null)?.message ?? 'Commit outcome is unknown; retry the exact request') : null);
          return;
        }
        await chain;
        record = await box.read();
      }
      if (!publishRefusal()) publish(record.intents.length || appendedGeneration !== localGeneration ? 'dirty' : 'saved');
    })().catch((error) => { publish('error', message(error)); }).finally(() => { sending = undefined; });
    return sending;
  }
  const pendingAppends: Array<{ localId: string; predecessor?: string; head: OutboxHead; payload: Payload; generation: number }> = [];
  async function persistAppends() {
    if (persistenceFailed || !box) return;
    try {
      while (pendingAppends.length) {
        const entry = pendingAppends[0];
        const basis: OutboxBasis = entry.predecessor
          ? { after: intentIds.get(entry.predecessor) ?? entry.predecessor } : { head: entry.head };
        const id = await box.append(json(entry.payload), basis);
        intentIds.set(entry.localId, id);
        appendedGeneration = entry.generation;
        pendingAppends.shift();
        record = await box.read();
      }
    } catch (error) {
      persistenceFailed = true;
      persistenceError = `Unsaved move: ${message(error)}`;
      publish('error', persistenceError);
    }
  }
  function enqueue(payload: Payload, preview: TimelinePatch | null, capturedBasis?: OutboxBasis) {
    assertReady();
    const predecessor = capturedBasis && 'after' in capturedBasis ? capturedBasis.after : capturedBasis ? undefined : lastIntent;
    const generation = ++localGeneration;
    const previousBundle = bundle;
    // Advance authored bytes synchronously, before the next capture/service call.
    bundle = payload.after;
    publish('dirty');
    try { if (preview) options.preview(preview); }
    catch (error) { bundle = previousBundle; localGeneration--; publish('error', message(error)); throw error; }
    const localId = crypto.randomUUID();
    lastIntent = localId;
    pendingAppends.push({ localId, predecessor, head: capturedBasis && 'head' in capturedBasis ? capturedBasis.head : known.head, generation,
      payload: { ...payload, displayBasis: acceptedBasis } });
    chain = chain.then(persistAppends);
    void chain.then(() => pump());
  }
  const intentIds = new Map<string, string>();
  const port: ClipMoveCapturePort = {
    capture({ clipId, current }) {
      assertReady();
      const matches = current.resolvedConfig.clips.filter((clip) => clip.id === clipId);
      if (matches.length !== 1) throw new Error('Move requires one raw clip identity');
      if (current.head?.headRevisionId !== displayHead.revisionId
        || (current.head.headPublicationId != null && current.head.headPublicationId !== displayHead.publicationId)) {
        throw new Error('Displayed timeline does not match the raw authoring basis');
      }
      const identity = matches[0].app?.canonical as { clipRef?: string } | undefined;
      const select = identity?.clipRef ?? `parent/clip:${clipId}`;
      return json({ ...captureClipMove(bundle, select), localGeneration,
        localBasis: lastIntent ? { after: lastIntent } : { head: known.head } }) as ReturnType<ClipMoveCapturePort['capture']>;
    },
    finish(basis, on) {
      assertReady();
      if (basis.localGeneration !== localGeneration) throw new Error('Timeline changed during the move');
      const result = finishClipMove(basis, on);
      prepared.set(JSON.stringify(result.command), { payload: {
        commands: [result.command], before: (basis as unknown as { bundle: AuthoredBundle }).bundle,
        after: result.bundle, preview: null,
      }, generation: localGeneration, basis: basis.localBasis as unknown as OutboxBasis });
      return { command: result.command as ClipMoveProposal, previewAt: result.previewAt };
    },
    submit({ command, preview }) {
      assertReady();
      const key = JSON.stringify(command);
      const entry = prepared.get(key);
      if (!entry || entry.generation !== localGeneration) throw new Error('Move was not captured by this session');
      prepared.delete(key);
      enqueue({ ...entry.payload, preview }, preview, entry.basis);
    },
  };
  async function claim(owner?: string) {
    if (stopped) throw new Error('Timeline command session is closed');
    if (lifetime) throw new Error('An outbox is already claimed');
    let ready!: () => void;
    let fail!: (error: unknown) => void;
    const mounted = new Promise<void>((resolve, reject) => { ready = resolve; fail = reject; });
    const hold = async (claimed: ClaimedOutbox, ownerId: string) => {
      box = claimed;
      state = { ...state, ownerId, recoverableOwners: [] };
      record = await box.read();
      if (record.intents.length) {
        lastIntent = record.intents[record.intents.length - 1].id;
        const payload = record.intents[record.intents.length - 1].payload as unknown as Payload;
        bundle = payload.after;
        // Repaint original local intent; do not replace it with a new capture on today's head.
        const first = record.intents[0].payload as unknown as Payload;
        const original = first.before.source_mapping as { _runtime_document?: JSON };
        const savedAcceptance = record.accepted?.value as unknown as TimelineCommitResult | undefined;
        const basis = record.intents[0].basis;
        // A's accepted submission base does not repin B's original displayed closure.
        const displayBasis = first.displayBasis ?? ('head' in basis ? {
          head: basis.head, canonicalDocument: original?._runtime_document as unknown as TimelineCommandBasis['canonicalDocument'],
        } : undefined);
        if (typeof displayBasis?.head?.revisionId !== 'string' || !displayBasis.head.revisionId
          || typeof displayBasis.head.publicationId !== 'string' || !displayBasis.head.publicationId
          || displayBasis.canonicalDocument?.parent_revision?.revision_id !== displayBasis.head.revisionId) {
          throw new Error('Recovered move has no verified original display basis');
        }
        acceptedBasis = savedAcceptance ? { head: savedAcceptance.accepted, canonicalDocument: savedAcceptance.canonicalDocument, graph: savedAcceptance.graph }
          : displayBasis;
        // Submission advances with A's ACK; B's display retains its original closure.
        await project(displayBasis,
          record.intents.map((intent) => (intent.payload as unknown as Payload).preview).filter((patch): patch is TimelinePatch => patch !== null));
      }
      if (!publishRefusal()) publish(record.intents.length ? 'dirty' : 'saved');
      ready();
      await new Promise<void>((resolve) => { release = resolve; if (stopped) resolve(); });
    };
    lifetime = (owner ? storage.recover(options.scope, owner, (claimed) => hold(claimed, owner))
      : storage.create(options.scope, hold)).catch((error) => { fail(error); publish('error', message(error)); });
    try { await mounted; }
    catch (error) {
      box = undefined;
      lifetime = undefined;
      state = { ...state, ownerId: null };
      throw error;
    }
  }
  const owners = (await storage.list(options.scope)).filter((owner) => owner.intents.length || owner.pending);
  if (owners.length) {
    state = { ...state, recoverableOwners: owners.map((owner) => owner.ownerId) };
    publish('recovery', 'Choose the persisted editor owner to recover its exact pending request');
  } else await claim();
  return {
    port,
    scope: freezeJson(json(options.scope)) as unknown as OutboxScope,
    /** Explicit manual choice only; the existing owner/outbox remains the sole writer. */
    async addOccurrenceMedia(input: {
      basis: TimelineCommandBasis; ownerRef: string; row: Record<string, JSON>;
      media: MediaSelection; verifiedMedia: VerifiedMedia;
      assertCurrent(): void;
      onEnqueued(): void;
    }): Promise<TimelineCommandBasis> {
      const original = await authoringBundleFromDocument(input.basis.canonicalDocument);
      input.assertCurrent();
      assertReady();
      if (state.status !== 'saved' || sending || record?.intents.length || pendingAppends.length
        || localGeneration !== appendedGeneration || !sameHead(input.basis.head, known.head)
        || !sameHead(input.basis.head, displayHead) || !equal(input.basis.canonicalDocument, acceptedBasis.canonicalDocument)
        || !equal(original, bundle)
        || input.basis.canonicalDocument.project_id !== options.scope.projectId
        || input.basis.canonicalDocument.timeline_id !== options.scope.timelineId) {
        throw new Error('Manual placement requires the unchanged selected head and an idle command owner');
      }
      const captured = captureOccurrenceAddMedia(bundle, input.ownerRef, input.row, input.media, [input.verifiedMedia]);
      // No optimistic Placed state or compatibility writer. Publish only the normal accepted closure.
      enqueue({ commands: [captured.command], before: bundle, after: captured.bundle, preview: null }, null);
      // The owner now retains this payload even if its durable append or ACK fails.
      input.onEnqueued();
      await chain;
      await pump();
      if (state.status !== 'saved') throw new Error(state.error ?? 'Manual placement is not acknowledged; draft kept');
      return acceptedBasis;
    },
    getState: () => state,
    async recover(ownerId: string) {
      if (!state.recoverableOwners.includes(ownerId)) throw new Error('Unknown persisted outbox owner');
      await claim(ownerId);
      // Explicit recovery authorizes retry; never adopt a sessionStorage owner.
      await pump();
    },
    async retry() {
      if (stopped) throw new Error('Timeline command session is closed');
      persistenceFailed = false;
      chain = chain.then(persistAppends);
      await chain;
      await pump();
    },
    async flush() {
      await chain;
      await pump();
      if (state.status !== 'saved') throw new Error(state.error ?? 'Timeline commands are not acknowledged');
      return known.head;
    },
    async undo() {
      assertReady();
      await chain;
      record = await box!.read();
      if (record.pending || sending) throw new Error('Resolve the uncertain commit before undo');
      if (record.intents.length) {
        const tail = record.intents[record.intents.length - 1];
        await box!.cancel(tail.id);
        record = await box!.read();
        bundle = (tail.payload as unknown as Payload).before;
        lastIntent = record.intents[record.intents.length - 1]?.id;
        localGeneration++;
        appendedGeneration = localGeneration;
        await project(acceptedBasis, record.intents.map((intent) => (intent.payload as unknown as Payload).preview)
          .filter((patch): patch is TimelinePatch => patch !== null));
        publish(record.intents.length ? 'dirty' : 'saved');
        return;
      }
      const publication = undos[undos.length - 1];
      if (!publication) throw new Error('No accepted local publication to undo');
      enqueue({ commands: [{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
        args: { publications: [publication] } }], before: bundle, after: bundle, preview: null }, null);
      await pump();
    },
    observe(remote: TimelineCommandBasis) {
      if (sameHead(remote.head, known.head)) return;
      known = remote;
      if (!record?.intents.length && localGeneration === appendedGeneration && !sending) {
        const generation = localGeneration;
        projectionPending = remote;
        void authoringBundleFromDocument(remote.canonicalDocument).then(async (next) => {
          if (!stopped && known === remote && !record?.intents.length && generation === localGeneration) {
            bundle = next as AuthoredBundle;
            acceptedBasis = remote;
            await project(remote, []);
            publish('saved');
          }
        }).catch((error) => publish('error', message(error)));
      }
    },
    dispose() {
      stopped = true;
      closing ??= (async () => {
        try {
          // Drain accepted gestures, never wait for an unknown network outcome.
          await chain;
          if (pendingAppends.length) {
            const error = persistenceError ?? 'Unsaved move: durable append did not finish';
            state = { ...state, status: 'error', error, canUndo: false };
            throw new Error(error);
          }
        } finally {
          release?.();
          await lifetime;
        }
      })();
      return closing;
    },
  };
}
export type TimelineCommandSession = Awaited<ReturnType<typeof createTimelineCommandSession>>;
