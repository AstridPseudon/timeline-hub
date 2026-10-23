const REDACTED = '[REDACTED]';

export const DIAGNOSTIC_MAX_BYTES = 16 * 1024;
export const DIAGNOSTIC_MAX_DEPTH = 8;
export const DIAGNOSTIC_MAX_KEYS = 40;
export const DIAGNOSTIC_MAX_ARRAY_ITEMS = 40;
export const DIAGNOSTIC_MAX_STRING = 500;
const DIAGNOSTIC_MAX_INPUT_STRING = 4 * 1024;
const DIAGNOSTIC_PRIORITY_MAX_ITEMS = 4;

const SENSITIVE_KEY = /^(?:body|principal|authorization|cookie|set-cookie|x-api-key|api[_-]?key|apikey|access[_-]?token|refresh[_-]?token|id[_-]?token|token|secret|password|credential|client[_-]?secret|private[_-]?key|session)$/i;
const SENSITIVE_ASSIGNMENT = /(["']?)([A-Za-z0-9_-]*(?:body|principal|authorization|cookie|set-cookie|x-api-key|api[_-]?key|apikey|access[_-]?token|refresh[_-]?token|id[_-]?token|token|secret|password|credential|client[_-]?secret|private[_-]?key|session)[A-Za-z0-9_-]*)\1(\s*[:=]\s*)(?:"(?:\\.|[^"\\])*"?|'(?:\\.|[^'\\])*'?|\{[\s\S]*|\[[\s\S]*|[^\s,;}\]]+)/gi;

function truncateUtf8(value: string, maxBytes: number): string {
  const encoded = new TextEncoder().encode(value);
  if (encoded.length <= maxBytes) return value;
  const marker = '…[TRUNCATED]';
  const markerBytes = new TextEncoder().encode(marker).length;
  let prefix = new TextDecoder().decode(encoded.slice(0, Math.max(0, maxBytes - markerBytes)));
  while (new TextEncoder().encode(prefix + marker).length > maxBytes) prefix = prefix.slice(0, -1);
  return prefix + marker;
}

export function redactDiagnosticText(value: string): string {
  const input = value.slice(0, DIAGNOSTIC_MAX_INPUT_STRING);
  const redacted = input
    .replace(/https?:\/\/[^\s"'<>]+/gi, (raw) => {
      try {
        const url = new URL(raw);
        return `${url.origin}${url.pathname}`;
      } catch {
        return '[REDACTED_URL]';
      }
    })
    .replace(/\bBearer\s+[^\s,;]+/gi, 'Bearer [REDACTED]')
    .replace(SENSITIVE_ASSIGNMENT, (_match, openingQuote: string, key: string, separator: string) => (
      `${openingQuote}${key}${openingQuote}${separator}${openingQuote ? `${openingQuote}${REDACTED}${openingQuote}` : REDACTED}`
    ))
    .replace(/([/?][^\s"'<>?]*)\?[^\s"'<>]*/g, '$1[QUERY_REDACTED]')
    .replace(/\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g, '[REDACTED_JWT]');
  return truncateUtf8(redacted, DIAGNOSTIC_MAX_STRING);
}

export type DiagnosticDomObservation = { attached: boolean; visible: boolean };

export function diagnosticObservedVisibility(observations: readonly DiagnosticDomObservation[]): boolean | 'UNKNOWN' {
  if (observations.length !== 1) return 'UNKNOWN';
  const observation = observations[0];
  if (typeof observation.attached !== 'boolean' || typeof observation.visible !== 'boolean') return 'UNKNOWN';
  return observation.attached ? observation.visible : 'UNKNOWN';
}

// Only these diagnostic containers may carry structure. All other allowed fields
// are primitives; a head or ID field can never smuggle a request body or principal.
const DIAGNOSTIC_CONTAINERS = new Set([
  'case', 'basis', 'displayedHead', 'sourceIdentities', 'traffic', 'commits', 'readonly',
  'commitReplies', 'currentWireHeads', 'readonlyReplies', 'head', 'replyHead', 'beforeHead',
  'splitHead', 'agentHead', 'runtimeHistoryHead', 'acceptedHead', 'reads', 'items',
  'outbox', 'outboxes', 'summary', 'records', 'owners', 'pending', 'request', 'outcome',
  'sourceWindow', 'before', 'after', 'sourceIn', 'selectedClip', 'identity',
  'ui', 'errors', 'errorSignals', 'page', 'console', 'requestFailures', 'runtimeResponses',
]);
const DIAGNOSTIC_PRIMITIVES = new Set([
  'title', 'phase', 'projectId', 'projectSlug', 'timelineId', 'sourceId', 'originalClipId', 'rightId',
  'expectedPostCount', 'observedPostCount', 'index', 'key', 'baseRevisionId', 'basePublicationId',
  'merge', 'kind', 'ref', 'path', 'state', 'revisionId', 'publicationId', 'providerProjectId',
  'providerTimelineId', 'historyReadFailed', 'method', 'route', 'status', 'replyReadFailed',
  'readFailed', 'ownerId', 'generation', 'intentCount', 'intentId', 'reason', 'rejected',
  'ownerCount', 'intentLengths', 'pendingIntentLengths', 'outcomeKinds', 'hasIdleOwner',
  'hasPending', 'hasIntents', 'hasConflict', 'value', 'numericValue', 'visible', 'text',
  'data-clip-id', 'data-testid', 'data-state', 'data-selected', 'aria-selected',
  'tagName', 'id', 'clipId', 'testId', 'ariaSelected', 'className',
  'connectionState', 'runtimePanelVisible', 'recoveryVisible', 'recoveryMessage',
  'timelineErrorVisible', 'timelineErrorMessage', 'alertCount', 'type', 'signal', 'message',
  'error', 'count', 'summarized', 'truncated', 'outboxReadFailed', 'selectedTimelineMatchesExpectedId',
  'known', 'capture', 'diagnostic', 'sourceAsset',
]);

function diagnosticPrimitive(value: unknown): unknown {
  if (typeof value === 'string') return redactDiagnosticText(value);
  if (value === null || typeof value === 'boolean') return value;
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  return 'UNKNOWN';
}

const DIAGNOSTIC_HEAD_FIELDS = new Set([
  'head', 'replyHead', 'beforeHead', 'splitHead', 'agentHead', 'runtimeHistoryHead', 'acceptedHead',
]);

function diagnosticHeadFields(value: unknown): unknown {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return 'UNKNOWN';
  const record = value as Record<string, unknown>;
  const identifier = (field: unknown) => typeof field === 'string' && /^[a-z0-9][a-z0-9._:-]{0,159}$/i.test(field)
    ? field : 'UNKNOWN';
  return { revisionId: identifier(record.revisionId), publicationId: record.publicationId === null ? null : identifier(record.publicationId) };
}

export function diagnosticStructure(value: unknown, depth = 0): unknown {
  if (depth >= DIAGNOSTIC_MAX_DEPTH) return 'UNKNOWN';
  if (!value || typeof value !== 'object') return diagnosticPrimitive(value);
  if (Array.isArray(value)) return value.slice(0, DIAGNOSTIC_MAX_ARRAY_ITEMS).map((item) => diagnosticStructure(item, depth + 1));
  const result: Record<string, unknown> = {};
  for (const key of [...DIAGNOSTIC_CONTAINERS, ...DIAGNOSTIC_PRIMITIVES]) {
    try {
      if (!Object.prototype.hasOwnProperty.call(value, key)) continue;
      const field = (value as Record<string, unknown>)[key];
      result[key] = key === 'sourceAsset' ? 'UNKNOWN'
        : DIAGNOSTIC_HEAD_FIELDS.has(key) ? diagnosticHeadFields(field)
        : DIAGNOSTIC_CONTAINERS.has(key) ? diagnosticStructure(field, depth + 1)
        : Array.isArray(field) && ['path', 'intentLengths', 'pendingIntentLengths', 'outcomeKinds', 'known'].includes(key)
          ? field.slice(0, DIAGNOSTIC_MAX_ARRAY_ITEMS).map(diagnosticPrimitive) : diagnosticPrimitive(field);
    } catch {
      result[key] = 'UNKNOWN';
    }
  }
  return result;
}

export function diagnosticListener<Args extends unknown[]>(callback: (...args: Args) => unknown): (...args: Args) => Promise<void> | void {
  return (...args) => {
    try {
      return Promise.resolve(callback(...args)).then(() => {}, () => {});
    } catch {
      // Event diagnostics are disposable, including synchronous getters and rejected thenables.
    }
  };
}

function isSensitiveKey(key: string): boolean {
  return SENSITIVE_KEY.test(key) || /(?:authorization|cookie|token|secret|password|credential|api[_-]?key)/i.test(key);
}

function redactArray(value: unknown[], depth: number): unknown[] {
  const result: unknown[] = [];
  const length = Math.min(value.length, DIAGNOSTIC_MAX_ARRAY_ITEMS);
  for (let index = 0; index < length; index += 1) {
    try {
      result.push(redactDiagnosticValue(value[index], depth + 1));
    } catch {
      result.push('[UNREADABLE]');
    }
  }
  if (value.length > DIAGNOSTIC_MAX_ARRAY_ITEMS) result.push('[TRUNCATED_ARRAY]');
  return result;
}

export function redactDiagnosticValue(value: unknown, depth = 0): unknown {
  if (depth >= DIAGNOSTIC_MAX_DEPTH) return '[REDACTED_DEPTH]';
  if (typeof value === 'string') return redactDiagnosticText(value);
  if (value === null || typeof value === 'boolean' || typeof value === 'number') return value;
  if (typeof value === 'bigint') return '[BIGINT]';
  if (typeof value === 'function' || typeof value === 'symbol' || value === undefined) return '[UNSERIALIZABLE]';

  try {
    if (Array.isArray(value)) return redactArray(value, depth);
  } catch {
    return '[UNREADABLE_ARRAY]';
  }

  const result: Record<string, unknown> = {};
  let visited = 0;
  try {
    for (const key in value as object) {
      if (visited >= DIAGNOSTIC_MAX_KEYS) break;
      visited += 1;
      if (!Object.prototype.hasOwnProperty.call(value, key)) continue;
      if (isSensitiveKey(key)) continue;
      const safeKey = truncateUtf8(redactDiagnosticText(key), DIAGNOSTIC_MAX_STRING);
      try {
        result[safeKey] = redactDiagnosticValue((value as Record<string, unknown>)[key], depth + 1);
      } catch {
        result[safeKey] = '[UNREADABLE]';
      }
    }
  } catch {
    result['[UNREADABLE_KEYS]'] = true;
  }
  return result;
}

export function formatDiagnostic(label: string, value: unknown): string {
  let safeValue: unknown = '[UNREADABLE]';
  try {
    safeValue = redactDiagnosticValue(value);
  } catch {
    // The diagnostic must remain disposable if a proxy/getter is hostile.
  }
  let body = '"[UNSERIALIZABLE]"';
  try {
    body = JSON.stringify(safeValue) ?? 'null';
  } catch {
    // Keep the fallback free of the original value.
  }
  return truncateUtf8(`[${redactDiagnosticText(label)}] ${body}`, DIAGNOSTIC_MAX_BYTES);
}

export type DiagnosticLogger = (message: string) => void;

function priorityRecord(value: unknown, keys: readonly string[]): unknown {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return redactDiagnosticValue(value);
  const result: Record<string, unknown> = {};
  const record = value as Record<string, unknown>;
  for (const key of keys) {
    try {
      if (Object.prototype.hasOwnProperty.call(record, key)) result[key] = redactDiagnosticValue(record[key]);
    } catch {
      result[key] = '[UNREADABLE]';
    }
  }
  return result;
}

function priorityList(value: unknown, transform: (item: unknown) => unknown = redactDiagnosticValue): unknown {
  if (!Array.isArray(value)) return redactDiagnosticValue(value);
  const items = value.slice(0, DIAGNOSTIC_PRIORITY_MAX_ITEMS).map((item) => {
    try {
      return transform(item);
    } catch {
      return '[UNREADABLE]';
    }
  });
  return { count: value.length, items, summarized: true, truncated: value.length > DIAGNOSTIC_PRIORITY_MAX_ITEMS };
}

function priorityReads(value: unknown): unknown {
  if (Array.isArray(value)) {
    const items = value.slice(0, DIAGNOSTIC_MAX_ARRAY_ITEMS).map((item) => priorityRecord(item, ['kind', 'ref', 'path', 'state']));
    return { count: value.length, items, summarized: true, truncated: value.length > DIAGNOSTIC_MAX_ARRAY_ITEMS };
  }
  return redactDiagnosticValue(value);
}

function priorityBasis(value: unknown): unknown {
  if (!Array.isArray(value)) return redactDiagnosticValue(value);
  const items = value.slice(0, DIAGNOSTIC_PRIORITY_MAX_ITEMS).map((item) => {
    const safeRecord = priorityRecord(item, ['index', 'key', 'baseRevisionId', 'basePublicationId', 'merge']);
    if (!safeRecord || typeof safeRecord !== 'object' || Array.isArray(safeRecord)) return safeRecord;
    const record = safeRecord as Record<string, unknown>;
    try {
      if (item && typeof item === 'object' && Object.prototype.hasOwnProperty.call(item, 'reads')) {
        record.reads = priorityReads((item as Record<string, unknown>).reads);
      }
    } catch {
      record.reads = '[UNREADABLE]';
    }
    return record;
  });
  return { count: value.length, items, summarized: true, truncated: value.length > DIAGNOSTIC_PRIORITY_MAX_ITEMS };
}

function priorityOwner(value: unknown): unknown {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return redactDiagnosticValue(value);
  const record = value as Record<string, unknown>;
  const result = priorityRecord(record, ['ownerId', 'generation', 'intentCount', 'acceptedHead']);
  try {
    if (Object.prototype.hasOwnProperty.call(record, 'pending')) {
      const pending = record.pending;
      if (!pending || typeof pending !== 'object' || Array.isArray(pending)) {
        result.pending = redactDiagnosticValue(pending);
      } else {
        const pendingRecord = pending as Record<string, unknown>;
        result.pending = priorityRecord(pendingRecord, ['intentId', 'request', 'outcome']);
        if (pendingRecord.request && typeof pendingRecord.request === 'object' && !Array.isArray(pendingRecord.request)) {
          (result.pending as Record<string, unknown>).request = priorityRecord(pendingRecord.request, ['method', 'path', 'key']);
        }
        if (pendingRecord.outcome && typeof pendingRecord.outcome === 'object' && !Array.isArray(pendingRecord.outcome)) {
          (result.pending as Record<string, unknown>).outcome = priorityRecord(pendingRecord.outcome, ['kind', 'status', 'reason']);
        }
      }
    }
  } catch {
    result.pending = '[UNREADABLE]';
  }
  return result;
}

function priorityOutbox(value: unknown): unknown {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return redactDiagnosticValue(value);
  const record = value as Record<string, unknown>;
  const result = priorityRecord(record, ['readFailed', 'summary']);
  try {
    if (Object.prototype.hasOwnProperty.call(record, 'owners')) {
      result.owners = Array.isArray(record.owners) ? priorityList(record.owners, priorityOwner) : redactDiagnosticValue(record.owners);
    }
  } catch {
    result.owners = '[UNREADABLE]';
  }
  return result;
}

function priorityValue(value: unknown): unknown {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null;
  const record = value as Record<string, unknown>;
  const result: Record<string, unknown> = {};
  let recognized = false;
  const read = (key: string, transform: (field: unknown) => unknown = redactDiagnosticValue) => {
    try {
      if (!Object.prototype.hasOwnProperty.call(record, key)) return;
      recognized = true;
      result[key] = transform(record[key]);
    } catch {
      recognized = true;
      result[key] = '[UNREADABLE]';
    }
  };
  read('case', (field) => priorityRecord(field, [
    'projectId', 'projectSlug', 'timelineId', 'sourceId', 'originalClipId', 'rightId', 'expectedPostCount', 'observedPostCount',
  ]));
  read('basis', priorityBasis);
  read('displayedHead', (field) => priorityRecord(field, [
    'revisionId', 'publicationId', 'providerProjectId', 'providerTimelineId', 'commitReplies', 'currentWireHeads', 'readonlyReplies', 'runtimeHistoryHead', 'historyReadFailed',
  ]));
  read('outbox', priorityOutbox);
  read('sourceWindow', (field) => priorityRecord(field, ['rightId', 'before', 'after']));
  read('ui', (field) => priorityRecord(field, [
    'connectionState', 'runtimePanelVisible', 'recoveryVisible', 'recoveryMessage', 'timelineErrorVisible', 'timelineErrorMessage', 'alertCount',
  ]));
  read('errors', (field) => priorityRecord(field, ['page', 'console', 'requestFailures']));

  if (!recognized) return null;
  if ('displayedHead' in result && result.displayedHead && typeof result.displayedHead === 'object') {
    const displayedHead = result.displayedHead as Record<string, unknown>;
    if (Array.isArray(displayedHead.commitReplies)) {
      displayedHead.commitReplies = priorityList(displayedHead.commitReplies, (item) => priorityRecord(item, ['index', 'head']));
    }
    if (Array.isArray(displayedHead.currentWireHeads)) {
      displayedHead.currentWireHeads = priorityList(displayedHead.currentWireHeads, (item) => priorityRecord(item, [
        'method', 'route', 'key', 'status', 'head', 'replyReadFailed',
      ]));
    }
    if (Array.isArray(displayedHead.readonlyReplies)) {
      displayedHead.readonlyReplies = priorityList(displayedHead.readonlyReplies, (item) => priorityRecord(item, ['route', 'status', 'head']));
    }
  }
  if ('outbox' in result && result.outbox && typeof result.outbox === 'object') {
    const outbox = result.outbox as Record<string, unknown>;
    if ('summary' in outbox) outbox.summary = priorityRecord(outbox.summary, [
      'ownerCount', 'intentLengths', 'pendingIntentLengths', 'outcomeKinds', 'hasIdleOwner', 'hasPending', 'hasIntents', 'hasConflict',
    ]);
  }
  if ('errors' in result && result.errors && typeof result.errors === 'object') {
    const errors = result.errors as Record<string, unknown>;
    for (const key of ['page', 'console', 'requestFailures']) {
      if (key in errors) errors[key] = priorityList(errors[key]);
    }
  }
  return result;
}

export function formatPriorityDiagnostic(label: string, value: unknown): string {
  const prefix = `[${redactDiagnosticText(label)}] `;
  let safeValue: unknown = { diagnostic: 'priority_over_budget' };
  try {
    safeValue = priorityValue(diagnosticStructure(value)) ?? { diagnostic: 'priority_over_budget' };
  } catch {
    // Priority state is best effort and must never affect the assertion.
  }
  let body = '{"diagnostic":"priority_unavailable"}';
  try {
    body = JSON.stringify(safeValue) ?? 'null';
  } catch {
    // Keep the fallback free of the original value.
  }
  const candidate = prefix + body;
  if (new TextEncoder().encode(candidate).length <= DIAGNOSTIC_MAX_BYTES) return candidate;
  return `${prefix}{"diagnostic":"priority_over_budget"}`;
}

export function logDiagnostic(label: string, value: unknown, logger?: DiagnosticLogger): void {
  let message = '[P1 diagnostic unavailable]';
  try {
    message = formatDiagnostic(label, diagnosticStructure(value));
  } catch {
    // Formatting is best effort and must never affect the assertion under test.
  }
  try {
    (logger ?? ((line: string) => console.log(line)))(message);
  } catch {
    try {
      if (!logger) console.log('[P1 diagnostic unavailable]');
    } catch {
      // The final stdout fallback is also best effort.
    }
  }
}

export function logPriorityDiagnostic(label: string, value: unknown, logger?: DiagnosticLogger): void {
  let message = '[P1 priority diagnostic unavailable]';
  try {
    message = formatPriorityDiagnostic(label, value);
  } catch {
    // Formatting is best effort and must never affect the assertion under test.
  }
  try {
    (logger ?? ((line: string) => console.log(line)))(message);
  } catch {
    try {
      if (!logger) console.log('[P1 priority diagnostic unavailable]');
    } catch {
      // The final stdout fallback is also best effort.
    }
  }
}
