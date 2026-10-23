# agt-G5-native-fixture-sol-1552

PASS: bounded test-only correction of the five known native-port oracles on the same qualified join. No product defect demonstrated. P1 remains NO-GO; no integration merge requested or performed.

## Source and scope

Worktree: `/home/user/work/wt/agt-G5-native-fixture-sol-1552`, branch `tl/agt-G5-native-fixture-sol-1552`.
Base: `7f6497db4bf63a10e6bb35c255d12affe08c1514` (`tl/agt-G5-native-qualified-join-1545` source join), containing normal CLI durable undo `cc8be25d4ad46fae3f7d0889aaee88f85ab6a9c6`.
Runtime dependency source: `/home/user/work/wt/rt-pin-9ce4242b`, HEAD `9ce4242bc01f100bab9efc51032a73985cefb2b2`; shared dependency environments were read-only.

Only `test_cli_native_sheet.py` and `test_verbs_working_copy.py` changed, within the four-file allowlist. AST comparison verifies only the three intended test bodies and the `shlex` import changed. The other two allowed files are byte-identical. No fixture/global helper, product source, schema, client, pin, archive, lock, dependency, vendor, or artifact change; no new product worktree files.

## Causal trace and correction

- `tests/sdk/test_timeline_sync.py::Generated.commit_timeline` executes the real `commands.execute` against `bundles[body[base_revision_id]]`, builds the canonical document and receipt, and stores `plan.bundle`. Its ordinal allocator gives r1/pub1 for the first accepted edit and r2/pub2 for undo.
- `tests/packs/timeline/test_cli_commit_move.py::_install_history` starts from the actual generated bootstrap head, then stamps retained accepted bundles with their accepted revision/publication pair when authenticated history is listed. This existing fixture behavior is unchanged.
- `TimelineSession._bundle` authenticates the exact state base via `store.fetch_bundle`; the latter hydrates the publication pair from history. `TimelineSession.undo` flushes an ordinary timeline.inverse command. Provider `commit.py::bundle_from_document` opens immutable Runtime documents and its execution service calls the same `commands.execute`; `commands.py::execute` deep-copies its input closure before applying authored writes. Undo retains its input transport base while restoring authored data.
- Trim acceptance therefore retains r0/pub0, including the publication wrongly removed from its old expectation. The test now asserts the outgoing pair and actual accepted bundle pair independently, then compares the entire accepted bundle to the original preview bundle.
- Undo runs at r1/pub1. Both trim and all three rational frontends assert the outgoing undo pair and the actual undo-result pair exactly. The rational case separately checks the actual accepted history and accepted input bundle pair. The expected restored closure is an independent deep copy of the full original with only the two known transport fields set to r1/pub1. Nothing is popped or copied from actual into expected; content digest, base payload, mappings, authored/opaque/null/absence values, and the rest of the full bundle equality remain checked. Existing per-occurrence/sibling/capture/receipt assertions remain.
- Draft checkout/status navigation uses `cli_common.checkout_summary` / `status_text` and `cli._document_edit_commands`. The test independently spells the normal commit module, exact saved draft path, and `--idempotency-key timeline-edit-1`; it checks the entire checkout commit line and exact clean/dirty status next-step lines. No product hint generator is called to construct the expected command.
- The 1545 detached-duration fix is unchanged: it sources the actual generated head, stamps the retained fixture and checkout, and re-renders. Its legacy writer failguard, target selector, hold=2, submitted base pair, source, and sheet-byte assertions are preserved and the test passes.

No decision was changed. No publish restoration or CLI-to-SDK substitution was introduced. All other authored/canonical/no-write/durable undo/receipt/history/force-local/retired-route assertions are unchanged. Independent no-weakening review remains the next manager action.

## Verification commands and results

Commands ran from the worktree above. The five known cases were executed exactly once in the corrected positive run, together with the previously passing retained-duration regression:

```sh
set -o pipefail
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-native-fixture-sol-1552/tmpdir PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9ce4242b PYTHONPATH=.:/home/user/work/wt/rt-pin-9ce4242b /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 tests/packs/timeline/test_cli_native_sheet.py::test_cli_trim_clear_and_params_are_one_captured_batch tests/packs/timeline/test_cli_native_sheet.py::test_rational_explicit_occurrence_move_is_lossless_across_native_frontends tests/packs/timeline/test_verbs_working_copy.py::test_draft_flow_checkout_edit_status_discard tests/packs/timeline/test_cli_native_sheet.py::test_original_detached_apply_uses_retained_duration_target | tee /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-native-fixture-sol-1552/tmpdir/targeted.log
```

Pytest: **6 passed in 9.91s**, including trim (1), rational CLI/Python/sheet (3), draft navigation (1), retained duration (1). The surrounding pipeline exited 1 solely because the harness's `tmpdir` is a text file containing `/tmp/w-49189d5f04`, not a directory; tee could not create its log. The completed pytest output was captured by the execution tool. No tests were repeated to repair that logging issue. Subsequent scratch/caches use the resolved directory.

Private strict pair mutation controls:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/w-49189d5f04/run_mutation_controls.py
```

Result: **PASS, 4/4 corruptions rejected**. The private plugin wraps Generated.commit_timeline after acceptance, corrupting either revision_id or publication_id on r1 (trim acceptance) or r2 (rational Python undo). Each run exits 1 with one intentional assertion failure at the new exact pair assertion; the driver exits 0 only when every corruption is caught. No skip/xfail or product test mutation was saved. Driver environments: `TMPDIR=/tmp/w-49189d5f04 PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9ce4242b PYTHONPATH=.:/home/user/work/wt/rt-pin-9ce4242b:/tmp/w-49189d5f04`, plus each MUTATION_REVISION / MUTATION_KEY below.

- `MUTATION_REVISION=r1 MUTATION_KEY=revision_id /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 -p base_pair_mutation --tb=short tests/packs/timeline/test_cli_native_sheet.py::test_cli_trim_clear_and_params_are_one_captured_batch`: intentional FAIL (exit 1), exact assertion caught; `/tmp/w-49189d5f04/mutation-r1-revision_id.log`.
- `MUTATION_REVISION=r1 MUTATION_KEY=publication_id /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 -p base_pair_mutation --tb=short tests/packs/timeline/test_cli_native_sheet.py::test_cli_trim_clear_and_params_are_one_captured_batch`: intentional FAIL (exit 1), exact assertion caught; `/tmp/w-49189d5f04/mutation-r1-publication_id.log`.
- `MUTATION_REVISION=r2 MUTATION_KEY=revision_id /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 -p base_pair_mutation --tb=short 'tests/packs/timeline/test_cli_native_sheet.py::test_rational_explicit_occurrence_move_is_lossless_across_native_frontends[python]'`: intentional FAIL (exit 1), exact assertion caught; `/tmp/w-49189d5f04/mutation-r2-revision_id.log`.
- `MUTATION_REVISION=r2 MUTATION_KEY=publication_id /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 -p base_pair_mutation --tb=short 'tests/packs/timeline/test_cli_native_sheet.py::test_rational_explicit_occurrence_move_is_lossless_across_native_frontends[python]'`: intentional FAIL (exit 1), exact assertion caught; `/tmp/w-49189d5f04/mutation-r2-publication_id.log`.

Scoped checks:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check --no-cache tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_commit_trim.py tests/packs/timeline/test_cli_native_sheet.py tests/packs/timeline/test_verbs_working_copy.py
TMPDIR=/tmp/w-49189d5f04 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --cache-dir=/tmp/w-49189d5f04/mypy --follow-imports=silent --hide-error-context --no-color-output --no-pretty --show-error-codes tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_commit_trim.py tests/packs/timeline/test_cli_native_sheet.py tests/packs/timeline/test_verbs_working_copy.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/w-49189d5f04/check_scope.py
git diff --check
```

Ruff: **PASS, all checks passed**. Mypy: **PASS, no issues in 4 source files**. AST/file-scope, four-file Python compile, unchanged fixtures/guards, untracked artifact check: **PASS**. Diff whitespace check: **PASS**.

No final 87-case execution: the brief permits that only if a global fixture/helper changes; none changed, as verified by AST comparison. The inherited 82 PASS/5 FAIL cohort plus this corrected five-case pass is not represented as a fresh 87 PASS result. No full/P1-P4/native14/V4/browser/live/socket suite, daemon tooling, Git mutation, or integration testing was performed. `pytest --help` exposes timeout support but no `--net` flag; tests used the existing local transport fixtures and `--timeout=30`.

## Exact four-file blob scope

| File | Baseline blob | Final blob |
| --- | --- | --- |
| `tests/packs/timeline/test_cli_commit_move.py` | `48d56160d77c8bc737a9d3ee0198135d272e61bc` | `48d56160d77c8bc737a9d3ee0198135d272e61bc` |
| `tests/packs/timeline/test_cli_commit_trim.py` | `966227db8797d7421d592f04d8f508eab517d8b5` | `966227db8797d7421d592f04d8f508eab517d8b5` |
| `tests/packs/timeline/test_cli_native_sheet.py` | `3f2481c711e49e9c9905932b5f9569e74422c1e7` | `6602ef1abe4dd658507069acf6f39128b6d32613` |
| `tests/packs/timeline/test_verbs_working_copy.py` | `c68598826b49d973182356d485c4b1f1670eba86` | `6fd04fa7445cf75a9ee0f9aec794918f673ea2e2` |

Final SHA-256 values:

- `tests/packs/timeline/test_cli_commit_move.py`: `da4024e0c999bb33861b72e78a4d48185d7f981a0299b4de6dee5932fada8fa1`
- `tests/packs/timeline/test_cli_commit_trim.py`: `137787402ff3fe7de40042ce2a8a44eb71240f1c3d3bee9190b050b848a1e157`
- `tests/packs/timeline/test_cli_native_sheet.py`: `8f552ed4f528efbaa60343fe1798982a4ae8d5bdd0bc315f08023693dd33a9cd`
- `tests/packs/timeline/test_verbs_working_copy.py`: `abf2d6b6e831d3708da9b028a216a24c33097cd8c9a6b731ee8b20a35bc73afe`

Full baseline/final SHA-256 and blob IDs: `/tmp/w-49189d5f04/source-hashes.json` (generated with read-only `git show HEAD:<path>`, `git rev-parse HEAD:<path>`, `git hash-object <path>` and hashlib.sha256). Base/runtime HEADs checked with `git rev-parse HEAD` and `git -C /home/user/work/wt/rt-pin-9ce4242b rev-parse HEAD`.

## Limits and next step

No blocking product issue or permission/tool refusal encountered. The temporary tee path error is described above. Independent review must assess the oracle corrections and no-weakening claim before any queue decision; the manager owns that review and the queue. P1 remains NO-GO. The separate 1548 normal-commit product work was neither modified nor qualified here. No integration merge or merge request. Commit message names this task; the harness owns committing. Reports and private controls are outside the product worktree.
