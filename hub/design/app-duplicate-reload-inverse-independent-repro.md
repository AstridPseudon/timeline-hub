# Independent verification: duplicate → RAW compile → reload → guarded inverse

**Confirmed native Agent blocker, 2026-10-20.** The exact repro is valid on both archived Agent S2 `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933` and archived current `78d548cf059a5875f5333590e6ae84051504f809`. Either derived root identity alone is sufficient. No App implementation, patch application, old-attempt merge, wire change or dependency change was made. App worktree `0ea988bdd2907c876b82fd2620820e3fb6d6ea84` remains clean, **+0/−0 product and test lines**.

This adds independent evidence to the already-filed **1155 native App-contract escalation**. It does not replace the settled root identity rule or qualify a Runtime/App pair.

## What was run

Read PLAN first, then `design/m2-occurrence-duplicate.md` (the settled derived-root rule), `design/app-duplicate-identity-review.md`, `design/app-refreshed-duplicate-source-port.md`, and the prior worker's source/logs. Caller reserves only occurrence/shot IDs. Agent derives the two existing root strings against the actual compiled destination; nested metadata and historical output/task/association values remain opaque.

The original minimal repro was copied byte-for-byte into this worker's private notes and run unchanged in all eight combinations. Both archived sources were imported read-only, with `PYTHONDONTWRITEBYTECODE=1`; pytest cache was disabled and cwd was private scratch. Eight relevant source/test/fixture files in each archive were compared byte-for-byte with `git show <frozen-ref>:<path>` before testing and rehashed afterward. This includes the original 33-test body and its native golden; none was edited. Hash details and commands are in the [private notes](../workers/app-m2-duplicate-reload-inverse-independent-repro/notes/matrix-results.json).

| Exact input variant | S2 result | Current result |
| --- | --- | --- |
| Both root fields | exit 1: `original authored guard changed` | same |
| `stable_deep_link` only | exit 1: same error | same |
| `output_identity` only | exit 1: same error | same |
| Neither root field | exit 0: exact guarded undo | same |
| Unmodified native recipe suite | **33 passed**, 1.55s, exit 0 | **33 passed**, 1.43s, exit 0 |

All six primary failures have kind `inverse_conflict`, ref `occurrence:occ-copy`, path `[]`. The unchanged repro retains its required successful-undo call and exits with the native exception; it was not rewritten into an expected failure.

A separately authored diagnostic trace ran all eight combinations, checked stage immutability, and printed the actual records, RAW row, reopened root, and error details. All eight diagnostic checks passed. These are diagnostic assertions, not eight passing behavior regressions. For each no-fields control it additionally proved exact undo → reload → redo → reload → second undo, and removal of **both** created roots. A separate synthetic same-value publication on the created root was correctly refused as `intervening_write`; it is not part of the primary repro.

## Actual path and mismatch

1. Construct the native suite's `duplicate_document(shared_shot=True)`. Add the chosen valid factory-produced source identity fields, `parent_document_id='doc /é'`, and opaque historical/nested data **before** opening the document. Recompute its parent content digest. This is fixture input construction, not a post-materialization edit.
2. Open with normal `bundle_from_document`; capture and execute normal `occurrence.duplicate`. Its single record has exactly two absent-to-present root writes: `shot:shot-copy` and `occurrence:occ-copy`. `derived_writes` is empty. The occurrence write's `after` equals the actual precompile `State(plan.bundle).get(ref, [])`, including the source identity strings.
3. Call normal `document_from_bundle(plan.bundle)` without any intervening edit. The RAW destination has the correct new fields from the existing factories and its actual compiled shot revision. The source/sibling rows remain exact and the new shot references an included internal timeline revision.
4. Open that exact RAW document with normal `bundle_from_document`. Compare its root with the original recorded `after`: **only the selected identity fields differ**. The comparison uses the union of keys, so it also checks absence. Opaque metadata/output records are unchanged.
5. Call the native test helper's normal guarded inverse with the unchanged records and an empty intervening-history sequence. The inverse rejects the root at `inverse.py:366`, before installation. Snapshots verify that original document, input bundle, plan bundle, records, RAW document and reopened bundle remain unchanged throughout, including after refusal.

For the both-fields case, the actual output key changes from:

```text
recorded: project/project-1/document/doc%20%2F%C3%A9/occurrence/occ-0/output/final-video
reloaded: project/project-1/document/doc%20%2F%C3%A9/occurrence/occ-copy/output/final-video
```

The recorded deep link points at `chapter-shot/revision/shot-1/occurrence/occ-0`; the RAW/reopened link correctly points at `shot-copy/revision/authoring-shot-revision-44fbac89c5e00d8c893cd59c66716b3d5ca1366e54bb1ed008c5118fe74f8dc5/occurrence/occ-copy`. Full values and actual root-create records are in [trace-s2-both.log](../workers/app-m2-duplicate-reload-inverse-independent-repro/notes/trace-s2-both.log).

Relevant frozen-source locations, identical in the relevant mechanism on both versions:

- `sdk/timeline/native_occurrence_duplicate.py:41–45`: copies the source row, removes revision keys and changes the two reserved IDs; the create records the remaining source strings.
- `core/timeline/authoring_bundle.py:231` and `:1045–1048`: derives present identity fields only for new placements, against the compiled destination revision.
- `sdk/timeline/commit.py:149,218`: normal document open/compile path. Provider `commit.py:911–917` compiles the canonical document then copies `plan.records` into prepared history, without reconciling those identity values. Thus the repro is not bypassing a later record-normalization step.
- `sdk/timeline/_command_state.py:299–310`: whole-occurrence matching handles the known shot alias, but otherwise compares the entire recorded root. `sdk/timeline/inverse.py:366` correctly refuses the resulting mismatch.

The original 33 pass because their reload/inverse cases have no root identity fields; their identity derivation case checks the RAW compiled row but does not then reload and undo it. The no-fields control is meaningful: it retains `parent_document_id`, nested identically named fields, output history and the same source/closure. It removes only the two input root fields, successfully removes both newly created roots, and preserves the exact original document through repeated history operations. It is a separate diagnostic input, not a proposed product workaround.

## Smallest repair scope and required safety

**Agent-owned consistency repair at the native root-create / compiler / recorded-history boundary.** Make the newly created occurrence's authoritative recorded representation agree with the compiler-derived destination identities, using the existing factories and actual compiled pin. Keep capture, replay, in-memory inverse, immutable reload inverse and redo consistent. Prefer finalizing the created row and its record coherently over globally ignoring identity fields in root comparison. Exact code placement remains the Agent owner's decision; this investigation implements no fix.

No App-supplied identity strings, schema/DTO/endpoint additions, suffix remapper, clearing of valid fields, history rewriting, or Runtime changes are justified by this counterexample. Do not weaken root equality or accept arbitrary replacement strings. If legacy pre-repair records need accommodation, it must use authenticated publication boundaries and exact factory equality, not today's row as its own proof.

Retain complete publication ancestry and intervening-write checks, including unchanged-value writes and A→B→A on overlapping guarded addresses. Preserve the existing distinction between history-sensitive undo and the established value-level ordinary-replay policy. Keep collisions, surviving dependents, collection membership/order, source/sibling isolation and opaque equality guarded.

Add the combined regression to Agent's existing editing-conformance suite: both/link-only/output-only/no-fields → normal RAW compile → reopen → exact undo → redo → second undo. Include escaped document IDs and the timeline-ID fallback; check the RAW fields before adapters can recompute them, and retain existing ABA/history cases. Keep all original 33 expectations unchanged. This is evidence for the settled rule, not evidence it should be revised.

## Exact commands and evidence limits

From private scratch, define:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
N="$O/workers/app-m2-refreshed-duplicate-source-port/notes"
W="$O/workers/app-m2-duplicate-reload-inverse-independent-repro/notes"
cd "$W"
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$W/run_matrix.py"
```

Matrix runner exit **0**; it runs the following exact child commands for each `S="$N/agent-s2"` and `S="$N/agent-source"`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python -m pytest -q -c /dev/null -p no:cacheprovider "$S/tests/editing_conformance/test_recipe_occurrence_duplicate.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/repro-native-duplicate-inverse.py" both
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/repro-native-duplicate-inverse.py" stable_deep_link
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/repro-native-duplicate-inverse.py" output_identity
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/repro-native-duplicate-inverse.py" none
```

Exit codes in order: **0, 1, 1, 1, 0** for each source. Every child invocation/environment/result/log path is retained in `matrix-results.json`. Diagnostic command, for each source and each of `both stable_deep_link output_identity none`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/trace_native.py" "$mode"
```

All eight diagnostic exits **0**, logs `trace-{s2,current}-{mode}.log`. `git diff --check` and final `git status --porcelain` are clean.

This is native in-process evidence at the same trusted `AcceptedRecords` test boundary as the original suite. The helper supplies a synthetic accepted publication entry; it does not prove actual Runtime acceptance, authenticated provider history loading, localhost transport, App gesture ingress, lost-ACK/restart retry or installed-pair behavior. Provider persistence consistency above was checked by source inspection, not a live commit. No Runtime/browser/socket/full/install/project-tsc/build/App suite was run or requested. Shared dependencies, runtimes, venvs and caches were untouched. Only this shared report and this worker's private notes/report/commit-msg/DONE were written; no KEEP or patch artifact was created.

Recommended next step: attach this evidence to existing escalation 1155, repair and qualify natively under Agent ownership, then independently re-review the bounded App port. Do not apply the old attempted patch as part of this finding. Verification task is complete; native duplicate adoption remains blocked by the confirmed defect.
