# App bootstrap adoption review: `timeline.init` v1

2026-10-20. **Design review complete; adoption remains HELD.** The Agent candidate covers the exact fresh App authored defaults through existing commands. It does not yet provide a complete replacement for all seven App positives: truly headless same-ID repair, the Door collection POST prerequisite, and App pre-create durability/wiring remain open. No candidate, pin, product, generated source, or test was changed. App mergers remain HELD until the **04:17 opaque-root writer closure** is reviewed; this report does not clear that hold.

## Fixed sources and decision

- App base: `5912bfc3284da03112ef6c235447cfbeffb678bd` (`tl/app-m2-bootstrap-init-contract-review`). Paths below are relative to this App unless marked otherwise.
- Agent: `31d02d45ad21f452724091b94b285478d00c9c21`, `hub/tl/agt-m2-bundle2-popup-init`, read with `git archive` from `/home/user/work/agent`. Native contract: `astrid/sdk/timeline/_init_commands.py:10-37`, schema `astrid/core/timeline/schema/edit-command.schema.json:408-463`, `docs/design/m2-empty-bootstrap-init.md`, and exact `tests/editing_conformance/fixtures/recipe_m2_timeline_init.json`.
- Runtime: `43fd77e5e5f8898d69bbda14a85a44f2ee40d76b`, read with `git show` from `/home/user/work/runtime`. Its separate Door-route prerequisite was not combined or adopted.
- Read `PLAN.md` and `design/app-writer-contract-gaps.md`. The task's “PLAN 03:20” bootstrap decision is preserved verbatim in `managers/app/INBOX.md:628-634`; this PLAN copy does not itself contain that timestamped bootstrap entry. It requires constrained same-ID repair, guarded output/name/slug/assets initialization, retained seven positives, and no defaults reapplied after edits/undo. The 04:17 hold is at `managers/app/INBOX.md:728-732`.

## Exact fresh creation mapping

1. Use the existing generated `createTimeline(projectId, timelineId, key, name?)`: `POST /v1/projects/{project}/timelines`, body `{timeline_id, name?}` and an unchanged `Idempotency-Key`. This is normal creation, not a snapshot payload. With its startup provider registered, Runtime `service.py:1887-1930` atomically creates the resource and accepted empty bootstrap.
2. Retain the returned **revision and publication pair**, H0 = `(data.head_revision_id, data.head_publication_id)`, and the ordinary `timeline.create` receipt. H0's publication is the bootstrap `parent_composition.publish` receipt, **not** the create receipt ID. Verify H0 against normal commit history and immutable parent reads. `loadTimelineCommandBasis` (`dataProvider.ts:777-819`) already provides checked history/manifest/scope reads, though it loads the current head, not automatically the historical H0.
3. On the exact verified native empty bundle, call published `capture_timeline_init(bundle, name=..., slug=..., output=...)`. Execute that command locally, capture `track.create` for V1 against its result, then capture A1 against the V1 result. Submit **one** normal commit at H0 with `[init, V1-create, A1-create]`. Capture each command against its predecessor's authored result; do not capture all three independently on H0.
4. Complete UI creation and project-pointer selection only after a verified accepted/reloaded initialized basis. Create's H0 is a legitimate intermediate accepted revision; the settled create→init recipe is two transactions, not an invented cross-operation transaction. An interrupted create must remain resumable rather than being reported as fully initialized.

The probe compiled that batch and compared the entire publication payload, not just displayed config:

```json
{
  "name": "Main",
  "slug": "main",
  "config": {
    "clips": [],
    "tracks": [
      {"id":"V1","kind":"visual","label":"V1","scale":1,"fit":"contain","opacity":1,"blendMode":"normal"},
      {"id":"A1","kind":"audio","label":"A1","scale":1,"fit":"contain","opacity":1,"blendMode":"normal"}
    ],
    "output": {"resolution":"1280x720","fps":30,"file":"output.mp4","background":null,"background_scale":null}
  },
  "registry": {"assets": {}},
  "clips": [],
  "occurrences": []
}
```

This exactly matches `defaults.ts:4-52` and `createDefaultTimeline.ts:48-67`; theme, theme_overrides and generation_defaults remain absent. Init records, in order, whole `config.output`, `name`, `slug`, `registry`; before states are ABSENT/ABSENT/ABSENT/PRESENT `{}`. Both null output leaves are present values. Init creates no IDs. Track commands record `parent/track:V1` then `parent/track:A1`; row order and every row field match App. Probe also passed `Timeline 2`/`timeline-2` and the current punctuation-slug fallback `!!!`/`timeline`. The published golden uses `My Timeline`/`my-timeline`; its **bundle, full captured command, after-bundle and actual records** all match exactly. Full-batch inverse restores the original empty bundle, inverse-of-inverse restores the defaults, and deterministic replay preserves records. These are native engine results, not Runtime admission evidence.

**FPS:** the new operation accepts integer fps only. Actual App creation uses integer **30**, which passes. Rational objects `30000/1001` and even `30/1`, and decimal `29.97`, are refused as `invalid_edit_command`. Existing neighboring move quantization at rational fps passed. Preserve that wider timeline/compiler behavior; this fixed-default initialization review gives no reason to widen the init schema or round a rational request. Arbitrary caller-supplied names are not all covered: init requires a nonempty name; Runtime resource creation trims and limits names to 120 characters. Actual Main/Timeline-N names meet both; arbitrary empty/overlong helper inputs are not qualified here.

## All seven original positives remain requirements

These are the unchanged tests in `src/integrations/runtime/createDefaultTimeline.test.ts`. The proposed route assertions below replace publisher-specific transport assertions only when qualified; every existing successful behavior stays asserted.

| Original positive / line | Mapping to existing legal commands and preserved result |
|---|---|
| Existing canonical head reuse, 20 | Honor active/default selection and return `main-id` with **no create/init/track write** for an established timeline. Verify readiness using the publication/revision pair and history rather than a truthy revision alone. An outstanding own creation is resumed before generic head reuse can discard it. Never initialize an established head merely because its current bytes happen to be empty. |
| Atomic fresh creation, 30 | Preserve deterministic Main identity; legal create installs H0 atomically, then one guarded `[timeline.init, track.create V1, track.create A1]` commit installs all App defaults atomically. Assert exact accepted reload of output/nulls/name/slug/assets/tracks/order and no duplicate timeline. Preserve positive completion across the legal intermediate H0. No composition publisher call. |
| Same-ID headless repair, 60 | Keep the selected `headless-shell` identity. Same-ID legal create must yield a verified empty H0, then the same Main/default command batch. Candidate only covers the narrower unpublished-revision shell; the test's null-head input remains a **blocking missing positive**, not a refusal test (details below). Repair must not allocate a replacement timeline. |
| Reassigned Main pointer, 72 | Return active `metadata.default_timeline_id = chosen`; leave both established compositions and metadata unchanged. No create/init/track write. A timeline named main never overrides this pointer. |
| Metadata CAS with concurrent chat, 83 | Finish create/init once; retain `createDefaultTimeline.ts:119-133`'s latest-version project CAS and metadata spread. After 409, reread and preserve chat/unrelated data. Do not recreate or reinitialize on the metadata retry; a concurrent Main reassignment still wins. |
| Additional named timeline, 95 | Keep explicit `project-timeline-2`, name `Timeline 2`, slug `timeline-2`, and key `astrid-timeline-create-project-id-project-timeline-2` as the original legal create identity; commit the same defaults/tracks with those name/slug args and a distinct persisted commit key. Random additional IDs must be durably allocated before create (below). |
| Lost-ACK stable first creation, 113 | Replace its two identical composition POST expectations with identical **legal create** request/key on uncertain create, and identical persisted **commit** request/key on uncertain init. Retry even if discovery now sees the created resource. Verify one creation/bootstrap/init result after reload/restart, without regenerating commands or advancing their base to today's head. The existing test uses a pure fake transport and is not real Door or crash evidence. |

## Proof of pristine history, not just pristine bytes

`_init_commands.py:16` checks exact parent bytes plus empty placements/shots. It refuses opaque root/config additions, including null theme and own `__proto__`/`constructor` keys, before writing; it does not merge or erase them. The executable diagnostic verifies input immutability on refusal.

**Concrete correction to an overbroad candidate-doc sentence:** the docs' Guards/Rebase paragraph says replay after editing and undo is `not_pristine`. Its later “Not covered” paragraph correctly limits this: exact state cannot distinguish never initialized from initialized then fully undone. The native probe confirms:

- init → inverse returns the original bundle exactly;
- recapture on that undone bundle succeeds, and `replay(original_plan, undone_bundle)` **without history** also succeeds;
- supplying the real init+inverse records to replay refuses with **`intervening_write`**;
- the unchanged original captured init against still-initialized bytes fails earlier with `dependency_changed`; a fresh capture there fails `not_pristine`.

This is evidence to clarify the candidate claim, not a change to the settled decision or permission to bypass history. It proves state-only recapture is unsafe; it does not prove an actual Runtime accepted a second init.

A sufficient App caller proof uses existing authority inputs:

1. Resolve an exact pending creation/adoption request and its ordinary receipt. Validate project/timeline and the original returned H0 pair. If no own request survives, normal Runtime history must prove the intended creation has **only its verified bootstrap entry** before starting a new init; a guessed ID, `name = Main`, metadata pointer, config equality, or client “initialized” flag is not proof.
2. Before constructing a **new** init request, read current history through a fixed head. Require current pair = H0, the matching bootstrap publication/receipt, `intent = bootstrap`, `previous = null`, and no later accepted publication. Verify the immutable closure equals the exact empty baseline with empty dependency lists. `HistoryPage` includes pairs, receipts, ancestry and records; follow `next_cursor` to the fixed terminal pair when history is longer. `Runtime timeline_commit_store.py:187-247` validates receipt/edge and cursor ancestry; `service.py:2722-2754` binds pagination to the original head.
3. If head has advanced, **never create a fresh init at that advanced head**, even if undo/restore made the payload byte-identical to bootstrap. If a persisted init is uncertain, retry its original request/key and original H0 instead. A matching accepted init in Runtime history establishes completion; read today's verified basis for display. A different intervening edit means preserve that authored state and retain/report unresolved local intent; no repair-by-defaults.
4. There is a race between read and send. Keep `base_revision_id/base_publication_id = H0` and the original native guards. Agent `commit.py:416-420,492-514` loads that original base, verifies publication pairing, reads complete intervening ancestry, and calls replay with its records. `rebase.py` calls `check_intervening` first. The pure init→undo history probe demonstrates rejection on this path. Recapturing at Hundo would bypass the original-history interval and is prohibited by the caller recipe. Track-ID reservations are not a substitute for this proof.

The Runtime retains accepted history after undo. Hundo may have the same content digest as H0 but has a different accepted pair and intervening records. No new DTO, init-status metadata authority, receipt ledger, or second client journal is needed. There is **no current App implementation of this proof**.

**Original create retry after head advances:** `service.py:1900-1904` returns `_command_replay` before collision/adoption. The exact original body/key returns its original create receipt and H0, never today's head; changed identity/name under that key conflicts. The existing Runtime source test `test_created_timeline_provenance_and_exact_retry_survive_restart` explicitly commits a later edit, replays create, compares original bytes, and asserts no row changes. It was read, not run here. A create first accepted without a provider returns no accepted pair; its original replay remains that headless result even after a later adoption. Do not turn an old no-provider receipt into authorization to initialize. A separate legal adoption has its own persisted identity and verified H0.

## Crash/outbox and metadata boundaries

Reuse the **one** IndexedDB outbox in `commands/commitOutbox.ts`, scoped by realm/actor/project/timeline, with explicit owner recovery and strict persistence before network. A local pending creation identity is request data, not Runtime history authority.

| Crash boundary | Required resume behavior |
|---|---|
| Before first create POST | Persist allocated timeline ID, exact create path/body/name/key and intended name/slug/default command inputs before sending. Failure to persist prevents dispatch. |
| Create committed; ACK lost, or ACK not persisted | Replay that same create request/key. Recover its original receipt/H0; do not allocate another timeline or infer current readiness from list results. |
| Create ACK persisted; init not yet reserved/sent | Apply the pristine-history proof above, capture against verified H0, and durably reserve the exact command request before send. Never fabricate an empty bundle from display defaults. |
| Init committed; ACK lost or process exits before storing ACK | Recover the original owner/request and retry its exact body/key/base/guards/allocated track IDs. Runtime idempotent lookup must return the original acceptance without another history edge. No fresh init. |
| Init acknowledged; later edits/undo; restart | Recover current verified history. An old create replay still names H0; it cannot authorize a new init. A late init ACK is a historical accepted result, not a reason to regress the displayed current head. `dataProvider.ts:754-770` already fences late accepted-cache replacement. |
| Init done; project metadata CAS incomplete/409/ACK lost | Reread project version/default pointer, preserve unrelated metadata, and finish only the existing metadata CAS. Do not rerun canonical initialization. |

**Concrete App gap:** existing outbox basis needs a real head pair or a predecessor intent (`commitOutbox.ts:11-16`); dispatch refuses any path except the canonical `/commit` (`:240-246`). `createTimelineCommandSession` also starts from an already verified canonical basis and exposes a move port/undo, not a bootstrap producer. Thus “just use the existing session” is insufficient before H0 exists. A narrow pre-create persistence phase must live in this same outbox and reuse its ownership/reservation/retry mechanics, then hand the verified H0 to normal command submission. Do not fake H0, use sessionStorage/ref as durable storage, or add a second journal. Its implementation remains later work.

**Stable identities:** Main currently derives UUID from `astrid-first-timeline:${projectId}` and uses `astrid-first-timeline-${projectId}` (`createDefaultTimeline.ts:32-38,111-115`). Retain that deterministic request identity. The old App-generated parent revision seed is not a substitute for Runtime's returned H0. `createCanonicalTimeline` uses an explicit timeline ID, else UUID of `astrid-timeline:${idempotencyKey}`, else randomness (`:79-88`). The extra-timeline UI allocates random ID/name in `pendingAdditionalTimeline` (`VideoEditorPage.tsx:700,1083-1107`), which survives a mounted retry but not reload/crash. Persist that actual ID/name/key in the existing outbox before the first POST; discovery plus a new random ID can create a duplicate. Even a deterministic helper ID does not preserve changed name/body or solve uncertain init; keep the exact request.

`metadata.default_timeline_id` is the existing **noncanonical project CAS**, never an authored init flag. Retain all 12 bounded rereads/retries, the latest metadata spread, and concurrent reassignment checks (`createDefaultTimeline.ts:119-133`). Its write key may change when constructing a new versioned CAS after 409, as today; that does not permit changing an uncertain create/commit request's identity.

## Remaining owner inputs and qualification

| Boundary | Exact evidence and smallest required follow-up |
|---|---|
| Truly headless resource: no parent head row or revision null | Runtime candidate `timeline_commit_store.py:809-810` rejects both. The diagnostic executes that exact guard expression for no row/null revision/unpublished revision/accepted head. Candidate tests first call `_shell`, publishing an empty revision, then adopt it; they do **not** exercise the App positive's null-head shape. Keep the original positive. Runtime must supply/prove the constrained same-ID truly-empty/no-head case through existing create/bootstrap machinery, or identify a normal authoritative input that already serves it. No App publication fallback to manufacture the missing revision. |
| Revision exists, publication null | Candidate can adopt only one exact empty unpublished parent, with no child/dependency/extra authored data, inside the same create transaction. `bootstrap_install_plan` requires exact empty canonical document and one entry, with `old_head = null` (`timeline_commit_baseline.py:429-443`). Scope/archive/provider/name checks are `service.py:1939-1946`. Do not require `name=Main` when adopting a shell with a different/null resource name: supplied name must match or be omitted; authored Main/slug remain explicit init args. Persist the chosen request unchanged. App currently treats any truthy revision as ready and misses this distinct headless shape. |
| Nonempty/opaque unpublished shell, headed resource, foreign project, archived or provider unavailable | Same-ID adoption stays closed: do not overwrite or default-fill these resources. A fresh create without a provider can still create a headless resource, so its success alone is not initialized success. The shell suite's source includes no-write nonempty/headed/name/project tests; no-provider/headless receipt behavior follows create's provider branch. These Runtime transactions were not executed here. A nonempty headless shell needs owner-proven history/migration authority, not bootstrap init. |
| Normal Door input | Pure execution of the candidate's actual `_entry`/`_find`/`_segment_matches` and route table returns collection GET=true, POST=false for `/v1/projects/project-id/timelines`. `door.py:157` is GET-only. Door POST is a separate prerequisite; this review does not bypass it with a service call or alternate route. |
| Normal App create/capture/submission input | `generated.ts:144` already has legal create with name/key and mutation envelope; `AstridRuntimeClient` has **no** `createTimeline` wrapper (diagnostic source assertion). Add the standard session/mutation wrapper later, preserving the generated DTO. This App base has no init/track-create capture module or general bootstrap submission port; consume exact native fixture/capture semantics through existing recorder/session work, not App-designed opnames or simplified hand-built guards. |
| History/authority inputs | Existing public history, immutable closure reads, create mutation receipt, and normal head-pair commit are sufficient for the caller proof. No missing public init-status DTO/endpoint was found. The integration and durable pre-create storage are missing; Runtime accepted/restart/race proof is unrun. Do not claim that source availability certifies the cross-product recipe. |

Smallest later App implementation task, **after** the root closure and official Agent/Runtime pair with Door + truly-headless positive: replace only `createDefaultTimeline.ts`'s publication path with the standard legal create wrapper, exact native init/track captures in one commit, original-H0 history gate, and narrow creation persistence in the existing outbox. Preserve selection, metadata CAS and extra-timeline request identity; retire `publishEmptyTimeline` only with all seven positives plus crash/restart/reload/undo/no-legacy tests green. A refusal is not a replacement for the repair positive. If a temporary product change removes it, retain the original success assertion with mandated `it.fails` and a restoration requirement comment. This review made no test change.

Later qualification must also cover concurrent initializers, init payload/key mismatch, track identity collision, provider absence, init→undo/restore followed by reopen, opaque nonempty refusal with unchanged history/draft, late historical ACK, real Door acceptance and zero composition-publish/timeline-document traffic. Retain `VideoEditorPage.test.tsx` empty-project/retry positives and local project CRUD coverage. Run browser/socket journeys centrally under the orchestrator rule only when the implementation brief authorizes them.

## Executed evidence and limits

Retained artifacts: `workers/app-m2-bootstrap-init-contract-review/notes/bootstrap-native-probe.py` and `.json`. Probe imports the unchanged Agent candidate archive; Runtime route/guard snippets are pure source extraction, **not** Runtime service/database/provider admission. No fake Runtime port, DTO, op, authority metadata, or alternate publisher was added.

Commands below use `NOTES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-init-contract-review/notes`.

- App cwd `/home/user/work/wt/app-m2-bootstrap-init-contract-review`:
  `node node_modules/vitest/vitest.mjs run src/integrations/runtime/createDefaultTimeline.test.ts --maxWorkers=1 --no-file-parallelism` → **1 file, 7 passed**, exit 0 (1.20s). Pure mocked transport; no sockets.
- Agent archive cwd `$NOTES/agent-source`:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_timeline_init.py tests/editing_conformance/test_recipe_m1_commands.py::test_track_create_inverse_redo_exact_opaque_row_and_identity_collision tests/editing_conformance/test_recipe_m1_commands.py::test_structural_group_uses_generic_creation_and_restores_order tests/editing_conformance/test_recipe_m1_commands.py::test_quantization_once_with_rational_fps_and_ms_codec` → **35 passed**, exit 0 (0.63s).
- App cwd:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$NOTES/agent-source" /home/user/work/venv-agent/bin/python "$NOTES/bootstrap-native-probe.py" > "$NOTES/bootstrap-native-probe.json"` → **exit 0**, exact fixture/default batches/inverse/redo/replay and diagnostic refusals/source boundary checks pass. Initial diagnostic expected `not_pristine` for a stale captured second init; actual guard failure was `dependency_changed`. The probe was corrected to distinguish original-capture refusal from fresh-capture refusal; no product test changed.

Archive was created by `git -C /home/user/work/agent archive 31d02d45 astrid tests pyproject.toml` and Python `tarfile` extraction into `$NOTES/agent-source`. It was removed after execution; to reproduce, extract that same read-only archive there and rerun the commands. Neither repo branch was checked out or changed.

**Unrun:** real Runtime create/adoption/commit/restart/receipt tests; App init/outbox recovery and UI integration; real Door/three-products/browser/socket journeys; full suites; typecheck/tsc/build/install. No central test-service request. No claim of real accepted bootstrap replacement, lost-ACK persistence, or writer retirement. No product/test/generated/root/Runtime/Agent edits; all seven original positives remain unchanged.
