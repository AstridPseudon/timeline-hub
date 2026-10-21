# normal014 Playwright child-exit repair

## Result

Fixed the App2-owned normal014 wrapper path in
`design/normal014-app-central.sh`. The Playwright/`flock` command is now run
under a narrow `set +e` window, its status is captured immediately in
`normal014_playwright_exit_status`, and that value is logged before the
structured verdict check and the common EXIT cleanup trap. The final wrapper
status is initialized from that captured value and cannot be replaced by a
successful post-step. The normal selector and structured required-case guard
remain intact.

The old loss-prone handoff was the conditional `if flock ... Playwright; then
... else ... fi`: the child was executed as a conditional command, with
errexit suppressed, and its status was only handed onward through that
conditional before verdict and cleanup. The new unconditional
invocation/capture makes the exact handoff explicit. The common trap still
receives and returns its incoming status; it was not changed to delete failure
evidence. The retained historical 4657 directory has no wrapper trace, so it
cannot distinguish whether that old handoff or the central finalizer performed
the original swallow; the fresh negative proves the repaired suite path does
not swallow it.

I also corrected the final95 source guard in `normal014-source-common.sh` from
the stale Runtime SHA `2c4ac180c2220bdad966bc01e95ad230e99ce26a` to the
final95 lock's `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`. This was required so
the negative test reaches the planted spec rather than being refused by source
binding. The normal source-binding and structured verdict checks remain
enabled.

## Negative proof

Private spec:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-suite-child-exit-root-fix-0154/normal014-negative.spec.ts`

It throws from the Playwright test body. The wrapper copies it only into the
disposable overlay as `tests/e2e/local/three-products.spec.ts`; no checked-in
App source, real bootstrap case, or passed neighbor was modified or run. In
private mode the command also names that exact file, so the central run had
exactly one test:

```text
Running 1 test using 1 worker
normal014 planted failure reached Playwright test body
1 failed
normal014 Playwright child exit: 1
```

Central result:

`ap2-m2-bootstrap-current95-create-observer-cause-0115-normal014-integration-e2e-gate5-negative-single-1021021120-3198`

`status=fail`, `exit=1`; the result summary reports `1 failed`. Thus the
planted Playwright child, wrapper, and central result all returned nonzero.
The log also shows the required summary guard refusing the absent real-case
summary, as expected defense in depth.

## Exact commands and checks

The exact registered normal command remains:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=bootstrap \
  bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh run "$PWD"
```

The narrow registered negative command was run through the central service:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-current95-create-observer-cause-0115 \
  normal014-integration-e2e-gate5-negative-single)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-bootstrap-current95-create-observer-cause-0115-normal014-integration-e2e-gate5-negative-single-1021021120-3198 100
```

The central log passed the final95 locked graph/source/artifact checks and
hosted build before the one browser test. Shell syntax also passed:

```sh
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
```

No full suite, real bootstrap case, passed neighbor, local server/browser
run, `bin/test-run` change, product-code change, dependency install, or shared
dependency mutation was performed.

## Changed artifact hashes

```text
8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e  design/normal014-app-central.sh
c76c48fa5f73b72ada6ba8fa857f229778e2ed6948568e77000bf4c1a8490270  design/normal014-source-common.sh
2c2c9be1d0fd3bc5ad6e85fda5bc19f7be88d9c7748363274acdce0668ad24bb  tests/suites.conf
10db990835b172c58a0d3a7a43ee8c00dead5b00cb6cc198ef8984edd9221b51  normal014-negative.spec.ts
```

The assigned App worktree is clean; orchestration files above are the only
changed artifacts. Recommended next step is independent review, then a new
normal gate request if the orchestrator authorizes it. The historical 4657
false-green result was not edited or relabeled.
