# Placement contract review

App base: `c8566f12d114c538db8136b8c580a1e663af1ad1`.
Agent candidate: `a6c2db3d14c14da3be61c7e28b615c0e4202e619`, read from
`hub/timeline/agent/tl/agt-m2-placement-create-unplace-b` in `/home/user/work/agent`.
Read PLAN, App STATUS, placement design, and the monotonic reservation rule in
`design/edit-recipe.md` / `design/m2-move-draft.md:299-306`.

## Changes and conclusion

Appended **Placement candidate review — 2026-10-20** to
`orch/design/app-writer-contract-gaps.md`. No product, schema, canonical contract,
test, dependency, pin, integration worktree or git mutation. The assigned App
worktree is clean after removal of the temporary candidate source archive.
The review and diagnostics are shared notes, outside the App repository.

Traced all direct place/unplace producers: add helper/hook, auto-position hook,
reference upload and reference backfill; remove hook always requests pooling,
with optional batch shifts. None carries an occurrence owner. Canonical
projection exposes owner/raw-child identity, but resolving a shot-only request
to one occurrence requires actual original accepted data, not ID spelling or
first-match inference. Native creation requires an exclusive translation-only
occurrence, image pin, fresh reserved raw child ID, explicit global time and
literal hold (App default is 4 seconds). This is a candidate supported subset,
not a converted or Runtime-qualified App caller.

Auto append, pool/null, collision shift, batch pool promotion, keepAsPooled,
video creation and registry refresh remain uncovered. R13 returns a selected
variant/object URL, not the immutable five-field catalog pin or verified media.
Use the existing Runtime media-selection operation and approved media capture
seam; no new port, op, DTO, verification fabricated from MIME, or guard bypass.

Two concrete blockers were reproduced through the candidate's real Agent
`RuntimeCommitService.commit`, using its existing detached MediaRealm port:

1. Pure execute accepts `[unplace, create(same ID)]`; provider admission rejects
   both the same-batch and separate post-unplace recreation with 409
   `identity_collision`, `occurrence:occ-a/clip:placed`. The accepted history's
   reservations survive removal. The candidate's same-ID re-place claim is
   incorrect. Existing placement.move is a possible narrow mapping only when
   an existing clip's media stays unchanged and explicit time needs no collision
   shift. No weakening of retired-ID reservations is recommended.
2. Create → unplace → undo(unplace) restores the exact post-create document;
   undo(create) rejects with 409 `intervening_write` on the child root. The
   removal and inverse remain overlapping accepted writes even with no other
   author. Agent/history owner must resolve this LIFO user-visible counterexample
   while retaining concurrent/other-author ABA protections. App must not call
   this a working undo stack.

Every diagnostic refusal preserved head, complete history, document map,
accepted results and prepared results. These are new diagnostic observations,
not replacement expectations for any original positive behavior test. All
original App expectations remain unchanged and passing.

## Exact commands and results

From `/home/user/work/wt/app-m2-placement-contract-review`:

```sh
npx vitest run --config config/testing/vitest.config.ts src/shared/lib/placement/__tests__/documentPlacement.test.ts src/shared/lib/placement/__tests__/placementService.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts src/shared/hooks/shots/__tests__/addImageToShotHelpers.test.ts src/shared/hooks/shots/__tests__/useShotGenerationMutations.test.ts --maxWorkers=1
```

**PASS: 40 tests / 5 files, 9.67 s.** Includes positive auto append, pooling,
collision shift, deterministic same-pair re-placement, pooled promotion,
keepAsPooled, shifts, and bounded CAS retry. Mocked service/hook evidence only.

```sh
npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/data/generationAssetResolver.test.ts --maxWorkers=1
```

**PASS: 5 tests / 1 file, 1.75 s**, including video media-type resolution.

Candidate source was temporarily extracted inside the assigned worktree:

```sh
mkdir -p .placement-review-source
git -C /home/user/work/agent archive a6c2db3d14c14da3be61c7e28b615c0e4202e619 astrid tests pyproject.toml | tar -x -C .placement-review-source
```

From that directory, with shared dependency-only venv and no installation:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_placement_create_unplace.py
```

**PASS: 35 tests, 2.69 s.** Existing candidate golden/capture/replay/inverse/
single-step provider undo/redo/refusal tests, unchanged.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-placement-contract-review/notes/placement-provider-probe.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-placement-contract-review/notes/placement-provider-probe.json
```

**Exit 0:** three diagnostic refusal assertions and exact undo(remove)
restoration assertion pass. Script/output retained beside this report.
It uses the candidate's unchanged `runtime_abi` fixture (fake ABI
exceptions/metadata) and detached in-memory port. This is actual Agent provider
admission logic, **not real Runtime commit-service acceptance**.

## Decisions, limits and next steps

No settled decision changed. Keep canonical reservation and guarded inverse
rules; report the candidate's unsupported claims and concrete LIFO blocker to
the Agent/history owner. Keep placement OPEN and existing writers/tests until
the complete replacement is qualified; no publisher deletion is justified.

Local Runtime `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136` lacks
placement.create in `contract/schemas/edit-command.json`; no matching official
candidate pair was available/used. No real Runtime, full suite, socket, browser,
install, build or typecheck was run or requested. App reload/undo/retry and
zero-legacy traffic are unverified.

The appended review provides the Runtime-owner test recipe: normal matched
schema/artifact release, actual image ingest/public media selection/canonical
occurrence bootstrap, accepted create/reload, both same-ID refusal shapes with
unchanged head/history, normal LIFO sequence retaining the positive original-
state expectation, restart/exact retry, and other-author ABA/dependency controls.
Run that through normal admission without schema overrides, then qualify the
bounded App mappings; do not fabricate an accepted result from pure execute.
