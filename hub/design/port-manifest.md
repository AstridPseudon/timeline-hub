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
