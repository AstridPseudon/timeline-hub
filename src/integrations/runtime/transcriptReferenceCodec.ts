/**
 * Explicit carrier relocation only. No store, revision, command, or ID work.
 * Association keys and complete values are opaque here: D's shared
 * media.transcript/v1 helper owns record validation and document identity.
 */
type JsonValue = null | boolean | number | string | JsonObject | readonly JsonValue[];
type JsonObject = { readonly [key: string]: JsonValue };
export type TranscriptReferenceIndex = Readonly<Record<string, JsonObject>>;
export type TranscriptReferencePresence =
  | { readonly present: false }
  | { readonly present: true; readonly value: TranscriptReferenceIndex };

export type TranscriptReferenceRefusal = {
  readonly ok: false;
  readonly reason: 'malformed-envelope' | 'malformed-carrier' | 'malformed-version'
    | 'unsupported-version' | 'conflicting-carriers';
  readonly path: string;
};
export type TranscriptReferenceReadResult = TranscriptReferenceRefusal | {
  readonly ok: true;
  readonly references: TranscriptReferencePresence;
  readonly carriers: { readonly legacy: boolean; readonly nested: boolean };
};
export type TranscriptReferenceMigrationResult =
  | (TranscriptReferenceRefusal & { readonly value: unknown })
  | {
    readonly ok: true;
    readonly changed: boolean;
    readonly value: Record<string, unknown>;
    readonly references: TranscriptReferencePresence;
  };

const own = (value: object, key: PropertyKey): boolean =>
  Object.prototype.hasOwnProperty.call(value, key);
const legacyPath = 'transcriptReferences';
const nestedPath = 'config.app.transcript.references';
const versionPath = 'config.app.transcript.v';

function record(value: unknown): value is Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

// Reject values that JSON would silently omit/coerce. No accepted opaque member
// is discarded for comparison. This is a carrier check, not a transcript schema.
function jsonValue(value: unknown, ancestors = new Set<object>()): value is JsonValue {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return true;
  if (typeof value === 'number') return Number.isFinite(value);
  if (typeof value !== 'object' || (!Array.isArray(value) && !record(value))) return false;
  if (ancestors.has(value)) return false;
  ancestors.add(value);
  const keys = Reflect.ownKeys(value);
  let valid = true;
  if (Array.isArray(value)) {
    // Dense JSON arrays only; order and every element remain significant.
    valid = keys.length === value.length + 1;
    for (let index = 0; valid && index < value.length; index += 1) {
      const descriptor = Object.getOwnPropertyDescriptor(value, String(index));
      valid = !!descriptor && descriptor.enumerable === true && 'value' in descriptor
        && jsonValue(descriptor.value, ancestors);
    }
  } else {
    for (const key of keys) {
      const descriptor = Object.getOwnPropertyDescriptor(value, key)!;
      if (typeof key !== 'string' || !descriptor.enumerable || !('value' in descriptor)
        || !jsonValue(descriptor.value, ancestors)) {
        valid = false;
        break;
      }
    }
  }
  ancestors.delete(value);
  return valid;
}

function index(value: unknown): value is TranscriptReferenceIndex {
  return record(value) && jsonValue(value) && Object.values(value).every(record);
}

// Equality ignores object insertion order only. Arrays, IDs, provenance, and
// unknown fields all participate. This is not another canonical JSON/hash codec.
function equal(left: JsonValue, right: JsonValue): boolean {
  if (Object.is(left, right)) return true;
  if (Array.isArray(left) || Array.isArray(right)) {
    return Array.isArray(left) && Array.isArray(right) && left.length === right.length
      && left.every((value, position) => equal(value, right[position]));
  }
  if (!record(left) || !record(right)) return false;
  const keys = Object.keys(left);
  return keys.length === Object.keys(right).length
    && keys.every((key) => own(right, key) && equal(left[key] as JsonValue, right[key] as JsonValue));
}

function copy(value: JsonValue): JsonValue {
  if (Array.isArray(value)) return value.map(copy);
  if (record(value)) return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, copy(item as JsonValue)]));
  return value;
}

function refuse(reason: TranscriptReferenceRefusal['reason'], path: string): TranscriptReferenceRefusal {
  return { ok: false, reason, path };
}

/**
 * Dual-read without mutation. The envelope is a parsed JSON document containing
 * a config object. Both carriers are object indexes of explicit association keys
 * to opaque objects. Arrays/scalars/null are not indexes or clear sentinels.
 * An own empty index is an explicit clear, distinct from an absent property.
 * A clear competing with a populated index refuses instead of losing intent.
 * No transcript record or stable document ID is constructed/validated here.
 */
export function readTranscriptReferences(input: unknown): TranscriptReferenceReadResult {
  if (!record(input)) return refuse('malformed-envelope', '$');
  let config: Record<string, unknown> = {};
  let app: Record<string, unknown> = {};
  let transcript: Record<string, unknown> = {};
  if (own(input, 'config')) {
    if (!record(input.config)) return refuse('malformed-envelope', 'config');
    config = input.config;
  }
  if (own(config, 'app')) {
    if (!record(config.app)) return refuse('malformed-envelope', 'config.app');
    app = config.app;
  }
  if (own(app, 'transcript')) {
    if (!record(app.transcript)) return refuse('malformed-envelope', 'config.app.transcript');
    transcript = app.transcript;
  }
  const carriers = { legacy: own(input, legacyPath), nested: own(transcript, 'references') };
  if (own(transcript, 'v')) {
    if (typeof transcript.v !== 'number' || !Number.isInteger(transcript.v) || transcript.v < 1) {
      return refuse('malformed-version', versionPath);
    }
    if (transcript.v !== 1) return refuse('unsupported-version', versionPath);
  } else if (carriers.nested) {
    return refuse('malformed-version', versionPath);
  }
  const legacy = input[legacyPath];
  const nested = transcript.references;
  if (carriers.legacy && !index(legacy)) return refuse('malformed-carrier', legacyPath);
  if (carriers.nested && !index(nested)) return refuse('malformed-carrier', nestedPath);
  if (!carriers.legacy && !carriers.nested) {
    return { ok: true, references: { present: false }, carriers };
  }
  const oldIndex = carriers.legacy ? legacy as TranscriptReferenceIndex : undefined;
  const newIndex = carriers.nested ? nested as TranscriptReferenceIndex : undefined;
  if (oldIndex && newIndex) {
    if ((Object.keys(oldIndex).length === 0) !== (Object.keys(newIndex).length === 0)) {
      return refuse('conflicting-carriers', nestedPath);
    }
    for (const key of Object.keys(oldIndex)) {
      if (own(newIndex, key) && !equal(oldIndex[key], newIndex[key])) {
        return refuse('conflicting-carriers', `${nestedPath}[${JSON.stringify(key)}]`);
      }
    }
  }
  const merged = { ...oldIndex, ...newIndex };
  return {
    ok: true, carriers,
    references: { present: true, value: copy(merged) as TranscriptReferenceIndex },
  };
}

/**
 * Explicit opt-in only. A refusal returns the exact original input; success
 * copies the modified envelope layers. Unrelated/foreign data is retained.
 * The caller owns any authorized command/journal integration; no automatic
 * load/save/read/replay/publish invocation belongs in this codec.
 */
export function migrateTranscriptReferencesV1(input: unknown): TranscriptReferenceMigrationResult {
  const decoded = readTranscriptReferences(input);
  if (!decoded.ok) return { ...decoded, value: input };
  const root = input as Record<string, unknown>;
  if (!decoded.carriers.legacy || !decoded.references.present) {
    return { ok: true, changed: false, value: root, references: decoded.references };
  }
  const config = root.config as Record<string, unknown> | undefined;
  const app = config?.app as Record<string, unknown> | undefined;
  const transcript = app?.transcript as Record<string, unknown> | undefined;
  const { transcriptReferences: _legacy, ...rest } = root;
  return {
    ok: true, changed: true, references: decoded.references,
    value: {
      ...rest,
      config: {
        ...config,
        app: {
          ...app,
          transcript: { ...transcript, v: 1, references: copy(decoded.references.value) },
        },
      },
    },
  };
}
