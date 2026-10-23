# R1 sequential parent clip mirror installation

Worker: `agt-R1-sequential-mirror-0811`. Agent base: `e49a6e76b3ab363e312c55b313714af1f845f54b`. Runtime inspected/imported: `a5d4258312c979024865ee704da2d632ca5b2730`. Worktree: `/home/user/work/wt/agt-R1-sequential-mirror-0811`. Product result is ready for independent review and home-owned merge; no Git writes were performed.

## Result and callable source

`astrid/sdk/timeline/_doc_patch.py:232` adds three lines inside existing `Closure.install`: after assigning a native `parent/clip:<id>` site, call the existing `Recording.compile_mirrors()`. The recorder synchronizes the config mirror and retains its existing derived-write facts before the next operand reads or validates the bundle. Its initial `mirrored_clips` eligibility gate remains unchanged. There is no second executor, reordered user input, suppressed validation, schema change, or alternate caller.

Production path exercised: `astrid.sdk.timeline.commands.execute` → registered `doc.patch` handler `astrid.sdk.timeline._doc_patch.patch` → `Closure.install` → `Recording.compile_mirrors`. Provider tests call `create_runtime_commit_service().commit` with the existing `DetachedPort` and immutable `DetachedRealm` harness. The provider still calls its final candidate validation and document conversion before acceptance. The detached harness supplies only Runtime ABI exceptions/metadata; it is not a live Runtime store/HTTP proof.

Exact callable imports verified by supplemental probe:

```text
execute: /home/user/work/wt/agt-R1-sequential-mirror-0811/astrid/sdk/timeline/commands.py
provider: /home/user/work/wt/agt-R1-sequential-mirror-0811/astrid/sdk/timeline/commit.py
Runtime auth: /home/user/work/runtime/runtime_protocol/timeline_commit_auth.py
```

Only product edit: `astrid/sdk/timeline/_doc_patch.py` (+3 lines). New main-suite regression: `tests/editing_conformance/test_doc_patch_mirrors.py` (183 lines, 13 tests). No existing tests or fixtures changed.

The new regression uses the existing complete `document_fixture()` (two mirrored parent clips, shared child images, registry/media manifest, opaque/app/null data) and adds an authored output filename to that fixture in test memory. It does not replace the selected clip with a stripped-down row. It covers both `clips/id:...` and `config/clips/id:...`, output before/after clip changes, repeated hold operands observing their own earlier value, absent → null → absent label changes, exact caller input retention, exact provider/direct execution records and steps, normalized sequential physical effects, declared field/collection dependencies, derived mirror writes, unselected-row retention, unchanged children/manifest, accepted history, and exact leaf-change undo back to the original document. Separate insert cases retain the new right row's original app payload and allocation fact and verify the complete resulting parent. Negative cases retain malformed initial mirrors, wrong previous value, wrong list order, wrong declared read, and stale same-field conflict with unchanged head/history/document on refusal. Existing suites cover the wider alias, original-base/replay, ABA, undo, and binding guards without modification.

## Diagnosis consumed and scope decisions

Read PLAN §3 R1, C0 request/guard/effect contract and board header, the full source-derived `handoff-ap2-P1-first-split-conflict-sol-0747.md`, and the available independent `handoff-ap2-P1-first-split-diagnosis-review-0802.md` under `$ORCH/design`. The independent review confirms the timing defect. Its precision correction is retained: the causal methods match frozen/current sources, but all of `_doc_patch.py` is not AST-identical because `Closure.__init__` gained `source_bundles`.

Chosen seam: use the existing recorder after successful native parent clip installation, rather than adding aggregate authored mirror writes or changing guards. This preserves authored write ranges, physical bindings, sequential effects, and the recorder's existing distinction between authored writes and derived storage mirrors. It also avoids broadening a leaf edit into authored intent over unrelated rows. Other commands still use the existing command-end compilation.

Initial contradictory mirrors continue to fail during the existing document/closure validation (`AuthoringBundleError: parent clips and config.clips disagree`); the new test asserts that exact existing refusal and unchanged input. `validate_payload` itself is unchanged.

## Final tests: exact commands and results

Commands below ran from the worker worktree. No full suite or test-service request was made. Per-test timeout was explicitly 45 seconds. Bytecode and pytest caches were disabled; Ruff/Mypy caches were private under the worker's configured tmpdir target `/tmp/w-7886052a6e`.

Requested targeted run, exit **0**, **219 passed in 15.45s**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/editing_conformance/test_doc_patch_v2.py tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/editing_conformance/test_recording_clear.py tests/editing_conformance/test_doc_patch_mirrors.py
```

Standalone final new regression, exit **0**, **13 passed in 2.32s**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_doc_patch_mirrors.py
```

Collection was checked separately, exit **0**, **219 tests collected in 1.31s**, with the requested command plus `--collect-only` before the filenames. The compact repeated collection command below also exited **0** and confirmed per-file counts:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -qq -o addopts= -p no:cacheprovider --timeout=45 --collect-only tests/editing_conformance/test_doc_patch_v2.py tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/editing_conformance/test_recording_clear.py tests/editing_conformance/test_doc_patch_mirrors.py
```

| File | Collected |
| --- | ---: |
| `tests/editing_conformance/test_doc_patch_v2.py` | 102 |
| `tests/sdk/test_p1_doc_patch_provider.py` | 24 |
| `tests/sdk/test_p1_doc_patch_requests.py` | 12 |
| `tests/editing_conformance/test_recording_clear.py` | 68 |
| `tests/editing_conformance/test_doc_patch_mirrors.py` | 13 |
| Total | 219 |

Lint/type/artifact checks, all exit **0**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-7886052a6e/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_doc_patch.py tests/editing_conformance/test_doc_patch_mirrors.py
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-7886052a6e/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-7886052a6e/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Exact summaries: scoped Ruff `All checks passed!`; `Ruff findings: current=2149 baseline=2149`; `✓ ruff baseline (no lint regression)`; `Mypy findings: current=1912 baseline=1912`; `ok runtime.lock.json`; `artifacts.json is current`; diff check empty. Neither budget nor baseline was changed. Vendor check verified local locked bytes; no producer-pin change was attempted.

Supplemental, non-main-suite annotation-authentication probe, exit **0**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/w-7886052a6e/auth_probe.py
```

Exact final output: `Real Runtime annotation authentication passed: 8 prepared candidates`. This imports the real `runtime_protocol.timeline_commit_auth.validate`, obtains prepared candidates through the unchanged production provider and detached port, and validates them against the original document and complete request. Cases are 2 aliases × 2 output orders × insert present/absent. The normal test harness ABI fixture is restored before the actual Runtime authenticator runs. It does not open a Runtime realm, run a live writer, or replace Runtime acceptance/authorization.

## Pre-existing inverse limitation found; no broader repair made

An exploratory split-insert + leaf-write + output test executed successfully after this timing fix, then its undo refused `inverse_conflict` at `['config', 'clips']`. Investigation found that the unchanged base has the same failure when the same operands use output-first order (which already executes on the base). Reversal restores native leaf values while the aggregate config-list authored write still sees the final derived mirror. This limitation predates this patch; it is not treated as a passing undo scenario.

Exact proof command, exit **0** with the expected diagnostic:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/w-7886052a6e/base_inverse_probe.py
```

The scratch probe obtains only original `Closure.install` through read-only `git show HEAD:astrid/sdk/timeline/_doc_patch.py` and AST-compiles that original method in process. It invokes the existing production provider and existing detached harness. Output: `Unchanged base output-first split: accepted`, followed by `http_status=409`, `code=conflict`, `details.status=conflict`, `reason=inverse_conflict`, `path=['config', 'clips']`, `message='original authored guard changed'`. The mirror expected source hold 2, while the actual config mirror retained hold 1.5. No source file was reverted or changed for this probe. It is a source-derived test harness control, not a replay of the lost P1 realm.

The final main-suite regression keeps full successful execution assertions for insert cases, and separately asserts successful exact undo for the leaf-only transaction this timing change repairs. No formerly passing test was rewritten, removed, skipped or marked xfail. The new exploratory failing insertion-undo expectation was outside the existing supported inverse harness behavior, so it is reported here for R2 ownership rather than encoded as expected refusal or addressed through an unauthorized inverse rewrite.

Exploratory test-run record (not counted as final green evidence):

- Before product repair, the standalone new-file command without `--tb=short` returned **6 failed, 3 passed in 2.33s**. It reproduced `identity_conflict` for output-last and previous-value mismatch through the config alias. Other failures were initial test setup/assertion issues (unmatched execution-boundary metadata, initial-document exception class) and the stale case being rejected before it could reach the expected stale guard.
- After the repair and boundary/exception fixes, the same command returned **4 failed, 5 passed in 2.21s** because the new expected effect assertion incorrectly assumed an aggregate diff; authoritative effects correctly retained sequential submitted changes.
- After correcting that new assertion, the same command returned **4 failed, 5 passed in 3.13s**, all at the pre-existing split-insert undo limitation.
- Isolated command with `--tb=short` and `-k 'False-path0'` returned **1 failed, 8 deselected in 1.88s**, locating that inverse guard at `inverse.py:648`.
- The first scoped Ruff run after removing an unused exception use reported **1 F401** in the new test; the unused import was removed and final scoped/baseline Ruff passed.
- An initial ad hoc base-method probe exited **1** because its manually constructed ABI shim omitted Runtime `platform`; the durable probe above uses the same preservation as the normal fixture and exited **0**. This was tooling setup, not a product failure.

## Contract, limits and handoff

C0 is retained unchanged: request API version/scope/base pair/commands/label/full steps (id, label, intent, tags, command ordinals, patch, reads), merge, request reads, idempotency key, dry-run, source/rationale/group; full `{data, receipt}` results; accepted/merged and authentic historical rebased; head/document/records/dependencies/effects/history/undo steps; required preview `would_status`; conflict reason/head and invalid code/path/hint/suggested command. No client, schema, pin, generated artifact, hydration, G5/V4, App/Proof fixture/source, dependency, or authentication source changed. No operands were reordered in production; both orders are test parameters only.

This is a bounded provider repair and main-suite proof. The original live P1 realm/request/trace is unavailable; no original replay, original P1 success, H3 GO, App provenance correction, split-insert undo success, browser/HTTP chain, lost ACK/restart, or full-suite qualification is claimed. Source-derived witnesses in the prior handoffs retain their original limits. No full 4249, original P1, P4 HTTP, native14, crash24, browser, or duplicate full run was requested.

No block remains for independent review of this narrow result. Recommended next steps: Luna independently reviews the three-line recorder timing change and the 13 regressions, home owns commit/merge and integrated targeted proof, R2 owner investigates the pre-existing aggregate-list/leaf undo guard with this probe, and Proof alone schedules the original P1 rerun after the separate App provenance correction is ready. No decision in PLAN was overridden.
