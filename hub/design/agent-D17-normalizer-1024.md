# D17/R1 normalizer 1024 — scoped result passes

The requested raw-parent and repeated-physical-root repair passes against unchanged real Runtime **1365e4b17b31c4a7093d5943674637067fd2bab4** (tree `6c69c3dc47822fffbaf27cd63815d2895155ffaa`). The retained-only media/document whole undo/redo positive also passes. This is a scoped semantic result, not full project or G5 qualification. Runtime authority was not changed.

## Delivered

- `Recording.assign` refreshes its existing mirror flag when the whole parent config is replaced. A copied raw parent with no `config.clips` stays that way; it no longer inherits the empty destination's mirror topology.
- `effect_diff` retains its normal alias effects when topology is stable. When either clips/registry storage presence changes, it emits the existing provider-only complete parent effect with the raw before/value images. Authenticated physical bindings and Runtime projection therefore see the same exact bytes. This avoids pretending a config alias can encode removal of a raw mirror.
- The existing root-inverse helper rejoins only unchanged working aliases of a selected physical aggregate, using exact authenticated source links and payload images. Changed alias payload/internal content refuses. The original aggregate and leaf guards, later-history scans, source links, stage execution, and physical sharing remain active. Historical inverse read reconstruction uses the same normalization. The existing validation adapter also handles shared roots restored by redo.
- Complete accepted root commands that actually read the closure scope reverse their retained-input deltas through the existing `_copy_manifest` path. The helper requires complete selected accepted command records and exact loaded boundaries, and leaves ordinary root creation inverses on their existing path. Hydration verifies restored media and document inputs without prematurely adding redo pins to the input image. Surviving media/document consumers refuse. There is no new request field, journal, authority path, receipt format, or cached source.
- Fixed the four prior Ruff findings in `test_timeline_restructure.py`: fixture re-export/import ordering, and the local import separation. The two original duplicate test bodies and their complete assertions are unchanged; `original-node-preservation.json` records exact AST equality against HEAD for both functions.
- New/expanded regressions cover four raw parent mirror-presence combinations, repeated shared roots both empty and carrying actual ingested media/content, retained-only inputs through copy/undo/redo, archive after capture, forged physical media, changed/ABA leaf writes, and actual destination archive after definitive refusal. Existing unknown-outcome/lost-ACK behavior remains covered unchanged.

No contract, generated files, Runtime lock, Runtime authority, client, Composition, V2, G5 retirement, P4, dependencies or quality budgets were edited. The assigned tree started at `f209b04551e7272e33117996bd8e2624e2808b93`; ef851 is its ancestor. Only the eight scoped files listed in `change.patch` were modified. No Git writes, installs, daemons, pushes, skips or xfails were used.

## Required evidence and inventory

Final source-copy selection: **40 passed**. It contains exactly the two original restructure duplicate nodes, the source-copy real-port file and its pure semantic neighbor. Both original nodes retain every assertion. Final inverse neighbor selection: **281 passed**. All tests use a 45-second per-test bound and no cache provider. The real-port tests run RuntimeService/store/provider in-process, with no HTTP or live sockets.

| Requirement | Evidence |
| --- | --- |
| Original chapter identities/order/distinct roots, repeated physical sharing/raw edges | Both exact original duplicate nodes pass; no assertion changed |
| Raw parent config presence and raw mirror topology | Four presence variants pass with exact parent payload equality excluding remapped occurrences |
| Repeated source-copy whole undo/redo | Both variants pass, including nonempty raw shot items, child clip, opaque data and actually ingested media; exact replay receipt, empty undo closure, exact redo document and unchanged source |
| Retained-only inputs | Real registered config document and real unused ingested media survive copying; whole undo equals the entire original empty destination document; redo equals the entire copied document |
| Source pair/digest/project/outside/same-source/archived/created/media/sharing/order | Existing real-port negatives pass, with complete SQL-dump equality; pure malformed-map/caller-source negatives pass |
| Captured stale authority | Archive **after** actual source capture refuses and preserves the complete post-archive SQL dump; this does not claim that advancing an immutable historical source head is invalid |
| Physical media forgery | A port-returned manifest corrupted with a real media object outside the captured source is refused by the unchanged port; complete SQL dump unchanged |
| Occupied IDs | Local-source identity and project-wide occupied-shot negatives pass |
| Idempotency | Original and repeated exact retries preserve the original receipt/document; no extra accepted publication |
| Lost ACK / restart | Both disconnect-before-acceptance and disconnect-after-acceptance retain the destination and public-open restart flush retries the exact durable body/key |
| Archive cleanup | Existing production wrapper refusal control passes; added real archive checks the actual archived catalog resource and unchanged empty destination head. A digest-corrupting sender induces the definitive Runtime refusal; this is cleanup evidence, not a valid request acceptance |
| Aggregate/leaf guards, ABA, forgery, surviving consumers, sequential stages | 281 neighboring tests pass, including the existing step, stage, mirror and grouped-cache guards; new real-copy leaf/ABA negatives leave full SQL dump unchanged |
| v2 requests, replies and recorded effects | Full actual contexts and returned envelopes are retained in `source-copy-wire.json`, including accepted/preview, labels/steps/dependencies/records/effects and failures. Request/reply/history shapes were preserved; historical `rebased` compatibility is not newly qualified here |

`origins-before.json` and `origins-after.json` record loaded Agent/Runtime module paths and SHA-256s. Both identify the exact Runtime HEAD above and an empty Runtime Git status (29 then 38 loaded Runtime modules). Agent modules resolve to this assigned worktree. `capture-evidence.py` only wraps the provider call to record its actual context/result or failure; it injects no source, authority, or recorder data. `source-copy-wire.json` contains full successful candidate/reply JSON and failure details. All evidence is in this stable adjacent artifact directory, not an expiring temp path.

## Exact final commands

Working directory: `/home/user/work/wt/agt-D17-normalizer-1024`.
Common environment for the saved commands:

```sh
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1:/tmp/w-e409539a14
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1
```

The two scratch Python helpers used for logging and origin capture are copied into the stable artifact directory as `run-checks.py` and `capture-evidence.py`. Each `.command.json` records argv, working directory, common environment and actual exit code. Scratch basetemp paths are not evidence destinations.


### source-copy

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -p evidence --timeout=45 --basetemp=/tmp/w-e409539a14/pytest-final4 tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared tests/editing_conformance/test_commit_runtime_source_copy.py tests/editing_conformance/test_recipe_timeline_source_copy.py
```

Actual exit: `0`. Log: `source-copy.log`.

### inverse-neighbors

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-e409539a14/pytest-inverse-final2 tests/editing_conformance/test_doc_patch_mirrors.py tests/editing_conformance/test_inverse_clip_mirrors.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_grouped_clip_cache_inverse.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_recording_clear.py
```

Actual exit: `0`. Log: `inverse-neighbors.log`.

### quality-ruff

```sh
/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```

Actual exit: `0`. Log: `quality-ruff.log`.

```text
Ruff findings: current=2149 baseline=2149
```

### quality-mypy

```sh
timeout 180 /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

Actual exit: `0`. Log: `quality-mypy.log`.

```text
Mypy findings: current=1912 baseline=1912
```

### changed-lint

```sh
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_commit_runtime_source_copy.py tests/sdk/test_timeline_restructure.py
```

Actual exit: `0`. Log: `changed-lint.log`.

```text
All checks passed!
```

### vendor

```sh
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
```

Actual exit: `0`. Log: `vendor.log`.

```text
ok runtime.lock.json
```

### artifacts

```sh
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
```

Actual exit: `0`. Log: `artifacts.log`.

```text
artifacts.json is current
```

### legacy-shared-current

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-e409539a14/pytest-legacy-final tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_slot_move_inverse_redo_and_rematerialization
```

Actual exit: `1`. Log: `legacy-shared-current.log`.

Quality commands use `RUFF_CACHE_DIR=/tmp/w-e409539a14/ruff-final` and `MYPY_CACHE_DIR=/tmp/w-e409539a14/mypy` respectively. The shared venvs were read-only. Vendor lock and artifact checks pass. Both `git diff --check` and `git diff ef851 --check` pass. No quality budget was rewritten.

## Earlier diagnostics, limits and next action

The first targeted post-mirror repair run passed raw parent fidelity but failed repeated undo because `shot:copy-film` was absent under the reopened per-occurrence aliases. After root normalization undo passed and redo exposed historical inverse read reconstruction, then timing validation of restored shared roots. Each cause was fixed in the existing paths, with no guard relaxation. Retained-only undo initially failed `unproven media boundary scope`; its positive now passes both directions. The broad inverse-neighbor run caught two introduced regressions in ordinary creation inverses, caused by treating every rooted inverse as a copy manifest reversal. Requiring the actual closure read and a real runtime document restored those original passing behaviors; the final entire 281-test selection is green. No failure was skipped or encoded as missing behavior.

An exploratory neighbor selection returned **10 failed, 77 passed**: all ten failures in the historical `test_commit_runtime_shared_inverse.py` file occurred on its first 3.5-second move, before inverse, with `timeline interval must fit the occurrence's half-open bounds`. A final bounded rerun of the representative original node has **2 failed** (both fixture variants), and a private overlay loaded from `git show HEAD:<path>` reproduces the same **2 failed** at the original baseline line 1133. `legacy-shared-baseline.log` identifies the baseline module origin; `legacy-shared-current.log` retains current failures. The initial overlay attempt did not preload modules before pytest changed sys.path, so it was not accepted as baseline proof; the saved baseline log is from the corrected preloaded run. The other eight exploratory failures were not separately baseline-replayed. They are reported, not waived or changed. The baseline helper and exact saved command are described below.

No full, original58, native14, HTTP, browser, P1 or P4 suite was requested or run. Historical `rebased`, arbitrary mixed inverse-plus-new-schema batches, process-kill recovery, and archive-operation failure are not newly qualified by this slice. The archive-after-capture refusal can surface as an unresolved SDK outcome through the production wrapper; the existing conservative retention behavior is preserved. Runtime's independent grouped-inverse/authority work is not duplicated.

Recommended next action: independently review and integrate this D17/R1 source-backed normalizer repair, then investigate the separate legacy shared-slot timing baseline in its owning lane. Keep the project/G5 gate under orchestrator control; these passing scoped results do not authorize writer deletion or a whole-project green statement. No task blocker remains for the delivered raw-parent/repeated-root/retained-input slice.

## Baseline replay

`baseline-overlay.py` constructs a private package overlay: changed product Python files come from `git show HEAD:<path>`, with unmodified package entries symlinked read-only to this worktree. It does not change any Git ref, shared install, or product file. The corrected process preloads baseline modules before pytest's conftest can add the assigned root to sys.path:

```sh
cd /tmp/w-e409539a14/baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-e409539a14/baseline:/home/user/work/wt/agt-D17-normalizer-1024:/home/user/work/wt/rt-pin-1365e4b1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1 /home/user/work/venv-agent/bin/python -c 'import astrid.sdk.timeline.commit as c; import astrid.sdk.timeline.commands, astrid.sdk.timeline.inverse, astrid.sdk.timeline._root_inverse; print(c.__file__); import pytest; raise SystemExit(pytest.main(["-q", "--tb=short", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=45", "--basetemp=/tmp/w-e409539a14/pytest-baseline2", "/home/user/work/wt/agt-D17-normalizer-1024/tests/editing_conformance/test_commit_runtime_shared_inverse.py::test_shared_slot_move_inverse_redo_and_rematerialization"]))'
```

Actual result: **2 failed in 3.04s**, same first-edit timing bound failure as current, with module origin `/tmp/w-e409539a14/baseline/astrid/sdk/timeline/commit.py`. No missing prior-worker artifact is used as proof.

The initial exploratory neighbor command (actual **10 failed, 77 passed in 27.19s**) was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1 /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-e409539a14/pytest-neighbors tests/editing_conformance/test_doc_patch_mirrors.py tests/editing_conformance/test_inverse_clip_mirrors.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_commit_runtime_shared_inverse.py tests/editing_conformance/test_recipe_timeline_source_copy.py tests/editing_conformance/test_commit_runtime_source_copy.py
```

Its complete output is in the tool transcript; the stable current and baseline representative logs reproduce the failure independently. It was not a full suite or the original58 qualification.
