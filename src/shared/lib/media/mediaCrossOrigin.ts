import { isGatewayUrl } from '@/integrations/runtime/connection';

/**
 * `crossOrigin` attribute value for an `<img>`, `<video>` or canvas source.
 *
 * Only gateway URLs get `'anonymous'`: the gateway authorizes media by the
 * `Origin` header, which a cross-origin element sends only in CORS mode, and
 * it also lets the canvas stay untainted. Same-origin, Supabase, CDN, `data:`
 * and `blob:` URLs return `undefined` so the attribute is not rendered.
 */
export function mediaCrossOrigin(url: string | null | undefined): 'anonymous' | undefined {
  return isGatewayUrl(url) ? 'anonymous' : undefined;
}
