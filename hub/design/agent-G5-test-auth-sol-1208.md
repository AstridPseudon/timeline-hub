# G5 authenticated emitter test correction — 1208

Status: BLOCKED on approved wrapper update; bounded source correction and all authorized local checks complete. DRAFT, no integration merge until P1 GO.

## Scope and decision

Only `tests/editing_conformance/test_native_sheet_current_runtime.py` is changed (28 insertions, 11 deletions). `tests/timeline/test_authoring_feedback.py` is unchanged, retaining all 33 cases. Runtime collection retains all 19 cases. No product/provider/emitter/Runtime/helper/fixture/shared-dependency/schema/generated/pin/contract changes, Git mutations, daemon actions, or direct HTTP bodies.

Read PLAN §3 G5/G3, C0 §§1–5, independent 1143 FAIL, independent 1155 SOURCE PASS, and 1201 actual-service failure evidence before editing. No evidence establishes a product defect.

Independently confirmed the production boundary:
- `astrid/sdk/timeline/commit_session.py:54–66`: `Timeline._execution_bundle()` calls `fetch_bundle()` with its exact revision/publication pair before child emission; `_capture_free_edits()` supplies this canonical context.
- `astrid/sdk/timeline/sync.py:202–219`: session `_bundle()` uses the exact base publication as well as revision.
- `astrid/sdk/timeline/store.py:641–654`: `fetch_bundle()` delegates to public `client.timelines.open_bundle()` with both pins.
- `astrid/sdk/_remote_timeline.py:169–208`: this read checks the original history publication/receipt/revision, verifies the canonical image, compares the entire public closure and dependency manifest, and returns authenticated canonical context. The default public read intentionally omits that context.

The test now reads both public and exact-pair bundles, checks scope/revision/head, exact seed canonical document equality and digest, projects that authenticated document with `bundle_from_document()`, and compares the complete public bundle plus exact hydrated bundle. This supplies the existing pure emitter boundary without injecting a private cache into the public bundle. The old expected-result manual private-image assignment is removed because execution now starts with the authenticated canonical bundle.

All original malformed-parameter wire/provider code, path, hint, command, no-write/head/history assertions remain. The accepted patch sequence, null/removal behavior, track label, canonical result equality, complete command records, opaque fields, physical shared-source/sibling isolation, reload, undo and redo assertions remain. An AST comparison shows 43 original vs 52 resulting distinct assertions: only two original assertions are replaced, by stronger full head-pair and exact canonical/public-closure comparisons. No assertions weakened to subset equality, no skip/xfail, fixture substitution, or success-to-refusal change.

## Source identities and origins

- Worktree: `/home/user/work/wt/agt-G5-test-auth-sol-1208`
- Base/HEAD: `tl/agt-G5-test-imports-return-1147`, `b4a5b3b7ef524049e569c9694aa730b9368f8ad0` (HEAD remains unchanged; harness owns commits).
- Original Agent tree: `0f15546b263450058f6d4a26ce0ad7ff901ed57d`.
- Corrected uncommitted Agent tree: `3ed568fbd57a7732712bdd3558edc6f5ba008282` (calculated from index entries and corrected blob without writing Git objects/index).
- Corrected test SHA-256: `28ca8b12f2ca21c84d74c6601ae3887fc4873e90ffa1f35c20a56177272df72e`.
- Runtime checkout: `/home/user/work/wt/rt-pin-3b926efa`, HEAD `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`; clean before local checks.
- Normal producer: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Frozen edit-command schema SHA-256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Client SCHEMA_DIGEST remains the separate normal-producer value `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
- Frozen Composition SHA-256 remains `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Local origin check: Agent `/home/user/work/wt/agt-G5-test-auth-sol-1208/astrid/__init__.py`; client same worktree `/astrid_runtime_client/__init__.py`; Runtime `/home/user/work/wt/rt-pin-3b926efa/runtime_protocol/__init__.py`.

## Exact local verification

Working directory `/home/user/work/wt/agt-G5-test-auth-sol-1208`. Common environment for pytest:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa
export TMPDIR=/tmp/w-e2c00da235
P=/home/user/work/venv-agent/bin/python
$P -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-e2c00da235/authoring tests/timeline/test_authoring_feedback.py
# 33 passed in 2.86s
$P -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-e2c00da235/emitter tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_native_sheet_ordinary.py tests/sdk/test_timeline_sheet_native.py
# 135 passed in 16.96s
$P -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
# 52 tests collected in 2.89s: 33 + 19
/home/user/work/venv-agent/bin/ruff check --no-cache tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
# All checks passed!
$P -m mypy --cache-dir=/tmp/w-e2c00da235/mypy tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
# Success: no issues found in 2 source files
git diff --check b4a5b3b7e
# exit 0
```

Logs: `/tmp/w-e2c00da235/{authoring,emitter,collection,mypy}.log`. First local invocations incorrectly used `$ORCH/workers/agt-G5-test-auth-sol-1208/tmpdir` as a directory; it is a pre-existing pointer file containing `/tmp/w-e2c00da235`. Those attempts produced 33/135 setup errors (`NotADirectoryError`) before test bodies. Reading the pointer and rerunning with its private directory resolved the invocation error; no source changes between attempts. No safety denial occurred.

## Prior service evidence (not this corrected tree)

Only `agt-G5-test-runtime-witness-1201-g5-emitter-current-runtime-nodes-1023120356-29910` executed a real body: FAIL, `1 failed in 4.07s`, original Agent tree `0f15546…`, exact Runtime `3b926efa…`. Its setup/genesis/restart and authenticated voiceover source succeeded; line 284 failed on missing `_runtime_document` during the first direct emitter call. The before/session-start/session-finish/after origins were the central synthetic Agent snapshot and exact Runtime checkout. Full trace: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-G5-test-runtime-witness-1201-g5-emitter-current-runtime-nodes-1023120356-29910/log.txt`.

1201 `1023120116-22440` was a runner preflight failure (client vs frozen schema digest confused); `1023120217-7687` reused that preflight failure from cache. Neither ran a test body. Independent 1155's previous service deselected all 19 Runtime tests and is not execution evidence.

## Central execution blocker / next step

The existing approved named suite `g5-emitter-current-runtime-nodes` invokes `$ORCH/workers/agt-G5-test-runtime-witness-1201/run-g5-emitter-current-runtime-nodes.sh`. It requires both `HEAD^ == b4a5b3b7e…` and `HEAD^{tree} == 0f15546…`, so any meaningful correction is rejected before executing pytest. This task forbids unreviewed changes to that wrapper. An asynchronous request to the orchestrator asks its ops owner to approve/update ONLY the Agent tree check to `3ed568fbd57a7732712bdd3558edc6f5ba008282`, retaining the base-parent, Runtime commit/tree, exact node, pins, and all four origin checks. No wrapper or suite change has been made by this worker, and no knowingly ineffective central request has been submitted. The approval request has received no response; central execution remains blocked. No DONE marker is created.

After the approved wrapper update, run exactly once:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$($O/bin/request-test agt-G5-test-auth-sol-1208 g5-emitter-current-runtime-nodes --files tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated)
$O/bin/wait-test "$R"
```

The edited tree creates a new cache key, so `--no-cache` is unnecessary. Do not request all 19 cases, another native/P1–P4 lane, full/browser suites, or a direct localhost body. If that body exposes another failure, stop and classify it. This draft is not Runtime-qualified and cannot merge/integrate until independent review and P1 GO.
