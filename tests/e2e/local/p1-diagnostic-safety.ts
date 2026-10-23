const REDACTED = '[REDACTED]';

export const DIAGNOSTIC_MAX_BYTES = 16 * 1024;
export const DIAGNOSTIC_MAX_DEPTH = 8;
export const DIAGNOSTIC_MAX_KEYS = 40;
export const DIAGNOSTIC_MAX_ARRAY_ITEMS = 40;
export const DIAGNOSTIC_MAX_STRING = 500;
const DIAGNOSTIC_MAX_INPUT_STRING = 4 * 1024;

const SENSITIVE_KEY = /^(?:authorization|cookie|set-cookie|x-api-key|api[_-]?key|apikey|access[_-]?token|refresh[_-]?token|id[_-]?token|token|secret|password|credential|client[_-]?secret|private[_-]?key|session)$/i;
const SENSITIVE_ASSIGNMENT = /(["']?)([A-Za-z0-9_-]*(?:authorization|cookie|set-cookie|x-api-key|api[_-]?key|apikey|access[_-]?token|refresh[_-]?token|id[_-]?token|token|secret|password|credential|client[_-]?secret|private[_-]?key|session)[A-Za-z0-9_-]*)\1(\s*[:=]\s*)(?:"(?:\\.|[^"\\])*"?|'(?:\\.|[^'\\])*'?|\{[\s\S]*|\[[\s\S]*|[^\s,;}\]]+)/gi;

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

export function formatPriorityDiagnostic(label: string, value: unknown): string {
  const prefix = `[${redactDiagnosticText(label)}] `;
  let safeValue: unknown = { diagnostic: 'priority_unavailable' };
  try {
    safeValue = redactDiagnosticValue(value);
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
    message = formatDiagnostic(label, value);
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
