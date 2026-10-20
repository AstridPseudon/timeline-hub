# M2 writer bundle 2 — manager review candidate, release HELD

All M2 integration remains HELD until PLAN records M1. This is the complete
required ordinary + popup + PARAM source composition for review before normal
Runtime generation. Manager owns source freeze. PARAM release is independently
HELD for `agt-m2-params-object-scope`; the reviewed `_hydrate` still fetches all
admission snapshot objects. No App readiness or popup acceptance is claimed.

Frozen Bundle1 stays Agent `3bf9e5368a956ef562c77e1beb0a745addf23daf` /
Runtime `6be970633cc82ab412428151e6bf42f3e7fc3081`, client `0.2.2`.
No leased Bundle2/Bundle1 refs, vendor files or Runtime artifacts changed.

## Source identity

| Field | Exact value |
|---|---|
| Branch | `tl/agt-m2-bundle2-complete-source` |
| Worktree | `/home/user/work/wt/agt-m2-bundle2-complete-source` |
| Base commit | `7b61efd5ea9fd9420b7fa577cfafa4487e3ca746` |
| Final tested source tree | `fe87ed862652e309a2dc86fd4845e859d3da5a9a` |
| Composed commit | `d4743e2984cef0908fa0b6bef166aa801f2bde8f` |
| Canonical schema | `/home/user/work/wt/agt-m2-bundle2-complete-source/astrid/core/timeline/schema/edit-command.schema.json` |
| Schema file SHA256 | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` |
| Runtime lock SHA256 | `76509204d81fdeb25dcf3b621a52f0f3ac919c4e53bfe64f0e6c261dbf23ec08` (unchanged) |
| Frozen Runtime for official HTTP proof | `6be970633cc82ab412428151e6bf42f3e7fc3081` |
| PARAM Runtime for direct source proof only | `b3ce5aa65151a6174064d73838ad23da4a8a7141` |

The sandbox cannot commit; the harness commits only after worker exit. Manager
must run `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-complete-source/notes/finalize-handoff.py` afterward. It verifies the harness
commit's exact tree, then publishes that exact commit in this absolute document.
The pending cell is not a source-freeze identity; do not substitute the base SHA.

## Exact composition

Base `7b61efd5` / tree `c401f772` already contains foundation `84db8bde`, popup
`5528c45c`, provenance `2f77310e`, placement `e4338c48`, frozen client `0.2.2`.
This candidate adds only the following approved deltas:

- Scalar: `84db8bde..7b54ca92` (`clip.set`, App golden).
- Root staging: `84db8bde..1b52391e`, including source-aware inverse context and
  provider/rebase state. Both root strict xfails now pass with their assertions.
- Pure pack `8b0946e6^..8b0946e6`, portable `8b0946e6..b2b51c4a`, PARAM
  `b2b51c4a..3565462c`. The three selected-schema strict xfails now pass with
  their assertions. Independent object-scope WIP is excluded.
- Trim prerequisite `51948d40..d82f6ef7` and source units `d82f6ef7..8de94595`.
- Split `51948d40..3b03eee9006990739fae19884389149c76d8fbd0`, including its
  reviewed stable create-after/order primitives. Foundation's staged-create
  selection validation is retained while recognizing the new stable boundary.
- Only the new shared-image inverse test file from `2ad74839`; no product fix.

The shared recorder/execute/rebase/provider accepts and forwards the union
`verified_media`, `schema_inputs`, `realm_id`. Clear-only scalar handling,
source mappings, retained pins, source-aware inverse state and the media
provenance removal/dependent guards survive the reconciliation. Canonical
`schema_source` references the closed named `DocumentPin` definition, with exactly
the reviewed document_id/version/content_digest fields. Existing root and scoped
asset patterns remain one union. No older whole commands/schema/core copy was used.
Reconciliation adds only argument forwarding, the named schema relocation, and
selection-condition reconciliation beyond the exact overlays (well below 40
product glue lines); no new behavior or compiler expansion.

Optional free moves are excluded. No word/default-compiler/physical-map WIP,
Runtime generated DTO/Protocol edits, release-version choice or pin change.
Per-overlay patches and a 47-check exact-byte/delta + canonical semantic-union
audit live under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-complete-source/notes`. `final-manifest.json` records the complete source tree,
changed files and goldens; `audit.py` is reproducible.

## Operations and capture exports

All registered operations are schema_version `1`, version `1`; engine/provider
`timeline.inverse` and `timeline.restore` remain separate. Every registered args
schema is closed and is the same object used by the native registry.

| Operation | Capture export (`astrid.sdk.timeline.` prefix) | Args |
|---|---|---|
| `clip.move` | `capture.capture_move` | `ClipMoveArgs` |
| `placement.move` | `native_placement_commands.capture_placement` | `ClipMoveArgs` |
| `clip.delete` | `capture.capture_clip_delete` | `ClipDeleteArgs` |
| `clip.add` | `_clip_commands.capture_clip_add` | `ClipAddArgs` |
| `clip.set` | `_clip_scalar_commands.capture_clip_set` | `ClipSetArgs` |
| `clip.trim` | `_trim_commands.capture_clip_trim` | `ClipTrimArgs` |
| `clip.split` | `_split_commands.capture_clip_split` | `ClipSplitArgs` |
| `clip.set-params` | `_scalar_commands.capture_clip_set_params` | `ClipSetParamsArgs` |
| `track.create` | `capture.capture_track_create` | `TrackCreateArgs` |
| `track.set` | `_track_commands.capture_track_set` | `TrackSetArgs` |
| `occurrence.add-media` | `native_occurrence_media_commands.capture_occurrence_add_media` | `OccurrenceAddMediaArgs` |
| `occurrence.swap-media` | `native_occurrence_media_commands.capture_occurrence_swap_media` | `OccurrenceSwapMediaArgs` |

Selected PARAM capture additionally accepts `schema_source`, `schema_inputs`,
`realm_id`; detached capture inputs never authorize server execution. The provider
loads exact scoped immutable inputs. `sync.TimelineSession.queue/commit` stays the
native ingress. MediaSelection's five fields and ABI1 selected_media are unchanged.

## Portable goldens

All paths below are under `/home/user/work/wt/agt-m2-bundle2-complete-source/tests/editing_conformance/fixtures/`.
M1/parent-label capture + records + output remain exactly **87776 bytes**,
SHA256 `b7f84a929716c9fc479fff1ea99e26daeeeb49b72ddc7594562b929f0feb3ff8`.
Original foundation/popup/placement/scalar/trim/split goldens are byte-preserved.

| Golden filename | SHA256 |
|---|---|
| `recipe_clip_delete.json` | `091bc1c7fa9c57583dde8fcc6d6af9226513bf4f214369ef0892cc1db492f0aa` |
| `recipe_m1_move.json` | `e1dc5fc72e42fa90aed3e46ccd3bb95e219004bddd2917dc99f0154cf768dba0` |
| `recipe_m1_occurrence.json` | `dba00dff12f8322f8613869170abd15cd8c8e330bbbee8a6da675270fda3a7bc` |
| `recipe_m1_shared.json` | `0828ae13255897d8bea25ba5fd28445835f374189e837b41b9f818bb017577d7` |
| `recipe_m2_app_clip_scalar_fields.json` | `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06` |
| `recipe_m2_app_track_label.json` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` |
| `recipe_m2_clip_add.json` | `5e9a54e75a0901724dedd3e62c0f37f78840a8edee001f30b92306383800479b` |
| `recipe_m2_clip_split.json` | `a0e24c1f78d8580f908973745950ed0196c17257831197ec2f75a55abc638f63` |
| `recipe_m2_clip_trim.json` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` |
| `recipe_m2_occurrence_media.json` | `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46` |
| `recipe_m2_placement.json` | `7404b665b2918ebf095abc68bd3a20176afb0589b79cf785887c1da50b68d271` |
| `recipe_m2_scalar_disjoint.json` | `0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866` |
| `recipe_m2_scalar_params_absent.json` | `9687956ee3850c5d873580a28cd6e8354f0b76dcb9a17bf56eb6ae0213f24b36` |
| `recipe_m2_scalar_params_null.json` | `15e945496b805af2554d78777be4585aa684615de575960352376f1dd4eaba74` |
| `recipe_m2_scalar_params_object.json` | `ae9f96e55432d0cf892f6045285e56265c6adc66058caf146bf4a7d7b1869638` |
| `recipe_m2_scalar_track.json` | `f982beb0493fbda9196d99c2dfb5200c26cb82d58cd23535b87eb7295747c75d` |

## Qualification

- Local bounded conformance/provider/sync/native CLI + pack/schema lane:
  **1496 passed, 4 existing platform skips, 65 integration deselected** (126.43s).
- Supplemental provider/reservation lane: **52 passed, 2 integration deselected**
  (3.84s). Canonical registry/closed args/reference union: **5 passed** (0.56s).
- Direct normal PARAM source pair, Runtime `b3ce5aa6`: **15 passed** (10.38s).
  No HTTP, mixed vendor-health claim, validator replacement or schema override.
- Direct frozen Runtime `6be9706` ordinary/popup/provenance/shared-image pair:
  **45 passed, 12 strict xfailed** (26.32s). The twelve popup positive/race
  expectations are unchanged and remain held for normal asset-schema generation.
- Final frozen Runtime HTTP proof: **95 passed, 13 strict xfailed** (106.65s),
  central exit 0 / 109s. Twelve popup cases plus the inherited first-clip
  nullable-speed case; no unexpected failures. One final-source request, exact
  snapshot tree matches the identity above. Result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-bundle2-complete-source-bundle1-runtime6be9706-integration-1020012332-852/`.
- Focused timeline/new-test Ruff passes; mypy for 11 touched timeline modules
  passes with Python 3.13 (the shared venv's actual version). Default project
  Python 3.11 checking hits installed NumPy's Python 3.12+ type syntax before
  checking source. Full changed-file Ruff reports 175 existing/reviewed compact
  style/import findings; no claim of a clean full lint gate. Four compact-style
  fixture findings originate in exact approved portable-pack `b2b51c4a` additions;
  the affected files retain their reviewed source, including the
  reviewed one-line model trim fix. No lint weakening or formatting churn.
- Vendor lock against exact `6be9706`, unchanged frozen vendor, 47 byte/delta
  checks, schema semantic union, M1 capture byte parity, and `git diff --check` pass.

Exact commands and results are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-complete-source/notes/report.md`.
No full suite / make check, installs, App/browser runs, release/artifact generation,
new Runtime contract qualification, merges, pushes or integration writes occurred.

## Blocking followups before release

1. Manager records the harness commit (helper above), reviews this exact tree and
   freezes source. All M2 integration stays HELD until PLAN records M1.
2. Resolve PARAM admission-object overfetch under the independent object-scope
   review; do not pull its WIP into this candidate. Any accepted fix requires a
   reviewed new source identity and bounded source-pair qualification.
3. Runtime owner generates normal official Python/TypeScript artifacts and root
   exports from this exact canonical schema/union, including all 12 operations’ closed args,
   DocumentPin/schema_source, MediaSelection, PreparedCommit recorder sites,
   MatchedSnapshot/VerifiedDocumentObject and Protocol declarations. Runtime owns
   artifact manifest, provider compatibility tuple and version choice.
4. Agent/App consume the same official artifacts and refresh pins together.
   Re-run the unchanged twelve positive/race popup tests on the managed provider
   through acceptance/reload, restart/exact retry, changed-key refusal, inverses,
   and lifecycle races. Source-pair results do not qualify that release tuple.
5. App owner qualifies captures/browser consumers and zero legacy writers. No
   readiness inference from local passes or preserved popup xfails.

## Manager01:32 — canonical schema FREEZE for Runtime generation; product release pending
Verified committed d4743e2984cef0908fa0b6bef166aa801f2bde8f treefe87ed862652e309a2dc86fd4845e859d3da5a9a and exact canonical-schema SHA256472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9. The schema bytes and this branch are FROZEN as normal Runtime generation input. All12 registered operation args, root/scopedasset refs, MediaSelection andschema_source/DocumentPin union are reviewed; 47delta/bytechecks,1496+52+5focused PASS,15actualPARAM,45actual+12oldassetxfail and95central+13strictxfail are exact source evidence. This permits Runtime official generation NOW; it is NOT App-release or integration approval.
Final Agent product tuple will be a NEW descendant, including reviewed45c3f328 (exact selected object reads; managerindependent21PASS12.01s), normal media helper/codec and native batch cleanup as applicable, with bounded tests and official newpins. These followups do not authorize changing the frozen schema; any needed schema change gets a new explicitly published freeze, never mutation. New materialization map/item refs remain a later separately coordinated contract candidate. Bundle1 remains3bf/6be FROZEN. All M2 merges await PLAN M1.

## Runtime manager01:48 — Bundle2 GENERATED REVIEW CANDIDATE (not final consumer release)
Runtime branch `tl/rt-m2-bundle2-runtime-artifacts`, committed `d691ddadb4ef3f5881a25fa893b4fb812211f102`, tree `2fc57ada4ccc52365732b3ee93315a716f529cc7`; client `0.2.3`; SCHEMA_DIGEST `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6`; artifact version `sha256:0f3d217ba0f3ca51d580bf3938fb3df1361a561de5acae7a911d21a9eea8bd9e` (74 files). Canonical Agent source bytes exactly frozen d4743e2984cef0908fa0b6bef166aa801f2bde8f/schema `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`.
Manager reviewed generator/public-export changes, verified schema byte parity, generated/artifact checks, unchanged compiled TimelineConfig+store.py, and service method delta ONLY `_validate_project_document` pack validation. No held core/catalog/D13 cuts imported. Includes reviewed pack custody, six-line nesting safety and generated VerifiedDocumentObject/Protocol; all twelve ordinary/PARAM ops get closed args, native Python/TS root exports. Nested row projections/open extras/empty closed args corrected in authored generator, not outputs. Worker234 bounded +156 neighbors and offline wheel/TS tarball/type consumers PASS (overlapping checks not summed); no actual Agent/new-runtime pair/full/browser qualification yet.
NEXT Agent may pin THIS EXACT committed producer normally in a qualification branch and prove unchanged popup/PARAM/replay/undo/door cases. Include selected-object read scope45c3 and APPROVED M1 opaque-remap helper/historical-image preservation fixes in its product descendant; schema bytes remain frozen. Keep the public product release/App consumer pin blocked until new M1 regression and exact paired qualification pass. This Runtime tuple is UNFROZEN REVIEW CANDIDATE, not ready-for-App. Any needed correction must be an explicitly published new tuple, never silent mutation. Materialization-map/item refs and D13/historical selector are later separate contracts; Bundle1 refs/0.2.2 unchanged.
