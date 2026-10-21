# AP2 M2 selected explicit-copy-return final review — 0954

## Decision

**APPROVE the exact `96629aa9` runner bytes for this retention hunk.** The
0941 HOLD is resolved. This review did not modify the runner, App source,
spec, helper, pin, selector, budget, dependency, or test.

Reviewed bytes:

```text
immutable 0927 source:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-copy-failure-explicit-return-0948/artifacts/source-0927-run-owned-selected-final95.sh
SHA-256 ff79ff6f32d248989b6227790cebbe34c1ffd4711b8b3dc90c0708fe6e7a8c8e

0948 corrected runner:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-copy-failure-explicit-return-0948/artifacts/run-owned-selected-final95.sh
SHA-256 96629aa9dbb00c6bb7ad23591a98229e56e6a6c0184a2ac254e2b825174707c9
```

The exact forward diff has four retention-only hunks and 34 changed lines
(18 corrected lines added, 16 old lines removed). The 0948 report's “17
removed and 17 added” split is an accounting error; it does not describe an
extra source change.

## Review findings

`retain_failure_evidence` is called as the condition of `if retain_failure_evidence ...` in `cleanup`, so shell `errexit` cannot be relied on inside it. The corrected bytes explicitly return from every relevant failure path:

- `copy_bounded`: source-file check, `wc -c` size read, size limit, and `cp`;
- durable-root creation, mode setting, child-log copy, and browser-output directory creation;
- each independent DOM, error-context, and trace copy;
- identity-file write, manifest-generation subshell, and nonempty `SHA256SUMS` check.

Each `*_retained=true` assignment follows its guarded copy. Therefore a
failed copy returns before its retained flag, identity, or manifest can be
written. Cleanup still removes the temporary run root and reports visible
`selected failure retention FAILED status=1`; the original child status is
preserved when retention succeeds. The independent trace/context behavior
and no-standalone-DOM behavior remain intact.

The unchanged source, destination, allowlist, pin, argv, graph, credential,
child-status, and cleanup guards remain byte-identical outside the retention
hunk. The retained allowlist remains `child.log`,
`browser-output/{dom.html,error-context.md,trace.zip}`, `identity.txt`, and
`SHA256SUMS`.

## Proof seam and controls

The bounded proof uses `SELECTED_FINAL95_MODE=run` and the runner's existing
`SELECTED_FINAL95_LAUNCH_STUB` seam. In `run_actual`, source/graph/spec,
destination, authority, and selected-contract checks occur before the stub
invocation; the stub replaces only the child command. No direct call to
`retain_failure_evidence` was used and validation was not stubbed. The
fixture emits trace plus error-context and exits 17, without DOM.

Reused controls:

- immutable old `ff79ff6f` RED: the deterministic error-context copy failure
  continued under conditional-function errexit semantics, set
  `error_context_retained=true`, and produced a manifest that passed
  `sha256sum -c` despite the missing context file;
- corrected `96629aa9` GREEN: the same failure produced visible retention
  failure status 1; the durable packet contained only `child.log`, with no
  `identity.txt` or `SHA256SUMS`;
- corrected successful partial-packet control: exit 17, trace/context/child
  log plus identity and manifest retained, `sha256sum -c` passed, and
  `dom_retained=false`.

`phase=BODY` and `body_started=1` in these packets are launch/output-phase
metadata only. They are not evidence that P1/P2, page or DOM setup, selected
assertions, or the original behavior ran.

Owned control/helper byte identities:

```text
fixture-failure-trace-context-only.sh 868fd91644ce38fed98511848436c1b92b21ba22a2026be4aa0e6cf3377c4fb5
bin/cp                                  95f8ad94ec768c04fdfea6defab4e91b596fcab585db5830de8ebd21f5c26de0
normal014-source-common.sh              96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109
normal014-parent-media-central.sh       1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
run-central-selected-p1.sh              a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f
```

## Checks run

```text
sh -n source-0927-run-owned-selected-final95.sh                 PASS
sh -n run-owned-selected-final95.sh                             PASS
(cd red-old-copy-failure-evidence && sha256sum -c SHA256SUMS)   PASS
(cd green-new-success-control && sha256sum -c SHA256SUMS)       PASS
worktree status                                                  CLEAN
```

No browser, build, daemon, socket, actual selected test, full suite,
installation, or service submission was run. No new tests were added.

## Next steps

This artifact approval does not authorize selected execution. The HOME
phase-order fixture and eventual data-only current-source binding remain
separate pending steps, as required by the plan.
