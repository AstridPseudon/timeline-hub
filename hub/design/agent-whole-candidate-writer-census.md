# Agent whole-candidate writer census (agt-whole-candidate-census)

Read-only census. No repo changes, no ledger edits, no commit message (per brief).
Scope: `publish_authoring_candidate` and `promote_approved_authoring_candidate` in
`astrid/core/timeline/authoring_bundle.py`, and every caller of the whole-candidate
writer path. Worktree read: `/home/user/work/wt/agt-whole-candidate-census` (branch base).
Runtime state read: `/home/user/work/runtime` (HEAD `1f3e64d`, contains `fe756c8`).

Governing decision (INBOX 06:59Z, orchestrator, APPROVED): `promote_approved_authoring_candidate`
and `publish_authoring_candidate` are DELETED as the whole-document fallback writer; candidate
producers emit EditCommand proposals in the D13 / bundle #3 shape; the requesting client commits
them; approval binds to the **proposal** digest; no `candidate.apply`. Until both land, the
functions stay with ledger rows `held`, and Runtime does not re-retire the route.

---

## 0. Key findings (read first)

1. **The route is already refused at the Runtime tip.** `runtime_protocol/service.py:2598-2600`
   defines `publish_parent_composition` as `self._require_timeline_command()`, and
   `service.py:1604-1611` raises `RetiredRouteError("legacy timeline writes are retired; submit
   EditCommands through commitTimeline", replacement POST .../timelines/{timeline_id}/commit)`.
   This is the fe756c8 retirement (audit `audits/20261020T0627Z.md` line 24). So the "held" framing
   in the 06:59Z INBOX is not what the code does: every production caller of
   `publish_authoring_candidate` fails today against the Runtime tip. Only stub-writer tests pass.
   Not executed: running pytest in this sandbox needed approval and was denied. This finding is from
   reading the code, so treat it as strong evidence to verify, not as a test result.
2. **Runtime-backed tests will fail at the tip (expected, not executed):**
   `tests/timeline/test_authoring_bundle.py:1035` (`test_candidate_compiler_integrates_with_runtime_atomic_publication`)
   and `tests/timeline/test_authoring_media.py:270` (`test_real_runtime_import_and_parent_publication_roundtrip`)
   both call `service.publish_parent_composition` directly. Under the orchestrator rule they must not be
   rewritten to expect refusal. Recommend strict `xfail` with a reason naming the EditCommand
   replacement, or a decision from the orchestrator. Not changed here.
3. **The commit path already exists on main.** `RemoteTimelines.commit` (`astrid/sdk/remote.py:1504-1530`,
   `commit_timeline`) and `TimelineSession` (`astrid/sdk/timeline/sync.py:124-333`: `commit`, `move`,
   `undo`, outbox, flush) already commit EditCommands. The whole-candidate writer is the legacy path next to
   it, not the only path.
4. **Only two callers are truly single-command edits**, and both map cleanly to registered commands:
   `update-element` → `clip.set-element` (already approved in the INBOX), and `replace-parent-media` → one
   media swap. These are the first conversions.
5. **The only real Producer caller is voiceover sync** (`sync_draft_voiceover` →
   `TargetBoundAuthoringBundle.publish`). It is the clean "Producers propose, the requester commits" case.
6. **Approval/promotion has zero production callers.** `approve_authoring_candidate` and
   `promote_approved_authoring_candidate` are used only by `tests/timeline/test_authoring_bundle.py`
   and by re-export shims. They can be deleted or rewritten with no product impact.
7. **Adjacent callers of the same retired route, outside the whole-candidate path, are broken too:**
   `RemoteTimelines.create_empty` (`astrid/sdk/remote.py:480`, retired publish at 533-535), which backs
   `timelines create` (`astrid/packs/timeline/cli.py:186`) and `astrid/sdk/timeline_duplicate.py:156`.
   These must migrate before the Runtime route can be deleted. See section 4.

### Corrections to the brief's line references
- `promote_approved_authoring_candidate` is at `authoring_bundle.py:1538` (not ~1605).
- `publish_authoring_candidate` is at `authoring_bundle.py:1587` (not ~1640; 1640 is its `__all__` entry).
- `approve_authoring_candidate` (not named in the brief) is at `:1504`.

---

## 1. What the writer publishes

`compile_authoring_candidate` (`authoring_bundle.py:753-1116`) builds one `publication` dict
(`:1084-1116`): `project_id`, `timeline_id`, `expected_head`, `parent_revision_id`, `content_digest`,
`parent_composition` (final parent), `internal_timeline_revisions` (only referenced ones),
`shot_revisions` (only changed/referenced ones), and `dependency_manifest` = `{shots,
internal_timelines, media: [{media_id, content_digest}]}`. The writer sends that one object through
`writer.publish_parent_composition(...)`, which is one Runtime parent-CAS. So each caller publishes the
parent, changed shot revisions, changed internal-timeline revisions, and the media manifest together,
in a single CAS. A single-clip edit still ships the whole closure it touches.

---

## 2. Caller table

Legend. **Re-express?** = can the flow become EditCommand proposals committed by the requesting client
(PLAN "Producers propose edits"; D13 proposal shape from `design/m2-render-producer-contract.md:100-120`:
`{schema_version, producer, admitted_target, commands[], rationale, proposal_digest}`; commit ownership
from `design/render-commit-handoff.md`): **YES** = one or a few registered commands; **PARTIAL** = some
edits map and the rest must be refused or given commands first; **NO** = needs new design.

| # | Location (file:line) | Publishes | User-visible flow | Re-express as EditCommand proposal? | Tests that cover it |
|---|---|---|---|---|---|
| W1 | `astrid/core/timeline/authoring_bundle.py:1587-1622` `publish_authoring_candidate` (36 lines) | Full compiled publication (§1); feedback via `authoring_feedback.publication_feedback` | Wrapper; no direct user flow. Called by W3-W7 below. | Target of deletion. Replaced by "producer emits proposal; requester commits". | See §3 |
| W2 | `authoring_bundle.py:1538-1584` `promote_approved_authoring_candidate` (47 lines) | Same publication, gated by an approval artifact | **None in production.** Tests only (`test_authoring_bundle.py:471, 476, 623`). | Delete. Approval re-binds to the proposal digest (INBOX). | `test_authoring_bundle.py:458` (approval binding), `:483` (render restart then promote) |
| W3 | `authoring_bundle.py:1504-1535` `approve_authoring_candidate` (32 lines) | Nothing (detached approval object bound to candidate_digest, publication_digest, base_parent) | Approval flow; no product caller | **Rewrite**, not delete: bind to proposal digest. Net 0 lines removed now. | `test_authoring_bundle.py:458, 483` |
| W4 | `astrid/sdk/timeline/store.py:257-331` `publish_bundle` (75 lines) → `publish_authoring_candidate` at `:304` (via `_Writer` at `:299-303`) | Whole Checkout document after three-way merge onto head (`_merge`/`three_way` `:139-256`) | `timelines publish` (`astrid/packs/timeline/cli.py:2934` `_cmd_publish` → `Checkout.publish`); also the re-export at `astrid/sdk/timeline_checkout.py:154` | **PARTIAL.** Moves, track labels, timing, and media swap map to registered commands; cut-sheet `apply`, chapter restructure (`restructure=True`), and narration edits need command coverage or a clear refusal. `TimelineSession` (`sync.py`) is the target path. | `tests/sdk/test_timeline_publish_connection.py:54, 62` (2 tests); `tests/sdk/test_timeline_structure.py:77-97`; `tests/sdk/test_timeline_sync.py:144` (guard that `publish_bundle` is never called); stubs in `test_timeline_journal.py:179`, `test_timeline_transaction.py:235, 257`, `test_media_transcript.py:154`, `test_timeline_persistence.py:97`; behaviour in `test_timeline_transaction.py:214, 246` (publish resets base; failed reread) and `test_timeline_journal.py:160` (publish records message as reason) |
| W5 | `astrid/sdk/timeline/publish.py:27-84` `publish()` (58 lines), `:108-125` `_publish_narration` (second `publish_bundle` at `:115`) | Whole-document publish, then a second narration-pin publish | `timelines publish -m ...` and the narration pin. Narration pinning itself uses `shots.set_text_binding` (`remote.py:2446`), which is a non-candidate route. | **PARTIAL.** The narration second publish exists only because of whole-document publish; it becomes a text-binding command or disappears. | Same as W4 plus `tests/sdk/test_timeline_transaction.py:214, 246` |
| W6 | `astrid/sdk/remote.py:1278-1503` `replace_parent_media` (226 lines); publish at `:1468` (`publish_authoring_candidate`), `_Writer` `:1449-1462`, import `:1395` | One parent CAS: parent + one changed shot revision + changed internal timeline revision + manifest | `timelines replace-parent-media` (`cli.py:1286` `_cmd_replace_parent_media`; configure `:2407`; CommandSpec `:3944`). Documented in `astrid/packs/rendering/docs/SKILL.md:624` and `docs/guides/cli-journeys.md:497, 499, 614`. | **YES.** One registered media swap addressed by occurrence + clip (`occurrence_id`, `clip_id`, `source_object_id`), with an explicit intent: shared shot vs this occurrence only (PLAN §4.1). The media-selection read stays in Runtime. | `tests/test_timeline_clip_replacement.py:35` (publishes exact closure once; replace). `:96` is the CLI forwarding test and stays. `:10, :25` cover typed 410 for legacy `replace_clip` and are unaffected. |
| W7 | `astrid/sdk/timeline_elements.py:16-73` `update_parent_element` (73 lines); publish at `:64`, `Writer` `:57-63`, import `:11` | Parent CAS with one changed effect clip (hold, params, elementRef), plus legacy `config.clips` / `config.app.elements` mirror pruning | `timelines update-element` (`cli.py:1277` `_cmd_update_element`; configure `:2390`); SDK `remote.py:1259-1262` (thin wrapper) | **YES.** `clip.set-element` is already approved (INBOX 06:59Z): same-identity guard, recorded write, guarded inverse. Legacy mirror handling moves into the compiler's derived projection, not into writes. | `tests/core/test_timeline_element_publication.py`: 4 test functions, 7 cases (`:27` same-clip exact head; `:45` stale head / CAS; `:48, :55, :62` bad duration (parametrized 4); unadmitted owner/source clip) |
| W8 | `astrid/sdk/authoring_remote.py:230-326` `TargetBoundAuthoringBundle.publish` (97 lines); publish at `:310`; `_Writer` `:297-306`; key normalizer `_transport_idempotency_key` `:65-82` (18 lines) | Whole candidate after media-ownership checks (`get_project_object_location`, `verified`), then parent CAS | **Producer path.** `client.open_authoring_target(target).publish(candidate)` (`astrid/sdk/client.py:589-593`) ← `astrid/packs/video_editing/shared/draft_voiceover.py:475` ← `sync_draft_voiceover` (`:414`; action `astrid/packs/video_editing/actions/sync_draft_voiceover/run.py`). Docs `docs/timeline-editing-guide.md:86, 228` and `SKILL.md:329` use only `open()`. | **YES (cleanest Producer case).** TTS stores immutable audio media and proposes the clip/track/text-binding commands, with ripple/preserve as a declared intention. The producer never commits; the requesting client does. | `tests/timeline/test_authoring_feedback.py:254` (forwards feedback), `:275` (replay and stale decisions deferred to Runtime); `tests/timeline/test_authoring_bundle.py:403` (key normalizer); `tests/packs/video_editing/test_draft_voiceover.py`: fake coordinator `:176-199` (publish stub at `:197`), no-op `:211`, CAS failure `:221`, publish-once `:234`, regenerated audio `:243` |
| W9 | `astrid/packs/rendering/docs/scripts/timeline_document.py:215` publish; `Writer` `:88-99`; publish-only tail `:202-248`; import `:10-15` | Candidate after `plan_authoring_media` + `import_authoring_media` (catalog import stays), then the writer | Skill script `python3 scripts/timeline_document.py publish --file ...` (`astrid/packs/rendering/docs/references/document-checkout.md:32`; `SKILL.md:747-750` lists only checkout/bind-script/check, so the doc itself lags the script). | **PARTIAL→YES.** Diff of the JSON document → commands where registered; refuse the rest. `check` stays (read-only report). | `tests/timeline/test_authoring_feedback.py:210` (stdout/receipt shared feedback); `tests/timeline/test_authoring_media.py:227` (forwards new stale head to Runtime, via the script's publish); `:797` (locator path, check-side; keep) |
| W10 | Docs: `docs/timeline-editing-guide.md:263-294` (publish example `:294`); `docs/timeline-authoring-capabilities.md:12-28`; `astrid/packs/rendering/docs/SKILL.md:629-645` (ordinary-Python recipe, `publish_authoring_candidate(candidate, writer, ...)`) | n/a (docs) | Agent-facing instructions | Rewrite to: edit → validate → **propose** → commit via the requesting client. | Doc-level only; no test imports these snippets. |
| W11 | Exports: `astrid/sdk/__init__.py:78, 79, 80`; `astrid/sdk/authoring_bundle.py:9, 17, 18, 31, 42, 43`; `astrid/core/timeline/__init__.py:27, 325`; `authoring_bundle.py:1633-1640` (`__all__`) | n/a | Public SDK surface | Remove with W1-W3 (public API break; ledger row required). | Golden lists: `tests/timeline/test_timeline_characterization.py:199` (`GOLDEN_ALL`, `test_all_exact_contents` at `:205`); `tests/sdk/test_timeline_checkout_facade.py:32` (facade name list) |

### Read-side that must stay (not writers)
- `open_authoring_bundle`, `validate_authoring_candidate`, `diff_authoring_candidate`, `preview_authoring_candidate`,
  `inspect_authoring_candidate`, `authoring_media_inventory`, `compile_authoring_candidate` (until the candidate
  concept itself is retired; its publication assembly `:1084-1116` becomes dead only after W1-W3 are gone and
  preview no longer returns a publication digest).
- `astrid/core/timeline/authoring_feedback.py` (210 lines): **keep whole.** `publication_feedback` is also used by
  `astrid/core/timeline/authoring_revision_diff.py:10, 242` (saved-revision diff) and `authoring_change_summary` by `:261`.
  Only the publish wiring at `authoring_bundle.py:1603-1621` goes.
- `astrid/sdk/authoring_media.py` (636 lines): media import/catalog. It is a producer artifact, not a candidate writer. Keep.
- `RemoteTimelines.commit` and `TimelineSession`: the target path. Keep and extend.

---

## 3. Tests that need replacements (and how to hold them)

General rule (orchestrator): when a behaviour is removed temporarily, keep its original expectation and mark only
that test `xfail(strict=True)` with a comment naming the restoring requirement. Do not rewrite them to expect refusal.
For stub-only tests that patch `publish_bundle` / `publish_authoring_candidate` by module attribute, deletion will
raise `AttributeError` under `monkeypatch.setattr` (default `raising=True`): these need re-pointing, not just
deletion.

| Test (file:line) | What it protects | Replacement needed |
|---|---|---|
| `tests/timeline/test_authoring_bundle.py:421` publish one compilation, complete mapping | one compilation, identity mapping, next actions | Proposal test: one proposal, same identity mapping, same next actions |
| `:439` group move via publication boundary | occurrence order and timing in the publication | Proposal of a group-move command; same parent order assertions |
| `:458` approval bound to candidate and base | stale approval rejected | Approval bound to proposal digest and base revision |
| `:483` frozen render restart then approval promotion (single generation) | render replay + single promotion | Proposal promotion; keep render replay assertions. **Strict-xfail until proposal approval lands.** |
| `:1035` candidate compiler integrates with Runtime atomic publication (incl. replay `:1127`, newer-head `:1131`) | atomic publish, exact replay, later writer wins | Commit-path replay and rebase test. **Already failing at Runtime tip (§0.2).** |
| `:403` transport key normalization | Runtime key rules | Keep if a commit key normaliser remains; otherwise move |
| `tests/timeline/test_authoring_feedback.py:60-194` (9 tests via the `publish()` helper, `:52-58`) | receipt text, counts, next actions | Re-point to `authoring_change_summary` + `publication_feedback` directly. These are feedback tests, not writer tests. |
| `test_authoring_feedback.py:148` no-op publish | "No authored changes" text | Same as above |
| `test_authoring_feedback.py:210` script publish stdout/receipt | shared feedback on the script's publish | Script publish replacement (W9) |
| `test_authoring_feedback.py:254, :275` TargetBound forwarding and replay | feedback forwarded; replay/stale decided by Runtime | Commit-path forwarding and idempotent replay test |
| `tests/timeline/test_authoring_media.py:227` script forwards new stale head | stale head reaches Runtime, not a local check | Commit-path stale-head test |
| `test_authoring_media.py:270` real-runtime import and parent publication round trip (publish at `:387`) | catalog reuse across retries, parent CAS, saved revision | Commit-path variant. **Already failing at Runtime tip (§0.2).** |
| `test_authoring_media.py:769` catalog import reusable after later parent CAS conflict (`StaleWriter` `:779-783`) | conflict leaves catalog reusable | Commit-conflict variant |
| `tests/timeline/test_timeline_characterization.py:199` (`GOLDEN_ALL`) | export surface | Golden update, tied to the ledger row that removes the exports |
| `tests/sdk/test_timeline_checkout_facade.py:32` | facade name list includes `publish_bundle` | Golden update, tied to W4 |
| `tests/sdk/test_timeline_publish_connection.py:54, :62` | publish writes through the connection that read the head; no launcher | Commit-path equivalent. Keep the invariant. |
| `tests/sdk/test_timeline_structure.py:77-97` joined music publication | joined-music publication fields (`expected_head` etc.) | Command-level test for join-music |
| `tests/sdk/test_timeline_persistence.py:97` (stub of `authoring_bundle.publish_authoring_candidate`) | persistence after publish | Re-point the stub to the commit path |
| `tests/sdk/test_timeline_sync.py:144` (guard: `publish_bundle` must fail if called) | legacy writer never called | Keep the guard; after deletion assert the name is absent rather than patching it |
| `tests/sdk/test_timeline_journal.py:160, :179` | publish records message as reason, new head as evidence | Re-point stub; the record assertion stays |
| `tests/sdk/test_timeline_transaction.py:214, :235, :246, :257` | publish resets base; failed reread keeps old base and says so | Re-point stub; behaviour stays (commit-based reset) |
| `tests/sdk/test_media_transcript.py:154` | transcript sync after publish | Re-point stub |
| `tests/test_timeline_clip_replacement.py:35` replace publishes exact closure once | exact closure, one CAS, selected clip asset | Media-swap command test: one command, exact occurrence and clip, same asset result |
| `tests/test_timeline_clip_replacement.py:96` CLI forwarding | argument surface | **Keep** (CLI surface unchanged) |
| `tests/core/test_timeline_element_publication.py` (4 functions, 7 cases) | same-clip exact-head publish; stale CAS; bad duration; unadmitted owner. Also legacy `config.app.elements` pruning (`:27` assertions) | `clip.set-element` command tests. The legacy-mirror assertions stay as behaviour; **strict-xfail until the compiler derives the mirror** |
| `tests/packs/video_editing/test_draft_voiceover.py:176-240` (fake coordinator, `:197` publish stub; `:211, :221, :234, :243`) | no-op does not publish; CAS failure surfaces; publish once with provenance; regenerated audio | Producer-proposal tests: proposal emitted once with provenance; requester commit replaces the stub |

Count: about 45 test functions (roughly 55 cases) touch the writer path directly, plus stub-only patches in about 9 more.

---

## 4. Adjacent callers of the same retired Runtime route (not whole-candidate; must migrate before the Runtime route is deleted)

| Location | Use | Status now | Action |
|---|---|---|---|
| `astrid/sdk/remote.py:480-551` `RemoteTimelines.create_empty`, publish at `:533-535` | Creates an empty timeline via `publish_parent_composition` | Refused at Runtime tip | Migrate to a create op or commit of initial config, or delete. Callers: `astrid/packs/timeline/cli.py:186` (`timelines create`), `astrid/sdk/timeline_duplicate.py:156`. Decide with Runtime owner. |
| `astrid/core/dev/reference_realm.py:99` | Reference-realm journey fixture publish | Refused at tip | Migrate fixture |
| `astrid/core/timeline/shot_composition_migration.py:151, 1030` | Migration writer protocol requires `publish_parent_composition` | Refused at tip | Owned by the migration; decide retire vs migrate |
| `astrid/sdk/shot_grouping.py:18-25`, `astrid/sdk/remote.py:2318` | Return 410 `retired_route` naming `publish_parent_composition` as the replacement | Stale pointer | Repoint the replacement hint to the commit path |
| `runtime_protocol/service.py:2598-2600` (Runtime) | the route itself | Refuses (`_require_timeline_command`, `:1604-1611`) | Delete only after the four callers above migrate; Runtime owner's call (INBOX: Runtime does not re-retire until consumers convert) |

---

## 5. Recommended order of conversion and deletion

Step 0 (now; no code change in Agent): reconcile the held-vs-refused state with the Runtime owner (§0.1). Decide the
strict-xfail marking for the two Runtime-backed tests (§0.2). Add `held` ledger rows (§7).

Step 1 - single-command edits (fastest proof, M2 registry):
- `clip.set-element` → convert W7 (`update-element`). Delete the publish body of `timeline_elements.py` (keep a thin builder).
- Media swap command → convert W6 (`replace-parent-media`). Replace the body of `remote.py:1278-1503` with a builder.
- Gate: `tests/editing_conformance` plus the replacement tests in §3. Retry-safety and stale-head behaviour from the Runtime commit.

Step 2 - Producer proposal (the D13 shape):
- Voiceover sync (W8): `sync_draft_voiceover` emits a proposal (commands + admitted target + base revision + `proposal_digest`). The requester commits. Delete `TargetBoundAuthoringBundle.publish` and `_transport_idempotency_key` if nothing else calls them, and remove `draft_voiceover.py:475`'s publish call.
- Gate: D13 proposal tests; requester-commit identity; no producer-side credential.

Step 3 - script and docs:
- W9: `timeline_document.py publish` → proposal + commit; keep `check`. Update `document-checkout.md:32`, `SKILL.md:629-645, 747-750`, `timeline-editing-guide.md`, `timeline-authoring-capabilities.md`.

Step 4 - the writer itself:
- Rewrite `approve_authoring_candidate` to bind the proposal digest (W3). Delete `promote_approved_authoring_candidate` (W2) and `publish_authoring_candidate` (W1). Remove their exports (W11). Re-point the feedback tests (§3). The publication-assembly block in `compile_authoring_candidate` (`:1084-1116`) can go only once preview no longer needs `publication_digest`.

Step 5 - whole-document Checkout publish (largest; last):
- Only after every Checkout edit is command-backed or refused: `store.publish_bundle` (W4), `Checkout.publish` body and the narration second publish (W5), `three_way`/`_merge` (shared with `checkout.py:203`, so delete with that path), `fetch_bundle`/`_units` (shared with `cli.py:2808` and `publish.py:89`), `_cmd_publish` body (`cli.py:2934-2998`), and the re-export `timeline_checkout.py:151-154`.
- Gate: `TimelineSession` parity over the Checkout edit set.

Step 6 - Runtime (other owner): retire `publish_parent_composition` only after §4 callers migrate.

---

## 6. Line counts removable (estimates from current file spans; replacement code not netted except where stated)

| Bucket | Lines removed (est.) | Notes |
|---|---|---|
| `authoring_bundle.py`: W1 publish 36 + W2 promote 47 + `__all__`/import lines ~4 | 87 | W3 approve rewritten: 0 net now |
| Exports: `sdk/authoring_bundle.py` ~5, `sdk/__init__.py` 3, `core/timeline/__init__.py` 2 | 10 | W11 |
| `sdk/authoring_remote.py`: W8 publish 97 + key normalizer 18 | 115 | |
| `sdk/remote.py`: W6 `replace_parent_media` 226 → ~40-line builder | ~186 | net of builder |
| `sdk/timeline_elements.py`: 73 → ~25-line builder | ~48 | net of builder |
| `packs/rendering/docs/scripts/timeline_document.py`: `Writer` 12 + publish tail ~47 | ~60 | `check` stays |
| **Subtotal, not contingent on Checkout** | **~506** | |
| Contingent (Checkout whole-doc chain): W4 `publish_bundle` 75; W5 `publish()` 58 + `_publish_narration` 18; `three_way`/`_merge` 118; `fetch_bundle`/`_units` ~50; `_cmd_publish` 65 → ~30 (~35); re-export 3 | ~355 | Only after Step 5 |
| **Total** | **~860** | Before replacement code. After command builders, adapters and new proposal tests, a realistic net is ~600-650 product lines. Estimate, not measured. |

Test-side: about 45 functions rewritten or re-pointed; none should be deleted without a replacement or a ledger row.

---

## 7. Proposed deletion-ledger rows (text only; not written to the ledger)

Ids are placeholders; the orchestrator assigns. All start `held` until the replacement lands (INBOX 06:59Z).

| id | what (paths) | contradicts | replaced by | owner | ms | status | evidence |
|---|---|---|---|---|---|---|---|
| WC1 | Agent `astrid/core/timeline/authoring_bundle.py` `publish_authoring_candidate` (:1587) and its exports | second writer; whole-document fallback | producer proposal committed by requester via `commit_timeline` | agent | M2 | held | Runtime already refuses `publish_parent_composition` (`service.py:2598-2600`, `:1604-1611`). Stub tests pass; Runtime-backed tests fail at tip (unexecuted). |
| WC2 | Agent `authoring_bundle.py` `promote_approved_authoring_candidate` (:1538) | approval-gated second writer | approval bound to proposal digest | agent | M2 | held | zero production callers; test-only `test_authoring_bundle.py:458, 483` |
| WC3 | Agent `sdk/remote.py` `replace_parent_media` body (:1278-1503) | whole-closure publish for a single media swap | media-swap `EditCommand` (occurrence + clip addressed) | agent | M2 | held | `tests/test_timeline_clip_replacement.py:35` replacement pending |
| WC4 | Agent `sdk/timeline_elements.py` `update_parent_element` publish path | whole-closure publish for a single effect update | `clip.set-element` (INBOX 06:59Z) | agent | M2 | held | `tests/core/test_timeline_element_publication.py` replacement pending |
| WC5 | Agent `sdk/authoring_remote.py` `TargetBoundAuthoringBundle.publish` (:230) and `_transport_idempotency_key` | SDK whole-candidate publisher used by voiceover | producer proposal (D13) committed by requester | agent+app | M2 | held | `draft_voiceover.py:475`; `test_draft_voiceover.py` proposal replacement pending |
| WC6 | Agent `packs/rendering/docs/scripts/timeline_document.py` publish subcommand | whole-candidate publish from a detached JSON file | proposal + commit; `check` kept | agent | M2 | held | `test_authoring_feedback.py:210`, `test_authoring_media.py:227` replacement pending |
| WC7 | Agent `sdk/timeline/store.py` `publish_bundle` (:257) with `timeline/publish.py` `publish()` / `_publish_narration` and `timeline_checkout.py` re-export | whole-document checkout publish with three-way merge | `TimelineSession` command commit | agent | M2 | held | after all Checkout edits are command-backed or refused; `test_timeline_publish_connection.py` replacement pending |
| WC8 | Agent `sdk/timeline/store.py` `three_way`/`_merge` and `fetch_bundle`/`_units` (whole-document) | whole-document merge | server-side rebase of commands | agent | M2 | held | depends on WC7; shared with `checkout.py:203` and `cli.py:2808` |
| WC9 | Docs: `timeline-editing-guide.md`, `timeline-authoring-capabilities.md`, `SKILL.md` (rendering), `document-checkout.md` writer examples | docs teach the second writer | propose + commit examples | agent | M2 | held | doc only |
| WC10 | Runtime `runtime_protocol/service.py` `publish_parent_composition` (:2598) | legacy composition writer (already refused) | commitTimeline | runtime | M2 | held | delete only after §4 callers (`remote.create_empty`, `reference_realm.py`, `shot_composition_migration.py`) migrate; not re-retired until then (INBOX 06:59Z) |

---

## 8. Unverified / open questions for the orchestrator

- **Runtime state vs INBOX "held" (§0.1).** Verify by running `test_candidate_compiler_integrates_with_runtime_atomic_publication`
  with `PYTHONPATH` pointing at the Runtime tree. I was denied approval to run pytest in this sandbox, so this is code evidence only.
- **Shared-shot intent for media swap (W6).** The current code edits the shot's internal timeline, which may be shared by several
  occurrences. The command must declare "shared shot" vs "this occurrence only" (PLAN §4.1). Not decided here.
- **`timelines create` (`create_empty`) needs a Runtime create op or an initial commit.** Not decided here; needs the Runtime owner.
- **Out of scope but adjacent:** the in-memory recipe helpers in `astrid/sdk/timeline_editing.py` (883 lines: `add_authoring_shot`,
  `place_media`, `sequence`, `move_occurrence_group`, `add_track`, `grid`) mutate the candidate in place and feed W1. They are not named
  in the brief. Recommend a follow-up census; the PLAN already flags the deprecated retime helpers there (D07).
- **Docs and SKILL are not tested.** No test imports the doc snippets, so doc drift will not be caught; the rewrite needs a manual check.
