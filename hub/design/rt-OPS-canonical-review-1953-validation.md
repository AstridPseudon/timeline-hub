# Canonical OPS check validation

Verdict: **PASS** for the requested independent source/unit review. The
Agent-only genuine whole-maker run remains **NOTRUN** and is not implied by
this result.

## Exact command and result

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python ops-child-custody/tests/canonical_check.py .
exit 0
```

The complete unaltered script stdout is in `canonical-check.log`; captured
stderr is empty and the captured exit code is `0`. The canonical script hash is
`d8e47bd0b98990d614ad755f69cd21e74fa72bbe55231c10df020d498e7ed0bc` both
before and after execution.

## Control results

- Governing `/root/.local/bin/ruff` reported `ruff 0.16.8`, ran the explicit three-file scope, and passed.
- Repository Ruff reported `ruff 0.12.0`, ran the `ops-child-custody/tests` scope, and passed.
- The exact existing unittest invocation ran **64 tests** and passed.
- Private-cache `py_compile` passed for the three canonical source paths.
- Source diff and canonical-script whitespace checks passed; the latter returned the expected no-index status 1 with no diagnostics.
- Historical maker EOF diff returned the expected status 2 with exactly the two preserved frozen diagnostics; these are separately reported and are not authored failures.
- The negative check-only census returned structured exit 2, enumerated the expected missing inputs, and reported `mutating_setup_started=false`, `maker_started=false`, `store_initialized=false`, and `git_mutated=false`.
- The actual worktree was clean. The final commit/tree were independently resolved as `b855b8a082153a12ca3a59383c4a08387b201bdd` / `ffb9c5ee22c6d7b138ab2bfc1dbd83188d9fc2fb`.

## Findings and scope

All seven 1903/1909 findings are mapped as fixed by the canonical run: Ruff
coverage, complete malformed/missing role/path census, required source-role
coverage, ambient interpreter/command census, and TMPDIR write census. The
actual final runner/source/support/manifest/maker hashes and modes match the
settled 607535 tree; the only changed path is the new canonical script.

No actual Store or Git fixture preparation, maker invocation, package
acquisition, production child, E2E, network/socket/browser/profile, collector,
ZIP, or D130 action was run. No full suite was requested. No review findings
remain.
