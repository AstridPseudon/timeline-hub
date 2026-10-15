import type { IncomingHttpHeaders } from 'node:http';
import { ACP_ROUTE_ENTRIES } from '../../src/integrations/astrid/acpRouteContract.ts';
import { PAIRED_CONSUMER_ROUTES, PAIRED_COMPOSE_ROUTE } from './pairedConsumerPolicy.generated.ts';

export const PAIRED_MAX_FRAME_BYTES = 64 * 1024;
// Runtime JSON matches the independently bounded local gateway. This is generic
// transport capacity, not evidence of any historical v8 save's measured size.
export const PAIRED_MAX_JSON_BYTES = 1024 * 1024;
export const PAIRED_MAX_CONTROL_JSON_BYTES = 128 * 1024;
export const PAIRED_MAX_COMPOSE_JSON_BYTES = 64 * 1024;
export const PAIRED_MAX_UPLOAD_BYTES = 64 * 1024 * 1024;
export const PAIRED_REQUEST_TIMEOUT_MS = 30_000;

export type PairedService = 'runtime' | 'astrid' | 'acp' | 'compose';
export interface PairedRoute {
  readonly service: PairedService;
  readonly upstreamPath: string;
  readonly stream: boolean;
}

function pattern(template: string): RegExp {
  return new RegExp(`^${template.split(/(:[A-Za-z]+)/).map(part => part.startsWith(':') ? '[^/?#]+' : part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('')}$`);
}
const routes = [
  ...PAIRED_CONSUMER_ROUTES.map(route => ({ service: route.service, method: route.method, pattern: pattern(route.path), specificity: route.path.replace(/:[A-Za-z]+/g, '').length })),
  ...ACP_ROUTE_ENTRIES.map(route => ({ service: 'acp' as const, method: route.method, pattern: pattern(route.template), specificity: route.template.replace(/:[A-Za-z]+/g, '').length })),
];

export function isSafeForwardPath(path: string): boolean {
  if (!path || path.length > 4096 || !path.startsWith('/') || /[\x00-\x20\x7f#\\]|\/\/|%2f|%5c|%2e|%25|:\/\//i.test(path)) return false;
  if (/%(?![a-f\d]{2})/i.test(path)) return false;
  return !path.split('?', 1)[0].split('/').some(segment => segment === '.' || segment === '..');
}

export function classifyPairedRoute(
  requestPath: string,
  method: string,
  headers: IncomingHttpHeaders | Readonly<Record<string, string | string[] | undefined>> = {},
): PairedRoute | null {
  if (!isSafeForwardPath(requestPath)) return null;
  const normalizedMethod = method.toUpperCase();
  const lengths = Object.entries(headers).filter(([name]) => name.toLowerCase() === 'content-length');
  if (lengths.length > 1 || lengths.some(([, length]) => Array.isArray(length) || (length !== undefined && (!/^\d+$/.test(length) || !Number.isSafeInteger(Number(length)))))) return null;
  if (requestPath === PAIRED_COMPOSE_ROUTE) {
    return normalizedMethod === 'POST' ? { service: 'compose', upstreamPath: requestPath, stream: false } : null;
  }
  const match = /^\/api\/(runtime|astrid)(\/.*)$/.exec(requestPath);
  if (!match) return null;
  const upstreamPath = match[2];
  const service = match[1] === 'astrid' && upstreamPath.startsWith('/acp/') ? 'acp' : match[1];
  const pathname = upstreamPath.split('?', 1)[0];
  if ((service === 'runtime' || service === 'astrid') && ['/v1/tasks/claim', '/v1/projects/selection'].includes(pathname)) return null;
  const candidates = routes.filter(route => route.service === service && route.pattern.test(pathname));
  const specificity = Math.max(...candidates.map(route => route.specificity));
  if (!candidates.some(route => route.specificity === specificity && route.method === normalizedMethod)) return null;
  // Only actual byte routes receive the upload allowance; JSON export receipts
  // and object-location reads never inherit it from a broad prefix match.
  const stream = (service === 'runtime' || service === 'astrid') && (
    (normalizedMethod === 'POST' && /^\/v1\/projects\/[^/]+\/(objects|media-imports)$/.test(pathname))
    || (['GET', 'HEAD'].includes(normalizedMethod) && /^\/v1\/objects\/[^/]+$/.test(pathname))
  );
  return { service: service as PairedService, upstreamPath, stream };
}

// All application headers come from observed generated-client requests. Length
// is HTTP framing; native conditional media reads use the byte response ETag.
export const PAIRED_FORWARD_HEADERS: ReadonlySet<string> = new Set([
  ...PAIRED_CONSUMER_ROUTES.flatMap(route => [...route.headers]),
  'content-length', 'if-none-match', 'if-modified-since',
]);

// Browser/HTTP envelope fields are consumed at the boundary, never tunneled.
const ENVELOPE_HEADERS = new Set([
  'host', 'connection', 'transfer-encoding', 'origin', 'cookie', 'referer',
  'user-agent', 'accept-encoding', 'accept-language', 'cache-control', 'pragma',
  'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site', 'sec-fetch-user',
  'sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform', 'priority', 'dnt',
  'access-control-request-method', 'access-control-request-headers', 'access-control-request-private-network',
]);

/** Unknown application headers cause a refusal, rather than silently widening authority. */
export function hasUnapprovedHeaders(headers: IncomingHttpHeaders): boolean {
  const seen = new Set<string>();
  return Object.entries(headers).some(([name, value]) => {
    const lower = name.toLowerCase();
    if (seen.has(lower)) return true;
    seen.add(lower);
    return value !== undefined && ((!PAIRED_FORWARD_HEADERS.has(lower) && !ENVELOPE_HEADERS.has(lower))
      || Array.isArray(value) || /[\r\n\x00]/.test(value));
  });
}

export function forwardHeaders(headers: IncomingHttpHeaders): Record<string, string> {
  const result: Record<string, string> = {};
  for (const [name, value] of Object.entries(headers)) {
    const lower = name.toLowerCase();
    if (PAIRED_FORWARD_HEADERS.has(lower) && typeof value === 'string' && !/[\r\n\x00]/.test(value)) result[lower] = value;
  }
  return result;
}

export function pairedBodyLimit(route: PairedRoute): number {
  if (route.stream) return PAIRED_MAX_UPLOAD_BYTES;
  if (route.service === 'acp') return PAIRED_MAX_CONTROL_JSON_BYTES;
  if (route.service === 'compose') return PAIRED_MAX_COMPOSE_JSON_BYTES;
  return PAIRED_MAX_JSON_BYTES;
}
