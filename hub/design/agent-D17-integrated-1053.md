# Agent D17 integrated current-home qualification

Date: 2026-10-23

## Verdict

**FAIL for the requested one actual-home qualification.** The exact integrated
40-test selection against the current Runtime `49ce53289bc37d9387a7d9e6b9c9b16072162181`
ran 36 tests successfully and failed 4 source-copy inverse cases. The exact
independent inverse selection passed all 281 tests. No product, test, contract,
environment, service, pin, or shared dependency was changed.

This is a current integrated-runtime result, not a legacy 1365 result. The
failure is in current Runtime inverse-stage validation:
`inverse stage write differs from its sequential input`.

## Exact trees and source boundary

- Agent HEAD: `ce1d1cca87379029924b0be6f98564f556597107`
- Agent tree: `68dee9124ab8f4026ac4119f816eceec654f0bba`
- Runtime checkout: `/home/user/work/runtime`
- Runtime HEAD: `49ce53289bc37d9387a7d9e6b9c9b16072162181`
- Runtime tree: `364380ae064c512c0a0d2b8903a599b7026642f4`
- Agent and Runtime were clean before and after the proof.

The 11 source/test blobs exactly match the reviewed `d57207fb5` candidate:

```text
astrid/sdk/timeline/_commit_patch.py                         081423635e9c132382c395d15af4a3ba8d34a74d
astrid/sdk/timeline/_recording.py                            10b17db43964ed0016e3d0527910bc9e56ccaf4f
astrid/sdk/timeline/_root_inverse.py                         5d2a1165c96e140482b427da0f3e26f06071f080
astrid/sdk/timeline/commands.py                              e06810281e6aafced856b3d0efce1753a733833c
astrid/sdk/timeline/commit.py                                65f55e30d7eb03f38e21fe02a26b56092859e498
astrid/sdk/timeline/inverse.py                               6385c8c3caa9761059d766b6487c967463736fb9
astrid/sdk/timeline/native_timeline_duplicate.py              6f3ff25caf8d2f165c83929c0ae4b386185d2376
astrid/sdk/timeline_duplicate.py                             1bc61a027ad8bf33e11affb472c30fe81ec31797
tests/editing_conformance/test_commit_runtime_source_copy.py 1cf5b42e477b28126b5ae12bfe217d6d224bae14
tests/editing_conformance/test_recipe_timeline_source_copy.py 89841e0475f5001a9275078254a8cbbba26b523f
tests/sdk/test_timeline_restructure.py                       03fe581af64bcb7bcd47b50a5a51acf36761ae49
```

The excluded `tests/integrations/test_d09_managed_scene_only.py` remains equal
to the integration base. No other path changed.

## Tests

The exact final-40 selection from the review, with only Runtime changed to the
verified current checkout, was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= \
-p no:cacheprovider --timeout=45 \
tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter \
tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared \
tests/editing_conformance/test_commit_runtime_source_copy.py \
tests/editing_conformance/test_recipe_timeline_source_copy.py
```

Result: **4 failed, 36 passed in 17.46s**.

Failures:

- `test_source_copy_real_port_receipts_preview_undo_redo`
- `test_repeated_source_copy_real_port_idempotency_and_guarded_inverse[False]`
- `test_repeated_source_copy_real_port_idempotency_and_guarded_inverse[True]`
- `test_source_copy_retained_inputs_whole_undo_redo`

All four fail while submitting the inverse, before the expected document
round-trip assertion, with Runtime's `inverse stage write differs from its
sequential input`. The source-copy authority, refusal, raw-preservation,
unknown-outcome, and production-caller cases in the same selection passed.

The exact inverse-281 selection was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= \
-p no:cacheprovider --timeout=45 \
tests/editing_conformance/test_doc_patch_mirrors.py \
tests/editing_conformance/test_inverse_clip_mirrors.py \
tests/editing_conformance/test_inverse_stage_images.py \
tests/editing_conformance/test_inverse_clear_batches.py \
tests/editing_conformance/test_grouped_clip_cache_inverse.py \
tests/editing_conformance/test_step_undo_v2.py \
tests/editing_conformance/test_provider_step_undo_v2.py \
tests/editing_conformance/test_recording_clear.py
```

Result: **281 passed in 38.63s**.

## Same-process Runtime provenance

A temporary read-only pytest observer recorded module origins and SHA-256s
before and after every case. The observer was outside the worktree and did not
alter imports or execution.

For the instrumented executions, the worker directory was added to
`PYTHONPATH` solely to load `observe_origins`, and `-p observe_origins` plus
`D17_OBSERVATION_LOG` were supplied. The test selections, Agent code, and
Runtime selection were otherwise unchanged.

- 40 selection: 40 before + 40 after records, 40 cases, 39 Runtime modules.
- 281 selection: 281 before + 281 after records, 281 cases, 4 Runtime modules.
- Every observed module path was under `/home/user/work/runtime/`.
- Every before/after snapshot had Runtime HEAD
  `49ce53289bc37d9387a7d9e6b9c9b16072162181`, tree
  `364380ae064c512c0a0d2b8903a599b7026642f4`, and empty status.
- For every case, each module present before and after had the same origin and
  SHA-256. The evidence logs are in the worker directory as
  `observations-40.jsonl` and `observations-281.jsonl`.

Runtime 1365 was not on `PYTHONPATH`, was not assigned to
`ASTRID_RUNTIME_CHECKOUT`, and no fixture archive was executed. It was used
only for a read-only source comparison. Current Runtime's
`timeline_commit_auth.py` is a meaningful new execution relative to 1365:
the diff is 246 lines and includes authenticated inverse-stage boundary,
history, and binding handling; its current SHA-256 is
`65fd735edafa0e9f4a77aaf4f473095f1539ea1ce453439177e9fe7f39b4466f1`.

## Post-proof checks

```text
git diff --check                                      PASS
git diff --check 7abfb8d...HEAD                      PASS
scripts/vendor_lock.py check runtime.lock.json      PASS: ok runtime.lock.json
scripts/artifact_manifest.py --check                PASS: artifacts.json is current
```

The independent review's quality evidence is reused on these exact 11 blobs:
Ruff **2149/2149** and mypy **1912/1912**. Global quality was not rerun.

## Decision / next step

No decision was available to make beyond the settled plan. The current-home
qualification is not accepted because the 40-test selection is not green.
Investigate the Runtime-49ce inverse-stage mismatch for the four failing
source-copy undo cases, then rerun the exact 40 selection; retain the passing
281 result and the provenance controls. Do not relabel this as a legacy timing
failure or proceed to G5 retirement from this run.
