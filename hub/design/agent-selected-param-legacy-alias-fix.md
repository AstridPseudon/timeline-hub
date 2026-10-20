# Restored original selected PARAM legacy-alias positive

Completed on `/home/user/work/wt/agt-m2-authority-legacy-alias-positive`. No product, provider, public S2, generated client or runtime.lock changes; no Git mutation, integration edit, install, shared dependency mutation, socket/browser run, full-suite request or push.

## Gap and rule

Read `PLAN.md` and `design/agent-selected-param-authority-provider.md`. The original positive failed during setup because a new first PARAM had no accepted selected-source history. Normal explicit set-element clears ignored `element_ref`, destroying this regression's alias scenario. That cleanup meaning is unchanged.

New PARAM requires prior accepted selected-source authority. A genuinely accepted complete PARAM from before enforcement remains historical proof; a newly executed PARAM cannot bootstrap an arbitrary admitted pin. Incomplete pre-snapshot records are exercised only at the original detached inverse-compatibility boundary, not claimed as native current authority. Automatic copy inheritance remains a separate fail-closed gap. Empty PARAM remains syntactically invalid S2. No rule change or orchestrator decision was needed.

## Implementation and fixture boundary

- Restored `tests/sdk/test_timeline_selected_schema.py::test_inverse_of_older_param_record_uses_only_selected_identity` using portable reads of authentic old accepted history. Original row equality (including opaque params and both aliases), inverse and exact selected-object-only read assertions remain. Added explicit checks that selected `elementRef` and ignored `element_ref` name different genuine admitted revisions.
- Kept the original test's dependency/binding projection to the pre-snapshot shape. This alteration exists only in the detached in-memory copy; the underlying backup and native accepted history are untouched. The test does not fabricate or freshly submit an accepted PARAM.
- Added a 34,299-byte ZIP with a normal authenticated Runtime backup, fixture-only operator key and unmodified exported history/closures/inputs/request/result. Runtime's normal admission, provider and commit path generated all accepted facts. Reused the old native admission fixture and Runtime's `backup` / `restore_backup` helpers. No SQL writes, Prepared provider, validator replacement or bypass.
- Added a reproducible bounded generator and fixture README, plus a JSON-only fixture reader. Generator checks the old provider and frozen Runtime service source hashes.
- Added one native companion: restore authenticated backup, register new provider, compare all five native history entries exactly, recover exact ledger retry, refuse 16 under retained max10 despite the ignored max20 alias, undo to the complete original row, redo to the complete accepted document, then accept a new authorized PARAM preserving aliases and opaque params. Every observed object read names only the selected revision's object. Pack source/build directories from fixture generation no longer exist.

## Frozen source identities

| Role | Commit | Tree |
| --- | --- | --- |
| Old Agent, normal acceptance producer | `ce363f6d6d60e504dbd4d79803c2d6299f648ade` | `78af007de1d7c5a59f86fffacd9823de355cd260` |
| New Agent provider, unchanged by this fix | `654da69321b73d7d23fb4b9e689c1c1dcb2334cf` | `d35d0a36e4bc1f0a33f278a1bd798e4e857ec557` |
| Real Runtime used for old acceptance and new native qualification | `b748ae723b51c6d578ba7a393209ce37d6e2b0c3` | `1711b198be7f693f11ee4640eb0922ec0d0da952` |

Both source checkouts were private `git archive` exports, never moving worktrees. Runtime and Agent client report contract `0.2.13`, schema digest `8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`; runtime.lock's normal producer remains `2c4ac180c2220bdad966bc01e95ad230e99ce26a`. The new test/helper/fixture changes are uncommitted for the harness; no final commit SHA is claimed.

## Exact commands and results

All commands ran in the assigned worktree. Shared Python dependencies were read-only. No bytecode or pytest/ruff caches were enabled. Native tests use in-process RuntimeService; no sockets or browsers.

Before removing the original strict xfail marker:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --runxfail tests/sdk/test_timeline_selected_schema.py::test_inverse_of_older_param_record_uses_only_selected_identity
```

Exit 0: **1 passed in 1.24s**. The marker was removed only after this real positive pass.

Final parameter/history/conformance lane:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider_scalar.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_recipe_occurrence_duplicate.py tests/editing_conformance/test_recipe_clip_scalar_fields.py
```

Exit 0: **447 passed in 86.60s**; no xfail, refusal conversion or weakened test. This includes the entire original 446-pass/one-xfail lane and selected-history positives/negatives.

Final frozen real Runtime lane:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-authority-legacy-alias-positive/runtime-source /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/sdk/test_timeline_selected_schema_runtime.py
```

Exit 0: **27 passed in 38.06s** (all original 26 plus the new historical companion). Preserves real max10 versus later max20 admission, source/build removal, restart, original ledger retry and undo/redo cases. The new companion also passed alone: **1 passed in 1.82s**.

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_selected_schema_runtime.py tests/helpers/selected_param_legacy.py tests/sdk/fixtures/selected-param-legacy/generate.py
git diff --check
```

Both exit 0; Ruff: **All checks passed!** One initial import-order lint finding in the new generator was corrected before final checks.

Fixture capture command (exit 0), using the private immutable archives:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-authority-legacy-alias-positive/runtime-source PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-authority-legacy-alias-positive/old-agent /home/user/work/venv-agent/bin/python tests/sdk/fixtures/selected-param-legacy/generate.py tests/sdk/fixtures/selected-param-legacy/accepted.zip
```

The final generator, including frozen source hash checks, was run again successfully with the same command except destination `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-authority-legacy-alias-positive/regenerated.zip`. This independent regeneration did not replace the qualified fixture. Both temporary source archives and this regeneration output were removed after verification; regenerate them to repeat these commands.

## Coordination, limits and next steps

Read the independent review's available test-log summaries (150 passed / 1 xfailed, native 26 passed); no report/decision file was present when checked. Wrote `notes/review-boundary.md` in this worker's own directory for read-only coordination. No other worker's tree was edited. No independent provider bug was identified, and no approval to change S2 selection semantics was sought or needed.

Nothing blocked. Full suites, browser/App outbox behavior, automatic copy-source inheritance and accepted empty PARAM are unverified/out of scope. Recommend orchestrator/independent reviewer inspect the detached projection versus untouched native boundary, then harness-commit and qualify integration as appropriate. This unit restores the original positive without claiming the separate known gaps closed.

Fixture SHA256: `79f881f95ce13338ee8cd5490529c43a55523819792eed682160a9042770dc56`.
