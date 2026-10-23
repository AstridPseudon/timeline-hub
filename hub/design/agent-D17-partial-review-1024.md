# D17 partial review — FAIL

Date: 2026-10-23

## Scope and verdict

Reviewed Agent merge `f209b04551e7272e33117996bd8e2624e2808b93` against
`80680fab5` and `ef851b22c`. Runtime authority was inspected only at the
immutable pin `1365e4b17b31c4a7093d5943674637067fd2bab4`.

Scoped result: **PASS** for the bounded lost-ack repair, known-refusal archive
cleanup, the 15 passing source-copy/neighbor selection cases, and all 12
SQL-dump negative controls.

Scoped result: **FAIL** for the mandatory repeated-copy guarded whole undo/redo
positive and raw-parent config-presence positive. Therefore the overall result
is **D17 FAIL**. This is not a G5-ready result and does not qualify the full
v2 contract or the remaining red behavior.

No product or test code was edited by this review. No xfail, skip, expectation
reversal, Runtime waiver, full suite, HTTP/browser/native suite, or daemon was
used.

## Focused evidence

Environment:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1
PY=/home/user/work/venv-agent/bin/python
```

The 15-case selection command covered both original restructure positives,
both lost-ack parameterizations, the accepted/preview/undo/redo neighbor, and
all recipe source-copy controls. Result: **15 passed in 4.42s**.

```sh
$PY -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=30 \
  --basetemp=/tmp/agt-D17-partial-review-1024/pytest-selection \
  tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter \
  tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_unknown_outcome_retains_destination_and_exact_retry \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo \
  tests/editing_conformance/test_recipe_timeline_source_copy.py
```

The 12 guard cases (11 authority/claim variants plus project-wide occupied
shot) used complete SQLite dump equality and passed: **12 passed in 4.80s**.

```sh
$PY -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=30 \
  --basetemp=/tmp/agt-D17-partial-review-1024/pytest-guards \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_refuses_bad_authority_or_claims_without_writes \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_rejects_project_wide_occupied_shot_without_writes
```

The production caller/refusal archive control passed: **1 passed in 1.83s**.
The caller is still `duplicate_timeline -> _duplicate -> _commit_bundle ->
timeline.open(...).session.submit` with the exact authenticated source
reference and durable request carrier.

```sh
$PY -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=30 \
  --basetemp=/tmp/agt-D17-partial-review-1024/pytest-archive \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_production_duplicate_caller_uses_authenticated_semantic_and_archives_failures
```

The two mandatory red positives remain active and fail independently; they
were not converted to xfail: **2 failed in 2.27s**. Repeated physical-root
copy reaches undo, then Runtime rejects it with `original authored guard
changed` (the Agent surfaces `CommitConflict`); redo is not reached. A source
with raw `parent.clips=[]` and `parent.registry={}` but no
`parent.config.clips` gains config mirror keys during copy, so the exact
raw-parent equality assertion fails.

```sh
$PY -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=30 \
  --basetemp=/tmp/agt-D17-partial-review-1024/pytest-red \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_preserves_raw_parent_config_presence
```

## Independent topology/effect diagnosis

The source fix belongs to the Agent normalizer, not Runtime. In
`astrid/sdk/timeline/native_timeline_duplicate.py:76-84`, the semantic copy
assigns the authenticated source's raw parent fields, including top-level
`clips` and `registry`. The reviewed range does not change
`astrid/sdk/timeline/_commit_patch.py`.

At `_commit_patch.py:182-195`, `effect_diff.logical_parent()` deep-copies the
parent and unconditionally removes top-level `clips`/`registry`, inserting
their values into `config`. This loses the absent-versus-present topology for
the exact counterexample above. The candidate and its effect/binding then no
longer describe the same parent image: the effect projection advertises the
config aliases while the raw candidate preserves the top-level fields and
does not author those config keys. This is a genuine Agent raw-topology/effect
mismatch, not a Runtime authority defect.

The pinned Runtime authority code at
`runtime_protocol/timeline_commit_auth.py:686-692` requires an authenticated
accepted parent image, or a specifically reconciled materialization, and
otherwise raises `provider intermediate parent lacks an effect image`.
Relaxing that check or duplicating the separate Runtime authority
implementation would be an invalid waiver. The required repair is lossless
parent effect/binding normalization that preserves presence and exact
physical sharing, followed by the existing guarded inverse checks.

## Contract and diff audit

The source-copy request fixture includes the v2 base pair, commands, label,
steps, merge, reads, dry-run, source, rationale and group ID. Passing controls
exercise accepted receipts/data, preview `would_status`, history records,
command dependencies, effects/steps and whole undo/redo for the single-root
case. Existing provider code still contains accepted, merged/rebased,
historical head/document, conflict reason/head, invalid code/path/hint/
suggested-command, records, preview and `undo_steps` paths. This review did
not claim broad v2 requalification; those paths are preserved but outside
this focused result.

The lost-ack repair correctly retains the exact flight/body/key when the
acknowledgement is lost before or after acceptance. Reopening through public
`timeline.open(...).session.flush()` retries the same request; the
accepted-before-disconnect case returns the original receipt. Known definitive
refusal still uses the existing archive wrapper. Ambiguous outcomes are not
archived.

The cumulative `80680fab5..f209b0455` diff has 17 paths, including
manager-supplied merge-forward repairs. The D17 seven-file delta against
`ef851b22c` is limited to command/commit wiring, duplicate semantic,
production wrapper, two source-copy test files, and restructure neighbors.
The original restructure semantic assertions remain present; the former
repeated-copy strict xfail is removed, not hidden. Current changed test files
contain no `xfail`, `skip`, or dropped red expectation.

## Quality checks

```text
compare_mypy_baseline: current=1912 baseline=1912 — PASS
compare_ruff_baseline: current=2149 baseline=2149 — PASS
Ruff on D17-owned duplicate/source-copy files — PASS (All checks passed)
vendor_lock.py check runtime.lock.json — PASS (ok)
artifact_manifest.py --check — PASS (artifacts.json is current)
git diff --check 80680fab5..f209b0455 — PASS
git diff --check ef851b22c..f209b0455 — PASS
```

Ruff over the entire neighboring `tests/sdk/test_timeline_restructure.py`
still reports the known four test-only findings (two import-order I001s and
two F811 fixture redefinitions at the two new real-service tests). The
baseline/count gate is unchanged; this review did not alter that neighboring
file to mask lint findings.

## Decision and next step

The settled plan decision is honored: D17 remains blocked by the two active
red positives. NewSol's normalizer owns the source fix. Preserve all passing
lost-ack/archive/SQL evidence and require raw-parent topology/effect
normalization plus repeated shared-root guarded undo and redo to pass before
any D17 PASS or G5 writer retirement statement.
