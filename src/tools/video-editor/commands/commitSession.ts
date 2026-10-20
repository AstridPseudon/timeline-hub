import type { ClipTrimCapturePort } from './clipTrimGesture.ts';
import { captureClipTrim, executeClipTrim } from './clipTrimCapture.ts';
import { captureClipSplit, executeClipSplit, finishClipSplit } from './clipSplitCapture.ts';
import { clipSplitPreview, type ClipSplitCapturePort } from './clipSplitGesture.ts';
import { clipScalarPreview, type ClipScalarCapturePort } from './clipScalarGesture.ts';
import { captureClipSet, executeClipSet } from './clipScalarCapture.ts';
import { stableOutputIdentity } from '../data/shotComposition.ts';
import type { CanonicalProjectedClipIdentity } from '../data/shotCompositionProjection.ts';
import type { ClipParamsCapturePort } from './clipParamsGesture.ts';
import { captureClipParams, finishClipParams } from './clipParamsCapture.ts';
import type { CommitRequest, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { ApiError } from '@/integrations/runtime/generated.ts';
import { classifyRuntimeCommitFailure } from '@/integrations/runtime/client.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { authoringBundleFromDocument, type AuthoringBundle } from './authoringBundle.ts';
import { captureClipMove, finishClipMove, type AuthoredBundle } from './clipMoveCapture.ts';
import type { ClipMoveCapturePort, ClipMoveProposal } from './semanticGestures.ts';
import { AuthoredState, MoveRecording, assertFiniteJson, copy, equal, freezeJson, object } from './clipMovePrimitives.ts';
import { captureTrackLabel, finishTrackLabel, type TrackLabelArgs } from './trackLabelCapture.ts';
import type { TrackLabelCapturePort } from './trackLabelGesture.ts';
import { createCommitOutbox, type ClaimedOutbox, type OutboxBasis, type OutboxHead, type OutboxRecord, type OutboxScope } from './commitOutbox.ts';

type Payload = { commands: EditCommand[]; before: AuthoredBundle; after: AuthoredBundle; preview: TimelinePatch | null; displayBasis?: TimelineCommandBasis };
export type CommandSessionState = {
  status: 'loading' | 'saved' | 'dirty' | 'saving' | 'retry' | 'conflict' | 'error' | 'recovery';
  error: string | null;
  ownerId: string | null;
  recoverableOwners: string[];
  canUndo: boolean;
  canDiscardRejected?: boolean;
  canReapplyLabel?: boolean;
};
type Options = {
  scope: OutboxScope;
  initial: TimelineCommandBasis;
  outboxes?: ReturnType<typeof createCommitOutbox>;
  loadLatest?(): Promise<TimelineCommandBasis>;
  send(request: CommitRequest, key: string): Promise<TimelineCommitResult>;
  preview(patch: TimelinePatch): void;
  project(basis: TimelineCommandBasis, previews: TimelinePatch[]): Promise<void>;
  changed(state: CommandSessionState): void;
};
const sameHead = (a: OutboxHead, b: OutboxHead) => a.revisionId === b.revisionId && a.publicationId === b.publicationId;
const message = (error: unknown) => error instanceof Error ? error.message : String(error);
const json = (value: unknown): JSON => JSON.parse(JSON.stringify(value)) as JSON;
const hasChildTrack = (bundle: AuthoredBundle, trackId: string) => Object.values(bundle.shots).some((shot) =>
  Array.isArray(shot.internal_timeline.tracks) && shot.internal_timeline.tracks.some((track) =>
    track !== null && typeof track === 'object' && !Array.isArray(track) && track.id === trackId));

/** One browser-lock lifetime, one durable prefix, original guarded suffixes. */
export async function createTimelineCommandSession(options: Options) {
  const storage = options.outboxes ?? createCommitOutbox();
  let bundle = await authoringBundleFromDocument(options.initial.canonicalDocument) as AuthoredBundle;
  let known = options.initial;
  let acceptedBasis = options.initial;
  let displayHead = options.initial.head;
  let projecting = false;
  let projectionGeneration = 0;
  let resolving = false;
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
  function rejected() {
    return !!box && !resolving && !persistenceFailed && !pendingAppends.length
      && record?.pending?.outcome?.kind === 'rejected' && record.pending.intentId === record.intents[0]?.id;
  }
  function labelIntent() {
    if (record?.intents.length !== 1) return;
    const commands = (record.intents[0].payload as unknown as Payload).commands;
    if (commands?.length !== 1) return;
    const command = commands[0];
    if (command.schema_version !== 1 || command.op !== 'track.set' || command.version !== '1'
      || typeof command.select !== 'string' || !/^parent\/track:[^/]+$/.test(command.select) || command.select.includes('::')
      || (command.intent !== undefined && !equal(command.intent, {}))) return;
    const args = command.args;
    if (!args || !equal(Object.keys(args).sort(), ['clear', 'values'])
      || !args.values || typeof args.values !== 'object' || Array.isArray(args.values)) return;
    if (!(equal(Object.keys(args.values), ['label']) && typeof args.values.label === 'string' && equal(args.clear, []))
      && !(equal(args.values, {}) && equal(args.clear, ['label']))) return;
    return { select: command.select, args: copy(args) as TrackLabelArgs };
  }
  function publish(status: CommandSessionState['status'], error: string | null = null) {
    if (stopped) return;
    state = { ...state, status, error, canDiscardRejected: rejected() && !!options.loadLatest,
      canReapplyLabel: rejected() && !!options.loadLatest && !!labelIntent(), canUndo: !persistenceFailed && !resolving
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
    if (stopped || !box || resolving || projecting || projectionPending || persistenceFailed || record?.intents[0]?.conflict !== undefined) {
      throw new Error(state.error ?? 'Timeline command session is unavailable');
    }
  }
  async function project(basis: TimelineCommandBasis, previews: TimelinePatch[]) {
    if (stopped) return;
    projecting = true;
    const generation = ++projectionGeneration;
    projectionPending = basis;
    try {
      await options.project(basis, previews);
      if (stopped || generation !== projectionGeneration) return;
      displayHead = basis.head;
      if (projectionPending === basis) projectionPending = undefined;
    } finally { projecting = false; }
  }
  async function pump() {
    if (sending) return sending;
    sending = (async () => {
      await chain;
      if (stopped || resolving || persistenceFailed || !box) return;
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
        record = await box.dispatch((intent, head) => {
          const commands = (intent.payload as unknown as Payload).commands;
          if (!Array.isArray(commands) || commands.length === 0) throw new Error('Timeline commit requires commands');
          return {
            method: 'POST',
            path: `/v1/projects/${encodeURIComponent(options.scope.projectId)}/timelines/${encodeURIComponent(options.scope.timelineId)}/commit`,
            body: json({ api_version: 1, project_id: options.scope.projectId, timeline_id: options.scope.timelineId,
              base_revision_id: head.revisionId, base_publication_id: head.publicationId,
              commands: [commands[0], ...commands.slice(1)], source: { via: 'app' } } satisfies CommitRequest),
          };
        }, async (request) => {
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
  const trackLabelPort: TrackLabelCapturePort = {
    capture({ trackId, current }) {
      assertReady();
      if (current.head?.projectId !== options.scope.projectId || current.head.timelineId !== options.scope.timelineId
        || current.head.headRevisionId !== displayHead.revisionId || current.head.headPublicationId !== displayHead.publicationId) {
        throw new Error('Displayed timeline does not match the raw authoring basis');
      }
      if (current.resolvedConfig.tracks.filter((track) => track.id === trackId).length !== 1
        || hasChildTrack(bundle, trackId)) {
        throw new Error('Track label requires one unambiguous parent track identity');
      }
      return json({ ...captureTrackLabel(bundle, `parent/track:${trackId}`), localGeneration,
        localBasis: lastIntent ? { after: lastIntent } : { head: known.head } }) as ReturnType<TrackLabelCapturePort['capture']>;
    },
    finish(basis, args) {
      assertReady();
      if (basis.localGeneration !== localGeneration) throw new Error('Timeline changed during the label edit');
      const result = finishTrackLabel(basis, args);
      const next = new AuthoredState(copy(bundle));
      // Remote changes during typing may advance the closure, but never refresh these guards.
      if (!result.command.reads!.every((read) => next.matches(read.ref, read.path, read.state))
        || !result.record.writes.every((write) => next.matches(write.ref, write.path, write.before))) {
        throw new Error('Track label changed during the label edit');
      }
      for (const write of result.record.writes) next.set(write.ref, write.path, write.after);
      prepared.set(JSON.stringify(result.command), { payload: {
        commands: [result.command], before: bundle, after: next.bundle, preview: null,
      }, generation: localGeneration, basis: basis.localBasis as unknown as OutboxBasis });
      return { command: result.command };
    },
    submit({ command, preview }) {
      assertReady();
      const key = JSON.stringify(command);
      const entry = prepared.get(key);
      if (command.op !== 'track.set' || !entry || entry.generation !== localGeneration || entry.payload.before !== bundle) {
        throw new Error('Track label was not captured by this session or the timeline changed');
      }
      const args = command.args as TrackLabelArgs;
      const trackId = command.select!.slice('parent/track:'.length);
      if (preview.version !== 1 || !equal(preview.operations, [{ op: 'track.update', target: trackId,
        payload: { label: 'label' in args.values ? args.values.label : trackId } }])) {
        throw new Error('Track label requires one label-only preview');
      }
      prepared.delete(key);
      enqueue({ ...entry.payload, preview }, preview, entry.basis);
    },
  };
  const clipParamsPort: ClipParamsCapturePort = {
    capture({ clipId, current }) {
      assertReady();
      if (current.head?.projectId !== options.scope.projectId || current.head.timelineId !== options.scope.timelineId
        || current.head.headRevisionId !== displayHead.revisionId || current.head.headPublicationId !== displayHead.publicationId) {
        throw new Error('Displayed timeline does not match the raw authoring basis');
      }
      const matches = current.resolvedConfig.clips.filter((clip) => clip.id === clipId);
      if (matches.length !== 1 || current.config.pinnedShotGroups?.some((group) => group.clipIds.includes(clipId))) {
        throw new Error('Clip parameters require one unambiguous raw clip identity');
      }
      const identity = matches[0].app?.canonical;
      let select = `parent/clip:${clipId}`;
      if (identity !== undefined) {
        if (!object(identity) || typeof identity.occurrenceId !== 'string' || typeof identity.rawClipId !== 'string'
          || identity.ownerRef !== `occurrence:${identity.occurrenceId}`
          || identity.clipRef !== `${identity.ownerRef}/clip:${identity.rawClipId}`
          || clipId !== `${identity.occurrenceId}:${identity.rawClipId}`) {
          throw new Error('Clip parameters require an addressable canonical clipRef');
        }
        select = identity.clipRef;
      } else if (Object.values(bundle.shots).some((shot) => Array.isArray(shot.internal_timeline.clips)
        && shot.internal_timeline.clips.some((clip) => object(clip) && clip.id === clipId))) {
        throw new Error('Clip parameters require explicit occurrence ownership');
      }
      if (!/^(?:parent|occurrence:[^/]+)\/clip:[^/]+$/.test(select) || select.includes('::')) {
        throw new Error('Clip parameters require a stable scoped clip identity');
      }
      new AuthoredState(bundle).entity(select);
      const basis = { bundle: copy(bundle), select, clipId, localGeneration,
        localBasis: lastIntent ? { after: lastIntent } : { head: known.head } };
      assertFiniteJson(basis);
      return freezeJson(json(basis)) as ReturnType<ClipParamsCapturePort['capture']>;
    },
    finish(basis, args) {
      assertReady();
      if (basis.localGeneration !== localGeneration) throw new Error('Timeline changed during the parameters edit');
      const original = basis.bundle as AuthoredBundle;
      const result = finishClipParams(captureClipParams(original, basis.select as string, args), args);
      const next = new MoveRecording(bundle, result.command);
      // Final keys and all native claims come only from the original snapshot.
      if (!result.command.reads!.every((read) => next.state.matches(read.ref, read.path, read.state))) {
        throw new Error('Clip parameters changed during the parameters edit');
      }
      for (const write of result.record.writes) {
        if (!next.state.matches(write.ref, write.path, write.before)) {
          throw new Error('Clip parameters changed during the parameters edit');
        }
        // Unchanged writes still claim the field; absent clears retain native ancestors.
        if (!equal(write.before, write.after)) next.state.set(write.ref, write.path, write.after);
      }
      next.compile();
      const beforeParams = new AuthoredState(bundle).get(result.command.select!, ['params']);
      const afterParams = next.state.get(result.command.select!, ['params']);
      const previewParams = afterParams.state === 'present' && object(afterParams.value) && !equal(beforeParams, afterParams)
        ? afterParams.value : null;
      const preview: TimelinePatch | null = previewParams === null ? null : { version: 1, operations: [{ op: 'clip.update', target: basis.clipId as string,
        payload: { params: copy(previewParams) } }] };
      freezeJson(result.command);
      prepared.set(JSON.stringify(result.command), { payload: {
        commands: [result.command], before: bundle, after: next.state.bundle, preview,
      }, generation: localGeneration, basis: basis.localBasis as unknown as OutboxBasis });
      return { command: result.command, previewParams: copy(previewParams) };
    },
    submit({ command, preview }) {
      assertReady();
      assertFiniteJson(command);
      assertFiniteJson(preview);
      const key = JSON.stringify(command);
      const entry = prepared.get(key);
      if (command.op !== 'clip.set-params' || !entry || entry.generation !== localGeneration || entry.payload.before !== bundle) {
        throw new Error('Clip parameters were not captured by this session or the timeline changed');
      }
      if (!equal(preview, entry.payload.preview)) throw new Error('Clip parameters require one params-only preview');
      prepared.delete(key);
      const localPreview = freezeJson(copy(preview));
      enqueue({ ...entry.payload, preview: localPreview }, localPreview, entry.basis);
    },
  };
  const clipScalarPort: ClipScalarCapturePort = {
    capture({ clipId, ownerRef: requestedOwner, current }) {
      assertReady();
      if (current.head?.projectId !== options.scope.projectId || current.head.timelineId !== options.scope.timelineId
        || current.head.headRevisionId !== displayHead.revisionId || current.head.headPublicationId !== displayHead.publicationId) {
        throw new Error('Displayed timeline does not match the raw authoring basis');
      }
      const matches = current.resolvedConfig.clips.filter((clip) => clip.id === clipId);
      if (matches.length !== 1) throw new Error('Scalar edit requires one raw clip identity');
      const identity = matches[0].app?.canonical as Partial<CanonicalProjectedClipIdentity> | undefined;
      const parentRef = `parent/clip:${clipId}`;
      const raw = new AuthoredState(bundle);
      // Parent app fields are authored opaque data, not projected ownership facts.
      const ownerRef = requestedOwner ?? (
        !clipId.includes('/') && !clipId.includes('::') && raw.entity(parentRef, true) ? 'parent' : identity?.ownerRef);
      const select = ownerRef === 'parent' ? parentRef : identity?.clipRef;
      if (typeof ownerRef !== 'string' || typeof select !== 'string' || select.slice(0, select.lastIndexOf('/')) !== ownerRef
        || !/^(?:parent|occurrence:[^/]+)\/clip:[^/]+$/.test(select) || select.includes('::')
        || !raw.entity(select, true)) {
        throw new Error('Scalar edit requires an explicit matching raw clip owner');
      }
      if (ownerRef !== 'parent') {
        if (!identity || typeof identity.occurrenceId !== 'string'
          || identity.ownerRef !== ownerRef || ownerRef !== `occurrence:${identity.occurrenceId}`
          || typeof identity.rawClipId !== 'string' || select !== `${ownerRef}/clip:${identity.rawClipId}`
          // Confirm the projector's output ID only after binding the explicit owner.
          || clipId !== `${identity.occurrenceId}:${identity.rawClipId}` || raw.entity(parentRef, true)
          || identity.projectId !== options.scope.projectId || identity.parentDocumentId !== options.scope.timelineId) {
          throw new Error('Scalar edit requires an explicit matching raw clip owner');
        }
        const occurrence = raw.occurrence(ownerRef);
        const source = (bundle as AuthoringBundle).source_mapping.shots[String(occurrence.shot_id)];
        if (!source || identity.shotId !== source.shot_id || identity.revisionId !== source.revision_id
          || identity.internalTimelineRevisionId !== source.internal_timeline_revision_id
          || identity.outputIdentity !== stableOutputIdentity(options.scope.projectId, options.scope.timelineId, identity.occurrenceId)) {
          throw new Error('Scalar edit requires an explicit matching raw clip owner');
        }
      }
      return json({ bundle, select, clipId, localGeneration,
        localBasis: lastIntent ? { after: lastIntent } : { head: known.head } }) as ReturnType<ClipScalarCapturePort['capture']>;
    },
    finish(basis, args) {
      assertReady();
      if (basis.localGeneration !== localGeneration) throw new Error('Timeline changed during the scalar edit');
      const original = basis as unknown as { bundle: AuthoredBundle; select: string; clipId: string; localBasis: OutboxBasis };
      const command = captureClipSet(original.bundle, original.select, args);
      // Re-execute the original claims on current raw bytes; an ACK never refreshes them.
      const result = executeClipSet(bundle, command);
      prepared.set(JSON.stringify(command), { payload: {
        commands: [command], before: bundle, after: result.bundle, preview: clipScalarPreview(original.clipId, args),
      }, generation: localGeneration, basis: original.localBasis });
      return { command };
    },
    submit({ command, preview }) {
      assertReady();
      const key = JSON.stringify(command);
      const entry = prepared.get(key);
      if (command.op !== 'clip.set' || !entry || entry.generation !== localGeneration || entry.payload.before !== bundle) {
        throw new Error('Scalar edit was not captured by this session or the timeline changed');
      }
      if (!equal(preview, entry.payload.preview)) throw new Error('Scalar edit requires its exact leaf-only preview');
      prepared.delete(key);
      enqueue({ ...entry.payload, preview }, preview, entry.basis);
    },
  };
  const clipTrimPort: ClipTrimCapturePort = {
    capture({ clipId, current }) {
      assertReady();
      if (current.head?.projectId !== options.scope.projectId || current.head.timelineId !== options.scope.timelineId
        || current.head.headRevisionId !== displayHead.revisionId || current.head.headPublicationId !== displayHead.publicationId) {
        throw new Error('Displayed timeline does not match the raw authoring basis');
      }
      const matches = current.resolvedConfig.clips.filter((clip) => clip.id === clipId);
      const identity = matches[0]?.app?.canonical as { clipRef?: string; occurrenceId?: string } | undefined;
      if (matches.length !== 1 || identity?.occurrenceId !== undefined
        || (identity?.clipRef !== undefined && identity.clipRef !== `parent/clip:${clipId}`)) {
        throw new Error('Trim requires one literal parent clip identity');
      }
      return json({ ...captureClipTrim(bundle, `parent/clip:${clipId}`), localGeneration,
        localBasis: lastIntent ? { after: lastIntent } : { head: known.head } }) as ReturnType<ClipTrimCapturePort['capture']>;
    },
    finish(basis, args) {
      assertReady();
      if (basis.localGeneration !== localGeneration) throw new Error('Timeline changed during the trim');
      if (!basis.bundle || !basis.command || !['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created']
        .every((key) => Object.prototype.hasOwnProperty.call(basis.command, key))) {
        throw new Error('Incomplete clip.trim basis');
      }
      const original = executeClipTrim(basis.bundle as AuthoredBundle,
        { ...copy(basis.command as EditCommand), args: { ...args, in_s: args.in_s ?? null, out_s: args.out_s ?? null } });
      // Verify original claims on today's closure; never replace disjoint remote fields with the captured bundle.
      const result = executeClipTrim(bundle, original.command);
      const payload: Record<string, unknown> = {};
      for (const write of result.record.writes) {
        if (write.after.state === 'present') payload[write.path[0]] = copy(write.after.value);
        else if (write.before.state === 'present') {
          throw new Error('Exact trim intent-container removal needs the session scalar clear preview');
        }
      }
      const source = new AuthoredState(result.bundle).entity(result.command.select!)!;
      // A preceding move preview may have serialized a held clip without its source speed.
      if ('speed' in source) payload.speed = copy(source.speed);
      const preview: TimelinePatch = { version: 1, source: 'clip.trim', operations: [
        { op: 'clip.update', target: result.command.select!.slice('parent/clip:'.length), payload },
      ] };
      prepared.set(JSON.stringify(result.command), { payload: {
        commands: [result.command], before: bundle, after: result.bundle, preview,
      }, generation: localGeneration, basis: basis.localBasis as unknown as OutboxBasis });
      return { command: result.command, preview };
    },
    submit({ command, preview }) {
      assertReady();
      const key = JSON.stringify(command);
      const entry = prepared.get(key);
      if (command.op !== 'clip.trim' || !entry || entry.generation !== localGeneration || entry.payload.before !== bundle) {
        throw new Error('Trim was not captured by this session or the timeline changed');
      }
      if (!equal(preview, entry.payload.preview)) throw new Error('Trim requires its native source-window preview');
      prepared.delete(key);
      enqueue(entry.payload, preview, entry.basis);
    },
  };
  const clipSplitPort: ClipSplitCapturePort = {
    capture({ clipId, on, rightId, current }) {
      assertReady();
      if (current.head?.projectId !== options.scope.projectId || current.head.timelineId !== options.scope.timelineId
        || current.head.headRevisionId !== displayHead.revisionId || current.head.headPublicationId !== displayHead.publicationId) {
        throw new Error('Displayed timeline does not match the raw authoring basis');
      }
      const matches = current.resolvedConfig.clips.filter((clip) => clip.id === clipId);
      const identity = matches[0]?.app?.canonical as { clipRef?: string; occurrenceId?: string } | undefined;
      if (matches.length !== 1 || identity?.occurrenceId !== undefined
        || (identity?.clipRef !== undefined && identity.clipRef !== `parent/clip:${clipId}`)
        || current.config.pinnedShotGroups?.some((group) => group.clipIds.includes(clipId))
        || current.config.clips.some((clip) => clip.id === rightId)
        || current.resolvedConfig.clips.some((clip) => clip.id === rightId)) {
        throw new Error('Split requires one literal parent clip identity');
      }
      return freezeJson(json({ ...captureClipSplit(bundle, `parent/clip:${clipId}`, { on, right_id: rightId }),
        localGeneration, localBasis: lastIntent ? { after: lastIntent } : { head: known.head } })) as ReturnType<ClipSplitCapturePort['capture']>;
    },
    finish(basis) {
      assertReady();
      if (basis.localGeneration !== localGeneration) throw new Error('Timeline changed during the split');
      const original = finishClipSplit(basis);
      // Re-execute the original guarded capture on current raw bytes; never recapture after an ACK.
      const result = executeClipSplit(bundle, original.command);
      const select = result.command.select!;
      const left = new AuthoredState(result.bundle).entity(select)!;
      const rightId = (result.command.args as { right_id: string }).right_id;
      const right = new AuthoredState(result.bundle).entity(`parent/clip:${rightId}`)!;
      const preview = clipSplitPreview(select.slice('parent/clip:'.length), left, right);
      prepared.set(JSON.stringify(result.command), { payload: {
        commands: [result.command], before: bundle, after: result.bundle, preview,
      }, generation: localGeneration, basis: basis.localBasis as unknown as OutboxBasis });
      return { command: result.command, preview };
    },
    submit({ command, preview }) {
      assertReady();
      assertFiniteJson(command);
      assertFiniteJson(preview);
      const key = JSON.stringify(command);
      const entry = prepared.get(key);
      if (command.op !== 'clip.split' || !entry || entry.generation !== localGeneration || entry.payload.before !== bundle) {
        throw new Error('Split was not captured by this session or the timeline changed');
      }
      if (!equal(preview, entry.payload.preview)) throw new Error('Split requires its exact native preview');
      prepared.delete(key);
      enqueue(entry.payload, preview, entry.basis);
    },
  };
  async function resolveRejected(keepLabel: boolean) {
    if (stopped || !rejected() || !options.loadLatest) throw new Error('Only a definitively rejected prefix can be resolved');
    const label = keepLabel ? labelIntent() : undefined;
    if (keepLabel && !label) throw new Error('Keep supports only one parent track label with no retained suffix');
    const ids = record!.intents.map((intent) => intent.id);
    resolving = true;
    projectionGeneration++;
    publish('loading');
    try {
      await chain;
      await sending;
      const fresh = await options.loadLatest();
      const document = fresh.canonicalDocument;
      if (document.project_id !== options.scope.projectId || document.timeline_id !== options.scope.timelineId
        || !fresh.head.revisionId || !fresh.head.publicationId || document.parent_revision.revision_id !== fresh.head.revisionId) {
        throw new Error('Resolution requires a verified closure in the current project and timeline');
      }
      const before = await authoringBundleFromDocument(document) as AuthoredBundle;
      let payload: Payload | undefined;
      if (label) {
        const trackId = label.select.slice('parent/track:'.length);
        if (hasChildTrack(before, trackId)) throw new Error('Track label requires one unambiguous parent track identity');
        const result = finishTrackLabel(captureTrackLabel(before, label.select), label.args);
        payload = { commands: [result.command], before, after: result.bundle, displayBasis: fresh,
          preview: { version: 1, operations: [{ op: 'track.update', target: trackId,
            payload: { label: 'label' in label.args.values ? label.args.values.label : trackId } }] } };
      }
      // One owner-fenced transaction either retains all original work or installs the new intent.
      record = await box!.resolveRejected(ids, payload ? { payload: json(payload), head: fresh.head } : undefined, () => !stopped);
      if (stopped) throw new Error('Timeline command session is closed');
      localGeneration++;
      appendedGeneration = localGeneration;
      lastIntent = record.intents[0]?.id;
      prepared.clear();
      intentIds.clear();
      bundle = payload?.after ?? before;
      known = fresh;
      acceptedBasis = fresh;
      await project(fresh, payload?.preview ? [payload.preview] : []);
      resolving = false;
      publish(payload ? 'dirty' : 'saved');
    } catch (error) {
      resolving = false;
      publish('error', message(error));
      throw error;
    }
    if (keepLabel) await pump();
  }
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
    trackLabelPort,
    clipTrimPort,
    clipScalarPort,
    clipParamsPort,
    clipSplitPort,
    useLatest: () => resolveRejected(false),
    keepLabelChanges: () => resolveRejected(true),
    getState: () => state,
    async recover(ownerId: string) {
      if (!state.recoverableOwners.includes(ownerId)) throw new Error('Unknown persisted outbox owner');
      await claim(ownerId);
      // Explicit recovery authorizes retry; never adopt a sessionStorage owner.
      await pump();
    },
    async retry() {
      if (stopped) throw new Error('Timeline command session is closed');
      if (resolving) throw new Error('Timeline conflict resolution is in progress');
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
      if (stopped || resolving || remote.canonicalDocument.project_id !== options.scope.projectId
        || remote.canonicalDocument.timeline_id !== options.scope.timelineId) return;
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
