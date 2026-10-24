## FAIL — authoritative popup proof remains unqualified

No production code, tests, or fixtures were changed.

### Verified production path

The mounted path is real and correctly reaches the v2 commit caller:

`ShotTimelinePreview` → `ShotTimelineMediaControls` → `useTimelineCommandsService.addClip` → A2 local save/outbox → `localSaveSession` → `RuntimeDataProvider.commitTimeline` → generated Runtime client with `Idempotency-Key`.

Relevant sources:

- [ShotTimelinePreview.tsx](/home/user/work/wt/app-A3-popup-authority-path-0846/src/tools/travel-between-images/components/ShotTimelinePreview.tsx)
- [ShotTimelineMediaControls.tsx](/home/user/work/wt/app-A3-popup-authority-path-0846/src/tools/travel-between-images/components/ShotTimelineMediaControls.tsx)
- [shotTimelineDataProvider.ts](/home/user/work/wt/app-A3-popup-authority-path-0846/src/tools/travel-between-images/components/shotTimelineDataProvider.ts)
- [localSaveSession.ts](/home/user/work/wt/app-A3-popup-authority-path-0846/src/tools/video-editor/commands/localSaveSession.ts)
- [dataProvider.ts](/home/user/work/wt/app-A3-popup-authority-path-0846/src/integrations/runtime/dataProvider.ts)

### Source-derived authoritative recipe

For a shared popup add, App produces:

1. `occurrence.fork`
2. `occurrence.add-media`

Each command carries `schema_version`, `op`, `version`, `select`, `args`, `intent`, and exact `created` identities. The add command creates the clip and, only when needed, the occurrence asset binding.

The request must preserve:

- `api_version`
- `project_id`, `timeline_id`
- `base_revision_id`, `base_publication_id`
- native commands
- nonempty `label`
- steps with `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, optional `reads`
- `merge: "fields"` or `"atomic"`
- optional bounded request `reads`
- `Idempotency-Key`

For this native semantic path, request reads may remain omitted; Agent must capture authoritative dependencies. No synthetic dependency fallback is valid.

The response must come from the actual Agent/Runtime provider and include:

- canonical document and digest
- authoritative commands and steps
- provider/compiler versions
- `id_map`
- merge mode
- base, previous, and accepted IDs
- publisher
- durable receipt whose `result` equals `data`

The canonical closure must show the parent occurrence adopting the forked shot/revision, the new child/internal closure, exact media registry binding, dependency manifest pins, and all preserved opaque/raw fields. Returned step patches and dependencies must contain the complete provider-generated effects, not a single manually selected occurrence update.

### Proof-gap finding

The post-fix witness in `63e3956746` is not an authoritative provider proof:

- `authoritativeAddedDocument(graph, request)` derives the “provider” document from request fields.
- `data.commands` is assigned from `request.commands`.
- Dependencies use `request.reads ?? synthetic scope`.
- Only one synthetic patch effect is returned.
- It does not prove Agent-generated command records, complete fork/add-media effects, authoritative dependencies, conflict/invalid outcomes, or authentic rebased/idempotent replay behavior.

That commit, and the related witness commit `aebf027aca`, are not ancestors of current `HEAD` (`82cb5c0005`). The witness therefore cannot close the A3 C0 gap.

### Existing evidence and limits

- P1 proves the real Agent/Runtime envelope, accepted/merged/rebased behavior, conflict handling, durable receipts, and idempotent replay in [three-products.p1-chain.spec.ts](/home/user/work/wt/app-A3-popup-authority-path-0846/tests/e2e/local/three-products.p1-chain.spec.ts).
- [p2-semantic-oracle.ts](/home/user/work/wt/app-A3-popup-authority-path-0846/tests/e2e/local/support/p2-semantic-oracle.ts) proves the semantic request shape but not authoritative provider output.
- [timelineCommitFixture.ts](/home/user/work/wt/app-A3-popup-authority-path-0846/src/integrations/runtime/__tests__/timelineCommitFixture.ts) is an envelope fixture, not semantic provider authority.
- No browser, backend, HTTP, Runtime service, full suite, or new fixture/probe was run, per task scope.

Exact checks:

- `git diff --check` — PASS
- `git status --short --branch` — clean
- No targeted/full tests run; evidence is source inspection only.

Commit message written and `DONE` marker created.