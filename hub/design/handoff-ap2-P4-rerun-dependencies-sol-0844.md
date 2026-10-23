# P4 command captures versus step dependencies — PASS (offline/source)

Classification: **legitimate one-file oracle correction**, not an observed product defect. Original service actual21332 returned 200/409/200 and passed canonical-document, full command-record and full authoritative-step equality before failing line 313's command dependency nonemptiness. No live behavioral PASS is claimed here.

## Exact identity

- Base/final pre-harness HEAD SHA: `2abeea693e95108fab811bdbe41ddac4fe0da6ac`.
- Base tree: `d45fe198104553c45b88c5fa80e547f9bfa25714`.
- Base target blob: `53a8ad9143e7464c0dc606c61f1e3339205bee32`.
- Candidate target blob: `192efbfa14607f0edfb362d47d5238645c64e984`.
- Candidate target SHA256: `02ffa65700ff1c4d2e4a017fbaef6f646d100de5af61bc85e9003866eb927f36`.
- Prospective candidate tree, calculated without writing Git objects: `52a203caa936a286e7b65d26668680c1e22153f3`.
- Candidate commit SHA is pending the harness commit; no commit/index/ref mutation was performed.
- Only tracked delta: `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`, 30 insertions / 1 replaced line.
- Runtime exact SHA/tree: `a5d4258312c979024865ee704da2d632ca5b2730` / `f74b016ea837f8148db4a602c972073a226ed177`, clean.
- Normal vendor source remains `34eac0041b0891e9011966b39bcbd26053fde5bc`; lock SHA256 `320d278366bc344aad35f3564845d9b62d9cc5f2e000a8a4cc6b6fea508d6cd2`.
- C0 contract SHA256: `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.
- Existing readonly `p4-v2-http-nodes` row SHA256: `fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`.

## Source/contract classification

Read PLAN §3 P4, C0 §§1,3,5,7, actual21332 log and independent0837 handoff/source evidence. C0 §1 lines 130–154 requires conservative scope reads for free transforms, distinguishes `records.commands` exact captures from the provider-only normalized `steps[].dependencies` undo index, and preserves input evaluation boundaries. C0 §5 lines 1628ff requires these step dependencies in undo checks; §7 persists the same authoritative steps/history.

Production source agrees:

- `commit_session.py:212–240`: public `commit(fn)` re-evaluates the function at the pinned input; omitted batch reads force atomic mode and add each step's timeline scope read.
- `_recording.py:91–120`: command `dependencies` starts empty; `dependency(key, kind, pin)` adds external exact pinned dependencies. A plain note `doc.patch` makes no such dependency call. Its actual note observations remain in command `reads`/`writes`, and its bindings remain in command `bindings`.
- `_doc_patch.py:417–434`: previous operands become sequential reads; normalized physical bindings are provider facts. Its binding's empty dependency list is separate again from the command and step arrays.
- `commands.py:213–278`: `CommitPatch.before` captures step declarations separately, restores inherited reads after exact native command claim validation, and preserves generated records.
- `_commit_patch.py:258–310,393–491`: timeline reads capture all three physical images; the step union contains the timeline scope plus the guarded canonical parent note field. Atomic fallback persists `commit.atomic` input bindings with the exact base pair, evaluated head, step ID and ordinal.
- `_step_undo.py:115–127`: selected undo dependencies come from authoritative recorded steps, not only command external-pin dependencies.
- `commit.py:1124–1139` and `_commit_preview.py:7–26` forward the authoritative records. Runtime `timeline_commit_auth.py:725–774` authenticates step read unions, atomic scope coverage and physical binding boundaries; `timeline_commit_store.py` validates/stores/exposes those same steps and commands in history.

Thus line 313 confused two different dependency schemas. The repair asserts the exact note write and exact empty command selections/created/external dependencies; full independent `expected_plan.records` equality continues to check **all** command arrays, including reads/bindings/derived writes. It additionally asserts the complete expected authoritative step with the exact timeline scope and canonical guarded field dependency, all three atomic physical images, and the exact input boundary pair/head/step/ordinal/phase. Existing patch/nonempty/scope checks remain as well.

`_expected_plan` remains unchanged: it opens the authenticated peer revision/publication pair and independently executes the submitted retry. No expected records are taken from the success response. Earlier request/base/idempotency/conflict/canonical/receipt/publisher/provider/compiler assertions and downstream restart/open/readback/outbox/history assertions are unchanged. No new undo operation was added to this conflict/rerun node; existing neighboring P4 undo coverage is unchanged and was only collected/typechecked as applicable, not behaviorally run.

## Exact commands and results

All commands ran from `/home/user/work/wt/ap2-P4-rerun-dependencies-sol-0844`. Private scratch is `/tmp/w-4c7397fa20`, named by the assigned worker's existing `tmpdir` pointer file. No shared dependency/cache writes.

```bash
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /home/user/work/venv-app2-native/bin/python -m pytest -q --collect-only -m integration -o cache_dir=/tmp/w-4c7397fa20/pytest-cache tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document
```

PASS, exit 0, exactly 1 test collected. Existing warning: unknown pytest config `timeout`.

```bash
timeout 45s /root/.local/bin/ruff check --config pyproject.toml --no-cache tests/editing_conformance/test_p4_note_rerun_v2_runtime.py tests/editing_conformance/test_p4_ten_note_v2_runtime.py
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /root/.local/bin/mypy --config-file pyproject.toml --platform linux --no-incremental --cache-dir /tmp/w-4c7397fa20/mypy-cache tests/editing_conformance/test_p4_note_rerun_v2_runtime.py tests/editing_conformance/test_p4_ten_note_v2_runtime.py
timeout 45s env PYTHONPYCACHEPREFIX=/tmp/w-4c7397fa20/pycache /home/user/work/venv-app2-native/bin/python -m py_compile tests/editing_conformance/test_p4_note_rerun_v2_runtime.py tests/editing_conformance/test_p4_ten_note_v2_runtime.py
git diff --check
timeout 45s env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-app2-native/bin/python scripts/vendor_lock.py check runtime.lock.json
```

PASS, each exit 0. Ruff all checks passed; Mypy no issues in 2 files (three existing untyped-function notes); compile/diff clean; vendor check `ok runtime.lock.json`.

```bash
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /home/user/work/venv-app2-native/bin/python /tmp/w-4c7397fa20/offline_controls.py
timeout 45s env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583 /home/user/work/venv-app2-native/bin/python /tmp/w-4c7397fa20/preflight.py
git diff --stat
git diff -- tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
git status --short
```

PASS, final exits 0. Preflight checks exact Runtime SHA/tree/clean state, actual module origins, normal vendor, readonly service row and one-file scope; computes candidate identity without Git writes. Runtime modules resolve inside the exact checkout; client modules resolve inside this worktree.

Offline witness directly executes the actual provider engine from an in-memory peer-note closure with all ten notes and the shared physical child, then executes the real test's history/capture assertion AST block only. It never runs the original HTTP body or replaces transport. Independent expected-plan data is fixed before tampering. All 32 negative controls pass:

- Seven command array alterations: writes, reads, selections, bindings, created, dependencies, derived_writes.
- Eight step alterations: missing scope, wrong scope root/path, missing field, wrong field state/root, wrong canonical patch path and wrong ordinal.
- Seven atomic-binding alterations: missing binding, wrong physical root/path, stale base revision/publication, wrong evaluated head and wrong input phase.
- Five actual provider refusals: wrong/absent previous guards and wrong note return `previous_value_mismatch`; timeline write root and wrong clip return `invalid_edit_command`.
- Removing the submitted closure read yields the engine's narrower parent fallback, which the exact original-case oracle refuses.
- Four actual Runtime annotation refusals return `invalid_records`: missing timeline scope, wrong scope root, stale base boundary, wrong patch-binding path. The unmodified plan passes Runtime authentication first.

Exploratory scratch-only setup initially found `tmpdir` was a pointer file rather than a directory; no file was replaced. The extended Runtime witness initially caught the wrong exception type (`ProtocolError`); Runtime correctly raised `CommitRejected`. Correcting the private witness handler produced the final PASS above. Neither issue required a tracked-source change.

## Limits and handoff

No live HTTP/body/socket/browser/service/full/build/request-test run; no original-node behavioral result credited. No product, fixture, generated, pin, lock, package, ops or shared install change; no files deleted; no tracked reports. No decisions were changed and no product defect is established by the investigated failure.

Recommended next step: independent Luna source/negative-control review, then manager-owned **one changed-evidence original node** using the existing readonly service route. Commit message names P4; harness owns the commit SHA.
