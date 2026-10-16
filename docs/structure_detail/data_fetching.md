# Data Fetching System

**Purpose**: Document which hooks own which data, how mutations invalidate caches, optimistic update patterns, and cache synchronization.

**Source of Truth**: `src/shared/lib/queryKeys/` (all cache keys), `src/shared/hooks/invalidation/useGenerationInvalidation.ts` (invalidation patterns), `src/shared/lib/query/queryDefaults.ts` (query presets).

---

## Runtime Connection (hosted build)

**Purpose**: How the hosted App reaches the local Runtime: origin prefix, the boot gate that precedes any Runtime read, and the gateway paths.

**Source of Truth**: `src/integrations/runtime/connection.ts` (origin, bases, state type, `RUNTIME_QUERY_ROOTS`), `src/integrations/runtime/RuntimeConnectionProvider.tsx` (gate), `src/integrations/runtime/localNetworkPermission.ts`, `scripts/reigh-loopback-gateway.ts` (checks), `config/vite/pairedRoutePolicy.ts` (route table).

| Build | `runtimeOrigin()` | `runtimeApiBase()` / `astridBase()` |
|-------|-------------------|-------------------------------------|
| Local dev, Plan B relay | `''` (`VITE_RUNTIME_ORIGIN` unset) | `/api/runtime` / `/api/astrid` |
| Hosted (`npm run build:hosted`) | `http://127.0.0.1:17340` | `{origin}/api/runtime` / `{origin}/api/astrid` |

**Boot gate**: `RuntimeConnectionProvider` (mounted in `src/shared/contexts/AuthContext.tsx`) and `RuntimeConnectionGate` (`src/app/Layout.tsx`) apply only when `runtimeOrigin() !== ''`. Order: permission (`local-network-access`), probe (`GET {runtimeApiBase()}/v1/health`, then `/v1/realm`), Runtime queries.

| `RuntimeConnectionState` | Set when (permission behavior) |
|--------------------------|--------------------------------|
| `connecting` | Permission unread, or `granted` and probing (re-probes every 3 s and on focus until connected) |
| `connected` (realm) | Health and realm both answer as a Reigh gateway's |
| `cant_reach` (`firstTime`) | Network error, non-OK, or a non-gateway body; also permission `prompt`/unknown/throws, where nothing is sent until `connect()` sends an untimed probe (that is what makes Chrome ask). `firstTime` holds until `reigh.runtime.connectedBefore` is set |
| `blocked` | Permission `denied`; nothing is sent |
| `not_ready` (reason) | Gateway 503: `realm_changed`; `runtime_unavailable` or `runtime_discovery_invalid` gives `runtime_stopped`; `runtime_identity_mismatch` gives `identity_mismatch`; other codes give `unknown` |

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
2. `connected` is sticky for the page's life; a Runtime that stops later shows the restart message in `client.ts`, not a gate state.
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
