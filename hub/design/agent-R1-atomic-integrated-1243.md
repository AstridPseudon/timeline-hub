# PASS — R1 atomic scope actual-integrated proof

## Target and exact-tree identity

The actual integrated Agent target is `5b1b4db8253f46e0e085908e79f309d492877386`,
tree `f641867d6fe7b13b07211158574c8219c7cee8ae`. The worktree was clean before
and after qualification. The reviewed R1 commit
`dcb4cee32285712f0639063f9efb96f810b357d7` has the identical tree, so its
independent review and exact-tree quality evidence are reused; no new review or
repeat of the 211 impacted tests is claimed.

The pinned Runtime was `/home/user/work/wt/rt-pin-3b926efa`, commit
`3b926efab2eed122d374540baee297d4cdcec62a`, tree
`b794170504544b259781e50d7ca4d61b6729e67c`, also clean before and after.

The only integration delta from the pre-fix Agent base `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`
is the two reviewed blobs:

```text
M  astrid/sdk/timeline/_commit_patch.py
A  tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
```

The production caller `astrid/packs/rendering/docs/scripts/timeline_document.py`
is byte-identical to the pre-fix base. Its existing `check`/`publish` route still
uses the complete-JSON path, `TimelineSession.commit_many`, `via="script"`,
label `Publish document`, and atomic merge.

## Actual focused proof

Command, run from the actual integrated Agent worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
```

Result: **3 passed in 8.22s**.

The three real in-process Runtime cases prove:

1. The production complete-JSON script `check` then `publish` path accepts an
   atomic request with the exact base revision/publication pair, commands,
   label, step patch and ordinal, conservative absent request reads, source,
   accepted data/receipt, canonical readback, records/dependencies, exact
   physical captures (`parent`, `shot-revision:shot-film`,
   `internal-revision:internal-film`), history, and idempotent replay. The
   actual landed document contains both the parent and child changes.
2. A native occurrence removal followed by a parent patch accepts through the
   real service and captures the surviving roots at every step while preserving
   untouched physical images.
3. Sequential atomic JSON steps preserve per-step input boundaries and digests,
   step reads, source/rationale/group ID, dry-run no-write behavior with
   `receipt: null` and `would_status: accepted`, accepted canonical data,
   records/dependencies, and idempotent replay.

The reviewed exact-tree impacted evidence remains applicable for the complete v2
surface: base pair, commands, label, steps with patches/reads/ordinals, merge
mode, request reads, idempotency key, dry-run, source/rationale/group ID,
accepted/merged/full canonical data and receipts, records/dependencies/effects,
history/undo steps, preview/required `would_status`, and structured
conflict/invalid code/path/hint/suggested-command behavior. This report does not
claim a new 211-test run.

## Provenance and integrity

Current source hashes:

```text
0683faf0b33bbc38938011819e1f9603c044bbdb4da41c325254c76d744a9c92  astrid/sdk/timeline/_commit_patch.py
c4e95a4cdc74fe8de9b151c818492f6a2fd4301c699a43bc686611bcbdeff5a4  tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
46304396494dc22897f17d2d0f8e7609ec8241a610d23c957ed21fe083b12844  astrid/packs/rendering/docs/scripts/timeline_document.py
a8a0b00025f99ace48e0fee989fe3e11c948c3f1e2fa47a33621791e91252756  Runtime runtime_protocol/timeline_commit_auth.py
267bec1aee551e7ea1f92f987adb24268be11c6dd165ee56f24aa68ff2b6a692  Runtime runtime_protocol/service.py
```

The import-origin/hash check loaded the production Agent Timeline modules from
the actual Agent worktree and all `runtime_protocol*` modules from the pinned
Runtime checkout; no selected module resolved outside those two roots.

The exact reviewed quality evidence is reused, not re-run or presented as new:
Ruff `2149/2149` and mypy `1912/1912`. The current checks were run directly:

```text
artifacts.json is current
ok runtime.lock.json (matches producer manifest)
git diff --check: PASS
git diff --no-index --check /dev/null tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py: PASS
```

No product/test edits were made by this proof worker. No schema, generated
client, contract, dependency, vendor pin, Runtime guard, authority, receipt,
or test-expectation changes were made. No full suite, P1/P4 journey, HTTP,
native-14/original-58, D17 duplicate, daemon, Git mutation, or shared-install
operation was performed.

## Decision / next step

**PASS.** The actual integrated tree is independently reviewed and the focused
atomic materialization proof passes against the requested pinned Runtime. The
orchestrator may use this as the R1/C0 §1/2/3 qualification receipt. Continue
with the already-settled plan gates; this proof does not clear unrelated G5 or
P1/P4 requirements.
