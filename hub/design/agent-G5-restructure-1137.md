# G5 restructure migration — agt-G5-restructure-1137

**DRAFT ONLY. Targeted checks pass; no integration merge requested before P1 GO.**

Base: `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`.
Worktree: `/home/user/work/wt/agt-G5-restructure-1137`.

## Change

The existing production `cli_working._cmd_restructure -> Checkout.publish(restructure=True)` now sends authored payload changes through the existing G3 emitter and the cut through the normal durable `TimelineSession.submit -> Runtime -> Python provider` path. It no longer calls `store.publish_bundle` for restructure. The ordinary legacy publisher body remains for final G5 retirement, as authorized.

Added the narrow registered `timeline.restructure` Python handler. Its arguments are empty: it derives the cut exclusively from the provider's authenticated current closure, applies the existing film-length helper and split/equivalence logic, and records native root allocations/writes. There is no caller-supplied source image, managed-edge patch, generic staging replacement, second executor, or duplicate reuse.

A retained chapter can reuse the source shot and occurrence. Removing/reinserting that occurrence incorrectly trips existing reservation guards. The existing Python State carrier now records an order write at the existing parent occurrences path, permitting only a permutation of complete unchanged rows. It rejects membership/content changes, including false versus zero. This is 13 lines in the provider carrier; the native handler supplies the order through the existing recorder. No wire/schema/tuple was added.

The durable outbox owns retries of the original cut body/key. Runtime history supplies the original cut receipt during narration reconciliation. Narration is reconciled even when the reopened head already contains its accepted binding after a lost ACK. A retry also recovers the current accepted cut after narration ingestion failed before a flight existed. Transcript creation remains idempotent and independently contained.

Core validation runs against a copy for restructure: its existing empty-slot accessor must not add absent fields to the authored cut. Exact complete raw-bundle comparisons verify this preservation.

## Restored behavior and controls

Restored all three named cases as successful current production-path tests:

- `test_cli_restructure_commits_the_complete_equivalent_bundle_and_followups`
- `test_restructure_reconciles_narration_without_republishing_the_cut`
- `test_restructure_retries_the_original_commit_after_lost_ack`

The first compares the entire raw parent payload, shot revisions, internal revisions and dependency manifest with the existing compiler's expected split. It checks renderer-input equivalence, placement/shot/occurrence identities, order, shared media, explicit null/false/zero and absence, exact base pair, atomic merge, narration command and transcript follow-up. Retry tests reopen the checkout, compare exact original request/key and replayed response, retain the original cut receipt, and require one transcript creation.

New real-provider controls reject foreign scope, changed before-state, created-ID order/identity claims, caller media claims, project-wide occupied shot IDs, and a stale closure. Every refusal checks the complete document, history and SQLite dump remain unchanged. Additional successes cover retained source IDs/order, narration failure before staging, and read-only preview with would_status.

The new fixture creates its source using normal Runtime creation, managed generation settlement/selection, native media/occurrence/track commands, and the public emitter/provider path. It uses no trusted seed, synthetic journal, prepared acceptance, source-authority substitute or renderer preflight. It asserts the Runtime module origin in the same process.

## Exact validation

All pytest invocations used this prefix, from the assigned worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=.:/tmp/w-ce7c2e1ed2/runtime-3b926ef \
ASTRID_RUNTIME_CHECKOUT=/tmp/w-ce7c2e1ed2/runtime-3b926ef \
PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest
```

Pinned Runtime was archived once, without changing any checkout:

```sh
mkdir -p /tmp/w-ce7c2e1ed2/runtime-3b926ef
git -C /home/user/work/runtime archive 3b926efab2eed122d374540baee297d4cdcec62a | tar -x -C /tmp/w-ce7c2e1ed2/runtime-3b926ef
```

Final targeted selection (append to the prefix above):

```sh
-q --tb=short -o addopts= -p no:cacheprovider \
--basetemp=/tmp/w-ce7c2e1ed2/final \
tests/sdk/test_timeline_restructure.py \
tests/sdk/test_timeline_narration_commit.py \
tests/sdk/test_scene_save_core.py \
tests/editing_conformance/test_document_patch_emitter_engine.py \
tests/editing_conformance/test_document_patch_emitter_v2.py \
tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones \
tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits \
-k 'not duplicate'
```

**109 passed, 5 deselected in 100.53s.** Log: `/tmp/w-ce7c2e1ed2/final.log`.

The last isolated carrier hardening changed Python row equality to canonical JSON equality and added the false-versus-zero refusal assertion. It was checked separately using the same pytest prefix:

```sh
-q --tb=short -o addopts= -p no:cacheprovider \
--basetemp=/tmp/w-ce7c2e1ed2/order-final \
tests/sdk/test_timeline_restructure.py::test_restructure_order_carrier_only_permutes_unchanged_rows
```

**1 passed in 0.92s.** No further product changes followed.

Earlier bounded probes exposed step patch grouping, implicit validation mutation, bootstrap registration order, missing fixture media authority and retained occurrence reservation collisions; these were corrected without weakening expectations or guards. An earlier 59-case selection passed before the additional retained-ID/preview controls. One unfiltered selection was interrupted after 19 cases to exclude duplicate cases; no duplicate qualification is claimed. No full, browser, socket, P1, P4 HTTP, native14, original58 or D17 duplicate suite was requested/run.

Quality commands:

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-ce7c2e1ed2/ruff-final2 make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-ce7c2e1ed2/ruff-final2 /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/native_restructure.py astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/commands.py
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-ce7c2e1ed2/mypy-final make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

**Normal Ruff 2149/2149 PASS; scoped Ruff PASS; private mypy 1912/1912 PASS; vendor lock PASS; artifact manifest PASS; diff check PASS.** No baseline/budget or dependency install changed. Mypy log: `/tmp/w-ce7c2e1ed2/mypy-last.log`.

Same-process source origins were also printed in `/tmp/w-ce7c2e1ed2/origins.json`: commands/provider resolve to this assigned worktree; Runtime resolves to `/tmp/w-ce7c2e1ed2/runtime-3b926ef/runtime_protocol/service.py`. The fixture independently asserts the Runtime package origin.

## Preservation, limits and next steps

Only `publish.py`, `commands.py`, `_command_state.py`, the new `native_restructure.py`, and the allowed restructure test file changed. Production CLI code needs no change because its existing publisher call now reaches the migrated branch.

Byte-for-byte preservation was checked with `git diff --exit-code HEAD --` over CLI, checkout/store, sync/commit_session, D17 provider/caller, commit.py, document_diff.py, schemas, generated clients, Runtime pin and artifacts. D17 remains intact. Full v2 request/result definitions and transport remain untouched: base pair, commands, label, step patches/reads/ordinals, merge/reads, key, dry_run/source/rationale/group_id; accepted/merged data+receipt, canonical closure, records/dependencies/effects/steps/history/undo_steps, preview would_status, conflict head/reason and invalid code/path/hint/command.

Schema SHA-256 remains `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`; Composition archive remains `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

No source-authority guard was waived. Generic detached membership/placement edits still require an appropriate semantic command; restructure derives its managed shape from the exact current closure and existing length helper. Broad undo/redo, renderer delivery, network and integration proofs are unverified here. Local-save merger retirement and final publisher deletion remain outside this task.

No merge, commit, rebase, checkout, push, daemon, shared dependency/cache write, skip/xfail or safety denial occurred. Recommend independent review of the narrow order carrier and caller recovery path, then integration qualification only after P1 GO.

