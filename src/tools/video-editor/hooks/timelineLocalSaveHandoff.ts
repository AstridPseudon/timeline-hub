import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import type { LocalSaveSession } from '../commands/localSaveSession.ts';
import { toOutboxJson, type OutboxJson } from '../commands/commitOutbox.ts';
import { canonicalJsonStringify, type TimelineBundleEnvelope } from '../data/typed/timelineBundle.ts';
import { authoringBundleFromDocument, type AuthoringBundle } from '../commands/authoringBundle.ts';
import { TimelineVersionConflictError, type DataProvider, type TimelineCommandBasis, type TimelineHeadRevision, type TimelineSaveReceipt } from '../data/DataProvider.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import { canonicalizeTimelinePair } from '../lib/timeline-domain.ts';
import { withDefaultTimelineOutput } from '../lib/defaults.ts';

export interface TimelineSaveSource {
  config: TimelineConfig;
  registry: AssetRegistry;
  bundle?: TimelineBundleEnvelope | null;
  head?: TimelineHeadRevision;
}

/** The split/inspector caller snapshots its input before authoring the local transform. */
export type TimelineGestureReadBasis = {
  config: TimelineConfig;
  registry: AssetRegistry;
  clipId: string;
} & ({ kind: 'split'; timeSeconds: number } | {
  kind: 'trim'; patch: Partial<Pick<TimelineConfig['clips'][number], 'from' | 'to' | 'hold' | 'speed'>>;
});

/** Assembly supplies the ORIGINAL verified read, not loadTimelineCommandBasis at save time. */
export interface TimelineLocalSaveHandoff {
  capture(source: TimelineSaveSource, gestureBasis?: TimelineGestureReadBasis): Promise<void>;
  flush(): Promise<TimelineSaveReceipt>;
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

function refuse(message: string): never {
  throw new TimelineVersionConflictError(`Local document save retained: ${message}`);
}
function checkHead(initial: TimelineCommandBasis, value: TimelineSaveSource) {
  if (!initial.head.revisionId || !initial.head.publicationId
    || initial.canonicalDocument.parent_revision.revision_id !== initial.head.revisionId
    || value.head?.projectId !== initial.canonicalDocument.project_id
    || value.head.timelineId !== initial.canonicalDocument.timeline_id
    || value.head.headRevisionId !== initial.head.revisionId
    || value.head.headPublicationId !== initial.head.publicationId) refuse('original verified authoring head is unavailable');
}
function checkSource(initial: TimelineCommandBasis, source: TimelineSaveSource) {
  const parent = initial.canonicalDocument.parent_revision.payload;
  if (!object(parent.config) || !object(parent.registry)) refuse('authored parent config/registry is unavailable');
  const { bundle: _bundle, ...config } = structuredClone(parent.config);
  const loaded = { ...config, ...withDefaultTimelineOutput(config as unknown as TimelineConfig) } as unknown as TimelineConfig;
  const projected = canonicalizeTimelinePair(loaded, structuredClone(parent.registry) as unknown as AssetRegistry);
  // Accept the original raw view or main's actual load/build view. No arbitrary
  // display snapshot can establish an authored entity binding.
  if ((!same(authoredJson(source.config), authoredJson(loaded))
    && !same(authoredJson(source.config), authoredJson(projected.config)))
    || !same(authoredJson(source.registry), authoredJson(projected.registry))) {
    refuse('upstream source differs from the verified authored parent');
  }
  for (const key of ['clips', 'tracks'] as const) {
    const raw = parent.config[key];
    const view = source.config[key];
    if (Array.isArray(raw) && (!Array.isArray(view) || raw.length !== view.length
      || raw.some((row, index) => !object(row) || row.id !== view[index].id)
      || new Set(raw.map((row) => (row as Record<string, unknown>).id)).size !== raw.length)) {
      refuse(`authored ${key} identity changed in projection`);
    }
  }
  if (source.bundle !== undefined && !same(parent.config.bundle, source.bundle)) refuse('original authored bundle differs');
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
    refuse('original verified authoring read is unavailable');
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
  adopted(basis: TimelineCommandBasis): { receipt: TimelineSaveReceipt; source: TimelineSaveSource };
}): TimelineLocalSaveHandoff {
  let initial = structuredClone(options.initial);
  let source = structuredClone(options.source);
  let authoringSource = structuredClone(options.source);
  let document = structuredClone(options.initial.canonicalDocument);
  let sourceChecked = false;
  function changes(raw: unknown, previous: unknown, next: unknown, path: string[]): unknown {
    if (same(previous, next)) return structuredClone(raw);
    if (Array.isArray(previous) && Array.isArray(next) && path.length === 2
      && path[0] === 'config' && ['clips', 'tracks'].includes(path[1])) {
      if (!Array.isArray(raw)) refuse(`authored collection is unavailable: ${path.join('/')}`);
      const oldRows = new Map(previous.map((row) => [row.id, row]));
      const rawRows = new Map(raw.map((row) => [row.id, row]));
      if (oldRows.size !== previous.length || new Set(next.map((row) => row.id)).size !== next.length
        || previous.some((row) => typeof row.id !== 'string' || !rawRows.has(row.id))
        || rawRows.size !== previous.length) refuse('authored parent entity binding is ambiguous');
      return next.map((row) => {
        if (!object(row) || typeof row.id !== 'string' || !row.id) refuse('authored entity identity is unavailable');
        return oldRows.has(row.id)
          ? changes(rawRows.get(row.id), oldRows.get(row.id), row, [...path, row.id]) : authoredJson(row);
      });
    }
    if (object(previous) && object(next)) {
      if (!object(raw)) refuse(`changed display container has no authored binding: ${path.join('/')}`);
      const result = structuredClone(raw);
      // The app extension is projected verbatim. Trim removes these authored
      // leaves from an explicitly supplied namespace; other omissions stay partial.
      if (path.length === 5 && path[0] === 'config' && path[1] === 'clips'
        && path[3] === 'app' && path[4] === 'astrid') {
        for (const key of ['for', 'until']) {
          if (!Object.prototype.hasOwnProperty.call(previous, key) || Object.prototype.hasOwnProperty.call(next, key)) continue;
          if (!same(field(raw, key), field(previous, key))) refuse(`trim intent has no exact authored binding: ${[...path, key].join('/')}`);
          delete result[key];
        }
      }
      // Omission is a partial editor view, not an explicit clear. An unchanged
      // default/undefined never overwrites the raw own key (including null).
      for (const [key, value] of Object.entries(next)) {
        if (same(field(previous, key), value)) continue;
        if (value === undefined) {
          if (key !== 'transition' || path.length !== 3 || path[0] !== 'config' || path[1] !== 'clips') {
            refuse(`explicit clear is unavailable: ${[...path, key].join('/')}`);
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
      refuse(`changed display value has no exact authored binding: ${path.join('/')}`);
    }
    return authoredJson(next);
  }
  return {
    capture(input, gestureBasis) {
      try {
        const next = structuredClone(input);
        checkHead(initial, source);
        checkHead(initial, next);
        const before = options.session.getDocument() as unknown as CanonicalDocument;
        const parent = before.parent_revision.payload;
        if (before.shot_revisions.length || before.internal_timeline_revisions.length
          || (Array.isArray(parent.occurrences) && parent.occurrences.length)) refuse('child ownership/fork mapping is unavailable');
        if (!sourceChecked) { checkSource(initial, source); sourceChecked = true; }
        if (!same(before, document)) refuse('local authored document changed outside this handoff');
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
          if (!same(parent[key], (parent.config as Record<string, unknown>)[key])) refuse(`contradictory parent ${key} mirror`);
          payload[key] = (payload.config as Record<string, OutboxJson>)[key];
        }
        let reads: OutboxJson[] | undefined;
        if (gestureBasis) {
          if (!['split', 'trim'].includes(gestureBasis.kind)
            || !same(authoredJson(gestureBasis.config), authoredJson(authoringSource.config))
            || !same(authoredJson(gestureBasis.registry), authoredJson(authoringSource.registry))) {
            refuse('gesture read basis differs from the original local authoring input');
          }
          const config = parent.config as Record<string, unknown>;
          const clips = config.clips;
          if (!Array.isArray(clips)) refuse('gesture clip read has no authored collection');
          const selected = clips.filter((clip) => object(clip) && clip.id === gestureBasis.clipId);
          if (selected.length !== 1) refuse('gesture selected clip has no unique authored binding');
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
          reads = ['id', 'track', 'at', 'clipType', 'hold', 'from', 'to', 'speed', 'asset']
            .map((key) => read(clip, key, ['config', 'clips', `id:${gestureBasis.clipId}`]));
          reads.push(readPath(config, ['output', 'fps'], ['config']));
          if (!object(config.output) || config.output.fps == null) {
            // withDefaultTimelineOutput falls back to the selected theme canvas.
            reads.push(read(config, 'theme', ['config']), readPath(config, ['theme_overrides', 'visual', 'canvas', 'fps'], ['config']));
          }
          if (typeof clip.asset === 'string') {
            if (!object(parent.registry)) refuse('gesture registry read has no authored registry');
            // Runtime/provider normalize parent/registry to config/registry and
            // resolve that path to the top-level raw registry when no mirror exists.
            if (Object.prototype.hasOwnProperty.call(config, 'registry')
              && (!object(config.registry) || !same(config.registry, parent.registry))) refuse('contradictory parent registry mirror');
            reads.push(readPath(parent.registry, ['assets', clip.asset], ['config', 'registry']));
          }
          if (gestureBasis.kind === 'split') {
            if (!Number.isFinite(gestureBasis.timeSeconds)) refuse('split time is unavailable');
            // splitClipAtPlayhead uses order for insertion and every ID for allocation;
            // its pinned-group check reads this id-less list, not neighbor contents.
            const order = clips.map((item) => item.id as string);
            reads.push({ kind: 'collection', ref: 'parent', path: ['config', 'clips'], members: [...order].sort(), order },
              read(config, 'pinnedShotGroups', ['config']));
          } else if (!Object.keys(gestureBasis.patch).length
            || Object.keys(gestureBasis.patch).some((key) => !['from', 'to', 'hold', 'speed'].includes(key))) {
            refuse('trim operands are unavailable');
          }
        }
        // The encoder supplies guards and created IDs; these bytes are never a wire DTO.
        const pending = options.session.appendDocument({ before, after,
          roots: [{ ref: 'parent', revisionId: before.parent_revision.revision_id, contentDigest: before.parent_revision.content_digest }],
          ...(reads === undefined ? {} : { reads, merge: 'fields' as const }),
          label: 'Edit timeline', step: { id: crypto.randomUUID(), label: 'Edit timeline', intent: gestureBasis ? (gestureBasis.kind === 'split'
            ? `Split ${gestureBasis.clipId} at ${gestureBasis.timeSeconds}`
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
        console.warn('DEPENDENT DIAGNOSTIC', error);
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
        return adopted.receipt;
      }
      catch (error) {
        if (['blocked', 'conflict', 'error', 'recovery'].includes(options.session.getState().status)) {
          refuse(error instanceof Error ? error.message : String(error));
        }
        throw error;
      }
    },
  };
}
