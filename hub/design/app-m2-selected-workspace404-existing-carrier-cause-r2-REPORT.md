# App HOME response: selected18585 workspace-config boundary

## Actionable source witness

The `workspace.json` 404 is a selected-wrapper handoff mismatch, but it is
not proven causal for the failed mount.

Origin/main's existing authoritative producer is
`scripts/runtime-discovery-proxy.mjs:79-105,404-416`: it reads Runtime's
published `discovery.json`, validates the Astrid product credential/realm/
identity, and serves `GET /runtime-config/v1/workspace.json`. Runtime itself
publishes `discovery.json`; it does not own this `/runtime-config/...` route.

Normal `scripts/dev-local-workspace.mjs:553-580,672-681` starts that proxy and
sets `VITE_WORKSPACE_RUNTIME_URL` to the proxy port. Selected18585 instead
uses `tests/e2e/local/support/harness.ts:717-732`: it starts Vite directly,
sets `VITE_WORKSPACE_RUNTIME_URL` to `this.runtimeUrl` (`:720`, the direct
Runtime port), and does not set `ASTRID_WORKSPACE_DISCOVERY` or start the
discovery proxy. Current `config/vite/vite.config.ts:89-98,123-128` forwards
the workspace path unchanged, so the captured request reaches Runtime and
gets 404. If DEV parity is required, the smallest existing runner-only fix is
to reuse/spawn the discovery proxy and target Vite at it; no new route/DTO/
authority or product fallback is justified. No patch was applied.

## Causality and first pending dependency

The preserved selected trace shows:

- original 20-second `#root > *` assertion failed before P1;
- shell remained `Loading project` with empty `main`;
- workspace request at `42843.954` returned 404 at `42851.789`;
- later same-frame `/api/astrid/v1/health` returned 200 at `43087.109`;
- `src/integrations/runtime/workspaceRuntimeConfig.ts:26,44-45` falls back
  on non-OK/error, and selected env supplies fallback identity at
  `harness.ts:722-724`;
- preserved stderr has only non-fatal Browserslist/PostCSS/Rollup warnings;
  no module failure, Runtime transport error, or browser exception.

The first unresolved boundary is therefore `src/app/main.tsx:112-123`, the
pre-render dynamic-import `Promise.all` followed by
`initializeWorkspaceRuntimeIdentity()`. The artifacts do not identify which
import/evaluation or scheduling phase was pending. The 404 is later and is
handled by fallback, so it must not be called the mount cause.

Automatic31868 remains separate: HOME's existing diagnosis found the first
failure before browser work was the invalid product credential (missing
`version: 1` and `scope: "astrid"`), plus missing normal ACP forwarding env.
Do not merge that credential-parser cause with selected18585.

No selected/automatic rerun, browser, full suite, build, install, TypeScript,
product source, route, or shared proxy change was made.
