# D17 source-authority final guard return

Status: ready for independent review; author checks passed. No integration merge is claimed.

## Change and cause

Base: `a01e9d806e08ee4ff6d35bad18dddafa1f09f862`, tree `645de16949982723f67db58be204611cf0a5bb95` (includes producer-fixture `014c09848` and stale-envelope `0b5da66ca`). Recovered only the three allowed source-authority files using `git show 2d95afef817748c86b463d3cfb260b1275851053:<path>`. No old ancestry was introduced. Prospective cumulative tree, computed from Git blob/tree hashing without writing Git objects or index: `6c69c3dc47822fffbaf27cd63815d2895155ffaa`.

F2 cause: `revision_closure()` has a nullable inferred result, and the source-authority store method accessed `document.get()` without a presence guard. The production method now reads the parent and returns the document only inside `if document is not None`. Otherwise it raises the existing structured `dependency_unavailable` refusal before candidate persistence. There are no casts, ignores, annotations to conceal the issue, or diagnostic-budget changes. The guard is a two-line net change over the recovered store method.

Added one behavioral regression through `RuntimeService` and the real request port: an authenticated accepted source publication whose closure becomes unavailable at the store boundary must produce a structured refusal, preserve the destination head, and add no history row. This is injected with a test-local monkeypatch returning `None` only for the source timeline; it does not claim a newly reproduced database corruption path.

F1 remains intact: `timeline_commit_port.py` is byte-for-byte identical to `2d95afef8`. The focused test retains the entire donor file as an unchanged 332-line prefix, including all 12 donor cases. The original `36f247869` five test functions/eight cases and donor nine functions/12 cases have identical ASTs, including decorators and assertions. No existing tests were edited, weakened, skipped, or deleted.

Exact five-field source reference, same-project/different-active-timeline scope, authenticated caller access, historical accepted publication/revision pairing, parent digest, complete closure capture, per-pin `raw_media_info()` capture, source document capture, and preacceptance revalidation are preserved. Exact historical source after head advancement passes. No interface changed, so `handoff-runtime-D17-input-interface-0842.md` was left untouched. Agent exclusively owns semantic copy/order/sharing/fresh IDs/undo/idempotency/archive cleanup.

## Test commands and results

Working directory for current-tree commands: `/home/user/work/wt/rt-D17-authority-sol-0910`. The actual worker TMPDIR is `/tmp/w-82668ba2bb`; the worker `tmpdir` file is only a pointer.

```bash
TMPDIR=/tmp/w-82668ba2bb PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py
```

Exit 0: **119 passed in 28.63s**. Log: `evidence/acceptance.log`.

```bash
TMPDIR=/tmp/w-82668ba2bb PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_port.py
```

Exit 0: **67 passed in 10.94s**. The current producer fixture is fixed and qualified by this run. Log: `evidence/port.log`.

```bash
/root/.local/bin/ruff check --no-cache tests/test_timeline_source_duplicate_authority.py
git diff --check
```

Both exit 0. New-test Ruff: all checks passed.

Full-resolver original snapshot prepared without checkout or Git writes:

```bash
mkdir -p /tmp/w-82668ba2bb/original-eb13
git archive eb13b2051d4d30a4d8b7df8878bb7451701eab5a | tar -x -C /tmp/w-82668ba2bb/original-eb13
/root/.local/bin/ruff check --no-cache --output-format=json runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py > /tmp/w-82668ba2bb/ruff-current.json
/root/.local/bin/pyright --outputjson runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py > /tmp/w-82668ba2bb/pyright-current.json
```

Then, with working directory `/tmp/w-82668ba2bb/original-eb13`:

```bash
/root/.local/bin/ruff check --no-cache --output-format=json runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py > /tmp/w-82668ba2bb/ruff-original.json
/root/.local/bin/pyright --outputjson runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py > /tmp/w-82668ba2bb/pyright-original.json
```

Each whole-file checker exits 1 for existing diagnostics: **Ruff 21 original / 21 current; Pyright 79 original / 79 current**. Counter comparison of normalized path, rule/code, severity, full message, columns and affected source text finds **zero added and zero removed diagnostic identities**, rather than comparing only totals. The F2 optional-document diagnostic is gone. All four raw JSON outputs are saved in `evidence/`.

An inline Python audit (recorded verbatim in the worker tool log) used `py_compile.compile(..., cfile=<actual TMPDIR>/<filename>c, doraise=True)` on the three allowed files: **3 passed**, with bytecode only in the private TMPDIR. It also compared the inherited frozen-77 list against `eb13`: **77 compared / 0 changed**; compared original eight and donor 12 test-case ASTs: **all preserved**; verified donor port bytes and test-file prefix; and computed the prospective cumulative tree. Results and SHA-256 source hashes: `evidence/verification.txt`. Frozen list: `evidence/frozen77.txt`. Complete three-file patch: `evidence/cumulative.patch`.

## Preserved contract and limits

The production caller continues through RuntimeDaemon / normal WorkspaceClient `commitTimeline` to the authenticated Runtime store/provider. The v2 carrier is unchanged: `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, semantic/`doc.patch` commands, label, steps (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), merge `fields|atomic`, reads, dry-run, source, rationale, group ID and stable idempotency.

Accepted/merged and authentic historical rebased replies preserve full data and receipt: document/head/revision/digests/records/effects/bindings/dependencies/history/undo_steps. Conflict reason/head, invalid code/path/hint/suggested_command, and receipt-free preview with `would_status` accepted|merged are unchanged. The narrow D17 tests do not independently qualify every v2 feature.

Only the three allowed files differ from the integration base. No schema/client/pin/artifact/config or authentication-module edits; frozen tuple remains unchanged from the base. No shared dependency files were modified. No full suite, Agent suite, browser/socket/HTTP-body/P5 suite, or interrupted accidental-dot run was requested or resumed. H3 remains NO-GO; V4 remains CUT. No git commit/merge/rebase/checkout/push or Git-internal writes were performed.

Decision: use an explicit positive non-None branch, with the existing refusal outside it, to validate the document domain before parent access while retaining the existing untyped refusal helper. No plan or interface decision changed. Nothing is blocked. Recommended next step: independent review of this exact cumulative tree, then the orchestrator's merge queue.
