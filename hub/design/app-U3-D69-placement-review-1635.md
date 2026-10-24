## D69 review: FAIL

Tree reviewed: `fe773e45aa4f95edfb4a30b4dab7908c7286443e`, clean.

What passed:

- Scope is exactly the two placement tests plus `placementService.ts`.
- Frozen upstream declaration hashes match exactly:
  - `fcf8e413...ce8dd0d`
  - `80bd6c08...a1183b`
- Targeted Vitest: 3 files, 30/30 passed.
- Serialized Node20 TypeScript: root, app, node all passed.
- Scoped ESLint and `git diff --check` passed.
- Caller remains `placeGeneration → LocalSaveSession → RuntimeDataProvider.commitTimeline`; no legacy writer/RPC/overwrite route.

Blocking finding:

`mutateTimelineDocument` retries every `TimelineVersionConflictError` ([placementService.ts:375](/home/user/work/wt/app-U3-D69-placement-review-1635/src/shared/lib/placement/placementService.ts:375)). However, `createPlacementLocalSaveHandoff.flush()` converts any rejected/error session state into `TimelineVersionConflictError` ([placementService.ts:215](/home/user/work/wt/app-U3-D69-placement-review-1635/src/shared/lib/placement/placementService.ts:215)). Therefore definitive Runtime refusals/validation failures can be cleared by `retryRejected()` and semantically replayed once, instead of remaining refused. The retry must be restricted to an explicitly classified stale-head conflict.

OldRED was not re-executed because this review was read-only; newGREEN is verified by the 30/30 run above. No code or design changes made.