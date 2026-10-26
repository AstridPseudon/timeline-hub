# D141ii writers15 protected return review: FAIL

Reviewed `3638da72332dee5ffccacb704c9ac3c794b7c959` / tree `6983046d907b9ec8f745a27a178b0413a66a2a45`, parent `c61c56d2f2b926febde4dad67d83d114790766ab`, against restored base `14ccf296f3768fcde857047b263834e4a6bbe52e` and Runtime `95d98f038320d5d46bd679ac000ab3e15825c935`.

## Finite findings

### F5 remains open: actor diagnostics do not use the supported authenticated caller

Both current parameter cases pass at execution level (`tests/packs/timeline/test_verbs_working_copy.py:595-627`), but the test constructs `SimpleNamespace` request data and a fabricated `Refusal`, then calls `_document_error(parsed, Refusal())` directly at lines 602-619. It does not invoke `commit_document`, the CLI handler, `TimelineSession`, the generated `commit_timeline` contract, or a real authenticated `WorkspaceClientError`/Runtime conflict. Thus the editor actor and generic actor strings asserted at lines 623-627 are private-presenter output only; propagation from the supported commit caller is unproved for both actor parameters.

The supported production route is `astrid/packs/timeline/cli.py:2239-2243` → `astrid/packs/timeline/cli_native.py:174-205`, where the exception is caught at lines 196-198 and passed to `_document_error`. The current CAS test at `tests/packs/timeline/test_cli_status_publish.py:412-438` exercises the real commit route but checks only a generic conflict code/human prefix, not either actor-specific diagnostic. This is a caller-coverage failure, not a pytest failure.

### F7: exact mypy remains an environment failure

The exact command failed before target checking:

`/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports astrid/packs/timeline/cli_native.py`

It reported `/home/user/work/venv-agent/lib/python3.13/site-packages/numpy/__init__.pyi:737`, where a `type` statement requires Python 3.12+, while the repository configuration selects Python 3.11 and the interpreter is Python 3.13.16. The narrow explicit-target fallback with only `--python-version 3.12` passed. This is recorded as `FAIL_ENVIRONMENT`; it is not source-level green evidence and does not silently replace the mandated check.

## Closure checks for prior F1–F4 and F6

- F1 is closed at `test_cli_status_publish.py:412-438`: both JSON and human parameter cases assert refusal, unchanged bytes/history, return code 1, and exactly one additional transport call.
- F2 is closed at `test_cli_status_publish.py:29-62`: accepted revision equals the canonical document and Runtime entry revision; receipt publication identity and idempotency are checked; parser `--force` exits 2 without a transport call.
- F3 is closed across the supported current reply contract: human summary, bounded/non-JSON output, and edits/cuts-before-commit are asserted at `test_cli_status_publish.py:381-410`; the exact five-key envelope and receipt-result identity (excluding the documented presentation fields) are asserted at lines 35-49. The changed C0 reply shape is recorded in `handoff.md`.
- F4 is closed at `test_cli_status_publish.py:441-455`: explicit `status == "unchanged"`, null receipt, unchanged bytes/history, and zero mutation calls.
- F6 is closed with the approved commit-route shape at `tests/v10/test_timelines_create.py:517-570` and following assertions: shell/idempotency, `timeline.init` plus patch commands, exact init args/default output, full config/registry/occurrences/empty lists, bootstrap/base pair, history, and recorded step reads are asserted. The old top-level legacy result and endpoint are intentionally changed and enumerated in `handoff.md`, not claimed as literal old-wire equality.

## Execution interpretation

The exact author/current return set reproduced `22 passed`; the prior review's seven distinct neighboring controls were also included in a 29-selector union and all passed. These green counts do not close F5 because its protected predicate is about the actual supported caller, and do not turn F7's environment error into a pass.
