# M2 writer bundle 2 — COMPOSED/REVIEWABLE; App release HELD

Latest qualification is recorded in the final section below. Historical sections
retain their original tuples and pending items; the final section supersedes
those items for the new candidate. Manager review/App qualification and PLAN's
M1 record still gate release/integration. No all-gate1 or all-M2 claim.

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

Manager01:54 status: frozenRuntime normal0.2.3 REVIEW candidate d691ddadb4ef3f5881a25fa893b4fb812211f102/tree2fc57ada, schemaa435/artifact0f3d; owned normalpin task agt-m2-bundle2-official-pin active, actualpopup12oldschema xfails nowreachXPASS onoriginalassertions andwillremoveonlythosegates. Productsuccessor45c+28561mixed+0edhold+pureliteral+approvedopaque active, originalschema472622bytesunchanged. OrdinarydependentABA 2590f86c+18productlines independentlyready40actual+535focused/162neighbors; separatesordinaryfinal-valueguards fromhistory-sensitiveUNDO whilekeepingidentityreplacement. Needsreview/composition, no frozenbranchmutation. Itsactualprobe exposed separate numericpublication revision_identity_mismatch (2→2.0/bool→1) BEFOREB; agt-m2-numeric-revision-integrity assigned exactcontentpinreuse investigation, no hash/equalitynormalization. No finalconsumerreleaseuntilM1opaquefix/exactredoqualification+fullpairedtuple.

## Reviewed product successor — agt-m2-bundle2-reviewed-successor (2026-10-20)

New candidate on `tl/agt-m2-bundle2-reviewed-successor`, base frozen `d4743e2984cef0908fa0b6bef166aa801f2bde8f`; harness commit pending. Applied selected deltas in order45c3f328→28561c7→0edcbc0, preserving d474's media/accepted-boundary/clear machinery; added only c17 split MIME/static-intent changes plus ccd pure-helper closure and direct tests. Current trim already supports native move static `for`; no trim/model product overlay. Applied exact875a9aff opaque remapper and opaque6 tests; all six passed before removing their restored exact-undo xfail. No M1 worker provider imported. Removed exactly four portable-fixture compact-style warnings.

Schema remains SHA256 `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`, twelve operations. All16 JSON goldens unchanged; M1+label also exact Bundle1 bytes. No pin/vendor/model change. PARAM adds reviewed selected snapshot dependency; hold after move records existing agreeing static `for` writes. No other capture footprint change requiring golden regeneration. No new xfails.

Final focused own-domain run: **1618 passed, 4 existing skips, 74 integration deselected** (239.23s). Actual clean Runtimeb3ce5aa custody/PARAM/provider: **22 passed** (35.14s). Actual clean frozen Runtime6be9706 direct scalar/shared/opaque/add-delete/occurrence-media/media-inverse: **53 passed, 12 unchanged old-assetref strict xfailed** (81.03s). Opaque6 also **6 passed with --runxfail** on b3 before marker removal. Fresh-interpreter native provider move→trim→undo import fence **1 passed** with legacy edits/model/Checkout/journal/renderer imports forbidden. Scoped Ruff clean on18 changed files; broader172→168 baseline findings, zero new. Native mypy7 files clean; broader ten-file104→104 identical baseline diagnostics. Vendor check, frozen invariants and diffcheck pass.

One mistaken direct invocation included daemon scalar/first-clip tests; interrupted exit130 with incomplete `FFx` output, not qualification. Replaced by the completed socket-free selection above. Nullable-speed test expectation/marker unchanged, not requalified; no socket/HTTP/browser success claim. Official0.2.3 and central exact-pair/App popup/legacy journeys remain pending. M2 integration **HELD until PLAN M1**; frozen d474 and Bundle1 untouched.

Exact commands, decisions, source manifest and logs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-reviewed-successor/notes/report.md`. Full diff including new opaque test: `notes/final.patch`, SHA256 `08e36e213132675502816a89205ceb80579b64710c2f53ce1178ecaa78aed973`. Both worker-root commit-message files ready; manager should record harness SHA here after commit, then coordinate the official pair without changing this task's pin.

## Release composition in progress — agt-m2-bundle2-release-compose

Working from exact `a31d712d4a5c9ad08f385e12d71d3f1f7cbfef83` in
`/home/user/work/wt/agt-m2-bundle2-release-compose`. Applied only f423's six-file
normal d691 pin/test delta, a95c native batches and 2590 ordinary replay delta,
retaining M2 state-aware inverse and PARAM forwarding. Added the missing a76
shared sibling/ABA/redo controls and exact reverse-source-alias tests; retained
the existing roundtrip and M2 provider. Initial modified recipe/sync/CLI run:
424 passed (30.25s); normal vendor and CLI surface checks pass. Direct official
d691 service-only popup/PARAM/scalar/identity/opaque qualification is running.

Numeric source `3eae37799447d476c7b82abddef66d230436384f` is now committed;
composition awaits explicit manager review, as assigned. Runtime null-speed
successor `65abc5d` is explicitly awaiting replacement of its rejected SQL-based
fixture (Runtime manager02:04); d691 remains the pin here. No central request
has been submitted: preserve the single final larger-cohort request for the
reviewed final producer/numeric tuple. Until that coordination finishes this
candidate is **HOLD**, with no App readiness claim. Frozen d474/schema472622 and
Bundle1 remain untouched. This paragraph records progress, not a final source
identity or release approval.


## Final ordinary release composition — new candidate HOLD (2026-10-20)

| Field | Exact value |
|---|---|
| Branch | `tl/agt-m2-bundle2-release-compose` |
| Worktree | `/home/user/work/wt/agt-m2-bundle2-release-compose` |
| Current pre-harness HEAD/base | `a31d712d4a5c9ad08f385e12d71d3f1f7cbfef83` |
| New candidate commit | **PENDING RELEASE-COMPOSE HARNESS COMMIT** |
| Exact final tested source tree | `3143c1e88522fed078ef1068a431fec7bee57ee3` |
| Runtime producer pin | `d691ddadb4ef3f5881a25fa893b4fb812211f102` |
| Runtime producer tree | `2fc57ada4ccc52365732b3ee93315a716f529cc7` |
| Client | `0.2.3` |
| Official SCHEMA_DIGEST | `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6` |
| Official artifact version | `sha256:0f3d217ba0f3ca51d580bf3938fb3df1361a561de5acae7a911d21a9eea8bd9e` |
| Canonical schema SHA256 | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` |
| Runtime lock SHA256 | `76695bbcb15945aa891edfdc7e379b80c971dbfabbaae4b406855c53ebee4deb` |

The harness commits after worker exit. Manager must run
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-release-compose/notes/finalize-handoff.py`
to verify the exact tree/parent and publish the actual new HEAD here. Pending
HEAD is not a freeze identity; the base SHA must not be substituted for it.

Composition is bounded to exact f423 six-file official pin/old-popup-xfail delta,
exact a95c native batch/CLI/surface delta, reviewed2590 ordinary ABA delta with
current state-aware inverse/source-root identities and PARAM forwarding retained,
and additional a76 permanent M1 controls only. Current a31 helper/history/provider
remain unchanged. Original capture/value/identity claims survive command-file
batches and normal outbox-prefix retry. Four newer recipe files reconcile sixteen
old ordinary equal-state refusals to require exact successful replay; all inverse
ABA and structural identity/container refusals remain. No passing positive was
changed to refusal, skipped, deleted or newly xfailed. No NativeSheet overlay was
needed to preserve calls; existing sheet module is byte-identical to a31 and its
tests pass. No grammar, operation, schema, map, producer guard, legacy cut,
renderer, model or unrelated pin expansion. Frozen d474/schema472622 and Bundle1
refs remain untouched; f423 leased worktree was never changed.

Final focused conformance/provider/rebase/sync/CLI/sheet/schema/golden lane:
**1578 passed, 5 skipped, 119 integration deselected in190.57s**, exit0.
Actual exact official d691 direct service pair, normal schemas/admissions:
**96 passed in99.55s**, exit0, no xfail. This includes all unchanged popup/race
positives after the12 old-schema marker removals, selected PARAM/scope controls,
media/scalar/identity/opaque and all shared undo/redo/ABA controls. It proves21
socket-free M1 obligations; the other2 daemon obligations and all23 together on
this larger pair still require central qualification. No direct HTTP/daemon ran.
Scoped Ruff clean; all changed Python scope has76 identical baseline diagnostics
(CLI15/generated61), zero new. Five native modules mypy clean; adding cli_parser
reports its one identical preexisting parse_args override error. Normal vendor
and CLI generator checks, exact-byte/golden/registry audit and diffcheck pass.
Initial broad16FAIL expectations are disclosed and reconciled in the report;
no full suite or skipped/weakened behavior to achieve green.

**Release HOLD:** numeric3eae37799447d476c7b82abddef66d230436384f is committed
but explicit manager review approval was not published at this handoff; it is
excluded as required. d691 does NOT contain nullable firstclip fix.65abc5d had
2centralfirstclipPASS but its SQL-rewrite fixture was rejected; clean successor
still active. Do not relabel d691/f423 as fixed or silently repoint the producer.
Manager must compose approved numeric changes onto this M2 provider, then consume
an explicitly published clean Runtime descendant through normal pin refresh.
A permitted own `agent bundle2-runtime-integration` suite line now contains exact
d691 preflight plus firstclip+M1+nativebatch+clientcutover+popup/PARAM/scalar/media.
**Zero central requests submitted**: keep the single final larger-cohort request
for the final reviewed source/pin. Update its exact Runtime SHA/path together
with the normal pin; all23 M1 obligations must pass in that final cohort. The
inherited nullable firstclip xfail remains unchanged. No App readiness/qualification
or all-M2 completion claim; M2 integration remains held until PLAN M1.

Capture exports below are unchanged; each is prefixed `astrid.sdk.timeline.`.
`sync.TimelineSession.queue_many/commit_many` is now the atomic batch ingress;
`queue/commit` continue as one-command adapters. CLI commands-file requires both
original immutable basis IDs. All12 registered ordinary args remain closed,v1.

| Operation | Capture export |
|---|---|
| `clip.move` | `capture.capture_move` |
| `placement.move` | `native_placement_commands.capture_placement` |
| `clip.delete` | `capture.capture_clip_delete` |
| `clip.add` | `_clip_commands.capture_clip_add` |
| `clip.set` | `_clip_scalar_commands.capture_clip_set` |
| `clip.trim` | `_trim_commands.capture_clip_trim` |
| `clip.split` | `_split_commands.capture_clip_split` |
| `clip.set-params` | `_scalar_commands.capture_clip_set_params` |
| `track.create` | `capture.capture_track_create` |
| `track.set` | `_track_commands.capture_track_set` |
| `occurrence.add-media` | `native_occurrence_media_commands.capture_occurrence_add_media` |
| `occurrence.swap-media` | `native_occurrence_media_commands.capture_occurrence_swap_media` |

All16 final goldens below are byte-identical to frozen d474; M1+track-label also
match Bundle1 (61722 combined bytes). Absolute final fixture root:
`/home/user/work/wt/agt-m2-bundle2-release-compose/tests/editing_conformance/fixtures/`.

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

Exact commands/results, decisions, limits and source manifest:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-release-compose/notes/report.md`
and neighboring `final-manifest.json`, `audit.py`, logs and `final.patch`.
Both worker-root commit-message files are ready. No build/temp output remains
in the worktree. This is a bounded twelve-ordinary-writer review candidate.
Complete patch SHA256 `6cbaabe11ce3ace7ddf34f727f5e046e9213ac59204fa8711f0557d9b017faa3`.


## rt-m2-popup-verified-media-read — final ordinary 0.2.6 UNFROZEN candidate
Source branch `tl/rt-m2-popup-verified-media-read`, base `d691ddadb4ef3f5881a25fa893b4fb812211f102`; **harness commit pending**. EXACT final central/current source tree **d9b5af4279bcb69aaa68b6e4056fcfce588437c7**, all340blobs verified. Manager must obtain final harness SHA after exit; base HEAD is not the candidate source. No source edits after final central snapshot.

Normal GET `/v1/projects/{project_id}/media-selection/verified`, operation `getProjectVerifiedMedia`, five REQUIRED query strings `{asset,generation_id,variant_id,object_id,catalog_digest}` → EXISTING `{selection,media_type,size,duration_seconds?,width?,height?}` VerifiedMedia, no envelope. Python `get_project_verified_media(project_id, selection: MediaSelection) -> VerifiedMedia`; TS `getProjectVerifiedMedia(projectId, selection: MediaSelection): Promise<VerifiedMedia>`; both root VerifiedMedia exports. Existing original selection operation/schema/response/verifier/acceptance/ABI/schema bundle unchanged. Same projects:read/actor/origin/credential/project+mutex checks, mutationFalse; no new client authority/hydrator/hash/DTO/table/provenance/fallback.

Officialversion **0.2.6**; canonical ordinary schema rawSHA256 **472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9** unchanged; RuntimeSCHEMA **sha256:f6b8bfd4159037c3a33f43332cad588a8cc1d90db9e571e0dd93e9fa38a9fcc8**; aggregateartifact **sha256:2579b3d1d163d52641e8fdd36f3b1f0cb7e9a7a336275c1bef03a0e11cb0a125**; artifacts.json rawSHA256 **b0801b6fe74f260a72d98ca317e88f3abd547a9e03caf0d52cd2b49d79b1a869**. Py generatedSHA256 **56de15bd14b22744431252b54f2c4a39bd0db515b2d99e8d40167bb2e87373fa**; TS generatedSHA256 **411689d44fffb6f7fda1b6170ff1ad9f3e0d42b60235a8932d330f414dd5bc75**. Normal generators/conformance/manifests, offline wheel and packed TS consumer PASS. Producer0.2.4/item0.2.5 feature unions not included.

Only announced committed M1 nullspeed files selectively consumed: d79758d8601c8ff40f4754c70b11312a93338aaf product/native tests +6db1d88c6c08fe8784ae323ce496573dc3bca4f5 genuine retained tests (announced219tree); no rejected65SQLfixture. Focused105PASS; central `rt-m2-popup-verified-media-read-targeted-1020022215-21879` **102PASS51.71s**, same d9b5aftree, actual settled ffmpeg PNG/old+new video, public generated read+door auth/origin/scope/query/object/digest/catalogmetadata/lifecycle/version refusals, ALL SQL/CAS unchanged; originaldoor/readlocks/retainednullneighborsPASS. Broaderneighbor/generator lane1466PASS/1FAIL/1deselected: inherited duplicate-add fixture select parent/clip:clip rejected by frozen clip.add parent rule, independently reproduced untouchedd691 (same1FAIL). Original expectation retained, no weaken/skip/xfail. Reports exactcommands+limits ONLY `workers/rt-m2-popup-verified-media-read/notes/report.md` and report.md.

**UNFROZEN review candidate**: manager review+final sourceSHA publication → normal Agent0.2.6 pin/exact popup+PARAM qualification → App-owned adapter/media-selection-integration extension/QA required. No final App pair or full suite/M2 merge/oldwriterretirement claimed. Bounded proof complete; stopping for harness commit.


## Final exact ordinary/PARAM/popup qualification — agt-m2-bundle2-final-qualify

Status: **COMPOSED/REVIEWABLE, not App READY**. Runtime owner02:22 reviewed the
exact4c145 successor with no correction. Agent final paired lane passes; manager
source review/freeze and App qualification remain. All M2 integration waits for
PLAN's M1 record. The following identities supersede historical pending items
above only for this new candidate; no old source/ref was changed.

| Field | Exact value |
|---|---|
| Branch | `tl/agt-m2-bundle2-final-qualify` |
| Worktree | `/home/user/work/wt/agt-m2-bundle2-final-qualify` |
| Current source HEAD / harness parent | `8c9c7428b070dc69c40bd3bb8ce573e8322418d2` |
| Verified predecessor tree | `3143c1e88522fed078ef1068a431fec7bee57ee3` |
| Candidate commit | **PENDING FINAL-QUALIFY HARNESS COMMIT** |
| Central tested tree | `5fb59b8957064256bd7c0c256d2304f54845b0bb` |
| Final source tree | `1434f42b48fd062248faf1f4abef7ff467186377` |
| Runtime producer checkout | `/home/user/work/wt/rt-m2-null-speed-clean-candidate` |
| Runtime producer SHA | `4c145dc62192f0e942e3ee3922a11488aefe9b41` |
| Runtime producer tree | `f640ccf4aacb08e15f493bc7e3e5befe26ed0ceb` |
| Client | `0.2.3` |
| Official SCHEMA_DIGEST | `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6` |
| Official artifact version | `sha256:0f3d217ba0f3ca51d580bf3938fb3df1361a561de5acae7a911d21a9eea8bd9e` |
| Runtime artifact manifest raw SHA256 | `58e88352de9bf47969de2ce72e0c0ad8c3530560f0120d10eb067314a3603920` |
| Canonical schema SHA256 | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` |
| Runtime lock SHA256 | `8ea9e36e64d0664257f8dbeefaa61e465f96c8bc3c471caed0242941ec283414` |

Canonical schema: `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/core/timeline/schema/edit-command.schema.json`.
Normal vendor-lock update/check consumed exact committed4c145. All74 official
artifacts are byte-identicald691; only lock source identity changed. The approved
3eae numeric21-line product comparison delta and direct tests were applied to the
CURRENT M2 provider. Six M1 numeric MOVE cases match compatibled9a exactly and use
the new normal source. No M1/older provider/core overlay, new op/schema/producer
guard/materialization/renderer/global cut or fixture normalization.

Exactly one named central request `agt-m2-bundle2-final-qualify-bundle2-runtime-integration-1020022131-5967`: **207 passed in262.40s,
exit0 / service274s, no skip/xfail/failure**. Includes the entire29 M1 cohort on
THIS pair, nativebatch40/suffixBABA, popup48, selected-object/mixed PARAM20,
numeric PARAM19, SDK/CLI/clientcontract39, firstclip2, scalar/clear/media and
add-delete. Full command/results: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-final-qualify/notes/report.md`.
Central result/log directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-bundle2-final-qualify-bundle2-runtime-integration-1020022131-5967/`.
Default integration heads in service `ext` do not override explicit4c145 preflight.

Both UNCHANGED firstclip cases passed with `--runxfail` in that final run BEFORE
removing only the nullable-speed strict marker. Final tree differs from central
snapshot only by that required marker removal; test body and both cases are
unchanged. Audit reconstructs the tested tree using the original marker. No
product/pin/test-body change after request, no second request or relabeled tree.
Local focused290PASS33.06s, native renderer/legacy-import fence1PASS0.90s, scoped
Ruff/vendor/CLIgen/audit/diffcheck allPASS. Mypy has only the same two preexisting
union-attr errors as exact shadowed base. Full-suite/make-check was not run.

Harness commits after worker exit. Manager runs `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-final-qualify/notes/finalize-handoff.py` to
verify finaltree/parent and publish actual new HEAD. The current8c9 parent is not
that commit. Read-only predecessor verification confirms8c9/tree3143 and a31 parent;
no old finalization script or old source mutated.

Current captures below use prefix `astrid.sdk.timeline.`; all12 ops remainv1,
closed args. Batch ingress remains `sync.TimelineSession.queue_many/commit_many`.

| Operation | Capture export | Absolute source path |
|---|---|---|
| `clip.move` | `capture.capture_move` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/capture.py` |
| `placement.move` | `native_placement_commands.capture_placement` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/native_placement_commands.py` |
| `clip.delete` | `capture.capture_clip_delete` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/capture.py` |
| `clip.add` | `_clip_commands.capture_clip_add` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/_clip_commands.py` |
| `clip.set` | `_clip_scalar_commands.capture_clip_set` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/_clip_scalar_commands.py` |
| `clip.trim` | `_trim_commands.capture_clip_trim` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/_trim_commands.py` |
| `clip.split` | `_split_commands.capture_clip_split` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/_split_commands.py` |
| `clip.set-params` | `_scalar_commands.capture_clip_set_params` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/_scalar_commands.py` |
| `track.create` | `capture.capture_track_create` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/capture.py` |
| `track.set` | `_track_commands.capture_track_set` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/_track_commands.py` |
| `occurrence.add-media` | `native_occurrence_media_commands.capture_occurrence_add_media` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/native_occurrence_media_commands.py` |
| `occurrence.swap-media` | `native_occurrence_media_commands.capture_occurrence_swap_media` | `/home/user/work/wt/agt-m2-bundle2-final-qualify/astrid/sdk/timeline/native_occurrence_media_commands.py` |

All16 goldens are byte-identical frozen d474; M1+track-label also match Bundle1.

| Absolute golden path | SHA256 |
|---|---|
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_clip_delete.json` | `091bc1c7fa9c57583dde8fcc6d6af9226513bf4f214369ef0892cc1db492f0aa` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m1_move.json` | `e1dc5fc72e42fa90aed3e46ccd3bb95e219004bddd2917dc99f0154cf768dba0` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m1_occurrence.json` | `dba00dff12f8322f8613869170abd15cd8c8e330bbbee8a6da675270fda3a7bc` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m1_shared.json` | `0828ae13255897d8bea25ba5fd28445835f374189e837b41b9f818bb017577d7` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_app_clip_scalar_fields.json` | `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_app_track_label.json` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_clip_add.json` | `5e9a54e75a0901724dedd3e62c0f37f78840a8edee001f30b92306383800479b` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_clip_split.json` | `a0e24c1f78d8580f908973745950ed0196c17257831197ec2f75a55abc638f63` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_clip_trim.json` | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_occurrence_media.json` | `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_placement.json` | `7404b665b2918ebf095abc68bd3a20176afb0589b79cf785887c1da50b68d271` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_scalar_disjoint.json` | `0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_scalar_params_absent.json` | `9687956ee3850c5d873580a28cd6e8354f0b76dcb9a17bf56eb6ae0213f24b36` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_scalar_params_null.json` | `15e945496b805af2554d78777be4585aa684615de575960352376f1dd4eaba74` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_scalar_params_object.json` | `ae9f96e55432d0cf892f6045285e56265c6adc66058caf146bf4a7d7b1869638` |
| `/home/user/work/wt/agt-m2-bundle2-final-qualify/tests/editing_conformance/fixtures/recipe_m2_scalar_track.json` | `f982beb0493fbda9196d99c2dfb5200c26cb82d58cd23535b87eb7295747c75d` |

Unsupported remaining cases: CLI/commands-file does not supply custom-pack
selected-schema capture inputs (`schema_inputs`/`realm_id`); refusal preserves
file/outbox. Native SDK/provider tests do not qualify that CLI surface. App's
actual browser/popup/PARAM pair, full suite, macOS, owner film and pixel/audio
parity are unverified here. No all-gate1/all-M2 completion or App readiness claim.
M2 integration stays HELD until PLAN M1 and manager approval; all frozen/leased
refs remain unchanged. Capture/golden/source manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-final-qualify/notes/final-manifest.json`;
exact report/commands/limitations: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-final-qualify/notes/report.md`.


## Runtime manager02:33 — public popup read REVIEWED 0.2.6 candidate
Exact tl/rt-m2-popup-verified-media-read a9a81078e2aa30f071f84d3c64e1025e9ed62df1/tree d9b5af4279bcb69aaa68b6e4056fcfce588437c7, clients0.2.6, canonical472622 unchanged, RuntimeSCHEMAsha256:f6b8bfd4159037c3a33f43332cad588a8cc1d90db9e571e0dd93e9fa38a9fcc8, artifactsha256:2579b3d1d163d52641e8fdd36f3b1f0cb7e9a7a336275c1bef03a0e11cb0a125. Managerreviewednarrowservice/route/door/query/generator: existingMediaReads.selected+scope/mutex, SAME5fields, noauthoritycopylogic. M1nullfix+genuinetestsincluded; noD13/itempartialunion.
GET /v1/projects/{project_id}/media-selection/verified/getProjectVerifiedMedia, queryrequired {asset,generation_id,variant_id,object_id,catalog_digest}; rawexistingVerifiedMediaresponse {selection,media_type,size,duration_seconds?,width?,height?}. Pyget_project_verified_media(project_id,selection:MediaSelection), TSgetProjectVerifiedMedia(projectId,selection:MediaSelection). OriginalgetProjectMediaSelectionresponseunchanged. Central102PASS(realsettledPNG/old+newffmpegvideo, exactaliases/catalog/object/scope/lifecycle/versionraces/origin/auth/allSQL+CASunchanged),105focused; normalgenerator/conformance/artifact/offlinewheel/packedTS PASS. Broader1466PASS/1inheritedbadclipaddfixture handledbyRuntimec82b56f6(testonly94PASS). No full/newactualApppairclaim.
UNFROZENreviewcandidateforadapter+normalownedpinpreparation; finalsourcecohortmustcomposemandatorycompatgate550ff4ee andknownDoorcreateTimelinePOSTfix(currentallowlistGETonly; rt-m2-empty-timeline-door-route active). Theseareproduct/test/toolingonly, artifacts expectedunchangedunlesswirechangeproven. Oldordinary0.2.3 4c145proofstaysvalidonitsexacttuple; nevermutate/refreeze. CoordinateNEXT0.2.6normalAgent/Apppinsasonechange, then actualpopupADD/SWAPmedia-selection-integration+PARAM/ordinaryQA. Appmaybuildadapteragainstthisexactreviewedmethodnow; nofinalintegrationadoptionuntilreleasequalification/globalM1record.
