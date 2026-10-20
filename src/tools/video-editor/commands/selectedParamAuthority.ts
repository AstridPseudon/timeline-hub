import type { DocumentPin, HeadPin, HistoryEntry, HistoryPage } from '@/integrations/runtime/timeline-commit-types.ts';

type JsonRecord = Record<string, unknown>;
type CapturedHead = HeadPin | { revisionId: string; publicationId: string };
type HistoryInput = HistoryPage | readonly HistoryEntry[];

export type SelectedParamAuthorityFailure = 'history_unavailable' | 'selection_changed';

export class SelectedParamAuthorityError extends Error {
  readonly code: SelectedParamAuthorityFailure;

  constructor(message: string, code: SelectedParamAuthorityFailure = 'history_unavailable') {
    super(message);
    this.name = 'SelectedParamAuthorityError';
    this.code = code;
  }
}

export interface SelectedParamAuthorityInput {
  /** Complete authenticated accepted history, ending at the captured head. */
  history: HistoryInput;
  head?: CapturedHead;
  select: string;
  /** The raw authored clip at the captured head, not a display projection. */
  rawClip: JsonRecord | null | undefined;
}

const isRecord = (value: unknown): value is JsonRecord =>
  value !== null && typeof value === 'object' && !Array.isArray(value);

const same = (left: unknown, right: unknown): boolean => {
  if (Array.isArray(left) || Array.isArray(right)) {
    return Array.isArray(left) && Array.isArray(right) && left.length === right.length
      && left.every((value, index) => same(value, right[index]));
  }
  if (isRecord(left) || isRecord(right)) {
    if (!isRecord(left) || !isRecord(right)) return false;
    const keys = Object.keys(left);
    return keys.length === Object.keys(right).length
      && keys.every((key) => Object.prototype.hasOwnProperty.call(right, key) && same(left[key], right[key]));
  }
  return left === right;
};

function fail(message: string, code: SelectedParamAuthorityFailure = 'history_unavailable'): never {
  throw new SelectedParamAuthorityError(message, code);
}

function headParts(head: CapturedHead | undefined): HeadPin | undefined {
  if (!isRecord(head)) return undefined;
  const value = head as JsonRecord;
  const revisionId = typeof value.revision_id === 'string' ? value.revision_id : value.revisionId;
  const publicationId = typeof value.publication_id === 'string' ? value.publication_id : value.publicationId;
  return typeof revisionId === 'string' && revisionId && typeof publicationId === 'string' && publicationId
    ? { revision_id: revisionId, publication_id: publicationId }
    : undefined;
}

function historyParts(history: HistoryInput, suppliedHead: CapturedHead | undefined) {
  const page = !Array.isArray(history) && isRecord(history) ? history : undefined;
  const items = page?.items ?? history;
  if (!Array.isArray(items)) fail('Selected PARAM accepted history is unavailable; draft preserved');
  if (page && page.next_cursor != null) {
    fail('Selected PARAM accepted history is incomplete; draft preserved');
  }
  const pageHead = headParts(page?.head as CapturedHead | undefined);
  const head = headParts(suppliedHead) ?? pageHead;
  if (!head || (pageHead && !same(head, pageHead))) {
    fail('Selected PARAM accepted history head changed; draft preserved', 'selection_changed');
  }
  return { items: items as readonly HistoryEntry[], head };
}

function orderedEntries(history: HistoryInput, suppliedHead: CapturedHead | undefined): readonly HistoryEntry[] {
  const { items, head } = historyParts(history, suppliedHead);
  const byPublication = new Map<string, HistoryEntry>();
  for (const entry of items) {
    if (!isRecord(entry) || typeof entry.publication_id !== 'string' || !entry.publication_id
      || typeof entry.revision_id !== 'string' || !entry.revision_id || byPublication.has(entry.publication_id)) {
      fail('Selected PARAM accepted history is malformed; draft preserved');
    }
    byPublication.set(entry.publication_id, entry);
  }
  const result: HistoryEntry[] = [];
  const seen = new Set<string>();
  let current: HeadPin | null = head;
  while (current) {
    if (seen.has(current.publication_id)) fail('Selected PARAM accepted history contains a cycle; draft preserved');
    const entry = byPublication.get(current.publication_id);
    if (!entry || entry.revision_id !== current.revision_id) {
      fail('Selected PARAM accepted history has an incomplete predecessor chain; draft preserved');
    }
    seen.add(current.publication_id);
    result.push(entry);
    current = entry.previous;
    if (current !== null && (!isRecord(current) || typeof current.publication_id !== 'string'
      || typeof current.revision_id !== 'string')) {
      fail('Selected PARAM accepted history has a malformed predecessor; draft preserved');
    }
  }
  if (result.length !== items.length) {
    fail('Selected PARAM accepted history contains an unreachable publication; draft preserved');
  }
  return result.reverse();
}

function elementFromClip(rawClip: JsonRecord | null | undefined): JsonRecord | undefined {
  if (!rawClip) return undefined;
  const preferred = isRecord(rawClip.elementRef) && Object.keys(rawClip.elementRef).length
    ? rawClip.elementRef : rawClip.element_ref;
  return isRecord(preferred) ? preferred : undefined;
}

function exactElement(value: unknown): JsonRecord | undefined {
  if (!isRecord(value) || Object.keys(value).length !== 4
    || typeof value.packId !== 'string' || !value.packId
    || typeof value.id !== 'string' || !value.id
    || typeof value.kind !== 'string' || !value.kind
    || typeof value.revision !== 'string' || !value.revision) return undefined;
  return value;
}

function exactDocumentPin(value: unknown): DocumentPin | undefined {
  if (!isRecord(value) || Object.keys(value).length !== 3
    || typeof value.document_id !== 'string' || !value.document_id
    || typeof value.version !== 'number' || !Number.isInteger(value.version) || value.version < 1
    || typeof value.content_digest !== 'string' || !value.content_digest) return undefined;
  return value as unknown as DocumentPin;
}

function exactSnapshotObject(value: unknown): boolean {
  if (!isRecord(value) || Object.keys(value).length !== 4
    || typeof value.object_id !== 'string' || !value.object_id
    || typeof value.digest !== 'string' || value.digest !== value.object_id
    || typeof value.size !== 'number' || !Number.isInteger(value.size) || value.size < 0
    || value.media_type !== 'application/json') return false;
  return true;
}

function directPin(record: JsonRecord, select: string, rawElement: JsonRecord): DocumentPin | undefined {
  const command = isRecord(record.command) ? record.command : undefined;
  if (!command || command.select !== select || (command.op !== 'clip.set-element' && command.op !== 'clip.set-params')) return undefined;
  const args = isRecord(command.args) ? command.args : undefined;
  const schemas = Array.isArray(record.dependencies)
    ? record.dependencies.filter((dependency) => isRecord(dependency) && dependency.key === 'params.schema')
    : [];
  const snapshots = Array.isArray(record.dependencies)
    ? record.dependencies.filter((dependency) => isRecord(dependency) && dependency.key === 'params.snapshot')
    : [];
  const bindings = Array.isArray(record.bindings)
    ? record.bindings.filter((binding) => isRecord(binding) && binding.key === 'params.element')
    : [];
  if (!args || schemas.length !== 1 || snapshots.length !== 1 || bindings.length !== 1
    || !Array.isArray(record.bindings)) return undefined;
  const schema = schemas[0] as JsonRecord;
  const snapshot = snapshots[0] as JsonRecord;
  const binding = bindings[0] as JsonRecord;
  const pin = exactDocumentPin(schema.pin);
  const snapshotPin = isRecord(snapshot.pin) ? snapshot.pin : undefined;
  const snapshotSource = snapshotPin?.source;
  const snapshotElement = exactElement(snapshotPin?.element);
  if (!pin || schema.kind !== 'source' || schema.policy !== 'exact'
    || snapshot.kind !== 'entity' || snapshot.policy !== 'exact'
    || !snapshotPin || Object.keys(snapshotPin).length !== 3
    || !same(snapshotSource, pin) || !snapshotElement || !same(snapshotElement, rawElement)
    || !exactSnapshotObject(snapshotPin.object)
    || binding.ref !== select || binding.policy !== 'fixed'
    || !Array.isArray(binding.dependencies) || !same(binding.dependencies, ['params.schema', 'params.snapshot'])
    || !same(args.schema_source, pin)) return undefined;
  const targetBindings = record.bindings.filter((candidate) => isRecord(candidate) && candidate.key === 'scalar.target');
  const owner = select.slice(0, select.lastIndexOf('/'));
  const ownerBindings = record.bindings.filter((candidate) => isRecord(candidate) && candidate.key === 'scalar.owner');
  const expectedTarget = { key: 'scalar.target', ref: select, policy: 'fixed', dependencies: ['scalar.images'] };
  if (targetBindings.length !== 1 || !same(targetBindings[0], expectedTarget)
    || (owner === 'parent' ? ownerBindings.length !== 0 : ownerBindings.length !== 1
      || !same(ownerBindings[0], { key: 'scalar.owner', ref: owner, policy: 'fixed', dependencies: [] }))) return undefined;
  if (command.op === 'clip.set-params') {
    const reads = Array.isArray(record.reads)
      ? record.reads.filter((read) => isRecord(read) && read.ref === select && Array.isArray(read.path)
        && (same(read.path, ['elementRef']) || same(read.path, ['element_ref'])))
      : [];
    const pathOf = (read: unknown) => isRecord(read) && Array.isArray(read.path) ? read.path : undefined;
    const readElement = reads.find((read) => pathOf(read)?.[0] === 'elementRef')
      ?? reads.find((read) => pathOf(read)?.[0] === 'element_ref');
    const readRecord = readElement as JsonRecord | undefined;
    const state = isRecord(readRecord?.state) ? readRecord.state : undefined;
    if (!state || state.state !== 'present' || !same(state.value, rawElement)) return undefined;
  }
  if (command.op === 'clip.set-element' && !same(args.elementRef, rawElement)) return undefined;
  return pin;
}

function touchesRow(record: JsonRecord, select: string): boolean {
  const command = isRecord(record.command) ? record.command : undefined;
  if (command?.select === select && (command.op === 'clip.set-element' || command.op === 'clip.set-params')) return true;
  if (!Array.isArray(record.writes)) return false;
  return record.writes.some((write) => isRecord(write) && write.ref === select
    && Array.isArray(write.path) && (write.path.length === 0
      || ['params', 'elementRef', 'element_ref'].includes(String(write.path[0]))));
}

function orderedRecords(entry: HistoryEntry): readonly JsonRecord[] {
  if (entry.intent !== 'recorded' || entry.records === null) return [];
  if (!isRecord(entry.records) || !Array.isArray(entry.records.commands)) {
    fail('Selected PARAM accepted record history is malformed; draft preserved');
  }
  const records = entry.records.commands.filter(isRecord);
  if (records.length !== entry.records.commands.length) {
    fail('Selected PARAM accepted record history is malformed; draft preserved');
  }
  const ordinals = records.map((record) => record.ordinal);
  if (ordinals.some((ordinal) => typeof ordinal !== 'number' || !Number.isInteger(ordinal))
    || new Set(ordinals).size !== ordinals.length
    || ordinals.some((ordinal, index) => ordinal !== index)) {
    fail('Selected PARAM accepted record order is unavailable; draft preserved');
  }
  return records;
}

/**
 * Resolve the selected clip's exact retained document pin from accepted history.
 * This is deliberately row-local: it does not inspect manifests, descriptors,
 * catalogs, caches, or authored command payloads other than schema_source.
 */
export function resolveSelectedParamAuthority(input: SelectedParamAuthorityInput): DocumentPin {
  if (!/^(?:parent|occurrence:[^/]+)\/clip:[^/]+$/.test(input.select) || input.select.includes('::')) {
    fail('Selected PARAM raw clip identity is unavailable; draft preserved');
  }
  const rawElement = exactElement(elementFromClip(input.rawClip));
  if (!rawElement) fail('Selected PARAM raw clip element is unavailable; draft preserved');
  const entries = orderedEntries(input.history, input.head);
  let authority: DocumentPin | undefined;
  let established = false;
  for (const entry of entries) {
    if (entry.intent !== 'recorded' || entry.records === null) {
      if (established) fail('Selected PARAM authority is unavailable after legacy history; draft preserved');
      continue;
    }
    for (const record of orderedRecords(entry)) {
      const command = isRecord(record.command) ? record.command : undefined;
      if (command?.op === 'timeline.inverse' || command?.op === 'timeline.restore') {
        if (established) fail('Selected PARAM authority cannot be reconstructed after inverse or restore; draft preserved');
        authority = undefined;
        established = true;
        continue;
      }
      if (!touchesRow(record, input.select)) continue;
      if (command?.select === input.select
        && (command.op === 'clip.set-element' || command.op === 'clip.set-params')) {
        authority = directPin(record, input.select, rawElement);
        established = true;
      } else {
        authority = undefined;
        established = true;
      }
    }
  }
  if (!authority) fail('Selected PARAM authority is unavailable; draft preserved');
  return { ...authority };
}
