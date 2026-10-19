/**
 * Dev-only demo identities and local Supabase defaults.
 *
 * Keep this module free of `import.meta.env` and of React/DOM-typed imports.
 */

/**
 * Canonical identities served by the committed Runtime fixture and printed
 * by `dev:editor`.
 */
export const DEMO_PROJECT_ID = 'demo-project-id';
export const DEMO_TIMELINE_ID = 'demo-timeline';

/**
 * The Supabase URL dev boot paths use when no real one is configured.
 *
 * This is the local `supabase start` convention (`http://127.0.0.1:54321`) —
 * not a fake external domain. The app's env getters are lazy and require the
 * value to exist, so `playwright.config.ts` and `scripts/dev-editor.mjs` supply
 * this one. If a developer is running local Supabase, the app shell's data
 * fetches resolve instead of erroring.
 */
export const DEFAULT_DEV_SUPABASE_URL = 'http://127.0.0.1:54321';

/**
 * Supabase persists its session under `sb-<projectRef>-auth-token`, where the
 * ref is the first hostname label. Derive it rather than hardcoding, so a
 * different `VITE_SUPABASE_URL` still lands on the key the client will read.
 */
export function devSessionStorageKey(supabaseUrl: string): string {
  return `sb-${new URL(supabaseUrl).hostname.split('.')[0]}-auth-token`;
}
