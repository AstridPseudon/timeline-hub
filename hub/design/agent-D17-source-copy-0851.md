# D17/G5 source-copy bounded draft — BLOCKED, do not integrate

Base: f77a750ad2318f8f2eb8ad3f6efc1ba55e7862d3 (preserved G5 WIP). This is still the old-base draft, not a current-port qualification. P1 remains gated. D17 is NOT complete.

## Work

Added one new registered Python semantic, `timeline.duplicate`, on the existing op/JSON-args carrier. Native parameters are registered with the provider; no public schema, client, tuple, pin, runtime.lock, dependency installation, Runtime executor, or direct store publication was added.

The private resolver calls actual Runtime `port.revision_closure(source_ref)`, with the five exact fields from handoff 0842, checks the returned scope/revision/digest, consumes every source media pin with `raw_media_info`, and hydrates document captures. The handler copies authenticated raw parent fields, shot payloads and internal timelines, preserving opaque values and repeated sharing/order. Known shot-item identities use the existing factory; fresh occurrence/shot identities use normal instrumented creation. Created-ID claims, reads, dependencies and step effects remain provider-derived and Runtime-checked. Retained media/documents are preserved in the candidate manifest.

The existing production `duplicate_timeline`/`_duplicate` caller now selects the exact source publication from normal source history and submits this command through the durable session outbox. A test runs that actual caller against the real Runtime service and confirms one `timeline.duplicate` command plus refusal cleanup. Structural restructure callers retain their prior path.

The inherited occurrence.attach WIP registration/helper/tests are deliberately **not retired in this bounded result**: both original positives remain red. Folding/removing that partial operation is still outstanding; this draft does not meet the requested final one-command retirement state. No inherited G5 deletions were expanded or reversed. On the eventual current port, keep/restore the old duplicate writer until BOTH original positives pass on the new command.

## Runtime source

Used actual staged authority source `36f24786942acd55af2395c1372dd4ac3d4c658a` from the existing local hub ref, extracted with read-only `git archive` to `/tmp/w-e475dee3e6/runtime-D17`. This is the worker's scratch directory (the assigned `tmpdir` marker contains `/tmp/w-e475dee3e6`; it is a marker file, not a directory). No fetch, checkout, shared install or integration-tree mutation occurred.

## Exact tests and results

All Agent commands ran in `/home/user/work/wt/agt-D17-source-copy-0851`.

Final D17 controls after all product edits:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-e475dee3e6/runtime-D17 ASTRID_RUNTIME_CHECKOUT=/tmp/w-e475dee3e6/runtime-D17 /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_runtime_source_copy.py tests/editing_conformance/test_recipe_timeline_source_copy.py
```

**24 passed in 33.39s**. Log: `/tmp/w-e475dee3e6/d17-final.log`. Real-port coverage: single-shot preview/no-write, exact destination undo/redo, durable receipt/idempotency, real production caller, cleanup, foreign/outside/same source, wrong publication/digest, archived source, forged media/create claims, invalid maps, and real project-wide occupied-shot rejection with an unchanged database. Recipe coverage: repeated sharing/order, full raw parent/child payload and opaque preservation, fresh item identities, manifest media/document retention, source/destination separation and strict claim refusal. Recipe authority fakes are explicitly separate from real-port proof.

Required positives plus focused/WIP controls (last execution of known failed bodies):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-e475dee3e6/runtime-D17 ASTRID_RUNTIME_CHECKOUT=/tmp/w-e475dee3e6/runtime-D17 /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_runtime_source_copy.py tests/editing_conformance/test_recipe_timeline_source_copy.py tests/editing_conformance/test_recipe_occurrence_attach.py tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared
```

**2 failed, 39 passed in 52.96s**. Log: `/tmp/w-e475dee3e6/final-targeted.log`. Original files/assertions were never changed. Chapter positive cannot obtain a source publication from its destination-only Generated transport. Repeated-shot positive reaches its unchanged assertion, but the old-base canonical reload exposes two per-occurrence authoring aliases instead of one physical shot. After this run only caller validation-order/helper extraction and additional controls changed; these known failed bodies were not repeatedly rerun. An earlier exact two-positive command also produced 2 failures before restoring the preserved attach registration.

Neighboring restructure suite:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-e475dee3e6/runtime-D17 ASTRID_RUNTIME_CHECKOUT=/tmp/w-e475dee3e6/runtime-D17 /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider tests/sdk/test_timeline_restructure.py -k 'not test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter and not test_duplicate_commit_keeps_a_repeated_shot_shared'
```

**35 passed, 2 deselected in 28.02s**. Log: `/tmp/w-e475dee3e6/restructure-neighbors.log`. The two known failures are the separately executed positives above, not skips or rewritten expectations.

Actual staged Runtime authority suite, working directory `/tmp/w-e475dee3e6/runtime-D17`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py
```

**8 passed in 19.18s**. Covers exact historical source, pair/digest, forged media, foreign/outside/archived source, revoked access, and source mutation after capture through the real private port. These are authority tests, not semantic completion credit.

A first real-port repeated-source setup failed at the inherited final timing guard: `shared shot requires canonical per-occurrence authoring materialization`. That run was 11 setup errors; the errors shared this cause. No guard was relaxed. Real-port single-shot tests and recipe sharing tests were then separated explicitly; full real-port repeated-copy proof is still missing.

## Checks

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-e475dee3e6/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-e475dee3e6/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Ruff **2148/2148**, no increase; scoped Ruff on all six changed files passes. Mypy **1904/1904**, no increase, including the final warm-cache rerun after the caller helper extraction. Vendor lock OK, artifacts current, diff clean. No baseline, skip, xfail or original assertion change. No full suite, localhost/socket/browser/journey, P1/P4 HTTP, native14 or crash24 duplicate run.

## Remaining limits / next owner

1. **Both original positives remain FAIL.** This is the hard gate; no integration or old-writer deletion is authorized by this report. Adapt the source-backed test boundary without weakening the original assertions, then qualify the new command on the correct current port.
2. Current-port join must preserve e49/G2 hydration, d462 mirrors, f7 R2/P4afc9 and later home changes. This worker did not touch those excluded paths or V2. The old-base timing adapter blocks real repeated materialization; recipe sharing is not a substitute.
3. Full retained-document/unreferenced-media undo and source-copy lost-ACK/restart/archive interaction are **unverified**. The existing `_duplicate` broad exception cleanup remains inherited and needs a source-copy unknown-outcome proof. Do not claim full authenticated-copy semantics from the single-shot proof.
4. A source with inherited non-default occurrence source maps reached the existing compiler refusal (`source_offset requires an internal clip source trim`) in a preliminary recipe probe. No fake compiler baseline or guard exception was added. The final raw-preservation recipe tests use supported source offsets; arbitrary inherited map copy is not qualified.
5. Multiple different revisions of the same physical source shot ID are explicitly refused rather than guessed; full closure support for that shape remains outstanding. Source text-binding/live projection semantics and richer parent-registry undo also need qualification.
6. Complete the source-copy semantic on current code, fold the partial attachment WIP into that one operation, obtain independent review and correct current-join/home proof, and only then consider P1/integration.

## Harness state

At 09:08:09 the harness wrote STOPPED as `orphan finalized by request: died in container restart (ensure-daemons)` and externally committed `a3dbf5fd8a27a59b2a182d71a4cb963bd141040e`. This worker session was still running. I made no git write. Current worktree therefore contains that captured WIP plus two later modified files: `astrid/sdk/timeline_duplicate.py` and `tests/editing_conformance/test_recipe_timeline_source_copy.py`. Preserve BOTH the harness commit and these remaining edits; do not assume a3db alone contains final controls/validation-order repair. Commit message is supplied separately for the harness. No DONE marker: BLOCKED accurately records unfinished acceptance.
