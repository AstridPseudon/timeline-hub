# Data Fetching System

**Purpose**: Document which hooks own which data, how mutations invalidate caches, optimistic update patterns, and cache synchronization.

**Source of Truth**: `src/shared/lib/queryKeys/` (all cache keys), `src/shared/hooks/invalidation/useGenerationInvalidation.ts` (invalidation patterns), `src/shared/lib/query/queryDefaults.ts` (query presets).

---

## Runtime Connection (hosted build)

**Purpose**: How the hosted App reaches the local Runtime: origin prefix, the boot gate that precedes any Runtime read, and the gateway paths.

**Source of Truth**: `src/integrations/runtime/connection.ts` (origin, bases, state type, `RUNTIME_QUERY_ROOTS`), `src/integrations/runtime/RuntimeConnectionProvider.tsx` (gate), `src/integrations/runtime/localNetworkPermission.ts`, `scripts/astrid-loopback-gateway.ts` (checks), `config/vite/pairedRoutePolicy.ts` (route table).

| Build | `runtimeOrigin()` | `runtimeApiBase()` / `astridBase()` |
|-------|-------------------|-------------------------------------|
| Local dev, Plan B relay | `''` (`VITE_RUNTIME_ORIGIN` unset) | `/api/runtime` / `/api/astrid` |
| Hosted (`npm run build:hosted`) | `http://127.0.0.1:17340` | `{origin}/api/runtime` / `{origin}/api/astrid` |

**Boot gate**: `RuntimeConnectionProvider` (mounted in `src/shared/contexts/AuthContext.tsx`) and `RuntimeConnectionGate` (`src/app/Layout.tsx`) apply only when `runtimeOrigin() !== ''`. Order: permission (`local-network-access`), probe (`GET {runtimeApiBase()}/v1/health`, then `/v1/realm`), Runtime queries.

| `RuntimeConnectionState` | Set when (permission behavior) |
|--------------------------|--------------------------------|
| `connecting` | Permission unread, or `granted` and probing (re-probes every 3 s and on focus until connected) |
| `connected` (realm) | Health and realm both answer as a Astrid App gateway's |
| `cant_reach` (`firstTime`) | Network error, non-OK, or a non-gateway body; also permission `prompt`/unknown/throws, where nothing is sent until `connect()` sends an untimed probe (that is what makes Chrome ask). `firstTime` holds until `astrid.runtime.connectedBefore` is set |
| `blocked` | Permission `denied`; nothing is sent |
| `not_ready` (reason) | Gateway 503: `realm_changed`; `runtime_unavailable` or `runtime_discovery_invalid` gives `runtime_stopped`; `runtime_identity_mismatch` gives `identity_mismatch`; other codes give `unknown` |

**What a person sees** (`src/shared/components/RuntimeConnection/`: wording only in `copy.ts`, layout in `RuntimeConnectionPanel.tsx`). The product is called Astrid on every screen; commands appear only in the agent block (`agent.instructions`). Several states share one screen because a person does the same thing for each:

| Screen | States that show it | Primary action |
|--------|---------------------|----------------|
| Mink only, "Looking for Astrid on this computer…" after 1 s | `connecting`, `not_ready` `starting` | none |
| "Connect to Astrid on this computer" | permission `prompt` (direct visit) | Connect (the landing page's "use it right here" click sets a one-shot flag, `autoConnectRequest.ts`, and the gate calls `connect()` at once) |
| "Choose Allow in Chrome" | Connect pressed, Chrome's prompt open | none (arrow up to the address bar) |
| "Allow Astrid in Chrome" | `blocked` | two steps in Chrome's site settings |
| "Set up Astrid on this computer" | `cant_reach` first time | Copy setup steps for your agent (footer links the install guide) |
| "Astrid isn't running" | `cant_reach` returning, `not_ready` `runtime_stopped` / `unknown` | Copy steps for your agent |
| "Astrid needs a restart" | `not_ready` `identity_mismatch` / `realm_changed` | Copy steps for your agent (restart variant) |
| "Open Astrid on your computer" | any not-connected state on a phone (`isMobileDevice`, the landing dialog's check) | Send the link to your computer |

Once connected nothing is shown while Astrid is up (a screen-reader-only "Connected to Astrid" in `runtime-connection-status`). `useRuntimeRestartWatch` polls health: two failed readings in a row show the "Astrid stopped" card (clears itself when the same instance answers), a new instance or a `realm_changed` 503 shows the "Astrid restarted" card (Reload). While either card shows, `recoveryCard.ts` tells the editor to stay quiet: no canonical-refresh banner, no load-error card, a neutral "Not saved" badge, and `WorkspaceConnectionRecovery` never renders on the hosted build. When the "stopped" card clears, the shell retries what failed meanwhile: the timeline read (`retryLoad`) and the save that never got an answer (`retryPendingSave`, which replays it under its own idempotency key; an edit made meanwhile queues behind it and is never reported as "changed somewhere else", see `OwnUnacknowledgedSaveError`). The hosted build never shows a red "Error" save badge, and `TimelineLoadErrorCard` (the connection cards' frame) also retries by itself when `/v1/health` starts answering. The gateway adds `app_url` (`http://127.0.0.1:<app port>`, schema in `gatewayHealth.ts`) to its health answer so disabled controls can link to the local app ("Open the full editor").

**Launcher output** (`scripts/dev-local-workspace.mjs`): a healthy `npm run dev:local` prints `Starting Astrid…`, then the `Open <hosted origin>` block, only after the gateway and the app both listen. Everything else (proxy, ACP bridge, gateway JSON line, Vite) is held back; `--verbose` or `ASTRID_VERBOSE=1` prints it after the Open block. Errors are one `Astrid: ` line plus one `Details: ` line for an agent. A second launcher for the same realm says `Astrid is already running in another window.` and prints the same block without starting anything. `--check` prints `Astrid is ready.`

**Gateway** (`127.0.0.1:17340`, `DEFAULT_GATEWAY_PORT`): serves the dev paths `/api/runtime/*` and `/api/astrid/*` on the route table; admin, doctor, backup, restore, export, realm recovery, workers, credentials, compose and ACP without `--acp` get 404 `route_not_allowed`. Checks run in this order:

| Check | Refusal |
|-------|---------|
| Host exactly `127.0.0.1:<port>` | 403 `invalid_host` |
| Origin exactly the hosted origin (no Referer fallback) | 403 `hosted_origin_required` |
| Route allowlist; preflight method and headers | 404 `route_not_allowed`; 403 `header_not_allowed` |
| `Authorization` or `Cookie` sent | 403 `browser_credentials_forbidden` |
| Runtime down, or realm or identity check fails | 503 `runtime_unavailable`, `realm_changed`, `runtime_identity_mismatch`, `runtime_discovery_invalid` |

Key invariants:

1. No Runtime query runs before `connected`; on connect every key rooted in `RUNTIME_QUERY_ROOTS` is invalidated (`isRuntimeQueryKey`, `AuthContext.tsx`).
2. `connected` is sticky for the page's life; a Runtime that stops or restarts later shows the "Astrid stopped" / "Astrid restarted" card from `useRuntimeRestartWatch`, not a gate state.
3. First connection calls `rememberAppEntryPreference` (a returning `/` visit skips the landing page); the storage flag is try/catch guarded.
4. `setRuntimeOrigin()` runs once at boot; a gateway origin plus a compiled `VITE_WORKSPACE_RUNTIME_EXPECTED_*` identity throws (`build:hosted` sets them empty). Bases are read per request, never cached.
5. The gateway checks Origin before routing, reads endpoint and token per request, and never sends the product token to the page; a changed realm is refused with 503 `realm_changed`.

## Query Scopes

Three intentionally separate scopes for generation data. These are NOT duplication.

| Scope | Hook | Query Key | Table | Use Case |
|-------|------|-----------|-------|----------|
| Project | `useProjectGenerations` | `['unified-generations', 'project', projectId, ...]` | `generations` | Paginated gallery (GenerationsPane, MediaGallery) |
| Shot | `useShotImages` | `['all-shot-generations', shotId]` | `shot_generations` JOIN `generations` | Timeline, ShotEditor, shot image grids |
| Variant | `useVariants` | `['generation-variants', generationId]` | `generation_variants` | Lightbox variant switching |

### Derived/selector hooks (no separate queries)

| Hook | Derives From | Filters |
|------|-------------|---------|
| `useTimelineImages(shotId)` | `useShotImages` | Positioned, non-video, valid location |
| `useUnpositionedImages(shotId)` | `useShotImages` | Null timeline_frame, non-video |
| `useVideoOutputs(shotId)` | `useShotImages` | Video type only |
| `useDerivedItems(generationId)` | Own query `['derived-items', id]` | Edits/children of a generation |

## Cache Priming & Loading

`useShotImages` is one query (`shot_generations` JOIN `generations`, no multi-phase loading). For instant display on shot navigation, `usePrimeShotGenerationsCache` seeds the cache first: shot selected, cache primed from `ShotsContext` (`usePrimeShotImagesCache` in `useShotImages.ts`, no metadata), selectors such as `useTimelineImages` have data at once, then the `useShotImages` queryFn replaces it with full data.

### Query Presets (`src/shared/lib/query/queryDefaults.ts`)

| Preset | staleTime | Use Case |
|--------|-----------|----------|
| `realtimeBacked` | 30s | Data updated by realtime/mutations (generations, tasks, shots) |
| `static` | 5min | Resources, presets, tool settings |
| `immutable` | Infinity | Completed task results, historical data |
| `userConfig` | 2min | User preferences, account settings |

## Mutation Ownership

Mutations live in `useGenerationMutations.ts` (re-exported from `useProjectGenerations.ts` for compatibility).

| Mutation Hook | Table | Invalidation |
|---------------|-------|-------------|
| `useDeleteGeneration` | `generations` | None (caller invalidates) |
| `useDeleteVariant` | `generation_variants` | None (caller invalidates) |
| `useUpdateGenerationLocation` | `generations` | None (caller invalidates) |
| `useCreateGeneration` | `generations` + `generation_variants` | None (caller invalidates) |
| `useToggleGenerationStar` | `generations` | Optimistic update on `unified-generations`, `shots`, `all-shot-generations` |

Shot-generation mutations in `useShotGenerationMutations.ts`:

| Mutation | Table | Optimistic? | Invalidation |
|----------|-------|-------------|-------------|
| `useAddImageToShot` | `shot_generations` | Yes (temp ID, cache update) | shots list, meta, unified |
| `useRemoveImageFromShot` | `shot_generations` | Yes (set frame null) | segment queries |
| `useUpdateShotImageOrder` | `shot_generations` | Yes (reorder frames) | meta, source-slot |
| `useDuplicateAsNewGeneration` | `generations` + `shot_generations` | No | shots, generations, segments |

Variant mutations in `useVariants.ts` (`setPrimaryVariant`, `deleteVariant`, both on `generation_variants`) call `invalidateVariantChange()`.

## Optimistic Update Pattern

Used by shot-generation mutations (`useShotGenerationMutations.ts`). All follow the same structure:

```
onMutate:  cancel queries -> snapshot previous -> update cache (mark _optimistic)
onError:   rollback from snapshot
onSuccess: replace temp IDs with real IDs -> scoped invalidation
```

Cache utilities (`src/shared/hooks/shots/cacheUtils.ts`) provide helpers: `cancelShotsQueries`, `updateAllShotsCaches`, `rollbackShotsCaches`, `updateShotGenerationsCache`, `rollbackShotGenerationsCache`.

Stable callbacks: use refs to prevent recreation storms (avoid `addMutation` in deps).

## Invalidation Patterns

### Centralized: `useGenerationInvalidation.ts`

| Function | When to Use | What It Invalidates |
|----------|------------|-------------------|
| `useInvalidateGenerations()(shotId, opts)` | After shot-scoped changes | `all-shot-generations`, `segment-live-timeline`, `shot-generations-meta`, `unpositioned-count` (scoped by `opts.scope`) |
| `invalidateVariantChange(qc, opts)` | After variant create/update/set-primary | Variants, detail, badges, all shot-generations (broad), unified, derived, segment children/sources |
| `invalidateAllShotGenerations(qc, reason)` | Global fallback (avoid if possible) | All `all-shot-generations` queries via predicate |

Scopes for `useInvalidateGenerations`: `'all'` | `'images'` | `'metadata'` | `'counts'`.

### Realtime invalidation

Realtime event -> invalidation mapping: see [realtime_system.md](realtime_system.md).

### Smart Polling (fallback)

`DataFreshnessManager` + `useSmartPollingConfig` provides intelligent polling when realtime is unhealthy. Hooks opt in via `useSmartPollingConfig(['namespace', id])`.

## When to Use Which Hook

| I want to... | Use |
|-------------|-----|
| Paginated project gallery | `useProjectGenerations(projectId, page, limit, enabled, filters)` |
| Shot timeline/grid, positioned, unpositioned, videos | `useShotImages(shotId)`, `useTimelineImages`, `useUnpositionedImages`, `useVideoOutputs` |
| Variants / derived edits in lightbox | `useVariants({ generationId })` / `useDerivedItems(generationId)` |
| Delete/star/create generations; shot add/remove/reorder | `useGenerationMutations` / `useShotGenerationMutations` |
| Invalidate after shot-scoped / variant changes | `useInvalidateGenerations()` / `invalidateVariantChange()` |

## Key Invariants

1. **Three scopes, three hooks** -- project, shot, variant. Don't merge them.
2. **Mutations in dedicated files** -- `useGenerationMutations.ts` and `useShotGenerationMutations.ts`, not in query hooks.
3. **Prefer `queryKeys.*` registry for all query keys** -- ~25 isolated hooks still use inline keys (see `code_quality_audit.md` S2).
4. **Realtime -> invalidation, not direct cache updates**; smart polling is the fallback; optimistic updates snapshot and roll back.
