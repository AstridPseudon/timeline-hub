import { z } from 'zod';

/**
 * What the loopback gateway adds to the Runtime's health answer, shared by the gateway (`scripts/reigh-loopback-gateway.ts`,
 * which writes it) and the hosted page (`RuntimeConnectionProvider`, which reads it), so the two cannot drift.
 *
 * `app_url` is the local Astrid app the launcher serves, `http://127.0.0.1:<app port>`. It is present only when the launcher
 * told the gateway its port; a page that does not see it shows no link to the local app.
 */
export const GATEWAY_APP_URL_PATTERN = /^http:\/\/127\.0\.0\.1:\d{1,5}$/;

export const gatewayHealthSchema = z.object({
  app_url: z.string().regex(GATEWAY_APP_URL_PATTERN).optional(),
}).passthrough();

/** The local app address in a health body, or null when it is absent or not a loopback app address. */
export function appUrlFromHealth(body: unknown): string | null {
  const parsed = gatewayHealthSchema.safeParse(body);
  return parsed.success ? parsed.data.app_url ?? null : null;
}

/** `body` with `app_url` set (an object body only); anything else comes back as it is. */
export function withAppUrl(body: unknown, appUrl: string): unknown {
  if (typeof body !== 'object' || body === null || Array.isArray(body)) return body;
  return gatewayHealthSchema.parse({ ...body, app_url: appUrl });
}
