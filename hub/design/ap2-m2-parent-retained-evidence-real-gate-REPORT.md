# AP2 M2 parent retained-evidence real gate

## Result

The App source candidate was verified before central submission as the exact
requested tree:

- HEAD: `d4c60b271d43df1512477cdbe2cf78dddf3a72e6`
- tree: `dea180c32cb49873215bd15b638d9fc8016ec008`
- worktree: clean

I added the uniquely named central-suite wrapper at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/run-parent-manual-drop-evidence.sh`.
It hard-fails on source drift, narrows the normal014 driver to the one mounted
manual-drop test, inserts the pre-build one-test collection, and retains the
trace, UI error context, redacted browser facts, runner tail, and source
identity outside the disposable run root. The shared normal014 driver supplies
the settled private014 / Agent `3c4f` / Runtime `202` / producer `a0` / artifact
`f021` / schema `6ba` / Composition13 graph guards.

## Central result

Exactly one named request was submitted:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-retained-evidence-real-gate ap2-m2-parent-retained-evidence-real-gate) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Run ID: `ap2-m2-parent-retained-evidence-real-gate-ap2-m2-parent-retained-evidence-real-gate-1020222027-10398`

Result: **FAIL, exit 1, 2s, before test execution.** The central
`test-run` failed at its cache lookup because
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/cache`
did not exist. The result log is empty; no pre-build collection, hosted build,
browser, localhost/socket, or App assertion ran. Therefore there is no first
visible native/drop/refusal fact, attempt history, accepted history, or browser
evidence to claim. No rerun was made because the brief requires one result.

## Validation and limits

- Source HEAD/tree and clean-state checks: **passed** before submission.
- Central suite registration: **present**, with an absolute wrapper path.
- No local wrapper/browser/full-suite run: intentionally not run.
- No product, dependency, pin, schema, API, or adoption change.

The gate is blocked by the central test-service cache-directory failure. The
service owner should restore/create its expected `tests/cache` directory and
run a fresh, explicitly authorized single gate against the same source tree.
