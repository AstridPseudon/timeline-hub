import type {
  CommandRecord,
  DocumentPin,
  EditCommand,
  JSON,
  VerifiedDocument,
} from '@/integrations/runtime/timeline-commit-types.ts';
import {
  canonicalJsonStringify,
  sha256Hex,
} from '../data/typed/timelineBundle.ts';
import {
  projectTranscriptSchema,
  transcriptDocumentId,
  type ProjectTranscriptContent,
} from '../data/typed/projectTranscript.ts';
import { computeHostFingerprint, HOST_GENERATION_PROVENANCE_VERSION } from '@/sdk/video/timeline/sourceMap.ts';
import {
  assertFiniteJson,
  ClipMoveError,
  copy,
  equal,
  freezeJson,
  has,
  MoveRecording,
  object,
  type AuthoredBundle,
} from './clipMovePrimitives.ts';

export const TRANSCRIPT_ASSOCIATE_OPERATION = 'transcript.associate';
export const TRANSCRIPT_SCHEMA_REF = 'astrid.transcript_segment/v1';
export const TRANSCRIPT_REFERENCES_SCHEMA = 'media.transcript.references/v1';

const MEDIA_ID = /^sha256:[0-9a-f]{64}$/;
const EXTENSION_ID = 'haus.astrid.transcript-lane';
const CONTRIBUTION_ID = 'transcript-caption-foundry';
const REVIEW_PREFIX = 'transcript-source-review:';
const CAPTION_TRACK_ID = 'transcript-caption-foundry-track';
const LEGACY_FIELDS = ['transcriptReferences', 'sourceItemsBySchemaRef'] as const;
const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;

type ObjectValue = { [key: string]: JSON };
export type TranscriptAssociateSource = Pick<VerifiedDocument, 'pin' | 'document'>;

type VerifiedTranscript = {
  readonly pin: DocumentPin;
  readonly document: ObjectValue;
  readonly content: ProjectTranscriptContent;
};

export type TranscriptAssociateBasis = Readonly<{
  readonly bundle: AuthoredBundle;
  readonly command: EditCommand;
  readonly document: TranscriptAssociateSource;
  readonly previousDocument?: TranscriptAssociateSource;
}>;

export type TranscriptAssociateResult = {
  readonly command: EditCommand;
  readonly bundle: AuthoredBundle;
  readonly record: CommandRecord;
};

const fail = (message: string, kind = 'invalid_edit_command'): never => {
  throw new ClipMoveError(message, kind);
};

const encodeComponent = (value: string): string => encodeURIComponent(value);

function asObject(value: unknown, message: string): ObjectValue {
  return object(value) ? value : fail(message, 'unsupported_shape');
}

function stringValue(value: unknown, message: string): string {
  return typeof value === 'string' && value.length > 0 ? value : fail(message, 'invalid_source');
}

function exactPin(value: unknown, label: string): DocumentPin {
  const pin = object(value) ? value : fail(`exact transcript ${label} DocumentPin is required`, 'invalid_source');
  if (!equal(Object.keys(pin).sort(), ['content_digest', 'document_id', 'version']) ||
    typeof pin.document_id !== 'string' || !pin.document_id.startsWith('transcript:') ||
    typeof pin.version !== 'number' || !Number.isSafeInteger(pin.version) || pin.version < 1 ||
    typeof pin.content_digest !== 'string' || !MEDIA_ID.test(pin.content_digest)) {
    return fail(`exact transcript ${label} DocumentPin is required`, 'invalid_source');
  }
  return {
    document_id: pin.document_id,
    version: pin.version,
    content_digest: pin.content_digest,
  };
}

function sourceDocument(value: unknown, label: string): ObjectValue {
  const source = asObject(value, `transcript ${label} source must be an object`);
  if (source.kind !== 'media.transcript' || typeof source.project_id !== 'string' ||
    typeof source.document_id !== 'string' || typeof source.version !== 'number' ||
    !Number.isSafeInteger(source.version) || source.version < 1) {
    fail(`transcript ${label} source envelope is unsupported`, 'invalid_source');
  }
  return source;
}

async function verifyTranscript(
  source: TranscriptAssociateSource,
  projectId: string,
  label: string,
): Promise<VerifiedTranscript> {
  assertFiniteJson(source);
  const pin = exactPin(source.pin, label);
  const document = sourceDocument(source.document, label);
  if (document.document_id !== pin.document_id || document.project_id !== projectId ||
    document.version !== pin.version) {
    fail(`transcript ${label} source does not match its exact scoped pin`, 'invalid_source');
  }
  const parsed = projectTranscriptSchema.safeParse(document.content);
  if (!parsed.success || parsed.data === undefined) return fail(`transcript ${label} content is malformed`, 'invalid_source');
  const content = parsed.data;
  if (content.schema !== 'media.transcript/v1' || !MEDIA_ID.test(content.media_id)) {
    fail(`transcript ${label} content identity is unsupported`, 'invalid_source');
  }
  const digest = `sha256:${await sha256Hex(canonicalJsonStringify(content))}`;
  if (digest !== pin.content_digest) fail(`transcript ${label} content does not match its exact pin`, 'invalid_source');
  if (pin.document_id !== await transcriptDocumentId(projectId, content.media_id, content.source_id)) {
    fail(`transcript ${label} document identity is not canonical`, 'invalid_source');
  }
  for (const segment of content.segments) {
    for (const word of segment.words ?? []) {
      if (word.start < segment.start || word.end > segment.end) {
        fail(`transcript ${label} word is outside its segment`, 'invalid_source');
      }
    }
  }
  return { pin, document: copy(document), content };
}

function sourcePrefixes(assetId: string, sourceId: string): { legacy: string; canonical: string } {
  const source = encodeComponent(sourceId);
  return {
    legacy: `transcript-source:${source}:segment:`,
    canonical: `transcript-source:${encodeComponent(assetId)}:source:${source}:segment:`,
  };
}

function captionId(occurrenceId: string): string {
  return `transcript-caption-${computeHostFingerprint(occurrenceId).split(':')[1]}`;
}

function sourceItemRow(value: unknown): ObjectValue {
  const row = asObject(value, 'transcript source item must be an object');
  const owner = asObject(row.sourceArtifactRef, 'transcript source item owner is unsupported');
  const payload = asObject(row.payload, 'transcript source item payload is unsupported');
  const provenance = asObject(row.provenance, 'transcript source item provenance is unsupported');
  if (row.schemaRef !== TRANSCRIPT_SCHEMA_REF || typeof row.id !== 'string' || !row.id ||
    typeof owner.assetId !== 'string' || !owner.assetId || typeof payload.sourceId !== 'string' ||
    !payload.sourceId || payload.segmentId !== row.id || typeof provenance.adapterId !== 'string' ||
    typeof provenance.adapterVersion !== 'string') {
    fail('unsupported transcript source-item envelope', 'unsupported_shape');
  }
  return row;
}

function sourceItemKey(row: ObjectValue): string {
  const owner = asObject(row.sourceArtifactRef, 'transcript source item owner is unsupported');
  const payload = asObject(row.payload, 'transcript source item payload is unsupported');
  return globalThis.JSON.stringify([owner.assetId, payload.sourceId, row.id]);
}

function sourceItemSelection(ctx: MoveRecording, rows: readonly ObjectValue[]): void {
  const keys: string[] = [];
  for (const row of rows) {
    const key = sourceItemKey(row);
    if (keys.includes(key)) fail('ambiguous existing transcript source-item identity', 'identity_conflict');
    keys.push(key);
  }
  ctx.command.selections!.push({
    key: 'transcript.source-items',
    query_version: 1,
    owner: 'parent',
    members: [...keys],
    order: [...keys],
    boundaries: [...keys],
    policy: 'guard-membership',
  });
}

function assertCanonicalCarrier(bundle: AuthoredBundle): void {
  const parent = bundle.parent;
  const config = parent.config === undefined ? undefined : asObject(parent.config, 'parent config must be an object');
  const candidates: unknown[] = [parent, config, parent.bundle];
  for (const candidate of candidates) {
    if (object(candidate) && (has(candidate, LEGACY_FIELDS[0]) || has(candidate, LEGACY_FIELDS[1]))) {
      fail('transcript source planes must use parent.config.bundle', 'unsupported_shape');
    }
  }
  const carrier = config?.bundle;
  if (carrier !== undefined && !object(carrier)) fail('parent.config.bundle must be an object', 'unsupported_shape');
  if (object(carrier) && has(carrier, LEGACY_FIELDS[1])) {
    fail('transcript source items must use persisted itemsBySchemaRef', 'unsupported_shape');
  }
}

function pinValue(pin: DocumentPin): ObjectValue {
  return { document_id: pin.document_id, version: pin.version, content_digest: pin.content_digest };
}

function projectId(bundle: AuthoredBundle): string {
  return stringValue(bundle.project_id, 'authored bundle project identity is missing');
}

function projectItems(source: VerifiedTranscript, assetId: string): ObjectValue[] {
  return source.content.segments.map((segment) => ({
    id: segment.id,
    shape: 'interval',
    domain: 'source_seconds',
    extent: { start: segment.start, end: segment.end },
    schemaRef: TRANSCRIPT_SCHEMA_REF,
    sourceArtifactRef: { assetId },
    provenance: { adapterId: 'astrid.projectTranscript', adapterVersion: '1' },
    payload: {
      sourceId: source.content.source_id,
      segmentId: segment.id,
      text: segment.text,
      ...(segment.speaker !== undefined ? { speaker: segment.speaker } : {}),
      ...(segment.words ? { words: globalThis.JSON.parse(globalThis.JSON.stringify(segment.words)) } : {}),
      documentId: source.pin.document_id,
      documentVersion: source.pin.version,
    },
  }));
}

function identityMapping(
  previous: readonly ObjectValue[],
  incoming: readonly ObjectValue[],
  assetId: string,
  sourceId: string,
): Map<string, string> {
  const scope = sourcePrefixes(assetId, sourceId);
  const belongs = (item: ObjectValue): boolean => {
    const owner = object(item.sourceArtifactRef) ? item.sourceArtifactRef : undefined;
    const payload = object(item.payload) ? item.payload : undefined;
    return item.schemaRef === TRANSCRIPT_SCHEMA_REF && owner?.assetId === assetId && payload?.sourceId === sourceId;
  };
  const previousById = new Map<string, ObjectValue>();
  for (const item of previous) {
    if (!belongs(item)) continue;
    if (previousById.has(String(item.id))) fail('ambiguous prior transcript identity', 'identity_conflict');
    previousById.set(String(item.id), item);
  }
  const mapped = new Map<string, string>();
  const incomingIds = new Set<string>();
  for (const item of incoming) {
    if (!belongs(item)) continue;
    const id = stringValue(item.id, 'incoming transcript item identity is unsupported');
    if (incomingIds.has(id)) fail('ambiguous incoming transcript identity', 'identity_conflict');
    incomingIds.add(id);
    if (!id.startsWith(scope.canonical)) continue;
    const oldId = scope.legacy + id.slice(scope.canonical.length);
    if (!previousById.has(oldId)) continue;
    if ((mapped.has(oldId) && mapped.get(oldId) !== id) || [...mapped.values()].includes(id)) {
      fail('ambiguous transcript identity mapping', 'identity_conflict');
    }
    mapped.set(oldId, id);
  }
  return mapped;
}

function reconcileReferences(
  config: ObjectValue,
  allPrevious: readonly ObjectValue[],
  incoming: readonly ObjectValue[],
  assetId: string,
  sourceId: string,
): ObjectValue {
  const segments = identityMapping(allPrevious, incoming, assetId, sourceId);
  if (segments.size === 0) return config;
  const clips = Array.isArray(config.clips)
    ? config.clips
    : fail('transcript reconciliation clips are unsupported', 'unsupported_shape');

  const owners = new Map<string, Set<string>>();
  for (const item of allPrevious) {
    const payload = object(item.payload) ? item.payload : undefined;
    const owner = object(item.sourceArtifactRef) ? item.sourceArtifactRef : undefined;
    if (item.schemaRef !== TRANSCRIPT_SCHEMA_REF || typeof payload?.sourceId !== 'string' ||
      typeof owner?.assetId !== 'string') continue;
    const ownerKey = globalThis.JSON.stringify([owner.assetId, payload.sourceId]);
    const scope = sourcePrefixes(owner.assetId, payload.sourceId);
    const itemId = typeof item.id === 'string' ? item.id : fail('transcript source item identity is unsupported', 'unsupported_shape');
    const aliases = [itemId];
    if (itemId.startsWith(scope.canonical)) {
      aliases.push(scope.legacy + itemId.slice(scope.canonical.length));
    }
    for (const alias of aliases) {
      const set = owners.get(alias) ?? new Set<string>();
      set.add(ownerKey);
      owners.set(alias, set);
    }
  }

  const mediaSuffixes: string[] = [];
  for (const media of clips) {
    if (!object(media) || media.asset !== assetId || typeof media.id !== 'string') continue;
    mediaSuffixes.push(`@${media.id}`, `@${encodeComponent(media.id)}`);
  }
  const occupied = new Set(clips.flatMap((clip: JSON) => object(clip) && typeof clip.id === 'string' ? [clip.id] : []));
  const nextClips = copy(clips);
  let clipsChanged = false;
  for (const [index, rawClip] of clips.entries()) {
    if (!object(rawClip)) continue;
    const generated = object(rawClip.app) && object(rawClip.app.__generated__) ? rawClip.app.__generated__ : undefined;
    const provenance = object(generated?.provenance) ? generated.provenance : undefined;
    if (rawClip.track !== CAPTION_TRACK_ID || !generated || generated.extensionId !== EXTENSION_ID ||
      generated.contributionId !== CONTRIBUTION_ID || provenance?.sourceSchemaRef !== TRANSCRIPT_SCHEMA_REF ||
      provenance?.contractVersion !== HOST_GENERATION_PROVENANCE_VERSION || typeof provenance?.sourceItemId !== 'string') continue;
    const oldId = provenance.sourceItemId;
    const newId = segments.get(oldId);
    if (!newId) continue;
    const suffixes = [...new Set(mediaSuffixes)];
    if (owners.get(oldId)?.size === 1) suffixes.push('', '@source', '@timeline');
    const matches = suffixes.filter((suffix) => captionId(oldId + suffix) === rawClip.id);
    if (matches.length > 1) fail('ambiguous transcript caption ownership', 'identity_conflict');
    if (matches.length === 0) {
      if ((owners.get(oldId)?.size ?? 0) > 1 && captionId(oldId) === rawClip.id) {
        fail('ambiguous transcript caption ownership', 'identity_conflict');
      }
      continue;
    }
    const nextId = captionId(newId + matches[0]);
    if (occupied.has(nextId)) fail('transcript caption destination is occupied', 'identity_conflict');
    occupied.add(nextId);
    const nextClip = object(nextClips[index]) ? nextClips[index] : fail('transcript caption metadata is unsupported', 'unsupported_shape');
    const nextApp = object(nextClip.app) ? nextClip.app : fail('transcript caption metadata is unsupported', 'unsupported_shape');
    const nextGenerated = object(nextApp.__generated__) ? nextApp.__generated__ : fail('transcript caption metadata is unsupported', 'unsupported_shape');
    const nextProvenance = object(nextGenerated.provenance)
      ? nextGenerated.provenance
      : fail('transcript caption metadata is unsupported', 'unsupported_shape');
    nextClip.id = nextId;
    nextProvenance.sourceItemId = newId;
    clipsChanged = true;
  }

  const extension = object(config.app) && object(config.app[EXTENSION_ID]) ? config.app[EXTENSION_ID] : undefined;
  const nextExtension = extension ? copy(extension) : undefined;
  let reviewsChanged = false;
  if (extension && nextExtension) {
    for (const [oldId, newId] of segments) {
      const ownership = owners.get(oldId)?.size ?? 0;
      const oldKey = REVIEW_PREFIX + encodeComponent(oldId);
      const newKey = REVIEW_PREFIX + encodeComponent(newId);
      const review = extension[oldKey];
      if (ownership > 1 && object(review) && review.schemaVersion === 1 &&
        review.sourceSchemaRef === TRANSCRIPT_SCHEMA_REF && review.sourceItemId === oldId) {
        fail('ambiguous transcript review ownership', 'identity_conflict');
      }
      if (ownership !== 1 || !object(review) || review.schemaVersion !== 1 ||
        review.sourceSchemaRef !== TRANSCRIPT_SCHEMA_REF || review.sourceItemId !== oldId) continue;
      if (has(nextExtension, newKey)) fail('transcript review destination is occupied', 'identity_conflict');
      delete nextExtension[oldKey];
      nextExtension[newKey] = { ...review, sourceItemId: newId };
      reviewsChanged = true;
    }
  }
  if (!clipsChanged && !reviewsChanged) return config;
  const result = copy(config);
  if (clipsChanged) result.clips = nextClips;
  if (reviewsChanged) {
    const app = object(result.app) ? result.app : {};
    app[EXTENSION_ID] = nextExtension!;
    result.app = app;
  }
  return result;
}

function parentAsset(bundle: AuthoredBundle, assetId: string): ObjectValue {
  const parent = bundle.parent;
  const config = parent.config === undefined ? {} : asObject(parent.config, 'parent config must be an object');
  const direct = parent.registry === undefined ? undefined : asObject(parent.registry, 'parent registry is unsupported');
  const nested = config.registry === undefined ? undefined : asObject(config.registry, 'parent config registry is unsupported');
  if (direct && nested && !equal(direct, nested)) fail('parent registry conflicts with parent.config.registry', 'identity_conflict');
  const registry = direct ?? nested;
  const assets = registry && registry.assets !== undefined ? asObject(registry.assets, 'parent asset registry is unsupported') : undefined;
  return object(assets?.[assetId])
    ? assets[assetId]
    : fail('selected transcript asset is missing', 'identity_conflict');
}

function commandArgs(command: EditCommand): ObjectValue {
  const allowed = ['asset_id', 'media_id', 'source_id', 'document', 'previous_document', 'source_schema_ref'];
  if (command.schema_version !== 1 || command.op !== TRANSCRIPT_ASSOCIATE_OPERATION || command.version !== '1' ||
    typeof command.select !== 'string' || !/^parent\/asset:(?!.*::)[^/]+$/.test(command.select) ||
    !object(command.args) || !equal(Object.keys(command.args).sort(), [...allowed].sort()) ||
    command.intent !== undefined && !equal(command.intent, { ownership: 'parent' })) {
    fail('transcript.associate requires the closed parent EditCommand envelope');
  }
  return command.args;
}

function assertClaims(supplied: EditCommand, actual: EditCommand): void {
  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], actual[key])) {
      fail(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
}

function applyTranscriptAssociation(
  bundle: AuthoredBundle,
  supplied: EditCommand,
  source: VerifiedTranscript,
  previousSource: VerifiedTranscript | undefined,
): TranscriptAssociateResult {
  const args = commandArgs(supplied);
  const assetRef = supplied.select!;
  const assetId = assetRef.slice('parent/asset:'.length);
  assertCanonicalCarrier(bundle);
  if (args.asset_id !== assetId || args.source_schema_ref !== TRANSCRIPT_SCHEMA_REF) {
    fail('transcript association asset or source schema differs from its owner', 'identity_conflict');
  }
  const asset = parentAsset(bundle, assetId);
  const mediaId = stringValue(asset.media_id ?? asset.content_sha256, 'selected transcript asset has no media identity');
  const sourceMedia = source.content.media_id;
  const sourceId = source.content.source_id;
  if (args.media_id !== mediaId || sourceMedia !== mediaId || args.source_id !== sourceId) {
    fail('transcript source owner differs from command', 'invalid_source');
  }
  const newPin = exactPin(args.document, 'new');
  if (!equal(newPin, source.pin)) {
    fail('submitted new transcript source does not match its exact pin', 'capture_mismatch');
  }
  const previousPin = args.previous_document === null ? undefined : exactPin(args.previous_document, 'prior');
  if (!equal(previousPin, previousSource?.pin)) fail('prior transcript source does not match its exact pin', 'history_unavailable');

  const ctx = new MoveRecording(bundle, { ...copy(supplied), intent: { ownership: 'parent' } });
  const configValue = ctx.read('parent', ['config']);
  const config = object(configValue) ? configValue : fail('parent config must be an object', 'unsupported_shape');
  const refsState = ctx.state.get('parent', ['config', 'bundle', 'transcriptReferences']);
  const itemsState = ctx.state.get('parent', ['config', 'bundle', 'itemsBySchemaRef']);
  const refsValue = refsState.state === 'absent' ? { schema: TRANSCRIPT_REFERENCES_SCHEMA, associations: [] } : refsState.value;
  const refs = object(refsValue) && refsValue.schema === TRANSCRIPT_REFERENCES_SCHEMA
    ? refsValue
    : fail('transcript reference plane is unsupported', 'unsupported_shape');
  const associations = Array.isArray(refs.associations)
    ? refs.associations
    : fail('transcript reference plane is unsupported', 'unsupported_shape');
  const owners = associations.map((row: JSON) => object(row) ? row.assetId : undefined);
  if (owners.some((owner) => typeof owner !== 'string') || new Set(owners).size !== owners.length ||
    associations.some((row: JSON) => !object(row) || typeof row.documentId !== 'string')) {
    fail('ambiguous transcript association ownership', 'identity_conflict');
  }
  const existing = associations.find((row: JSON): row is ObjectValue => object(row) && row.assetId === assetId);
  if ((existing === undefined && previousPin !== undefined) ||
    (existing !== undefined && (previousPin === undefined || previousPin.document_id !== existing.documentId))) {
    fail('exact prior DocumentPin is required for replacement', 'history_unavailable');
  }
  if (existing !== undefined && previousSource && previousSource.content.media_id !== mediaId) {
    fail('prior transcript source belongs to different media', 'invalid_source');
  }

  const sourceMapValue = itemsState.state === 'absent' ? {} : itemsState.value;
  const sourceMap = object(sourceMapValue)
    ? sourceMapValue
    : fail('transcript source item plane is unsupported', 'unsupported_shape');
  const rawItems = sourceMap[TRANSCRIPT_SCHEMA_REF];
  const oldItems = (Array.isArray(rawItems) ? rawItems : rawItems === undefined ? [] :
    fail('transcript source item collection must be an array', 'unsupported_shape')).map(sourceItemRow);
  const itemKeys = oldItems.map(sourceItemKey);
  if (new Set(itemKeys).size !== itemKeys.length) fail('ambiguous existing transcript source-item identity', 'identity_conflict');

  const projected = projectItems(source, assetId);
  const reconciled = reconcileReferences(config, oldItems, projected, assetId, sourceId);
  sourceItemSelection(ctx, oldItems);
  ctx.read('parent', ['config', 'bundle', 'transcriptReferences']);
  ctx.read('parent', ['config', 'bundle', 'itemsBySchemaRef']);
  ctx.bind('transcript.owner', assetRef);
  for (const row of projected) {
    ctx.bind(`transcript.segment:${row.id}`, assetRef);
    const payload = asObject(row.payload, 'projected transcript source payload is unsupported');
    for (const word of Array.isArray(payload.words) ? payload.words : []) {
      if (object(word) && typeof word.id === 'string') ctx.bind(`transcript.word:${word.id}`, assetRef);
    }
  }
  ctx.dependency('transcript.document', 'transcript', pinValue(source.pin));
  if (previousPin) ctx.dependency('transcript.previous', 'transcript', pinValue(previousPin));

  const retained = oldItems.filter((row) => {
    const owner = asObject(row.sourceArtifactRef, 'transcript source item owner is unsupported');
    const payload = asObject(row.payload, 'transcript source item payload is unsupported');
    const provenance = asObject(row.provenance, 'transcript source item provenance is unsupported');
    const projectTranscript = provenance.adapterId === 'astrid.projectTranscript';
    return !(owner.assetId === assetId && (projectTranscript || payload.sourceId === sourceId));
  });
  const nextRefs = copy(refs);
  nextRefs.associations = associations.filter((row) => object(row) && row.assetId !== assetId);
  nextRefs.associations.push({ assetId, documentId: source.pin.document_id });
  const nextMap = copy(sourceMap);
  nextMap[TRANSCRIPT_SCHEMA_REF] = [...retained, ...projected];

  ctx.object('parent', ['config', 'bundle']);
  ctx.write('parent', ['config', 'bundle', 'transcriptReferences'], nextRefs);
  ctx.write('parent', ['config', 'bundle', 'itemsBySchemaRef'], nextMap);
  if (!equal(config.clips, reconciled.clips)) {
    const primary = ctx.state.bundle.parent.clips;
    const path = Array.isArray(primary) && (primary.length > 0 || !Array.isArray(config.clips) || config.clips.length === 0)
      ? ['clips'] : ['config', 'clips'];
    ctx.write('parent', path, reconciled.clips ?? []);
  }
  const oldExtension = object(config.app) ? config.app[EXTENSION_ID] : undefined;
  const nextExtension = object(reconciled.app) ? reconciled.app[EXTENSION_ID] : undefined;
  if (!equal(oldExtension, nextExtension)) {
    ctx.write('parent', ['config', 'app', EXTENSION_ID], nextExtension ?? null);
  }
  ctx.compile();
  assertClaims(supplied, ctx.command);
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

export async function captureTranscriptAssociation(
  bundle: AuthoredBundle,
  assetId: string,
  document: TranscriptAssociateSource,
  previousDocument?: TranscriptAssociateSource,
): Promise<TranscriptAssociateBasis> {
  assertFiniteJson(bundle);
  assertFiniteJson(assetId);
  const source = await verifyTranscript(document, projectId(bundle), 'new');
  const previousSource = previousDocument ? await verifyTranscript(previousDocument, projectId(bundle), 'prior') : undefined;
  const command: EditCommand = {
    schema_version: 1,
    op: TRANSCRIPT_ASSOCIATE_OPERATION,
    version: '1',
    select: `parent/asset:${assetId}`,
    args: {
      asset_id: assetId,
      media_id: source.content.media_id,
      source_id: source.content.source_id,
      document: pinValue(source.pin),
      previous_document: previousSource ? pinValue(previousSource.pin) : null,
      source_schema_ref: TRANSCRIPT_SCHEMA_REF,
    },
    intent: { ownership: 'parent' },
  };
  const snapshot = copy(bundle);
  const result = applyTranscriptAssociation(snapshot, command, source, previousSource);
  return freezeJson({
    bundle: copy(bundle),
    command: result.command,
    document: { pin: copy(document.pin), document: copy(document.document) },
    ...(previousDocument ? { previousDocument: { pin: copy(previousDocument.pin), document: copy(previousDocument.document) } } : {}),
  });
}

export async function finishTranscriptAssociation(basis: TranscriptAssociateBasis): Promise<TranscriptAssociateResult> {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) || !object(basis.document)) {
    fail('incomplete transcript association basis');
  }
  const source = await verifyTranscript(basis.document, projectId(basis.bundle), 'new');
  const previousSource = basis.previousDocument ? await verifyTranscript(basis.previousDocument, projectId(basis.bundle), 'prior') : undefined;
  return applyTranscriptAssociation(basis.bundle, copy(basis.command), source, previousSource);
}

export async function executeTranscriptAssociation(
  bundle: AuthoredBundle,
  command: EditCommand,
  document: TranscriptAssociateSource,
  previousDocument?: TranscriptAssociateSource,
): Promise<TranscriptAssociateResult> {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  const source = await verifyTranscript(document, projectId(bundle), 'new');
  const previousSource = previousDocument ? await verifyTranscript(previousDocument, projectId(bundle), 'prior') : undefined;
  return applyTranscriptAssociation(bundle, command, source, previousSource);
}
