# Data Fetching System

**Purpose**: Document which hooks own which data, how mutations invalidate caches, optimistic update patterns, and cache synchronization.

**Source of Truth**: `src/shared/lib/queryKeys/` (all cache keys), `src/shared/hooks/invalidation/useGenerationInvalidation.ts` (invalidation patterns), `src/shared/lib/query/queryDefaults.ts` (query presets).

---

## Runtime Connection (hosted build)

**Purpose**: How the hosted App reaches the local Runtime: origin prefix, the boot gate that precedes any Runtime read, and the Runtime door's paths.

**Source of Truth**: `src/integrations/runtime/connection.ts` (origin, bases, state type, `RUNTIME_QUERY_ROOTS`), `src/integrations/runtime/RuntimeConnectionProvider.tsx` (gate), `src/integrations/runtime/localNetworkPermission.ts`, astrid-runtime `runtime_protocol/door.py` (the Runtime's door: checks and route table).

| Build | `runtimeOrigin()` | `runtimeApiBase()` / `astridBase()` |
|-------|-------------------|-------------------------------------|
| Local dev, Plan B relay | `''` (`VITE_RUNTIME_ORIGIN` unset) | `/api/runtime` / `/api/astrid` |
| Hosted (`npm run build:hosted`) | `http://127.0.0.1:17340` | `{origin}/api/runtime` / `{origin}/api/astrid` |

**Boot gate**: `RuntimeConnectionProvider` (mounted in `src/shared/contexts/AuthContext.tsx`) and `RuntimeConnectionGate` (`src/app/Layout.tsx`) apply only when `runtimeOrigin() !== ''`. Order: permission (`local-network-access`), probe (`GET {runtimeApiBase()}/v1/health`, then `/v1/realm`), Runtime queries. Chrome prompts only after Connect. Safari and Firefox skip that prompt. The page polls every 3 s and on focus; background polls never add a checking indicator.

| `RuntimeConnectionState` | Set when |
|--------------------------|----------|
| `connecting` | Permission is unread or `prompt`, or fewer than two consecutive readings have failed |
| `connected` | Health and realm both answer successfully |
| `set_up` | Two consecutive failed readings, with no previous connection and no `down` reading this page |
| `not_running` | Two consecutive failed readings after a previous connection or any `down` reading this page |
| `restart_needed` | The door reports `runtime_identity_mismatch`; shown immediately |
| `blocked` | Permission is `denied`; nothing is sent |

Otherwise the provider stays on `connecting` until two readings in a row fail. A door refusal (503 `runtime_unavailable`: listening, but the Runtime is not ready) is evidence Astrid is installed; network errors and other replies are silent. A `restart` response takes precedence and shows `restart_needed` immediately. Background re-checks do not produce a temporary checking line.

**What a person sees** (`src/shared/components/RuntimeConnection/`: wording only in `copy.ts`, layout in `RuntimeConnectionPanel.tsx`). Each gate state names its screen; permission and phone screens come from browser context. Setup, repair, restart, and update states show the corresponding OS installer line with a copy action. The landing installer opens `/?connect=1`, which the app entry routes through to this gate:

| Screen | States that show it | Primary action |
|--------|---------------------|----------------|
| Mink only, "Looking for Astrid on this computer…" after 1 s | `connecting` while waiting for permission or probe readings | none |
| "Connect to Astrid on this computer" | permission `prompt` (direct visit or before installer auto-connect) | Connect on a direct visit; the installer's `connect=1` query is consumed by `autoConnectRequest.ts`, and the gate calls `connect()` automatically |
| "Choose Allow in Chrome" | Connect pressed, Chrome's prompt open | none (arrow up to the address bar) |
| "Allow Astrid in Chrome" | `blocked` | two steps in Chrome's site settings |
| "Set up Astrid on this computer" | `set_up` | Copy the OS installer line |
| "Astrid isn't running" | `not_running` | Copy the install/repair line |
| "Astrid needs a restart" | `restart_needed` | Copy the install/repair line |
| "Open Astrid on your computer" | any not-connected state on a phone (`isMobileDevice`, the landing dialog's check) | Send the link to your computer |

Once connected nothing is shown while Astrid is up (a screen-reader-only "Connected to Astrid" in `runtime-connection-status`). `useRuntimeRestartWatch` polls health: two failed readings in a row show the "Astrid stopped" card (clears itself when the same instance answers), a new instance or a `runtime_identity_mismatch` 503 shows the "Astrid restarted" card (Reload). While either card shows, `recoveryCard.ts` tells the editor to stay quiet: no canonical-refresh banner, no load-error card, a neutral "Not saved" badge, and `WorkspaceConnectionRecovery` never renders on the hosted build. When the "stopped" card clears, the shell retries what failed meanwhile: the timeline read (`retryLoad`) and the save that never got an answer (`retryPendingSave`, which replays it under its own idempotency key; an edit made meanwhile queues behind it and is never reported as "changed somewhere else", see `OwnUnacknowledgedSaveError`). The hosted build never shows a red "Error" save badge, and `TimelineLoadErrorCard` (the connection cards' frame) also retries by itself when `/v1/health` starts answering.

**Launcher output** (`scripts/dev-local-workspace.mjs`; start it from the [repository README](../../README.md)): a healthy launch prints `Starting Astrid…`, then the `Open <hosted origin>` block, only after the Runtime's door and the app both listen. Other startup details (proxy, door line, Vite) are held back; `--verbose` or `ASTRID_VERBOSE=1` prints them after the Open block. Errors are one `Astrid: ` line plus one `Details: ` line for an agent. A second launcher for the same realm says `Astrid is already running in another window.` and prints the same block without starting anything. `--check` prints `Astrid is ready.`

**The Runtime's door** (`127.0.0.1:17340`, opened by `astrid-runtime up`; astrid-runtime `runtime_protocol/door.py`): serves the dev paths `/api/runtime/*` and `/api/astrid/*` on the route table; admin, doctor, backup, restore, export, realm recovery, workers, credentials and compose get 404 `route_not_allowed`. Chat is forwarded to the agent-owned chat service registered in the Runtime's `chat.json`; the Runtime supervises that service, and the app does not launch a local bridge. Checks run in this order:

| Check | Refusal |
|-------|---------|
| Host exactly `127.0.0.1:<port>` | 403 `invalid_host` |
| Origin exactly the hosted origin (no Referer fallback) | 403 `hosted_origin_required` |
| Route allowlist; preflight method and headers | 404 `route_not_allowed`; 403 `header_not_allowed` |
| `Authorization` or `Cookie` sent | 403 `browser_credentials_forbidden` |
| Runtime not ready, or its credential is not the product's | 503 `runtime_unavailable`, `runtime_identity_mismatch` |
| Chat route with no chat service registered | 503 `acp_unavailable` (the chat pane says so in one plain line) |

Key invariants:

1. No Runtime query runs before `connected`; on connect every key rooted in `RUNTIME_QUERY_ROOTS` is invalidated (`isRuntimeQueryKey`, `AuthContext.tsx`).
2. `connected` is sticky for the page's life; a Runtime that stops or restarts later shows the "Astrid stopped" / "Astrid restarted" card from `useRuntimeRestartWatch`, not a gate state.
3. First connection calls `rememberAppEntryPreference` (a returning `/` visit skips the landing page); the storage flag is try/catch guarded.
4. `setRuntimeOrigin()` runs once at boot; a gateway origin plus a compiled `VITE_WORKSPACE_RUNTIME_EXPECTED_*` identity throws (`build:hosted` sets them empty). Bases are read per request, never cached.
5. The door (astrid-runtime `runtime_protocol/door.py`, inside the Runtime) checks Origin before routing, acts with the product credential through the Runtime's own handlers, and never sends that credential to the page.

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
