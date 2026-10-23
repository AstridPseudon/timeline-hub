import type { CanonicalDocument, EditCommand, HistoryPage } from '@/integrations/runtime/timeline-commit-types.ts';
import type { LocalSaveSession } from '../commands/localSaveSession.ts';
import { toOutboxJson, type OutboxJson } from '../commands/commitOutbox.ts';
import { canonicalJsonStringify, type TimelineBundleEnvelope } from '../data/typed/timelineBundle.ts';
import { authoringBundleFromDocument, type AuthoringBundle } from '../commands/authoringBundle.ts';
import { TimelineVersionConflictError, type DataProvider, type TimelineCommandBasis, type TimelineHeadRevision, type TimelineSaveReceipt } from '../data/DataProvider.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import { canonicalizeTimelinePair } from '../lib/timeline-domain.ts';
import { withDefaultTimelineOutput } from '../lib/defaults.ts';
import { markTimelineSaveRejection, type TimelineSaveRejectionCode } from '../lib/timeline-diagnostics.ts';

export interface TimelineSaveSource {
  config: TimelineConfig;
  registry: AssetRegistry;
  bundle?: TimelineBundleEnvelope | null;
  head?: TimelineHeadRevision;
}

/** Known gesture callers snapshot their input before authoring the local transform. */
export type TimelineGestureReadBasis = {
  config: TimelineConfig;
  registry: AssetRegistry;
  clipId: string;
} & ({ kind: 'split'; timeSeconds: number } | { kind: 'move'; trackId: string } | {
  kind: 'trim'; patch: Partial<Pick<TimelineConfig['clips'][number], 'from' | 'to' | 'hold' | 'speed'>>;
});

/** Assembly supplies the ORIGINAL verified read, not loadTimelineCommandBasis at save time. */
export interface TimelineLocalSaveHandoff {
  capture(source: TimelineSaveSource, gestureBasis?: TimelineGestureReadBasis): Promise<void>;
  flush(): Promise<TimelineSaveReceipt>;
  /** True only when the durable owner is settled and has an accepted target. */
  remoteHistoryAvailable(): boolean;
  canUndo(): boolean;
  canRedo(): boolean;
  undo(): Promise<void>;
  redo(): Promise<void>;
}

const same = (a: unknown, b: unknown) => a === undefined || b === undefined
  ? a === b : canonicalJsonStringify(a) === canonicalJsonStringify(b);
const object = (value: unknown): value is Record<string, unknown> =>
  value !== null && typeof value === 'object' && !Array.isArray(value);
const field = (value: Record<string, unknown>, key: string) => Object.prototype.hasOwnProperty.call(value, key) ? value[key] : undefined;

// Upstream config builders include optional undefined fields. Object omission
// also preserves the editor's explicit transition-clear action as a removal.
function authoredJson(value: unknown): OutboxJson {
  if (Array.isArray(value)) return value.map(authoredJson);
  if (value && typeof value === 'object' && Object.getPrototypeOf(value) === Object.prototype) {
    return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== undefined)
      .map(([key, item]) => [key, authoredJson(item)]));
  }
  return toOutboxJson(value);
}

function refuse(message: string, reason?: TimelineSaveRejectionCode): never {
  const error = new TimelineVersionConflictError(`Local document save retained: ${message}`);
  throw reason ? markTimelineSaveRejection(error, reason) : error;
}
function checkHead(initial: TimelineCommandBasis, value: TimelineSaveSource,
  reason: TimelineSaveRejectionCode = 'original-head-unavailable') {
  if (!initial.head.revisionId || !initial.head.publicationId
    || initial.canonicalDocument.parent_revision.revision_id !== initial.head.revisionId
    || value.head?.projectId !== initial.canonicalDocument.project_id
    || value.head.timelineId !== initial.canonicalDocument.timeline_id
    || value.head.headRevisionId !== initial.head.revisionId
    || value.head.headPublicationId !== initial.head.publicationId) refuse('original verified authoring head is unavailable', reason);
}
function checkSource(initial: TimelineCommandBasis, source: TimelineSaveSource) {
  const parent = initial.canonicalDocument.parent_revision.payload;
  if (!object(parent.config) || !object(parent.registry)) refuse('authored parent config/registry is unavailable', 'source-parent-unavailable');
  const { bundle: _bundle, ...config } = structuredClone(parent.config);
  const loaded = { ...config, ...withDefaultTimelineOutput(config as unknown as TimelineConfig) } as unknown as TimelineConfig;
  const projected = canonicalizeTimelinePair(loaded, structuredClone(parent.registry) as unknown as AssetRegistry);
  // Accept the original raw view or main's actual load/build view. No arbitrary
  // display snapshot can establish an authored entity binding.
  if ((!same(authoredJson(source.config), authoredJson(loaded))
    && !same(authoredJson(source.config), authoredJson(projected.config)))
    || !same(authoredJson(source.registry), authoredJson(projected.registry))) {
    refuse('upstream source differs from the verified authored parent', 'source-parent-mismatch');
  }
  for (const key of ['clips', 'tracks'] as const) {
    const raw = parent.config[key];
    const view = source.config[key];
    if (Array.isArray(raw) && (!Array.isArray(view) || raw.length !== view.length
      || raw.some((row, index) => !object(row) || row.id !== view[index].id)
      || new Set(raw.map((row) => (row as Record<string, unknown>).id)).size !== raw.length)) {
      refuse(`authored ${key} identity changed in projection`, key === 'clips' ? 'source-clip-identity' : 'source-track-identity');
    }
  }
  if (source.bundle !== undefined && !same(parent.config.bundle, source.bundle)) refuse('original authored bundle differs', 'source-bundle-mismatch');
}

export interface TimelineOriginalSaveBasis {
  initial: TimelineCommandBasis;
  source: TimelineSaveSource;
  authoringBundle: AuthoringBundle;
}

/** Read during assembly only; a newer head cannot substitute for the displayed original. */
export async function readTimelineOriginalSaveBasis(
  provider: DataProvider, timelineId: string, input: TimelineSaveSource,
): Promise<TimelineOriginalSaveBasis> {
  const source = structuredClone(input);
  if (!provider.loadTimelineCommandBasis || source.head?.timelineId !== timelineId) {
    refuse('original verified authoring read is unavailable', 'original-read-unavailable');
  }
  const initial = structuredClone(await provider.loadTimelineCommandBasis(timelineId));
  checkHead(initial, source);
  // The existing carrier binds raw physical images and occurrence ownership.
  // It neither executes edits nor invents successor pins.
  const authoringBundle = await authoringBundleFromDocument(initial.canonicalDocument);
  checkSource(initial, source);
  return { initial, source, authoringBundle };
}

/** Parent-only upstream save mapping. Child/occurrence ownership needs its own authored assembly join. */
export function createTimelineLocalSaveHandoff(options: {
  initial: TimelineCommandBasis;
  source: TimelineSaveSource;
  session: LocalSaveSession;
  /** Read the upstream assembly after the session has adopted the complete canonical result. */
  loadHistory?(): Promise<TimelineCommandBasis>;
  adopted(basis: TimelineCommandBasis): { receipt: TimelineSaveReceipt; source: TimelineSaveSource };
}): TimelineLocalSaveHandoff {
  checkHead(options.initial, options.source);
  let initial = structuredClone(options.initial);
  let source = structuredClone(options.source);
  let authoringSource = structuredClone(options.source);
  let document = structuredClone(options.initial.canonicalDocument);
  let sourceChecked = false;
  let targets = historyTargets(options.initial.history, options.initial.head);
  let inversePending = false;

  async function appendInverse(kind: 'undo' | 'redo'): Promise<void> {
    if (!remoteHistoryAvailable()) refuse('durable timeline history is not settled');
    const target = targets[kind].at(-1);
    if (!target) refuse(`no persisted ${kind} target is available`);
    inversePending = true;
    try {
      const before = options.session.getDocument();
      const command: EditCommand = {
        schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
        args: { publications: [target] },
      };
      await options.session.append({ before, after: before,
        label: `${kind === 'undo' ? 'Undo' : 'Redo'} timeline`, commands: [command] });
      await handoff.flush();
    } finally {
      inversePending = false;
    }
  }

  function remoteHistoryAvailable(): boolean {
    return !inversePending && options.session.getState().status === 'saved';
  }
  function changes(raw: unknown, previous: unknown, next: unknown, path: string[]): unknown {
    if (same(previous, next)) return structuredClone(raw);
    if (Array.isArray(previous) && Array.isArray(next) && path.length === 2
      && path[0] === 'config' && ['clips', 'tracks'].includes(path[1])) {
      if (!Array.isArray(raw)) refuse(`authored collection is unavailable: ${path.join('/')}`, 'authored-collection-unavailable');
      const oldRows = new Map(previous.map((row) => [row.id, row]));
      const rawRows = new Map(raw.map((row) => [row.id, row]));
      if (oldRows.size !== previous.length || new Set(next.map((row) => row.id)).size !== next.length
        || previous.some((row) => typeof row.id !== 'string' || !rawRows.has(row.id))
        || rawRows.size !== previous.length) refuse('authored parent entity binding is ambiguous', 'authored-binding-ambiguous');
      return next.map((row) => {
        if (!object(row) || typeof row.id !== 'string' || !row.id) refuse('authored entity identity is unavailable', 'authored-identity-unavailable');
        return oldRows.has(row.id)
          ? changes(rawRows.get(row.id), oldRows.get(row.id), row, [...path, row.id]) : authoredJson(row);
      });
    }
    if (object(previous) && object(next)) {
      if (!object(raw)) refuse(`changed display container has no authored binding: ${path.join('/')}`, 'display-container-unbound');
      const result = structuredClone(raw);
      // The app extension is projected verbatim. Trim removes these authored
      // leaves from an explicitly supplied namespace; other omissions stay partial.
      if (path.length === 5 && path[0] === 'config' && path[1] === 'clips'
        && path[3] === 'app' && path[4] === 'astrid') {
        for (const key of ['for', 'until']) {
          if (!Object.prototype.hasOwnProperty.call(previous, key) || Object.prototype.hasOwnProperty.call(next, key)) continue;
          if (!same(field(raw, key), field(previous, key))) refuse(`trim intent has no exact authored binding: ${[...path, key].join('/')}`, 'trim-binding-mismatch');
          delete result[key];
        }
      }
      // Omission is a partial editor view, not an explicit clear. An unchanged
      // default/undefined never overwrites the raw own key (including null).
      for (const [key, value] of Object.entries(next)) {
        if (same(field(previous, key), value)) continue;
        if (value === undefined) {
          if (key !== 'transition' || path.length !== 3 || path[0] !== 'config' || path[1] !== 'clips') {
            refuse(`explicit clear is unavailable: ${[...path, key].join('/')}`, 'explicit-clear-unavailable');
          }
          delete result[key];
        } else {
          Object.defineProperty(result, key, { value: changes(field(raw, key), field(previous, key), value, [...path, key]),
            enumerable: true, writable: true, configurable: true });
        }
      }
      return result;
    }
    if ((Array.isArray(next) || object(next)) && raw !== undefined && !same(raw, previous)) {
      refuse(`changed display value has no exact authored binding: ${path.join('/')}`, 'display-value-unbound');
    }
    return authoredJson(next);
  }
  const handoff: TimelineLocalSaveHandoff = {
    capture(input, gestureBasis) {
      try {
        const next = structuredClone(input);
        checkHead(initial, source, 'capture-source-head-unavailable');
        checkHead(initial, next, 'capture-input-head-unavailable');
        const before = options.session.getDocument() as unknown as CanonicalDocument;
        const parent = before.parent_revision.payload;
        if (before.shot_revisions.length || before.internal_timeline_revisions.length
          || (Array.isArray(parent.occurrences) && parent.occurrences.length)) refuse('child ownership/fork mapping is unavailable', 'child-ownership-unavailable');
        if (!sourceChecked) { checkSource(initial, source); sourceChecked = true; }
        if (!same(before, document)) refuse('local authored document changed outside this handoff', 'local-document-changed');
        authoredJson(next); // Reject non-finite editor values before mutating the chain.
        const after = structuredClone(before);
        const payload = after.parent_revision.payload;
        payload.config = changes(parent.config, source.config, next.config, ['config']) as Record<string, OutboxJson>;
        payload.registry = changes(parent.registry, source.registry, next.registry, ['registry']) as Record<string, OutboxJson>;
        if (next.bundle !== undefined && !same(source.bundle, next.bundle)) {
          (payload.config as Record<string, OutboxJson>).bundle = authoredJson(next.bundle);
        }
        for (const key of ['clips', 'tracks'] as const) {
          if (!Object.prototype.hasOwnProperty.call(parent, key)) continue;
          if (!same(parent[key], (parent.config as Record<string, unknown>)[key])) refuse(`contradictory parent ${key} mirror`, 'parent-mirror-mismatch');
          payload[key] = (payload.config as Record<string, OutboxJson>)[key];
        }
        let reads: OutboxJson[] | undefined;
        if (gestureBasis) {
          if (!['split', 'trim', 'move'].includes(gestureBasis.kind)
            || !same(authoredJson(gestureBasis.config), authoredJson(authoringSource.config))
            || !same(authoredJson(gestureBasis.registry), authoredJson(authoringSource.registry))) {
            refuse('gesture read basis differs from the original local authoring input', 'gesture-basis-mismatch');
          }
          const config = parent.config as Record<string, unknown>;
          const clips = config.clips;
          if (!Array.isArray(clips)) refuse('gesture clip read has no authored collection', 'gesture-clips-unavailable');
          const selected = clips.filter((clip) => object(clip) && clip.id === gestureBasis.clipId);
          if (selected.length !== 1) refuse('gesture selected clip has no unique authored binding', 'gesture-clip-ambiguous');
          const clip = selected[0] as Record<string, unknown>;
          const read = (value: Record<string, unknown>, key: string, path: string[]): OutboxJson => ({
            kind: 'field', ref: 'parent', path: [...path, key],
            state: Object.prototype.hasOwnProperty.call(value, key)
              ? { state: 'present', value: authoredJson(value[key]) } : { state: 'absent' },
          });
          // Read the nearest missing/null ancestor as such, rather than inventing
          // a leaf under it. Raw defaults stay absent, null and opaque verbatim.
          const readPath = (value: Record<string, unknown>, keys: string[], path: string[]): OutboxJson => {
            const [key, ...rest] = keys;
            return rest.length && object(value[key]) ? readPath(value[key], rest, [...path, key]) : read(value, key, path);
          };
          // recalcActionEnd/getClipTimelineDuration consult these selected fields.
          // Serializing copied rows/tracks is not a read of their entire contents.
          const timingReads = (item: Record<string, unknown>) => ['id', 'track', 'at', 'clipType', 'hold', 'from', 'to', 'speed', 'asset']
            .map((key) => read(item, key, ['config', 'clips', `id:${item.id}`]));
          reads = timingReads(clip);
          reads.push(readPath(config, ['output', 'fps'], ['config']));
          if (!object(config.output) || config.output.fps == null) {
            // withDefaultTimelineOutput falls back to the selected theme canvas.
            reads.push(read(config, 'theme', ['config']), readPath(config, ['theme_overrides', 'visual', 'canvas', 'fps'], ['config']));
          }
          const assetRead = (item: Record<string, unknown>) => {
            if (typeof item.asset !== 'string') return;
            if (!object(parent.registry)) refuse('gesture registry read has no authored registry', 'gesture-registry-unavailable');
            // Runtime/provider normalize parent/registry to config/registry and
            // resolve that path to the top-level raw registry when no mirror exists.
            if (Object.prototype.hasOwnProperty.call(config, 'registry')
              && (!object(config.registry) || !same(config.registry, parent.registry))) refuse('contradictory parent registry mirror', 'registry-mirror-mismatch');
            reads!.push(readPath(parent.registry, ['assets', item.asset], ['config', 'registry']));
          };
          assetRead(clip);
          if (gestureBasis.kind === 'split') {
            if (!Number.isFinite(gestureBasis.timeSeconds)) refuse('split time is unavailable', 'split-time-unavailable');
            // splitClipAtPlayhead uses order for insertion and every ID for allocation;
            // its pinned-group check reads this id-less list, not neighbor contents.
            const order = clips.map((item) => item.id as string);
            reads.push({ kind: 'collection', ref: 'parent', path: ['config', 'clips'], members: [...order].sort(), order },
              read(config, 'pinnedShotGroups', ['config']));
          } else if (gestureBasis.kind === 'move') {
            if (clip.track !== gestureBasis.trackId) refuse('move is not on its original track', 'move-track-mismatch');
            const tracks = config.tracks;
            if (!Array.isArray(tracks)) refuse('move track read has no authored collection', 'move-tracks-unavailable');
            const track = tracks.filter((item) => object(item) && item.id === gestureBasis.trackId);
            if (track.length !== 1) refuse('move track has no unique authored binding', 'move-track-ambiguous');
            reads.push(read(track[0], 'kind', ['config', 'tracks', `id:${gestureBasis.trackId}`]),
              read(config, 'pinnedShotGroups', ['config']));
            // Both snap planners select siblings by track. Guard membership and
            // routing, then timing only for the siblings actually consulted.
            const order = clips.map((item) => item.id as string);
            reads.push({ kind: 'collection', ref: 'parent', path: ['config', 'clips'], members: [...order].sort(), order });
            for (const item of clips) {
              if (!object(item)) refuse('move clip routing is unavailable', 'move-routing-unavailable');
              if (item.id === clip.id) continue;
              reads.push(read(item, 'track', ['config', 'clips', `id:${item.id}`]));
              if (item.track === gestureBasis.trackId) { reads.push(...timingReads(item)); assetRead(item); }
            }
          } else if (!Object.keys(gestureBasis.patch).length
            || Object.keys(gestureBasis.patch).some((key) => !['from', 'to', 'hold', 'speed'].includes(key))) {
            refuse('trim operands are unavailable', 'trim-operands-unavailable');
          }
        }
        // The encoder supplies guards and created IDs; these bytes are never a wire DTO.
        const pending = options.session.appendDocument({ before, after,
          roots: [{ ref: 'parent', revisionId: before.parent_revision.revision_id, contentDigest: before.parent_revision.content_digest }],
          ...(reads === undefined ? {} : { reads, merge: 'fields' as const }),
          label: 'Edit timeline', step: { id: crypto.randomUUID(), label: 'Edit timeline', intent: gestureBasis ? (gestureBasis.kind === 'split'
            ? `Split ${gestureBasis.clipId} at ${gestureBasis.timeSeconds}`
            : gestureBasis.kind === 'move' ? `Move ${gestureBasis.clipId} on ${gestureBasis.trackId}`
              : `Trim ${gestureBasis.clipId}: ${canonicalJsonStringify(gestureBasis.patch)}`) : 'Save local editor changes', tags: [] } });
        source = { ...next,
          config: changes(source.config, source.config, next.config, ['config']) as TimelineConfig,
          registry: changes(source.registry, source.registry, next.registry, ['registry']) as AssetRegistry,
          ...(next.bundle === undefined && source.bundle !== undefined ? { bundle: source.bundle } : {}),
        };
        authoringSource = structuredClone(next);
        document = structuredClone(after);
        return pending;
      } catch (error) {
        return Promise.reject(error instanceof TimelineVersionConflictError ? error
          : new TimelineVersionConflictError(`Local document save retained: ${error instanceof Error ? error.message : String(error)}`));
      }
    },
    async flush() {
      try {
        const basis = await options.session.flush();
        const adopted = options.adopted(basis);
        const head = adopted.receipt.head;
        if (head.projectId !== initial.canonicalDocument.project_id || head.timelineId !== initial.canonicalDocument.timeline_id
          || head.headRevisionId !== basis.head.revisionId || head.headPublicationId !== basis.head.publicationId
          || !same(adopted.source.head, head)) refuse('canonical assembly did not adopt the accepted head');
        initial = structuredClone(basis);
        source = structuredClone(adopted.source);
        authoringSource = structuredClone(adopted.source);
        document = structuredClone(basis.canonicalDocument);
        sourceChecked = false;
        targets = historyTargets(basis.history, basis.head);
        if (options.loadHistory) {
          const latest = await options.loadHistory();
          targets = historyTargets(same(latest.head, basis.head) ? latest.history : undefined, basis.head);
        }
        return adopted.receipt;
      }
      catch (error) {
        if (['blocked', 'conflict', 'error', 'recovery'].includes(options.session.getState().status)) {
          refuse(error instanceof Error ? error.message : String(error));
        }
        throw error;
      }
    },
    remoteHistoryAvailable,
    canUndo: () => remoteHistoryAvailable() && targets.undo.length > 0,
    canRedo: () => remoteHistoryAvailable() && targets.redo.length > 0,
    undo: () => appendInverse('undo'),
    redo: () => appendInverse('redo'),
  };
  return handoff;
}

function historyTargets(history: HistoryPage | undefined, head: TimelineCommandBasis['head']): { undo: string[]; redo: string[] } {
  if (!history?.items?.length || history.next_cursor !== null
    || history.head.revision_id !== head.revisionId || history.head.publication_id !== head.publicationId) return { undo: [], redo: [] };
  // Follow the authoritative ancestry so pagination/display ordering cannot
  // change the target. Unknown and partial-step entries are history barriers.
  const entries = new Map(history.items.map((entry) => [entry.publication_id, entry]));
  const ordered = [];
  const seen = new Set<string>();
  let publication: string | undefined = history.head.publication_id;
  while (publication) {
    if (seen.has(publication)) return { undo: [], redo: [] };
    seen.add(publication);
    const entry = entries.get(publication);
    if (!entry) return { undo: [], redo: [] };
    ordered.push(entry);
    publication = entry.previous?.publication_id;
  }
  const undo: string[] = [];
  const redo: string[] = [];
  for (const entry of ordered.reverse()) {
    if (entry.intent !== 'recorded' || !entry.records || entry.records.undo_steps != null) {
      undo.length = 0;
      redo.length = 0;
      continue;
    }
    const targets = entry.records.undo_of;
    if (!targets.length) {
      undo.push(entry.publication_id);
      redo.length = 0;
    } else if (targets.every((target) => undo.includes(target))) {
      for (const target of targets) undo.splice(undo.lastIndexOf(target), 1);
      redo.push(entry.publication_id);
    } else if (targets.every((target) => redo.includes(target))) {
      for (const target of targets) redo.splice(redo.lastIndexOf(target), 1);
      undo.push(entry.publication_id);
    } else {
      undo.length = 0;
      redo.length = 0;
    }
  }
  return { undo, redo };
}
