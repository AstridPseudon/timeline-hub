import {
  projectedClipCounterparts,
  serializeProjectedTimelineConfig,
  verifiedRetainedRawClipIds,
} from '@/tools/video-editor/lib/serialize.ts';
import type { DataProvider } from '@/tools/video-editor/data/DataProvider.ts';
import type {
  LoadedTimeline,
} from '@/tools/video-editor/data/DataProvider.ts';
import type {
  MediaSelection,
  MediaSelectionQuery,
  VerifiedMedia,
} from '@/integrations/runtime/generated.ts';
import {
  advanceTimelineDraftBaseAfterAcknowledgement,
  clearTimelineDraftIfMatches,
  loadTimelineDraft,
  reconcileTimelineDraftHeadMarker,
  saveTimelineDraftIfOwner,
  type TimelineDraftRecoveryMetadata,
} from '@/tools/video-editor/data/timelineDraftIndexedDb.ts';
import type {
  PreparedShotComposition,
  ShotCompositionAdapter,
} from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import type { ShotCompositionContract } from '@/tools/video-editor/data/shotComposition.ts';
import { StaleWriteError } from '@/tools/video-editor/data/shotComposition.ts';
import { projectCanonicalComposition } from '@/tools/video-editor/data/shotCompositionProjection.ts';
import { recordShotTimelinePhase } from '@/tools/video-editor/lib/shot-timeline-timing.ts';
import {
  enqueueCanonicalShotPublish,
  hardDurationMs,
  updateCanonicalShotTimeline,
} from '@/tools/video-editor/data/shotCompositionEditor.ts';
import { createLocalSaveSession, type LocalSave, type LocalSaveSession } from '@/tools/video-editor/commands/localSaveSession.ts';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { toOutboxJson, type OutboxJson } from '@/tools/video-editor/commands/commitOutbox.ts';
import type {
  ResolvedAssetRegistryEntry,
  ResolvedTimelineConfig,
  TimelineConfig,
} from '@/tools/video-editor/types/index.ts';
import { timelineContentExtentMs } from '@/tools/video-editor/data/shotCompositionTiming.ts';
import { bridgeMediaUrl } from '@/shared/lib/media/bridgeMediaUrl.ts';
import { assembleTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { buildAssetReferenceMap } from '@/tools/video-editor/lib/asset-registry.ts';

type JsonObject = Record<string, unknown>;

export type ShotTimelineMediaProvider = Pick<DataProvider,
  'supportsDirectAssetUpload'
  | 'prepareMediaImport'
> & {
  getProjectMediaSelection?(query: MediaSelectionQuery): Promise<MediaSelection>;
  getProjectVerifiedMedia?(selection: MediaSelection): Promise<VerifiedMedia>;
};

export function shotTimelineSessionId(
  parentDocumentId: string,
  occurrenceId: string,
  editorSessionToken: string,
): string {
  // Query cache identity is per popup opening; durable recovery has its own
  // stable occurrence key below and is not tied to React Query freshness.
  return `${parentDocumentId}:shot:${occurrenceId}:session:${editorSessionToken}`;
}

export function shotTimelineRecoveryId(parentDocumentId: string, occurrenceId: string): string {
  return `${parentDocumentId}:shot:${occurrenceId}`;
}

export function createShotTimelineEditorSessionToken(): string {
  // Retained as a mount-local diagnostic token; durable recovery identity is
  // deliberately independent of the popup opening.
  return globalThis.crypto?.randomUUID?.() ?? `editor-${Date.now()}`;
}

export type ShotTimelineEditorHeadState = {
  canonicalHeadRevisionId: string | null;
  displayedHeadRevisionId: string | null;
};

function headRevisionIdFromConfig(config: Pick<TimelineConfig, 'app'>): string | null {
  const app = config.app && typeof config.app === 'object' && !Array.isArray(config.app)
    ? config.app as Record<string, unknown>
    : null;
  const canonical = app?.canonicalComposition && typeof app.canonicalComposition === 'object'
    && !Array.isArray(app.canonicalComposition)
    ? app.canonicalComposition as Record<string, unknown>
    : null;
  return typeof canonical?.headRevisionId === 'string' ? canonical.headRevisionId : null;
}

function reconcileConfigHeadRevision(config: TimelineConfig, headRevisionId: string): TimelineConfig {
  const app = config.app && typeof config.app === 'object' && !Array.isArray(config.app)
    ? config.app as Record<string, unknown>
    : null;
  const canonical = app?.canonicalComposition
    && typeof app.canonicalComposition === 'object'
    && !Array.isArray(app.canonicalComposition)
    ? app.canonicalComposition as Record<string, unknown>
    : null;
  if (!app || !canonical || canonical.headRevisionId === headRevisionId) return config;
  return {
    ...config,
    app: {
      ...app,
      canonicalComposition: { ...canonical, headRevisionId },
    },
  };
}

export function shotTimelineDurationSeconds(
  config: Pick<ResolvedTimelineConfig, 'clips'>,
  hardDurationSeconds?: number,
): number {
  const contentSeconds = timelineContentExtentMs({ clips: config.clips }) / 1000;
  return hardDurationSeconds === undefined
    ? contentSeconds
    : Math.min(contentSeconds, Math.max(0, hardDurationSeconds));
}

function createShotTimelineConfig(config: ResolvedTimelineConfig): TimelineConfig {
  return {
    output: config.output,
    clips: config.clips,
    tracks: config.tracks,
    ...(config.theme ? { theme: config.theme } : {}),
    ...(config.theme_overrides ? { theme_overrides: config.theme_overrides } : {}),
    ...(config.generation_defaults ? { generation_defaults: config.generation_defaults } : {}),
    ...(config.app ? { app: config.app } : {}),
  };
}

/** Build first-render editor data from the already-resolved parent projection. */
export function createShotTimelineInitialData(
  config: ResolvedTimelineConfig,
  configVersion = 1,
): TimelineData {
  const registry = {
    assets: Object.fromEntries(Object.entries(config.registry).map(([assetId, entry]) => ([assetId, {
      ...entry,
      file: entry.file ?? entry.media_id ?? entry.url,
    }]))),
  };
  const timelineConfig = createShotTimelineConfig(config);
  return assembleTimelineData({
    config: timelineConfig,
    configVersion,
    registry,
    resolvedConfig: config,
    output: config.output,
    assetMap: buildAssetReferenceMap(registry),
  });
}

function createCanonicalTimeline(config: TimelineConfig, composition: PreparedShotComposition): Record<string, unknown> {
  const retainedRawClipIds = verifiedRetainedRawClipIds(composition);
  for (const clip of config.clips) {
    if (retainedRawClipIds.has(clip.id)) {
      throw new Error(`The shot draft clip ${clip.id} collides with a retained raw clip ID; keep the draft`);
    }
  }
  const counterparts = projectedClipCounterparts(composition, config.clips);
  const clips = (config.clips ?? []).map((clip) => {
    const raw = counterparts.get(clip.id);
    // A clip absent from the verified identity map is a newly authored editor
    // clip (existing projected clips are present with either a raw match or a
    // null value when their identity is ambiguous). Keep it intact so popup
    // add remains a normal authoring operation.
    if (!raw && counterparts.has(clip.id)) {
      throw new Error('The shot draft has no unambiguous raw clip counterpart');
    }
    if (!raw) {
      const { assetEntry: _assetEntry, ...persistedClip } = clip as typeof clip & { assetEntry?: unknown };
      return persistedClip;
    }
    const rawApp = raw.app as Record<string, unknown> | undefined;
    const app = clip.app && typeof clip.app === 'object' && !Array.isArray(clip.app)
      ? { ...clip.app } : clip.app;
    if (app) {
      for (const key of ['canonical', 'canonicalTiming']) {
        if (rawApp && Object.prototype.hasOwnProperty.call(rawApp, key)) {
          Object.defineProperty(app, key, { value: structuredClone(rawApp[key]),
            enumerable: true, configurable: true, writable: true });
        } else Reflect.deleteProperty(app, key);
      }
    }
    const { assetEntry: _assetEntry, ...persistedClip } = clip as typeof clip & { assetEntry?: unknown };
    return {
      ...persistedClip,
      id: String(raw.id),
      ...(app && typeof app === 'object' ? { app } : {}),
    };
  });
  return {
    tracks: config.tracks ?? [],
    clips,
    ...(config.theme ? { theme: config.theme } : {}),
    ...(config.theme_overrides ? { theme_overrides: config.theme_overrides } : {}),
    ...(config.generation_defaults ? { generation_defaults: config.generation_defaults } : {}),
    ...(config.app ? { app: config.app } : {}),
  };
}

function stableStringify(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`;
  if (value !== null && typeof value === 'object') {
    return `{${Object.entries(value as Record<string, unknown>)
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([key, item]) => `${JSON.stringify(key)}:${stableStringify(item)}`)
      .join(',')}}`;
  }
  return JSON.stringify(value);
}

function normalizeHeadForSignature(
  timeline: Record<string, unknown>,
  headRevisionId: string,
): Record<string, unknown> {
  const app = timeline.app && typeof timeline.app === 'object' && !Array.isArray(timeline.app)
    ? timeline.app as Record<string, unknown>
    : null;
  const canonical = app?.canonicalComposition
    && typeof app.canonicalComposition === 'object'
    && !Array.isArray(app.canonicalComposition)
    ? app.canonicalComposition as Record<string, unknown>
    : null;
  if (!app || !canonical) return timeline;
  return {
    ...timeline,
    app: {
      ...app,
      canonicalComposition: { ...canonical, headRevisionId },
    },
  };
}

async function digest(value: unknown): Promise<string> {
  const bytes = new TextEncoder().encode(stableStringify(value));
  const result = await globalThis.crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(result), (byte) => byte.toString(16).padStart(2, '0')).join('');
}

type PendingCanonicalPublication = {
  configSignature: string;
  expectedHeadRevisionId: string;
  idempotencyKey: string;
  graph: ShotCompositionContract;
};

type ShotTimelineDataProvider = DataProvider & {
  getProjectMediaSelection?: (query: MediaSelectionQuery) => Promise<MediaSelection>;
  getProjectVerifiedMedia?: (selection: MediaSelection) => Promise<VerifiedMedia>;
  timelineQueryIdentity: string;
  setPublishCallback: (callback?: (
    composition: PreparedShotComposition,
    generation: number,
    expectedHeadRevisionId: string | null,
  ) => void) => void;
  setDraftState: (dirty: boolean) => void;
  setDraftGeneration: (generation: number) => PreparedShotComposition;
  adoptCleanBaseline: (config: ResolvedTimelineConfig, composition: PreparedShotComposition) => boolean;
  dispose: () => Promise<void>;
};

type PopupLocalSaveProvider = Pick<DataProvider,
  'loadTimelineCommandBasis' | 'getRecoverableIdentity' | 'commitTimeline'>;

function object(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function sameJson(left: unknown, right: unknown): boolean {
  return stableStringify(left) === stableStringify(right);
}

function mergeAuthoredValue(raw: unknown, authored: unknown): unknown {
  if (authored === null || authored === undefined || Array.isArray(authored)
    || typeof authored !== 'object') return authored;
  const rawObject = object(raw);
  const result: Record<string, unknown> = rawObject ? structuredClone(rawObject) : {};
  for (const [key, value] of Object.entries(authored)) {
    result[key] = mergeAuthoredValue(rawObject?.[key], value);
  }
  return result;
}

function registryValue(document: CanonicalDocument, timeline: Record<string, unknown>): unknown {
  if (Object.prototype.hasOwnProperty.call(timeline, 'registry')) return timeline.registry;
  const parent = object(document.parent_revision.payload);
  if (parent && Object.prototype.hasOwnProperty.call(parent, 'registry')) return parent.registry;
  return object(parent?.config)?.registry;
}

function mergeAuthoredRows(
  raw: unknown,
  authored: unknown,
  key: 'clips' | 'tracks',
): OutboxJson[] {
  if (!Array.isArray(raw) || !Array.isArray(authored)) {
    throw new Error(`Popup save requires the verified child ${key} collection`);
  }
  const rawRows = new Map(raw.map((value) => [object(value)?.id, object(value)]));
  const authoredRows = authored.map((value) => object(value));
  if (authoredRows.some((value) => !value || typeof value.id !== 'string')) {
    throw new Error(`Popup ${key} rows require stable authored IDs`);
  }
  return authoredRows.map((value) => {
    const authoredRow = value!;
    const rawRow = rawRows.get(authoredRow.id);
    return toOutboxJson(rawRow
      ? mergeAuthoredValue(rawRow, authoredRow)
      : authoredRow) as OutboxJson;
  });
}

type PopupDocumentEdit = {
  document: CanonicalDocument;
  roots: Array<{ ref: `parent` | `internal-revision:${string}`; revisionId: string; contentDigest: string }>;
};

function popupDocumentAfter(
  before: CanonicalDocument,
  nextConfig: TimelineConfig,
  nextRegistry: unknown,
  composition: PreparedShotComposition,
  occurrenceId: string,
): PopupDocumentEdit {
  const document = structuredClone(before);
  const parent = object(document.parent_revision.payload);
  const occurrences = Array.isArray(parent?.occurrences) ? parent.occurrences : [];
  const occurrence = occurrences.find((value) => object(value)?.occurrence_id === occurrenceId);
  const occurrenceRecord = object(occurrence);
  if (!occurrenceRecord) throw new Error('Popup save has no verified physical occurrence binding');
  const shotId = occurrenceRecord.shot_id;
  const shotRevisionId = occurrenceRecord.shot_revision_id;
  const shot = document.shot_revisions.find((value) => value.shot_id === shotId && value.revision_id === shotRevisionId);
  if (!shot) throw new Error('Popup save has no verified child shot revision binding');
  const shared = occurrences.filter((value) => object(value)?.shot_revision_id === shotRevisionId);
  if (shared.length !== 1) throw new Error('Popup save refuses a shared child revision; use the later copy-on-write A3 seam');
  const internal = document.internal_timeline_revisions.find((value) => value.revision_id === shot.internal_timeline_revision_id);
  if (!internal) throw new Error('Popup save has no verified child timeline root binding');
  const rawTimeline = object(internal.payload);
  if (!rawTimeline) throw new Error('Popup save has no verified raw child timeline');

  // This is the existing graph identity join. It restores raw clip IDs/app
  // collisions from the retained closure instead of guessing from display IDs.
  const authoredTimeline = createCanonicalTimeline(nextConfig, composition);
  const nextTimeline: Record<string, unknown> = {
    ...rawTimeline,
    ...Object.fromEntries(Object.entries(authoredTimeline).filter(([key]) => !['clips', 'tracks'].includes(key))),
    clips: mergeAuthoredRows(rawTimeline.clips, authoredTimeline.clips, 'clips'),
    tracks: mergeAuthoredRows(rawTimeline.tracks, authoredTimeline.tracks, 'tracks'),
  };
  internal.payload = nextTimeline as typeof internal.payload;
  const roots: PopupDocumentEdit['roots'] = [{
    ref: `internal-revision:${internal.revision_id}`,
    revisionId: internal.revision_id,
    contentDigest: internal.content_digest,
  }];
  if (nextRegistry !== undefined && !sameJson(nextRegistry, registryValue(before, rawTimeline))) {
    const parentPayload = object(document.parent_revision.payload);
    const childRegistry = object(rawTimeline.registry);
    if (childRegistry) {
      nextTimeline.registry = mergeAuthoredValue(childRegistry, nextRegistry);
    } else if (parentPayload && Object.prototype.hasOwnProperty.call(parentPayload, 'registry')) {
      parentPayload.registry = mergeAuthoredValue(parentPayload.registry, nextRegistry);
      const config = object(parentPayload.config);
      if (config && Object.prototype.hasOwnProperty.call(config, 'registry')) {
        config.registry = structuredClone(parentPayload.registry);
      }
      roots.push({ ref: 'parent', revisionId: document.parent_revision.revision_id,
        contentDigest: document.parent_revision.content_digest });
    } else {
      const config = object(parentPayload?.config);
      if (!config || !Object.prototype.hasOwnProperty.call(config, 'registry')) {
        throw new Error('Popup asset registry changes lack a verified registry root');
      }
      config.registry = mergeAuthoredValue(config.registry, nextRegistry);
      roots.push({ ref: 'parent', revisionId: document.parent_revision.revision_id,
        contentDigest: document.parent_revision.content_digest });
    }
  }
  return {
    document,
    roots,
  };
}

type PopupPatchChange = Record<string, unknown>;

function tagged(value: unknown, present: boolean): PopupPatchChange {
  return present ? { state: 'present', value: toOutboxJson(value) } : { state: 'absent' };
}

function own(value: Record<string, unknown> | null, key: string): boolean {
  return value !== null && Object.prototype.hasOwnProperty.call(value, key);
}

function collectionRows(value: unknown, path: string[]): Map<string, Record<string, unknown>> {
  if (!Array.isArray(value)) throw new Error(`Popup patch requires an identified collection at ${path.join('/')}`);
  const rows = new Map<string, Record<string, unknown>>();
  for (const item of value) {
    const row = object(item);
    if (!row || typeof row.id !== 'string' || rows.has(row.id)) {
      throw new Error(`Popup patch requires unique row IDs at ${path.join('/')}`);
    }
    rows.set(row.id, row);
  }
  return rows;
}

function appendPopupDiff(
  ref: string,
  oldValue: unknown,
  nextValue: unknown,
  oldPresent: boolean,
  nextPresent: boolean,
  path: string[],
  changes: PopupPatchChange[],
  created: string[],
  owner: string,
  skipRegistryMirror = false,
): void {
  if (oldPresent && nextPresent && sameJson(oldValue, nextValue)) return;
  if (skipRegistryMirror && path[0] === 'config' && path[1] === 'registry') return;
  const identityCollection = (path.length === 1 && (path[0] === 'clips' || path[0] === 'tracks'));
  if (identityCollection) {
    const oldRows = collectionRows(oldValue, path);
    const nextRows = collectionRows(nextValue, path);
    let order = [...oldRows.keys()];
    for (const [id, value] of oldRows) {
      if (nextRows.has(id)) continue;
      changes.push({ op: 'list.remove', ref, path, id, before: tagged(value, true), order_before: [...order] });
      order = order.filter((candidate) => candidate !== id);
    }
    let anchor: string | null = null;
    for (const [id, value] of nextRows) {
      if (!oldRows.has(id)) {
        changes.push({ op: 'list.insert', ref, path, id, before: tagged(undefined, false),
          order_before: [...order], after_id: anchor, value: toOutboxJson(value) });
        order.splice(anchor === null ? 0 : order.indexOf(anchor) + 1, 0, id);
        created.push(`${owner}/${path[0] === 'clips' ? 'clip' : 'track'}:${id}`);
      } else if (order[anchor === null ? 0 : order.indexOf(anchor) + 1] !== id) {
        changes.push({ op: 'list.move', ref, path, id, before: tagged(oldRows.get(id), true),
          order_before: [...order], after_id: anchor });
        order = order.filter((candidate) => candidate !== id);
        order.splice(anchor === null ? 0 : order.indexOf(anchor) + 1, 0, id);
      }
      anchor = id;
    }
    for (const [id, value] of nextRows) {
      if (oldRows.has(id)) appendPopupDiff(ref, oldRows.get(id), value, true, true,
        [...path, `id:${id}`], changes, created, owner, skipRegistryMirror);
    }
    return;
  }
  const oldObject = oldPresent ? object(oldValue) : null;
  const nextObject = nextPresent ? object(nextValue) : null;
  if (oldObject && nextObject) {
    if (path.at(-2) === 'registry' && path.at(-1) === 'assets') {
      for (const key of Object.keys(nextObject)) {
        if (!Object.prototype.hasOwnProperty.call(oldObject, key)) {
          created.push(`${owner}/asset:${key}`);
        }
      }
    }
    for (const key of new Set([...Object.keys(oldObject), ...Object.keys(nextObject)])) {
      appendPopupDiff(ref, oldObject[key], nextObject[key], own(oldObject, key), own(nextObject, key),
        [...path, key], changes, created, owner, skipRegistryMirror);
    }
    return;
  }
  if (path.length === 0) throw new Error(`Popup patch cannot replace the ${ref} payload root`);
  changes.push(nextPresent
    ? { op: 'set', ref, path, before: tagged(oldValue, oldPresent), value: toOutboxJson(nextValue) }
    : { op: 'remove', ref, path, before: tagged(oldValue, oldPresent) });
}

function popupDocumentPatchIntent(
  before: CanonicalDocument,
  edit: PopupDocumentEdit,
  occurrenceId: string,
  label: string,
  step: { id: string; label: string; intent: string; tags: string[] },
): OutboxJson {
  const beforeJson = toOutboxJson(before);
  const afterJson = toOutboxJson(edit.document);
  const beforeShell = structuredClone(before);
  const afterShell = structuredClone(edit.document);
  for (const image of [beforeShell.parent_revision, ...beforeShell.shot_revisions, ...beforeShell.internal_timeline_revisions]) image.payload = {};
  for (const image of [afterShell.parent_revision, ...afterShell.shot_revisions, ...afterShell.internal_timeline_revisions]) image.payload = {};
  if (!sameJson(beforeShell, afterShell)) throw new Error('Popup save changed a canonical wrapper or closure pin');
  const beforeParent = object(before.parent_revision.payload);
  const afterParent = object(edit.document.parent_revision.payload);
  if (!beforeParent || !afterParent || !sameJson(beforeParent.occurrences, afterParent.occurrences)) {
    throw new Error('Popup save changed provider-managed occurrence membership');
  }
  const changes: PopupPatchChange[] = [];
  const created: string[] = [];
  for (const root of edit.roots) {
    const beforeImage = root.ref === 'parent'
      ? before.parent_revision
      : before.internal_timeline_revisions.find((candidate) => candidate.revision_id === root.revisionId);
    const afterImage = root.ref === 'parent'
      ? edit.document.parent_revision
      : edit.document.internal_timeline_revisions.find((candidate) => candidate.revision_id === root.revisionId);
    if (!beforeImage || !afterImage || beforeImage.content_digest !== root.contentDigest
      || afterImage.content_digest !== root.contentDigest) {
      throw new Error('Popup save lost its original physical root binding');
    }
    const logicalRef = root.ref === 'parent' ? 'parent' : `occurrence:${occurrenceId}`;
    const parentPayload = root.ref === 'parent' ? object(beforeImage.payload) : null;
    const skipRegistryMirror = Boolean(parentPayload
      && own(parentPayload, 'registry')
      && own(object(parentPayload.config), 'registry'));
    appendPopupDiff(logicalRef, beforeImage.payload, afterImage.payload, true, true, [], changes, created,
      logicalRef, skipRegistryMirror);
  }
  if (!changes.length) throw new Error('Popup save has no authored changes');
  return toOutboxJson({ kind: 'document-patch-intent', basis: { head: {
    revisionId: before.parent_revision.revision_id, publicationId: 'popup-session-basis',
  } }, before: beforeJson, after: afterJson, roots: edit.roots, label, step, changes, created, merge: 'atomic' });
}

function hasPopupStructuralChange(before: CanonicalDocument, after: CanonicalDocument): boolean {
  const mediaIdentity = (row: Record<string, unknown>): unknown => {
    for (const key of ['asset', 'asset_id', 'source_uuid', 'media_id', 'object_id', 'file']) {
      if (own(row, key)) return row[key];
    }
    return undefined;
  };
  const arraysChanged = (key: 'clips' | 'tracks') => before.internal_timeline_revisions.some((beforeInternal) => {
    const afterInternal = after.internal_timeline_revisions.find((candidate) => (
      candidate.revision_id === beforeInternal.revision_id));
    const oldRows = Array.isArray(object(beforeInternal.payload)?.[key])
      ? (object(beforeInternal.payload)![key] as Array<Record<string, unknown>>).map((row) => row.id)
      : [];
    const nextRows = Array.isArray(object(afterInternal?.payload)?.[key])
      ? (object(afterInternal?.payload)![key] as Array<Record<string, unknown>>).map((row) => row.id)
      : [];
    return !sameJson(oldRows, nextRows);
  });
  const mediaChanged = before.internal_timeline_revisions.some((beforeInternal) => {
    const afterInternal = after.internal_timeline_revisions.find((candidate) => (
      candidate.revision_id === beforeInternal.revision_id));
    const oldRows = object(beforeInternal.payload)?.clips;
    const nextRows = object(afterInternal?.payload)?.clips;
    if (!Array.isArray(oldRows) || !Array.isArray(nextRows)) return false;
    const nextById = new Map(nextRows.map((row) => [object(row)?.id, object(row)]));
    return oldRows.some((row) => {
      const oldRow = object(row);
      const nextRow = oldRow?.id === undefined ? undefined : nextById.get(oldRow.id);
      return oldRow && nextRow && !sameJson(mediaIdentity(oldRow), mediaIdentity(nextRow));
    });
  });
  const beforeParent = object(before.parent_revision.payload);
  const afterParent = object(after.parent_revision.payload);
  const registryChanged = before.internal_timeline_revisions.some((beforeInternal) => {
    const afterInternal = after.internal_timeline_revisions.find((candidate) => (
      candidate.revision_id === beforeInternal.revision_id));
    return !sameJson(object(beforeInternal.payload)?.registry, object(afterInternal?.payload)?.registry);
  });
  return arraysChanged('clips') || arraysChanged('tracks')
    || mediaChanged
    || !sameJson(beforeParent?.registry, afterParent?.registry)
    || registryChanged;
}

/** Ephemeral shot-local geometry projection; it never changes the CAS graph. */
export function projectShotTimelineDraftComposition(
  composition: PreparedShotComposition,
  occurrenceId: string,
  config: ResolvedTimelineConfig,
  rawComposition = composition,
): PreparedShotComposition {
  const occurrence = composition.occurrences.find((candidate) => candidate.occurrenceId === occurrenceId);
  if (!occurrence) return composition;
  const timeline = createCanonicalTimeline(createShotTimelineConfig(config), rawComposition);
  const extentMs = timelineContentExtentMs(timeline);
  const hardLimitMs = hardDurationMs(composition.contract, occurrenceId, occurrence.atMs);
  const revision = occurrence.revision;
  const internal = revision.internal_timeline_revision
    && typeof revision.internal_timeline_revision === 'object'
    && !Array.isArray(revision.internal_timeline_revision)
    ? revision.internal_timeline_revision as JsonObject
    : {};
  return {
    ...composition,
    occurrences: composition.occurrences.map((candidate) => candidate.occurrenceId === occurrenceId
      ? {
        ...candidate,
        durationMs: hardLimitMs === undefined ? extentMs : Math.min(extentMs, hardLimitMs),
        revision: {
          ...revision,
          internal_timeline_revision: { ...internal, timeline },
        },
      }
      : candidate),
  };
}

/** DataProvider bridge for the shot-local popup's canonical CAS publication. */
export function createShotTimelineDataProvider(
  config: ResolvedTimelineConfig,
  composition: PreparedShotComposition,
  occurrenceId: string,
  shotCompositionAdapter?: ShotCompositionAdapter,
  onCanonicalCompositionPublished?: (
    composition: PreparedShotComposition,
    generation: number,
    expectedHeadRevisionId: string | null,
  ) => void,
  editorHeadState?: { current: ShotTimelineEditorHeadState },
  initialDraftGeneration = 0,
  mediaProvider?: ShotTimelineMediaProvider,
  timelineDataProvider?: PopupLocalSaveProvider,
): ShotTimelineDataProvider {
  let registry: { assets: Record<string, ResolvedAssetRegistryEntry> } = {
    assets: Object.fromEntries(Object.entries(config.registry).map(([assetId, entry]) => ([assetId, {
      ...entry,
      file: entry.file ?? entry.media_id ?? entry.url,
    }]))),
  };
  const resolve = async (file: string): Promise<string> => {
    const entry = Object.values(registry.assets).find((candidate) => (
      candidate.file === file || candidate.media_id === file || candidate.url === file
    ));
    // Canonical projection has already resolved managed object IDs into src.
    // Prefer that display address over the persisted file/media identity so
    // opaque sha256: references never reach <img>/<video> as a request URL.
    if (entry?.src) return entry.src;
    if (entry?.url) return entry.url;
    return file.startsWith('sha256:')
      ? bridgeMediaUrl(composition.projectId, file)
      : file;
  };
  let timelineConfig = createShotTimelineConfig(config);
  let canonicalTimelineConfig = timelineConfig;
  let configVersion = 1;
  // This is the CAS base for the mounted popup session. Never reload here:
  // doing so would turn a stale local draft into an unconditional write over
  // a concurrent canonical head. Advance the base only after its publication
  let canonicalBase = composition;
  const editorHeadStateIsMounted = editorHeadState !== undefined;
  const activeEditorHeadState = editorHeadState ?? {
    current: {
      canonicalHeadRevisionId: composition.headRevisionId,
      displayedHeadRevisionId: headRevisionIdFromConfig(config),
    },
  };
  activeEditorHeadState.current.canonicalHeadRevisionId = composition.headRevisionId;
  const adoptCanonicalBase = (next: PreparedShotComposition, advanceDisplayedHead = false) => {
    canonicalBase = next;
    activeEditorHeadState.current.canonicalHeadRevisionId = next.headRevisionId;
    if (!editorHeadStateIsMounted || advanceDisplayedHead) {
      activeEditorHeadState.current.displayedHeadRevisionId = next.headRevisionId;
    }
  };
  const assertEditorHeadIsCurrent = () => {
    const { canonicalHeadRevisionId, displayedHeadRevisionId } = activeEditorHeadState.current;
    if (canonicalHeadRevisionId
      && displayedHeadRevisionId !== canonicalHeadRevisionId) {
      throw new StaleWriteError(
        'The shot timeline is still adopting the latest canonical revision; retry after the displayed shot updates.',
      );
    }
  };
  const recoveryKey = shotTimelineRecoveryId(composition.parentDocumentId, occurrenceId);
  let timelineQueryIdentity = composition.headRevisionId;
  let pendingPublication: PendingCanonicalPublication | null = null;
  let activeTimingTraceId: string | null = null;
  let publishCallback = onCanonicalCompositionPublished;
  let draftGeneration = initialDraftGeneration;
  let draftDirty = false;
  let pendingPublishes = 0;
  let localSaveSessionPromise: Promise<LocalSaveSession> | undefined;
  const localSaveEnabled = Boolean(
    timelineDataProvider?.loadTimelineCommandBasis
      && timelineDataProvider.getRecoverableIdentity
      && timelineDataProvider.commitTimeline,
  );
  if (timelineDataProvider && !localSaveEnabled) {
    throw new Error('Popup A2 save requires the existing command-basis, identity, and commit transport seam');
  }
  if (localSaveEnabled) {
    localSaveSessionPromise = (async () => {
      const [initial, identity] = await Promise.all([
        timelineDataProvider!.loadTimelineCommandBasis!(composition.parentDocumentId),
        timelineDataProvider!.getRecoverableIdentity!(),
      ]);
      if (initial.head.revisionId !== composition.headRevisionId
        || initial.canonicalDocument.project_id !== composition.projectId
        || initial.canonicalDocument.timeline_id !== composition.parentDocumentId) {
        throw new Error('Popup A2 save requires the original verified canonical closure');
      }
      return createLocalSaveSession({
        scope: { ...identity, projectId: composition.projectId, timelineId: composition.parentDocumentId },
        initial,
        document: toOutboxJson(initial.canonicalDocument),
        send: (request, key) => timelineDataProvider!.commitTimeline!(request, key),
        loadLatest: () => timelineDataProvider!.loadTimelineCommandBasis!(composition.parentDocumentId),
        changed: () => {},
        prepareDisplay: async (basis) => ({ document: toOutboxJson(basis.canonicalDocument), adopt: () => {} }),
      });
    })();
  }

  const provider: ShotTimelineDataProvider = {
    get timelineQueryIdentity() {
      return timelineQueryIdentity;
    },
    persistenceEnabled: Boolean(shotCompositionAdapter?.publish || localSaveEnabled),
    ...(mediaProvider?.supportsDirectAssetUpload !== undefined
      ? { supportsDirectAssetUpload: mediaProvider.supportsDirectAssetUpload }
      : {}),
    ...(mediaProvider?.prepareMediaImport
      ? { prepareMediaImport: mediaProvider.prepareMediaImport.bind(mediaProvider) }
      : {}),
    ...(mediaProvider?.getProjectMediaSelection
      ? { getProjectMediaSelection: mediaProvider.getProjectMediaSelection.bind(mediaProvider) }
      : {}),
    ...(mediaProvider?.getProjectVerifiedMedia
      ? { getProjectVerifiedMedia: mediaProvider.getProjectVerifiedMedia.bind(mediaProvider) }
      : {}),
    setShotTimelineTraceId: (traceId) => { activeTimingTraceId = traceId; },
    getTimelineDraftRecoveryMetadata: (rememberRaw): TimelineDraftRecoveryMetadata => {
      rememberRaw?.(composition);
      return {
        recoveryKey,
        baseHeadRevisionId: canonicalBase.headRevisionId,
        baseCanonicalGraph: canonicalBase.contract as unknown as Record<string, unknown>,
        draftIdentity: globalThis.crypto?.randomUUID?.() ?? `edit-${Date.now()}-${Math.random()}`,
      };
    },
    resolveAssetUrl: resolve,
    onResolve: async ({ file }) => resolve(file),
    loadTimeline: async (_timelineId) => {
      timelineConfig = canonicalTimelineConfig;
      const recovery = await loadTimelineDraft(recoveryKey).catch(() => null);
      let recoveryBaseHeadRevisionId: string | null = null;
      if (recovery?.baseCanonicalGraph && shotCompositionAdapter) {
        try {
          const recoveredBase = shotCompositionAdapter.prepare(recovery.baseCanonicalGraph);
          if (recoveredBase.headRevisionId === recovery.baseHeadRevisionId) {
            const recoveryBaseIsCurrent = recoveredBase.headRevisionId === canonicalBase.headRevisionId;
            // A recovery base is CAS provenance, not proof that it is still the
            // current canonical head. Only adopt its displayed marker when it
            // matches the provider's latest known base; never rewrite a stale
            // draft's original CAS revision here.
            composition = recoveredBase;
            adoptCanonicalBase(recoveredBase, recoveryBaseIsCurrent);
            if (recoveryBaseIsCurrent) {
              recoveryBaseHeadRevisionId = recoveredBase.headRevisionId;
            }
          }
        } catch {
          // A malformed recovery base is not authority; keep the fresh graph.
        }
      }
      if (recoveryBaseHeadRevisionId && recovery?.draftIdentity) {
        // Keep the durable draft's marker aligned with the validated base.
        // Retry reads the one-slot record again, so an in-memory-only repair
        // here would let it rehydrate the stale marker and hit the edit gate.
        await reconcileTimelineDraftHeadMarker(
          recoveryKey,
          recovery.draftIdentity,
          recoveryBaseHeadRevisionId,
        ).catch(() => false);
      }
      const recoveredConfig = recovery?.draft.config;
      if (recoveredConfig && typeof recoveredConfig === 'object' && !Array.isArray(recoveredConfig)) {
        timelineConfig = recoveryBaseHeadRevisionId
          ? reconcileConfigHeadRevision(recoveredConfig as TimelineConfig, recoveryBaseHeadRevisionId)
          : recoveredConfig as TimelineConfig;
      }
      if (recoveredConfig) {
        const identities = projectCanonicalComposition(composition, undefined, { clampToOccurrenceDuration: false }).clipIdentities;
        timelineConfig = { ...timelineConfig, clips: timelineConfig.clips.map((clip) => {
          const identity = identities.get(clip.id);
          const original = composition.occurrences.find((item) => item.occurrenceId === identity?.occurrenceId);
          return original ? { ...clip, app: { ...clip.app, canonicalTiming: {
            ...(clip.app?.canonicalTiming as object), storedOccurrenceDurationMs: original.durationMs,
          } } } : clip;
        }) };
      }
      const savedPublication = recovery?.draft.canonicalPublication;
      if (savedPublication && typeof savedPublication === 'object' && !Array.isArray(savedPublication)) {
        const candidate = savedPublication as Record<string, unknown>;
        if (typeof candidate.configSignature === 'string'
          && typeof candidate.expectedHeadRevisionId === 'string'
          && typeof candidate.idempotencyKey === 'string'
          && candidate.graph && typeof candidate.graph === 'object' && !Array.isArray(candidate.graph)) {
          pendingPublication = {
            configSignature: candidate.configSignature,
            expectedHeadRevisionId: candidate.expectedHeadRevisionId,
            idempotencyKey: candidate.idempotencyKey,
            graph: candidate.graph as unknown as ShotCompositionContract,
          };
        }
      }
      return { config: timelineConfig, configVersion };
    },
    loadCanonicalTimeline: async (_timelineId): Promise<LoadedTimeline> => {
      if (shotCompositionAdapter) {
        const latest = await shotCompositionAdapter.load({
          projectId: composition.projectId,
          parentDocumentId: composition.parentDocumentId,
        });
        if (!latest) throw new Error('The canonical shot composition is unavailable');
        composition = latest;
        adoptCanonicalBase(latest);
        timelineQueryIdentity = latest.headRevisionId;
        const occurrence = latest.occurrences.find((candidate) => candidate.occurrenceId === occurrenceId);
        if (!occurrence) throw new Error('The canonical shot occurrence is unavailable');
        const projected = projectCanonicalComposition(
          { ...latest, occurrences: [occurrence] },
          { ...canonicalTimelineConfig, clips: [], tracks: [], registry: {} },
          { clampToOccurrenceDuration: false },
        ).config;
        const offsetSeconds = occurrence.atMs / 1000;
        const canonicalResolvedConfig = {
          ...projected,
          clips: projected.clips.map((clip) => {
            const app = clip.app && typeof clip.app === 'object' && !Array.isArray(clip.app) ? clip.app : null;
            const timing = app?.canonicalTiming && typeof app.canonicalTiming === 'object'
              && !Array.isArray(app.canonicalTiming) ? app.canonicalTiming : null;
            return {
              ...clip,
              at: Math.max(0, clip.at - offsetSeconds),
              ...(app && timing
                ? { app: { ...app, canonicalTiming: { ...timing, occurrenceStartMs: 0 } } }
                : {}),
            };
          }),
        };
        registry = {
          assets: Object.fromEntries(Object.entries(canonicalResolvedConfig.registry).map(([assetId, entry]) => ([assetId, {
            ...entry,
            file: entry.file ?? entry.media_id ?? entry.url,
          }]))),
        };
        canonicalTimelineConfig = createShotTimelineConfig(canonicalResolvedConfig);
      }
      timelineConfig = canonicalTimelineConfig;
      pendingPublication = null;
      return { config: timelineConfig, configVersion };
    },
    loadAssetRegistry: async () => registry,
    saveTimeline: async (timelineId, nextConfig, expectedVersion, nextRegistry) => {
      const publicationGeneration = draftGeneration;
      const rawComposition = composition;
      const draftRegistry = nextRegistry ?? registry;
      assertEditorHeadIsCurrent();
      if (localSaveEnabled) {
        if (!shotCompositionAdapter) throw new Error('Popup A2 save requires the validated canonical composition adapter');
        const session = await localSaveSessionPromise!;
        const before = session.getDocument() as unknown as CanonicalDocument;
        const edit = popupDocumentAfter(
          before,
          nextConfig,
          nextRegistry && !sameJson(nextRegistry, registry) ? draftRegistry : undefined,
          rawComposition,
          occurrenceId,
        );
        const step = {
          id: globalThis.crypto?.randomUUID?.() ?? `popup-edit-${Date.now()}`,
          label: 'Edit shot timeline',
          intent: 'Save shot-local timeline changes',
          tags: ['shot-popup'],
        };
        if (hasPopupStructuralChange(before, edit.document)) {
          const intent = popupDocumentPatchIntent(before, edit, occurrenceId, 'Edit shot timeline', step);
          const intentObject = intent as unknown as Record<string, unknown>;
          const command = {
            schema_version: 1 as const,
            op: 'doc.patch',
            version: '1',
            select: null,
            created: intentObject.created,
            args: { changes: intentObject.changes },
          };
          await session.append({
            before: toOutboxJson(before),
            after: toOutboxJson(edit.document),
            label: 'Edit shot timeline',
            commands: [command] as never,
            documentIntent: intent,
          } as LocalSave & { documentIntent: OutboxJson });
        } else {
          await session.appendDocument({
            before,
            after: edit.document,
            roots: edit.roots,
            label: 'Edit shot timeline',
            step,
          });
        }
        const basis = await session.flush();
        if (!basis.graph) throw new Error('Popup A2 save received no accepted canonical closure');
        const published = shotCompositionAdapter.prepare(basis.graph);
        if (!published.occurrences.some((value) => value.occurrenceId === occurrenceId)) {
          throw new Error('Popup A2 save received a canonical closure without the edited occurrence');
        }
        adoptCanonicalBase(published, true);
        composition = published;
        canonicalTimelineConfig = nextConfig;
        timelineConfig = nextConfig;
        registry = {
          assets: Object.fromEntries(Object.entries(draftRegistry.assets).map(([assetId, entry]) => {
            const previous = registry.assets[assetId];
            return [assetId, {
              ...previous,
              ...entry,
              file: entry.file ?? entry.media_id ?? entry.url,
              src: (entry as typeof entry & { src?: string }).src
                ?? previous?.src ?? entry.url ?? entry.file ?? entry.media_id ?? '',
            }];
          })),
        };
        pendingPublication = null;
        publishCallback?.(published, publicationGeneration, before.parent_revision.revision_id);
        configVersion += 1;
        return configVersion;
      }
      if (!shotCompositionAdapter?.publish) {
        throw new Error('The canonical shot-composition provider is read-only');
      }
      pendingPublishes += 1;
      const requestedAt = import.meta.env.DEV ? performance.now() : 0;
      const timingTraceId = activeTimingTraceId;
      let publicationExpectedHeadRevisionId: string | null = null;
      if (timingTraceId) recordShotTimelinePhase(timingTraceId, 'request-start', { expectedVersion });
      try {
        const timeline = createCanonicalTimeline(nextConfig, rawComposition);
        // Reserve the project queue synchronously in caller order before any
        // async recovery read or hashing. Otherwise a later edit can finish
        // preparation first and publish ahead of the save that was requested
        // before it.
        const published = await enqueueCanonicalShotPublish(
          composition.projectId,
          composition.parentDocumentId,
          async () => {
            // The queued publication may have waited behind another shot edit
            // while the mounted popup adopted a newer head. Recheck at the
            // actual write boundary, not just when the UI requested the save.
            assertEditorHeadIsCurrent();
            // Another edit can become durable while this publication hashes
            // and prepares its graph, so owner comparison and write below are
            // still transactional.
            const recoveryAtStart = await loadTimelineDraft(recoveryKey).catch(() => null);
            const configSignature = await digest(normalizeHeadForSignature(timeline, canonicalBase.headRevisionId));
            let candidate = pendingPublication?.configSignature === configSignature
              ? pendingPublication
              : null;
            if (!candidate) {
              const identitySeed = (await digest({
                projectId: canonicalBase.projectId,
                parentDocumentId: canonicalBase.parentDocumentId,
                occurrenceId,
                expectedHeadRevisionId: canonicalBase.headRevisionId,
                configSignature,
              })).slice(0, 32);
              const graph = await updateCanonicalShotTimeline(
                canonicalBase.contract,
                occurrenceId,
                timeline,
                identitySeed,
              );
              candidate = {
                configSignature,
                expectedHeadRevisionId: canonicalBase.headRevisionId,
                idempotencyKey: `astrid.shot-popup.${identitySeed}`,
                graph,
              };
              pendingPublication = candidate;
            }
            publicationExpectedHeadRevisionId = candidate.expectedHeadRevisionId;
            const recoveryDraftConfig = recoveryAtStart?.draft.config;
            const recoveryMatchesThisSave = Boolean(
              recoveryAtStart?.draftIdentity
              && recoveryDraftConfig
              && typeof recoveryDraftConfig === 'object'
              && !Array.isArray(recoveryDraftConfig)
              && await digest(normalizeHeadForSignature(
                createCanonicalTimeline(recoveryDraftConfig as TimelineConfig, rawComposition),
                canonicalBase.headRevisionId,
              )) === configSignature,
            );
            const expectedRecoveryOwner = recoveryAtStart === null
              ? null
              : recoveryMatchesThisSave
                ? recoveryAtStart.draftIdentity!
                // A different durable config is newer than this save or has
                // no trustworthy owner token. Force the conflict-merge path;
                // never adopt its owner token and overwrite its config.
                : `superseded:${candidate.idempotencyKey}`;
            const publicationDraft = {
              ...(recoveryAtStart?.draft ?? {}),
              // Existing recovery bytes keep their owner and retry meaning.
              config: recoveryMatchesThisSave ? recoveryAtStart!.draft.config
                : serializeProjectedTimelineConfig(nextConfig, rawComposition),
              registry: draftRegistry,
              canonicalPublication: candidate,
            };
            await saveTimelineDraftIfOwner(
              timelineId,
              publicationDraft,
              expectedVersion,
              {
                recoveryKey,
                baseHeadRevisionId: candidate.expectedHeadRevisionId,
                baseCanonicalGraph: canonicalBase.contract as unknown as Record<string, unknown>,
                draftIdentity: candidate.idempotencyKey,
                acknowledgementIdentity: candidate.idempotencyKey,
              },
              expectedRecoveryOwner,
              (current, candidateRecord) => ({
                ...current,
                // Keep B's config/base/owner, but make A's exact publication
                // candidate available as a retry without making A the owner.
                draft: {
                  ...current.draft,
                  canonicalPublication: candidateRecord.draft.canonicalPublication,
                },
              }),
            );
            const publishStartedAt = import.meta.env.DEV ? performance.now() : 0;
            const acknowledged = await shotCompositionAdapter.publish!({
              projectId: canonicalBase.projectId,
              parentDocumentId: canonicalBase.parentDocumentId,
              expectedHeadRevisionId: candidate.expectedHeadRevisionId,
              graph: candidate.graph,
              idempotencyKey: candidate.idempotencyKey,
              timingTraceId: timingTraceId ?? undefined,
            });
            // This head is our own acknowledged publication. The mounted
            // editor contains that saved revision plus any newer local edits,
            // so it can continue on the new CAS base without waiting for a
            // redundant query echo to rewrite its head marker.
            adoptCanonicalBase(acknowledged, true);
            canonicalTimelineConfig = nextConfig;
            timelineConfig = canonicalTimelineConfig;
            pendingPublication = null;
            const clearedAcknowledgedDraft = await clearTimelineDraftIfMatches(
              recoveryKey,
              candidate.idempotencyKey,
            ).catch(() => false);
            if (!clearedAcknowledgedDraft) {
              await advanceTimelineDraftBaseAfterAcknowledgement(
                recoveryKey,
                candidate.expectedHeadRevisionId,
                acknowledged.headRevisionId,
                acknowledged.contract as unknown as Record<string, unknown>,
                candidate.idempotencyKey,
              ).catch(() => false);
            }
            if (import.meta.env.DEV) {
              console.debug('[ShotTimelineLatency]', {
                phase: 'canonical-publish-ack',
                occurrenceId,
                queueWaitMs: Math.round(publishStartedAt - requestedAt),
                publishMs: Math.round(performance.now() - publishStartedAt),
              });
            }
            if (timingTraceId) recordShotTimelinePhase(timingTraceId, 'canonical-ack', {
              headRevisionId: acknowledged.headRevisionId,
            });
            return acknowledged;
          },
        );
        if (timingTraceId) recordShotTimelinePhase(timingTraceId, 'request-end', {
          durationMs: Math.round(performance.now() - requestedAt),
        });
        // A publication can finish after React has rendered a newer callback.
        // Keep the callback current without rebuilding the editor's provider.
        publishCallback?.(published, publicationGeneration, publicationExpectedHeadRevisionId);
        configVersion += 1;
        return configVersion;
      } finally {
        pendingPublishes -= 1;
      }
    },
    setPublishCallback: (callback) => { publishCallback = callback; },
    setDraftState: (dirty) => { draftDirty = dirty; },
    setDraftGeneration: (generation) => { draftGeneration = Math.max(draftGeneration, generation); return composition; },
    adoptCleanBaseline: (nextConfig, nextComposition) => {
      if (draftDirty || pendingPublishes > 0) {
        return false;
      }
      timelineConfig = createShotTimelineConfig(nextConfig);
      canonicalTimelineConfig = timelineConfig;
      registry = {
        assets: Object.fromEntries(Object.entries(nextConfig.registry).map(([assetId, entry]) => ([assetId, {
          ...entry,
          file: entry.file ?? entry.media_id ?? entry.url,
        }]))),
      };
      composition = nextComposition;
      adoptCanonicalBase(nextComposition);
      timelineQueryIdentity = nextComposition.headRevisionId;
      return true;
    },
    dispose: async () => {
      await localSaveSessionPromise?.then((session) => session.dispose());
    },
  };
  return provider;
}
