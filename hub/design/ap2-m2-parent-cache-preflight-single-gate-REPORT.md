# ap2-m2-parent-cache-preflight-single-gate

## Result

Blocked after the requested test-service environment repair. No product source
was changed and no guard or test runner was weakened.

## Repair and preflight

- Created only `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/cache`.
- Validated it as a normal `755` directory before the request.
- Validated the absolute retained-evidence driver, `normal014-app-central.sh`,
  `normal014-source-common.sh`, request/wait helpers, package manifest, and
  shared `node_modules` paths before the request.
- Target worktree was clean at `d4c60b271d43df1512477cdbe2cf78dddf3a72e6`,
  tree `dea180c32cb49873215bd15b638d9fc8016ec008`.

## One central run

Command:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-cache-preflight-single-gate ap2-m2-parent-retained-evidence-real-gate)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$(basename "$R")"
```

Result: fail, exit 1, request
`ap2-m2-parent-cache-preflight-single-gate-ap2-m2-parent-retained-evidence-real-gate-1020222631-15183`.
The service snapshot retained the exact tree, but the evidence driver failed its
static `expected_app_head=d4c60b271...` check because the service runs a new
`commit-tree` snapshot commit. The run stopped before the wrapper created a
browser run root; `log.txt` and `runner.log` were empty, and no trace, console,
request, refusal summary, or product assertions exist.

## Blocker / next step

The absolute driver must either accept the service snapshot by tree identity or
the test service must provide a snapshot preserving the requested commit HEAD.
That decision belongs to the driver/test-service owner; I did not alter either
guard or submit another run.

No full, local browser, socket, dependency, adoption, or source tests were run.
