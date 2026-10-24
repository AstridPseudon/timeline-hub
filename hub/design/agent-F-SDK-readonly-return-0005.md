# SDK FIRSTRETURN classification report

No product, test, generated, or pin files were modified. No pytest, compile, full-suite, or test-service execution was performed.

Evidence:

- Current tree: `f88cc5242d4b6c87b97a83878b86ec3168daa3db`
- Current tree hash: `c8ce72197087f4ef7dc86c979ca0c8fb43ff1581`
- Retained outcome shard: `974f3324334ca329e5140b72a54fb5820fc60f4268a2b5178c99ce2503d34c4b`
- Retained full run: 17,159 passed, 262 failed, 5 errors, 4 skipped; no retry.
- D14/D23/H9 remain visible, unskipped, and unchanged.
- Worktree remains clean.

## Family findings

| Family / nodes | Classification and source-backed cause | Bounded owner scope |
|---|---|---|
| `helper_capture16` | One genuine defect: `test_genuine_anchor_capture_has_exact_source_scope_and_base_pair` fails with missing `publication_id`. `sync.py:171` reads the exact revision/publication pair, but `commit_session.py:275-276` calls `fetch_bundle()` with revision only. | Agent SDK session/G2: pass `base["publication_id"]` at that call. |
| Remaining 15 helper nodes | Stale fixture/API seam. `publish.py:249` refuses because `test_timeline_restructure.py:413-415` supplies an `open_bundle` lambda that ignores `publication_id` and returns a bundle without the exact publication pin. The guarded-input tests therefore inspect a prior peer call rather than their own publish. The `"second"` cut case separately reaches `_timing_evaluators.py:387` because the fixture writes `on` without an exact captured word binding. | Test fixture owner: use the revision-pinned opener and add the exact transcript binding for `"second"`. Do not weaken closure or timing guards. |
| `persistence7` | All seven fail before their intended persistence assertions with `AttributeError: '_FakeTimelines' object has no attribute 'history'`. `TimelineSession.open()` in `sync.py:171` now requires history; fixture `_FakeTimelines` only implements `open_composition`/`open_bundle` (`test_timeline_persistence.py:49-69`). | Persistence fixture owner: implement the current history/pair contract. No product bypass. |
| `normal_publish6` | All six stop at `publish.py:249` with `closure membership changes require a semantic command`; same stale two-argument fixture opener described above. | Restructure/runtime fixture owner; repair opener seam before judging publish behavior. |
| `restructure6` | Five have the exact retained error `restructure requires its exact current closure; reopen the timeline` at `publish.py:376`, caused by the same stale opener. CLI restructure retains only return code `1`; exact CLI stderr is absent from the retained outcome, so that subcase is unconfirmed beyond the shared fixture path. | Fixture owner first; CLI symptom requires one future targeted run after repair. |
| `publish_connection2` | Both fail at `publish.py:249` for the same stale closure opener; no connection-ownership conclusion is justified. | Fixture/API seam owner. |
| `occurrence_delete_provider2` (`count=3,index=0/1`) | Genuine R2 inverse defect. `_commit_patch.py:522-541` compares recomputed nested inverse effects with captured effects and raises `nested inverse effects differ from execution` at line 539. | Agent R2: restrict work to `occurrence.delete` inverse staging/effect projection. Preserve refusal guards. Exact inherited-vs-captured key delta requires execution, which was prohibited. |
| `capture_closure_source2` (`working_copy=False/True`) | Stale oracle/API expectation. The failing test requires no inline `capture_snapshot`, but `invocation.py:2867-2892` deliberately retains inline capture data for the runtime-capture path; the same file’s later test explicitly expects inline `capture_snapshot`. | Capture-contract test owner: reconcile the oracle with the current inline-versus-reference branch. No production change inferred. |
| SDK schema singleton | Genuine schema omission. `commands.py:65-76` registers `timeline.restructure`; `publish.py:389-401` emits and executes it. `edit-command.schema.json` has no `TimelineRestructureArgs` or `timeline.restructure` union condition, producing the `KeyError` and union-inventory failures. | Agent schema/API owner: update the authoritative schema source and regenerate the artifact. Do not patch generated JSON only. The generator/source path was not identifiable from this tree. |
| P4 singleton | Stale fixture metadata. `cases.json:20-22` names `test_ordinary_edit_literal_move_uses_native_outbox`; current source defines `test_ordinary_edit_literal_move_uses_commit_outbox` at `test_cli_commit_move.py:101`. | P4 fixture owner: update the symbol reference only. |
| Restructure guard singleton (`historical`) | Genuine guard-order/diagnostic defect. The guarded fixture explicitly replaces the legacy opener with `RemoteTimelines.open_bundle` and expects `original revision/publication pair changed`; `_commit_restructure()` instead merges local state and raises the generic closure error at `publish.py:376`. | Restructure/G5 owner: validate the original revision/publication pair before generic closure comparison, preserving no-write refusal behavior. |
| Commit-provider scalar singleton | Genuine R2 materialization-binding defect. `_materialization_sites()` records `(old,new,owner)` at `_commit_patch.py:957`, but `continuation()` resolves successors by `old` only at lines 1006-1012. Independent sibling successors are conflated and rejected as `inverse image has ambiguous successors`. | Agent R2: make successor resolution owner/site-aware so later sibling pins survive inverse. Exact replacement structure requires execution. |

The already-owned graphroot5, scalar1, and scene2 nodes were not redispatched.

## Contract disposition

The specified v2 base-pair, scope, command/step metadata, receipt, dependency, binding, effect, history, undo, preview, and structured-error contract was not changed or weakened. The schema finding is specifically based on the production caller emitting `timeline.restructure`; it should not be reclassified as harmless provider-only behavior.

## Test status

No tests were run, by explicit READONLY/FIRSTRETURN instruction. No PASS, baseline, or upstream claim is made beyond the retained outcome shard and current source/tree inspection.