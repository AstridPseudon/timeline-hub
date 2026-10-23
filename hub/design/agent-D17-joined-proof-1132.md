# Agent D17/G2 joined consumer qualification

Date: 2026-10-23

## Verdict

**PASS for this bounded joined qualification.** The exact current 40-case
duplicate/source-copy selection passed, the exact current 281-case inverse
selection passed, and the new public whole/selected v2 undo caller passed both
parameterizations: **323 passed total**. This qualifies the current Agent
consumer pair against the pinned Runtime for D17/G2 evidence. It does not
claim the separately pending producer integrations, clear P1, or authorize
G5 by itself.

No tracked files, tests, pins, dependencies, services, or Git refs were
changed. No product code or test was deleted, skipped, weakened, or edited.

## Exact trees

- Agent worktree: `/home/user/work/wt/agt-D17-joined-proof-1132`
- Agent HEAD: `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`
- Agent tree: `ff6c46d0b5ba420e3fb9e912e5a30c7a9a41e27b`
- Runtime checkout used for every test: `/home/user/work/wt/rt-pin-3b926efa`
- Runtime commit: `3b926efab2eed122d374540baee297d4cdcec62a`
- Runtime tree: `b794170504544b259781e50d7ca4d61b6729e67c`
- Agent and Runtime status were empty before and after.

The 11 D17 source/test blobs are the reviewed current closure (the blob IDs
are unchanged from the reviewed D17 set):

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

The merged public G2 caller files are also the expected reviewed blobs:

```text
astrid/sdk/timeline/sync.py                         3f8b7f9dec28d4e7b500088e9afefea394899922
tests/sdk/test_timeline_sync_native.py               1d54c89498a280ee29880ece96d699fa56b7861f
tests/sdk/test_timeline_commit_provider_runtime.py  f37a8e20db50694a24fb8dd413cb6df425fbf9cd
```

## Exact qualification commands and results

Each command used `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa`,
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa`, the Agent venv,
`--tb=short -o addopts= -p no:cacheprovider --timeout=45`, and the read-only
observer described below.

1. Current exact 40 selection:

```text
tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter
tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared
tests/editing_conformance/test_commit_runtime_source_copy.py
tests/editing_conformance/test_recipe_timeline_source_copy.py
```

Result: **40 passed in 34.96s**.

2. Current exact inverse-281 selection:

```text
tests/editing_conformance/test_doc_patch_mirrors.py
tests/editing_conformance/test_inverse_clip_mirrors.py
tests/editing_conformance/test_inverse_stage_images.py
tests/editing_conformance/test_inverse_clear_batches.py
tests/editing_conformance/test_grouped_clip_cache_inverse.py
tests/editing_conformance/test_step_undo_v2.py
tests/editing_conformance/test_provider_step_undo_v2.py
tests/editing_conformance/test_recording_clear.py
```

Result: **281 passed in 171.87s**.

3. New public caller:

```text
tests/sdk/test_timeline_commit_provider_runtime.py::test_public_undo_redo_persists_v2_effect_bindings
```

Result: **2 passed in 4.36s** (`selected=False` and `selected=True`). This
real public path checked the complete v2 wire/provider path, including request
base pair, commands, label, stable inverse step/ordinal and empty submitted
patch, source/dry-run/preview behavior, exact idempotency replay, canonical
and selected restoration, history/undo_steps, provider reads/dependencies,
effects, and every effect's before/after binding. It did not drop the actual
v2 effect bindings.

The 40-case body passed the original duplicate positives and the mandatory
guards on the meaningfully fixed pair, including raw presence/media and source
pair closure/order/sharing, guarded undo/redo and idempotency, archive cleanup
and unknown-outcome handling, forgery/occupied-ID refusal, ABA and surviving
consumer controls. The original tests were unchanged.

## Same-process provenance

The observer was loaded from the external worker scratch area and only read
module files and Git metadata. It did not wrap or replace providers, stores,
requests, history, executor calls, or imports.

- 40-case log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-joined-proof-1132/probe/observations-40.jsonl`
  - 40 cases, 80 before/after records.
- 281-case log: same directory, `observations-281.jsonl`
  - 281 cases, 562 before/after records.
- Public log: same directory, `observations-public-2.jsonl`
  - 2 cases, 4 before/after records.

Every record reported Runtime commit
`3b926efab2eed122d374540baee297d4cdcec62a`, tree
`b794170504544b259781e50d7ca4d61b6729e67c`, and empty status. For every case,
the common loaded Agent/Runtime module origins and SHA-256 hashes were stable
between the before and after snapshots. Newly imported modules were retained
in the after snapshot; no existing module identity changed.

## Postchecks

```text
PYTHONDONTWRITEBYTECODE=1 TMPDIR=<worker probe> /home/user/work/venv-agent/bin/python -m ruff check --no-cache <11 D17 files>
All checks passed!

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check
PASS
```

The direct `scripts/vendor_lock.py` spelling is not executable in this
worktree; invoking the same checker through the prescribed Agent interpreter
passed. The independently reviewed unchanged-source quality evidence remains
Ruff **2149/2149** and mypy **1912/1912**; no new full quality budget was
spent.

## Scope and next steps

No original-58 recovery, HTTP/P1/P4, native-14, full, browser, daemon, or
moving-main/old-49ce/1365 run was made. The separately pending producer
integrations `28978+4445` remain pending and were not made a prerequisite for
this consumer-body run. The prior 49ce result (36 pass/4 fail) is not evidence
for this pair and was not retried.

This PASS clears the old duplicate qualification only. P1 remains the NO-GO
gate for G5 merge, and producer integration plus any later G5 decisions remain
with the orchestrator.
