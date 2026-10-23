# G2/R2 public undo v2 — complete

Worktree: `/home/user/work/wt/agt-G2-undo-v2-1113`, base Agent `abfa78a657b4ce1cc625104e8472fb29938e3d64`. Actual Runtime `/home/user/work/runtime`, `49ce53289bc37d9387a7d9e6b9c9b16072162181`, clean before and after. Read PLAN and the D17 current-auth diagnosis first; retained C0 request/undo semantics.

## Change and decisions

Only production change: `astrid/sdk/timeline/sync.py`, `TimelineSession.undo`. Use the existing `_flush(prepare=...)` transaction to stage the inverse and freeze its existing `commit_options` representation together. New intent gets label `Undo timeline edit`, merge `fields`, and one stable step `inverse` with ordinal `[0]`, empty submitted native patch, intent and tags. The real provider generates the full accepted patch, dependencies and effect bindings. No caller reads are invented; request/step `reads` remain omitted, while actual inverse/history reads survive.

Existing flights receive no new options, body or key. Existing matching pending metadata is preserved; other pending commands refuse before writing. Whole/default and selected-step arguments, dry-run, source/via, exact base pair, error envelopes, acknowledgement checking and persisted retry processing retain their existing paths. No facade, provider, inverse engine, Runtime, contract, generated client, pin or fixture changes. No new public signature, transport or executor.

Added five SDK cases for whole/selected wire metadata, lost ACK/reopen/exact frozen replay, changed key/dry-run rejection, pending-intent preservation, preview/fresh-key/base guards, and legacy flight replay without metadata insertion. The legacy case models a previously persisted flight at the fake generated-client boundary; it makes no real Runtime/provider claim.

Added two parameterized real Runtime nodes in the existing provider-runtime integration file. Public timeline birth uses `RuntimeService.create_timeline`; native track birth uses the approved `capture_track_create` helper through `timeline.open().command().commit()`. Two public `track.set` commands then commit as separate steps. Ordinary public whole or selected-step `undo`, preview, exact replay and public undo-of-undo reach real Runtime/provider/store validation through the existing generated-method boundary seam. No socket, HTTP, daemon, renderer or D17 copy case is involved.

The first regression draft used raw track creation without the required created-ID capture; Runtime correctly rejected it (`provider executed a different command`, 2 failures). Replaced this test setup with the existing public capture helper rather than changing Runtime/auth or adding claims manually. An initial SDK test launch also failed importing Runtime because PYTHONPATH lacked the checkout; corrected the launch environment. Neither failed invocation is counted as qualification.

## Exact final checks

All commands below ran from the assigned worktree. Environment prefixes are literal values used, not instructions to modify shared dependencies.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-2b3ab2f86e PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-2b3ab2f86e/pytest-sdk-final tests/sdk/test_timeline_sync_native.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_open_commit.py tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_p4_commit_v2.py tests/test_vendor_lock.py tests/test_artifact_manifest.py tests/sdk/test_timeline_commit_provider_runtime.py
```

**Exit 0: 185 passed, 4 deselected in 23.82s.** Default integration policy deselects both new real Runtime nodes and the file's two pre-existing integration tests. This is not four passes; no skips/xfails were added. The two new nodes were explicitly executed separately:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-2b3ab2f86e PYTHONPATH=.:/home/user/work/runtime:/tmp/w-2b3ab2f86e ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -p g2_observer --timeout=45 --basetemp=/tmp/w-2b3ab2f86e/pytest-public-runtime-final 'tests/sdk/test_timeline_commit_provider_runtime.py::test_public_undo_redo_persists_v2_effect_bindings'
```

**Exit 0: 2 passed in 8.33s.** The same real nodes passed without the read-only observer before the final assertion strengthening (2 passed in 4.77s). Observer uses trace callbacks only; it does not wrap the provider/store, edit requests or substitute history.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-2b3ab2f86e PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/sync.py tests/sdk/test_timeline_sync_native.py tests/sdk/test_timeline_commit_provider_runtime.py
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-2b3ab2f86e PYTHONPATH=.:/home/user/work/runtime make PY=/home/user/work/venv-agent/bin/python ruff
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-2b3ab2f86e MYPY_CACHE_DIR=/tmp/w-2b3ab2f86e/mypy-cache PYTHONPATH=.:/home/user/work/runtime make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy
git diff --check
```

All exit 0. Scoped Ruff: all checks passed. Repository Ruff: **2149 current / 2149 baseline**. Mypy: **1912 current / 1912 baseline**. Vendor-lock and artifact-manifest tests are included in the 185-pass run. No full suite, central full request, shared-dependency mutation, Git write, browser, native14/original58, all4 copy rerun or new qualification tuple.

## Actual evidence and limits

Full real wires, keys, original data/receipt envelopes, canonical documents, history records (commands, dependencies, effects/step patches and undo selectors), and loaded source origins/hashes:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G2-undo-v2-1113.json`

Read-only observer retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G2-undo-v2-1113/g2_observer.py`

Capture: 414599 bytes, 102 loaded Agent/Runtime module origins. Independently checked every captured Runtime module path originates in `/home/user/work/runtime/`. Each case has six observed calls (track birth, label commit, inverse preview, inverse accept, exact inverse replay, redo) and five history entries including bootstrap. Whole undo and redo each persist 2 patch effects, 4 dependencies, 4 native reads and 4 effect bindings. Selected undo and redo each persist 1 effect, 2 dependencies, 2 reads and 2 effect bindings. Every effect has both before/after bindings. Stored `undo_steps` selects exactly the original `step-1`. Original selected native read addresses are retained as a subset of inverse read addresses. Redo restores the entire forward canonical document; whole undo restores the entire pre-label document, while selected undo leaves the other label intact.

Request base pair/commands/label/step identity/ordinals/patch/merge/source/dry-run and real idempotency key are retained verbatim. Request and step `reads`, rationale and group_id are absent in these actual ordinary public calls, not fabricated. Preview has `would_status=accepted` and no receipt. Accepted receipts retain their full original `result`. No new merged/historical-rebased/conflict/invalid real Runtime scenario is claimed; existing SDK session/facade guards cover their unchanged handling, including error code/path/hint/suggested-command propagation. New tests do not claim D17 copy undo is repaired.

No blocker. Recommended next step: review and integrate this bounded Agent fix; Runtime native-representation repair remains separately owned by 1105. Orchestrator should authorize any later combined D17 qualification after both changes are integrated. This report does not retire P1/G5 holds or replace the prior current-tuple finding.
