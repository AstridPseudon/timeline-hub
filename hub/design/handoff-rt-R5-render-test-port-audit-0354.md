## R5 audit — FAIL for migration readiness

R5 itself is correct: Runtime now rejects retired writers with 410 `timeline_commit_required`, before provider/CAS/history writes. The 17 authority failures are genuine migration blockers, not candidates for blanket 410 expectations.

Source audited:

- Runtime: `ac115014b01fc2e970c53d588b53432f7306a615`, tree `da7d10da5014fddb6e0a985da4ff6a4481aef640`
- Agent G4 staged ref: `737df3dbfd567943e7d21f085b2d290c31087449`, tree `629a19c8ccf75b602ea9cd91c3fd5a02dec68623`
- Contract: `contract/commit-v2.md`
- Review: `agent-G4-render-current-review-0314.md`
- Frozen Runtime pins `34eac0041` / `ad823e0a0` remain unchanged.

### Scenario disposition

| Existing scenario | R5 disposition |
|---|---|
| Direct old render/publication route, tracked/headless, no-write guard | Keep as 410 policy coverage in `test_timeline_legacy_authority.py`; do not preserve nuanced old reasons |
| Fence/stale attempt and cancel seam | Migrate to producer-attempt fencing through Agent requester → Runtime commit |
| Immutable admitted target/project scope | Migrate to authenticated `producer.guard` and requester-scope checks |
| Exact checkpoint/restart/idempotency | Migrate to Runtime commit receipt/history plus Agent outbox exact retry |
| Changed payload under same key | Assert `idempotency_mismatch` and no writes |
| Exact canonical render pin | Assert render task `params.canonical_revision` equals accepted commit revision/publication/content digest |
| Accepted/merged/conflict/invalid/preview | Preserve full v2 fields, structured details, `would_status`, bindings/effects/history/undo metadata |

The old positive cases `legacy_head_without_canonical_publication_remains_publishable` and direct `publish_timeline_render` publication are retired behavior; they must become either 410 policy tests or real canonical-commit setup, never remain successful direct saves.

### Exact Agent production path

Use the staged G4 requester path:

`publish_stitched_render` → `publish_authoring_proposal` → `RemoteTasks.publish_timeline_render` → `commit_assembly` → `TimelineSession.commit_many`/`_flush` → Runtime `/commit`, then ordinary `tasks.admit` with `canonical_revision`.

The Agent `publish_timeline_render` name is now an adapter, not the retired Runtime writer.

Existing reusable Runtime integration fixtures:

- `tests/test_timeline_commit_integration.py`: `film`, `agent`, `_start_door`, `_post_door`, `Editing`
- `tests/astrid_checkout.py`: `astrid_importable`
- `tests/test_shot_composition_runtime.py`: `restore_provider`

The staged Agent requester tests are useful evidence but use generated transport fakes; they are not Runtime-mounted proof.

### Minimal subsequent author scope

Runtime-only test migration:

- `tests/test_timeline_render_publication.py`
- `tests/test_timeline_render_publication_authority.py`

Reuse the existing real Agent/Runtime integration harness. Do not change schemas, clients, pins, or production Runtime code. Do not reuse `_ready_authoring_attempt`, `_publication_body`, or `_track` for positive behavior; those fixtures exercise retired saves.

True prerequisites:

1. Agent G4 must be normally adopted; `737df3…` is staging evidence.
2. A real settled assembly proposal and original requester session must be available—no fake executor, fake publisher, mock provider, or invented adapter.
3. Runtime must mount the actual Agent provider through `authoring_profile="astrid"` with `ASTRID_CHECKOUT`.
4. The known Runtime structured-preview/partial-receipt hold must be resolved before preview assertions are accepted.

### Evidence

- `git diff --check`: PASS
- Worktree: clean; no repository edits made.
- No pytest suite rerun, per instruction not to repeat the 17 known failures or run broad/heavy suites.
- Prior draft report: 96 bounded tests passed, 74 neighbor tests passed, 17 authority failures; `py_compile` passed; Ruff/Pyright unverified.
- Agent G4 review reported 13 requester, 48 v2/error/meta, and 221 render/assembly/producer tests passing, but all were staged/transport-level evidence.

Harness files written: `DONE` and the requested commit message.