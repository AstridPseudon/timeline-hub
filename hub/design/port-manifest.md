# Timeline R4 M0 forward-port manifest

## Scope and reading rule

This is a forward-port recommendation, not a merge list. The experiment was
run on `tl/agt-m0-spike` at `8003c8dd`, from main `e51595c6`, using frozen
R4 SDK ref `origin/codex/handover-timeline-r4-20261019-candidate-sdk`.
The spike is disposable and not for merge.

Every source row has two independent classifications:

* **Experiment status** says what the disposable branch did: `COPIED` means
  the R4 file was overlaid without a source edit, `ADAPTED` means it was
  edited for the import closure or a main-wins rule, `IMPORT-ONLY STUB` means
  it exists only to make imports possible, and `MAIN` means the R4 file was
  not overlaid because current main owns the path.
* **Forward recommendation** says what M1/M2 should actually do. `FORWARD`
  never means copy the experiment unchanged. `DEFER`, `CUT`, and `MAIN`
  recommendations are intentional even when the experiment status is
  `COPIED`.

The canonical source disposition for every row is **port with changes** for `FORWARD`, timing slices, playback subsets and one-path/outbox adapters; **do not port** for `MAIN`, `CUT`, `DEFER` or replaced writers. No source is approved **port as-is** solely from this import experiment. A narrow unchanged helper can be accepted as-is later only with its actual main-facing behavioral tests. The milestone/subset labels below describe the required slice; they are not another source of port authority.

Import success is not semantic validation. The 58-module smoke walk passed
only because the closure includes an unsupported Pack V3 check stub, optional
generated Runtime validation with a local fallback, a local request-bound
transcript codec, and legacy intent-name shims. A real port replaces those
four conveniences with, respectively: the current Pack/check admission
boundary (or an explicit no-check path that cannot enter save), the generated
Runtime package and schema validators, main's transcript/source-window
implementation, and main's actual intent API. None of these shims can be
accepted as M1 behaviour merely because imports are clean.

## Settled main rules every forward port must absorb

1. **Main schema wins.** Preserve Astrid's current namespace, chapters-as-
   shots/occurrence model, current parent-track ownership, and opaque data.
   Both main and R4 use `app.astrid`; preserve main's current namespace migration and collision handling rather than replacing them with R4 carrier/version assumptions. Adapt parent/child addresses and schema adapters to the single canonical command contract.
2. **Main text/time wins.** Use current transcript and source-window
   contracts, rational frame rates, half-open intervals, explicit time maps,
   and the current Moment grammar. `null` is a value; an explicit clear is a
   distinct setter operation and removes presence.
3. **The runner is the write boundary.** Every authored write, including
   unchanged intentional writes, is an `EditCommand` with recorded reads,
   writes, bindings, expectations, and created IDs. Direct bundle mutation is
   not a supported compiler or test setup path.
4. **M1 is the complete walking skeleton.** It includes the move command,
   registry and runner, guarded inverse, server rebase, Agent provider,
   Runtime `/v1` commit operation, CLI and Python producers, `show`,
   renderer-free commit, and crash/restart-safe retry. The compiler rows below
   identify only the narrow timing dependency for that move; they do not
   delete or defer any M1 deliverable.
5. **M2 completes the edit surface.** Port the full registry and compiler,
   sheet/CLI/Python conformance, transcript/source bindings, media add/swap,
   occurrence isolation, explicit clears, and App command producers. Delete
   fallback writers and duplicate save/history routes after their consumers
   use the one commit path.
6. **One commit/history path.** Runtime owns accepted history and receipts.
   The client may retain only a small crash-safe outbox, exact in-flight
   request, retry identity, and local undo intent. `publish`, saved-publish,
   restore, and local history adapters must not become alternate persistence
   routes.
7. **Save is renderer-free.** The provider checks commands, structure,
   timing, references, media/revision dependencies, and authority. Scene
   evaluation belongs to preview/check/render and is never required by commit.
8. **Existing playback stays.** Existing films' music beds, audio envelopes,
   fades, transitions, and timing playback remain readable/materializable.
   New story, motion, ducking, music-bed authoring, copy-sync, and lint
   authoring remain deferred as the plan requires.

## File-by-file recommendation

### SDK timeline closure

| Source file | Experiment status | Forward recommendation | Main rules / required action |
|---|---|---|---|
| `astrid/sdk/timeline/__init__.py` | ADAPTED | M1 FORWARD | Remove import-only legacy intent shims; expose the command API against main's namespace and current public checkout. |
| `astrid/sdk/timeline/_common.py` | ADAPTED | M1 FORWARD | Keep main error/address/digest rules; make runner refusals and explicit clears canonical. |
| `astrid/sdk/timeline/_timing_evaluators.py` | ADAPTED | M1 slice, M2 full | Keep as the one evaluator set; port rational-fps, half-open, source-window, and current Moment rules, with no direct writes outside the runner. |
| `astrid/sdk/timeline/api.py` | COPIED | M1 FORWARD | Retain only the facade needed by the move; route every mutation to `EditCommand`, not an R4 save API. |
| `astrid/sdk/timeline/apply_file.py` | COPIED | M2 FORWARD | JSON, Python, and sheet inputs must build commands; remove monkeypatched save/undo/publish fallbacks and preserve exact outer transaction scope. |
| `astrid/sdk/timeline/audio_envelope.py` | COPIED | KEEP PLAYBACK | Keep existing audio-envelope reads/materialization; use main audio fields and the one timing compiler. No new authoring surface. |
| `astrid/sdk/timeline/bed_adoption.py` | COPIED | KEEP PLAYBACK; DEFER AUTHORING | Keep adoption/read paths needed by existing films; defer new bed-selection/authoring and replace its R4 carrier assumptions with main schema. |
| `astrid/sdk/timeline/chapter_storage.py` | COPIED | M2 FORWARD | Adapt storage to chapters-as-shots and current parent/occurrence ownership; never resurrect the R4 chapter carrier. |
| `astrid/sdk/timeline/check.py` | ADAPTED | M2 FORWARD, outside commit | Keep checks as non-blocking read/preview diagnostics; remove scene evaluation from save and use the published Composition evaluator only in See paths. |
| `astrid/sdk/timeline/checkout.py` | ADAPTED | M1 FORWARD | Preserve main checkout shape and runner guard; command execution must be the only authored write boundary. |
| `astrid/sdk/timeline/checks.py` | IMPORT-ONLY STUB | REPLACE in M2 | The stub returns no checks and raises `unsupported`; replace it with current Pack/check admission or keep checks completely outside commit. |
| `astrid/sdk/timeline/commands.py` | ADAPTED | M1 FORWARD; M2 COMPLETE | M1 must include registry, runner, move, recorded footprints, and CLI/Python builders; M2 fills the registry and conformance surface. |
| `astrid/sdk/timeline/commit.py` | ADAPTED | M1 FORWARD | Keep provider/rebase/idempotency/pinned reads, but delete `requires_scene_evaluation` and all scene-answer calls from acceptance; Runtime loads the provider at `/v1`. |
| `astrid/sdk/timeline/compiler.py` | COPIED | M1 timing slice; M2 FORWARD | Replace R4 assumptions with one rational-fps, half-open, explicit-map compiler; derived timing has one writer and all input changes are commands. |
| `astrid/sdk/timeline/components/__init__.py` | COPIED | M2 FORWARD | Retain registry wiring needed by existing elements; use main element schemas and defer new component authoring. |
| `astrid/sdk/timeline/composite_effects.py` | COPIED | M2 FORWARD | Preserve playback of existing effects; route any supported edit through commands and current element/Composition contracts. |
| `astrid/sdk/timeline/continuous.py` | COPIED | M1 timing slice; M2 FORWARD | Keep continuous timing dependency helpers, but bind them to the main compiler and runner rather than raw bundle mutation. |
| `astrid/sdk/timeline/copy_sync.py` | COPIED | DEFER | New copy-sync authoring is explicitly deferred. Keep only any read projection required by current text views; do not label the R4 authoring implementation port-as-is. |
| `astrid/sdk/timeline/doc.py` | ADAPTED | M1 FORWARD | Use current document/namespace/chapters-as-shots shape and preserve unknown data; no R4 schema carrier. |
| `astrid/sdk/timeline/drafts.py` | COPIED | CUT | Delete R4 draft lease/expiry and retention machinery. Draft/outbox lifetime is explicit and crash-safe; accepted history remains in Runtime. |
| `astrid/sdk/timeline/duplicate_fidelity.py` | COPIED | DEFER | Generation/timeline duplication is not an M1/M2 deliverable. If later revived, it must use pinned Runtime ancestry and the command/rebase recipe. |
| `astrid/sdk/timeline/edits.py` | ADAPTED | M1 FORWARD | Keep thin semantic builders for the move and existing edits; no second patch/save vocabulary. |
| `astrid/sdk/timeline/element_reference.py` | COPIED | M2 FORWARD | Use stable IDs/anchors and current source-window/occurrence addresses; preserve opaque reference-bearing fields during rebase. |
| `astrid/sdk/timeline/graph_commands.py` | COPIED | M2 FORWARD | Port occurrence/add/swap graph commands with exact pinned reads and created IDs; leave duplicate-generation branches deferred. |
| `astrid/sdk/timeline/history.py` | COPIED | M1/M2 OUTBOX ONLY | Keep crash-safe local undo/outbox transitions only; Runtime is the accepted history authority and local snapshots are not publication truth. |
| `astrid/sdk/timeline/identity.py` | COPIED | M1 FORWARD | Preserve stable created-ID reservations across retry, inverse, and rebase; use main namespace/address rules. |
| `astrid/sdk/timeline/inverse.py` | COPIED | M1 FORWARD | Keep generalized guarded inverse, publication ancestry, and A→B→A/intervening-write checks; retire duplicate core inverse machinery after registry inverse lands. |
| `astrid/sdk/timeline/journal.py` | ADAPTED | M1 FORWARD | Persist exact request bytes, retry key, base revision, and local outbox state; do not create a second accepted-history ledger. |
| `astrid/sdk/timeline/lookup.py` | ADAPTED | M1 FORWARD | Provide stable selection and anchor lookup for move/rebase/show using current shots, occurrences, words, and source windows. |
| `astrid/sdk/timeline/loops.py` | COPIED | M2 FORWARD | Keep only existing playback/timing loop semantics; rationalize frames and make cycle refusal atomic through the runner. |
| `astrid/sdk/timeline/manual_text.py` | COPIED | M2 LIMITED | Preserve existing text-card playback/edit compatibility where needed; defer new story/copy authoring and use current element schemas. |
| `astrid/sdk/timeline/model.py` | ADAPTED | M1 FORWARD | Main model, rename, chapters-as-shots, transcripts, source windows, explicit clears, and opaque preservation are authoritative. |
| `astrid/sdk/timeline/modifiers.py` | COPIED | M2 LIMITED | Keep modifiers used by existing playback; any new modifier authoring waits for the command conformance contract. |
| `astrid/sdk/timeline/music_beds.py` | COPIED | M2 LIMITED | Keep existing authored-bed materialization/readback and playback dependencies; adapt carrier/schema/occurrence layout to main and cut new bed authoring. |
| `astrid/sdk/timeline/music_lane.py` | COPIED | KEEP PLAYBACK | Preserve existing music lane projection, fades, and bed playback; no independent save/history route or new authoring API. |
| `astrid/sdk/timeline/narration.py` | COPIED | M2 FORWARD | Use main transcript/source-window contracts and exact take dependencies; no R4 local transcript authority. |
| `astrid/sdk/timeline/overhang.py` | COPIED | M2 FORWARD | Keep existing timing/playback overhang behaviour under the single compiler and current half-open intervals. |
| `astrid/sdk/timeline/publish.py` | ADAPTED | REPLACE by M1 `/v1` | Keep only request construction needed for the Runtime door; remove local publish acceptance and duplicate save/history semantics. |
| `astrid/sdk/timeline/rebase.py` | COPIED | M1 FORWARD | Server-side rebase is required in M1; replay recorded intent/bindings/IDs on current main and conflict only on changed dependencies. |
| `astrid/sdk/timeline/relations.py` | COPIED | M2 FORWARD | Keep occurrence/transition relation semantics with main address grammar; fix R4 `parent/clip:follower` assumptions and preserve explicit choices. |
| `astrid/sdk/timeline/restore_commit.py` | COPIED | M1/M2 ONE-PATH ADAPTER | Emit a guarded inverse/restore `EditCommand` to `/v1`; do not retain a local restore publication route. |
| `astrid/sdk/timeline/revisions.py` | ADAPTED | M1 FORWARD | Use Runtime accepted revision/publication identity and immutable pinned reads; never report merely a moving head. |
| `astrid/sdk/timeline/saved_intent.py` | COPIED | M1 OUTBOX ADAPTER | Retain exact unsent/in-flight command intent only; replace any local saved-publish authority with Runtime receipt state. |
| `astrid/sdk/timeline/saved_publish.py` | COPIED | CUT/REPLACE | This is a duplicate saved-publish route. Reduce it to outbox migration if needed, then delete it after `/v1` commit and Runtime history are live. |
| `astrid/sdk/timeline/selection.py` | ADAPTED | M1 FORWARD | Keep stable selection/query semantics for commands and Read views; honor current shots/occurrences and explicit scope. |
| `astrid/sdk/timeline/sequence_fit.py` | COPIED | M2 FORWARD | Port fit/curve semantics through the one compiler, rational fps, and command runner; fix raw-mutation setup failures shown by the spike. |
| `astrid/sdk/timeline/shader_slots.py` | COPIED | M2 LIMITED | Keep existing playback slot resolution only; defer new shader/effect authoring and use current element registry. |
| `astrid/sdk/timeline/shot_groups.py` | COPIED | M2 FORWARD | Port occurrence/shot grouping and inverse footprints using chapters-as-shots and current placement ownership; generation duplication remains deferred. |
| `astrid/sdk/timeline/source_hydration.py` | COPIED | M1/M2 FORWARD | Keep exact immutable media/revision/transcript dependency reads; replace local closure fallbacks with Runtime-authorized reads. |
| `astrid/sdk/timeline/story.py` | COPIED | DEFER | Story authoring is explicitly deferred. Current chapter/shot text views win; retain only a pinned read projection if a current Read command needs it. |
| `astrid/sdk/timeline/sync.py` | COPIED | M1/M2 ONE-PATH ADAPTER | Keep outbox refresh and server rebase; remove local publish/history duplication and label every view with the immutable accepted revision. |
| `astrid/sdk/timeline/tools/__init__.py` | COPIED | M2 LIMITED | Keep only shared command/test helpers required by main; no R4 host/custody or receipt machinery. |
| `astrid/sdk/timeline/transaction.py` | ADAPTED | M1 FORWARD | Preserve atomic rollback/history boundaries and explicit unchanged-write footprints; renderer/check adapters cannot be required for commit. |
| `astrid/sdk/timeline/transcript_binding.py` | COPIED | M2 FORWARD | Port stable word/source bindings and exact correspondence against main transcripts/source windows; no guessed rebinding. |
| `astrid/sdk/timeline/transcript_commands.py` | COPIED | M2 FORWARD | Make transcript bind/reference edits normal commands with explicit clears and pinned source dependencies. |
| `astrid/sdk/timeline/transcripts.py` | ADAPTED | M2 FORWARD | Replace local request-bound codec with main transcript/source-window implementation; preserve current schema and opaque data. |
| `astrid/sdk/timeline/transitions.py` | COPIED | KEEP PLAYBACK; M2 EDIT | Existing fades/transitions must keep playing; supported authoring becomes commands and does not add a renderer-dependent save path. |
| `astrid/sdk/timeline/units.py` | ADAPTED | M1 FORWARD | Use main rational frame/time units and reject ambiguous conversions; no float-only R4 timing contract. |
| `astrid/sdk/timeline/look.py` | MAIN / unchanged | KEEP MAIN | Retain main declarative look-field codec and read projection; new setters use the command registry and preserve unknown fields. |
| `astrid/sdk/timeline/reflow.py` | ADAPTED | M1 timing slice; M2 FORWARD | Retain the thin compiler entrypoint facade; absorb main timing fixes in `_timing_evaluators.py` and remove direct authored mutation outside the recorder. Do not keep a second timing engine. |
| `astrid/sdk/timeline/store.py` | ADAPTED | M1/M2 REPLACE WRITERS | Reuse exact immutable read and outbox file/lock utilities where needed; delete local three-way accepted-save and `publish_bundle` authority once clients commit commands. No client semantic rebase or competing accepted-history snapshots. |

### Core timeline closure

| Source file | Experiment status | Forward recommendation | Main rules / required action |
|---|---|---|---|
| `astrid/core/timeline/audio_envelope.py` | COPIED | KEEP PLAYBACK | Keep existing audio envelope/fade playback and adapt field names only through main's schema. |
| `astrid/core/timeline/chapter_storage.py` | COPIED | M2 FORWARD | Use main chapter/shot storage and migration; do not restore the R4 carrier. |
| `astrid/core/timeline/compatibility.py` | COPIED | M1 ADAPTER | Replace R4 compatibility assumptions with current namespace, parent/occurrence, transcript/source-window, and explicit-clear validators. |
| `astrid/core/timeline/copy_sync.py` | COPIED | DEFER | No new copy-sync authoring in M1/M2; preserve only current read data if required. |
| `astrid/core/timeline/cut_index.py` | COPIED | M1 FORWARD | Keep stable cut/shot lookup for move, compiler, and show, using chapters-as-shots. |
| `astrid/core/timeline/moments.py` | ADAPTED | M1 FORWARD | Main Moment grammar and anchors win; keep only helpers that do not change source-window or address semantics. |
| `astrid/core/timeline/motion_curves.py` | COPIED | M2 FORWARD | Keep curve math and explicit inverse semantics; restore/update the generator before claiming freshness. |
| `astrid/core/timeline/motion_curves.json` | COPIED | M2 GENERATED INPUT | Treat as generated source data; validate against the real main generator and do not hide a missing generator behind import smoke. |
| `astrid/core/timeline/motion_curves.generated.ts` | COPIED | M2 GENERATED OUTPUT | Regenerate from the main-owned generator and verify Python/TypeScript parity. |
| `astrid/core/timeline/music_bed.py` | COPIED | KEEP PLAYBACK; M2 LIMITED | Preserve current films' music-bed materialization and fades; adapt R4 carrier fields/occurrence layout and defer new bed authoring. |
| `astrid/core/timeline/shot_composition_projection.py` | ADAPTED | M2 FORWARD | Keep main projection and strict parent-track helpers; Composition remains the one See evaluator and no evaluator enters save. |

The following R4 infrastructure is intentionally not a forward-port: host
custody/attestation and launch expansion, relay/gateway, retention/purge,
scene-in-save, evidence/handback decoration, `astrid/core/timeline/inverses.py`
after registry inverses land, vendored evaluators, and unrelated pack/demo
code. Current-main files such as `astrid/core/timeline/astrid_ns.py`,
`authoring_bundle.py`, `model.py`, `validators/**`, and
`shot_composition_migration.py` remain the authority and must not be replaced
by R4 copies. R4-only `scene_answers.py` is not present on main and is not a save dependency to port.

### M1 integration surfaces (not erased by the narrow compiler slice)

| Source file / surface | Experiment status | Forward recommendation | Main rules / required action |
|---|---|---|---|
| M1 command registry/runner deliverable (see `astrid/sdk/timeline/commands.py`) | ADAPTED | M1 REQUIRED | Move command, registry, runner, recorded footprints, inverse hooks, and deterministic replay are all M1 deliverables. |
| M1 Agent provider deliverable (see `astrid/sdk/timeline/commit.py`) | ADAPTED | M1 REQUIRED | Provider loads in Runtime and accepts renderer-free semantic commits through the normal `/v1` door. |
| `astrid/packs/timeline/cli.py` | MAIN | M1 REQUIRED | CLI edit must emit the same EditCommand as Python/App; preserve main parser/help and explicit clear flags. |
| `astrid/packs/timeline/cli_parser.py` | MAIN | M1 REQUIRED | Add the main parser's command JSON/dry-run/clear forms without replacing its existing command census. |
| `astrid/sdk/timeline_checkout.py` Python facade | MAIN | M1 REQUIRED | Python move producer uses the same registry/provider and cannot bypass the runner with direct bundle writes. |
| `astrid/packs/timeline/cli_show.py` | MAIN | M1 REQUIRED | `show` must read the accepted immutable revision and current chapters-as-shots/transcript/source-window model. |
| Runtime `/v1` commit door and generated client | MAIN | M1 REQUIRED | Runtime owns authorization, pinned dependency reads, idempotent retry, accepted revision identity, and history; no `/astrid/v1` side route. |

## Evidence and limitations

Commands were run with `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python`
and `PYTHONDONTWRITEBYTECODE=1` where shown. The focused lane intentionally
included the freshness test; its failures remain evidence.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python - <<'PY'
import importlib, pkgutil
package = importlib.import_module('astrid.sdk.timeline')
names = [item.name for item in pkgutil.walk_packages(package.__path__, package.__name__ + '.') if not item.ispkg]
failures = []
for name in names:
    try: importlib.import_module(name)
    except Exception as exc: failures.append((name, type(exc).__name__, str(exc)))
print(f'import candidates: {len(names)}')
print(f'failed: {len(failures)}')
for item in failures: print(item)
raise SystemExit(bool(failures))
PY
# import candidates: 58; failed: 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py \
  tests/sdk/test_sequence_fit_curves.py tests/core/timeline/test_motion_curves.py
# 104 passed, 5 failed, 2 warnings in 9.18s (audit rerun; the required
# timing5 log reports 104 passed, 5 failed, 2 warnings in 9.61s).

baseline_dir=$(mktemp -d /tmp/agt-m0-baseline-audit.XXXXXX)
git archive tl/integration | tar -x -C "$baseline_dir"
cd "$baseline_dir"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$baseline_dir" /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_selection.py \
  tests/sdk/test_timeline_transaction.py tests/sdk/test_timeline_sheet.py \
  tests/core/timeline/test_music_edit.py tests/core/timeline/test_expand_shots.py
# 196 passed, 17 deselected, 4 warnings in 5.64s
```

The six supplied spike runs are indexed node-for-node in
`port-failure-index.tsv`: timing5 `104 passed/5 failed`, commands
`68/48`, rebase `7/35`, music `36/23`, inverse `2/9`, and data `3/15`.
The audit focused rerun is also indexed separately as
`agt-m0-spike-port-audit-focused.log` (`104/5`). No failure was excluded to
produce a passing headline.

The recipe-versus-overlay comparison is additionally indexed as `recipe-overlay`: 9 failed at the same absent R4 CheckAdmissionContext import. This verifies the command acceptance boundary remains unresolved even though the package import walk passes. The combined index contains 149 per-run failed/error nodes; repeated tests in distinct runs are deliberately separate evidence.


## Current implementation queue after M1 (2026-10-19; design only)

**Authority/source:** inspected Agent `7a7acc0eea47b372e15bb7921563b281ada00fb4`
(the assigned integration base; original main `e51595c68fc23d3d1734a0885c84a6511999697b`)
and frozen SDK `11caf1d9de291d76f491cf69f7942606b7471d7a`
(`origin/codex/handover-timeline-r4-20261019-candidate-sdk`, read with `git show`).
This section supersedes the historical rows' *implementation ordering/scope*,
not their M0 observations or `port-failure-index.tsv`. M1's native
`commands.py`, `capture.py`, `_recording.py`, `_command_state.py`, `inverse.py`,
`rebase.py`, `commit.py`, `sync.py` and `outbox.py` are the starting point.
Do not overlay the disposable spike or R4's 2,860-line registry.

**Release prerequisite:** PLAN has not recorded M1 closed. Latest Agent INBOX
holds closure for restored App track-name conflict/open-draft restart journeys,
classification of every new suite failure, and the orchestrator's deep audit.
The later `restore-regressions-m1` decision authorizes existing restore as an
**M1 preservation fix**, through the frozen sole-command `timeline.restore` v1,
exact head pair, recorder, semantic restore and inverse; it is not M2 backlog.
At this inspected SHA, `commit.py:373–381` still refuses that adapter. Consume
its reviewed implementation before widening; do not build another restore path.
No M2 product implementation is authorized by this queue.

**First M2 dependency (DECIDED A; merging waits for recorded M1):** follow
`m2-move-draft.md`: approved order/staged-inverse groundwork, then explicit
recorded lossless legacy-group→canonical-shot migration + whole-occurrence move
to an existing lane + explicitly owner-bound derived App group view. Retrack
updates occurrence-owned child tracks atomically; `pinnedShotGroups` is consumed
migration input, never an editable store. Next compose track.create+move, then
separately add free multi-clip move-set. Preserve all three original App success
assertions; local patch/group-array shapes are compatibility output only. Refresh
new command/ref schemas and reservation semantics through the existing artifact
handoff, without new Runtime DTO/ABI. This supersedes pending group-choice language
below, not historical M0 observations. The 22:35 INBOX allows branch implementation;
this task stays design only. Later rows are bounded source/test slices, not one
registry-wide PR; M1 restore preservation and closure remain merge prerequisites.

### What “full registry” must cover

“Full” means every retained current editing producer and supported App gesture
uses the native recipe, not every operation found on the frozen branch. Existing
`operations()` contains `clip.move` and `track.create`; `timeline.inverse` is a
special runner dispatch. `validate_command` hard-codes those three today.
Extend that one admission/dispatch source with annotated parameters/version,
clear/default/unit rules, handler and fixtures; generate aliases/help from it.
R4 operation names below are donor vocabulary, not approval to replace M1 names
(`track.create` stays canonical) or add snapshot/storage commands to the registry.

| Actual retained surface / builder seam | Native command coverage to supply; boundary |
|---|---|
| `packs/timeline/cli.py:_configure_edit/_apply_edit`; `sdk/timeline/model.py:Clip`, `look.py`, `core/timeline/clip_fields.py` | `--set`, `set_param`, `set_look`, `tag`, `keyframe_at`, `set_track`, explicit clear; look flags `--opacity`, `--volume/--gain-db`, `--entrance/--exit`, `--fade-in/--fade-out`. Reuse codecs/validation in thin builders of `clip.set`, `clip.set-param`, `clip.set-look`/`look.opacity`, `clip.clear`; track set/remove/reorder and create must record membership/order and dependents. Existing animation values remain editable; no new motion authoring subsystem. |
| Same CLI/model plus `sdk/timeline/reflow.py`, `edits.py`, `StepSequence`, `Voice` | `--on`, `--at/--at-word` (+`--n/--near/--offset`), `--until`, `--for/--duration`, `--extend`, `--nudge/--nudge-frames`, `--trim-in/--trim-out`, `--slip`, `--keep`, `--retime`, `--fit-sequence/--shape-from`, `--close-gap-before`, `--insert`, film-end flags from `cli_film.py`; `--split/--add-cut`, cut note `--why/--hold`, remove. Reuse builders as recorded timing declarations/intents (`clip.on/until/set-duration/nudge/trim/slip`, `sequence.fit`, timeline reflow/resolve/retime/insert-time/close-gap/film-end and cut operations); never dispatch raw mutable methods behind the recorder. |
| `Voice.replace/set_gap_after`, `reflow.py:insert_line/remove_line/apply_script`, `timeline_transcripts.py`, `media_transcript.py` | Preserve `--replace-line/--line`, `--insert-line`, `--remove-line`, `--gap-after`, `--from-script` with take/words/text/gap options; existing `--beats`, slots/fill and source bindings. Transcript bind/reference use exact retained sources. These existing narration/script features are not deferred R4 story/copy-sync expansion. Transcript artifact creation may remain a Documents write; selecting it into a film is a command. |
| `edits.py:add/replace_asset`, CLI `_add_media/_add_layer/_crossfade`; `remote.py:replace_parent_media`, `timeline_elements.py:update_parent_element`; `timeline_editing.py` public builders | Preserve `--add-media`, `--add-layer`, `--swap-asset`, `--replace-asset`, `--clear-asset`, `--crossfade/--over`, clip/layer remove, explicit media trim and IDs; add/swap require the immutable selected media tuple. Cover existing `shot.set`, occurrence add/set/remove, source/element reference and reorder edits using main `source_mapping`/chapters-as-shots; R4 graph/track handlers are parts, not their carrier or duplicate-generation branches. |
| `timeline_sheet.py:parse_sheet/_apply_parsed/_update_layer/_apply_sound`; CLI `apply`; `Checkout` and `timeline_checkout.py` facade | Parser produces the same commands for layer add/omit/update, sound, line gaps/text/removals, cut notes, film end, params/look and clears; fragments touch only selected cuts. Python aliases and JSON share the registry. A batch is the atomic unit/one undo step; do not add a second `timeline.batch` executor or R4 save/undo storage entries. |

Keep existing music clips, literal sound-row gain/length edits, fades,
transitions, formula/sequence values, music ending/ripple policy and playback.
Defer **new** R4 story, motion, ducking, managed music-bed authoring, copy-sync,
lint expansion and generation duplication. Thus historical `music_beds`,
`bed_adoption`, `modifiers`, `manual_text`, `shader_slots`, `continuous`,
`loops`, motion-curve rows mean only the playback/dependency subset actually
needed by retained films/builders, not wholesale authoring ports. Preserve
unknown payloads. Existing `duplicate`, adopt, restructure, create/rename and
archive/recover are real callable main surfaces, not evidence for new R4 extras:
retain their behavior; lifecycle/bootstrap versus timeline-edit routing needs
Agent/Runtime ownership reconciliation before their old writer can disappear.
No permission here to restore retired `save`/`replace_clip` routes in `remote.py`.

### Timing contract and atomic boundary

Public deterministic entrypoint: **`astrid.sdk.timeline.compiler.compile_timing`
with `TimingInputs` → `TimingResult`**, adapted from frozen `compiler.py:323–461`.
`reflow.py` becomes a facade; `_timing_evaluators.py` contains the one timing
implementation. Operation handlers record authored inputs; compilation produces
only derived timing/materialization and its dependencies/consequence records.
Do not port R4's partial-checkout adoption on evaluator failure. Do not have
`compile_timing` execute hidden authored edits or reconstruct intent from cached
`at`/`hold`. Frozen `commands` timing-call arguments, if retained internally,
are evaluation requests for recorded intent, not a second command runner.

* Normalize FPS once to positive integer numerator/denominator; use exact
  rational arithmetic through source mapping and frame boundaries (including
  `30000/1001`). Seconds/ms are explicit codecs. Keep main's versioned policies:
  fixed move uses `Math.round` ties toward +infinity; Moment onset uses floor
  (`core/timeline/moments.py`, including its legacy boundary tolerance).
  `duration.py:clip_end_frame` rounds start and duration separately, with the
  existing minimum-one-frame playback rule; `quantize_interval` quantizes both
  endpoints and refuses collapse. They are distinct contracts, not interchangeable
  helpers. Preserve each in parity fixtures; don't silently replace one by the
  other or repeatedly float-round intermediate values.
* All domains use `[start,end)`; adjacency is not overlap. Main numeric `hold`
  wins over trim, and timeline duration is `hold/speed` or `(to-from)/speed`,
  speed finite and positive. Keep source windows/unknown window metadata pinned,
  windowless footage windowless, trim bounds valid, slip film span unchanged.
  An affine source time `s` maps to clip time `C + (s-F)/v`, inverse
  `F + (t-C)*v`; compose an occurrence's **explicit admitted** map once.
  Clip-local projected words must not be source-trimmed/rate-scaled a second time.
  Never infer a missing map from duration, endpoint, index or text. New unsupported,
  ambiguous, contradictory or cyclic maps fail atomically, while inherited opaque
  maps round-trip. At this SHA move refuses explicit child maps and nontrivial
  occurrence maps; main graph validation also refuses new occurrence speed/offset
  semantics. General map support is required to be explicit and tested, not
  claimed already implemented or a license to bypass that validation.
* Bind a word by immutable `DocumentPin` plus source/lineage/word identity and
  occurrence/map identity. Main `media_transcript.py` supplies stable word IDs;
  `lookup.py:_word_list`'s synthesized segment/index labels and Moment text are
  discovery adapters, not authority across republication. Retain exact prior
  header/content when latest transcript/config changes; missing/changed/foreign
  source or removed anchor refuses, never a text-match fallback. Carry those pins
  in canonical dependency manifests and recorded compile dependencies. Do not
  port the spike's request-local transcript codec. M1 only retains these inputs
  and clears fixed-move anchors; `document_from_bundle` is currently a graph
  serializer, not a word-anchor compiler, and `word:word-1` is not a proven main
  Moment spelling. Test real supported source-word bindings through this public
  compiler/accepted command path, not a detached corrupted-cache helper probe.
* `commands.execute` stages the whole authored batch on an owned copy; resolve
  shared versus occurrence-local ownership with main's deterministic isolation
  and exact source mapping, compile timing, then graph/materialize through
  `core/timeline/authoring_bundle.py:compile_authoring_candidate`, validate the
  complete closure, and prepare the one Runtime acceptance. First materialization,
  parent/config mirrors, child/shot/parent revisions, retained sources and records
  share that failure/rollback boundary; no sibling rewrite or premature publish.
  `commit.py:document_from_bundle` and provider dry-run/replay/inverse/restore must
  consume the same compiled result. If a later command needs a resolved semantic
  prefix, materialize it inside this detached transaction; final refusal discards
  every prefix. Fresh and rebased candidates both compile; CAS retry retains
  original claims/created IDs. Undo restores authored values then compiles.
  See adapters may request the same pure compilation on a copy; no scene evaluator,
  renderer, pack checks, files/network or mutable “latest” inputs enter it.

### Ordered slices after the first drag contract

All paths below are Agent-relative (`sdk/` = `astrid/sdk/`, `core/` =
`astrid/core/`, `packs/` = `astrid/packs/`). Line effects are planning estimates
of authored nonblank/noncomment product lines, excluding tests/generated files;
reuse/delete existing evaluators rather than counting an R4 overlay as progress.

| # / dependency | Bounded implementation and test boundary | Removal trigger / approximate line effect |
|---|---|---|
| 1 / drag contract, M1 restore | Extend `sdk/timeline/{_command_state,_recording,inverse}.py` with collection position restoration and staged guarded reversal for composed commands. Preserve `[A,B]`, absent/null/container shape, created-ID reservations and later-dependent refusal. Start with create→set→inverse and remove→restore-first-row cases in `tests/editing_conformance/test_recipe_m1_commands.py`; keep the existing structural-group tests. | Generic structural primitives replace per-op inverse guesses before more structural commands; +150–300. Group representation remains outside this slice. |
| 2 / 1 | Fill native `commands.py` admission/metadata and scalar/clear/look + track edit handlers, keeping M1 capture. Adapt `model.py`, `look.py`, `clip_fields.py` builders; add/remove/reorder tracks use slice 1, never raw arrays. Exercise `tests/sdk/test_timeline_param_values.py`, `tests/packs/timeline/test_cli_look.py`, `tests/core/timeline/test_clip_fields.py` and recipe inverse/ABA nodes. | Remove each migrated method's `_journaled`/direct setter path after CLI/Python equivalent behavior and guarded inverse pass; +300–600. No R4 inventory.json/help monkeypatch. |
| 3 / 2 | Extract `sdk/timeline/reflow.py` timing into `compiler.py` + `_timing_evaluators.py`; adapt `core/timeline/moments.py`, `sdk/timeline/units.py` and relocate useful exact-time utilities from `timeline_editing.py`. Wire provider/graph boundary above and retain source pins. Bring only playback projection dependencies required by fixtures. | Retire the 1,136 nonblank/noncomment-line in-place reflow engine after facade/compile consumer parity, cycle/immutability and renderer-free provider tests; roughly +400–700 net, not +1.7k beside the old engine. |
| 4 / 3 | Register timing/anchor, trim/slip/sequence/film-end/ripple and existing narration builders in `model.py`, `edits.py`, `reflow.py`; bind main transcripts in `media_transcript.py`/`timeline_transcripts.py`. Move any inverse/music projection into compiler; explicit invertible format migration precedes legacy→managed materialization. Use media-verbs, reflow/film-end golden, transcript-ID nodes below plus converted R4 timing/inverse cases. | No remaining timing setter/reflow bypass for these callers before removal; keep main music endings and word-gap/orphan semantics. +350–650 after reuse. |
| 5 / 1,3,4 | Add media/layer add/swap/remove and existing element-reference/crossfade builders in `edits.py`, `timeline_elements.py`, `remote.py`; use immutable media-selection reads, injected/recorded IDs and full source bounds. Tests: `tests/sdk/test_timeline_media_verbs.py`, `tests/packs/timeline/test_cli_media.py`, `test_cli_add_layer.py`, `tests/test_timeline_clip_replacement.py`, `tests/core/test_timeline_element_publication.py`. | Replace same-placement CAS publishers with commands before deleting their `_Writer` adapters; preserve admission/authority and original positive behaviors. +250–500 net. |
| 6 / 1,3,5 | Adapt retained occurrence/shot/cut structural operations via `timeline_editing.py`, `timeline_structure.py`, `timeline_restructure.py` and `edits.py`; donor `graph_commands.py` is a reference only. Keep chapters-as-shots, parent track ownership, exact shared-child isolation and source windows. Tests: provider document/shared-materialization nodes, `tests/sdk/test_timeline_structure.py`, `test_timeline_restructure.py`, `tests/timeline/test_authoring_bundle.py`. | Remove direct structural publication only once actual consumers emit these commands; no new fork/remap/generation service. +200–450; group-specific changes wait for separate decision. |
| 7 / 2–6 | Generalize `sync.py` queue/capture/flush for registry commands; route `packs/timeline/cli.py` old edit/apply and Python `checkout.py`/`timeline_checkout.py` through it. `timeline_sheet.py` diffs the exact exported base into commands, with original guards; server alone rebases. Preserve fragment/omission/error semantics, one outer transaction, aliases and help. Extend existing `tests/editing_conformance/runner.py`/scenarios rather than add a harness; include exact command-capture parity and canonical JSON input. | Delete client semantic three-way sheet/publish merging once stale-base disjoint and true-conflict behavior passes; no refreshing guards to current head. Reuse M1 exact flight/pending suffix; about −300 to +100. |
| 8 / 1–7 + Runtime/App writer retirement | Fold `publish.py`, `checkout.py` local save/history and `journal.py` into command/outbox + Runtime history adapters; finish deletion inventory below. `revisions.py`/CLI history/log remain views of exact accepted edges. Re-run main conformance, transaction, sheet, journal behavior mappings, sync/history tests plus central integration journeys under their owners. | Delete old accepted writers/inverses/extensions/helpers only after consumer/behavior replacement and direct legacy-endpoint rejection. Roughly −2.3–3.2k, including core inverse/extensions, without counting viewer/vendor deletions owned by Viewing. |

These estimates are budgets, not a measured final diff: roughly −2k to +1k
net after all retirements, with uncertainty in compiler/source adaptation. Keep
PLAN's **20–26k authored product lines for the entire consolidated core** in
view; do not treat this Agent increment as another 20–26k allocation. Measured
static anchors here: core inverses 605 nonblank/noncomment lines (783 physical),
core extensions Python 1,420 (1,637 physical), journal 277 (335 physical), old
reflow 1,136 (1,221 physical); frozen compiler/evaluators/facade are 433/1,272/29
by the same crude count (docstrings included). No complete four-repo census is
claimed; managers must reconcile aggregate size before accepting a larger port.

### Current M2 retirement audit (Agent integration, 2026-10-19)

| Target | Actual callers / registry evidence | Native replacement | Deletion readiness | Next small deletion |
|---|---|---|---|---|
| `astrid/core/timeline/inverses.py:1-783` | No production Python import/call; only `tests/timeline/test_inverses.py:45-48` imports `InverseRequest`, `plan_inverse`, `plan_inverses`. | `astrid/sdk/timeline/inverse.py:24-148` plus `timeline.inverse` in `commands.py:62,132`; accepted history/records come from Runtime. | Production-dead now. Delete with its legacy test after native inverse/ABA/structural coverage is retained; do not delete `sdk/timeline/inverse.py`. | PR 1: remove file + old test; negative import grep and targeted `test_recipe_m1_commands.py`, `test_timeline_commit_provider.py`, `test_timeline_sync.py`. |
| `astrid/core/extensions/:1-636` (7 files) | No production import outside the package. Dedicated legacy tests only: `tests/core/extensions/{test_model,test_registry,test_scopes,test_sidecar}.py`; current discovery/registries are `astrid/core/pack/{loader,registry,permissions}.py` and Pack-declared metadata tests. | Normal Pack discovery/registry (`astrid.core.pack.discover_packs`, element/timeline extension descriptors); no second core-extension registry. | Production-dead now. Remove package and its self-tests together; replacement Pack tests must remain. | PR 2: remove `core/extensions` + `tests/core/extensions`; negative import grep and targeted `test_sdk_public_surface.py`, `test_pack_rendering_extensions.py`, editor extension catalog tests. |
| Deprecated retime helpers `astrid/sdk/timeline_editing.py:351-433` (plus timing utilities `436-540`) | No internal production import of `retime`/`retime_with_ripple`; both remain public lazy exports at `astrid/sdk/__init__.py:53,64`, and helper behavior is covered by `tests/test_timeline_editing_helpers.py:7-171`. Whole module remains production-live: `add_authoring_shot` is imported by `timeline_structure.py:8`, `timeline_adopt.py:10`, `timeline_duplicate.py:21`, `timeline_restructure.py:401`; CLI imports only `TimelineEditError` at `cli.py:3176,3315,3504`. | Move exact time/source/quantization utilities to the compiler/`timeline/units.py` seam; migrate supported timing edits to registry handlers and `compile_timing`. Migrate `add_authoring_shot` consumers to retained structural command adapters; no canonical new op is authorized here. | Helper block is deletion-ready only after public Python export compatibility is intentionally cut and utility tests move. Whole module is blocked by four structural callers and public exports. | Follow-up slice: relocate utilities, migrate the four `add_authoring_shot` callers, then remove helper block and lazy exports; retain `timeline_editing.py` until no supported structural caller remains. |
| Local durable journal/history `astrid/sdk/timeline/journal.py:1-335` | Active legacy writers: `checkout.py:188,242,264,285,307,339`, `publish.py:79`, `transaction.py:83`; `cli_log.py:11,39-82` reads/verifies it; `timeline/api.py:6,12` publicly exports `JournalRecord`. Legacy local save/undo/redo remains in `checkout.py:116-265` and `store.py:117,257`. Runtime history is separately read by `revisions.py`/`cli_history.py`; native pending path is `sync.py:19,114-280` + `outbox.py`. | Ordinary CLI/Python/sheet producers -> `EditCommand` capture/`TimelineSession.flush` -> Runtime `/v1`; accepted log/history -> `revisions.py`/`cli_history.py`. Keep `outbox.py` for pending, exact flight, retry identity and newer suffix only. | Not ready. Remove accepted-history writes and local accepted-save/undo authority only after ordinary writer migration and direct legacy-endpoint rejection. Journal compatibility reads may remain transiently for diagnostics, never publication truth. | After M2 writer migration: delete journal append hooks/`cli_log` accepted-history surface and local `_journaled`/snapshot publication path in a separately tested cleanup; do not delete `outbox.py` or Runtime history adapters. |

### Known alternate writers and deletion conditions

| Current writer / callable consumer | Required one-path replacement before deletion |
|---|---|
| `publish.py:_PublishMixin.publish/_publish_narration` → `store.py:publish_bundle`; CLI `_cmd_publish`, restructure, `timeline_duplicate.py`, public Checkout | Emit retained authored commands via `sync.py`/Runtime commit; narration selection is part of the same candidate, never a second `-narration` publication. Keep immutable transcript artifact storage separate. Remove `publish_bundle`'s client `three_way`/`force`, launcher fallback and duplicate accepted save only after every listed caller is mapped; existing duplicate/bootstrap boundary still pending with Runtime. |
| `sdk/authoring_remote.py:RuntimeAuthoringTarget.publish`; `core/timeline/authoring_bundle.py:publish_authoring_candidate`, exported via `sdk/authoring_bundle.py`/`sdk/__init__.py`; `WorkspaceClient.publish_parent_composition`/`remote.py` transport | Command-producing compatibility adapters for supported authored actions; read/validate/diff/preview compilation stays pure. Do not accept a whole candidate as an ordinary edit or hide it inside a generic patch command. Runtime owns removing/rejecting the legacy publication endpoint and any lifecycle bootstrap exception. |
| `remote.py:replace_parent_media` → CAS `_Writer`; `timeline_elements.py:update_parent_element` → its CAS `_Writer`; CLI replace-parent-media/update-element | Slice 5 commands plus exact pinned media/admitted-element reads, strict guards as appropriate and one receipt. Preserve closure, custom params, media authority and stale refusal tests; retired `save`/`replace_clip` stay typed refusals. |
| `checkout.py:save/_save_locked/_merge_writer/undo/redo/step`, `transaction.py:edit_transaction`, `store.py:_journaled` and snapshot/undo/redo directories; CLI `_cmd_edit/_cmd_apply/_cmd_undo/_cmd_redo`; `timeline_sheet.py:find_version/merge_sheet` | Local files hold pending command intent/exact flight only; accepted undo/redo uses publication-targeted guarded inverse, redo inverses the accepted inverse. Preserve one undo step, dry-run, rollback and stale-sheet disjoint/overlap behavior with Runtime bases. No snapshot rewind or client semantic rebase. |
| `journal.py:append/record_working_copy`, `Checkout.log`, `api.py:JournalRecord`, CLI `cli_log.py:run_log`, transaction/publish/save hooks | Accepted `log`/history/filter/attribution become Runtime history projections; pending/error/dry-run diagnostics can be explicitly local outbox information, never publication truth. Keep legacy journal read/verify compatibility until existing log and damaged-journal tests have equivalent coverage; stop appending a second hash-chain history, then remove unused exports/hooks. Do not port R4 `history/saved_publish/saved_intent/restore_commit` as authorities. |
| In-place timing in `reflow.py`, `model.py`/`edits.py` helpers; `_recording.py:compile_mirrors`; `commit.py:document_from_bundle`; graph compiler/read-preview callers `authoring_remote.py`, `authoring_render_preview.py`, core candidate validate/diff/inspect/preview/approve/promote | Move derived timing/mirrors/music projection into the compiler result; retain graph closure serialization as a subordinate pure materializer. Handlers may write authored timing intentionally, but never independently refresh derived timing. All public timing and preview entrypoints consume that result. Static write search plus behavioral stale-cache/atomic-failure tests must prove exclusivity before deleting old engines. |
| `core/timeline/inverses.py`; `core/extensions/` | At this SHA text search finds no product Python imports/calls: only old inverse tests and extension self/tests (not an active commit path). After mapping each distinct inverse behavior to native `inverse.py`/recipe tests, delete the duplicate inverse; preserve generalized SDK inverse/ancestry/dependency checks. Remove the unused extension registry after Pack/core consumer scan; M5 will use normal packs, not revive it. Do not label these dormant modules current writers. |
| Deprecated `timeline_editing.py:retime/retime_with_ripple/sequence/align` and mutation helpers; `sdk/__init__.py` public lazy exports | These are still callable public APIs even where only tests call them internally. Move exact `frame_time`, source↔timeline and quantization utilities to the timing unit seam first; make retained mutation builders command adapters and migrate their helper tests. Keep `add_authoring_shot` consumers in `timeline_structure/adopt/duplicate/restructure` working. Delete deprecated engines only after replacement behavior exists, not the whole useful module. |

### Executable regression nodes to retain/convert (not results of this task)

Already present at `7a7acc0e` (source-inspected; **not run here**):

* `tests/editing_conformance/test_recipe_m1_commands.py::test_quantization_once_with_rational_fps_and_ms_codec`, `::test_disjoint_same_child_rebase_and_original_guards_after_materialization`, `::test_shared_first_materialization_golden_preserves_original_sibling_capture`, `::test_compiler_records_exact_retained_document_pin_without_evaluating_anchor` and `::test_structural_group_uses_generic_creation_and_restores_order` pin M1's limits as well as its successes.
* `tests/sdk/test_media_transcript.py::test_word_ids_survive_a_front_trim_of_the_same_recording`; `tests/sdk/test_timeline_media_verbs.py::test_trim_slip_and_move_keep_the_window_equal_to_the_hold` and `::test_for_on_windowless_footage_stays_windowless_and_unrefused`; `tests/test_timeline_editing_helpers.py::test_source_timeline_conversion_is_exact_and_rate_aware` and `::test_quantize_interval_reports_rounding_and_rejects_collapsed_ranges` preserve source/interval math.
* `tests/sdk/test_timeline_sheet.py::test_text_verb_and_code_make_the_same_change`, `::test_the_music_bed_is_in_the_sheet_and_its_line_edits_it`, `::test_visual_clip_looks_round_trip_and_omission_clears_them`, `::test_trim_syntax_on_a_visual_layer_is_refused_atomically`; `tests/sdk/test_timeline_transaction.py::test_nested_edits_join_the_outer_transaction` preserve actual CLI/Python/sheet behavior.
* `tests/sdk/test_timeline_commit_provider_document.py::test_complete_document_roundtrip_reuses_original_images_and_unknown_fields`, `::test_occurrence_edit_closes_reused_sibling_and_new_exact_child`; provider `::test_undo_detects_aba_and_unchanged_write_publications`; revisions `::test_runtime_commit_history_keeps_same_content_publications_and_walks_edges` preserve source closure/opaque/history identity. Sync's `::test_invalid_ack_retains_exact_flight_and_suffix` and `::test_dependent_suffix_conflict_preserves_original_guards_and_identity` must survive generalization. Inverse ABA guards remain stronger than dependent-suffix equal-state guards, per PLAN.

Convert selected frozen behaviors into these main suites, not the whole R4 suite:
`tests/sdk/test_timing_compiler.py::test_compiler_does_not_mutate_declared_bundle_state_or_commands`,
`::test_compiler_resolve_is_idempotent_on_the_available_fixture`,
`tests/sdk/test_timing_cycles.py::test_cycle_refusal_keeps_inputs_state_and_commands_immutable`,
`::test_real_checkout_transaction_rolls_back_new_cycle`,
`tests/sdk/test_timing_compiler_consumers.py::test_authored_placement_edits_adopt_the_final_compiler_result`,
`::test_compiler_refusal_cannot_expose_a_final_authored_placement`, and
`tests/sdk/test_timeline_inverse_compiled_timing.py::test_source_window_convention_is_preserved`,
`::test_restored_until_remains_live_when_its_anchor_moves`. Add supported exact
source-word DocumentPin, rational tie/half-open boundary and composed map vectors,
ordered delete restoration/staged inverse, stable add/swap IDs, and unchanged-write
clear/null concurrency cases. Adapt R4 raw-dict setup to real recorded commands;
`port-failure-index.tsv` identifies those setup/admission failures and absent
curve-generator/parity artifacts. Never add a Pack V3 stub or suppress the runner
guard. Preserve existing successful behavior expectations; if temporarily lost,
use only strict expected failures naming restoration, never refusal rewrites.
Provider `test_restore_is_sole_and_strictly_pair_guarded_until_adapter_lands`'s
unsupported branch is not the desired outcome: the authorized M1 fix must replace
it with positive main restore/semantic inverse coverage before this queue opens.

**Extension seams, no M5:** `core/timeline/moments.py:Context/resolve`, compiler
reference/dependency validation and main pinned source maps expose `MarkerRef` /
`resolve_marker(ref, pinned_marker_table, occurrence/time_map)` and `SignalRef` /
pinned resolver interfaces plus core fixtures only. Fixtures cover valid/missing,
ambiguous, foreign pin, domain mapping and out-of-range inputs; missing marker
fails closed without changing bindings or materialized state. No detector,
publication/republication service, generalized signal binding, sampling host,
extension discovery or new authoring UI before the hard stop. Follow the bounded
interfaces in `extensions.md`, not its future M5 publication model.

**Pending handoffs:** group ownership/move operation design (Agent/App/orchestrator);
Runtime scope of lifecycle/bootstrap and legacy endpoint rejection; exact explicit
map support shared with Runtime Read/Viewing; compiler inputs to the published
Composition consumer (Viewing owns See, no scene-in-save); log/local compatibility
presentation with Runtime/App. These are dependencies to confirm against behavior,
not decisions made here. Existing advisory-check/scene-gap tests must be reviewed
with Viewing to preserve the finding while removing renderer-dependent acceptance.
M1 restore implementation/evidence and closure are prerequisite gates. This task
ran only read-only `git show`/`rg`/`sed` inspection and a stdlib AST/line-count probe
(exit 0); no pytest, make, network, installs, full suite or test-service requests,
and no claim that any proposed regression passes. Product worktree unchanged.
